# RAG 001 Naive Prompt

This project implements a framework-agnostic baseline Retrieval-Augmented Generation (RAG) system. It is designed to be modular, maintainable, and easily extendable.

## Features
- Load local documents from disk
- Chunk text with overlap
- Generate embeddings
- Store and retrieve vectors locally using FAISS
- Query with a manually assembled prompt
- Support OpenAI as an LLM provider
- Configurable embeddings provider

## CLI Usage
```bash
# Index documents
python -m src.main index

# Query the system
python -m src.main query "your question"
```

## Direct Testing
You can use `app_direct.py` to test the system with predefined inputs:
```bash
python app_direct.py
```

## Project Structure
- `src/`: Source code for the system
- `docs/`: Documentation
- `tests/`: Unit tests
- `data/raw/`: Placeholder for raw data files

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```