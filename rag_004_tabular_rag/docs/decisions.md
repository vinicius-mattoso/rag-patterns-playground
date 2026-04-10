# Design Decisions

## Why Move from Table Querying to Graph RAG?
The logistics CSVs contain explicit relationships. Graph RAG makes those connections first-class instead of leaving them implicit inside separate tables.

## Why Use `ontology.yaml`?
The ontology externalizes graph semantics. It becomes the central place to evolve how CSV records turn into graph entities and graph edges. This reduces hidden assumptions in code and makes the graph model reviewable.

## Why `networkx`?
`networkx` is local, inspectable, and sufficient for a repository module whose goal is to demonstrate a pattern rather than production graph infrastructure.

## Why Interactive HTML?
Graph construction is easier to validate when the derived knowledge graph can be inspected visually. The HTML artifact also makes ontology debugging easier and helps explain the pattern to people who are not reading the code.

## Why Ground Answers on Retrieved Triples Instead of Using a Classic Graph Chain Directly?
The project now uses a more controlled pattern:
- detect relevant entities locally
- retrieve supporting triples deterministically
- ask the model to answer from that explicit context

This gives more predictable behavior and cleaner evidence output than relying entirely on a generic graph QA chain to infer entities and context by itself.

## Why Add Visual Explanation Assets?
The ontology image and the answer-flow infographic serve a documentation purpose. They help communicate:
- how the CSVs become a graph
- how a specific answer is derived from graph evidence
- why Graph RAG is different from plain document retrieval

## Trade-offs
- Ontology quality directly affects graph quality.
- The answer quality still depends on the LLM understanding graph triples correctly.
- `networkx` is not intended for very large-scale graph serving.
- A static ontology is explicit and maintainable, but it requires manual upkeep as schemas evolve.
