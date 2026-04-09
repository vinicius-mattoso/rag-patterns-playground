# loaders.py
# Document loader for the RAG pipeline

import os
from llama_index.core import SimpleDirectoryReader

def load_documents(data_path):
    reader = SimpleDirectoryReader(data_path)
    return reader.load_data()