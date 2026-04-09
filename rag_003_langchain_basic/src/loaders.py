"""Document loading and chunking helpers."""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(
    data_path: Path,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    """Load local text files and split them into retrievable chunks."""
    loader = DirectoryLoader(
        str(data_path),
        glob="**/*",
        show_progress=False,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        silent_errors=False,
    )
    raw_documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunked_documents = splitter.split_documents(raw_documents)

    for chunk_id, document in enumerate(chunked_documents):
        document.metadata.setdefault("source", "unknown")
        document.metadata["chunk_id"] = chunk_id

    return chunked_documents
