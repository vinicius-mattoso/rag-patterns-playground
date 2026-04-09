"""Provider factories for chat models and embeddings."""

from __future__ import annotations

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.config import AppConfig


def get_llm(config: AppConfig) -> BaseChatModel:
    """Create a chat model for the configured provider."""
    if config.llm_provider == "openai":
        return ChatOpenAI(model=config.llm_model)
    if config.llm_provider == "ollama":
        return ChatOllama(model=config.llm_model, base_url=config.ollama_base_url)
    raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")


def get_embeddings(config: AppConfig) -> Embeddings:
    """Create an embeddings client for the configured provider."""
    if config.embedding_provider == "openai":
        return OpenAIEmbeddings(model=config.embedding_model)
    if config.embedding_provider == "ollama":
        return OllamaEmbeddings(model=config.embedding_model, base_url=config.ollama_base_url)
    raise ValueError(f"Unsupported embedding provider: {config.embedding_provider}")
