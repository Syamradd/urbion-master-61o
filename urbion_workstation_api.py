"""End-to-end planning workstation bridge for the championship release."""
from fastapi import APIRouter, Body, HTTPException
from server import app, AssessmentRequest, assess_core
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_what_if import build_scenario_plan, compare_assessments
from urbion_scenario_ranking import rank_scenarios
from urbion_decision_center import build_decision_center
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_kebenaran_merancang import build_km_readiness
from urbion_agent_orchestrator import run_agents

router = APIRouter(tags=["planner-workstation"])

@router.post("/workstation/analysis")
def workstation_analysis(payload: dict = Body(default_factory=dict)):
    raw = payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=422, detail={"code":"ASSESSMENT_INPUT_REQUIRED"})
    try:
        assessment = assess_core(AssessmentRequest(**raw))
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_ASSESSMENT_INPUT","message":str(exc)}) from exc
    site = assessment["site"]
    steps = [{"id":"ASSESSMENT","label":"Site assessment","status":"COMPLETE"}]
    spatial = build_spatial_intelligence(site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(payload.get("radii") or (400,800)), payload.get("constraints"))
    steps.append({"id":"SPATIAL","label":"Spatial intelligence","status":"COMPLETE"})
    variants = payload.get("variants") or payload.get("scenario_variants") or []
    if not isinstance(variants, list) or len(variants) > 12:
        raise HTTPException(status_code=422, detail={"code":"INVALID_SCENARIO_VARIANTS"})
    plans = build_scenario_plan(raw, variants)
    executed = []
    for plan in plans:
        executed.append({"id":plan["id"],"name":plan["name"],"assessment":assess_core(AssessmentRequest(**plan["inputs"]))})
    comparison = rank_scenarios(compare_assessments(assessment, executed)) if executed else {"scenarios":[],"ranked_scenarios":[]}
    steps.append({"id":"WHAT_IF","label":"Scenario comparison","status":"COMPLETE" if executed else "SKIPPED","count":len(executed)})
    decision = build_decision_center(assessment=assessment)
    steps.append({"id":"DECISION","label":"Decision centre","status":"COMPLETE"})
    lcp = build_lcp_intelligence(assessment=assessment, development_inputs=payload.get("development_inputs"), policy_links=payload.get("policy_links"), national_links=payload.get("national_links"), sdg_links=payload.get("sdg_links"), spatial_inputs=payload.get("spatial_inputs"), station_snapshot=payload.get("station_snapshot"), km_inputs=payload.get("km_inputs"), what_if_summary=comparison if executed else None, environment_context=payload.get("environment_context"), agency_assets=payload.get("agency_assets"), agency_radius_m=float(payload.get("agency_radius_m",5000)), guideline_topics=payload.get("guideline_topics"))
    steps.append({"id":"LCP","label":"LCP intelligence","status":"COMPLETE"})
    km = build_km_readiness(pbt=raw.get("pbt",""), development_type=raw.get("development_type",""), documents=payload.get("documents"), km_category=payload.get("km_category"), technical_reviews=payload.get("technical_reviews"))
    steps.append({"id":"KM","label":"KM readiness","status":"COMPLETE"})
    agents = run_agents(assessment=assessment, spatial=spatial, scenarios=comparison if executed else None, decision=decision)
    steps.append({"id":"AGENTS","label":"Bounded agent synthesis","status":"COMPLETE"})
    return {"project":"URBION HORIZON","version":"PHASE-E.8","workflow":{"name":"Planner Decision Workstation","steps":steps,"completed":sum(x["status"]=="COMPLETE" for x in steps),"total":len(steps)},"assessment":assessment,"spatial":spatial,"what_if":comparison,"decision_center":decision,"lcp_intelligence":lcp,"km_readiness":km,"agents":agents,"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED"}

app.include_router(router)
