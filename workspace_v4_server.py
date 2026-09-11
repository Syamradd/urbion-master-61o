from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
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

@app.get('/', include_in_schema=False)
def root() -> HTMLResponse:
    target = BASE_DIR / 'workspace_v5.html'
    if not target.is_file():
        raise HTTPException(status_code=404, detail='Workspace V5 frontend is missing')
    return HTMLResponse(
        target.read_text(encoding='utf-8'),
        media_type='text/html; charset=utf-8',
        headers={'Cache-Control':'no-store, max-age=0', 'X-URBION-UI':'CANONICAL-V5-ISOLATED'},
    )

@app.get('/workspace-v5.html', include_in_schema=False)
def workspace() -> HTMLResponse:
    return root()

@app.get('/urbion_logo_dark.svg', include_in_schema=False)
def logo_dark():
    target = BASE_DIR / 'urbion_logo_dark.svg'
    if not target.is_file():
        raise HTTPException(status_code=404, detail='Dark logo is missing')
    return FileResponse(target, media_type='image/svg+xml')

@app.get('/urbion_logo_light.svg', include_in_schema=False)
def logo_light():
    target = BASE_DIR / 'urbion_logo_light.svg'
    if not target.is_file():
        raise HTTPException(status_code=404, detail='Light logo is missing')
    return FileResponse(target, media_type='image/svg+xml')

@app.get('/__urbion_runtime_identity', include_in_schema=False)
def runtime_identity():
    return {'ui':'CANONICAL-V5-ISOLATED','legacy_frontend_routes':'EXCLUDED','backend':'REUSED','source':'workspace_v4_server.py'}
