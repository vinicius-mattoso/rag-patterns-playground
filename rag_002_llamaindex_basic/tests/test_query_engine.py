# test_query_engine.py
# Tests for the query engine

import pytest
from src.query_engine import query_index
from llama_index import GPTSimpleVectorIndex, Document

@pytest.fixture
def sample_index(tmp_path):
    index_path = tmp_path / "index.json"
    documents = [Document(text="Sample document 1"), Document(text="Sample document 2")]
    index = GPTSimpleVectorIndex.from_documents(documents)
    index.save_to_disk(index_path)
    return GPTSimpleVectorIndex.load_from_disk(index_path)

def test_query_index(sample_index):
    question = "What is this document about?"
    answers, sources = query_index(sample_index, question)
    assert answers is not None
    assert len(sources) > 0