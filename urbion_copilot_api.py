"""Compatibility module for the unified bounded planner copilot.

The production ``/copilot/run`` route is owned by ``urbion_agent_api.py``.
This module remains import-safe for existing application startup contracts but
intentionally does not register a second route, avoiding duplicate FastAPI
endpoint definitions. The shared ``build_copilot_packet`` implementation is
still imported for compatibility and direct module access.
"""
from urbion_copilot import build_copilot_packet

__all__ = ["build_copilot_packet"]
