"""Configuration loading for the ontology-guided Neo4j GraphRAG module."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


MODULE_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    """Normalized application settings loaded from environment variables."""

    data_path: Path
    ontology_path: Path
    graph_html_path: Path
    llm_provider: str
    llm_model: str
    ollama_base_url: str
    chunk_size: int
    chunk_overlap: int
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str
    neo4j_timeout_seconds: int
    neo4j_enhanced_schema: bool
    rebuild_graph: bool
    include_source_documents: bool
    base_entity_label: bool
    strict_mode: bool
    query_top_k: int
    context_limit: int
    visualization_limit: int
    inline_texts: tuple[str, ...]


def _resolve_path(raw_value: str, default_relative: str) -> Path:
    candidate = Path(raw_value or default_relative)
    if candidate.is_absolute():
        return candidate
    return MODULE_ROOT / candidate


def _parse_bool(raw_value: str | None, default: bool) -> bool:
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_csv_list(raw_value: str | None) -> tuple[str, ...]:
    if not raw_value:
        return ()
    return tuple(item.strip() for item in raw_value.split(",") if item.strip())


def load_config() -> AppConfig:
    """Load and normalize the module configuration from `.env`."""
    load_dotenv(MODULE_ROOT / ".env")

    return AppConfig(
        data_path=_resolve_path(os.getenv("DATA_PATH", "data/raw"), "data/raw"),
        ontology_path=_resolve_path(os.getenv("ONTOLOGY_PATH", "ontology.yaml"), "ontology.yaml"),
        graph_html_path=_resolve_path(
            os.getenv("GRAPH_HTML_PATH", "artifacts/knowledge_graph.html"),
            "artifacts/knowledge_graph.html",
        ),
        llm_provider=os.getenv("LLM_PROVIDER", "openai").strip().lower(),
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini").strip(),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip(),
        chunk_size=int(os.getenv("CHUNK_SIZE", "900")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "180")),
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687").strip(),
        neo4j_username=os.getenv("NEO4J_USERNAME", "neo4j").strip(),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "").strip(),
        neo4j_database=os.getenv("NEO4J_DATABASE", "neo4j").strip(),
        neo4j_timeout_seconds=int(os.getenv("NEO4J_TIMEOUT_SECONDS", "30")),
        neo4j_enhanced_schema=_parse_bool(os.getenv("NEO4J_ENHANCED_SCHEMA"), False),
        rebuild_graph=_parse_bool(os.getenv("REBUILD_GRAPH"), False),
        include_source_documents=_parse_bool(os.getenv("INCLUDE_SOURCE_DOCUMENTS"), True),
        base_entity_label=_parse_bool(os.getenv("BASE_ENTITY_LABEL"), True),
        strict_mode=_parse_bool(os.getenv("STRICT_MODE"), True),
        query_top_k=int(os.getenv("QUERY_TOP_K", "8")),
        context_limit=int(os.getenv("CONTEXT_LIMIT", "6")),
        visualization_limit=int(os.getenv("VISUALIZATION_LIMIT", "180")),
        inline_texts=_parse_csv_list(os.getenv("INLINE_TEXTS")),
    )
