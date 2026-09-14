"""Isolated Render entrypoint for the canonical URBION HORIZON Workspace V3 preview."""
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

@app.get("/", include_in_schema=False)
def workspace_root() -> HTMLResponse:
    target = BASE_DIR / "workspace_v3.html"
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Workspace V3 frontend is missing")
    return HTMLResponse(target.read_text(encoding="utf-8"), media_type="text/html; charset=utf-8", headers={"Cache-Control":"no-store, max-age=0"})

@app.get("/workspace-v3.html", include_in_schema=False)
def workspace_html() -> HTMLResponse:
    return workspace_root()
