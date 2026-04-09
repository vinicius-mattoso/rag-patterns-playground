# Design Decisions

## Why LlamaIndex?
LlamaIndex was chosen for its simplicity and abstraction capabilities, which reduce development time and improve maintainability.

### Pros:
- Pre-built components for document ingestion, indexing, and querying.
- Easy integration with multiple LLMs.
- Active community and documentation.

### Cons:
- Less control over low-level operations.
- Dependency on an external library.

## Why Modular Design?
A modular design ensures that components can be reused and extended in future modules (e.g., `rag_003`, `rag_004`).

## Why Local Persistence?
Keeping all data and indexes locally ensures:
- Reproducibility.
- No reliance on external storage.
- Easier debugging and testing.

## Why `.env` Configuration?
Environment-based configuration allows:
- Easy switching between LLM providers.
- Centralized management of paths and settings.

## Trade-offs
- **Abstraction vs. Control**: Using LlamaIndex sacrifices some low-level control for faster development.
- **Local vs. Cloud**: Local persistence limits scalability but simplifies the setup.

## Comparison with Naive Prompt RAG

### Why LlamaIndex?
- **Ease of Use**: LlamaIndex abstracts complex operations like document parsing and index management.
- **Modularity**: Encourages a clean architecture with reusable components.
- **Performance**: Optimized for querying large datasets efficiently.

### Naive Prompt RAG Limitations:
- **Manual Management**: Requires manual handling of documents and embeddings.
- **Error-Prone**: More code means higher chances of bugs.
- **Scalability**: Harder to scale for larger datasets.

### Conclusion:
LlamaIndex provides a more robust and scalable solution for RAG pipelines, making it a better choice for production systems.