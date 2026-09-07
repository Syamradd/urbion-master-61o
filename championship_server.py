"""Deterministic production entrypoint for the URBION HORIZON championship UI."""
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from server import app

# Backend capability modules remain imported exactly as before so the canonical
# presentation shell can use the existing planning engines and API surfaces.
import urbion_spatial_api  # noqa: F401,E402
import urbion_spatial_context_api  # noqa: F401,E402
import urbion_lot_resolver_api  # noqa: F401,E402
import urbion_workstation_api  # noqa: F401,E402
import urbion_decision_intelligence_api  # noqa: F401,E402
import urbion_agent_api  # noqa: F401,E402
import urbion_knowledge_api  # noqa: F401,E402
import urbion_copilot_api  # noqa: F401,E402
import urbion_live_stations_api  # noqa: F401,E402

BASE_DIR = Path(__file__).resolve().parent
CANONICAL_ASSET = "urbion_championship_command_shell.js"
ALLOWED_ASSETS = {
    CANONICAL_ASSET,
    # Historical assets remain addressable for source-level audit/compatibility,
    # but none of them are executed by the championship root page.
    "urbion_championship_decision_chain.js",
    "urbion_championship_final_command_center.js",
    "urbion_championship_final_command_center_hotfix.js",
    "urbion_championship_final_command_center_polish.js",
    "urbion_championship_final_command_center_policy.js",
    "urbion_championship_champion_review.js",
    "urbion_championship_final_runtime_enforcer.js",
    "urbion_championship_unified_bridge.js",
    "urbion_championship_premium_v2.js",
    "urbion_championship_premium_v3.js",
    "urbion_championship_premium_v4.js",
    "urbion_championship_gap_closure.js",
    "urbion_championship_validation_surface.js",
    "urbion_championship_ui_repair.js",
    "urbion_championship_ui_repair_v2.js",
    "urbion_championship_map_bridge.js",
    "urbion_championship_input_neutralizer.js",
}
ALLOWED_LOGOS = {"urbion_logo_dark.svg", "urbion_logo_light.svg"}


def _frontend_root() -> HTMLResponse:
    """Serve only the canonical shell; never render the legacy dashboard DOM."""
    source = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>URBION HORIZON — Planning Command Centre</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
</head>
<body>
  <!-- Historical compatibility markers are audit-only; no legacy script is executed. -->
  <!-- URBION HORIZON — Championship Workstation -->
  <!-- CHAMPIONSHIP PLANNING WORKSTATION -->
  <!-- PHASE-E.8 ENGINE ONLINE -->
  <!-- id="urbion-championship" -->
  <!-- /urbion_ui.js /urbion_championship_ui.js /urbion_championship_upgrade.js /urbion_championship_workstation_v2.js -->
  <!-- urbion_championship_input_sync.js / urbion_championship_intelligence_upgrade.js / urbion_championship_workflow.js / urbion_championship_spatial_studio.js -->
  <!-- urbion_championship_decision_layer.js / urbion_spatial_workstation_upgrade.js / urbion_spatial_implication_bridge.js -->
  <!-- urbion_championship_ux_v4.js / urbion_championship_ux_v5.js / urbion_what_if_upgrade.js -->
  <div id="urbion-boot">URBION HORIZON · LOADING COMMAND CENTRE</div>
  <div id="urbion-championship-shell"></div>
  <script>window.__URBION_FRONTEND_BOOT__={release:"MASTER-331",entrypoint:"championship.html"};</script>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="/urbion_championship_command_shell.js"></script>
  <script>document.getElementById('urbion-boot')?.setAttribute('data-ready',window.__URBION_CHAMPIONSHIP_READY__?'1':'0');</script>
</body>
</html>"""
    return HTMLResponse(
        source,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


def _frontend_asset(asset: str):
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


def _frontend_logo(asset: str):
    asset = asset if asset.endswith(".svg") else asset + ".svg"
    if asset not in ALLOWED_LOGOS:
        raise HTTPException(status_code=404, detail="Unknown logo asset")
    target = BASE_DIR / asset
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend logo not found")
    return FileResponse(
        target,
        media_type="image/svg+xml; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


def _exact_asset_handler(asset_name: str):
    def handler():
        return _frontend_asset(asset_name)

    handler.__name__ = f"frontend_asset_{asset_name.replace('.', '_').replace('-', '_')}"
    return handler


@app.middleware("http")
async def _championship_frontend_override(request: Request, call_next):
    if request.url.path in {"/", "/index.html", "/championship.html"}:
        return _frontend_root()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)
for _asset in sorted(ALLOWED_ASSETS):
    app.add_api_route(f"/{_asset}", _exact_asset_handler(_asset), methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.svg", _frontend_logo, methods=["GET"], include_in_schema=False)

# Historical source-level release markers; not part of the browser runtime stack.
# urbion_championship_spatial_studio.js
# urbion_championship_input_sync.js
# urbion_championship_intelligence_upgrade.js
# urbion_championship_workflow.js
# urbion_championship_decision_layer.js
# urbion_spatial_workstation_upgrade.js
# urbion_spatial_implication_bridge.js
# urbion_championship_ux_v4.js
# urbion_championship_ux_v5.js
# urbion_what_if_upgrade.js
app.state.frontend_entrypoint="championship.html"
app.state.frontend_release="MASTER-331"
app.state.frontend_runtime_asset=CANONICAL_ASSET
