# Architecture

## Overview
This project is a modular Retrieval-Augmented Generation (RAG) system. It is designed to be framework-agnostic and allows for easy replacement of components.

## Components
- **Loaders**: Load documents from disk.
- **Chunking**: Split text into overlapping chunks.
- **Embeddings**: Generate vector embeddings for text.
- **Vector Store**: Store and retrieve vectors using FAISS.
- **Retriever**: Retrieve relevant chunks for a query.
- **Prompt Builder**: Assemble a prompt for the LLM.
- **LLM**: Query the language model (OpenAI or Ollama).

## Data Flow
1. Documents are loaded and chunked.
2. Chunks are embedded and stored in FAISS.
3. Queries retrieve relevant chunks.
4. A prompt is built and sent to the LLM.
5. The LLM generates a response.

## Testing
- Use `app_direct.py` for direct testing with predefined inputs and questions.