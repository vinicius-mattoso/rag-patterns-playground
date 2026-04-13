# rag_007_graphrag_neo4j

`rag_007_graphrag_neo4j` is the production-oriented GraphRAG variant of this repository. Instead of keeping the graph only in process memory or local JSON, it extracts entities and relationships from local text, persists them in Neo4j, and answers natural-language questions through LangChain's Cypher QA flow.

## What This Module Adds

Compared with `rag_005_text_langchain_local` and `rag_006_text_langchain_prompt_graph`, this module adds:

- durable graph persistence in Neo4j
- reusable graph schema and query surface across runs
- LangChain `LLMGraphTransformer` ingestion directly into Neo4j
- `langchain-neo4j` as the preferred Neo4j integration path
- Cypher-based retrieval with traceable intermediate context
- interactive HTML export from the database-backed graph

This is the first module in the repo designed around a graph database as the system of record, which makes it a better base for production hardening, governance, and future agent workflows.

## Why GraphRAG Here

GraphRAG is useful when the answer depends on relationships rather than just semantic similarity. With logistics-style text, the critical facts are often relational:

- a shipment is handled by a carrier
- a shipment departs from one warehouse and arrives at another
- an event belongs to a shipment
- a route connects cities and operational entities

Persisting these connections in Neo4j makes the retrieval step more explicit and inspectable than a plain vector-only pipeline.

## Why LangChain + Neo4j

LangChain provides the application primitives:

- `LLMGraphTransformer` to turn text chunks into graph documents
- `GraphCypherQAChain` to convert questions into Cypher and answer from query results
- provider abstraction for OpenAI and Ollama

Neo4j provides the graph runtime:

- persisted nodes and relationships
- graph-native traversal and Cypher querying
- inspectable data model and schema
- a path toward production controls such as read-only users, indexes, and query governance

## Architecture

1. `app_direct.py` loads local `.txt` and `.md` files from `data/raw`.
2. `src/loaders.py` chunks the text and assigns stable chunk ids.
3. `src/graph_ingestion.py` uses `LLMGraphTransformer` to extract graph documents.
4. `src/neo4j_store.py` connects to Neo4j and persists the extracted graph.
5. `src/query_engine.py` runs `GraphCypherQAChain` with a read-only oriented Cypher prompt.
6. `src/visualization.py` exports a `.html` graph snapshot for inspection.

During ingestion, node labels and relationship types are normalized before persistence. This avoids drift such as `Deliveryevent` versus `DeliveryEvent` and keeps the stored graph aligned with the configured domain labels.

## Run

From inside `rag_007_graphrag_neo4j`:

```powershell
python app_direct.py
```

Before that, configure `.env` with:

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `NEO4J_DATABASE`
- `LLM_PROVIDER`
- `LLM_MODEL`

The generated interactive graph will be written to `artifacts/knowledge_graph.html`.

## Production Notes

This module is closer to production than the prior local graph examples, but the safe operating model still matters:

- use a read-only Neo4j user for query-time access
- isolate ingestion credentials from query credentials when moving beyond a demo
- keep `validate_cypher=True`
- review generated Cypher in logs or traces before broader rollout
- constrain the graph schema with `ALLOWED_NODES` and `ALLOWED_RELATIONSHIPS` when your domain is stable
- keep APOC enabled if you want automatic schema refresh through LangChain's Neo4j integration
