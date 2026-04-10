# RAG 004: Graph RAG from Tabular Data

This module implements Graph RAG over local CSV files in a logistics domain. It converts structured tables into a knowledge graph, queries that graph with natural language, and exports the same graph as an interactive HTML artifact.

## Core Idea
- CSV files remain the source of truth.
- `ontology.yaml` defines how rows become graph entities and relationships.
- The graph is used for both QA and visualization.

## What We Built
- A CSV-to-graph pipeline driven by a declarative ontology.
- A local knowledge graph assembled from shipments, routes, carriers, warehouses, and delivery events.
- A grounded QA flow that answers from retrieved graph triples instead of raw text chunks.
- An interactive HTML export of the full knowledge graph.
- Two illustrative diagram assets to explain the ontology and the answer path.

## How This Differs from Document RAG
- Retrieval is graph-oriented rather than chunk-oriented.
- Evidence is shown as graph triples instead of document excerpts.
- The data model is driven by entity relationships already present in the CSVs.

## Benefits of This Approach
- Better fit for operational data with explicit relationships across tables.
- More explainable answers, because the system can show the exact triples used.
- Easier ontology evolution, since graph semantics live in `ontology.yaml` instead of being spread across code.
- Stronger debugging workflow, because the same graph can be inspected visually in HTML.

## Structure
- `app_direct.py`: direct execution entry point.
- `ontology.yaml`: graph mapping directives.
- `src/`: configuration, loading, graph building, QA, visualization, formatting.
- `docs/`: architecture and design rationale.

## Interactive Graph
Running `app_direct.py` generates a local HTML file, by default `artifacts/knowledge_graph.html`, with an interactive visualization of the derived knowledge graph.

- Interactive HTML graph:
  [knowledge_graph.html](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_004_tabular_rag/artifacts/knowledge_graph.html)
- Ontology illustration:
  [ontology-neo4j-style.png](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_004_tabular_rag/artifacts/ontology-neo4j-style.png)
- Answer flow illustration:
  [answer-flow-infographic.png](c:/Users/vinicius/Documents/MEUGITHUB/rag-patterns-playground/rag_004_tabular_rag/artifacts/answer-flow-infographic.png)

## How the Answering Flow Works
1. Load all CSV tables from `data/raw`.
2. Apply `ontology.yaml` to map rows into graph nodes and relationships.
3. Build a full `networkx` graph and export it to HTML.
4. Match entities mentioned in the question.
5. Retrieve the most relevant supporting triples.
6. Ask the LLM to answer using only those triples as grounded context.

## Example Outcome
For the question `Which carrier is responsible for shipment SHP-004?`, the system retrieves a decisive triple equivalent to:

`Shipment SHP-004 --[is handled by carrier CAR-003 with priority critical]--> Carrier Cargo Pulse`

That is why the answer can be returned as:

`The carrier responsible for shipment SHP-004 is Cargo Pulse.`

## How to Run
```bash
pip install -r requirements.txt
python app_direct.py
```

## Configuration
Copy `.env.example` to `.env` and configure an LLM provider.

### OpenAI example
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key
```

### Ollama example
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```
