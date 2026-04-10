"""Pipeline orchestration for Graph RAG over CSV data."""

from __future__ import annotations

import re
from collections import Counter

from src.graph_builder import build_knowledge_graph
from src.graph_query import GraphAnswerChain
from src.schemas import GraphAssets, GraphQueryResult, KnowledgeTripleView, LoadedTable, Ontology


STOPWORDS = {
    "which",
    "what",
    "who",
    "where",
    "when",
    "why",
    "how",
    "is",
    "are",
    "the",
    "a",
    "an",
    "for",
    "to",
    "from",
    "of",
    "does",
    "do",
    "did",
    "was",
    "were",
    "shipment",
    "shipments",
    "carrier",
    "carriers",
    "warehouse",
    "warehouses",
    "route",
    "routes",
    "event",
    "events",
    "recorded",
    "responsible",
    "handled",
    "latest",
}


def build_graph_rag_assets(
    tables: dict[str, LoadedTable],
    ontology: Ontology,
) -> GraphAssets:
    """Build the knowledge graph artifacts used by the application."""
    return build_knowledge_graph(tables=tables, ontology=ontology)


def _extract_entities(question: str, assets: GraphAssets) -> list[str]:
    candidates = set(re.findall(r"[A-Z]{2,}-\d+|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", question))
    for node_name in assets.node_text_index.values():
        if node_name.lower() in question.lower():
            candidates.add(node_name)

    resolved: list[str] = []
    for candidate in candidates:
        if candidate.lower() in assets.node_text_index:
            resolved.append(assets.node_text_index[candidate.lower()])
        else:
            resolved.append(candidate)

    filtered = []
    for entity in sorted(set(resolved)):
        if entity.lower() in STOPWORDS:
            continue
        filtered.append(entity)
    return filtered


def _collect_supporting_triples(
    entities: list[str],
    assets: GraphAssets,
    support_limit: int,
) -> list[KnowledgeTripleView]:
    if not entities:
        return list(assets.triple_views[:support_limit])

    normalized = {entity.lower() for entity in entities}
    matches = [
        triple
        for triple in assets.triple_views
        if triple.subject.lower() in normalized or triple.object_.lower() in normalized
    ]
    if matches:
        return matches[:support_limit]

    token_counts = Counter(re.findall(r"[a-z0-9]+", " ".join(entities).lower()))
    scored = []
    for triple in assets.triple_views:
        haystack = f"{triple.subject} {triple.relation} {triple.object_}".lower()
        score = sum(count for token, count in token_counts.items() if token in haystack)
        scored.append((score, triple))

    ranked = [triple for score, triple in sorted(scored, key=lambda item: item[0], reverse=True) if score > 0]
    return ranked[:support_limit]

def _format_context(triples: list[KnowledgeTripleView]) -> str:
    if not triples:
        return "No relevant triples were retrieved."
    return "\n".join(
        f"- {triple.subject} --[{triple.relation}]--> {triple.object_}"
        for triple in triples
    )


def query_graph(
    question: str,
    assets: GraphAssets,
    qa_chain: GraphAnswerChain,
    support_limit: int,
) -> GraphQueryResult:
    """Query the knowledge graph and attach supporting triples."""
    entities = _extract_entities(question, assets)
    supporting_triples = _collect_supporting_triples(entities, assets, support_limit)
    answer = str(
        qa_chain.invoke(
            {
                "question": question,
                "context": _format_context(supporting_triples),
            }
        )
    )
    return GraphQueryResult(
        answer=answer,
        entities=entities,
        supporting_triples=supporting_triples,
    )
