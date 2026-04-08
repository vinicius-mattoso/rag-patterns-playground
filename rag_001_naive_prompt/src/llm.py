"""
Implementation for interacting with the LLM (OpenAI or Ollama).
"""
import openai
from typing import Optional
from .config import OPENAI_API_KEY

def query_llm(prompt: str, provider: str = "openai") -> Optional[str]:
    """
    Query the LLM with a prompt.

    Args:
        prompt (str): The prompt to send to the LLM.
        provider (str): The LLM provider ("openai" or "ollama").

    Returns:
        Optional[str]: The response from the LLM.
    """
    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set in the environment variables.")

        openai.api_key = OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use the appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Failed to query OpenAI API: {e}")

    elif provider == "ollama":
        # Placeholder for Ollama API integration
        raise NotImplementedError("Ollama provider is not yet implemented.")

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")