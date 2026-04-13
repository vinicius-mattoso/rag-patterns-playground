"""Pipeline orchestration for Neo4j-backed GraphRAG."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_core.language_models import BaseLanguageModel

from src.config import AppConfig
from src.neo4j_compat import Neo4jGraph
from src.query_engine import build_query_chain, run_query
from src.schemas import GraphQueryResult


@dataclass(frozen=True)
class GraphPipeline:
    """Application-level bundle required for graph queries."""

    graph: Neo4jGraph
    chain: object
    config: AppConfig


def build_pipeline(config: AppConfig, llm: BaseLanguageModel, graph: Neo4jGraph) -> GraphPipeline:
    """Create the reusable Neo4j GraphRAG query pipeline."""
    chain = build_query_chain(config=config, llm=llm, graph=graph)
    return GraphPipeline(graph=graph, chain=chain, config=config)


def query_graph(question: str, pipeline: GraphPipeline, config: AppConfig) -> GraphQueryResult:
    """Run a natural-language question through the configured graph pipeline."""
    return run_query(
        chain=pipeline.chain,
        graph=pipeline.graph,
        question=question,
        context_limit=config.context_limit,
    )
