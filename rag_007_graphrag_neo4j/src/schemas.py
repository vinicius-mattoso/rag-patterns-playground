"""Schema definitions for Neo4j-backed GraphRAG."""

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
