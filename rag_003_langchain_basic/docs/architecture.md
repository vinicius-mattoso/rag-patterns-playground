# Architecture

## Overview
`rag_003_langchain_basic` implements the same direct-execution RAG flow used in `rag_002_llamaindex_basic`, but swaps LlamaIndex abstractions for LangChain building blocks. The module stays intentionally small so the framework differences remain easy to inspect.

## Components

### `app_direct.py`
Loads configuration, ingests documents, builds or loads the persisted FAISS index, executes predefined example questions, and prints answers plus retrieved sources.

### `src/config.py`
Loads `.env` values into a typed configuration object. Paths are resolved relative to the module root so execution remains stable from different working directories.

### `src/loaders.py`
Reads local files from `data/raw` and chunks them with `RecursiveCharacterTextSplitter`. Chunk metadata is preserved so retrieved sources are easy to print and compare.

### `src/llm_provider.py`
Centralizes provider selection for chat models and embeddings. Both OpenAI and Ollama are supported without changing retrieval or query logic.

### `src/index_builder.py`
Creates or reloads a persisted FAISS vector store. Persistence remains local-only so the module matches the repository's current development constraints.

### `src/query_engine.py`
Runs retrieval, formats the context, prompts the configured chat model, and returns both the final answer and source metadata.

## Data Flow
1. Files are loaded from `data/raw`.
2. Documents are chunked before indexing.
3. Chunks are embedded and persisted in a local FAISS index under `data/index`.
4. Queries retrieve the most relevant chunks.
5. The selected chunks are passed to the configured chat model to generate the answer.

## Design Notes
- The module mirrors `rag_002` at the file and execution level.
- LangChain-specific logic is isolated behind small helper modules.
- Persistence is local and replaceable, making future migration to other vector stores straightforward.
