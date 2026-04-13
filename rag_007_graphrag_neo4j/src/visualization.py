"""Interactive graph export based on Neo4j query results."""

from __future__ import annotations

from pathlib import Path

from src.neo4j_compat import Neo4jGraph


GRAPH_EXPORT_QUERY = """
MATCH (n)-[r]->(m)
WHERE NOT n:Document AND NOT m:Document
RETURN
  coalesce(n.id, head(labels(n))) AS source_id,
  coalesce(n.id, head(labels(n))) AS source_label,
  labels(n) AS source_labels,
  properties(n) AS source_properties,
  type(r) AS relationship_type,
  properties(r) AS relationship_properties,
  coalesce(m.id, head(labels(m))) AS target_id,
  coalesce(m.id, head(labels(m))) AS target_label,
  labels(m) AS target_labels,
  properties(m) AS target_properties
LIMIT $limit
"""


def _format_node_title(labels: list[str], properties: dict) -> str:
    preview = "<br>".join(f"{key}: {value}" for key, value in list(properties.items())[:8])
    label_text = ", ".join(labels) if labels else "Entity"
    return f"{label_text}<br>{preview}"


def export_graph_html(graph: Neo4jGraph, output_path: Path, relationship_limit: int) -> None:
    """Export a graph snapshot from Neo4j to an interactive HTML page."""
    try:
        from pyvis.network import Network
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "PyVis is required to export the interactive knowledge graph HTML. "
            "Install the dependencies from requirements.txt before running app_direct.py."
        ) from exc

    print(f"[rag_007] querying Neo4j for up to {relationship_limit} relationships to render html")
    rows = graph.query(GRAPH_EXPORT_QUERY, params={"limit": relationship_limit})
    print(f"[rag_007] rendering html graph with {len(rows)} relationships")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    network = Network(
        height="840px",
        width="100%",
        directed=True,
        bgcolor="#08111f",
        font_color="#e5e7eb",
        notebook=False,
        cdn_resources="in_line",
    )

    color_map = {
        "Shipment": "#2563eb",
        "Carrier": "#7c3aed",
        "Route": "#0f766e",
        "Warehouse": "#b45309",
        "DeliveryEvent": "#dc2626",
        "__Entity__": "#334155",
    }

    for row in rows:
        source_labels = list(row["source_labels"])
        target_labels = list(row["target_labels"])

        network.add_node(
            str(row["source_id"]),
            label=str(row["source_label"]),
            title=_format_node_title(source_labels, dict(row["source_properties"])),
            color=color_map.get(source_labels[0], "#2563eb") if source_labels else "#2563eb",
        )
        network.add_node(
            str(row["target_id"]),
            label=str(row["target_label"]),
            title=_format_node_title(target_labels, dict(row["target_properties"])),
            color=color_map.get(target_labels[0], "#0f766e") if target_labels else "#0f766e",
        )
        relation = str(row["relationship_type"])
        network.add_edge(str(row["source_id"]), str(row["target_id"]), label=relation, title=relation, arrows="to")

    network.set_options(
        """
        const options = {
          "physics": {"stabilization": true, "barnesHut": {"gravitationalConstant": -20000}},
          "nodes": {"shape": "dot", "size": 18, "font": {"size": 13}},
          "edges": {"font": {"size": 10}, "smooth": {"type": "dynamic"}}
        }
        """
    )
    html = network.generate_html(notebook=False)
    output_path.write_text(html, encoding="utf-8")
    print(f"[rag_007] graph html written to {output_path}")
