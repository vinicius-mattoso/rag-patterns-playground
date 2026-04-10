"""Console formatting helpers for Graph RAG output."""

from __future__ import annotations

from pathlib import Path

from src.schemas import GraphQueryResult


def format_query_result(question: str, result: GraphQueryResult, graph_html_path: Path) -> str:
    """Render a query result into a readable terminal output."""
    lines = [
        f"Question: {question}",
        f"Answer: {result.answer}",
        "Matched Entities:",
    ]
    if result.entities:
        for entity in result.entities:
            lines.append(f"  - {entity}")
    else:
        lines.append("  - none")

    lines.append("Supporting Triples:")
    if result.supporting_triples:
        for triple in result.supporting_triples:
            lines.append(
                f"  - {triple.subject} --[{triple.relation}]--> {triple.object_} "
                f"(source: {triple.source_table})"
            )
    else:
        lines.append("  - none")

    lines.append(f"Graph HTML: {graph_html_path}")
    return "\n".join(lines)
