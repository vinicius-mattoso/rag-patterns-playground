"""Compatibility layer for Neo4j graph integration."""

from __future__ import annotations

try:
    from langchain_neo4j import Neo4jGraph
except ImportError:  # pragma: no cover
    from langchain_community.graphs.neo4j_graph import Neo4jGraph


__all__ = ["Neo4jGraph"]
