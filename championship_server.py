"""Deterministic production entrypoint for the URBION HORIZON championship UI."""
from pathlib import Path
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from server import app
import urbion_spatial_api
import urbion_workstation_api
import urbion_decision_intelligence_api
import urbion_agent_api
import urbion_knowledge_api
BASE_DIR = Path(__file__).resolve().parent
ALLOWED_ASSETS = {"urbion_ui.js","urbion_championship_ui.js","urbion_championship_upgrade.js","urbion_championship_dashboard.js","urbion_championship_polish.js","urbion_championship_v279.js","urbion_public_source_ui.js","urbion_public_spatial_v283.js","urbion_public_spatial_v284.js","urbion_championship_spatial_studio.js","urbion_championship_decision_layer.js","urbion_championship_intelligence_upgrade.js","urbion_championship_input_sync.js","urbion_championship_workflow.js","urbion_championship_decision_chain.js","urbion_what_if_upgrade.js","urbion_spatial_workstation_upgrade.js","urbion_spatial_implication_bridge.js","urbion_championship_workstation_v2.js","urbion_decision_intelligence_ui.js"}
def _remove_routes(*paths: str)->None:
    targets=set(paths); app.router.routes[:]=[r for r in app.router.routes if getattr(r,"path",None) not in targets]
_remove_routes("/","/index.html","/championship.html")

def _design_system(source: str) -> str:
    css='''<style id="urbion-premium-system">:root{--urbion-accent:#35e2b0;--urbion-cyan:#18cce5;--urbion-navy:#07131f;--urbion-ink:#eaf5f7;--urbion-muted:#8ea7b5}body{font-family:Inter,system-ui,sans-serif;background:radial-gradient(circle at 78% 12%,rgba(24,204,229,.10),transparent 28%),radial-gradient(circle at 16% 85%,rgba(53,226,176,.07),transparent 30%),#07131f}body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.22;background-image:linear-gradient(rgba(53,226,176,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(53,226,176,.045) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,black,transparent 88%);z-index:0}#urbion-theme-toggle{position:fixed;right:18px;bottom:18px;z-index:9999;border:1px solid rgba(53,226,176,.35);border-radius:999px;padding:10px 13px;background:rgba(7,19,31,.88);backdrop-filter:blur(14px);color:#eaf5f7;font:800 10px Inter;letter-spacing:.04em;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.28)}body.urbion-light{background:radial-gradient(circle at 78% 12%,rgba(24,204,229,.10),transparent 28%),#f4f8fa;color:#102330}body.urbion-light:before{opacity:.16;background-image:linear-gradient(rgba(11,74,91,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(11,74,91,.07) 1px,transparent 1px)}body.urbion-light #urbion-theme-toggle{background:rgba(255,255,255,.92);color:#102330;border-color:rgba(8,99,112,.24)}body.urbion-light #spatial-studio,body.urbion-light #intel-upgrade{background:linear-gradient(135deg,#ffffff,#eef6f8);color:#102330;border-color:#d5e2e7}body.urbion-light #spatial-studio .ss-panel,body.urbion-light #intel-upgrade .iu-card{background:rgba(255,255,255,.78);color:#102330}body.urbion-light #spatial-studio .ss-metrics div,body.urbion-light #intel-upgrade .iu-row{background:#f6fafb;color:#18303d;border-color:#d9e6ea}body.urbion-light #intel-upgrade .iu-reason,body.urbion-light #spatial-studio .ss-note{color:#4e6672}@media(max-width:600px){#urbion-theme-toggle{right:12px;bottom:12px;padding:9px 11px}}</style>'''
    if 'id="urbion-premium-system"' not in source: source=source.replace('</head>',css+'</head>',1)
    toggle='''<button id="urbion-theme-toggle" type="button" aria-label="Toggle URBION theme">◐ THEME · DARK</button><script>(function(){function apply(){var light=document.body.classList.contains('urbion-light'),b=document.getElementById('urbion-theme-toggle');if(b)b.textContent=light?'◐ THEME · LIGHT':'◐ THEME · DARK';localStorage.setItem('urbion-theme',light?'light':'dark')}function boot(){var saved=localStorage.getItem('urbion-theme');if(saved==='light')document.body.classList.add('urbion-light');var b=document.getElementById('urbion-theme-toggle');if(b)b.onclick=function(){document.body.classList.toggle('urbion-light');apply()};apply()}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot()})();</script>'''
    if 'id="urbion-theme-toggle"' not in source: source=source.replace('</body>',toggle+'</body>',1)
    return source

