"""Compatibility layer for Neo4j graph QA chains."""

from __future__ import annotations

try:
    from langchain_neo4j import GraphCypherQAChain
except ImportError:  # pragma: no cover
    from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain


__all__ = ["GraphCypherQAChain"]
