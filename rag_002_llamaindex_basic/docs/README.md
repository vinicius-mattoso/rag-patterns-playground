# RAG 002: LlamaIndex Basic

This module implements a basic Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex. It improves upon the naive implementation by leveraging framework abstractions while maintaining modularity and production readiness.

## Key Changes from `rag_001_naive_prompt`
- **LlamaIndex Integration**: Simplifies document ingestion, indexing, and querying.
- **Modular Design**: Clear separation of concerns for better maintainability.
- **Environment Configuration**: Supports OpenAI and Ollama as LLM providers via `.env`.

## Benefits of Using LlamaIndex
- Faster development with pre-built abstractions.
- Simplified document handling and querying.
- Easy integration with multiple LLMs.

## Trade-offs
- Less low-level control compared to a naive implementation.
- Dependency on the LlamaIndex library.

## Comparison: LlamaIndex vs Naive Prompt RAG

### Advantages of LlamaIndex:
1. **Abstraction**: Simplifies document ingestion, indexing, and querying with pre-built components.
2. **Modularity**: Clear separation of concerns for better maintainability.
3. **Flexibility**: Supports multiple LLMs (e.g., OpenAI, Ollama) and embedding providers.
4. **Persistence**: Built-in support for saving and loading indexes locally.
5. **Error Handling**: Provides robust mechanisms for handling edge cases.

### Trade-offs:
1. **Less Control**: Abstracted operations reduce low-level customization.
2. **Dependency**: Requires the LlamaIndex library, adding an external dependency.

### Why LlamaIndex is Better:
- Faster development with fewer lines of code.
- Easier to extend and maintain.
- Built-in optimizations for querying and storage.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file based on `.env.example`.
3. Run the pipeline:
   ```bash
   python app_direct.py
   ```