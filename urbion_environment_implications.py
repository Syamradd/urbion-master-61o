"""Translate environmental screening flags into explicit planning implications."""
from __future__ import annotations
from typing import Any

IMPLICATIONS = {
    "flood": ("Flood exposure", "Require flood-risk assessment and confirm applicable drainage/flood mitigation requirements."),
    "ksas": ("KSAS sensitivity", "Review development compatibility, avoidance/minimisation measures and applicable environmental controls."),
    "slope": ("Slope risk", "Require terrain/slope stability review and confirm applicable earthwork and development controls."),
    "geohazard": ("Geohazard exposure", "Require geotechnical/geohazard assessment and confirm appropriate mitigation before planning determination."),
    "geology": ("Geology context", "Review geological conditions and confirm whether technical assessment is required."),
    "seismic": ("Seismic context", "Review seismic hazard context and confirm applicable structural/technical requirements."),
    "groundwater": ("Groundwater context", "Review groundwater sensitivity and confirm applicable technical/environmental controls."),
    "quarry_mining": ("Mining/quarry context", "Review proximity and operational constraints associated with mines or quarries."),
    "ecology": ("Ecological sensitivity", "Review ecological connectivity/sensitivity and prioritise avoidance or mitigation where applicable."),
    "water_quality": ("Water quality context", "Review water-quality sensitivity and confirm applicable discharge/environmental controls."),
    "river_reserve": ("River/drainage context", "Confirm river reserve/drainage constraints and required technical-agency review."),
}


def build_environment_implications(environment: dict[str, Any] | None = None) -> dict[str, Any]:
    environment = environment or {}
    items: list[dict[str, Any]] = []
    for metric in environment.get("metrics", []) or []:
        if not isinstance(metric, dict):
            continue
        domain = str(metric.get("id", ""))
        if domain not in IMPLICATIONS:
            continue
        risk = metric.get("risk_flag") is True
        screened = metric.get("value") is not None and metric.get("status") != "REVIEW_REQUIRED"
        if not risk and not screened:
            continue
        label, action = IMPLICATIONS[domain]
        items.append({
            "domain": domain,
            "issue": label,
            "action": action if risk else "Confirm current authoritative evidence and technical thresholds before relying on this context.",
            "risk_flag": risk,
            "evidence": metric.get("evidence", "UNVERIFIED"),
            "source": metric.get("source"),
            "status": "PLANNER_REVIEW",
            "decision_use": "SCREENING_ONLY",
        })
    gaps = []
    if not items:
        gaps.append("ENVIRONMENT_NO_TRACEABLE_PLANNING_IMPLICATION")
    return {
        "version": "MASTER-233",
        "implications": items,
        "count": len(items),
        "flagged_count": sum(item["risk_flag"] for item in items),
        "review_gaps": gaps,
        "trace": "ENVIRONMENT/EVIDENCE → RISK → PLANNING IMPLICATION → PLANNER REVIEW",
        "decision_boundary": "ENVIRONMENTAL_PLANNING_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
    }
