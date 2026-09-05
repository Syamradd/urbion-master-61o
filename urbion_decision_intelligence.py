"""Explainable decision-intelligence layer for URBION HORIZON.

This module deliberately separates calculated decision support from statutory
verification. It consumes an existing assessment and turns its evidence into
priorities, confidence signals and scenario sensitivity without inventing
planning standards.
"""
from __future__ import annotations


def _status_weight(status: str | None) -> float:
    return {
        "COMPLY": 1.0,
        "CONDITIONAL RISK": 0.65,
        "REQUIRES REVIEW": 0.45,
        "NON-COMPLIANCE": 0.15,
        "NOT APPLICABLE": 0.9,
        "NOT_LOADED": 0.25,
    }.get(str(status or "").upper(), 0.35)


def _priority(status: str | None) -> str:
    s = str(status or "").upper()
    if "NON-COMPLIANCE" in s:
        return "HIGH"
    if "CONDITIONAL" in s or "REQUIRES REVIEW" in s or "NOT_LOADED" in s:
        return "MEDIUM"
    return "LOW"


def build_decision_intelligence(assessment: dict) -> dict:
    compliance = list(assessment.get("compliance_results") or [])
    rules = list(assessment.get("retrieved_rules") or [])
    spatial = assessment.get("spatial") or {}
    evidence = assessment.get("evidence_state") or {}
    final_status = assessment.get("final_status") or "REQUIRES REVIEW"

    actions = []
    for item in compliance:
        rule_id = item.get("rule_id") or "UNMAPPED"
        status = item.get("status") or item.get("compliance") or "REQUIRES REVIEW"
        actions.append({
            "rule_id": rule_id,
            "priority": _priority(status),
            "status": status,
            "applicability": item.get("applicability", "UNKNOWN"),
            "reason": item.get("reason") or item.get("message") or "Review the applicable evidence and planning requirement.",
            "evidence": "SOURCE_CONTEXT" if rules else "UNVERIFIED",
        })
    actions.sort(key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["priority"]])

    source_score = 1.0 if rules else 0.25
    compliance_score = sum(_status_weight(x.get("status") or x.get("compliance")) for x in compliance) / len(compliance) if compliance else 0.35
    spatial_score = 1.0 if assessment.get("tod_distance_m") is not None else 0.25
    evidence_score = sum(1 for value in evidence.values() if value in {"CALCULATED", "SOURCE_CONTEXT", "VERIFIED"}) / max(1, len(evidence))
    confidence = round(max(0.0, min(1.0, 0.30 * source_score + 0.30 * compliance_score + 0.20 * spatial_score + 0.20 * evidence_score)), 3)

    return {
        "version": "DI-1",
        "decision_status": final_status,
        "confidence": {"score": confidence, "band": "HIGH" if confidence >= 0.8 else ("MEDIUM" if confidence >= 0.5 else "LOW")},
        "evidence_breakdown": {
            "planning_rules_loaded": bool(rules),
            "retrieved_rule_count": len(rules),
            "spatial_distance_calculated": assessment.get("tod_distance_m") is not None,
            "statutory_verification": "NOT_CLAIMED",
        },
        "priority_actions": actions[:12],
        "decision_boundary": "DECISION_SUPPORT_ONLY",
        "next_best_actions": [
            "Validate authoritative planning documents and current local requirements before submission.",
            "Resolve every HIGH or MEDIUM priority item using source evidence.",
            "Use What-If comparisons to test proposal changes before finalising the scheme.",
        ],
        "provenance": "Calculated from the supplied assessment, retrieved rule context and evidence states; no statutory threshold is inferred.",
    }


def build_sensitivity_matrix(assessment: dict) -> dict:
    proposal = assessment.get("proposal") or {}
    baseline = {
        "plot_ratio": proposal.get("Plot Ratio"),
        "building_height": proposal.get("Building Height"),
        "perimeter_planting": proposal.get("Perimeter Planting"),
        "landscaped_pedestrian_walkway": proposal.get("Landscaped Pedestrian Walkway"),
    }
    dimensions = []
    for key, label in [
        ("plot_ratio", "Plot Ratio"),
        ("building_height", "Building Height"),
        ("perimeter_planting", "Perimeter Planting"),
        ("landscaped_pedestrian_walkway", "Landscaped Pedestrian Walkway"),
    ]:
        value = baseline[key]
        dimensions.append({
            "parameter": key,
            "label": label,
            "baseline": value,
            "sensitivity": "INPUT-DEPENDENT" if value is not None else "NOT_PROVIDED",
            "reason": "Changes may alter downstream assessment results; rerun the assessment rather than assuming compliance impact.",
            "evidence": "USER_PROVIDED" if value is not None else "UNVERIFIED",
        })
    return {
        "version": "DI-1",
        "dimensions": dimensions,
        "method": "Deterministic rerun recommended for each changed input; no undocumented planning threshold is applied.",
        "statutory_verification": "NOT_CLAIMED",
    }
