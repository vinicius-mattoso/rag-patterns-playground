"""Graph answer synthesis helpers."""

from __future__ import annotations

from typing import Protocol

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable


class GraphAnswerChain(Protocol):
    """Minimal protocol for graph answer synthesis."""

    def invoke(self, values: dict[str, str]) -> str:
        """Generate an answer from graph context."""


PROMPT = ChatPromptTemplate.from_template(
    """You answer questions using only the supplied knowledge graph triples.
If the answer is directly supported, answer concisely and explicitly.
If the triples do not contain enough information, say that you don't know.

Question:
{question}

Knowledge Graph Triples:
{context}
"""
)


def build_graph_qa_chain(llm: BaseLanguageModel) -> GraphAnswerChain:
    """Build a simple grounded QA chain over graph triples."""
    chain: RunnableSerializable[dict[str, str], str] = PROMPT | llm | StrOutputParser()
    return chain
