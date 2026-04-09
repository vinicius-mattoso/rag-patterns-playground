# Architecture

## Overview
The `rag_002_llamaindex_basic` module is designed to implement a basic Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex. The architecture emphasizes modularity, configurability, and local persistence.

## Components

### 1. `app_direct.py`
- Entry point for the pipeline.
- Handles document loading, index building/loading, and querying.

### 2. `src/config.py`
- Loads configuration from environment variables.
- Supports switching between OpenAI and Ollama as LLM providers.

### 3. `src/loaders.py`
- Handles document ingestion from the `data/raw` directory.
- Uses LlamaIndex's `SimpleDirectoryReader` for simplicity.

### 4. `src/index_builder.py`
- Builds or loads a persisted index.
- Uses LlamaIndex's `GPTSimpleVectorIndex`.

### 5. `src/query_engine.py`
- Queries the index and retrieves answers and sources.

### 6. `src/llm_provider.py`
- Abstracts LLM provider selection.
- Supports OpenAI and Ollama.

## Data Flow
1. **Document Loading**: Documents are loaded from `data/raw`.
2. **Indexing**: Documents are indexed and persisted locally.
3. **Querying**: Predefined questions are queried, and answers with sources are returned.

## Design Principles
- **Modularity**: Each component has a single responsibility.
- **Configurability**: Environment-based configuration for flexibility.
- **Local Persistence**: Keeps all data and indexes locally for simplicity and reproducibility.