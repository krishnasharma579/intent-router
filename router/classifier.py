"""
Core classification logic for the Clob Intent Router.

This module integrates the LLM, the Pydantic schema, and the system prompt
to classify user inputs into predefined routing intents.
"""

import logging
from langchain_core.prompts import ChatPromptTemplate
from core.llm_setup import get_router_llm
from router.schemas import IntentResponse
from prompts.system_prompt import ROUTER_SYSTEM_PROMPT

# Setup basic logging for production monitoring
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def classify_intent(user_input: str) -> str:
    """
    Analyzes the user's input and classifies it into a specific intent route.

    Args:
        user_input (str): The raw text input provided by the user.

    Returns:
        str: The strictly typed classified intent (e.g., 'hardware_query').

    Raises:
        RuntimeError: If the LangChain pipeline fails to process the request.
    """
    try:
        # 1. Initialize the fast routing LLM
        llm = get_router_llm()
        
        # 2. Bind the LLM to our Pydantic schema to enforce strict output
        structured_llm = llm.with_structured_output(IntentResponse)
        
        # 3. Construct the prompt template using system and human messages
        prompt = ChatPromptTemplate.from_messages([
            ("system", ROUTER_SYSTEM_PROMPT),
            ("human", "{input}")
        ])
        
        # 4. Build the LangChain pipeline using LCEL (LangChain Expression Language)
        chain = prompt | structured_llm
        
        logger.info(f"Classifying intent for input: '{user_input}'")
        
        # 5. Invoke the chain and extract the intent string
        result: IntentResponse = chain.invoke({"input": user_input})
        
        logger.info(f"Successfully routed to: '{result.intent}'")
        
        return result.intent
        
    except Exception as e:
        logger.error(f"Failed to classify intent. Error: {str(e)}")
        # In a real production system, you might return a default intent 
        # (like 'general_chat') here instead of crashing, but for the MVP, 
        # failing fast helps in debugging.
        raise RuntimeError(f"Routing Pipeline Failed: {str(e)}") from e