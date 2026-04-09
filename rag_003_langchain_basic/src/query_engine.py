"""Retrieval and answer generation for the LangChain RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_community.vectorstores import FAISS


@dataclass(frozen=True)
class QueryResult:
    """Structured query response containing answer text and retrieved sources."""

    answer: str
    sources: list[dict[str, Any]]


PROMPT = ChatPromptTemplate.from_template(
    """You are answering questions using only the supplied context.
If the context is insufficient, say that explicitly.

Question:
{question}

Context:
{context}
"""
)


def _format_context(documents: list[Document]) -> str:
    return "\n\n".join(document.page_content for document in documents)


def _serialize_sources(documents: list[Document]) -> list[dict[str, Any]]:
    return [
        {
            "source": document.metadata.get("source", "unknown"),
            "chunk_id": document.metadata.get("chunk_id", "n/a"),
            "content": document.page_content,
        }
        for document in documents
    ]


def query_index(
    vectorstore: FAISS,
    llm: BaseChatModel | Runnable[Any, Any],
    question: str,
    top_k: int = 3,
) -> QueryResult:
    """Retrieve documents and produce an answer with source snippets."""
    documents = vectorstore.similarity_search(question, k=top_k)
    chain = PROMPT | llm | StrOutputParser()
    answer = chain.invoke(
        {
            "question": question,
            "context": _format_context(documents),
        }
    )
    return QueryResult(answer=answer, sources=_serialize_sources(documents))
