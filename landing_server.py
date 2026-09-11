"""URBION HORIZON public presentation entrypoint.

The existing FastAPI application and planning engines remain unchanged. This
adapter owns only the judge-facing presentation routes so legacy championship
frontend layers cannot be injected into the canonical pages.
"""
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse, Response

from championship_server import app

BASE_DIR = Path(__file__).resolve().parent
WELCOME_FILE = BASE_DIR / "welcome.html"
ABOUT_FILE = BASE_DIR / "urbion_horizon_about.html"
WORKSPACE_FILE = BASE_DIR / "workspace_v5.html"
WORKSPACE_JS = BASE_DIR / "urbion_workspace_final.js"


def _html(path: Path) -> HTMLResponse:
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


def _workspace() -> HTMLResponse:
    if not WORKSPACE_FILE.is_file():
        return HTMLResponse(
            "URBION HORIZON workspace asset missing: workspace_v5.html",
            status_code=500,
        )
    if not WORKSPACE_JS.is_file():
        return HTMLResponse(
            "URBION HORIZON function layer missing: urbion_workspace_final.js",
            status_code=500,
        )
    html = WORKSPACE_FILE.read_text(encoding="utf-8")
    script = '<script src="/urbion_workspace_final.js"></script>'
    if script not in html and "</body>" in html:
        html = html.replace("</body>", script + "</body>", 1)
    return HTMLResponse(
        html,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.middleware("http")
async def _urbion_canonical_presentation(request: Request, call_next):
    path = request.url.path
    if path in {"/", "/index.html"}:
        return _html(WELCOME_FILE)
    if path == "/about":
        return _html(ABOUT_FILE)
    if path == "/workspace":
        return _workspace()
    if path == "/urbion_workspace_final.js":
        if not WORKSPACE_JS.is_file():
            return Response(
                "URBION HORIZON function layer missing.",
                status_code=500,
                media_type="text/plain; charset=utf-8",
            )
        return Response(
            WORKSPACE_JS.read_text(encoding="utf-8"),
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    return await call_next(request)
