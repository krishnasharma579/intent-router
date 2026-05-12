"""
Configuration module for the Clob Intent Router.

Handles environment variable loading, parsing, and validation using Pydantic
to ensure the application starts with a consistent state.
"""

import logging
import os
from typing import Final

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Industry Standard Constants
DEFAULT_MODEL_NAME: Final = "llama-3.1-8b-instant"
DEFAULT_ROUTER_TEMPERATURE: Final = 0.0
MIN_TEMP: Final = 0.0
MAX_TEMP: Final = 2.0

class Settings(BaseModel):
    """
    Application settings schema with automated validation.
    """
    GROQ_API_KEY: str = Field(..., min_length=1)
    MODEL_NAME: str = Field(default=DEFAULT_MODEL_NAME)
    ROUTER_TEMPERATURE: float = Field(default=DEFAULT_ROUTER_TEMPERATURE)

    @field_validator("GROQ_API_KEY")
    @classmethod
    def validate_groq_api_key(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("GROQ_API_KEY cannot be empty or just whitespace.")
        return normalized

def _parse_router_temperature(raw_value: str) -> float:
    """Helper to safely parse and range-check the LLM temperature."""
    try:
        val = float(raw_value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Invalid temperature format: {raw_value!r}. Must be numeric.") from exc

    if not MIN_TEMP <= val <= MAX_TEMP:
        raise ValueError(f"ROUTER_TEMPERATURE must be in range [{MIN_TEMP}, {MAX_TEMP}]. Got: {val}")
    return val

def _load_settings() -> Settings:
    """
    Orchestrates the loading of environment variables into the Settings schema.
    """
    try:
        raw_temp = os.getenv("ROUTER_TEMPERATURE", str(DEFAULT_ROUTER_TEMPERATURE))
        
        return Settings(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            MODEL_NAME=os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME),
            ROUTER_TEMPERATURE=_parse_router_temperature(raw_temp),
        )
    except (ValidationError, ValueError) as exc:
        logger.error(f"Configuration Boot Error: {exc}")
        # Clean error message for the end user/developer
        raise RuntimeError(
            "FATAL: Application configuration failed. Please check your .env file "
            f"for GROQ_API_KEY and a valid ROUTER_TEMPERATURE ({MIN_TEMP}-{MAX_TEMP})."
        ) from exc

# Singleton instance for application-wide use
settings = _load_settings()