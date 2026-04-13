"""Console formatting helpers for Neo4j GraphRAG output."""

from __future__ import annotations

from pathlib import Path

from src.schemas import GraphQueryResult


def format_query_result(question: str, result: GraphQueryResult, graph_html_path: Path) -> str:
    """Render a query result into readable terminal output."""
    lines = [
        f"Question: {question}",
        f"Answer: {result.answer}",
        "Generated Cypher:",
        f"  {result.generated_cypher or 'none'}",
        "Context Rows:",
    ]

    if result.context_records:
        for record in result.context_records:
            lines.append(f"  {record.row_number}. {record.payload}")
    else:
        lines.append("  - none")

    lines.append("Source Documents:")
    if result.source_documents:
        for source_name in result.source_documents:
            lines.append(f"  - {source_name}")
    else:
        lines.append("  - none")

    lines.append(f"Graph HTML: {graph_html_path}")
    return "\n".join(lines)
