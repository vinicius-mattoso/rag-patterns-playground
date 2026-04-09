# llm_provider.py
# LLM provider abstraction for the RAG pipeline

from llama_index.llms import OpenAI, Ollama

def get_llm_provider(provider_name):
    if provider_name == 'openai':
        return OpenAI()
    elif provider_name == 'ollama':
        return Ollama()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")