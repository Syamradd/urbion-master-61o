"""Production entrypoint that adds a standalone URBION HORIZON welcome page.

The existing championship application is imported unchanged. Only the public
root entrypoint and the canonical workstation presentation layer are intercepted.
"""
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse, Response

from championship_server import _frontend_root, app

BASE_DIR = Path(__file__).resolve().parent
LANDING_FILE = BASE_DIR / "urbion_horizon_landing.html"
LANGUAGE_BOOTSTRAP = BASE_DIR / "urbion_horizon_language_bootstrap.js"
HORIZON_UI_ASSET = BASE_DIR / "urbion_championship_horizon_ui.js"
VISUAL_V1 = BASE_DIR / "urbion_championship_visual_system_v1.js"
VISUAL_OVERHAUL = BASE_DIR / "urbion_horizon_visual_overhaul.js"
VISUAL_V2 = BASE_DIR / "urbion_championship_visual_system_v2.js"
LAYER_TOGGLE_REPAIR = BASE_DIR / "urbion_layer_toggle_repair.js"
HORIZON_H1_CONTRACT = "body.horizon-ui .hero h1{font-size:clamp(38px,4vw,58px)!important;line-height:1.03!important;"
HORIZON_H1_SAFE = "body.horizon-ui .hero h1{font-size:clamp(38px,4vw,58px)!important;line-height:1.2!important;"
HORIZON_H1_STYLE = "body.horizon-ui .hero h1{line-height:1.2!important;height:auto!important;min-height:0!important;overflow:visible!important;box-sizing:border-box!important;}"
MAP_SIZE_STYLE = "body.horizon-ui .map-panel-canonical .leaflet-container{height:clamp(520px,62vh,760px)!important;min-height:500px!important;}@media(max-width:1120px){body.horizon-ui .map-panel-canonical .leaflet-container{height:600px!important;min-height:520px!important;}}@media(max-width:760px){body.horizon-ui .map-panel-canonical .leaflet-container{height:540px!important;min-height:0!important;}}"


def _canonical_championship_page() -> HTMLResponse:
    response = _frontend_root()
    body = getattr(response, "body", b"")
    if not isinstance(body, bytes):
        body = str(body).encode("utf-8")
    html = body.decode("utf-8")
    marker = "</body>"
    if marker in html:
        if "urbion_championship_visual_system_v1.js" not in html:
            html = html.replace(marker, '<script src="/urbion_championship_visual_system_v1.js"></script>' + marker, 1)
        if "urbion_horizon_visual_overhaul.js" not in html:
            html = html.replace(marker, '<script src="/urbion_horizon_visual_overhaul.js"></script>' + marker, 1)
        if "urbion_championship_visual_system_v2.js" not in html:
            html = html.replace(marker, '<script src="/urbion_championship_visual_system_v2.js"></script>' + marker, 1)
        if "urbion_horizon_language_bootstrap.js" not in html:
            html = html.replace(marker, '<script src="/urbion_horizon_language_bootstrap.js"></script>' + marker, 1)
        if "urbion_layer_toggle_repair.js" not in html:
            html = html.replace(marker, '<script src="/urbion_layer_toggle_repair.js"></script>' + marker, 1)
        if "horizon-h1-visual-contract" not in html:
            html = html.replace(marker, f'<style id="horizon-h1-visual-contract">{HORIZON_H1_STYLE}</style>' + marker, 1)
        if "horizon-map-size-visual-contract" not in html:
            html = html.replace(marker, f'<style id="horizon-map-size-visual-contract">{MAP_SIZE_STYLE}</style>' + marker, 1)
    for asset in (VISUAL_V1, VISUAL_OVERHAUL, VISUAL_V2, LAYER_TOGGLE_REPAIR):
        if not asset.is_file():
            return HTMLResponse(f"URBION HORIZON presentation asset missing: {asset.name}", status_code=500)
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
        visual_script = '<script src="/urbion_horizon_visual_overhaul.js"></script>'
        if visual_script not in landing_html and "</body>" in landing_html:
            landing_html = landing_html.replace("</body>", visual_script + "</body>", 1)
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
        return Response(LANGUAGE_BOOTSTRAP.read_text(encoding="utf-8"), media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    if request.url.path == "/urbion_championship_visual_system_v1.js":
        if not VISUAL_V1.is_file():
            return Response("Visual system v1 is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        return Response(VISUAL_V1.read_text(encoding="utf-8"), media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    if request.url.path == "/urbion_horizon_visual_overhaul.js":
        if not VISUAL_OVERHAUL.is_file():
            return Response("Visual overhaul is missing.", status_code=500, media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
        return Response(VISUAL_OVERHAUL.read_text(encoding="utf-8"), media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    if request.url.path == "/urbion_championship_visual_system_v2.js":
        if not VISUAL_V2.is_file():
            return Response("Visual system v2 is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        return Response(VISUAL_V2.read_text(encoding="utf-8"), media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    if request.url.path == "/urbion_layer_toggle_repair.js":
        if not LAYER_TOGGLE_REPAIR.is_file():
            return Response("Layer toggle repair asset is missing.", status_code=500, media_type="application/javascript; charset=utf-8")
        return Response(LAYER_TOGGLE_REPAIR.read_text(encoding="utf-8"), media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    if request.url.path == "/urbion_championship_horizon_ui.js":
        if not HORIZON_UI_ASSET.is_file():
            return Response("URBION HORIZON UI asset is missing.", status_code=500, media_type="application/javascript; charset=utf-8")
        payload = HORIZON_UI_ASSET.read_text(encoding="utf-8")
        if HORIZON_H1_CONTRACT not in payload:
            return Response("URBION HORIZON heading visual contract is missing.", status_code=500, media_type="text/plain; charset=utf-8")
        payload = payload.replace(HORIZON_H1_CONTRACT, HORIZON_H1_SAFE, 1)
        return Response(payload, media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
    return await call_next(request)