def _frontend_root():
    target=BASE_DIR/"championship.html"
    if not target.is_file(): raise HTTPException(status_code=500,detail="Championship frontend is missing")
    source=target.read_text(encoding="utf-8")
    source=source.replace('<div class="health"><i></i> ENGINE ONLINE</div>','<div class="health"><i></i> PHASE-E.8 ENGINE ONLINE</div>')
    if 'id="urbion-championship"' not in source:
        marker='<body>'; source=source.replace(marker,marker+'<div id="urbion-championship" aria-hidden="true" style="display:none"></div>',1) if marker in source else '<div id="urbion-championship" aria-hidden="true" style="display:none"></div>'+source
    for asset in ("urbion_championship_input_sync.js","urbion_championship_spatial_studio.js","urbion_championship_intelligence_upgrade.js","urbion_championship_decision_layer.js","urbion_championship_workflow.js","urbion_championship_decision_chain.js","urbion_spatial_workstation_upgrade.js","urbion_spatial_implication_bridge.js","urbion_championship_workstation_v2.js","urbion_decision_intelligence_ui.js"):
        script=f'<script src="/{asset}"></script>'
        if script not in source: source=source.replace('</body>',script+'</body>',1)
    source=_design_system(source)
    return HTMLResponse(source,media_type="text/html; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
def _what_if_page():
    target=BASE_DIR/"what-if.html"
    if not target.is_file(): raise HTTPException(status_code=404,detail="What-If frontend is missing")
    source=target.read_text(encoding="utf-8")
    script='<script src="/urbion_what_if_upgrade.js"></script>'
    if script not in source: source=source.replace('</body>',script+'</body>',1)
    return HTMLResponse(source,media_type="text/html; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
def _frontend_asset(asset:str):
    if asset not in ALLOWED_ASSETS: raise HTTPException(status_code=404,detail="Unknown frontend asset")
    target=BASE_DIR/asset
    if not target.is_file(): raise HTTPException(status_code=404,detail="Frontend asset not found")
    return FileResponse(target,media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
@app.middleware("http")
async def _championship_frontend_override(request:Request,call_next):
    if request.url.path in {"/","/index.html","/championship.html"}: return _frontend_root()
    if request.url.path in {"/what-if.html"}: return _what_if_page()
    return await call_next(request)
app.add_api_route("/",_frontend_root,methods=["GET"],include_in_schema=False)
app.add_api_route("/index.html",_frontend_root,methods=["GET"],include_in_schema=False)
app.add_api_route("/championship.html",_frontend_root,methods=["GET"],include_in_schema=False)
# Keep the newest workstation asset explicit: server.py contains legacy wildcard routes,
# so an exact production route prevents route-order regressions from turning the asset into 404.
app.add_api_route("/urbion_championship_workstation_v2.js",lambda: _frontend_asset("urbion_championship_workstation_v2.js"),methods=["GET"],include_in_schema=False)
app.add_api_route("/{asset}.js",_frontend_asset,methods=["GET"],include_in_schema=False)
for _path in ("/{asset}.js","/urbion_championship_workstation_v2.js","/championship.html","/index.html","/"):
    for _idx,_route in enumerate(app.router.routes):
        if getattr(_route,"path",None)==_path: app.router.routes.insert(0,app.router.routes.pop(_idx)); break
app.state.frontend_entrypoint="championship.html"
app.state.frontend_release="MASTER-330"
