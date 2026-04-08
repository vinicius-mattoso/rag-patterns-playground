"""
Module for loading documents from disk.
"""
import os
from typing import List

def load_documents(directory: str) -> List[str]:
    """
    Load text documents from a specified directory.

    Args:
        directory (str): Path to the directory containing text files.

    Returns:
        List[str]: List of document contents as strings.
    """
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                documents.append(file.read())
    return documents