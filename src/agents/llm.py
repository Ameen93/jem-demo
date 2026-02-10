"""Centralized LLM configuration for agent nodes."""

from langchain_ollama import ChatOllama

MODEL_NAME = "llama3.1"


def get_llm(max_tokens: int = 500) -> ChatOllama:
    """Get the LLM instance for agent nodes.

    Args:
        max_tokens: Maximum tokens for response.

    Returns:
        ChatOllama instance.
    """
    return ChatOllama(model=MODEL_NAME, num_predict=max_tokens)
