"""Build or load the ontology-guided Neo4j knowledge graph from local text."""

from __future__ import annotations

import re

from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_core.language_models import BaseLanguageModel
from langchain_experimental.graph_transformers import LLMGraphTransformer

from src.config import AppConfig
from src.neo4j_store import clear_graph, connect_neo4j_graph, ensure_graph_ready, fetch_graph_counts
from src.schemas import GraphAssets, Ontology, SourceChunk


def _graph_has_documents(node_count: int, document_count: int) -> bool:
    return node_count > 0 and document_count > 0


def _normalize_key(raw_value: str) -> str:
    return "".join(character.lower() for character in raw_value if character.isalnum())


def _canonicalize_node_id(raw_id: str) -> str:
    cleaned = raw_id.strip()
    if re.fullmatch(r"[A-Za-z]{2,}-\d+", cleaned):
        prefix, suffix = cleaned.split("-", maxsplit=1)
        return f"{prefix.upper()}-{suffix}"
    return cleaned


def _canonicalize_node_type(raw_type: str, ontology: Ontology) -> str:
    if not raw_type:
        return "Entity"
    return ontology.entity_lookup.get(_normalize_key(raw_type), raw_type.strip().replace(" ", ""))


def _canonicalize_relationship_type(raw_type: str, ontology: Ontology) -> str:
    if not raw_type:
        return "RELATED_TO"
    normalized = ontology.relationship_lookup.get(_normalize_key(raw_type))
    if normalized:
        return normalized
    cleaned = raw_type.strip().replace("-", "_").replace(" ", "_")
    return cleaned.upper()


def _relationship_allowed(source_type: str, relationship_type: str, target_type: str, ontology: Ontology) -> bool:
    for spec in ontology.relationship_types:
        if spec.name != relationship_type:
            continue
        if source_type in spec.source_types and target_type in spec.target_types:
            return True
    return False


def _normalize_graph_document(graph_document: GraphDocument, ontology: Ontology) -> GraphDocument:
    node_by_key: dict[tuple[str, str], Node] = {}
    normalized_nodes: list[Node] = []

    for node in graph_document.nodes:
        canonical_type = _canonicalize_node_type(str(node.type), ontology)
        if canonical_type not in {item.name for item in ontology.entity_types}:
            continue
        canonical_id = _canonicalize_node_id(str(node.id))
        key = (canonical_type, canonical_id)
        if key not in node_by_key:
            node_by_key[key] = Node(id=canonical_id, type=canonical_type, properties=dict(node.properties))
            normalized_nodes.append(node_by_key[key])
        else:
            node_by_key[key].properties.update(dict(node.properties))

    normalized_relationships: list[Relationship] = []
    for relationship in graph_document.relationships:
        source_type = _canonicalize_node_type(str(relationship.source.type), ontology)
        target_type = _canonicalize_node_type(str(relationship.target.type), ontology)
        relationship_type = _canonicalize_relationship_type(str(relationship.type), ontology)
        if not _relationship_allowed(source_type, relationship_type, target_type, ontology):
            continue

        source_id = _canonicalize_node_id(str(relationship.source.id))
        target_id = _canonicalize_node_id(str(relationship.target.id))
        source_node = node_by_key.get((source_type, source_id))
        target_node = node_by_key.get((target_type, target_id))
        if source_node is None or target_node is None:
            continue

        normalized_relationships.append(
            Relationship(
                source=source_node,
                target=target_node,
                type=relationship_type,
                properties=dict(relationship.properties),
            )
        )

    return GraphDocument(nodes=normalized_nodes, relationships=normalized_relationships, source=graph_document.source)


def build_or_load_graph(
    config: AppConfig,
    llm: BaseLanguageModel,
    documents: tuple[SourceChunk, ...],
    ontology: Ontology,
) -> GraphAssets:
    """Build the ontology-guided graph in Neo4j if needed, otherwise reuse the persisted graph."""
    graph = connect_neo4j_graph(config)
    ensure_graph_ready(graph)
    print("[rag_008] Neo4j readiness check passed")

    node_count, relationship_count, document_count = fetch_graph_counts(graph)
    if config.rebuild_graph:
        clear_graph(graph)
        node_count = relationship_count = document_count = 0

    if not _graph_has_documents(node_count=node_count, document_count=document_count):
        print("[rag_008] no persisted graph detected, starting ontology-guided extraction and ingestion")
        transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=[item.name for item in ontology.entity_types],
            allowed_relationships=[item.name for item in ontology.relationship_types],
            strict_mode=config.strict_mode,
            node_properties=True,
        )

        graph_documents = []
        for source_chunk in documents:
            print(f"[rag_008] extracting graph chunk: {source_chunk.chunk_id}")
            converted = transformer.convert_to_graph_documents([source_chunk.document])
            graph_documents.extend(_normalize_graph_document(item, ontology=ontology) for item in converted)

        graph_documents = [item for item in graph_documents if item.nodes or item.relationships]
        if not graph_documents:
            raise RuntimeError("The ontology-guided graph extraction step produced no graph documents.")

        print(f"[rag_008] writing {len(graph_documents)} graph documents to Neo4j")
        graph.add_graph_documents(
            graph_documents,
            include_source=config.include_source_documents,
            baseEntityLabel=config.base_entity_label,
        )
        print("[rag_008] refreshing schema after ingestion")
        graph.refresh_schema()
        node_count, relationship_count, document_count = fetch_graph_counts(graph)
    else:
        print("[rag_008] using persisted Neo4j graph, skipping extraction")

    return GraphAssets(
        graph=graph,
        source_chunks=documents,
        node_count=node_count,
        relationship_count=relationship_count,
        document_count=document_count,
    )
