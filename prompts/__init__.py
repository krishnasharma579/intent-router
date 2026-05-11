"""
Prompts initialization module for the Clob Intent Router.

This module exposes the system prompts required by the routing engine,
ensuring clean and centralized imports across the application.
"""

from .system_prompt import ROUTER_SYSTEM_PROMPT

# Restrict the public API to only the necessary prompt strings
__all__ = [
    "ROUTER_SYSTEM_PROMPT"
]