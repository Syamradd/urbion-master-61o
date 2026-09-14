"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, routes, frontend owner,
or planning engine.
"""

from landing_server import app

__all__ = ["app"]
