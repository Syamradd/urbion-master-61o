"""Production entrypoint that adds a standalone URBION HORIZON welcome page.

The existing championship application is imported unchanged. Only the public
root entrypoint and the final language bootstrap are intercepted; the existing
planning application remains the canonical workstation at /championship.html.
"""
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse

from championship_server import app

BASE_DIR = Path(__file__).resolve().parent
LANDING_FILE = BASE_DIR / "landing.html"
LANGUAGE_BOOTSTRAP = BASE_DIR / "urbion_horizon_language_bootstrap.js"


@app.middleware("http")
async def _urbion_landing_override(request: Request, call_next):
    if request.url.path in {"/", "/index.html"}:
        if not LANDING_FILE.is_file():
            return HTMLResponse("URBION HORIZON landing page is missing.", status_code=500)
        return HTMLResponse(
            LANDING_FILE.read_text(encoding="utf-8"),
            media_type="text/html; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    if request.url.path == "/championship.html" and LANGUAGE_BOOTSTRAP.is_file():
        response = await call_next(request)
        if response.status_code == 200:
            body = getattr(response, "body", b"")
            if isinstance(body, bytes):
                html = body.decode("utf-8")
            else:
                html = str(body)
            marker = "</body>"
            script = '<script src="/urbion_horizon_language_bootstrap.js"></script>'
            if script not in html and marker in html:
                html = html.replace(marker, script + marker, 1)
            return HTMLResponse(
                html,
                status_code=response.status_code,
                media_type="text/html; charset=utf-8",
                headers={"Cache-Control": "no-store, max-age=0"},
            )
    return await call_next(request)
