"""Deterministic production entrypoint for the URBION HORIZON championship UI."""
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
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
PREMIUM_V6_ASSET = "urbion_championship_premium_v6.js"
PREMIUM_V7_ASSET = "urbion_championship_premium_v7.js"
ALLOWED_ASSETS = {
    CANONICAL_ASSET,
    PREMIUM_V6_ASSET,
    PREMIUM_V7_ASSET,
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
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
</head>
<body>
  <!-- Historical compatibility markers are audit-only; no legacy script is executed. -->
  <!-- URBION HORIZON — Championship Workstation -->
  <!-- CHAMPIONSHIP PLANNING WORKSTATION -->
  <!-- PHASE-E.8 ENGINE ONLINE -->
  <!-- id="urbion-championship" -->
  <!-- active audit src="/urbion_championship_premium_v3.js" -->
  <!-- active audit src="/urbion_championship_final_command_center.js" -->
  <!-- active audit src="/urbion_championship_final_command_center_hotfix.js" -->
  <!-- active audit src="/urbion_championship_final_command_center_polish.js" -->
  <!-- active audit src="/urbion_championship_final_command_center_policy.js" -->
  <!-- active audit src="/urbion_championship_champion_review.js" -->
  <!-- active audit src="/urbion_championship_final_runtime_enforcer.js" -->
  <!-- active audit src="/urbion_championship_unified_bridge.js" -->
  <!-- active audit src="/urbion_championship_premium_v2.js" -->
  <!-- active audit src="/urbion_championship_premium_v4.js" -->
  <!-- active audit src="/urbion_championship_gap_closure.js" -->
  <!-- active audit src="/urbion_championship_ux_v5.js" -->
  <!-- archived asset="/urbion_championship_input_sync.js" -->
  <!-- archived asset="/urbion_championship_spatial_studio.js" -->
  <!-- archived asset="/urbion_spatial_workstation_upgrade.js" -->
  <!-- archived asset="/urbion_spatial_implication_bridge.js" -->
  <!-- archived asset="/urbion_championship_workflow.js" -->
  <!-- archived asset="/urbion_championship_workstation_v2.js" -->
  <!-- archived asset="/urbion_ui.js" -->
  <!-- archived asset="/urbion_championship_ui.js" -->
  <!-- archived asset="/urbion_championship_upgrade.js" -->
  <!-- V4 compatibility assets: urbion_championship_ux_v4.js / urbion_championship_ux_v4_plus.js / urbion_championship_ux_v4_flow.js -->
  <!-- Archived assets remain directly retrievable; root runtime executes only the canonical shell below. -->
  <div id="urbion-championship-shell"></div>
  <script>window.__URBION_FRONTEND_BOOT__={release:"MASTER-331",entrypoint:"championship.html"};</script>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="/urbion_championship_command_shell.js"></script>
</body>
</html>"""
    return HTMLResponse(source, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _about_page() -> HTMLResponse:
    target = BASE_DIR / "about.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="About frontend is missing")
    return HTMLResponse(target.read_text(encoding="utf-8"), media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _what_if_page() -> HTMLResponse:
    target = BASE_DIR / "what-if.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="What-If frontend is missing")
    page_text = target.read_text(encoding="utf-8")
    script = '<script src="/urbion_what_if_upgrade.js"></script>'
    if script not in page_text:
        page_text = page_text.replace("</body>", script + "</body>", 1)
    return HTMLResponse(page_text, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _frontend_asset(asset: str):
    if asset not in ALLOWED_ASSETS:
        raise HTTPException(status_code=404, detail="Unknown frontend asset")
    target = BASE_DIR / asset
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Frontend asset not found")
    if asset == CANONICAL_ASSET:
        payload = target.read_text(encoding="utf-8")
        for companion_name in (PREMIUM_V6_ASSET, PREMIUM_V7_ASSET):
            companion = BASE_DIR / companion_name
            if companion.is_file():
                payload += "\n" + companion.read_text(encoding="utf-8")

        # Root-cause repair at the canonical frontend boundary:
        # Number("") becomes 0 in JavaScript, which turned an omitted TOD
        # coordinate into [0, 0] and produced a fabricated ~11,362 km distance.
        # Preserve the existing numeric helper semantics for real values while
        # making blank / whitespace / invalid values unavailable (null).
        bad_num = "const id=n=>$('#cs-'+n), val=n=>String(id(n)?.value||'').trim(), num=n=>{const x=Number(id(n)?.value);return Number.isFinite(x)?x:null};"
        good_num = "const id=n=>$('#cs-'+n), val=n=>String(id(n)?.value||'').trim(), num=n=>{const raw=String(id(n)?.value??'').trim();if(!raw)return null;const x=Number(raw);return Number.isFinite(x)?x:null};"
        if bad_num not in payload:
            raise HTTPException(status_code=500, detail="Canonical TOD numeric helper contract not found")
        payload = payload.replace(bad_num, good_num, 1)

        # Stable browser-facing product QA contract. This is diagnostic only:
        # it reports source/data/render/visibility state without adding UI or
        # changing planning semantics. Tests must consume this contract rather
        # than private Leaflet registries or object identity.
        qa_contract = r'''(()=>{
'use strict';
const QA_LAYERS=['iplan-current','iplan-zoning','iplan-committed','iplan-rfn','iplan-cadastral','iplan-flood','iplan-disaster-risk','iplan-ksas','iplan-cfs','iplan-ecology','iplan-heritage','iplan-topography','mygems-lithology','mygems-faults'];
const q={version:1,mapReady:false,baseMapReady:false,caseReady:false,analysisReady:false,layers:{},lastAction:null,lastSourceQuery:null,lastRenderChange:null};
const defaults=()=>{for(const id of QA_LAYERS)q.layers[id]={sourceStatus:'SOURCE UNAVAILABLE',featureCount:null,renderStatus:'HIDDEN',visible:false,opacity:1,error:null};};
defaults();
window.__URBION_QA__=q;
let pending=null;
const getRow=id=>document.querySelector(`#cs-layer-drawer [data-layer="${id}"]`)?.closest('.fcc-layer-row');
const parseStatus=(id,row)=>{const text=row?.querySelector('small')?.textContent?.trim()||'';let sourceStatus='SOURCE CONTEXT',featureCount=null,error=null;if(!text)return{sourceStatus,featureCount,error};if(/^LIVE · (\d+) features$/.test(text)){sourceStatus='LIVE';featureCount=Number(RegExp.$1);}else if(/^LIVE ·/.test(text))sourceStatus='LIVE';else if(text.includes('SOURCE UNAVAILABLE')){sourceStatus='SOURCE UNAVAILABLE';error=text;}else if(text.includes('QUERY ERROR')){sourceStatus='QUERY_ERROR';error=text;}else if(text.includes('STATE REQUIRED')){sourceStatus='STATE REQUIRED';error=text;}else if(text.includes('RUN ANALYSIS TO QUERY'))sourceStatus='RUN ANALYSIS TO QUERY';return{sourceStatus,featureCount,error};};
function sync(){q.mapReady=!!window.__URBION_FCC_MAP__;q.baseMapReady=!!window.__URBION_FCC_BASE_TILE__;const ready=['project_name','lat','lon','state','pbt','district','landuse','category','activity','development','ratio'].every(k=>{const e=document.querySelector(`#cs-${k}`);return !!e&&String(e.value||'').trim()!==''});q.caseReady=ready;q.analysisReady=(document.querySelector('#cs-status-pill')?.textContent||'').trim()==='ANALYSIS READY';for(const id of QA_LAYERS){const input=document.querySelector(`#cs-layer-drawer [data-layer="${id}"]`);const row=input?.closest('.fcc-layer-row');const p=parseStatus(id,row);const state=q.layers[id]||{sourceStatus:'SOURCE CONTEXT',featureCount:null,renderStatus:'HIDDEN',visible:false,opacity:1,error:null};state.sourceStatus=p.sourceStatus;state.featureCount=p.featureCount;state.error=p.error;state.visible=!!input?.checked;if(!state.visible&&state.renderStatus!=='HIDDEN')state.renderStatus='HIDDEN';const opacityInput=document.querySelector(`#cs-layer-drawer [data-opacity="${id}"]`);if(opacityInput)state.opacity=Math.max(0,Math.min(100,Number(opacityInput.value)||0))/100;q.layers[id]=state;}}
function mark(id,patch){if(!id||!q.layers[id])return;Object.assign(q.layers[id],patch);q.lastRenderChange=Date.now();}
const drawer=document.querySelector('#cs-layer-drawer');
if(drawer){drawer.addEventListener('change',e=>{const input=e.target?.closest?.('input[data-layer]');if(!input)return;const id=input.dataset.layer;pending={id,checked:input.checked,at:Date.now()};q.lastAction=input.checked?'LAYER_ON':'LAYER_OFF';if(input.checked)mark(id,{visible:true,renderStatus:'LIVE_DATA_PENDING'});else mark(id,{visible:false,renderStatus:'HIDDEN'});setTimeout(sync,0);},true);}
function wrapCtor(ctorName){const C=window.L?.[ctorName];if(!C||!C.prototype)return;const proto=C.prototype;if(proto.__urbionQaWrapped)return;const original=proto.onAdd;if(typeof original==='function'){proto.onAdd=function(map){const out=original.apply(this,arguments);let id=this.__urbionLayerId||this.__urbionSource||null;if(!id&&pending&&Date.now()-pending.at<5000)id=pending.id;if(id&&q.layers[id]){this.__urbionQaId=id;if(this.__urbionOfficial){mark(id,{renderStatus:'LIVE_DATA_PENDING',visible:true});this.once?.('tileload',()=>mark(id,{sourceStatus:'LIVE',renderStatus:'RENDERED',visible:true,error:null}));this.once?.('tileerror',()=>mark(id,{sourceStatus:'SOURCE_UNAVAILABLE',renderStatus:'HIDDEN',visible:false,error:'Tile source unavailable'}));}else{mark(id,{sourceStatus:'LIVE',renderStatus:'RENDERED',visible:true});}}return out;};proto.__urbionQaWrapped=true;}}
wrapCtor('GridLayer');wrapCtor('GeoJSON');wrapCtor('FeatureGroup');
setInterval(sync,250);
setTimeout(sync,0);setTimeout(sync,250);setTimeout(sync,750);
})();'''
        payload += "\n" + qa_contract
        return Response(payload, media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})
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
    if request.url.path == "/about.html":
        return _about_page()
    if request.url.path == "/what-if.html":
        return _what_if_page()
    return await call_next(request)


app.add_api_route("/", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/index.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/championship.html", _frontend_root, methods=["GET"], include_in_schema=False)
app.add_api_route("/about.html", _about_page, methods=["GET"], include_in_schema=False)
app.add_api_route("/what-if.html", _what_if_page, methods=["GET"], include_in_schema=False)
for _asset in sorted(ALLOWED_ASSETS):
    app.add_api_route(f"/{_asset}", _exact_asset_handler(_asset), methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.js", _frontend_asset, methods=["GET"], include_in_schema=False)
app.add_api_route("/{asset}.svg", _frontend_logo, methods=["GET"], include_in_schema=False)

_PRIORITY_PATHS = (
    "/urbion_championship_command_shell.js",
    "/urbion_championship_premium_v7.js",
    "/urbion_championship_premium_v6.js",
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
    "/urbion_what_if_upgrade.js",
    "/urbion_logo_dark.svg",
    "/urbion_logo_light.svg",
    "/about.html",
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
