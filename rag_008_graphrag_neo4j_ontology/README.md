# rag_008_graphrag_neo4j_ontology

`rag_008_graphrag_neo4j_ontology` is the ontology-guided evolution of `rag_007_graphrag_neo4j`. It keeps the same LangChain + Neo4j GraphRAG structure, but introduces an explicit `ontology.yaml` so extraction, normalization, persistence, and query behavior stay aligned with a domain contract.

## Why This Evolution Exists

`rag_007` already moved the graph into Neo4j, but the graph schema still depended heavily on what the LLM chose to emit. That creates drift:

- entity labels can vary between runs
- relationship names can become semantically inconsistent
- identifiers can lose formatting consistency
- Cypher generation can miss valid nodes because the stored graph is not canonical enough

`rag_008` addresses those problems by making ontology a first-class input to the pipeline.

## What the Ontology Adds

The [ontology.yaml](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/ontology.yaml) defines:

- allowed entity types
- allowed relationship types
- aliases for both
- expected id patterns
- source and target constraints for relationships

This means the LLM still helps extract graph structure, but the persisted graph is filtered and normalized through domain rules before it reaches Neo4j.

## Architecture

1. [app_direct.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/app_direct.py) loads config, ontology, documents, graph, and questions.
2. [src/loaders.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/src/loaders.py) loads `.txt` and `.md` sources from `data/raw`.
3. [src/ontology.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/src/ontology.py) loads and indexes ontology rules.
4. [src/graph_ingestion.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/src/graph_ingestion.py) uses `LLMGraphTransformer` and then enforces ontology-guided normalization.
5. [src/query_engine.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/src/query_engine.py) answers questions through Text2Cypher using the Neo4j schema.
6. [src/visualization.py](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_008_graphrag_neo4j_ontology/src/visualization.py) exports the graph to HTML.

## Run

From inside `rag_008_graphrag_neo4j_ontology`:

```powershell
& ..\.venv\Scripts\python app_direct.py
```

The module still interprets natural-language questions through Text2Cypher:

1. question in natural language
2. LLM generates Cypher
3. Neo4j executes the Cypher
4. the answer is synthesized only from the returned rows

## Benefits Compared with `rag_007`

- more stable labels and relationship types
- less schema drift between runs
- clearer path to production governance
- better alignment between extraction and downstream Cypher
- easier evolution into domain-specific GraphRAG systems
