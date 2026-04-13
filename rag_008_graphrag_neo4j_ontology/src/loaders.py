"""Load local text sources and split them into graph extraction chunks."""

from __future__ import annotations

from pathlib import Path
import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import AppConfig
from src.schemas import SourceChunk


SUPPORTED_EXTENSIONS = {".txt", ".md"}


def _build_chunk_id(source_name: str, index: int, content: str) -> str:
    digest = hashlib.sha1(content.encode("utf-8")).hexdigest()[:10]
    return f"{source_name}_chunk_{index}_{digest}"


def _load_file_documents(data_path: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(data_path.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={
                    "source_name": path.stem,
                    "source_path": str(path),
                    "source_type": path.suffix.lower().lstrip("."),
                },
            )
        )
    return documents


def _load_inline_documents(inline_texts: tuple[str, ...]) -> list[Document]:
    documents: list[Document] = []
    for index, text in enumerate(inline_texts, start=1):
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_name": f"inline_{index}",
                    "source_path": "",
                    "source_type": "inline",
                },
            )
        )
    return documents


def load_text_chunks(config: AppConfig) -> tuple[SourceChunk, ...]:
    """Load local text sources and split them into stable chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    raw_documents = _load_file_documents(config.data_path) + _load_inline_documents(config.inline_texts)
    if not raw_documents:
        raise ValueError(
            f"No supported text files were found in {config.data_path}. "
            "Add at least one .txt or .md source before running app_direct.py."
        )

    chunks: list[SourceChunk] = []
    for document in raw_documents:
        source_name = str(document.metadata["source_name"])
        source_path = str(document.metadata.get("source_path", ""))
        for index, chunk in enumerate(splitter.split_documents([document])):
            chunk_id = _build_chunk_id(source_name=source_name, index=index, content=chunk.page_content)
            chunk.metadata.update(
                {
                    "id": chunk_id,
                    "chunk_id": chunk_id,
                    "source_name": source_name,
                    "source_path": source_path,
                }
            )
            chunks.append(
                SourceChunk(
                    chunk_id=chunk_id,
                    source_name=source_name,
                    path=Path(source_path) if source_path else None,
                    document=chunk,
                )
            )
    return tuple(chunks)
