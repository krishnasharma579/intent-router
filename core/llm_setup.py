"""
LLM Initialization module for the Clob Intent Router.

This module provides helper functions to instantiate and retrieve the 
Language Model client used for routing user queries. It implements 
caching to ensure resource efficiency.
"""

import logging
from functools import lru_cache
from langchain_groq import ChatGroq
from core.config import settings

# Configure logger for this module
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_router_llm() -> ChatGroq:
    """
    Initializes and returns a singleton instance of the ChatGroq client.
    
    The function is decorated with @lru_cache to ensure that the LLM 
    is only initialized once, reducing overhead during high-frequency routing.

    Returns:
        ChatGroq: A configured instance of the Groq LLM.

    Raises:
        RuntimeError: If the initialization fails due to configuration 
                      or connectivity issues.
    """
    try:
        logger.info(f"Initializing Router LLM with model: {settings.MODEL_NAME}")
        
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.ROUTER_TEMPERATURE,
            max_retries=2,
            # Adding timeout ensures the app doesn't hang indefinitely 
            # during the Ideathon live pitch.
            request_timeout=30.0 
        )
        
    except Exception as exc:
        # Logging the full stack trace for internal debugging
        logger.exception("Failed to initialize router LLM.")
        
        # Raising a clean, actionable error for the application layer
        raise RuntimeError(
            "CRITICAL: Failed to initialize the routing LLM. "
            "Please verify GROQ_API_KEY and MODEL_NAME in your .env file."
        ) from exc