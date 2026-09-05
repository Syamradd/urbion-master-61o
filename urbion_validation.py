"""Canonical validation cases and compact evidence cards for URBION HORIZON.

These cases are deterministic demonstration fixtures. Result values are generated
by the same production engines used by the application so the report can point
to a repeatable live validation path instead of fabricated screenshots.
"""
from __future__ import annotations
from typing import Any
from urbion_demo_scenarios import get_demo_scenario
from urbion_spatial_intelligence import build_spatial_intelligence

VALIDATION_CASES=(
 {"id":"TC-01","scenario_id":"TOD-COMPLY","title":"GIS Spatial Proximity","purpose":"Validate GIS feature proximity and TOD spatial classification.","focus":"GIS & Spatial Validation"},
 {"id":"TC-02","scenario_id":"SHOP-FAIL","title":"Planning Rule & Compliance","purpose":"Validate retrieval of planning controls and rule-based compliance review.","focus":"Rule Retrieval & Compliance"},
 {"id":"TC-03","scenario_id":"TOD-COMPLY","title":"End-to-End Assessment","purpose":"Demonstrate the integrated assessment, spatial, evidence, decision and scenario workflow.","focus":"End-to-End Assessment","variants":[{"id":"LOWER-DENSITY","name":"Lower Density","overrides":{"plot_ratio":3.0}},{"id":"HIGHER-DENSITY","name":"Higher Density","overrides":{"plot_ratio":6.0}}]},
)

def validation_cases()->list[dict[str,Any]]:
 return [dict(item,variants=[dict(v,overrides=dict(v.get("overrides",{}))) for v in item.get("variants",[])]) for item in VALIDATION_CASES]

def get_validation_case(case_id:str)->dict[str,Any]|None:
 return next((item for item in validation_cases() if item["id"]==case_id),None)

def _compact_assessment(result:dict[str,Any])->dict[str,Any]:
 site=result.get("site",{}) or {}; evidence=result.get("evidence_state",{}) or {}
 return {"status":result.get("final_status"),"recommendation":result.get("recommendation"),"decision_confidence":result.get("decision_confidence"),"site":{"latitude":site.get("latitude"),"longitude":site.get("longitude"),"pbt":site.get("pbt"),"lot_no":site.get("lot_no")},"tod":{"distance_m":result.get("tod_distance_m"),"classification":result.get("classification")},"rules":{"retrieved_count":len(result.get("retrieved_rules",[]) or []),"applicability_count":len(result.get("applicability_results",[]) or []),"compliance_count":len(result.get("compliance_results",[]) or [])},"evidence_state":evidence,"decision_trace":result.get("decision_trace",[])}

def _compact_spatial(result:dict[str,Any])->dict[str,Any]:
 return {"site":result.get("site"),"tod":result.get("tod"),"tod_distance_m":result.get("tod_distance_m"),"tod_classification":result.get("tod_classification"),"planning_signals":result.get("planning_signals",{}) or {},"evidence_model":result.get("evidence_model",{}),"review_gaps":result.get("review_gaps",[]),"statutory_verification":result.get("statutory_verification") or "NOT_CLAIMED"}

def _compact_copilot(packet:dict[str,Any])->dict[str,Any]:
 decision=packet.get("decision",{}) or {}; knowledge=packet.get("knowledge",{}) or {}; impact=packet.get("impact",{}) or {}; scenario=packet.get("scenario_intelligence",{}) or {}
 return {"mode":packet.get("mode"),"assessment":_compact_assessment(packet.get("assessment",{}) or {}),"knowledge":{"retrieval_count":knowledge.get("retrieval_count"),"evidence_state":knowledge.get("evidence_state"),"review_gaps":knowledge.get("review_gaps",[])},"impact":{"status":impact.get("status"),"evidence_state":impact.get("evidence_state"),"signal_count":impact.get("signal_count"),"domains":impact.get("domains")},"scenario":{"status":scenario.get("status"),"count":scenario.get("count"),"ranked_scenarios":scenario.get("ranked_scenarios",[]),"best_candidate":scenario.get("best_candidate")},"decision":{"status":decision.get("decision",{}).get("status"),"confidence":decision.get("decision",{}).get("confidence"),"next_actions":decision.get("next_actions",[])},"guardrails":{"decision_authority":packet.get("decision_authority"),"statutory_verification":packet.get("statutory_verification")},"evidence_ledger":packet.get("evidence_ledger",{})}

def run_validation_case(case_id:str,assess_fn,copilot_fn)->dict[str,Any]|None:
 case=get_validation_case(case_id)
 if not case:return None
 scenario=get_demo_scenario(case["scenario_id"])
 if not scenario:raise ValueError(f"Missing demo scenario: {case['scenario_id']}")
 inputs=dict(scenario["inputs"])
 if case_id=="TC-01":
  result=assess_fn(inputs); spatial=build_spatial_intelligence(inputs["site_lat"],inputs["site_lon"],inputs.get("tod_lat"),inputs.get("tod_lon")); evidence_card=_compact_assessment(result); evidence_card["spatial"]=_compact_spatial(spatial); evidence_card["validation_path"]=["ASSESSMENT","SPATIAL"]
 elif case_id=="TC-03":
  result=copilot_fn(inputs,variants=case.get("variants")); evidence_card=_compact_copilot(result); evidence_card["validation_path"]=["ASSESSMENT","SPATIAL","KNOWLEDGE","IMPACT","SCENARIO","DECISION","AGENTS","EVIDENCE_LEDGER"]
 else:
  result=assess_fn(inputs); evidence_card={"assessment":_compact_assessment(result),"validation_path":["ASSESSMENT","POLICY","APPLICABILITY","COMPLIANCE"]}
 return {"case":{"id":case["id"],"title":case["title"],"purpose":case["purpose"],"focus":case["focus"],"scenario_id":case["scenario_id"]},"evidence_card":evidence_card,"result":result}
