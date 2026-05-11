"""
Core module for Clob Intent Router.

This module is responsible for application-wide configuration, 
environment variable management, and Language Model (LLM) initialization.
"""

# __all__ restricts what gets imported when someone uses `from core import *`.
# It is a standard industry practice to keep the namespace clean and prevent 
# accidental imports of internal functions or variables.

__all__ = []

# NOTE: As we build `config.py` and `llm_setup.py`, we will expose their main 
# functions here.
# Example future state:
# from .config import settings
# from .llm_setup import get_router_llm
# __all__ = ["settings", "get_router_llm"]