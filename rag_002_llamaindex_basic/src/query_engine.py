# query_engine.py
# Query engine for the RAG pipeline

# from llama_index.core import VectorStoreIndex

def query_index(index, question):
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    answers = response.response
    sources = [node.node.get_text() for node in response.source_nodes]
    return answers, sources