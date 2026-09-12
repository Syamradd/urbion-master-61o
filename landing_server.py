"""URBION HORIZON public presentation entrypoint.

The existing FastAPI application and planning engines remain unchanged. This
adapter owns only the judge-facing presentation routes so legacy championship
frontend layers cannot be injected into the canonical pages.
"""
from pathlib import Path
import json

from fastapi import Request
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse

from championship_server import app
from server import AssessmentRequest, assess_core
from urbion_decision_center import build_decision_center
from urbion_wms_proxy import router as urbion_wms_router

BASE_DIR = Path(__file__).resolve().parent
WELCOME_FILE = BASE_DIR / "welcome.html"
WELCOME_BACKGROUND_FILE = BASE_DIR / "background_welcoming_page.png"
ABOUT_FILE = BASE_DIR / "urbion_horizon_about.html"
WORKSPACE_FILE = BASE_DIR / "workspace_v5.html"
WORKSPACE_BRIDGE = BASE_DIR / "urbion_workspace_bridge.js"
WORKSPACE_RUNTIME = BASE_DIR / "urbion_workspace_runtime.js"
WORKSPACE_LAYER = BASE_DIR / "urbion_layer_runtime_fix.js"
WORKSPACE_CANONICAL_UI = BASE_DIR / "urbion_workspace_canonical_ui.js"
WORKSPACE_MODAL_OWNER = BASE_DIR / "urbion_workspace_modal_owner.js"

app.include_router(urbion_wms_router)


def _html(path: Path) -> HTMLResponse:
    if not path.is_file():
        return HTMLResponse(f"URBION HORIZON presentation asset missing: {path.name}", status_code=500)
    return HTMLResponse(path.read_text(encoding="utf-8"), media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _workspace() -> HTMLResponse:
    required = (WORKSPACE_FILE, WORKSPACE_BRIDGE, WORKSPACE_RUNTIME, WORKSPACE_LAYER, WORKSPACE_CANONICAL_UI, WORKSPACE_MODAL_OWNER)
    for path in required:
        if not path.is_file():
            return HTMLResponse(f"URBION HORIZON workspace asset missing: {path.name}", status_code=500)
    html = WORKSPACE_FILE.read_text(encoding="utf-8")
    scripts = (
        '<script src="/urbion_workspace_bridge.js"></script>'
        '<script src="/urbion_workspace_runtime.js"></script>'
        '<script src="/urbion_layer_runtime_fix.js"></script>'
        '<script src="/urbion_workspace_canonical_ui.js"></script>'
        '<script src="/urbion_workspace_modal_owner.js"></script>'
    )
    if "</body>" in html:
        html = html.replace("</body>", scripts + "</body>", 1)
    atmosphere = '''<style id="urbion-presentation-atmosphere">
html,body{background-color:#020b12!important}
body{position:relative}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.42;background-image:radial-gradient(circle at 7% 14%,rgba(255,255,255,.65) 0 1px,transparent 1.7px),radial-gradient(circle at 18% 24%,rgba(81,224,244,.5) 0 1px,transparent 1.7px),radial-gradient(circle at 34% 10%,rgba(255,255,255,.48) 0 1px,transparent 1.7px),radial-gradient(circle at 53% 17%,rgba(92,232,205,.42) 0 1px,transparent 1.8px),radial-gradient(circle at 71% 8%,rgba(255,255,255,.54) 0 1px,transparent 1.7px),radial-gradient(circle at 89% 18%,rgba(86,220,242,.5) 0 1px,transparent 1.8px),radial-gradient(ellipse at 73% -10%,rgba(42,231,236,.12),transparent 40%)}
.top,.layout{position:relative;z-index:1}
</style>'''
    if "urbion-presentation-atmosphere" not in html and "</head>" in html:
        html = html.replace("</head>", atmosphere + "</head>", 1)
    return HTMLResponse(html, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0", "X-URBION-UI": "CANONICAL-V5-ISOLATED"})


@app.middleware("http")
async def _urbion_canonical_presentation(request: Request, call_next):
    path = request.url.path
    if path == "/decision-center" and request.method == "POST":
        try:
            raw = await request.body()
            payload = json.loads(raw.decode("utf-8")) if raw else None
            assessment = payload.get("assessment") if isinstance(payload, dict) else None
            if isinstance(assessment, dict):
                validated = AssessmentRequest.model_validate(assessment)
                return JSONResponse(build_decision_center(assessment=assess_core(validated)))
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
        except Exception:
            pass
    if path in {"/", "/index.html"}:
        return _html(WELCOME_FILE)
    if path == "/background_welcoming_page.png":
        if not WELCOME_BACKGROUND_FILE.is_file(): return Response("URBION HORIZON welcome background missing", status_code=404, media_type="text/plain")
        return FileResponse(WELCOME_BACKGROUND_FILE, media_type="image/png", headers={"Cache-Control":"no-store, max-age=0, must-revalidate","X-URBION-WELCOME-BACKGROUND":"CANONICAL-WELCOME"})
    if path == "/about": return _html(ABOUT_FILE)
    if path == "/workspace": return _workspace()
    assets={
        "/urbion_workspace_bridge.js": (WORKSPACE_BRIDGE,"URBION HORIZON workspace bridge missing."),
        "/urbion_workspace_runtime.js": (WORKSPACE_RUNTIME,"URBION HORIZON runtime layer missing."),
        "/urbion_layer_runtime_fix.js": (WORKSPACE_LAYER,"URBION HORIZON live layer renderer missing."),
        "/urbion_workspace_canonical_ui.js": (WORKSPACE_CANONICAL_UI,"URBION HORIZON canonical UI owner missing."),
        "/urbion_workspace_modal_owner.js": (WORKSPACE_MODAL_OWNER,"URBION HORIZON modal owner missing."),
    }
    if path in assets:
        target,message=assets[path]
        if not target.is_file(): return Response(message,status_code=500,media_type="text/plain; charset=utf-8")
        return Response(target.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
    if path == "/urbion_workspace_final.js":
        target=BASE_DIR/"urbion_workspace_final.js"
        if not target.is_file(): return Response("URBION HORIZON legacy compatibility asset missing.",status_code=404,media_type="text/plain")
        return Response(target.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
    return await call_next(request)
