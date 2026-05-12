"""Core classification logic for routing user queries to downstream agents."""

import logging

from langchain_core.prompts import ChatPromptTemplate

from core.llm_setup import get_router_llm
from prompts.system_prompt import ROUTER_SYSTEM_PROMPT
from router.schemas import IntentResponse

logger = logging.getLogger(__name__)


def classify_intent(user_input: str) -> str:
    """Classify a user query into one routing intent."""
    if not isinstance(user_input, str):
        raise TypeError(
            f"user_input must be a string, got {type(user_input).__name__}."
        )
    normalized_input = user_input.strip()
    if not normalized_input:
        raise ValueError("user_input cannot be empty.")

    try:
        llm = get_router_llm()
        structured_llm = llm.with_structured_output(IntentResponse)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", ROUTER_SYSTEM_PROMPT),
                ("human", "{input}"),
            ]
        )

        chain = prompt | structured_llm
        logger.info("Classifying intent for input.")
        result: IntentResponse = chain.invoke({"input": normalized_input})
        logger.info("Successfully routed to: %s", result.intent)
        return result.intent
    except Exception as exc:
        logger.exception("Failed to classify user input due to routing pipeline error.")
        raise RuntimeError(f"Routing pipeline failed: {exc}") from exc
