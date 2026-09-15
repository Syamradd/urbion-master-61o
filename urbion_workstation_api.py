"""End-to-end planning workstation bridge for the championship release."""
from __future__ import annotations
import faulthandler
import math
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


def _finite_number(value):
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def _normalise_yes_no_number(value):
    """Legacy Yes/No controls are preserved as unknown numeric evidence, not truthy numbers."""
    if value is None:
        return None
    if isinstance(value, str):
        token = value.strip().lower()
        if token in {"", "yes", "no", "n/a", "na", "not verified", "unverified"}:
            return None
    return _finite_number(value)


def _enrich_assessment_inputs(assessment: dict, raw: dict, spatial: dict | None = None) -> dict:
    """Carry explicit workstation inputs into the canonical assessment proposal.

    The historical AssessmentRequest intentionally stays small, while the
    workstation UI already collects additional planning inputs used by the
    impact/evidence layer. Preserve those explicit values here so downstream
    packet builders can use them without inventing data.
    """
    proposal = dict(assessment.get("proposal") or {})
    numeric_keys = {
        "units": raw.get("units"),
        "commercial_gfa_m2": raw.get("commercial_gfa_m2", raw.get("gfa")),
        "site_area_ha": raw.get("site_area_ha"),
        "jobs": raw.get("jobs"),
        "population": raw.get("population"),
        "daily_trips": raw.get("daily_trips"),
        "road_distance_m": raw.get("road_distance_m"),
    }
    for key, value in numeric_keys.items():
        number = _finite_number(value)
        if number is not None:
            proposal[key] = number

    # When a user supplies both GFA and plot ratio, site area can be transparently
    # calculated instead of silently assumed: area_ha = GFA / plot ratio / 10,000.
    if proposal.get("site_area_ha") is None:
        gfa = _finite_number(proposal.get("commercial_gfa_m2"))
        ratio = _finite_number(proposal.get("Plot Ratio"))
        if gfa is not None and ratio is not None and ratio > 0:
            proposal["site_area_ha"] = round(gfa / ratio / 10000.0, 6)
            proposal["site_area_basis"] = "CALCULATED_FROM_GFA_AND_PLOT_RATIO"

    flood = raw.get("flood_exposure")
    if isinstance(flood, bool):
        proposal["flood_exposure"] = flood
    nearby = raw.get("nearby_facilities")
    if isinstance(nearby, dict):
        clean = {str(k): v for k, v in nearby.items() if _finite_number(v) is not None}
        if clean:
            proposal["nearby_facilities"] = {k: _finite_number(v) for k, v in clean.items()}

    # Preserve the four land-use levels/context fields as planner inputs. These
    # are source/context fields and do not by themselves become statutory proof.
    for key in ("landuse1", "landuse2", "landuse3", "environment_note", "infra_note", "constraint_note", "source_note", "analysis_focus", "project_ref", "mukim"):
        if key in raw and raw.get(key) not in (None, ""):
            proposal[key] = raw.get(key)

    proposal["perimeter_planting"] = _normalise_yes_no_number(raw.get("perimeter_planting"))
    proposal["Landscaped Pedestrian Walkway"] = _normalise_yes_no_number(raw.get("landscaped_pedestrian_walkway"))
    proposal["shop_frontage_verified"] = bool(raw.get("shop_frontage_verified", False))
    proposal["shop_office_verified"] = bool(raw.get("shop_office_verified", False))

    if spatial:
        tod = spatial.get("tod") or {}
        if proposal.get("road_distance_m") is None:
            road = spatial.get("road_distance_m") or (spatial.get("planning_signals") or [])
            if isinstance(road, (int, float)):
                proposal["road_distance_m"] = _finite_number(road)
        proposal["spatial_intelligence"] = spatial

    assessment["proposal"] = proposal
    assessment["planning_inputs"] = {
        "land_use": {
            "level_1": raw.get("landuse1") or None,
            "level_2": raw.get("landuse2") or None,
            "level_3": raw.get("landuse3") or None,
        },
        "development_scale": {
            "units": proposal.get("units"),
            "commercial_gfa_m2": proposal.get("commercial_gfa_m2"),
            "site_area_ha": proposal.get("site_area_ha"),
        },
        "explicit_notes": {k: proposal.get(k) for k in ("environment_note", "infra_note", "constraint_note", "source_note") if proposal.get(k)},
        "impact_inputs_present": sum(proposal.get(k) is not None for k in ("units", "site_area_ha", "commercial_gfa_m2", "jobs", "population", "daily_trips", "road_distance_m", "flood_exposure", "nearby_facilities")),
    }
    return assessment


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
    stage = time.perf_counter()
    spatial = build_spatial_intelligence(site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(payload.get("radii") or (400,800)), payload.get("constraints"))
    marks["SPATIAL"] = time.perf_counter() - stage
    print(f"[URBION-ANALYSIS-STAGE] SPATIAL={marks['SPATIAL']:.3f}s", flush=True)
    assessment = _enrich_assessment_inputs(assessment, raw, spatial)
    steps = [{"id":"ASSESSMENT","label":"Site assessment","status":"COMPLETE"}]
    steps.append({"id":"SPATIAL","label":"Spatial intelligence","status":"COMPLETE"})
    variants = payload.get("variants") or payload.get("scenario_variants") or []
    if not isinstance(variants, list) or len(variants) > 12 or any(not isinstance(v, dict) for v in variants):
        faulthandler.cancel_dump_traceback_later()
        raise HTTPException(status_code=422, detail={"code":"INVALID_SCENARIO_VARIANTS"})
    stage = time.perf_counter()
    plans = build_scenario_plan(raw, variants)
    executed = []
    for plan in plans:
        variant_assessment = assess_core(AssessmentRequest(**plan["inputs"]))
        variant_assessment = _enrich_assessment_inputs(variant_assessment, plan["inputs"], spatial)
        executed.append({
            "id":plan["id"],
            "name":plan["name"],
            "inputs":dict(plan["inputs"]),
            "baseline_inputs":dict(plan["baseline_inputs"]),
            "overrides":dict(plan["overrides"]),
            "assessment":variant_assessment,
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
