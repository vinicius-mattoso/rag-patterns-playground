# index_builder.py
# Index builder for the RAG pipeline

import os
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage

def build_or_load_index(documents, index_path):
    storage_context = StorageContext.from_defaults(persist_dir=index_path)

    if os.path.exists(index_path):
        return load_index_from_storage(storage_context)

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    storage_context.persist()
    return index