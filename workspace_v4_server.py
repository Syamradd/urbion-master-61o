from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from server import app as backend_app
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
app = FastAPI(title='URBION HORIZON Workspace V5', version='CANONICAL-V5')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])

_FRONTEND_SUFFIXES = ('.html', '.js', '.css', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.ico')
_SKIP_PATHS = {'/', '/index.html'}
for route in backend_app.router.routes:
    path = getattr(route, 'path', '')
    if path in _SKIP_PATHS or path.startswith('/assets/') or path.endswith(_FRONTEND_SUFFIXES):
        continue
    app.router.routes.append(route)

WELCOME_FILE = BASE_DIR / 'welcome.html'
WELCOME_BACKGROUND_FILE = BASE_DIR / 'background_welcoming_page.png'
ABOUT_FILE = BASE_DIR / 'urbion_horizon_about.html'
ABOUT_MASTER_FILE = BASE_DIR / 'about_master.png'
WORKSPACE_FILE = BASE_DIR / 'workspace_v5.html'
WORKSPACE_JS = BASE_DIR / 'urbion_workspace_final.js'
WORKSPACE_BRIDGE = BASE_DIR / 'urbion_workspace_bridge.js'
WORKSPACE_RUNTIME = BASE_DIR / 'urbion_workspace_runtime.js'
LAYER_RUNTIME = BASE_DIR / 'urbion_layer_runtime_fix.js'
CANONICAL_UI = BASE_DIR / 'urbion_workspace_canonical_ui.js'
ABOUT_CITY_IMAGE = BASE_DIR / 'about_city_reference.jpg'

def _read(path: Path) -> str:
    if not path.is_file():
        raise HTTPException(status_code=500, detail=f'Presentation asset missing: {path.name}')
    return path.read_text(encoding='utf-8')

def _workspace() -> str:
    html = _read(WORKSPACE_FILE)
    scripts = (
        '<script src="/urbion_workspace_bridge.js"></script>'
        '<script src="/urbion_workspace_runtime.js"></script>'
        '<script src="/urbion_layer_runtime_fix.js"></script>'
        '<script src="/urbion_workspace_canonical_ui.js"></script>'
    )
    if '</body>' in html:
        html = html.replace('</body>', scripts + '</body>', 1)
    atmosphere = '<style id="urbion-presentation-atmosphere">html,body{background-color:#020b12!important}body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.42;background-image:radial-gradient(circle at 7% 14%,rgba(255,255,255,.65) 0 1px,transparent 1.7px),radial-gradient(circle at 18% 24%,rgba(81,224,244,.5) 0 1px,transparent 1.7px),radial-gradient(circle at 53% 17%,rgba(92,232,205,.42) 0 1px,transparent 1.8px),radial-gradient(ellipse at 73% -10%,rgba(42,231,236,.12),transparent 40%)}.top,.layout{position:relative;z-index:1}</style>'
    if 'urbion-presentation-atmosphere' not in html and '</head>' in html:
        html = html.replace('</head>', atmosphere + '</head>', 1)
    return html

def _about() -> HTMLResponse:
    return HTMLResponse(
        _read(ABOUT_FILE),
        media_type='text/html; charset=utf-8',
        headers={
            'Cache-Control': 'no-store, max-age=0, must-revalidate',
            'X-URBION-UI': 'CANONICAL-ABOUT',
            'X-URBION-ABOUT': 'ABOUT-CANONICAL-V3-PNG',
            'X-URBION-ABOUT-SOURCE': 'urbion_horizon_about.html',
            'X-URBION-ABOUT-MASTER-FORMAT': 'PNG',
        },
    )

@app.get('/', include_in_schema=False)
@app.get('/index.html', include_in_schema=False)
def root() -> HTMLResponse:
    return HTMLResponse(_read(WELCOME_FILE), media_type='text/html; charset=utf-8', headers={'Cache-Control':'no-store, max-age=0', 'X-URBION-UI':'CANONICAL-WELCOME'})

@app.get('/background_welcoming_page.png', include_in_schema=False)
def welcome_background():
    if not WELCOME_BACKGROUND_FILE.is_file():
        raise HTTPException(status_code=404, detail='Welcome background is missing')
    return FileResponse(WELCOME_BACKGROUND_FILE, media_type='image/png', headers={'Cache-Control':'no-store, max-age=0, must-revalidate','X-URBION-WELCOME-BACKGROUND':'CANONICAL-WELCOME'})

@app.get('/about', include_in_schema=False)
def about() -> HTMLResponse:
    return _about()

@app.get('/workspace', include_in_schema=False)
@app.get('/workspace-v5.html', include_in_schema=False)
def workspace() -> HTMLResponse:
    return HTMLResponse(_workspace(), media_type='text/html; charset=utf-8', headers={'Cache-Control':'no-store, max-age=0', 'X-URBION-UI':'CANONICAL-V5-ISOLATED'})

def _js(path: Path, message: str) -> Response:
    if not path.is_file():
        return Response(message, status_code=500, media_type='text/plain; charset=utf-8')
    return Response(path.read_text(encoding='utf-8'), media_type='application/javascript; charset=utf-8', headers={'Cache-Control':'no-store, max-age=0'})

@app.get('/urbion_workspace_final.js', include_in_schema=False)
def workspace_final_js(): return _js(WORKSPACE_JS, 'URBION HORIZON function layer missing.')
@app.get('/urbion_workspace_bridge.js', include_in_schema=False)
def workspace_bridge_js(): return _js(WORKSPACE_BRIDGE, 'URBION HORIZON workspace bridge missing.')
@app.get('/urbion_workspace_runtime.js', include_in_schema=False)
def workspace_runtime_js(): return _js(WORKSPACE_RUNTIME, 'URBION HORIZON workspace runtime missing.')
@app.get('/urbion_layer_runtime_fix.js', include_in_schema=False)
def layer_runtime_fix_js(): return _js(LAYER_RUNTIME, 'URBION HORIZON live layer renderer missing.')
@app.get('/urbion_workspace_canonical_ui.js', include_in_schema=False)
def canonical_ui_js(): return _js(CANONICAL_UI, 'URBION HORIZON canonical UI owner missing.')

@app.get('/about_master.png', include_in_schema=False)
def about_master_png():
    if not ABOUT_MASTER_FILE.is_file():
        raise HTTPException(status_code=404, detail='About master PNG is missing')
    return FileResponse(ABOUT_MASTER_FILE, media_type='image/png', headers={'Cache-Control':'no-store, max-age=0, must-revalidate','X-URBION-ABOUT-MASTER':'CANONICAL-PNG'})

@app.get('/about_master.webp', include_in_schema=False)
def about_master_legacy():
    target = BASE_DIR / 'about_master.webp'
    if not target.is_file():
        raise HTTPException(status_code=404, detail='Legacy About master is missing')
    return FileResponse(target, media_type='image/webp', headers={'Cache-Control':'no-store, max-age=0'})

@app.get('/about_city_reference.jpg', include_in_schema=False)
def about_city_reference():
    if not ABOUT_CITY_IMAGE.is_file(): raise HTTPException(status_code=404, detail='About city image is missing')
    return FileResponse(ABOUT_CITY_IMAGE, media_type='image/jpeg', headers={'Cache-Control':'no-store, max-age=0'})

@app.get('/urbion_logo_dark.svg', include_in_schema=False)
def logo_dark():
    target = BASE_DIR / 'urbion_logo_dark.svg'
    if not target.is_file(): raise HTTPException(status_code=404, detail='Dark logo is missing')
    return FileResponse(target, media_type='image/svg+xml')

@app.get('/urbion_logo_light.svg', include_in_schema=False)
def logo_light():
    target = BASE_DIR / 'urbion_logo_light.svg'
    if not target.is_file(): raise HTTPException(status_code=404, detail='Light logo is missing')
    return FileResponse(target, media_type='image/svg+xml')

@app.get('/team_photo.svg', include_in_schema=False)
def team_photo():
    target = BASE_DIR / 'team_photo.svg'
    if not target.is_file(): raise HTTPException(status_code=404, detail='Team photo is missing')
    return FileResponse(target, media_type='image/svg+xml')

@app.get('/__urbion_runtime_identity', include_in_schema=False)
def runtime_identity():
    return {'ui':'CANONICAL-PRESENTATION','root':'WELCOME','about':'ABOUT-CANONICAL-V3-PNG','workspace':'CANONICAL-V5-ISOLATED','legacy_frontend_routes':'EXCLUDED','backend':'REUSED','source':'workspace_v4_server.py','layer_runtime':'AUTHORITATIVE-V1','about_mode':'SINGLE-SOURCE','about_master':'CANONICAL-PNG','workspace_ui_owner':'urbion_workspace_canonical_ui.js'}
