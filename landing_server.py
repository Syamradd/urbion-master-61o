"""URBION HORIZON public presentation entrypoint."""
from pathlib import Path
import json

from fastapi import Request
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse
from championship_server import app
from server import AssessmentRequest, assess_core
from urbion_decision_center import build_decision_center
from urbion_wms_proxy import router as urbion_wms_router
from urbion_environment_api import router as urbion_environment_router
from urbion_mobility_api import router as urbion_mobility_router
from urbion_canonical_evidence import build_canonical_evidence_packet
from urbion_development_impact import build_development_impact

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
WORKSPACE_PBT_CATALOG = BASE_DIR / "urbion_workspace_pbt_catalog.js"
WORKSPACE_UTILITY_OWNER = BASE_DIR / "urbion_workspace_utility_owner.js"
WORKSPACE_REVIEW_GAPS = BASE_DIR / "urbion_workspace_review_gaps_owner.js"
WORKSPACE_ENVIRONMENT = BASE_DIR / "urbion_workspace_environment_owner.js"
WORKSPACE_MOBILITY = BASE_DIR / "urbion_workspace_mobility_owner.js"
WORKSPACE_DEVELOPMENT_IMPACT = BASE_DIR / "urbion_workspace_development_impact_owner.js"

app.include_router(urbion_wms_router)
app.include_router(urbion_environment_router)
app.include_router(urbion_mobility_router)


