"""Deployment gateway that adds optional advisory integrations without changing core rules."""
from fastapi import Body, HTTPException
from server import AssessmentRequest, app, assess_core
from urbion_gemini_redteam import gemini_configured, review_with_gemini
from urbion_live_stations import build_live_station_snapshot
from urbion_station_intelligence import build_station_intelligence
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_release_packet import build_release_packet


@app.get("/gemini/status")
def gemini_status():
    return {"provider":"Google Gemini","role":"RED_TEAM_ADVISORY","configured":gemini_configured(),"decision_authority":"NONE"}


@app.post("/gemini/red-team")
def gemini_red_team(packet: dict = Body(...)):
    return review_with_gemini(packet)


@app.post("/gemini/red-team-assessment")
def gemini_red_team_assessment(r: AssessmentRequest):
    assessment = assess_core(r)
    return review_with_gemini({"assessment":assessment,"guardrails":{"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED","purpose":"independent red-team review only"}})


@app.get("/stations/nearby")
def stations_nearby(site_lat: float, site_lon: float, state: str = "Melaka", limit: int = 5):
    """Find nearby JPS rainfall and configured DOE air-quality stations."""
    if not (-90 <= site_lat <= 90 and -180 <= site_lon <= 180) or (site_lat, site_lon) == (-90.0, -180.0):
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"Site coordinates are invalid or placeholder coordinates."})
    return build_live_station_snapshot(site_lat, site_lon, state, limit)


@app.get("/station-intelligence")
def station_intelligence(site_lat: float, site_lon: float, state: str = "Melaka"):
    """Unified station evidence contract with live observation context when available."""
    if not (-90 <= site_lat <= 90 and -180 <= site_lon <= 180) or (site_lat, site_lon) == (-90.0, -180.0):
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"Site coordinates are invalid or placeholder coordinates."})
    live = build_live_station_snapshot(site_lat, site_lon, state, 5)
    core = build_station_intelligence(site_lat, site_lon, state)
    core["live_snapshot"] = live
    core["decision_boundary"] = "OBSERVATION_CONTEXT"
    core["statutory_verification"] = "NOT_CLAIMED"
    return core


@app.post("/lcp/intelligence")
def lcp_intelligence(payload: dict = Body(...), live_stations: bool = False):
    """Compose the full LCP evidence chain from deterministic URBION modules."""
    raw_assessment = payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw_assessment, dict):
        raise HTTPException(status_code=422, detail={"code":"ASSESSMENT_INPUT_REQUIRED","message":"Provide an assessment object using the normal /assess input contract."})
    try:
        assessment = assess_core(AssessmentRequest(**raw_assessment))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_LCP_INPUT","message":str(exc)})
    station_snapshot = payload.get("station_snapshot")
    if live_stations:
        station_snapshot = build_live_station_snapshot(assessment["site"]["latitude"], assessment["site"]["longitude"], assessment["site"].get("state", "Melaka"), int(payload.get("station_limit", 5)))
    return build_lcp_intelligence(
        assessment=assessment,
        development_inputs=payload.get("development_inputs"),
        policy_links=payload.get("policy_links"),
        national_links=payload.get("national_links"),
        sdg_links=payload.get("sdg_links"),
        spatial_inputs=payload.get("spatial_inputs"),
        station_snapshot=station_snapshot,
        km_inputs=payload.get("km_inputs"),
    )


@app.post("/lcp/release-packet")
def lcp_release_packet(payload: dict = Body(...)):
    """Create a compact auditable handoff packet from an existing LCP result."""
    lcp = payload.get("lcp") or payload.get("lcp_intelligence")
    if not isinstance(lcp, dict):
        raise HTTPException(status_code=422, detail={"code":"LCP_RESULT_REQUIRED","message":"Provide an LCP intelligence result."})
    return build_release_packet(lcp)
