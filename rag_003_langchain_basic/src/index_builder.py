"""FAISS index construction and persistence."""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS


def build_or_load_index(
    documents: list[Document],
    embeddings: Embeddings,
    index_path: Path,
) -> FAISS:
    """Load a persisted FAISS index or build it from documents and persist it."""
    index_path.mkdir(parents=True, exist_ok=True)
    faiss_file = index_path / "index.faiss"
    pickle_file = index_path / "index.pkl"

    if faiss_file.exists() and pickle_file.exists():
        return FAISS.load_local(
            folder_path=str(index_path),
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )

    if not documents:
        raise ValueError("Cannot build a new index without documents.")

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(str(index_path))
    return vectorstore
