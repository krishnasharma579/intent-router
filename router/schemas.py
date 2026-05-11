"""
Pydantic schemas for the Clob Intent Router.

This module defines the expected output structure from the LLM,
ensuring that the routing logic receives strictly typed and validated data.
"""

from pydantic import BaseModel, Field
from typing import Literal

class IntentResponse(BaseModel):
    """
    Schema to enforce structured JSON output from the routing LLM.
    The LLM must strictly choose one of the predefined intent categories.
    """
    
    # Using Literal forces the LLM to output ONLY one of these exact three strings.
    # If the LLM tries to output anything else, Pydantic will throw a validation error.
    intent: Literal["hardware_query", "code_generation", "general_chat"] = Field(
        description=(
            "The classified intent of the user input. You must choose exactly one "
            "of the following: 'hardware_query', 'code_generation', or 'general_chat'."
        )
    )