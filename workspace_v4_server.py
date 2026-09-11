from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

app: FastAPI = backend_app
BASE_DIR = Path(__file__).resolve().parent


def root() -> HTMLResponse:
    target = BASE_DIR / 'workspace_v5.html'
    if not target.is_file():
        raise HTTPException(status_code=404, detail='Workspace V5 frontend is missing')
    return HTMLResponse(
        target.read_text(encoding='utf-8'),
        media_type='text/html; charset=utf-8',
        headers={'Cache-Control': 'no-store, max-age=0', 'X-URBION-UI': 'CANONICAL-V5'},
    )


def workspace() -> HTMLResponse:
    return root()

# server.app already contains a legacy '/' route. Add canonical routes and
# move them to the front so Starlette resolves V5 before the legacy handlers.
app.add_api_route('/', root, methods=['GET'], include_in_schema=False)
app.add_api_route('/workspace-v5.html', workspace, methods=['GET'], include_in_schema=False)
workspace_route = app.router.routes.pop()
root_route = app.router.routes.pop()
app.router.routes.insert(0, root_route)
app.router.routes.insert(1, workspace_route)
