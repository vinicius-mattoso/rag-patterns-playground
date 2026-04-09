"""Direct entry point for the LangChain RAG pipeline."""

from src.config import load_config
from src.index_builder import build_or_load_index
from src.llm_provider import get_embeddings, get_llm
from src.loaders import load_documents
from src.query_engine import query_index


def main() -> None:
    """Run a predefined set of example queries against the local index."""
    config = load_config()
    documents = load_documents(
        data_path=config.data_path,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    embeddings = get_embeddings(config)
    vectorstore = build_or_load_index(
        documents=documents,
        embeddings=embeddings,
        index_path=config.index_path,
    )
    llm = get_llm(config)

    questions = [
        "What is the best tourist spot in Rio de Janeiro according to the documents?",
        "Which attractions and events are highlighted in Rio de Janeiro?",
    ]

    for question in questions:
        result = query_index(
            vectorstore=vectorstore,
            llm=llm,
            question=question,
            top_k=config.retrieval_k,
        )
        print(f"Question: {question}")
        print(f"Answer: {result.answer}")
        print("Retrieved Sources:")
        for source in result.sources:
            path = source.get("source", "unknown")
            chunk = source.get("chunk_id", "n/a")
            preview = source.get("content", "").strip().replace("\n", " ")
            print(f"  - {path} [chunk {chunk}]")
            print(f"    {preview}")
        print("---")


if __name__ == "__main__":
    main()
