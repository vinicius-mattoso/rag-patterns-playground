"""Schema definitions for ontology-guided Neo4j GraphRAG."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document

from src.neo4j_compat import Neo4jGraph


@dataclass(frozen=True)
class SourceChunk:
    """A local text chunk prepared for graph extraction."""

    chunk_id: str
    source_name: str
    path: Path | None
    document: Document


@dataclass(frozen=True)
class EntityTypeSpec:
    """Ontology directive for an allowed entity type."""

    name: str
    aliases: tuple[str, ...]
    id_patterns: tuple[str, ...]
    required_properties: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class RelationshipTypeSpec:
    """Ontology directive for an allowed relationship type."""

    name: str
    aliases: tuple[str, ...]
    source_types: tuple[str, ...]
    target_types: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class Ontology:
    """Loaded ontology metadata used to normalize extracted graph elements."""

    entity_types: tuple[EntityTypeSpec, ...]
    relationship_types: tuple[RelationshipTypeSpec, ...]
    entity_lookup: dict[str, str]
    relationship_lookup: dict[str, str]


@dataclass(frozen=True)
class GraphAssets:
    """Graph assets returned after ingestion or loading."""

    graph: Neo4jGraph
    source_chunks: tuple[SourceChunk, ...]
    node_count: int
    relationship_count: int
    document_count: int


@dataclass(frozen=True)
class GraphSupportRecord:
    """Structured context record returned from the graph query."""

    row_number: int
    payload: str


@dataclass(frozen=True)
class GraphQueryResult:
    """Final query result shown to the user."""

    answer: str
    generated_cypher: str
    context_records: tuple[GraphSupportRecord, ...]
    source_documents: tuple[str, ...]
