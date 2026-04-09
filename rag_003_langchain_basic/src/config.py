"""Configuration loading for the LangChain RAG module."""

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
    index_path: Path
    llm_provider: str
    llm_model: str
    embedding_provider: str
    embedding_model: str
    ollama_base_url: str
    chunk_size: int
    chunk_overlap: int
    retrieval_k: int


def _resolve_path(raw_value: str, default_relative: str) -> Path:
    candidate = Path(raw_value or default_relative)
    if candidate.is_absolute():
        return candidate
    return MODULE_ROOT / candidate


def load_config() -> AppConfig:
    """Load and validate module configuration from a local `.env` file."""
    load_dotenv(MODULE_ROOT / ".env")

    return AppConfig(
        data_path=_resolve_path(os.getenv("DATA_PATH", "data/raw"), "data/raw"),
        index_path=_resolve_path(os.getenv("INDEX_PATH", "data/index"), "data/index"),
        llm_provider=os.getenv("LLM_PROVIDER", "openai").strip().lower(),
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini").strip(),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "openai").strip().lower(),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip(),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip(),
        chunk_size=int(os.getenv("CHUNK_SIZE", "600")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "120")),
        retrieval_k=int(os.getenv("RETRIEVAL_K", "3")),
    )
