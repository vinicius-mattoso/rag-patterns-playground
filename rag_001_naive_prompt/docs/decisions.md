# Decisions

## Key Design Choices

### Framework-Agnostic Design
The system avoids using LangChain or LlamaIndex to ensure flexibility and maintainability.

### Modular Components
Each component (e.g., chunking, embeddings, vector store) is implemented as a separate module to allow for easy replacement.

### Local Storage
FAISS is used for local vector storage to avoid external dependencies.

### Environment Variables
Configuration is managed via a `.env` file to keep sensitive information secure.

### CLI Interface
A simple CLI interface is provided for indexing and querying.

### Direct Testing
`app_direct.py` was added to allow testing with predefined inputs and questions, making it easier to validate the system's behavior.