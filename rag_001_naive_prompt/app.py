"""
App for testing the RAG system.

Usage:
- Pass a path to a file to index and query.
- Alternatively, provide a text string directly in the docstring below.
"""
import argparse
from src.loaders import load_documents
from src.chunking import chunk_text
from src.embeddings import generate_embeddings
from src.vectorstore import VectorStore
from src.retriever import Retriever
from src.prompt_builder import build_prompt
from src.llm import query_llm
from src.config import EMBEDDINGS_PROVIDER

def index_and_query(file_path: str = None, text: str = None):
    """
    Index and query the system using a file or direct text.

    Args:
        file_path (str): Path to the file to index.
        text (str): Direct text to index.
    """
    if file_path:
        documents = load_documents(file_path)
    elif text:
        documents = [text]
    else:
        print("Error: Provide either a file path or text.")
        return

    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc, chunk_size=500, overlap=50))
    embeddings = generate_embeddings(chunks, EMBEDDINGS_PROVIDER)

    vector_store = VectorStore("data/index.faiss", "data/metadata.json")
    vector_store.add_vectors(embeddings, chunks)
    vector_store.save()

    # Query the system
    vector_store.load()
    retriever = Retriever(vector_store)
    # Placeholder for generating query vector
    query_vector = []
    context = retriever.retrieve(query_vector, top_k=5)
    prompt = build_prompt(context, "What is the content about?")
    response = query_llm(prompt)
    print(response)

def main():
    parser = argparse.ArgumentParser(description="Test the RAG system.")
    parser.add_argument("--file", help="Path to the file to index and query.")
    parser.add_argument("--text", help="Direct text to index and query.")
    args = parser.parse_args()

    index_and_query(file_path=args.file, text=args.text)

if __name__ == "__main__":
    main()