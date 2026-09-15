"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, planning engine, or
frontend owner. It only exposes the canonical About raster asset required by the
existing About HTML and normalizes a legacy UI payload shape before assessment.
"""

import json
from pathlib import Path

from fastapi import Request
from fastapi.responses import FileResponse, Response

from landing_server import app

_BASE_DIR = Path(__file__).resolve().parent
_ABOUT_MASTER = _BASE_DIR / "about_master.png"


_LEGACY_BOOLEAN_FIELDS = {
    "perimeter_planting",
    "landscaped_pedestrian_walkway",
}


def _normalise_legacy_inputs(payload: object) -> object:
    """Convert legacy Yes/No/blank values to nullable numeric assessment inputs.

    The current assessment contract expects metres as numbers. Older workspace
    controls could emit Yes/No strings for these controls, which must not block
    the canonical analysis path. Unknown values are preserved so the canonical
    validation layer can still report them honestly.
    """
    if not isinstance(payload, dict):
        return payload
    out = dict(payload)
    for key in _LEGACY_BOOLEAN_FIELDS:
        if key not in out:
            continue
        value = out[key]
        if isinstance(value, str):
            token = value.strip().lower()
            if token in {"", "yes", "no", "n/a", "na", "not verified", "unverified"}:
                out[key] = None
            else:
                try:
                    out[key] = float(token)
                except ValueError:
                    pass
    return out


@app.middleware("http")
async def _normalise_legacy_analysis_payload(request: Request, call_next):
    if request.method == "POST" and request.url.path in {"/assess", "/workstation/analysis"}:
        raw = await request.body()
        if raw:
            try:
                payload = json.loads(raw.decode("utf-8"))
                normalised = _normalise_legacy_inputs(payload)
                if normalised != payload:
                    request._body = json.dumps(normalised, separators=(",", ":")).encode("utf-8")
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass
    return await call_next(request)


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
