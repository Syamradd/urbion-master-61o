"""Deployment gateway that adds optional advisory integrations without changing core rules."""
from fastapi import Body
from server import AssessmentRequest, app, assess_core
from urbion_gemini_redteam import gemini_configured, review_with_gemini
from urbion_live_stations import build_live_station_snapshot
from urbion_station_intelligence import build_station_intelligence


@app.get("/gemini/status")
def gemini_status():
    return {
        "provider": "Google Gemini",
        "role": "RED_TEAM_ADVISORY",
        "configured": gemini_configured(),
        "decision_authority": "NONE",
    }


@app.post("/gemini/red-team")
def gemini_red_team(packet: dict = Body(...)):
    return review_with_gemini(packet)


@app.post("/gemini/red-team-assessment")
def gemini_red_team_assessment(r: AssessmentRequest):
    """Run Gemini against the deterministic URBION assessment as an advisory review."""
    assessment = assess_core(r)
    packet = {
        "assessment": assessment,
        "guardrails": {
            "decision_authority": "NONE",
            "statutory_verification": "NOT_CLAIMED",
            "purpose": "independent red-team review only",
        },
    }
    return review_with_gemini(packet)


@app.get("/stations/nearby")
def stations_nearby(site_lat: float, site_lon: float, state: str = "Melaka", limit: int = 5):
    """Find nearby JPS rainfall and configured DOE air-quality stations."""
    if not (-90 <= site_lat <= 90 and -180 <= site_lon <= 180):
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"Site coordinates are outside valid bounds."})
    if (site_lat, site_lon) == (-90.0, -180.0):
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail={"code":"INVALID_SPATIAL_INPUT","message":"Placeholder coordinates cannot be used."})
    return build_live_station_snapshot(site_lat, site_lon, state, limit)


@app.get("/station-intelligence")
def station_intelligence(site_lat: float, site_lon: float, state: str = "Melaka"):
    """Unified LCP evidence contract; live adapters are injected/configured separately."""
    try:
        return build_station_intelligence(site_lat, site_lon, state)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail={"code": str(exc), "message": "Site coordinates are invalid or placeholder coordinates."})
