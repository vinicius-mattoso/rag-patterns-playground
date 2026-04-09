# app_direct.py
# Entry point for the RAG pipeline using LlamaIndex

from src.loaders import load_documents
from src.index_builder import build_or_load_index
from src.query_engine import query_index
from src.config import load_config

def main():
    # Load configuration
    config = load_config()

    # Load documents
    documents = load_documents(config['data_path'])

    # Build or load the index
    index = build_or_load_index(documents, config['index_path'])

    # Define example questions
    questions = [
        "What is the best tourist spot in Rio?",
        "What are the main attractions in Rio?",
    ]

    # Query the index and print answers
    for question in questions:
        print(f"Question: {question}")
        answers, sources = query_index(index, question)
        print("Answer:", answers)
        print("Sources:", sources)
        print("---")

if __name__ == "__main__":
    main()