"""Production API surfaces for URBION's bounded planning-agent synthesis and copilot."""
import json

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from server import app, AssessmentRequest, assess_core
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_what_if import build_scenario_plan, compare_assessments
from urbion_scenario_ranking import rank_scenarios
from urbion_decision_center import build_decision_center
from urbion_agent_orchestrator import run_agents
from urbion_copilot import build_copilot_packet
from urbion_validation import validation_cases, run_validation_case
from urbion_planner_handoff import build_planner_handoff_from_copilot
from urbion_judge_demo import build_judge_demo
from urbion_llm_provider import generate_planner_explanation
from urbion_decision_os import build_decision_os
from urbion_championship_optional_assessment_api import assess_optional, what_if_ui
import urbion_frontend_asset_guard

router = APIRouter(tags=["planning-agents"])


@app.middleware("http")
async def _optional_tod_compat(request: Request, call_next):
    """Route only TOD-optional UI payloads through the existing optional adapter.

    Complete TOD payloads continue through the original production endpoints, so
    deterministic planning behaviour is unchanged unless the caller actually
    exercises the optional-TOD contract.
    """
    if request.method != "POST" or request.url.path not in {"/assess", "/what-if"}:
        return await call_next(request)

    body = await request.body()
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return await call_next(request)

    target = payload.get("baseline") if request.url.path == "/what-if" and isinstance(payload, dict) else payload
    if not isinstance(target, dict):
        return await call_next(request)

    tod_keys = ("tod_lat", "tod_lon")
    missing_tod = all(target.get(key) in (None, "") for key in tod_keys)
    partial_tod = (target.get("tod_lat") in (None, "")) != (target.get("tod_lon") in (None, ""))
    if not (missing_tod or partial_tod):
        return await call_next(request)

    try:
        if request.url.path == "/assess":
            return JSONResponse(content=assess_optional(payload))
        return JSONResponse(content=what_if_ui(payload))
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as exc:
        return JSONResponse(status_code=422, content={"detail": {"code": "OPTIONAL_TOD_INPUT_ERROR", "message": str(exc)}})


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

@router.post("/copilot/explain")
def explain_copilot_workflow(payload: dict = Body(default_factory=dict)):
    """Add optional LLM narrative without changing deterministic planning outputs."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code":"SITE_INPUT_REQUIRED"})
    try:
        packet = build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400, 800), constraints=payload.get("constraints"))
        explanation = generate_planner_explanation(packet)
        return {"mode":"BOUNDED_PLANNER_COPILOT_LLM","explanation":explanation,"evidence_ledger":packet.get("evidence_ledger") or {},"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED","deterministic_packet":packet,"generation_boundary":"LLM_NARRATIVE_ONLY; DETERMINISTIC_PACKET_REMAINS_SOURCE_OF_TRUTH"}
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"COPILOT_EXPLANATION_ERROR","message":str(exc)}) from exc

@router.post("/intelligence/decision-os")
def decision_os_workflow(payload: dict = Body(default_factory=dict)):
    """Run the unified deterministic copilot, then apply an evidence-gated planner-review gate."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code":"SITE_INPUT_REQUIRED"})
    try:
        packet = build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400, 800), constraints=payload.get("constraints"))
        result = build_decision_os(packet)
        return {"mode":"URBION_DECISION_OS","decision_os":result,"deterministic_packet":packet,"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED"}
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"DECISION_OS_ERROR","message":str(exc)}) from exc

@router.post("/planner/handoff")
def run_planner_handoff(payload: dict = Body(default_factory=dict)):
    """Run the production copilot and convert its evidence into a planner handoff."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code":"SITE_INPUT_REQUIRED"})
    try:
        return build_planner_handoff_from_copilot(inputs,copilot_fn=lambda raw: build_copilot_packet(raw,variants=payload.get("variants"),radii=payload.get("radii") or (400,800),constraints=payload.get("constraints")))
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"PLANNER_HANDOFF_ERROR","message":str(exc)}) from exc

@router.post("/judge/demo")
def run_judge_demo(payload: dict = Body(default_factory=dict)):
    """Run one production copilot path and return a judge-ready evidence snapshot."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code":"SITE_INPUT_REQUIRED"})
    try: return build_judge_demo(inputs, build_copilot_packet)
    except Exception as exc: raise HTTPException(status_code=422, detail={"code":"JUDGE_DEMO_ERROR","message":str(exc)}) from exc

@router.get("/validation/cases")
def list_validation_cases():
    """Return the three canonical report validation cases without executing them."""
    return {"project":"URBION HORIZON","cases":validation_cases()}

@router.post("/validation/run/{case_id}")
def execute_validation_case(case_id: str):
    """Execute one report validation case through the same production engines."""
    try: result = run_validation_case(case_id, assess_fn=lambda inputs: assess_core(AssessmentRequest(**inputs)), copilot_fn=build_copilot_packet)
    except Exception as exc: raise HTTPException(status_code=422, detail={"code":"VALIDATION_CASE_ERROR","message":str(exc)}) from exc
    if result is None: raise HTTPException(status_code=404, detail={"code":"VALIDATION_CASE_NOT_FOUND","case_id":case_id})
    return result

app.include_router(router)
