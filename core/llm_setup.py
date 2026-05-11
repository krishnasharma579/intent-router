"""
LLM initialization module for the Clob Intent Router.

This module handles the instantiation of the language model
using the centralized application settings.
"""

from langchain_groq import ChatGroq
from core.config import settings

def get_router_llm() -> ChatGroq:
    """
    Initializes and returns the ChatGroq instance configured specifically 
    for the intent routing task.

    Returns:
        ChatGroq: A configured instance of the LangChain Groq chat model.
        
    Raises:
        RuntimeError: If the LLM initialization fails.
    """
    try:
        # Initialize the model using the validated settings from config.py
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.ROUTER_TEMPERATURE,
            max_retries=2  # Prevents infinite hangs if the API is temporarily down
        )
        return llm
    except Exception as e:
        # Catching any initialization errors and raising a clean runtime error
        raise RuntimeError(f"CRITICAL: Failed to initialize the routing LLM. Details: {e}") from e