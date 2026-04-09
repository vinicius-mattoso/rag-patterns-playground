"""Shared test doubles."""

from langchain_core.embeddings import Embeddings


class DeterministicEmbeddings(Embeddings):
    """Offline embeddings implementation for repeatable tests."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    @staticmethod
    def _embed(text: str) -> list[float]:
        length = float(len(text))
        checksum = float(sum(ord(char) for char in text) % 997)
        vowels = float(sum(char.lower() in "aeiou" for char in text))
        return [length, checksum, vowels]
