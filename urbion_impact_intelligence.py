"""Evidence-bounded impact intelligence for planning review."""

DOMAINS = ("social", "environment", "mobility", "economic")


def _add_signal(signals, domain, signal, evidence_state, value=None, status="REVIEW_REQUIRED", source=None):
    item = {"domain": domain, "signal": signal, "evidence_state": evidence_state, "status": status}
    if value is not None:
        item["value"] = value
    if source:
        item["source"] = source
    signals.append(item)


def _environment_layer_summary(environmental_context):
    """Convert explicit layer query states into conservative impact signals."""
    layers = environmental_context.get("layers") if isinstance(environmental_context, dict) else None
    if not isinstance(layers, dict) or not layers:
        return [], ["Environmental layer evidence was not supplied; environmental impact remains unverified."]

    signals = []
    gaps = []
    for key, layer in layers.items():
        if not isinstance(layer, dict):
            continue
        status = str(layer.get("status") or "UNKNOWN")
        count = layer.get("feature_count")
        source = layer.get("provider") or environmental_context.get("provider") or "PLANMalaysia"
        if status == "LIVE_QUERY":
            _add_signal(signals, "environment", f"{key}_source_context", "SOURCE_CONTEXT", count if count is not None else 0, "REVIEW_REQUIRED", source)
            if key in {"flood", "slope", "geohazard", "seismic", "coastal_erosion", "fault", "ksas", "ecology", "protected_area"}:
                _add_signal(signals, "environment", f"{key}_constraint_screening", "SOURCE_CONTEXT", count if count is not None else 0, "REVIEW_REQUIRED", source)
        elif status == "NO_FEATURE":
            _add_signal(signals, "environment", f"{key}_screened_no_feature", "SOURCE_CONTEXT", 0, "REVIEW_REQUIRED", source)
        else:
            _add_signal(signals, "environment", f"{key}_query_gap", "UNVERIFIED", status, "REVIEW_REQUIRED", source)
            gaps.append(f"Environmental layer {key} could not be established as a usable query result.")
    gaps.append("Environmental layer results are screening evidence only; confirm currency, geometry, thresholds and agency requirements.")
    return signals, gaps


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
        elif sid == "catchment_coverage":
            _add_signal(signals, "mobility", "geometric_catchment_context", "CALCULATED", signal.get("value"), "READY_FOR_REVIEW")
        elif sid == "constraint_flags" and signal.get("value", 0):
            _add_signal(signals, "environment", "user_constraint_flag", "USER_PROVIDED", signal.get("value"), "REVIEW_REQUIRED")
            review_gaps.append("User-provided spatial constraints require authoritative verification before impact conclusions.")
        elif str(sid).startswith("environment_"):
            _add_signal(signals, "environment", signal.get("id"), signal.get("evidence", "UNVERIFIED"), signal.get("value"), "REVIEW_REQUIRED")

    env_signals, env_gaps = _environment_layer_summary(environmental_context)
    signals.extend(env_signals)
    review_gaps.extend(env_gaps)

    if spatial.get("catchments", {}).get("features") and not any(s.get("signal") == "geometric_catchment_context" for s in signals):
        _add_signal(signals, "mobility", "geometric_catchment_context", "CALCULATED", len(spatial["catchments"]["features"]), "READY_FOR_REVIEW")

    if assessment:
        _add_signal(signals, "social", "development_assessment_context", "CALCULATED", status="REVIEW_REQUIRED")
        _add_signal(signals, "economic", "development_assessment_context", "CALCULATED", status="REVIEW_REQUIRED")

    source_context_present = any(s["evidence_state"] == "SOURCE_CONTEXT" for s in signals)
    calculated_present = any(s["evidence_state"] == "CALCULATED" for s in signals)
    user_provided_present = any(s["evidence_state"] == "USER_PROVIDED" for s in signals)
    evidence_state = "SOURCE_CONTEXT" if source_context_present else ("CALCULATED" if calculated_present else ("USER_PROVIDED" if user_provided_present else "UNVERIFIED"))

    environment_signals = [s for s in signals if s.get("domain") == "environment"]
    environment_hits = sum(1 for s in environment_signals if s.get("evidence_state") == "SOURCE_CONTEXT" and s.get("status") == "REVIEW_REQUIRED" and isinstance(s.get("value"), (int, float)) and s.get("value") > 0)
    environment_gaps = sum(1 for s in environment_signals if s.get("evidence_state") == "UNVERIFIED")
    mobility_ready = any(s.get("signal") in {"tod_access_screening", "geometric_catchment_context"} and s.get("evidence_state") == "CALCULATED" for s in signals)

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
            "mobility": "READY_FOR_REVIEW" if mobility_ready else "UNVERIFIED",
            "economic": "REVIEW_REQUIRED",
        },
        "environmental_summary": {
            "layer_signal_count": len(environment_signals),
            "source_context_hits": environment_hits,
            "unverified_layers": environment_gaps,
            "interpretation": "Source-context hits indicate screening relevance only; they do not establish statutory constraint, clearance or safety.",
        },
        "authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "guardrail": "Impact intelligence supports planner review; it does not issue statutory approval or replace required impact studies.",
    }
