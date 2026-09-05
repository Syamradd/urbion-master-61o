"""Evidence-bounded impact intelligence for planning review."""

DOMAINS = ("social", "environment", "mobility", "economic")


def build_impact_intelligence(spatial=None, assessment=None, evidence=None):
    spatial = spatial or {}
    assessment = assessment or {}
    evidence = evidence or {}
    signals = []
    for key in ("flood", "slope", "geohazard", "ecology", "environment"):
        value = spatial.get(key)
        if value not in (None, {}, [], ""):
            signals.append({"domain": "environment", "signal": key, "evidence_state": "SOURCE_CONTEXT"})
    if spatial.get("nearest_features"):
        signals.append({"domain": "mobility", "signal": "proximity_context", "evidence_state": "CALCULATED"})
    if assessment:
        signals.append({"domain": "social", "signal": "development_assessment_context", "evidence_state": "CALCULATED"})
        signals.append({"domain": "economic", "signal": "development_assessment_context", "evidence_state": "CALCULATED"})
    return {
        "status": "REVIEW_REQUIRED" if signals or not evidence else "READY_FOR_REVIEW",
        "domains": list(DOMAINS),
        "signals": signals,
        "evidence_state": "SOURCE_CONTEXT" if any(s["evidence_state"] == "SOURCE_CONTEXT" for s in signals) else ("CALCULATED" if signals else "UNVERIFIED"),
        "review_gaps": ["Impact-specific verified evidence is required before material impact conclusions."],
        "authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "guardrail": "Impact intelligence supports planner review; it does not issue statutory approval or replace required impact studies.",
    }
