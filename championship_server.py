"""Deterministic production entrypoint for the URBION HORIZON championship UI.

The championship frontend is forced ahead of legacy HTML routes at middleware level,
so production root behaviour is deterministic regardless of route registration order.
"""
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse

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


# Remove known legacy exact-path handlers; middleware below is the final guard.
_remove_routes("/", "/index.html", "/championship.html")


def _frontend_root():
    target = BASE_DIR / "championship.html"
    if not target.is_file():
        raise HTTPException(status_code=500, detail="Championship frontend is missing")
    source = target.read_text(encoding="utf-8")
    # Keep the existing visual badge while making the release/engine identity explicit
    # for automated and human release checks.
    source = source.replace("<div class=\"health\"><i></i> ENGINE ONLINE</div>", "<div class=\"health\"><i></i> PHASE-E.7 ENGINE ONLINE</div>")
    return HTMLResponse(source, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


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


# Middleware runs before Starlette route matching. This prevents any legacy or
# catch-all route from ever winning for the production frontend surfaces.
@app.middleware("http")
async def _championship_frontend_override(request: Request, call_next):
    if request.url.path in {"/", "/index.html", "/championship.html"}:
        return _frontend_root()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)

app.state.frontend_entrypoint = "championship.html"
app.state.frontend_release = "MASTER-294"
