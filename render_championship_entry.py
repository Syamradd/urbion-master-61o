"""Runtime entrypoint for the isolated URBION HORIZON visual-flow preview.

Keeps the existing application/analysis routes intact while replacing only the
three public frontend entry routes used by the landing -> workspace flow.
"""
from pathlib import Path

from fastapi.responses import FileResponse, HTMLResponse
from fastapi.routing import APIRoute

import championship_server as cs

app = cs.app
BASE_DIR = Path(__file__).resolve().parent


def _strip_frontend_override() -> None:
    """Remove only the middleware that hijacks / into the workspace shell."""
    kept = []
    for middleware in app.user_middleware:
        dispatch = getattr(middleware, "kwargs", {}).get("dispatch")
        if dispatch is cs._championship_frontend_override:
            continue
        kept.append(middleware)
    app.user_middleware = kept
    app.middleware_stack = None


def _remove_public_frontend_routes() -> None:
    paths = {"/", "/index.html", "/championship.html"}
    app.router.routes = [
        route for route in app.router.routes
        if not (isinstance(route, APIRoute) and route.path in paths)
    ]


def _landing() -> FileResponse:
    target = BASE_DIR / "index.html"
    return FileResponse(target, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _workspace() -> HTMLResponse:
    response = cs._frontend_root()
    body = response.body.decode("utf-8")
    marker = '<script src="/urbion_championship_horizon_ui.js"></script>'
    patch = marker + '\n  <script src="/urbion_championship_visual_system_v1.js"></script>'
    if marker in body and "urbion_championship_visual_system_v1.js" not in body:
        body = body.replace(marker, patch, 1)
    return HTMLResponse(body, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


_strip_frontend_override()
_remove_public_frontend_routes()
app.add_api_route("/", _landing, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _landing, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _workspace, methods=["GET"], include_in_schema=False)
