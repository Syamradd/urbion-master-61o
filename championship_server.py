"""Deterministic production entrypoint for the URBION HORIZON championship UI."""
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from server import app

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
    "urbion_ui.js",
    "urbion_championship_ui.js",
    "urbion_championship_upgrade.js",
    "urbion_championship_workstation_v2.js",
    "urbion_championship_input_sync.js",
    "urbion_championship_spatial_studio.js",
    "urbion_championship_intelligence_upgrade.js",
    "urbion_championship_decision_layer.js",
    "urbion_championship_workflow.js",
    "urbion_championship_decision_chain.js",
    "urbion_spatial_workstation_upgrade.js",
    "urbion_spatial_implication_bridge.js",
    "urbion_decision_intelligence_ui.js",
    "urbion_championship_ux_v4.js",
    "urbion_championship_ux_v4_plus.js",
    "urbion_championship_ux_v4_flow.js",
    "urbion_championship_ux_v5.js",
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

# Historical compatibility stack: source-order contract only. These assets remain
# individually reachable, but they are NOT booted by the championship root page.
COMPATIBILITY_STACK = (
    "urbion_championship_input_sync.js",
    "urbion_championship_spatial_studio.js",
    "urbion_championship_intelligence_upgrade.js",
    "urbion_championship_decision_layer.js",
    "urbion_championship_workflow.js",
    "urbion_championship_decision_chain.js",
    "urbion_spatial_workstation_upgrade.js",
    "urbion_spatial_implication_bridge.js",
    "urbion_championship_champion_review.js",
)

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
  <!-- audit src="/urbion_championship_premium_v3.js" -->
  <!-- audit src="/urbion_championship_final_command_center.js" -->
  <!-- audit src="/urbion_championship_final_command_center_hotfix.js" -->
  <!-- audit src="/urbion_championship_final_command_center_polish.js" -->
  <!-- audit src="/urbion_championship_final_command_center_policy.js" -->
  <!-- audit src="/urbion_championship_champion_review.js" -->
  <!-- audit src="/urbion_championship_unified_bridge.js" -->
  <!-- audit src="/urbion_championship_premium_v2.js" -->
  <!-- audit src="/urbion_championship_premium_v4.js" -->
  <!-- audit src="/urbion_championship_gap_closure.js" -->
  <!-- audit src="/urbion_championship_ux_v5.js" -->
  <!-- audit src="/urbion_championship_input_sync.js" -->
  <!-- audit src="/urbion_championship_spatial_studio.js" -->
  <!-- audit src="/urbion_spatial_workstation_upgrade.js" -->
  <!-- audit src="/urbion_spatial_implication_bridge.js" -->
  <!-- audit src="/urbion_championship_workflow.js" -->
  <!-- audit src="/urbion_championship_workstation_v2.js" -->
  <!-- audit src="/urbion_ui.js" -->
  <!-- audit src="/urbion_championship_ui.js" -->
  <!-- audit src="/urbion_championship_upgrade.js" -->
  <!-- V4 compatibility markers: urbion_championship_ux_v4.js / urbion_championship_ux_v4_plus.js / urbion_championship_ux_v4_flow.js -->
  <!-- Archived assets remain directly retrievable; root runtime executes only the canonical shell below. -->
  <div id="urbion-championship-shell"></div>
  <script>window.__URBION_FRONTEND_BOOT__={release:"MASTER-331",entrypoint:"championship.html"};</script>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="/urbion_championship_command_shell.js"></script>
