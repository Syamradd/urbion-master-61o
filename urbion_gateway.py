"""Deployment gateway for optional advisory and intelligence integrations."""
from fastapi import Body, HTTPException
from server import AssessmentRequest, app, assess_core
from urbion_gemini_redteam import gemini_configured, review_with_gemini
from urbion_live_stations import build_live_station_snapshot
from urbion_station_intelligence import build_station_intelligence, _valid_coord
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_environment_intelligence import build_environment_intelligence
from urbion_iplan import query_environment_context
from urbion_release_packet import build_release_packet
from urbion_review_packet import build_review_packet
from urbion_release_contract import build_championship_gate
from urbion_what_if import execute_what_if
import json
from pathlib import Path


def _validate_site_coords(site_lat: float, site_lon: float) -> None:
    if not _valid_coord(site_lat, site_lon) or (float(site_lat), float(site_lon)) == (-90.0, -180.0):
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT"})


@app.get("/gemini/status")
def gemini_status(): return {"provider":"Google Gemini","role":"RED_TEAM_ADVISORY","configured":gemini_configured(),"decision_authority":"NONE"}
@app.post("/gemini/red-team")
def gemini_red_team(packet:dict=Body(...)): return review_with_gemini(packet)
@app.post("/gemini/red-team-assessment")
def gemini_red_team_assessment(r:AssessmentRequest): return review_with_gemini({"assessment":assess_core(r),"guardrails":{"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED","purpose":"independent red-team review only"}})
@app.get("/stations/nearby")
def stations_nearby(site_lat:float,site_lon:float,state:str="Melaka",limit:int=5):
    _validate_site_coords(site_lat, site_lon)
    return build_live_station_snapshot(site_lat,site_lon,state,limit)
@app.get("/station-intelligence")
def station_intelligence(site_lat:float,site_lon:float,state:str="Melaka"):
    _validate_site_coords(site_lat, site_lon)
    live=build_live_station_snapshot(site_lat,site_lon,state,5);core=build_station_intelligence(site_lat,site_lon,state);core["live_snapshot"]=live;core["decision_boundary"]="OBSERVATION_CONTEXT";core["statutory_verification"]="NOT_CLAIMED";return core
@app.post("/environment/intelligence")
def environment_intelligence(payload:dict=Body(default_factory=dict)):
    context=payload.get("environment_context") or payload.get("context")
    if context is None and payload.get("site_lat") is not None and payload.get("site_lon") is not None: context=query_environment_context(float(payload["site_lat"]),float(payload["site_lon"]),float(payload.get("radius_m",1000)),payload.get("state","Melaka"))
    return build_environment_intelligence(context or payload)
@app.post("/lcp/intelligence")
def lcp_intelligence(payload:dict=Body(...),live_stations:bool=False,auto_environment:bool=True):
    raw=payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw,dict): raise HTTPException(status_code=422,detail={"code":"ASSESSMENT_INPUT_REQUIRED"})
    try: assessment=assess_core(AssessmentRequest(**raw))
    except Exception as exc: raise HTTPException(status_code=422,detail={"code":"INVALID_LCP_INPUT","message":str(exc)})
    station=payload.get("station_snapshot")
    if live_stations: station=build_live_station_snapshot(assessment["site"]["latitude"],assessment["site"]["longitude"],assessment["site"].get("state","Melaka"),int(payload.get("station_limit",5)))
    env=payload.get("environment_context")
    if env is None and auto_environment: env=query_environment_context(assessment["site"]["latitude"],assessment["site"]["longitude"],float(payload.get("environment_radius_m",1000)),assessment["site"].get("state","Melaka"))
    variants=payload.get("scenario_variants") or payload.get("variants");what_if=None
    if variants:
        if not isinstance(variants,list) or len(variants)>12: raise HTTPException(status_code=422,detail={"code":"INVALID_SCENARIO_VARIANTS"})
        comparison=execute_what_if(raw,variants,lambda inputs:assess_core(AssessmentRequest(**inputs)));what_if={k:comparison.get(k) for k in ["title","version","baseline_status","baseline_score","scenarios","ranked_scenarios","best_candidate","disclaimer"]}
    return build_lcp_intelligence(assessment=assessment,development_inputs=payload.get("development_inputs"),policy_links=payload.get("policy_links"),national_links=payload.get("national_links"),sdg_links=payload.get("sdg_links"),spatial_inputs=payload.get("spatial_inputs"),station_snapshot=station,km_inputs=payload.get("km_inputs"),what_if_summary=what_if,environment_context=env,agency_assets=payload.get("agency_assets"),agency_radius_m=float(payload.get("agency_radius_m",5000)),guideline_topics=payload.get("guideline_topics"))
@app.post("/lcp/release-packet")
def lcp_release_packet(payload:dict=Body(...)):
    lcp=payload.get("lcp") or payload.get("lcp_intelligence")
    if not isinstance(lcp,dict): raise HTTPException(status_code=422,detail={"code":"LCP_RESULT_REQUIRED"})
    return build_release_packet(lcp)
@app.post("/lcp/review-packet")
def lcp_review_packet(payload:dict=Body(...)):
    lcp=payload.get("lcp") or payload.get("lcp_intelligence")
    if not isinstance(lcp,dict): raise HTTPException(status_code=422,detail={"code":"LCP_RESULT_REQUIRED"})
    return build_review_packet(lcp=lcp)
@app.get("/championship-gate")
def championship_gate():
    manifest=json.loads((Path(__file__).resolve().parent/"DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"));return build_championship_gate(lcp=build_lcp_intelligence(assessment=assess_core(AssessmentRequest(site_lat=2.285,site_lon=102.196,tod_lat=2.286,tod_lon=102.197))),manifest=manifest)
