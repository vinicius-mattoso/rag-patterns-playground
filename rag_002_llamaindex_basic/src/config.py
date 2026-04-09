# config.py
# Configuration loader for the RAG pipeline

import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'data_path': os.getenv('DATA_PATH', './data/raw'),
        'index_path': os.getenv('INDEX_PATH', './data/index.json'),
        'llm_provider': os.getenv('LLM_PROVIDER', 'openai'),
        'embedding_provider': os.getenv('EMBEDDING_PROVIDER', 'openai'),
    }