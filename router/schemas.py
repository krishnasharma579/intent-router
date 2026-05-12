"""
Pydantic schemas for the Clob Intent Router.

This module defines the expected output structure from the LLM,
ensuring that the routing logic receives strictly typed and validated data.
"""

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class IntentResponse(BaseModel):
    """
    Schema to enforce structured JSON output from the routing LLM.
    The LLM must strictly choose one of the predefined intent categories.
    """
    
    # model_config helps in making the schema strictly validated and immutable.
    model_config = ConfigDict(
        frozen=True,
        extra='forbid'
    )

    # Using Literal forces the LLM to output ONLY one of these exact three strings.
    intent: Literal["hardware_query", "code_generation", "general_chat"] = Field(
        description=(
            "The classified intent of the user input. You must choose exactly one "
            "of the following: 'hardware_query', 'code_generation', or 'general_chat'."
        )
    )