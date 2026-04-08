"""
Module for retrieving relevant chunks from the vector store.
"""
from typing import List
from .vectorstore import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        """
        Initialize the retriever.

        Args:
            vector_store (VectorStore): The vector store instance.
        """
        self.vector_store = vector_store

    def retrieve(self, query_vector: List[float], top_k: int = 5) -> List[str]:
        """
        Retrieve the top-k relevant chunks for a query vector.

        Args:
            query_vector (List[float]): The query vector.
            top_k (int): Number of top results to retrieve.

        Returns:
            List[str]: List of relevant chunks.
        """
        return self.vector_store.query(query_vector, top_k)