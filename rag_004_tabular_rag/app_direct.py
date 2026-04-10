"""Direct entry point for the tabular Graph RAG pipeline."""

from src.answer_formatter import format_query_result
from src.config import load_config
from src.graph_query import build_graph_qa_chain
from src.llm_provider import get_llm
from src.loaders import load_csv_tables
from src.ontology import load_ontology
from src.pipeline import build_graph_rag_assets, query_graph
from src.visualization import export_graph_html


def main() -> None:
    """Run predefined graph-based questions over CSV-derived knowledge graph data."""
    config = load_config()
    tables = load_csv_tables(config.data_path)
    ontology = load_ontology(config.ontology_path)
    assets = build_graph_rag_assets(tables=tables, ontology=ontology)
    export_graph_html(assets.graph, config.graph_html_path)

    llm = get_llm(config)
    qa_chain = build_graph_qa_chain(llm=llm)

    questions = [
        "Which carrier is responsible for shipment SHP-004?",
        # "Which warehouse does shipment SHP-003 depart from?",
        # "What is the latest event recorded for shipment SHP-004?",
        # "Which route connects Rio de Janeiro to Brasilia?",
        # "Which delayed shipments were handled by Blue Route Logistics?",
    ]

    for question in questions:
        result = query_graph(
            question=question,
            assets=assets,
            qa_chain=qa_chain,
            support_limit=config.support_limit,
        )
        print(format_query_result(question, result, config.graph_html_path))
        print("---")


if __name__ == "__main__":
    main()
