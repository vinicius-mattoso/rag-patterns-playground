# Decisions

## Why Ontology Now

After `rag_007`, the next bottleneck is graph consistency. The database exists, the graph is queryable, but production robustness requires a stronger schema contract.

## Why Keep `LLMGraphTransformer`

The goal here is not to remove model-driven extraction. The goal is to constrain it. `LLMGraphTransformer` stays because it accelerates extraction, while ontology prevents uncontrolled graph drift.

## Why Filter Relationships by Source/Target Type

A relationship name alone is not enough to guarantee semantic validity. Restricting source and target types makes the graph materially safer and more coherent.

## Why Keep Text2Cypher

The question-answer mechanism is still Text2Cypher because the major architectural change in this module is graph governance, not query style. That keeps the comparison against `rag_007` clean.
