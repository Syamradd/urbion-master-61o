"""Evidence-aware compliance decision helpers.

The helper consumes retrieved rule records and supplied proposal evidence. It
never upgrades SOURCE_CONTEXT/UNVERIFIED evidence into statutory verification.
"""
from __future__ import annotations

from typing import Any

_DECISIVE_STATES = {"VERIFIED", "USER_PROVIDED", "CALCULATED"}


def evaluate_rule_evidence(rule: dict[str, Any], proposal_value: Any = None) -> dict[str, Any]:
    """Classify one candidate rule without pretending it is statutory approval."""
    evidence = str(rule.get("evidence_classification") or "UNVERIFIED")
    applicability = str(rule.get("applicability") or "UNKNOWN")
    result: dict[str, Any] = {
        "rule_id": rule.get("rule_id"),
        "parameter": rule.get("parameter"),
        "requirement": rule.get("requirement"),
        "source_document": rule.get("source_document"),
        "source_section": rule.get("source_section"),
        "evidence_classification": evidence,
        "applicability": applicability,
        "decision": "REVIEW_REQUIRED",
        "reason": "Rule evidence is not sufficient for an automated statutory determination.",
    }
    if evidence == "RULE_ESTABLISHED" and applicability in {"DEVELOPMENT_TYPE_MATCH", "TYPOLOGY_DEPENDENT"}:
        result["decision"] = "CANDIDATE_RULE"
        result["reason"] = "Rule is established in the loaded rule database and matches the retrieved typology; planner verification remains required."
    elif evidence == "RULE_ESTABLISHED" and applicability in {"SPATIAL_DEPENDENT", "TOD_SPATIAL_DEPENDENT"}:
        result["decision"] = "SPATIAL_VERIFICATION_REQUIRED"
        result["reason"] = "Rule is spatially dependent; the relevant precinct, planning block or TOD position must be verified."
    if proposal_value is not None:
        result["proposal_value"] = proposal_value
    return result


def build_justification(rule: dict[str, Any], proposal_value: Any = None, spatial_evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a traceable planner-facing WHY record."""
    assessment = evaluate_rule_evidence(rule, proposal_value)
    gaps: list[str] = []
    if assessment["decision"] == "SPATIAL_VERIFICATION_REQUIRED":
        gaps.append("Verify the rule's spatial condition against the authoritative planning source.")
    if not spatial_evidence:
        gaps.append("No site-specific spatial verification was supplied to this justification.")
    return {
        "why": assessment["reason"],
        "rule": {
            "rule_id": rule.get("rule_id"),
            "parameter": rule.get("parameter"),
            "requirement": rule.get("requirement"),
            "source_document": rule.get("source_document"),
            "source_section": rule.get("source_section"),
        },
        "evidence": {
            "classification": rule.get("evidence_classification", "UNVERIFIED"),
            "spatial": spatial_evidence or None,
        },
        "gaps": gaps,
        "statutory_status": "NOT_CLAIMED",
        "planner_action": "VERIFY BEFORE STATUTORY DECISION",
    }
