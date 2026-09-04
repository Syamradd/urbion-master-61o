"""Deterministic production entrypoint for the URBION HORIZON championship UI.

This wrapper deliberately removes the legacy / and /index.html handlers from server.app
and installs the championship frontend as the production frontend surface. It also serves
allow-listed frontend assets directly, so the result does not depend on Python's optional
sitecustomize startup hook.
"""
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse

from server import app

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_ASSETS = {
    "urbion_ui.js",
    "urbion_championship_ui.js",
    "urbion_championship_upgrade.js",
    "urbion_championship_dashboard.js",
    "urbion_championship_polish.js",
    "urbion_championship_v279.js",
    "urbion_public_source_ui.js",
    "urbion_public_spatial_v283.js",
    "urbion_public_spatial_v284.js",
}


def _remove_routes(*paths: str) -> None:
    targets = set(paths)
    app.router.routes[:] = [
        route for route in app.router.routes
        if getattr(route, "path", None) not in targets
    ]


# server.py still owns all business/API routes, but its legacy HTML roots must not win.
_remove_routes("/", "/index.html")


def _frontend_root():
    target = BASE_DIR / "championship.html"
    if not target.is_file():
        raise HTTPException(status_code=500, detail="Championship frontend is missing")
    return FileResponse(
        target,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


def _frontend_asset(asset: str):
    filename = f"{asset}.js"
    if filename not in ALLOWED_ASSETS:
        raise HTTPException(status_code=404, detail="Unknown frontend asset")
    target = BASE_DIR / filename
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend asset not found")
    return FileResponse(
        target,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


# Middleware is intentional: it sits before Starlette's route matching, so a legacy
# static/catch-all handler can never shadow the championship /index.html compatibility URL.
@app.middleware("http")
async def _championship_frontend_override(request: Request, call_next):
    if request.url.path in {"/index.html", "/championship.html"}:
        return _frontend_root()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)

# Expose a production identity without changing the existing backend health contract.
app.state.frontend_entrypoint = "championship.html"
app.state.frontend_release = "MASTER-292"
