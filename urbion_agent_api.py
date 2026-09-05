"""Production API surfaces for URBION's bounded planning-agent synthesis and copilot."""
from fastapi import APIRouter, Body, HTTPException
from server import app, AssessmentRequest, assess_core
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_what_if import build_scenario_plan, compare_assessments
from urbion_scenario_ranking import rank_scenarios
from urbion_decision_center import build_decision_center
from urbion_agent_orchestrator import run_agents
from urbion_copilot import build_copilot_packet

router = APIRouter(tags=["planning-agents"])

def _run(payload: dict):
    raw = payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw, dict): raise HTTPException(status_code=422, detail={"code":"ASSESSMENT_INPUT_REQUIRED"})
    try: assessment = assess_core(AssessmentRequest(**raw))
    except Exception as exc: raise HTTPException(status_code=422, detail={"code":"INVALID_ASSESSMENT_INPUT","message":str(exc)}) from exc
    spatial = build_spatial_intelligence(assessment["site"]["latitude"], assessment["site"]["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(payload.get("radii") or (400,800)), payload.get("constraints"))
    variants = payload.get("variants") or []
    if not isinstance(variants, list) or len(variants) > 12: raise HTTPException(status_code=422, detail={"code":"INVALID_SCENARIO_VARIANTS"})
    plans = build_scenario_plan(raw, variants)
    executed = [{"id":p["id"],"name":p["name"],"assessment":assess_core(AssessmentRequest(**p["inputs"]))} for p in plans]
    scenarios = rank_scenarios(compare_assessments(assessment, executed)) if executed else None
    decision = build_decision_center(assessment=assessment)
    return run_agents(assessment=assessment, spatial=spatial, scenarios=scenarios, decision=decision)

@router.post("/agents/run")
def run_agent_workflow(payload: dict = Body(default_factory=dict)): return _run(payload)

@router.post("/copilot/run")
def run_copilot_workflow(payload: dict = Body(default_factory=dict)):
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code":"SITE_INPUT_REQUIRED"})
    try:
        return build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400,800), constraints=payload.get("constraints"))
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"COPILOT_INPUT_ERROR","message":str(exc)}) from exc

app.include_router(router)
