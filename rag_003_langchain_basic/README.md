# RAG 003: LangChain Basic

This module implements a basic Retrieval-Augmented Generation pipeline using LangChain while keeping the same direct-execution structure used in `rag_002_llamaindex_basic`. The point is not to make the architecture radically different. The point is to make the framework choice easy to compare.

## What Changed Compared to `rag_002_llamaindex_basic`
- LangChain replaces LlamaIndex for document loading, chunking, embeddings, vector storage, and answer generation.
- FAISS persistence is explicit and local instead of being hidden behind LlamaIndex storage abstractions.
- Chat model and embedding selection are separated so OpenAI and Ollama can be mixed independently.
- Retrieval and prompt execution are assembled directly, which makes the RAG flow more visible.

## Benefits of Using LangChain
- Broad ecosystem coverage across loaders, vector stores, chat models, and orchestration patterns.
- Lower-level composition than `rag_002`, which makes future experimentation easier.
- Clear separation between retrieval, prompting, and provider wiring.
- Strong fit for future modules that may need custom chains, tools, or agent integration.

## Trade-offs
- Higher abstraction than `rag_001_naive_prompt`, but less opinionated than `rag_002_llamaindex_basic`.
- More integration flexibility comes with more package surface and more assembly code.
- Persistence and query flow are easier to customize, but require slightly more implementation discipline.

## Project Structure
- `app_direct.py`: direct execution entry point with predefined example questions.
- `src/config.py`: environment-based typed configuration.
- `src/loaders.py`: local file ingestion and chunking.
- `src/index_builder.py`: FAISS build/load persistence layer.
- `src/query_engine.py`: retrieval plus answer generation.
- `src/llm_provider.py`: chat model and embedding provider factories.
- `docs/`: architecture and decision records.
- `tests/`: offline tests for indexing and querying.

## Configuration
Create `.env` from `.env.example` and select providers there.

### OpenAI example
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=your-key
```

### Ollama example
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

## How to Run
```bash
pip install -r requirements.txt
python app_direct.py
```

Run tests with:

```bash
pytest
```
