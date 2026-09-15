"""End-to-end planning workstation bridge for the championship release."""
from __future__ import annotations
import faulthandler
import time
from concurrent.futures import ThreadPoolExecutor
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

@router.get("/workstation/metadata")
def workstation_metadata():
    return {
        "project": "URBION HORIZON",
        "version": "PHASE-E.8",
        "status": "ready",
        "workflow": "Planner Decision Workstation",
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
    }


def _build_lcp(assessment, payload, comparison):
    return build_lcp_intelligence(
        assessment=assessment,
        development_inputs=payload.get("development_inputs"),
        policy_links=payload.get("policy_links"),
        national_links=payload.get("national_links"),
        sdg_links=payload.get("sdg_links"),
        spatial_inputs=payload.get("spatial_inputs"),
        station_snapshot=payload.get("station_snapshot"),
        km_inputs=payload.get("km_inputs"),
        what_if_summary=comparison,
        environment_context=payload.get("environment_context"),
        agency_assets=payload.get("agency_assets"),
        agency_radius_m=float(payload.get("agency_radius_m",5000)),
        guideline_topics=payload.get("guideline_topics"),
    )


def _build_km(raw, payload):
    return build_km_readiness(
        pbt=raw.get("pbt",""),
        development_type=raw.get("development_type",""),
        documents=payload.get("documents"),
        km_category=payload.get("km_category"),
        technical_reviews=payload.get("technical_reviews"),
    )


def _build_agents(assessment, spatial, comparison, decision):
    return run_agents(assessment=assessment, spatial=spatial, scenarios=comparison, decision=decision)


def _timed_future(name, future, started):
    value = future.result()
    elapsed = time.perf_counter() - started
    print(f"[URBION-ANALYSIS-STAGE] {name}={elapsed:.3f}s", flush=True)
    return value


@router.post("/workstation/analysis")
def workstation_analysis(payload: dict = Body(default_factory=dict)):
    started = time.perf_counter()
    marks: dict[str, float] = {}
    dump_cm = faulthandler.dump_traceback_later(15.0, repeat=False)
    raw = payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw, dict):
        faulthandler.cancel_dump_traceback_later()
        raise HTTPException(status_code=422, detail={"code":"ASSESSMENT_INPUT_REQUIRED"})
    try:
        stage = time.perf_counter()
        assessment = assess_core(AssessmentRequest(**raw))
        marks["ASSESSMENT"] = time.perf_counter() - stage
        print(f"[URBION-ANALYSIS-STAGE] ASSESSMENT={marks['ASSESSMENT']:.3f}s", flush=True)
    except Exception as exc:
        faulthandler.cancel_dump_traceback_later()
        raise HTTPException(status_code=422, detail={"code":"INVALID_ASSESSMENT_INPUT","message":str(exc)}) from exc
    site = assessment["site"]
    steps = [{"id":"ASSESSMENT","label":"Site assessment","status":"COMPLETE"}]
    stage = time.perf_counter()
    spatial = build_spatial_intelligence(site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(payload.get("radii") or (400,800)), payload.get("constraints"))
    marks["SPATIAL"] = time.perf_counter() - stage
    print(f"[URBION-ANALYSIS-STAGE] SPATIAL={marks['SPATIAL']:.3f}s", flush=True)
    steps.append({"id":"SPATIAL","label":"Spatial intelligence","status":"COMPLETE"})
    variants = payload.get("variants") or payload.get("scenario_variants") or []
    if not isinstance(variants, list) or len(variants) > 12 or any(not isinstance(v, dict) for v in variants):
        faulthandler.cancel_dump_traceback_later()
        raise HTTPException(status_code=422, detail={"code":"INVALID_SCENARIO_VARIANTS"})
    stage = time.perf_counter()
    plans = build_scenario_plan(raw, variants)
    executed = []
    for plan in plans:
        executed.append({
            "id":plan["id"],
            "name":plan["name"],
            "inputs":dict(plan["inputs"]),
            "baseline_inputs":dict(plan["baseline_inputs"]),
            "overrides":dict(plan["overrides"]),
            "assessment":assess_core(AssessmentRequest(**plan["inputs"])),
        })
    comparison = rank_scenarios(compare_assessments(assessment, executed)) if executed else {"scenarios":[],"ranked_scenarios":[]}
    marks["WHAT_IF"] = time.perf_counter() - stage
    print(f"[URBION-ANALYSIS-STAGE] WHAT_IF={marks['WHAT_IF']:.3f}s count={len(executed)}", flush=True)
    steps.append({"id":"WHAT_IF","label":"Scenario comparison","status":"COMPLETE" if executed else "SKIPPED","count":len(executed)})
    stage = time.perf_counter()
    decision = build_decision_center(assessment=assessment)
    marks["DECISION"] = time.perf_counter() - stage
    print(f"[URBION-ANALYSIS-STAGE] DECISION={marks['DECISION']:.3f}s", flush=True)
    steps.append({"id":"DECISION","label":"Decision centre","status":"COMPLETE"})

    stage = time.perf_counter()
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="urbion-analysis") as pool:
        f_lcp = pool.submit(_build_lcp, assessment, payload, comparison if executed else None)
        f_km = pool.submit(_build_km, raw, payload)
        f_agents = pool.submit(_build_agents, assessment, spatial, comparison if executed else None, decision)
        lcp = _timed_future("LCP", f_lcp, stage)
        km = _timed_future("KM", f_km, stage)
        agents = _timed_future("AGENTS", f_agents, stage)
    marks["ENRICHMENTS_PARALLEL"] = time.perf_counter() - stage
    steps.append({"id":"LCP","label":"LCP intelligence","status":"COMPLETE"})
    steps.append({"id":"KM","label":"KM readiness","status":"COMPLETE"})
    steps.append({"id":"AGENTS","label":"Bounded agent synthesis","status":"COMPLETE"})
    total = time.perf_counter() - started
    marks["TOTAL"] = total
    faulthandler.cancel_dump_traceback_later()
    print("[URBION-ANALYSIS-TIMING] " + " ".join(f"{k}={v:.3f}s" for k, v in marks.items()), flush=True)
    return {"project":"URBION HORIZON","version":"PHASE-E.8","workflow":{"name":"Planner Decision Workstation","steps":steps,"completed":sum(x["status"]=="COMPLETE" for x in steps),"total":len(steps)},"assessment":assessment,"spatial":spatial,"what_if":comparison,"decision_center":decision,"lcp_intelligence":lcp,"km_readiness":km,"agents":agents,"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED"}

app.include_router(router)
