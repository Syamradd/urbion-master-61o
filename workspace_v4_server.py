"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, planning engine, or
frontend owner. It exposes the canonical About raster asset and normalises
legacy UI Yes/No values before they reach the strict planning API.
"""

import json
from pathlib import Path

from fastapi import Request
from fastapi.responses import FileResponse, Response

from landing_server import app

_BASE_DIR = Path(__file__).resolve().parent
_ABOUT_MASTER = _BASE_DIR / "about_master.png"


@app.middleware("http")
async def normalise_legacy_analysis_inputs(request: Request, call_next):
    """Keep the canonical /assess contract numeric while tolerating old UI values.

    Some production workspace controls can still submit ``Yes``/``No`` strings
    for optional numeric planning inputs. Those values mean that the field was
    presented/affirmed, not that a numeric dimension is known. Preserve that
    distinction by converting such legacy values to ``None`` so the analysis can
    run and the rule engine can honestly surface the missing metric as review.
    """
    if request.method == "POST" and request.url.path == "/assess":
        content_type = (request.headers.get("content-type") or "").lower()
        if "application/json" in content_type:
            body = await request.body()
            try:
                payload = json.loads(body.decode("utf-8"))
                if isinstance(payload, dict):
                    for key in ("perimeter_planting", "landscaped_pedestrian_walkway"):
                        value = payload.get(key)
                        if isinstance(value, str):
                            token = value.strip().lower()
                            if token in {"yes", "no", "n/a", "na", "not provided", "not verified", ""}:
                                payload[key] = None
                            else:
                                try:
                                    payload[key] = float(value)
                                except (TypeError, ValueError):
                                    pass
                    body = json.dumps(payload).encode("utf-8")
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass

            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}

            request = Request(request.scope, receive)

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
