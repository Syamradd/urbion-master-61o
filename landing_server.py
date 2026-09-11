"""URBION HORIZON public presentation entrypoint.

The existing FastAPI application and planning engines remain unchanged. This
adapter owns only the judge-facing presentation routes so legacy championship
frontend layers cannot be injected into the canonical pages.
"""
from pathlib import Path
import json

from fastapi import Request
from fastapi.responses import HTMLResponse, Response, JSONResponse

from championship_server import app
from server import AssessmentRequest, assess_core
from urbion_decision_center import build_decision_center

BASE_DIR = Path(__file__).resolve().parent
WELCOME_FILE = BASE_DIR / "welcome.html"
ABOUT_FILE = BASE_DIR / "urbion_horizon_about.html"
WORKSPACE_FILE = BASE_DIR / "workspace_v5.html"
WORKSPACE_JS = BASE_DIR / "urbion_workspace_final.js"
WORKSPACE_BRIDGE = BASE_DIR / "urbion_workspace_bridge.js"
WORKSPACE_RUNTIME = BASE_DIR / "urbion_workspace_runtime.js"


def _html(path: Path) -> HTMLResponse:
    if not path.is_file():
        return HTMLResponse(
            f"URBION HORIZON presentation asset missing: {path.name}",
            status_code=500,
        )
    return HTMLResponse(
        path.read_text(encoding="utf-8"),
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


def _workspace() -> HTMLResponse:
    for path in (WORKSPACE_FILE, WORKSPACE_JS, WORKSPACE_BRIDGE, WORKSPACE_RUNTIME):
        if not path.is_file():
            return HTMLResponse(
                f"URBION HORIZON workspace asset missing: {path.name}",
                status_code=500,
            )
    html = WORKSPACE_FILE.read_text(encoding="utf-8")
    scripts = (
        '<script src="/urbion_workspace_final.js"></script>'
        '<script src="/urbion_workspace_bridge.js"></script>'
        '<script src="/urbion_workspace_runtime.js"></script>'
    )
    if "</body>" in html and "/urbion_workspace_final.js" not in html:
        html = html.replace("</body>", scripts + "</body>", 1)
    elif "/urbion_workspace_runtime.js" not in html:
        html = html.replace(
            "</body>",
            '<script src="/urbion_workspace_runtime.js"></script></body>',
            1,
        )
    atmosphere = '''<style id="urbion-presentation-atmosphere">
html,body{background-color:#020b12!important}
body{position:relative}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.42;background-image:radial-gradient(circle at 7% 14%,rgba(255,255,255,.65) 0 1px,transparent 1.7px),radial-gradient(circle at 18% 24%,rgba(81,224,244,.5) 0 1px,transparent 1.7px),radial-gradient(circle at 34% 10%,rgba(255,255,255,.48) 0 1px,transparent 1.7px),radial-gradient(circle at 53% 17%,rgba(92,232,205,.42) 0 1px,transparent 1.8px),radial-gradient(circle at 71% 8%,rgba(255,255,255,.54) 0 1px,transparent 1.7px),radial-gradient(circle at 89% 18%,rgba(86,220,242,.5) 0 1px,transparent 1.8px),radial-gradient(ellipse at 73% -10%,rgba(42,231,236,.12),transparent 40%)}
.top,.layout{position:relative;z-index:1}
</style>'''
    if "urbion-presentation-atmosphere" not in html and "</head>" in html:
        html = html.replace("</head>", atmosphere + "</head>", 1)
    return HTMLResponse(
        html,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@app.middleware("http")
async def _urbion_canonical_presentation(request: Request, call_next):
    path = request.url.path

    # Hard compatibility boundary for the canonical workspace decision action.
    # The workspace sends {"assessment": {...}, "analysis": {...}}, while the
    # production engine route accepts AssessmentRequest directly. Handle this
    # exact presentation shape before FastAPI route validation and reuse the same
    # deterministic decision engine. No alternate approval logic is introduced.
    if path == "/decision-center" and request.method == "POST":
        try:
            raw = await request.body()
            payload = json.loads(raw.decode("utf-8")) if raw else None
            assessment = payload.get("assessment") if isinstance(payload, dict) else None
            if isinstance(assessment, dict):
                validated = AssessmentRequest.model_validate(assessment)
                result = build_decision_center(assessment=assess_core(validated))
                return JSONResponse(result)
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
        except Exception:
            pass

    if path in {"/", "/index.html"}:
        return _html(WELCOME_FILE)
    if path == "/about":
        return _html(ABOUT_FILE)
    if path == "/workspace":
        return _workspace()
    if path == "/urbion_workspace_final.js":
        if not WORKSPACE_JS.is_file():
            return Response(
                "URBION HORIZON function layer missing.",
                status_code=500,
                media_type="text/plain; charset=utf-8",
            )
        return Response(
            WORKSPACE_JS.read_text(encoding="utf-8"),
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    if path == "/urbion_workspace_bridge.js":
        if not WORKSPACE_BRIDGE.is_file():
            return Response(
                "URBION HORIZON workspace bridge missing.",
                status_code=500,
                media_type="text/plain; charset=utf-8",
            )
        return Response(
            WORKSPACE_BRIDGE.read_text(encoding="utf-8"),
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    if path == "/urbion_workspace_runtime.js":
        if not WORKSPACE_RUNTIME.is_file():
            return Response(
                "URBION HORIZON runtime layer missing.",
                status_code=500,
                media_type="application/javascript; charset=utf-8",
            )
        return Response(
            WORKSPACE_RUNTIME.read_text(encoding="utf-8"),
            media_type="application/javascript; charset=utf-8",
            headers={"Cache-Control": "no-store, max-age=0"},
        )
    return await call_next(request)
