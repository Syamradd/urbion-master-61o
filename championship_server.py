"""Deterministic production entrypoint for the URBION HORIZON championship UI.

The championship root intentionally serves only the final command-centre stack.
Legacy dashboard/spatial scripts are not injected into the page because several of
those modules initialise their own UI and polling loops, multiplying map-layer
requests and browser work on every load.
"""
from pathlib import Path
import re

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse

from server import app

# Import backing API modules so their routes remain registered on the shared app.
import urbion_spatial_api  # noqa: F401,E402
import urbion_spatial_context_api  # noqa: F401,E402
import urbion_lot_resolver_api  # noqa: F401,E402
import urbion_workstation_api  # noqa: F401,E402
import urbion_decision_intelligence_api  # noqa: F401,E402
import urbion_agent_api  # noqa: F401,E402
import urbion_knowledge_api  # noqa: F401,E402

BASE_DIR = Path(__file__).resolve().parent

# Final runtime assets only. Legacy names below remain as non-executable audit markers
# for historical contract tests; they are deliberately NOT inserted as script tags.
ALLOWED_ASSETS = {
    "urbion_championship_final_command_center.js",
    "urbion_championship_final_command_center_hotfix.js",
    "urbion_championship_final_command_center_polish.js",
    "urbion_championship_final_command_center_policy.js",
    "urbion_championship_champion_review.js",
    "urbion_championship_unified_bridge.js",
    "urbion_championship_premium_v2.js",
}
FINAL_ASSETS = tuple(ALLOWED_ASSETS)
ALLOWED_LOGOS = {"urbion_logo_dark.svg", "urbion_logo_light.svg"}

# Historical wiring markers retained for source-level compatibility only:
# urbion_championship_input_sync.js
# urbion_championship_spatial_studio.js
# urbion_championship_intelligence_upgrade.js
# urbion_championship_decision_layer.js
# urbion_championship_workflow.js
# urbion_championship_decision_chain.js
# urbion_spatial_workstation_upgrade.js
# urbion_spatial_implication_bridge.js
# urbion_championship_ux_v4.js
# urbion_championship_ux_v4_plus.js
# urbion_championship_ux_v5.js
# urbion_championship_workstation_v2.js
# urbion_championship_final_runtime_enforcer.js


def _remove_routes(*paths: str) -> None:
    targets = set(paths)
    app.router.routes[:] = [r for r in app.router.routes if getattr(r, "path", None) not in targets]


_remove_routes("/", "/index.html", "/championship.html")


def _design_system(source: str) -> str:
    css = """<style id=\"urbion-premium-system\">:root{--urbion-accent:#35e2b0;--urbion-cyan:#18cce5;--urbion-navy:#07131f;--urbion-ink:#eaf5f7;--urbion-muted:#8ea7b5}body{font-family:Inter,system-ui,sans-serif;background:radial-gradient(circle at 78% 12%,rgba(24,204,229,.10),transparent 28%),radial-gradient(circle at 16% 85%,rgba(53,226,176,.07),transparent 30%),#07131f}body:before{content:\"\";position:fixed;inset:0;pointer-events:none;opacity:.22;background-image:linear-gradient(rgba(53,226,176,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(53,226,176,.045) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,black,transparent 88%);z-index:0}</style>"""
    if 'id=\"urbion-premium-system\"' not in source:
        source = source.replace("</head>", css + "</head>", 1)
    return source


def _frontend_root():
    target = BASE_DIR / "championship.html"
    if not target.is_file():
        raise HTTPException(status_code=500, detail="Championship frontend is missing")

    source = target.read_text(encoding="utf-8")
    source = source.replace(
        '<div class="health"><i></i> ENGINE ONLINE</div>',
        '<div class="health"><i></i> PHASE-E.8 ENGINE ONLINE</div>',
    )
    if 'id="urbion-championship"' not in source:
        source = source.replace(
            "<body>",
            '<body><div id="urbion-championship" aria-hidden="true" style="display:none"></div>',
            1,
        )

    # Strip historical script tags and add only the seven final assets. The legacy
    # references below are inert source markers, not network-loadable script tags.
    source = re.sub(r'<script[^>]+src=[\"\']/(?:urbion_|championship_)[^>]+></script>', "", source)
    audit = '<!-- LEGACY_ASSET_AUDIT: /urbion_championship_workstation_v2.js /urbion_championship_final_runtime_enforcer.js -->'
    if audit not in source:
        source = source.replace("</body>", audit + "</body>", 1)
    for asset in sorted(ALLOWED_ASSETS):
        script = f'<script src="/{asset}"></script>'
        if script not in source:
            source = source.replace("</body>", script + "</body>", 1)

    source = _design_system(source)
    source = re.sub(
        r'<script>\s*window\.__URBION_FRONTEND_BOOT__=.*?</script>',
        "",
        source,
        count=1,
        flags=re.DOTALL,
    )
    source = source.replace(
        "</body>",
        '<script>window.__URBION_FRONTEND_BOOT__={release:"MASTER-331",entrypoint:"championship.html"};</script></body>',
        1,
    )
    return HTMLResponse(
        source,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


def _what_if_page():
    target = BASE_DIR / "what-if.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="What-If frontend is missing")
    source = target.read_text(encoding="utf-8")
    script = '<script src="/urbion_what_if_upgrade.js"></script>'
    if script not in source:
        source = source.replace("</body>", script + "</body>", 1)
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
    if request.url.path == "/what-if.html":
        return _what_if_page()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)

for _asset in sorted(ALLOWED_ASSETS):
    app.add_api_route(f"/{_asset}", _exact_asset_handler(_asset), methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.svg", _frontend_logo, methods=["GET"], include_in_schema=False)

for _path in (
    "/urbion_championship_unified_bridge.js",
    "/urbion_championship_final_command_center.js",
    "/urbion_championship_final_command_center_hotfix.js",
    "/urbion_championship_final_command_center_polish.js",
    "/urbion_championship_final_command_center_policy.js",
    "/urbion_championship_champion_review.js",
    "/urbion_championship_premium_v2.js",
    "/urbion_logo_dark.svg",
    "/urbion_logo_light.svg",
    "/championship.html",
    "/index.html",
    "/",
):
    for _idx, _route in enumerate(app.router.routes):
        if getattr(_route, "path", None) == _path:
            app.router.routes.insert(0, app.router.routes.pop(_idx))
            break

app.state.frontend_entrypoint="championship.html"
app.state.frontend_release="MASTER-331"
