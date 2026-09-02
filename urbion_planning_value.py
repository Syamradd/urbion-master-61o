"""Deterministic planning-readiness value layer for URBION.

This layer converts an existing assessment into actionable planning value.
It never invents statutory controls and never represents screening as approval.
"""
from __future__ import annotations
from typing import Any

SAFE_EVIDENCE = {"AVAILABLE", "VERIFIED", "REFERENCE_REGISTERED"}
GAP_EVIDENCE = {"PLANNED", "QUERY_UNAVAILABLE", "DISCOVERY_COMPLETE", "NO_EVIDENCE"}


def _unique(items: list[str]) -> list[str]:
    seen = set(); out = []
    for item in items:
        if item and item not in seen:
            seen.add(item); out.append(item)
    return out


def _rule_findings(compliance_results: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    findings=[]; blockers=[]; drivers=[]
    for result in compliance_results or []:
        status=str(result.get("status", "")).upper()
        rule_id=result.get("rule_id") or "Applicable control"
        reason=str(result.get("reason", "")).strip()
        if status == "NON-COMPLIANCE":
            blockers.append(f"{rule_id}: {reason or 'Control requirement is not satisfied.'}")
            drivers.append(str(rule_id))
        elif status == "COMPLY":
            findings.append(f"{rule_id}: compliant based on the current proposal evidence.")
            drivers.append(str(rule_id))
        elif status in {"REQUIRES REVIEW", "NOT_VERIFIED"}:
            findings.append(f"{rule_id}: verification is still required{': ' + reason if reason else '.'}")
            drivers.append(str(rule_id))
    return _unique(findings), _unique(blockers), _unique(drivers)


def _evidence_gaps(evidence_intelligence: dict[str, Any] | None) -> list[str]:
    gaps=[]
    for item in (evidence_intelligence or {}).get("items", []):
        status=str(item.get("status", "UNKNOWN")).upper()
        if status in GAP_EVIDENCE:
            source=item.get("source") or "Source"
            note=item.get("evidence") or "Additional evidence"
            gaps.append(f"{source} ({status}): {note}.")
    return _unique(gaps)


def build_planning_value(*, site: dict[str, Any], final_status: str,
                         policy_coverage: dict[str, Any], retrieved_rules: list[dict[str, Any]],
                         compliance_results: list[dict[str, Any]], site_analysis: dict[str, Any],
                         evidence_intelligence: dict[str, Any] | None = None) -> dict[str, Any]:
    status=str(final_status or "REQUIRES REVIEW").upper()
    recommendation=(site_analysis or {}).get("recommendation", {})
    readiness_score=float((site_analysis or {}).get("score", 0))
    findings, blockers, rule_drivers = _rule_findings(compliance_results)
    gaps=_evidence_gaps(evidence_intelligence)
    actions=[]; strengths=[]

    if status == "NON-COMPLIANCE":
        actions=["Identify the failed control(s) in the decision trace.",
                 "Revise the affected development parameter(s) in the proposal.",
                 "Re-run URBION assessment before progressing to planner review."]
        headline="Planning redesign required"
        value_band="BLOCKED"
    elif status == "COMPLY":
        actions=["Preserve the parameters that produced the compliant result.",
                 "Validate remaining site evidence with the planner / relevant authority process.",
                 "Re-run the assessment if any material proposal parameter changes."]
        headline="Planning-ready candidate for further review"
        value_band="READY FOR FURTHER REVIEW"
        strengths=["Applicable controls currently return COMPLY."]
    elif status == "NOT APPLICABLE":
        actions=["Recheck the development position against the selected planning pathway.",
                 "Consider an alternative development position or policy pathway.",
                 "Reassess after the planning position is clarified."]
        headline="Planning pathway needs reconsideration"
        value_band="REPOSITION"
    else:
        actions=["Resolve the outstanding applicability or evidence questions.",
                 "Confirm the relevant local planning controls with a planner.",
                 "Re-run URBION once verified evidence is available."]
        headline="Planner verification required"
        value_band="REVIEW"

    if policy_coverage.get("coverage") != "FULL_RULE_ENGINE":
        actions.insert(0, "Load or verify the applicable local planning policy before relying on a local-rule decision.")
        strengths.append("URBION keeps unverified local policy separate from decision evidence.")

    tod=site.get("tod_distance_m")
    if tod is not None and tod <= 400:
        strengths.append("Site is within the calculated 400 m TOD screening band.")
    elif tod is not None and tod <= 800:
        strengths.append("Site is within the calculated 800 m TOD screening band.")

    strengths=_unique(strengths)
    actions=_unique(actions)
    rationale=(recommendation.get("reason") or "Assessment outcome translated into planning actions.")
    if gaps:
        rationale += " Outstanding source gaps remain disclosed and should be resolved before treating the result as decision-grade evidence."

    return {
        "title":"Planning Value & Readiness",
        "version":"PHASE-C",
        "band":value_band,
        "score":readiness_score,
        "score_label":"Screening readiness score",
        "headline":headline,
        "status":status,
        "key_findings":findings,
        "blockers":blockers,
        "decision_drivers":_unique(rule_drivers + (["Policy coverage"] if policy_coverage else [])),
        "evidence_gaps":gaps,
        "strengths":strengths,
        "next_actions":actions,
        "rationale":rationale,
        "disclaimer":"Planning decision-support only; not statutory approval, certification or an authority decision."
    }
