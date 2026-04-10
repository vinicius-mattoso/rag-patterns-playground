"""Interactive knowledge graph export."""

from __future__ import annotations

from pathlib import Path

import networkx as nx


def export_graph_html(graph: nx.MultiDiGraph, output_path: Path) -> None:
    """Export the graph as an interactive HTML visualization."""
    try:
        from pyvis.network import Network
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "PyVis is required to export the interactive knowledge graph HTML. "
            "Install the dependencies from requirements.txt before running app_direct.py."
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    network = Network(
        height="820px",
        width="100%",
        directed=True,
        bgcolor="#0b1020",
        font_color="#e5e7eb",
        notebook=False,
        cdn_resources="in_line",
    )

    for node_name, attrs in graph.nodes(data=True):
        title = f"{attrs.get('entity_type', 'entity')}<br>{attrs.get('description', '')}"
        network.add_node(
            node_name,
            label=node_name,
            title=title,
            color=attrs.get("color", "#4f46e5"),
        )

    for source, target, attrs in graph.edges(data=True):
        relation = attrs.get("relation", "")
        network.add_edge(source, target, label=relation, title=relation, arrows="to")

    network.set_options(
        """
        const options = {
          "physics": {"stabilization": true, "barnesHut": {"gravitationalConstant": -22000}},
          "nodes": {"shape": "dot", "size": 18, "font": {"size": 14}},
          "edges": {"font": {"size": 10}, "smooth": {"type": "dynamic"}}
        }
        """
    )
    html = network.generate_html(notebook=False)
    output_path.write_text(html, encoding="utf-8")
