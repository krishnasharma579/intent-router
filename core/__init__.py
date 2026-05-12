"""
Core module for the Clob Intent Router.

This package centralizes application-wide configuration, environment 
management, and Language Model (LLM) initialization to ensure 
a consistent state across the system.
"""

from .config import settings
from .llm_setup import get_router_llm

# Exposing essential components at the package level.
# This allows cleaner imports like: from core import settings, get_router_llm
__all__ = [
    "settings",
    "get_router_llm",
]