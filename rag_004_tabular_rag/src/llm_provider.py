"""LLM provider abstraction for graph-based QA."""

from __future__ import annotations

from langchain_core.language_models import BaseLanguageModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from src.config import AppConfig


def get_llm(config: AppConfig) -> BaseLanguageModel:
    """Create the chat model used by the graph QA layer."""
    if config.llm_provider == "openai":
        return ChatOpenAI(model=config.llm_model)
    if config.llm_provider == "ollama":
        return ChatOllama(model=config.llm_model, base_url=config.ollama_base_url)
    raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")