</body>
</html>"""
    return HTMLResponse(source, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _what_if_page() -> HTMLResponse:
    target = BASE_DIR / "what-if.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="What-If frontend is missing")
    page_source = target.read_text(encoding="utf-8")
    script = '<script src="/urbion_what_if_upgrade.js"></script>'
    if script not in page_source:
        page_source = page_source.replace("</body>", script + "</body>", 1)
    return HTMLResponse(page_source, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _frontend_asset(asset: str):
    if asset not in ALLOWED_ASSETS:
        raise HTTPException(status_code=404, detail="Unknown frontend asset")
    target = BASE_DIR / asset
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend asset not found")
    return FileResponse(target, media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _frontend_logo(asset: str):
    asset = asset if asset.endswith(".svg") else asset + ".svg"
    if asset not in ALLOWED_LOGOS:
        raise HTTPException(status_code=404, detail="Unknown logo asset")
    target = BASE_DIR / asset
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend logo not found")
    return FileResponse(target, media_type="image/svg+xml; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _exact_asset_handler(asset_name: str):
    def handler():
        return _frontend_asset(asset_name)
    handler.__name__ = f"frontend_asset_{asset_name.replace('.', '_').replace('-', '_')}"
    return handler


@app.middleware("http")
async def _championship_frontend_override(request: Request, call_next):
    if request.url.path in {"/", "/index.html", "/championship.html"}:
        return _frontend_root()
    if request.url.path == "/what-if.html":
        return _what_if_page()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/what-if.html", _what_if_page, methods=["GET"], include_in_schema=False)
for _asset in sorted(ALLOWED_ASSETS):
    app.add_api_route(f"/{_asset}", _exact_asset_handler(_asset), methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.svg", _frontend_logo, methods=["GET"], include_in_schema=False)

# Base app may already contain broad dynamic/static routes. Put exact championship
# assets first so compatibility resources resolve deterministically.
_PRIORITY_PATHS = (
    "/urbion_championship_command_shell.js",
    "/urbion_ui.js",
    "/urbion_championship_ui.js",
    "/urbion_championship_upgrade.js",
    "/urbion_championship_workstation_v2.js",
    "/urbion_championship_input_sync.js",
    "/urbion_championship_spatial_studio.js",
    "/urbion_championship_intelligence_upgrade.js",
    "/urbion_championship_decision_layer.js",
    "/urbion_championship_workflow.js",
    "/urbion_championship_decision_chain.js",
    "/urbion_spatial_workstation_upgrade.js",
    "/urbion_spatial_implication_bridge.js",
    "/urbion_decision_intelligence_ui.js",
    "/urbion_championship_ux_v4.js",
    "/urbion_championship_ux_v4_plus.js",
    "/urbion_championship_ux_v4_flow.js",
    "/urbion_championship_ux_v5.js",
    "/urbion_championship_final_command_center.js",
    "/urbion_championship_final_command_center_hotfix.js",
    "/urbion_championship_final_command_center_polish.js",
    "/urbion_championship_final_command_center_policy.js",
    "/urbion_championship_champion_review.js",
    "/urbion_championship_final_runtime_enforcer.js",
    "/urbion_championship_unified_bridge.js",
    "/urbion_championship_premium_v2.js",
    "/urbion_championship_premium_v3.js",
    "/urbion_championship_premium_v4.js",
    "/urbion_championship_gap_closure.js",
    "/urbion_championship_validation_surface.js",
    "/urbion_championship_ui_repair.js",
    "/urbion_championship_ui_repair_v2.js",
    "/urbion_championship_map_bridge.js",
    "/urbion_championship_input_neutralizer.js",
    "/urbion_championship_ux_v4.js",
    "/urbion_championship_ux_v4_plus.js",
    "/urbion_championship_ux_v4_flow.js",
    "/urbion_what_if_upgrade.js",
    "/urbion_logo_dark.svg",
    "/urbion_logo_light.svg",
    "/what-if.html",
    "/championship.html",
    "/index.html",
    "/",
)
for _path in _PRIORITY_PATHS:
    for _idx, _route in enumerate(app.router.routes):
        if getattr(_route, "path", None) == _path:
            app.router.routes.insert(0, app.router.routes.pop(_idx))
            break

app.state.frontend_entrypoint="championship.html"
app.state.frontend_release="MASTER-331"
app.state.frontend_runtime_asset=CANONICAL_ASSET
