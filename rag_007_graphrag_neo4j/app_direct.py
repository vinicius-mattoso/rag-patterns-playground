"""Direct entry point for Neo4j-backed GraphRAG over local text."""

from src.answer_formatter import format_query_result
from src.config import load_config
from src.graph_ingestion import build_or_load_graph
from src.llm_provider import get_llm
from src.loaders import load_text_chunks
from src.pipeline import build_pipeline, query_graph
from src.visualization import export_graph_html


def main() -> None:
    """Run a predefined set of questions against the Neo4j knowledge graph."""
    print("[rag_007] loading configuration")
    config = load_config()
    print(f"[rag_007] configuration loaded, provider={config.llm_provider}, model={config.llm_model}")

    print("[rag_007] initializing llm")
    llm = get_llm(config)

    print(f"[rag_007] loading text chunks from {config.data_path}")
    documents = load_text_chunks(config)
    print(f"[rag_007] loaded {len(documents)} text chunks")

    print("[rag_007] building or loading graph in Neo4j")
    assets = build_or_load_graph(config=config, llm=llm, documents=documents)

    print(f"[rag_007] exporting interactive graph html to {config.graph_html_path}")
    export_graph_html(
        graph=assets.graph,
        output_path=config.graph_html_path,
        relationship_limit=config.visualization_limit,
    )

    print("[rag_007] building query pipeline")
    pipeline = build_pipeline(config=config, llm=llm, graph=assets.graph)
    questions = [
        "Which carrier is responsible for shipment SHP-004?",
        # "Why was shipment SHP-004 delayed?",
        # "Which warehouse should receive shipment SHP-007?",
        # "Which route does Cargo Pulse monitor most closely in the briefings?",
    ]

    print(
        f"[rag_007] Neo4j graph ready with {assets.node_count} nodes, "
        f"{assets.relationship_count} relationships, and {assets.document_count} source documents."
    )
    for question in questions:
        print(f"[rag_007] running question: {question}")
        result = query_graph(question=question, pipeline=pipeline, config=config)
        print(format_query_result(question=question, result=result, graph_html_path=config.graph_html_path))
        print("---")


if __name__ == "__main__":
    main()
