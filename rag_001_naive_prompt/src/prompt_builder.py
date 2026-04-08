"""
Module for building prompts for the LLM.
"""
from typing import List

def build_prompt(context: List[str], question: str) -> str:
    """
    Build a prompt for the LLM using the context and question.

    Args:
        context (List[str]): List of context strings.
        question (str): The question to ask.

    Returns:
        str: The assembled prompt.
    """
    prompt = "\n".join(context)
    prompt += f"\n\nQuestion: {question}\nAnswer:"
    return prompt