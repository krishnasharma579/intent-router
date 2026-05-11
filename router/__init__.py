"""
Router module for the Clob Intent Router.

This package contains the core classification engine, schemas, and logic 
required to route user queries to the appropriate specialized agents 
(e.g., hardware retrieval, code generation, or general chat).
"""

# Import the main functionalities that should be exposed to the outside world
from .classifier import classify_intent
from .schemas import IntentResponse

# Restrict the module's public API to only these essential components
__all__ = [
    "classify_intent",
    "IntentResponse"
]