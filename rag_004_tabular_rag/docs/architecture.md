# Architecture

## Overview
`rag_004_tabular_rag` implements Graph RAG over local logistics CSVs. The module transforms rows and foreign-key style references into a knowledge graph using `ontology.yaml`, then uses that graph both for natural-language QA and for interactive HTML visualization.

The final implementation intentionally keeps the same software shape used across the repository:
- direct execution from `app_direct.py`
- modular responsibilities inside `src/`
- local data and local artifacts only
- documentation that explains both architecture and reasoning

## Components

### `app_direct.py`
Loads configuration, CSVs, ontology, graph assets, exports the HTML graph, builds the QA layer, and runs fixed example questions.

### `src/config.py`
Loads `.env` values and resolves paths for raw data, ontology, and exported graph HTML.

### `src/loaders.py`
Reads local CSV tables from `data/raw`.

### `src/ontology.py`
Parses `ontology.yaml`, which declares how CSV tables map into graph entities and relationships.

### `src/graph_builder.py`
Builds the `networkx.MultiDiGraph` for visualization and a graph-facing structure for QA. This is the key bridge between raw CSV rows and graph-native reasoning.

### `src/graph_query.py`
Creates the grounded answer synthesis layer. Instead of asking the model to infer directly from raw tables, the model receives only the retrieved graph triples relevant to the question.

### `src/pipeline.py`
Coordinates graph assembly and query execution. It performs entity matching, supporting triple retrieval, and grounded answer synthesis.

### `src/visualization.py`
Exports a self-contained interactive HTML graph.

### `src/answer_formatter.py`
Prints answers, matched entities, and evidence in a terminal-friendly format.

### `src/diagram_renderer.py`
Generates project illustrations that explain the ontology and the answer-retrieval path. These are communication assets for understanding the pattern, not part of runtime QA.
 
## Data Flow
1. CSV tables are loaded from `data/raw`.
2. `ontology.yaml` defines entity and relationship extraction rules.
3. The graph builder constructs nodes and edges from tabular rows.
4. The graph is exported to `artifacts/knowledge_graph.html`.
5. The pipeline matches entities mentioned in the question.
6. Supporting triples are selected from the local graph.
7. The LLM answers only from those triples.
8. Answers are returned together with the evidence triples used.

## Why This Architecture Helps
- It separates graph construction from graph questioning.
- It makes ontology changes safer, because mapping logic is centralized.
- It improves explainability, because the QA step is grounded on retrieved triples.
- It gives two debugging surfaces:
  `knowledge_graph.html` for visual inspection and terminal evidence output for query inspection.
