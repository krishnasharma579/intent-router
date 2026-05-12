"""
Prompts initialization module for the Clob Intent Router.

This package centralizes all prompt templates used by the routing engine, 
ensuring consistent behavior and making it easier to manage future 
prompt iterations (e.g., Coder or RAG prompts).
"""

from .system_prompt import ROUTER_SYSTEM_PROMPT

# Public API for the prompts package.
# Adding more prompts here as the project grows will keep the root imports clean.
__all__ = [
    "ROUTER_SYSTEM_PROMPT"
]