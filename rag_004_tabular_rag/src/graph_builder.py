"""Knowledge graph construction from CSV tables and ontology rules."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from langchain_community.graphs.networkx_graph import KnowledgeTriple, NetworkxEntityGraph
import networkx as nx

from src.schemas import GraphAssets, KnowledgeTripleView, LoadedTable, Ontology


def _safe_format(template: str, values: dict[str, Any]) -> str:
    normalized = {key: ("" if value != value else value) for key, value in values.items()}
    return template.format(**normalized).strip()


def build_knowledge_graph(
    tables: dict[str, LoadedTable],
    ontology: Ontology,
) -> GraphAssets:
    """Build the NetworkX and LangChain graph views from CSV data and ontology."""
    graph = nx.MultiDiGraph()
    entity_graph = NetworkxEntityGraph()
    triple_views: list[KnowledgeTripleView] = []
    node_text_index: dict[str, str] = {}
    node_lookup: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)

    for entity in ontology.entities:
        dataframe = tables[entity.table].dataframe
        for _, row in dataframe.iterrows():
            row_dict = row.to_dict()
            entity_id = str(row_dict[entity.id_column])
            node_name = _safe_format(entity.label_template, row_dict)
            description = _safe_format(entity.description_template, row_dict)
            attributes = {column: row_dict.get(column) for column in entity.attribute_columns}

            graph.add_node(
                node_name,
                entity_type=entity.entity_type,
                source_table=entity.table,
                entity_id=entity_id,
                description=description,
                color=entity.color,
                attributes=attributes,
            )
            node_lookup[(entity.table, entity.entity_type)][entity_id] = node_name
            node_text_index[node_name.lower()] = node_name

    for relationship in ontology.relationships:
        source_df = tables[relationship.source_table].dataframe
        for _, row in source_df.iterrows():
            row_dict = row.to_dict()
            source_key = str(row_dict[relationship.source_key_column])
            target_key = str(row_dict[relationship.target_key_column])

            source_name = node_lookup[(relationship.source_table, relationship.source_entity)].get(source_key)
            target_name = node_lookup[(relationship.target_table, relationship.target_entity)].get(target_key)
            if not source_name or not target_name:
                continue

            relation = _safe_format(relationship.relation_template, row_dict)
            graph.add_edge(
                source_name,
                target_name,
                relation=relation,
                relationship_name=relationship.name,
                source_table=relationship.source_table,
                row_snapshot=row_dict,
            )
            entity_graph.add_triple(KnowledgeTriple(source_name, relation, target_name))
            triple_views.append(
                KnowledgeTripleView(
                    subject=source_name,
                    relation=relation,
                    object_=target_name,
                    source_table=relationship.source_table,
                )
            )

    return GraphAssets(
        graph=graph,
        entity_graph=entity_graph,
        triple_views=tuple(triple_views),
        node_text_index=node_text_index,
    )
