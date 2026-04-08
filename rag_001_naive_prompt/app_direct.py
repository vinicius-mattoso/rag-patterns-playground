"""
Direct app for testing the RAG system with predefined inputs.

Usage:
- Define the `file_path` or `text` variable for ingestion.
- Define the `questions` list for queries.
- Choose to run ingestion, querying, or both.
"""
from src.loaders import load_documents
from src.chunking import chunk_text
from src.embeddings import generate_embeddings
from src.vectorstore import VectorStore
from src.retriever import Retriever
from src.prompt_builder import build_prompt
from src.llm import query_llm
from src.config import EMBEDDINGS_PROVIDER

# Define input variables
file_path = None  # Example: "data/raw/sample.txt"
text = """
O Rio de Janeiro é uma das cidades mais icônicas do Brasil, conhecida por suas praias deslumbrantes, como Copacabana e Ipanema, e pelo Cristo Redentor, uma das sete maravilhas do mundo moderno. Outros pontos turísticos incluem o Pão de Açúcar, o Jardim Botânico e o Maracanã, um dos estádios de futebol mais famosos do mundo. A cidade também é famosa pelo Carnaval, com desfiles de escolas de samba que atraem turistas do mundo inteiro.
"""
questions = [
    "Quais são os pontos turísticos mencionados?",
    "O que torna o Rio de Janeiro famoso?",
    "Qual é a temporada mais popular para visitar o Rio de Janeiro?",
    "Qual é a temática do texto?"
]

def ingest():
    """Ingest documents into the vector store."""
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
    print("Ingestion completed.")

def query():
    """Query the system with predefined questions."""
    vector_store = VectorStore("data/index.faiss", "data/metadata.json")
    vector_store.load()
    retriever = Retriever(vector_store)

    for question in questions:
        # Generate query vector using the question text
        query_vector = generate_embeddings([question], EMBEDDINGS_PROVIDER)[0]
        context = retriever.retrieve(query_vector, top_k=5)
        prompt = build_prompt(context, question)
        response = query_llm(prompt)
        print(f"Question: {question}\nAnswer: {response}\n")

def main():
    # Choose which part to run
    run_ingestion = True
    run_querying = True

    if run_ingestion:
        ingest()
    if run_querying:
        query()

if __name__ == "__main__":
    main()