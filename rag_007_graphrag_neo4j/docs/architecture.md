# Architecture

## Overview

`rag_007_graphrag_neo4j` is a text-to-graph RAG pipeline with Neo4j as the persistence layer. The module keeps the same direct execution style used in the earlier examples, but replaces the local graph store with a database-backed graph runtime.

## Components

### `app_direct.py`

Coordinates the end-to-end flow:

- loads configuration
- creates the LLM
- loads and chunks local text files
- builds or reuses the Neo4j graph
- exports the interactive graph HTML
- executes a fixed list of example questions


### `src/loaders.py`

Reads `.txt` and `.md` files from `data/raw`, applies deterministic chunking, and produces LangChain `Document` objects with stable metadata. This metadata is later used by Neo4j source-document linking.

### `src/graph_ingestion.py`

Transforms text chunks into `GraphDocument` objects through `LLMGraphTransformer`, then persists them into Neo4j using `Neo4jGraph.add_graph_documents(...)`.

### `src/neo4j_store.py`

Owns connectivity and low-level database operations:

- readiness check
- optional rebuild
- count/stat queries

### `src/query_engine.py`

Creates a `GraphCypherQAChain` with:

- a constrained Cypher generation prompt
- `validate_cypher=True`
- intermediate step capture

The module extracts:

- generated Cypher
- raw context rows returned by the graph query
- source document names when available

This gives the user both the answer and the retrieval trace.

### `src/visualization.py`

Queries Neo4j for a relationship snapshot and exports it as an interactive HTML file with PyVis. This is useful both for demos and for debugging the extracted graph.

## Data Flow

1. Local text files are loaded from `data/raw`.
2. Text is chunked with stable ids.
3. Each chunk is converted into graph structures via `LLMGraphTransformer`.
4. The graph is persisted in Neo4j.
5. A natural-language question is translated into Cypher.
6. Neo4j executes the query.
7. The LLM synthesizes an answer from the returned rows only.

## Robustness Choices

- persisted graph instead of ephemeral in-memory graph
- deterministic source chunk ids
- explicit rebuild flag instead of implicit destructive behavior
- exported Cypher and context rows in the output
- HTML graph snapshot for graph inspection
