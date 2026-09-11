"""URBION HORIZON public presentation entrypoint.

The existing FastAPI application and planning engines remain unchanged. This
adapter owns only the judge-facing presentation routes so legacy championship
frontend layers cannot be injected into the canonical pages.
"""
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse

from championship_server import app

BASE_DIR = Path(__file__).resolve().parent
ROUTES = {
    "/": BASE_DIR / "welcome.html",
    "/index.html": BASE_DIR / "welcome.html",
    "/about": BASE_DIR / "about.html",
    "/workspace": BASE_DIR / "workspace_v5.html",
}


def _serve(path: Path) -> HTMLResponse:
    if not path.is_file():
        return HTMLResponse(
            f"URBION HORIZON presentation asset missing: {path.name}",
            status_code=500,
        )
    return HTMLResponse(
        path.read_text(encoding="utf-8"),
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.middleware("http")
async def _urbion_canonical_presentation(request: Request, call_next):
    target = ROUTES.get(request.url.path)
    if target is not None:
        return _serve(target)
    return await call_next(request)
