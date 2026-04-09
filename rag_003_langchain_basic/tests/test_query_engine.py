"""Tests for querying the LangChain RAG pipeline."""

from pathlib import Path

from langchain_core.runnables import RunnableLambda

from src.index_builder import build_or_load_index
from src.loaders import load_documents
from src.query_engine import QueryResult, query_index
from tests.helpers import DeterministicEmbeddings


def test_query_index_returns_answer_and_sources(tmp_path: Path) -> None:
    data_dir = tmp_path / "raw"
    data_dir.mkdir()
    (data_dir / "rio.txt").write_text(
        "The Christ the Redeemer statue and Sugarloaf Mountain are iconic attractions in Rio.",
        encoding="utf-8",
    )

    documents = load_documents(data_dir, chunk_size=120, chunk_overlap=20)
    vectorstore = build_or_load_index(documents, DeterministicEmbeddings(), tmp_path / "index")
    llm = RunnableLambda(
        lambda prompt_value: f"Answer generated from context: {prompt_value.to_string()[:80]}"
    )

    result = query_index(
        vectorstore=vectorstore,
        llm=llm,
        question="What attractions are mentioned?",
        top_k=1,
    )

    assert isinstance(result, QueryResult)
    assert "Answer generated from context" in result.answer
    assert len(result.sources) == 1
    assert "Christ the Redeemer" in result.sources[0]["content"]
