import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

# Load environment variables from the .env file
load_dotenv()

class Settings(BaseModel):
    """
    Application settings and environment variables validation.
    This ensures that all required API keys are present before the application starts.
    """
    GROQ_API_KEY: str
    MODEL_NAME: str = "llama-3.1-8b-instant"
    ROUTER_TEMPERATURE: float = 0.0

try:
    # Initialize settings and validate environment variables
    # We fetch values from os.environ, falling back to defaults where applicable
    settings = Settings(
        GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
        MODEL_NAME=os.getenv("MODEL_NAME", "llama3-8b-8192"),
        ROUTER_TEMPERATURE=float(os.getenv("ROUTER_TEMPERATURE", "0.0"))
    )
except ValidationError as e:
    raise ValueError(
        "CRITICAL ERROR: Missing GROQ_API_KEY in .env file. "
        "Please get it from console.groq.com and add it."
    ) from e