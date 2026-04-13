"""Neo4j connectivity and low-level graph storage helpers."""

from __future__ import annotations

from src.config import AppConfig
from src.neo4j_compat import Neo4jGraph


def connect_neo4j_graph(config: AppConfig) -> Neo4jGraph:
    """Connect to Neo4j and load the current schema."""
    if not config.neo4j_password:
        raise ValueError("NEO4J_PASSWORD is required to connect to Neo4j.")

    print(f"[rag_008] connecting to Neo4j at {config.neo4j_uri} using database {config.neo4j_database}")
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
            "The neo4j Python driver is required for rag_008_graphrag_neo4j_ontology. "
            "Install the dependencies from requirements.txt before running app_direct.py."
        ) from exc

    try:
        print("[rag_008] refreshing Neo4j schema")
        graph.refresh_schema()
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Neo4j schema refresh failed. Ensure the database is reachable and APOC is enabled "
            "for schema introspection."
        ) from exc
    print("[rag_008] Neo4j connection ready")
    return graph


def ensure_graph_ready(graph: Neo4jGraph) -> None:
    """Run a minimal readiness check against Neo4j."""
    graph.query("RETURN 1 AS ok")


def clear_graph(graph: Neo4jGraph) -> None:
    """Delete all nodes and relationships from the configured Neo4j database."""
    print("[rag_008] clearing existing Neo4j graph contents")
    graph.query("MATCH (n) DETACH DELETE n")


def fetch_graph_counts(graph: Neo4jGraph) -> tuple[int, int, int]:
    """Return node, relationship, and document counts for the current graph."""
    node_count = int(graph.query("MATCH (n) RETURN count(n) AS count")[0]["count"])
    relationship_count = int(graph.query("MATCH ()-[r]->() RETURN count(r) AS count")[0]["count"])
    document_count = int(graph.query("MATCH (d:Document) RETURN count(d) AS count")[0]["count"])
    print(
        f"[rag_008] graph counts: nodes={node_count}, "
        f"relationships={relationship_count}, documents={document_count}"
    )
    return node_count, relationship_count, document_count
