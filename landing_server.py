"""Production entrypoint that adds a standalone URBION HORIZON welcome page.

The existing championship application is imported unchanged. Only the public
root entrypoint and the final language bootstrap are intercepted; the existing
planning application remains the canonical workstation at /championship.html.
"""
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse, Response

from championship_server import _frontend_root, app

BASE_DIR = Path(__file__).resolve().parent
LANDING_FILE = BASE_DIR / "landing.html"
LANGUAGE_BOOTSTRAP = BASE_DIR / "urbion_horizon_language_bootstrap.js"
HORIZON_UI_ASSET = BASE_DIR / "urbion_championship_horizon_ui.js"
HORIZON_H1_CONTRACT = "body.horizon-ui .hero h1{font-size:clamp(38px,4vw,58px)!important;line-height:1.03!important;"
HORIZON_H1_SAFE = "body.horizon-ui .hero h1{font-size:clamp(38px,4vw,58px)!important;line-height:1.12!important;"
HORIZON_H1_STYLE = "body.horizon-ui .hero h1{line-height:1.12!important;height:auto!important;min-height:0!important;overflow:visible!important;box-sizing:border-box!important;}"


def _canonical_championship_page() -> HTMLResponse:
    """Return the exact canonical workstation HTML plus the language bootstrap."""
    response = _frontend_root()
    body = getattr(response, "body", b"")
    if not isinstance(body, bytes):
        body = str(body).encode("utf-8")
    html = body.decode("utf-8")
    marker = "</body>"
    script = '<script src="/urbion_horizon_language_bootstrap.js"></script>'
    style = f'<style id="horizon-h1-visual-contract">{HORIZON_H1_STYLE}</style>'
    if script not in html and marker in html:
        html = html.replace(marker, script + style + marker, 1)
    elif marker in html and "horizon-h1-visual-contract" not in html:
        html = html.replace(marker, style + marker, 1)
    return HTMLResponse(
        html,
        status_code=response.status_code,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.middleware("http")
async def _urbion_landing_override(request: Request, call_next):
    if request.url.path in {"/", "/index.html"}:
        if not LANDING_FILE.is_file():
            return HTMLResponse("URBION HORIZON landing page is missing.", status_code=500)
        landing_html = LANDING_FILE.read_text(encoding="utf-8")
        # Preserve the existing landing asset verbatim while normalizing the
        # single known team-name capitalization typo at the served entrypoint.
        landing_html = landing_html.replace("Wan Nur Alea NajihaH", "Wan Nur Alea Najihah")
        return HTMLResponse(
            landing_html,
            media_type="text/html; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    if request.url.path == "/championship.html":
        return _canonical_championship_page()
    if request.url.path == "/urbion_horizon_language_bootstrap.js":
        if not LANGUAGE_BOOTSTRAP.is_file():
            return Response("URBION HORIZON language bootstrap is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        return Response(
            LANGUAGE_BOOTSTRAP.read_text(encoding="utf-8"),
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    if request.url.path == "/urbion_championship_horizon_ui.js":
        if not HORIZON_UI_ASSET.is_file():
            return Response("URBION HORIZON UI asset is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        payload = HORIZON_UI_ASSET.read_text(encoding="utf-8")
        # Keep the canonical UI asset unchanged on disk; only the production
        # entrypoint applies this surgical visual guard against 4px heading
        # clipping reported by the browser acceptance contract.
        if HORIZON_H1_CONTRACT not in payload:
            return Response("URBION HORIZON heading visual contract is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        payload = payload.replace(HORIZON_H1_CONTRACT, HORIZON_H1_SAFE, 1)
        return Response(
            payload,
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    return await call_next(request)
