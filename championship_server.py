"""Deterministic production entrypoint for the URBION HORIZON championship UI.

A fresh FastAPI application is assembled from the legacy API route table. This prevents
legacy root handlers and sitecustomize route injection from competing with the
championship frontend at ``/`` and ``/index.html``.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from server import app as legacy_app

BASE_DIR = Path(__file__).resolve().parent

# Build a clean application shell while preserving the established API route objects.
app = FastAPI(title="URBION API — Championship", version="PHASE-E.7")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# sitecustomize may inject a root route into every FastAPI instance. Remove all exact
# frontend surfaces before adding the deterministic championship implementation.
app.router.routes[:] = [
    route for route in legacy_app.router.routes
    if getattr(route, "path", None) not in {"/", "/index.html", "/championship.html"}
]

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


def _frontend_root():
    target = BASE_DIR / "championship.html"
    if not target.is_file():
        raise HTTPException(status_code=500, detail="Championship frontend is missing")
    source = target.read_text(encoding="utf-8")
    source = source.replace(
        '<div class="health"><i></i> ENGINE ONLINE</div>',
        '<div class="health"><i></i> PHASE-E.7 ENGINE ONLINE</div>',
    )
    return HTMLResponse(
        source,
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


@app.get("/", include_in_schema=False)
def championship_root():
    return _frontend_root()


@app.get("/index.html", include_in_schema=False)
def championship_index():
    return _frontend_root()


@app.get("/championship.html", include_in_schema=False)
def championship_html():
    return _frontend_root()


@app.get("/{asset}.js", include_in_schema=False)
def championship_asset(asset: str):
    return _frontend_asset(asset)


# Final precedence assertion at import time: exact frontend paths must resolve to the
# championship endpoint functions, never a legacy server root handler.
_FRONTEND_ENDPOINTS = {
    "/": championship_root,
    "/index.html": championship_index,
    "/championship.html": championship_html,
}
for _path, _endpoint in _FRONTEND_ENDPOINTS.items():
    _matches = [
        route for route in app.router.routes
        if getattr(route, "path", None) == _path
        and getattr(route, "endpoint", None) is _endpoint
    ]
    if not _matches:
        raise RuntimeError(f"Championship route registration failed for {_path}")

app.state.frontend_entrypoint = "championship.html"
app.state.frontend_release = "MASTER-296"
