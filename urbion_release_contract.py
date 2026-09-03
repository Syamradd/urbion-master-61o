"""Championship contract audit for URBION integrated planning outputs.

This module is intentionally deterministic and side-effect free. It validates the
shape and disclosure boundaries of an integrated LCP result without deciding
statutory approval or inventing missing evidence.
"""
from __future__ import annotations
from typing import Any

REQUIRED_LCP_KEYS = (
    "version", "project", "site", "assessment", "spatial_intelligence",
    "station_intelligence", "development_impact", "policy_graph",
    "recommendations", "what_if", "decision_center", "km_readiness",
    "evidence_summary", "review_gaps", "trace", "decision_boundary",
    "statutory_verification",
)
REQUIRED_MANIFEST_KEYS = ("framework", "server", "health_endpoint", "assessment_endpoint", "frontend", "deployment_ready")
EVIDENCE_STATES = {"USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED"}
# Keep the legacy POLICY/SDG contract token while accepting the richer
# GUIDELINES/POLICY trace introduced by context intelligence.
REQUIRED_TRACE = ("SITE", "SPATIAL", "STATION", "IMPACT", "RECOMMENDATION", "WHAT-IF", "DECISION CENTER", "LCP/PLANNER REVIEW")


def audit_lcp_contract(result: dict[str, Any] | None) -> dict[str, Any]:
    result = result or {}
    failures: list[str] = []
    warnings: list[str] = []
    missing = [key for key in REQUIRED_LCP_KEYS if key not in result]
    if missing:
        failures.append("missing:" + ",".join(missing))
    if result.get("project") != "URBION HORIZON":
        failures.append("project:EXPECTED_URBION_HORIZON")
    if result.get("statutory_verification") != "NOT_CLAIMED":
        failures.append("statutory_verification:NOT_CLAIMED_REQUIRED")
    if result.get("decision_boundary") != "INTEGRATED_LCP_PLANNING_SUPPORT":
        failures.append("decision_boundary:INTEGRATED_LCP_PLANNING_SUPPORT_REQUIRED")

    trace = str(result.get("trace", ""))
    for token in REQUIRED_TRACE:
        if token not in trace:
            failures.append(f"trace:{token}")
    if "POLICY/SDG" not in trace and "GUIDELINES/POLICY" not in trace:
        failures.append("trace:POLICY/SDG")

    counts = (result.get("evidence_summary") or {}).get("counts", {})
    invalid_states = sorted(set(counts) - EVIDENCE_STATES)
    if invalid_states:
        failures.append("evidence_state:" + ",".join(invalid_states))

    what_if = result.get("what_if") or {}
    ranked = what_if.get("ranked_scenarios", []) if isinstance(what_if, dict) else []
    if len(ranked) > 12:
        failures.append("what_if:MAX_12_SCENARIOS")
    if what_if and what_if.get("status") == "NOT_PROVIDED":
        warnings.append("what_if:OPTIONAL_NOT_PROVIDED")

    gaps = result.get("review_gaps")
    if not isinstance(gaps, list):
        failures.append("review_gaps:LIST_REQUIRED")
    elif len(gaps) != int((result.get("evidence_summary") or {}).get("review_gap_count", len(gaps))):
        warnings.append("review_gap_count:OUT_OF_SYNC")

    return {
        "status": "PASS" if not failures else "FAIL",
        "version": result.get("version"),
        "failures": failures,
        "warnings": warnings,
        "required_keys": list(REQUIRED_LCP_KEYS),
        "statutory_verification": result.get("statutory_verification"),
        "decision_boundary": result.get("decision_boundary"),
    }


def audit_deployment_manifest(manifest: dict[str, Any] | None) -> dict[str, Any]:
    manifest = manifest or {}
    failures: list[str] = []
    missing = [key for key in REQUIRED_MANIFEST_KEYS if key not in manifest]
    if missing:
        failures.append("missing:" + ",".join(missing))
    if manifest.get("framework") != "FastAPI":
        failures.append("framework:FASTAPI_REQUIRED")
    if manifest.get("server") != "Uvicorn":
        failures.append("server:UVICORN_REQUIRED")
    if manifest.get("health_endpoint") != "/health":
        failures.append("health_endpoint:/health_REQUIRED")
    if manifest.get("assessment_endpoint") != "/assess":
        failures.append("assessment_endpoint:/assess_REQUIRED")
    if manifest.get("deployment_ready") is not True:
        failures.append("deployment_ready:TRUE_REQUIRED")
    return {"status": "PASS" if not failures else "FAIL", "failures": failures, "required_keys": list(REQUIRED_MANIFEST_KEYS)}


def build_championship_gate(*, lcp: dict[str, Any] | None = None, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    lcp_audit = audit_lcp_contract(lcp)
    deployment_audit = audit_deployment_manifest(manifest)
    failures = lcp_audit["failures"] + deployment_audit["failures"]
    return {
        "status": "PASS" if not failures else "FAIL",
        "release": "CHAMPIONSHIP",
        "lcp": lcp_audit,
        "deployment": deployment_audit,
        "failures": failures,
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
        "disclaimer": "Automated contract gate only; planner/PBT and authorised-agency verification remains required.",
    }
