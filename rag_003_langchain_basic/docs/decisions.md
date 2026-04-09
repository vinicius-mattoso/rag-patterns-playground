# Design Decisions

## Why LangChain Here?
LangChain exposes lower-level composition primitives than LlamaIndex while still providing strong integrations for loaders, splitters, vector stores, and model providers. That makes it a useful comparison point after `rag_002_llamaindex_basic`.

## Why FAISS?
FAISS keeps storage local, simple, and fast for a repository that is demonstrating RAG patterns rather than production infrastructure. It also keeps the storage choice easy to swap in later modules.

## Why Separate LLM and Embedding Providers?
Real RAG systems often mix providers. Keeping model and embedding selection independent makes the module closer to production constraints and leaves room for later experiments.

## Why Manual Retrieval Plus Prompting?
LangChain offers higher-level chains, but the module uses explicit retrieval followed by prompt execution so the control flow stays obvious when compared against `rag_001` and `rag_002`.

## Trade-offs
- LangChain offers broad integration coverage, but the package surface is larger and more fragmented than LlamaIndex.
- Explicit composition gives more control, but it requires more assembly code.
- FAISS is local and lightweight, but it is not the right long-term choice for distributed or multi-user workloads.

## Comparison with `rag_002_llamaindex_basic`
- `rag_002` hides more orchestration behind the framework.
- `rag_003` exposes chunking, retrieval, prompting, and provider wiring more directly.
- The extra visibility improves extensibility, but it also increases implementation detail and dependency management.
