"""Token counting utilities using tiktoken."""

import tiktoken
from typing import Union


def count_tokens(text: Union[str, list[str]], model: str = "gpt-4o-mini") -> int:
    """
    Count the number of tokens in text using tiktoken.

    Args:
        text: Text or list of texts to count tokens for
        model: OpenAI model name to use for tokenization

    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base encoding for newer models
        encoding = tiktoken.get_encoding("cl100k_base")

    if isinstance(text, str):
        return len(encoding.encode(text))
    elif isinstance(text, list):
        return sum(len(encoding.encode(t)) for t in text)
    else:
        raise ValueError("Text must be a string or list of strings")


def estimate_cost(tokens: int, model: str = "gpt-4o-mini") -> float:
    """
    Estimate the cost of processing tokens.

    Args:
        tokens: Number of tokens
        model: OpenAI model name

    Returns:
        Estimated cost in USD
    """
    # Approximate costs per 1K tokens (as of 2024)
    costs = {
        "gpt-4o": 0.005,  # $5 per 1M input tokens
        "gpt-4o-mini": 0.00015,  # $0.15 per 1M input tokens
        "gpt-3.5-turbo": 0.0005,  # $0.5 per 1M input tokens
    }

    cost_per_1k = costs.get(model, costs["gpt-4o-mini"])
    return (tokens / 1000) * cost_per_1k
