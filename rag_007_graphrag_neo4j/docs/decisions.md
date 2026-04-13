# Decisions

## Why Neo4j Instead of a Local Graph File

The previous graph modules were useful for learning and comparison, but they were still application-local artifacts. Neo4j was chosen here because the graph should become a persistent query surface rather than an in-memory intermediate object.

## Why `LLMGraphTransformer`

The module follows the LangChain graph extraction path already introduced in `rag_005`. That keeps the extraction flow concise and aligned with the ecosystem that will later support more advanced GraphRAG patterns.

## Why `GraphCypherQAChain`

The query side intentionally uses Cypher generation rather than a custom ad hoc graph traversal layer. The trade-off is that generated Cypher must be constrained and observed, but the benefit is a much more flexible natural-language interface over the persisted graph.

## Why Keep `app_direct.py`

The repository compares RAG patterns side by side. Keeping the same execution model across modules makes the architectural changes easier to isolate and understand.

## Why Include Raw Context Rows

For this module, answer traceability is more important than a polished terminal UI. Showing the generated Cypher and the returned context rows helps debug both the graph model and the Cypher generation behavior.
