"""
Main entry point for the CLI interface.
"""
import argparse
from .loaders import load_documents
from .chunking import chunk_text
from .embeddings import generate_embeddings
from .vectorstore import VectorStore
from .retriever import Retriever
from .prompt_builder import build_prompt
from .llm import query_llm
from .config import EMBEDDINGS_PROVIDER

def index_documents():
    """Index documents from the data/raw directory."""
    documents = load_documents("data/raw")
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc, chunk_size=500, overlap=50))
    embeddings = generate_embeddings(chunks, EMBEDDINGS_PROVIDER)
    vector_store = VectorStore("data/index.faiss", "data/metadata.json")
    vector_store.add_vectors(embeddings, chunks)
    vector_store.save()

def query_system(question: str):
    """Query the system with a question."""
    vector_store = VectorStore("data/index.faiss", "data/metadata.json")
    vector_store.load()
    retriever = Retriever(vector_store)
    # Placeholder for generating query vector
    query_vector = []
    context = retriever.retrieve(query_vector, top_k=5)
    prompt = build_prompt(context, question)
    response = query_llm(prompt)
    print(response)

def main():
    parser = argparse.ArgumentParser(description="RAG CLI Interface")
    parser.add_argument("command", choices=["index", "query"], help="Command to execute")
    parser.add_argument("--question", help="Question to query the system")
    args = parser.parse_args()

    if args.command == "index":
        index_documents()
    elif args.command == "query":
        if not args.question:
            print("Error: --question is required for the query command.")
        else:
            query_system(args.question)

if __name__ == "__main__":
    main()