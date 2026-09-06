"""Canonical same-origin gateway for championship frontend assets.

This module is intentionally small and deterministic.  It puts explicit routes
for every allow-listed JavaScript asset ahead of legacy wildcard routes in
``server.py`` so production and TestClient resolve the same files.
"""
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse

from server import app

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_ASSETS = frozenset(
    {
        "urbion_ui.js",
        "urbion_championship_ui.js",
        "urbion_championship_upgrade.js",
        "urbion_championship_dashboard.js",
        "urbion_championship_polish.js",
        "urbion_championship_v279.js",
        "urbion_public_source_ui.js",
        "urbion_public_spatial_v283.js",
        "urbion_public_spatial_v284.js",
        "urbion_championship_spatial_studio.js",
        "urbion_championship_decision_layer.js",
        "urbion_championship_intelligence_upgrade.js",
        "urbion_championship_input_sync.js",
        "urbion_championship_workflow.js",
        "urbion_championship_decision_chain.js",
        "urbion_what_if_upgrade.js",
        "urbion_spatial_workstation_upgrade.js",
        "urbion_spatial_implication_bridge.js",
        "urbion_championship_workstation_v2.js",
        "urbion_decision_intelligence_ui.js",
    }
)


def _asset_response(asset: str):
    if asset not in ALLOWED_ASSETS:
        raise HTTPException(status_code=404, detail="Unknown frontend asset")
    target = BASE_DIR / asset
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend asset not found")
    return FileResponse(
        target,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


# Register explicit routes and move each to the front of the Starlette route
# table.  This is stronger than relying on a later wildcard route because the
# legacy server.py wildcard may otherwise consume these paths first.
for _asset in ALLOWED_ASSETS:
    _path = f"/{_asset}"
    app.add_api_route(
        _path,
        lambda asset=_asset: _asset_response(asset),
        methods=["GET"],
        include_in_schema=False,
    )
    _route = app.router.routes.pop()
    app.router.routes.insert(0, _route)

app.state.frontend_asset_gateway = "CANONICAL_EXPLICIT_ROUTES"
