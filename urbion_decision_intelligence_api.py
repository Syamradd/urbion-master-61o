"""Production decision-intelligence routes for URBION HORIZON."""
from __future__ import annotations
from fastapi import HTTPException
from server import app, AssessmentRequest, assess_core
from urbion_decision_intelligence import build_decision_intelligence, build_sensitivity_matrix
from urbion_canonical_evidence import build_canonical_evidence_packet

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

@app.post("/decision-center")
def decision_center(request: dict):
    """Compatibility adapter for the canonical workspace decision button.

    Accept both the canonical {"assessment": {...}} wrapper and a direct
    assessment object. Both paths execute the same deterministic engine and
    return the same canonical evidence contract; no approval authority is
    implied by this route.
    """
    raw = request.get("assessment") if isinstance(request, dict) and isinstance(request.get("assessment"), dict) else request if isinstance(request, dict) else None
    if not isinstance(raw, dict):
        raise HTTPException(status_code=422, detail="assessment object is required")
    try:
        assessment_request = AssessmentRequest.model_validate(raw)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Invalid assessment payload") from exc
    assessment = assess_core(assessment_request)
    di = build_decision_intelligence(assessment)
    packet = build_canonical_evidence_packet(
        assessment=assessment,
        spatial=assessment.get("site_analysis"),
        environment=assessment.get("live_environment_evidence") or assessment.get("evidence_intelligence"),
        stations=assessment.get("live_station_evidence") or assessment.get("stations"),
        development_impact=assessment.get("development_impact"),
        policy_graph={"policy_coverage": assessment.get("policy_coverage")},
    )
    actions = di.get("priority_actions") or assessment.get("review_gaps") or [
        "Verify adopted plan and authority requirements"
    ]
    return {
        "status": assessment.get("final_status", "REQUIRES REVIEW"),
        "recommendation": assessment.get("final_status", "REQUIRES REVIEW"),
        "rationale": di.get("rationale") or di.get("summary") or "Decision support generated from the deterministic assessment packet.",
        "next_actions": actions,
        "assessment": assessment,
        "decision_intelligence": di,
        "canonical_evidence_packet": packet,
        "review_gaps": list(packet.get("review_gaps", [])),
        "review_required": bool(packet.get("review_gaps")),
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
