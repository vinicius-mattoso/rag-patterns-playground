"""Neo4j connectivity and low-level graph storage helpers."""

from __future__ import annotations

import re

from src.config import AppConfig
from src.neo4j_compat import Neo4jGraph


def connect_neo4j_graph(config: AppConfig) -> Neo4jGraph:
    """Connect to Neo4j and load the current schema."""
    if not config.neo4j_password:
        raise ValueError("NEO4J_PASSWORD is required to connect to Neo4j.")

    print(f"[rag_007] connecting to Neo4j at {config.neo4j_uri} using database {config.neo4j_database}")
    try:
        graph = Neo4jGraph(
            url=config.neo4j_uri,
            username=config.neo4j_username,
            password=config.neo4j_password,
            database=config.neo4j_database,
            timeout=config.neo4j_timeout_seconds,
            enhanced_schema=config.neo4j_enhanced_schema,
            refresh_schema=False,
        )
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "The neo4j Python driver is required for rag_007_graphrag_neo4j. "
            "Install the dependencies from requirements.txt before running app_direct.py."
        ) from exc

    try:
        print("[rag_007] refreshing Neo4j schema")
        graph.refresh_schema()
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Neo4j schema refresh failed. Ensure the database is reachable and APOC is enabled "
            "for schema introspection."
        ) from exc
    print("[rag_007] Neo4j connection ready")
    return graph


def ensure_graph_ready(graph: Neo4jGraph) -> None:
    """Run a minimal readiness check against Neo4j."""
    graph.query("RETURN 1 AS ok")


def clear_graph(graph: Neo4jGraph) -> None:
    """Delete all nodes and relationships from the configured Neo4j database."""
    print("[rag_007] clearing existing Neo4j graph contents")
    graph.query("MATCH (n) DETACH DELETE n")


def fetch_graph_counts(graph: Neo4jGraph) -> tuple[int, int, int]:
    """Return node, relationship, and document counts for the current graph."""
    node_count = int(graph.query("MATCH (n) RETURN count(n) AS count")[0]["count"])
    relationship_count = int(graph.query("MATCH ()-[r]->() RETURN count(r) AS count")[0]["count"])
    document_count = int(graph.query("MATCH (d:Document) RETURN count(d) AS count")[0]["count"])
    print(
        f"[rag_007] graph counts: nodes={node_count}, "
        f"relationships={relationship_count}, documents={document_count}"
    )
    return node_count, relationship_count, document_count


def fetch_label_counts(graph: Neo4jGraph) -> list[dict]:
    """Return counts by node-label combination."""
    return list(
        graph.query(
            """
            MATCH (n)
            RETURN labels(n) AS labels, count(*) AS count
            ORDER BY count DESC, labels
            """
        )
    )


def fetch_relationship_counts(graph: Neo4jGraph) -> list[dict]:
    """Return counts by relationship type."""
    return list(
        graph.query(
            """
            MATCH ()-[r]->()
            RETURN type(r) AS type, count(*) AS count
            ORDER BY count DESC, type
            """
        )
    )


def fetch_sample_nodes(graph: Neo4jGraph, label: str, limit: int = 10) -> list[dict]:
    """Return sample nodes for a selected label."""
    safe_label = re.sub(r"[^A-Za-z0-9_]", "", label)
    if not safe_label:
        return []
    query = f"""
    MATCH (n:{safe_label})
    RETURN properties(n) AS properties
    LIMIT $limit
    """
    return list(graph.query(query, params={"limit": limit}))


def run_read_only_cypher(graph: Neo4jGraph, query: str, limit: int = 100) -> list[dict]:
    """Execute a read-only Cypher query with a lightweight safety gate."""
    normalized = query.strip().lower()
    forbidden_tokens = (
        "create ",
        "merge ",
        "delete ",
        "detach delete",
        "set ",
        "remove ",
        "drop ",
        "call dbms",
        "apoc.periodic",
    )
    if any(token in normalized for token in forbidden_tokens):
        raise ValueError("Only read-only Cypher is allowed in the Streamlit console.")

    limited_query = query.strip().rstrip(";")
    if " limit " not in normalized:
        limited_query = f"{limited_query}\nLIMIT {limit}"
    return list(graph.query(limited_query))
