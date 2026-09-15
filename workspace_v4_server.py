"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, planning engine, or
frontend owner. It only exposes the canonical About raster asset required by the
existing About HTML.
"""

from pathlib import Path

from fastapi.responses import FileResponse, Response

from landing_server import app

_BASE_DIR = Path(__file__).resolve().parent
_ABOUT_MASTER = _BASE_DIR / "about_master.png"


@app.get("/about_master.png", include_in_schema=False)
def about_master():
    if not _ABOUT_MASTER.is_file():
        return Response(
            "URBION HORIZON canonical About visual master missing.",
            status_code=500,
            media_type="text/plain; charset=utf-8",
        )
    return FileResponse(
        _ABOUT_MASTER,
        media_type="image/png",
        headers={"Cache-Control": "no-store, max-age=0, must-revalidate"},
    )


__all__ = ["app"]
