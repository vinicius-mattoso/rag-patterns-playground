"""Tests for FAISS index construction and persistence."""

from pathlib import Path

from src.index_builder import build_or_load_index
from src.loaders import load_documents
from tests.helpers import DeterministicEmbeddings


def test_build_index_persists_faiss_files(tmp_path: Path) -> None:
    data_dir = tmp_path / "raw"
    data_dir.mkdir()
    (data_dir / "sample.txt").write_text(
        "Rio has beaches, samba, football, and landmarks.",
        encoding="utf-8",
    )

    documents = load_documents(data_dir, chunk_size=80, chunk_overlap=10)
    index_dir = tmp_path / "index"

    vectorstore = build_or_load_index(documents, DeterministicEmbeddings(), index_dir)

    assert vectorstore is not None
    assert (index_dir / "index.faiss").exists()
    assert (index_dir / "index.pkl").exists()


def test_load_existing_index_without_rebuilding(tmp_path: Path) -> None:
    data_dir = tmp_path / "raw"
    data_dir.mkdir()
    (data_dir / "sample.txt").write_text(
        "Copacabana is one of the best-known beaches in Rio de Janeiro.",
        encoding="utf-8",
    )
    embeddings = DeterministicEmbeddings()
    index_dir = tmp_path / "index"

    first_documents = load_documents(data_dir, chunk_size=80, chunk_overlap=10)
    build_or_load_index(first_documents, embeddings, index_dir)

    loaded_index = build_or_load_index([], embeddings, index_dir)

    results = loaded_index.similarity_search("Which beach is in Rio?", k=1)
    assert len(results) == 1
    assert "Copacabana" in results[0].page_content