def _html(path: Path) -> HTMLResponse:
    if not path.is_file():
        return HTMLResponse(f"URBION HORIZON presentation asset missing: {path.name}", status_code=500)
    return HTMLResponse(path.read_text(encoding="utf-8"), media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store, max-age=0"})


def _workspace() -> HTMLResponse:
    required = (WORKSPACE_FILE, WORKSPACE_BRIDGE, WORKSPACE_RUNTIME, WORKSPACE_LAYER,
                WORKSPACE_CANONICAL_UI, WORKSPACE_MODAL_OWNER, WORKSPACE_PBT_CATALOG,
                WORKSPACE_UTILITY_OWNER, WORKSPACE_REVIEW_GAPS, WORKSPACE_ENVIRONMENT,
                WORKSPACE_MOBILITY, WORKSPACE_DEVELOPMENT_IMPACT)
    for path in required:
        if not path.is_file():
            return HTMLResponse(f"URBION HORIZON workspace asset missing: {path.name}", status_code=500)
    html = WORKSPACE_FILE.read_text(encoding="utf-8")
    scripts = ('<script src="/urbion_workspace_bridge.js"></script>'
               '<script src="/urbion_workspace_runtime.js"></script>'
               '<script src="/urbion_layer_runtime_fix.js"></script>'
               '<script src="/urbion_workspace_canonical_ui.js"></script>'
               '<script src="/urbion_workspace_modal_owner.js"></script>'
               '<script src="/urbion_workspace_pbt_catalog.js"></script>'
               '<script src="/urbion_workspace_utility_owner.js"></script>'
               '<script src="/urbion_workspace_review_gaps_owner.js"></script>'
               '<script src="/urbion_workspace_environment_owner.js"></script>'
               '<script src="/urbion_workspace_mobility_owner.js"></script>'
               '<script src="/urbion_workspace_development_impact_owner.js"></script>')
    if "</body>" in html:
        html = html.replace("</body>", scripts + "</body>", 1)
    return HTMLResponse(html, media_type="text/html", headers={"Cache-Control":"no-store, max-age=0", "X-URBION-UI":"CANONICAL-V5-ISOLATED"})


def _development_impact(assessment: dict) -> dict:
    """Build impact screening strictly from explicit assessment proposal inputs."""
    proposal = assessment.get("proposal") or {}
    spatial = assessment.get("site_analysis") or {}
    return build_development_impact(
        development_type=assessment.get("development_type") or proposal.get("development_type") or "",
        units=proposal.get("units"),
        site_area_ha=proposal.get("site_area_ha"),
        commercial_gfa_m2=proposal.get("commercial_gfa_m2"),
        jobs=proposal.get("jobs"),
        population=proposal.get("population"),
        daily_trips=proposal.get("daily_trips"),
        road_distance_m=proposal.get("road_distance_m", spatial.get("road_distance_m")),
        flood_exposure=proposal.get("flood_exposure", spatial.get("flood_exposure")),
        nearby_facilities=proposal.get("nearby_facilities"),
        source_context={
            "assessment_inputs": {k: proposal.get(k) for k in (
                "units", "site_area_ha", "commercial_gfa_m2", "jobs",
                "population", "daily_trips", "road_distance_m",
                "flood_exposure", "nearby_facilities") if proposal.get(k) is not None},
            "plot_ratio": proposal.get("Plot Ratio"),
            "evidence_policy": "Explicit proposal/spatial inputs only; missing values remain review-required."
        },
    )


def _canonical_packet(assessment: dict) -> dict:
    impact = assessment.get("development_impact")
    if not isinstance(impact, dict):
        impact = _development_impact(assessment)
        assessment["development_impact"] = impact
    return build_canonical_evidence_packet(assessment=assessment,
                                           spatial=assessment.get("site_analysis"),
                                           environment=assessment.get("live_environment_evidence") or assessment.get("evidence_intelligence"),
                                           stations=assessment.get("live_station_evidence") or assessment.get("stations"),
                                           development_impact=impact,
                                           policy_graph={"policy_coverage": assessment.get("policy_coverage")})


def _attach_packet(payload: dict, path: str) -> dict:
    assessment = payload if path == "/assess" else payload.get("assessment")
    if isinstance(assessment, dict):
        packet = _canonical_packet(assessment)
        payload["development_impact"] = packet.get("evidence", {}).get("development_impact", {})
        payload["canonical_evidence_packet"] = packet
        decision = payload.get("decision_center")
        if isinstance(decision, dict):
            decision["development_impact"] = packet.get("evidence", {}).get("development_impact", {})
            decision["canonical_evidence_packet"] = packet
            decision["review_gaps"] = list(packet.get("review_gaps", []))
            decision["review_required"] = bool(decision["review_gaps"])
    return payload


async def _response_json(response: Response) -> tuple[bytes, object]:
    try:
        body = b"".join([chunk async for chunk in response.body_iterator])
        return body, json.loads(body.decode("utf-8")) if body else None
    except Exception:
        return b"", None


@app.middleware("http")
async def _urbion_canonical_presentation(request: Request, call_next):
    path = request.url.path
    if path == "/decision-center" and request.method == "POST":
        try:
            raw = await request.body()
            incoming = json.loads(raw.decode("utf-8")) if raw else None
            source = incoming.get("assessment") if isinstance(incoming, dict) else None
            if isinstance(source, dict):
                assessed = assess_core(AssessmentRequest.model_validate(source))
                packet = _canonical_packet(assessed)
                result = build_decision_center(assessment=assessed)
                if isinstance(result, dict):
                    result["development_impact"] = packet.get("evidence", {}).get("development_impact", {})
                    result["canonical_evidence_packet"] = packet
                    result["review_gaps"] = list(packet.get("review_gaps", []))
                    result["review_required"] = bool(result["review_gaps"])
                return JSONResponse(result)
        except Exception:
            pass

    if path in {"/", "/index.html"}: return _html(WELCOME_FILE)
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
        "/urbion_workspace_pbt_catalog.js": (WORKSPACE_PBT_CATALOG,"URBION HORIZON PBT catalogue missing."),
        "/urbion_workspace_utility_owner.js": (WORKSPACE_UTILITY_OWNER,"URBION HORIZON utility owner missing."),
        "/urbion_workspace_review_gaps_owner.js": (WORKSPACE_REVIEW_GAPS,"URBION HORIZON review-gap presentation owner missing."),
        "/urbion_workspace_environment_owner.js": (WORKSPACE_ENVIRONMENT,"URBION HORIZON environment evidence owner missing."),
        "/urbion_workspace_mobility_owner.js": (WORKSPACE_MOBILITY,"URBION HORIZON mobility evidence owner missing."),
        "/urbion_workspace_development_impact_owner.js": (WORKSPACE_DEVELOPMENT_IMPACT,"URBION HORIZON development impact owner missing."),
    }
    if path in assets:
        target,message=assets[path]
        if not target.is_file(): return Response(message,status_code=500,media_type="text/plain; charset=utf-8")
        return Response(target.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})
    if path == "/urbion_workspace_final.js":
        target=BASE_DIR/"urbion_workspace_final.js"
        if not target.is_file(): return Response("URBION HORIZON legacy compatibility asset missing.",status_code=404,media_type="text/plain")
        return Response(target.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0"})

    response = await call_next(request)
    if path in {"/assess", "/workstation/analysis"} and request.method == "POST":
        body, payload = await _response_json(response)
        if not isinstance(payload, dict) or response.status_code >= 400:
            return Response(content=body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
        payload = _attach_packet(payload, path)
        headers = dict(response.headers)
        headers.pop("content-length", None)
        headers.pop("content-type", None)
        return JSONResponse(payload, status_code=response.status_code, headers=headers)
    return response
