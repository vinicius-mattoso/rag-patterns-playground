"""
Module for managing vector storage using FAISS.
"""
import faiss
import numpy as np
import json
from typing import List

class VectorStore:
    def __init__(self, index_file: str, metadata_file: str):
        """
        Initialize the vector store.

        Args:
            index_file (str): Path to the FAISS index file.
            metadata_file (str): Path to the metadata JSON file.
        """
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.index = None
        self.metadata = {}

    def load(self):
        """Load the FAISS index and metadata from disk."""
        self.index = faiss.read_index(self.index_file)
        with open(self.metadata_file, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

    def save(self):
        """Save the FAISS index and metadata to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "w", encoding="utf-8") as file:
            json.dump(self.metadata, file)

    def add_vectors(self, vectors: List[List[float]], metadata: List[str]):
        """
        Add vectors and their metadata to the store.

        Args:
            vectors (List[List[float]]): List of vectors to add.
            metadata (List[str]): List of metadata strings corresponding to the vectors.
        """
        if self.index is None:
            self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors, dtype=np.float32))
        self.metadata.update({str(i): meta for i, meta in enumerate(metadata)})

    def query(self, vector: List[float], k: int = 5) -> List[str]:
        """
        Query the vector store for the nearest neighbors.

        Args:
            vector (List[float]): Query vector.
            k (int): Number of nearest neighbors to retrieve.

        Returns:
            List[str]: List of metadata for the nearest neighbors.
        """
        distances, indices = self.index.search(np.array([vector], dtype=np.float32), k)
        return [self.metadata[str(idx)] for idx in indices[0] if str(idx) in self.metadata]