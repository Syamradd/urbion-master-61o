"""Production decision-intelligence routes for URBION HORIZON."""
from __future__ import annotations
from fastapi import HTTPException
from server import app, AssessmentRequest, assess_core
from urbion_decision_intelligence import build_decision_intelligence, build_sensitivity_matrix

@app.post("/intelligence/decision")
def decision_intelligence(request: AssessmentRequest):
    assessment = assess_core(request)
    return {
        "project": "URBION HORIZON",
        "version": "DI-1",
        "assessment": assessment,
        "decision_intelligence": build_decision_intelligence(assessment),
        "sensitivity": build_sensitivity_matrix(assessment),
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
    }

@app.post("/intelligence/decision/batch")
def decision_intelligence_batch(requests: list[AssessmentRequest]):
    if not requests:
        raise HTTPException(status_code=422, detail="At least one assessment is required.")
    if len(requests) > 12:
        raise HTTPException(status_code=422, detail="At most 12 assessments may be compared in one batch.")
    results = []
    for item in requests:
        assessment = assess_core(item)
        di = build_decision_intelligence(assessment)
        results.append({
            "decision_status": assessment.get("final_status"),
            "confidence": di["confidence"],
            "priority_actions": di["priority_actions"],
            "classification": assessment.get("classification"),
            "tod_distance_m": assessment.get("tod_distance_m"),
        })
    return {
        "project": "URBION HORIZON",
        "version": "DI-1",
        "count": len(results),
        "results": results,
        "comparison_boundary": "DECISION_SUPPORT_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
