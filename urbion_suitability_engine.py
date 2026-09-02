"""Evidence-weighted site suitability for URBION planning pre-assessment."""
from __future__ import annotations
from typing import Any


def score_suitability(*, planning_fit: float, transit_access: float, data_confidence: float, site_completeness: float, environment_evidence: float) -> dict[str, Any]:
    values = {"planning_fit": planning_fit, "transit_access": transit_access, "data_confidence": data_confidence, "site_completeness": site_completeness, "environment_evidence": environment_evidence}
    values = {k: max(0.0, min(100.0, float(v))) for k, v in values.items()}
    score = round(values["planning_fit"]*.30 + values["transit_access"]*.25 + values["data_confidence"]*.20 + values["site_completeness"]*.10 + values["environment_evidence"]*.15, 1)
    band = "HIGH POTENTIAL" if score >= 80 else "MODERATE" if score >= 65 else "REQUIRES FURTHER STUDY"
    return {"score": score, "band": band, "indicators": values, "decision_type": "PRELIMINARY_PLANNING_SUPPORT", "note": "Suitability is decision support, not statutory planning approval."}
