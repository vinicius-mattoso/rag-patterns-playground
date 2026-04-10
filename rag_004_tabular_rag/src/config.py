"""Configuration loading for the Graph RAG module."""

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
    support_limit: int
    neighborhood_depth: int


def _resolve_path(raw_value: str, default_relative: str) -> Path:
    candidate = Path(raw_value or default_relative)
    if candidate.is_absolute():
        return candidate
    return MODULE_ROOT / candidate


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
        support_limit=int(os.getenv("SUPPORT_LIMIT", "6")),
        neighborhood_depth=int(os.getenv("NEIGHBORHOOD_DEPTH", "2")),
    )
