"""UI compatibility routes for genuinely optional TOD context.

The deterministic planning engines remain unchanged. These routes only adapt the
request orchestration so a planner may run a site assessment without supplying a
TOD reference; missing TOD is represented as unavailable and never fabricated.
"""
from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any

from fastapi import APIRouter, HTTPException

from server import (
    assess_core as _legacy_assess_core,
    build_planning_value,
    classify,
    distance_m,
    normalise_class,
    policy_coverage,
    source_registry_snapshot,
    summarise_sources,
    decision_trace,
    urbion_create_spatial_context,
    urbion_retrieve_rules,
    urbion_check_applicability,
    urbion_evaluate_compliance,
    urbion_calculate_overall_status,
    build_site_analysis,
)

from urbion_scenario_ranking import rank_scenarios
from urbion_what_if import build_scenario_plan, compare_assessments

router = APIRouter(tags=["championship-ui-compat"])


def _payload_namespace(data: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(
        site_lat=float(data["site_lat"]),
        site_lon=float(data["site_lon"]),
        tod_lat=None if data.get("tod_lat") in (None, "") else float(data["tod_lat"]),
        tod_lon=None if data.get("tod_lon") in (None, "") else float(data["tod_lon"]),
        plot_ratio=float(data.get("plot_ratio", 4.5)),
        precinct=str(data.get("precinct", "Terminal Sg. Udang")),
        development_type=str(data.get("development_type", "New Development")),
        development_class=str(data.get("development_class", "Mixed Use")),
        state=str(data.get("state", "Melaka")),
        district=str(data.get("district", "Melaka Tengah")),
        pbt=str(data.get("pbt", "Majlis Bandaraya Melaka Bersejarah")),
        lot_no=str(data.get("lot_no", "")),
        building_height=data.get("building_height"),
        perimeter_planting=data.get("perimeter_planting"),
        landscaped_pedestrian_walkway=data.get("landscaped_pedestrian_walkway"),
        shop_frontage_verified=bool(data.get("shop_frontage_verified", False)),
        shop_office_verified=bool(data.get("shop_office_verified", False)),
    )


def assess_optional(data: dict[str, Any]) -> dict[str, Any]:
    r = _payload_namespace(data)
    if not all(math.isfinite(v) for v in (r.site_lat, r.site_lon)):
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT", "message": "Site coordinates must be finite numeric values."})
    if (r.tod_lat is None) != (r.tod_lon is None):
        raise HTTPException(status_code=422, detail={"code": "INCOMPLETE_TOD_INPUT", "message": "Provide both TOD latitude and longitude, or leave both blank."})
    if r.tod_lat is not None and not all(math.isfinite(v) for v in (r.tod_lat, r.tod_lon)):
        raise HTTPException(status_code=422, detail={"code": "INVALID_TOD_INPUT", "message": "TOD coordinates must be finite numeric values."})
    d = distance_m(r.site_lat, r.site_lon, r.tod_lat, r.tod_lon) if r.tod_lat is not None else None
    cl = classify(d) if d is not None else "NO TOD DISTANCE"
    dc = normalise_class(r.development_type, r.development_class)
    cov = policy_coverage(r.pbt)
    sc = urbion_create_spatial_context(
        precinct=r.precinct,
        precinct_verified=False,
        tod_verified=d is not None and d <= 800,
        tod_400_verified=d is not None and d <= 400,
        tod_800_verified=d is not None and d <= 800,
        shop_frontage_verified=r.shop_frontage_verified,
        shop_office_verified=r.shop_office_verified,
        tod_distance_m=d,
    )
    prop = {
        "development_type": r.development_type,
        "authority": "MBMB" if r.pbt == "Majlis Bandaraya Melaka Bersejarah" else r.pbt,
        "planning_reference": "RT MBMB 2035" if r.pbt == "Majlis Bandaraya Melaka Bersejarah" else "Local planning policy not loaded",
        "Plot Ratio": r.plot_ratio,
        "Building Height": r.building_height,
        "Perimeter Planting": r.perimeter_planting,
        "Landscaped Pedestrian Walkway": r.landscaped_pedestrian_walkway,
        "shop_frontage_verified": r.shop_frontage_verified,
        "shop_office_verified": r.shop_office_verified,
        "spatial_context": sc,
    }
    rr: list[dict] = []
    ar: list[dict] = []
    cr: list[dict] = []
    fr = None
    fs = "REQUIRES REVIEW"
    if r.pbt == "Majlis Bandaraya Melaka Bersejarah":
        rr = urbion_retrieve_rules(development_type=prop["development_type"], authority=prop["authority"], spatial_context=sc)
        ar = urbion_check_applicability(prop, rr)
        cr = urbion_evaluate_compliance(ar, prop)
        applicable = [x for x in cr if x.get("applicability") == "APPLICABLE"]
        if applicable:
            fr = applicable[0].get("rule_id")
            overall = urbion_calculate_overall_status(cr)
            fs = "NON-COMPLIANCE" if "NON-COMPLIANCE" in overall else ("CONDITIONAL RISK" if "CONDITIONAL RISK" in overall else ("COMPLY" if "COMPLY" in overall else fs))
        elif d is not None and cl == "OUTSIDE TOD 800m" and ("tod" in r.development_type.lower() or "mixed" in r.development_type.lower()):
            fs = "NOT APPLICABLE"
    else:
        cr = [{"rule_id": None, "applicability": "NOT_LOADED", "status": "REQUIRES REVIEW", "reason": "Local statutory rule set is not loaded into the verified decision engine."}]
    sa = build_site_analysis(
        state=r.state,
        district=r.district,
        pbt=r.pbt,
        lot_no=r.lot_no,
        latitude=r.site_lat,
        longitude=r.site_lon,
        tod_distance_m=d,
        development_class=dc,
        development_type=r.development_type,
        policy_status=fs,
        final_status=fs,
        retrieved_rules=len(rr),
    )
    reg = source_registry_snapshot()
    ei = summarise_sources(reg)
    trace = decision_trace(fs, rr, ar, cr)
    site = {
        "latitude": r.site_lat,
        "longitude": r.site_lon,
        "state": r.state,
        "district": r.district,
        "pbt": r.pbt,
        "lot_no": r.lot_no or "Not specified",
        "tod_distance_m": d,
    }
    pv = build_planning_value(site=site, final_status=fs, policy_coverage=cov, retrieved_rules=rr, compliance_results=cr, site_analysis=sa, evidence_intelligence=ei)
    return {
        "project": "URBION",
        "version": "PHASE-E.8",
        "site": site,
        "tod": {"latitude": r.tod_lat, "longitude": r.tod_lon},
        "precinct": r.precinct,
        "development_class": dc,
        "development_type": r.development_type,
        "proposal": prop,
        "tod_distance_m": d,
        "classification": cl,
        "policy_coverage": cov,
        "retrieved_rules": rr,
        "applicability_results": ar,
        "compliance_results": cr,
        "final_rule": fr,
        "final_status": fs,
        "site_analysis": sa,
        "recommendation": sa["recommendation"],
        "decision_confidence": sa["decision_confidence"],
        "planning_value": pv,
        "source_registry": reg,
        "evidence_intelligence": ei,
        "decision_trace": trace,
        "evidence_state": {
            "site_coordinates": "USER_PROVIDED",
            "tod_distance": "CALCULATED" if d is not None else "UNVERIFIED",
            "planning_rules": "SOURCE_CONTEXT" if rr else "UNVERIFIED",
            "final_decision": "CALCULATED",
            "statutory_verification": "NOT_CLAIMED",
        },
        "gis_provenance": "URBION GIS decision pipeline + official-source registry; missing TOD is disclosed and excluded from transit scoring.",
    }


@router.post("/assess-ui")
def assess_ui(data: dict[str, Any]):
    return assess_optional(data)


@router.post("/what-if-ui")
def what_if_ui(data: dict[str, Any]):
    baseline_data = dict(data.get("baseline") or {})
    baseline = assess_optional(baseline_data)
    plans = build_scenario_plan(baseline_data, list(data.get("variants") or []))
    executed = []
    for plan in plans:
        executed.append({"id": plan["id"], "name": plan["name"], "assessment": assess_optional(plan["inputs"])})
    return rank_scenarios(compare_assessments(baseline, executed))


from server import app
app.include_router(router)
