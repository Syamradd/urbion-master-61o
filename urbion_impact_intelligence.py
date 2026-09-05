"""Evidence-bounded impact intelligence for planning review."""

DOMAINS = ("social", "environment", "mobility", "economic")


def _add_signal(signals, domain, signal, evidence_state, value=None, status="REVIEW_REQUIRED", source=None):
    item = {"domain": domain, "signal": signal, "evidence_state": evidence_state, "status": status}
    if value is not None:
        item["value"] = value
    if source:
        item["source"] = source
    signals.append(item)


def build_impact_intelligence(spatial=None, assessment=None, evidence=None, environmental_context=None):
    """Translate available spatial/context evidence into review signals.

    No environmental hit is treated as proof of safety, and missing context is
    surfaced as a gap rather than replaced with a guessed score.
    """
    spatial = spatial or {}
    assessment = assessment or {}
    evidence = evidence or {}
    environmental_context = environmental_context or spatial.get("environment") or {}
    signals = []
    review_gaps = []

    for signal in spatial.get("planning_signals") or []:
        sid = signal.get("id")
        if sid == "tod_access":
            _add_signal(signals, "mobility", "tod_access_screening", "CALCULATED", signal.get("value"), "READY_FOR_REVIEW")
            _add_signal(signals, "social", "accessibility_context", "CALCULATED", signal.get("classification"), "REVIEW_REQUIRED")
        elif sid == "constraint_flags" and signal.get("value", 0):
            _add_signal(signals, "environment", "user_constraint_flag", "USER_PROVIDED", signal.get("value"), "REVIEW_REQUIRED")
            review_gaps.append("User-provided spatial constraints require authoritative verification before impact conclusions.")

    layers = environmental_context.get("layers") if isinstance(environmental_context, dict) else None
    if isinstance(layers, dict) and layers:
        for key, layer in layers.items():
            if not isinstance(layer, dict):
                continue
            status = layer.get("status")
            if status == "LIVE_QUERY":
                _add_signal(signals, "environment", f"{key}_source_context", "SOURCE_CONTEXT", layer.get("feature_count", 0), "REVIEW_REQUIRED", "PLANMalaysia")
            elif status == "NO_FEATURE":
                _add_signal(signals, "environment", f"{key}_screened_no_feature", "SOURCE_CONTEXT", 0, "REVIEW_REQUIRED", "PLANMalaysia")
            else:
                _add_signal(signals, "environment", f"{key}_query_gap", "UNVERIFIED", status or "UNKNOWN", "REVIEW_REQUIRED", "PLANMalaysia")
        review_gaps.append("Environmental layer results are source context only; confirm currency, geometry, thresholds and agency requirements.")
    else:
        review_gaps.append("Environmental layer evidence was not supplied; environmental impact remains unverified.")
        for key in ("flood", "slope", "geohazard", "ecology"):
            _add_signal(signals, "environment", f"{key}_evidence_gap", "UNVERIFIED", status="REVIEW_REQUIRED")

    if spatial.get("catchments", {}).get("features"):
        _add_signal(signals, "mobility", "geometric_catchment_context", "CALCULATED", len(spatial["catchments"]["features"]), "READY_FOR_REVIEW")

    if assessment:
        _add_signal(signals, "social", "development_assessment_context", "CALCULATED", status="REVIEW_REQUIRED")
        _add_signal(signals, "economic", "development_assessment_context", "CALCULATED", status="REVIEW_REQUIRED")

    source_context_present = any(s["evidence_state"] == "SOURCE_CONTEXT" for s in signals)
    calculated_present = any(s["evidence_state"] == "CALCULATED" for s in signals)
    evidence_state = "SOURCE_CONTEXT" if source_context_present else ("CALCULATED" if calculated_present else "UNVERIFIED")
    return {
        "status": "REVIEW_REQUIRED",
        "domains": list(DOMAINS),
        "signals": signals,
        "signal_count": len(signals),
        "evidence_state": evidence_state,
        "review_gaps": list(dict.fromkeys(review_gaps)),
        "impact_readiness": {
            "social": "REVIEW_REQUIRED",
            "environment": "SOURCE_CONTEXT" if source_context_present else "UNVERIFIED",
            "mobility": "READY_FOR_REVIEW" if calculated_present else "UNVERIFIED",
            "economic": "REVIEW_REQUIRED",
        },
        "authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "guardrail": "Impact intelligence supports planner review; it does not issue statutory approval or replace required impact studies.",
    }
