"""LLM initialization helpers for the intent router."""

import logging

from langchain_groq import ChatGroq

from core.config import settings

logger = logging.getLogger(__name__)


def get_router_llm() -> ChatGroq:
    """Return a configured ``ChatGroq`` client for routing."""
    try:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.ROUTER_TEMPERATURE,
            max_retries=2,
        )
    except Exception as exc:
        logger.exception("Failed to initialize router LLM.")
        raise RuntimeError(
            "CRITICAL: Failed to initialize the routing LLM. "
            "Verify GROQ_API_KEY and MODEL_NAME configuration."
        ) from exc
