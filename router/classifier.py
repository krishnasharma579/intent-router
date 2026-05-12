"""
Core classification logic for the Clob Intent Router.

This module leverages the structured output capabilities of the LLM 
to parse user intent into predefined categories with high precision.
"""

import logging
from langchain_core.prompts import ChatPromptTemplate

# Using the clean imports from our package initializers
from core import get_router_llm
from prompts import ROUTER_SYSTEM_PROMPT
from router.schemas import IntentResponse

# Module-level logger
logger = logging.getLogger(__name__)

def classify_intent(user_input: str) -> str:
    """
    Analyzes user input and returns the predicted intent category.

    Args:
        user_input (str): The raw text input from the user.

    Returns:
        str: The classified intent (e.g., 'hardware_query', 'code_generation').

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input is empty or just whitespace.
        RuntimeError: If the LLM pipeline fails to execute.
    """
    # 1. Strict Input Validation
    if not isinstance(user_input, str):
        raise TypeError(f"Expected string for user_input, got {type(user_input).__name__}.")
    
    normalized_input = user_input.strip()
    if not normalized_input:
        raise ValueError("User input cannot be empty or null.")

    try:
        # 2. Setup LLM with Structured Output
        # The 'include_raw=False' (default) ensures we get the Pydantic object directly.
        llm = get_router_llm()
        structured_llm = llm.with_structured_output(IntentResponse)

        # 3. Define Prompt Template
        prompt = ChatPromptTemplate.from_messages([
            ("system", ROUTER_SYSTEM_PROMPT),
            ("human", "{input}"),
        ])

        # 4. Construct and Invoke the Chain (LCEL)
        chain = prompt | structured_llm
        
        logger.info("Initiating intent classification.")
        result: IntentResponse = chain.invoke({"input": normalized_input})

        # 5. Result Validation and Logging
        logger.info(f"Classification successful. Target: [ {result.intent} ]")
        return result.intent

    except Exception as exc:
        # Logging the stack trace for developers
        logger.exception("Intent classification failed at the pipeline level.")
        
        # Raising a descriptive error for the main application flow
        raise RuntimeError(f"Routing Pipeline Failure: {exc}") from exc