# test_index_builder.py
# Tests for the index builder

import os
import pytest
from src.index_builder import build_or_load_index
from llama_index import Document

@pytest.fixture
def sample_documents():
    return [Document(text="Sample document 1"), Document(text="Sample document 2")]

@pytest.fixture
def temp_index_path(tmp_path):
    return os.path.join(tmp_path, "index.json")

def test_build_index(sample_documents, temp_index_path):
    index = build_or_load_index(sample_documents, temp_index_path)
    assert os.path.exists(temp_index_path)
    assert index is not None

def test_load_index(sample_documents, temp_index_path):
    build_or_load_index(sample_documents, temp_index_path)
    index = build_or_load_index([], temp_index_path)
    assert index is not None