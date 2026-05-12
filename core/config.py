import logging
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "llama-3.1-8b-instant"
DEFAULT_ROUTER_TEMPERATURE = 0.0


class Settings(BaseModel):
    """Application settings with environment variable validation."""

    GROQ_API_KEY: str = Field(min_length=1)
    MODEL_NAME: str = DEFAULT_MODEL_NAME
    ROUTER_TEMPERATURE: float = Field(default=DEFAULT_ROUTER_TEMPERATURE, ge=0.0, le=1.0)

    @field_validator("GROQ_API_KEY")
    @classmethod
    def validate_groq_api_key(cls, value: str) -> str:
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("GROQ_API_KEY cannot be empty.")
        return normalized_value


def _parse_router_temperature(raw_value: str) -> float:
    try:
        return float(raw_value)
    except ValueError as exc:
        raise ValueError(
            "Invalid ROUTER_TEMPERATURE value. Expected a number between 0.0 and 1.0."
        ) from exc


def _load_settings() -> Settings:
    raw_temperature = os.getenv("ROUTER_TEMPERATURE", str(DEFAULT_ROUTER_TEMPERATURE))
    try:
        return Settings(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            MODEL_NAME=os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME),
            ROUTER_TEMPERATURE=_parse_router_temperature(raw_temperature),
        )
    except ValidationError as exc:
        logger.error("Configuration validation failed.")
        raise ValueError(
            "Configuration error: set GROQ_API_KEY and ensure ROUTER_TEMPERATURE is between 0.0 and 1.0."
        ) from exc


settings = _load_settings()
