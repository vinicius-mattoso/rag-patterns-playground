# Architecture

## Overview

`rag_008_graphrag_neo4j_ontology` keeps the same major building blocks as `rag_007`, but inserts ontology as an explicit contract between extraction and persistence.

## Key Difference from `rag_007`

In `rag_007`, graph normalization was mostly heuristic. In `rag_008`, the ontology decides:

- what entity types are allowed
- what relationship types are allowed
- how aliases map to canonical names
- which source and target types are valid for each relationship

## Flow

1. Text is loaded from `data/raw`.
2. Chunks are extracted with `LLMGraphTransformer`.
3. Extracted nodes and edges are canonicalized against the ontology.
4. Invalid or non-ontology relationships are dropped.
5. The remaining graph is persisted in Neo4j.
6. Questions are answered through Text2Cypher over the persisted graph.

## Production Value

The ontology layer makes the graph easier to govern and reason about. This is the point where the system starts to move from “LLM-extracted graph” toward “domain graph with LLM-assisted population.”
