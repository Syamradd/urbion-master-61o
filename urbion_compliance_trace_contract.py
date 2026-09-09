"""Deterministic compliance-trace output contract for URBION HORIZON."""
from __future__ import annotations

from typing import Any


STATUSES = {"COMPLY", "REVIEW", "NON-COMPLIANCE"}
CONFIDENCE = {"SUPPORTED", "GAP", "REVIEW"}


def compliance_trace(*, status: str, rule: str, requirement: str, why: str,
                     evidence: str, reference: str | None = None,
                     confidence: str = "REVIEW", planner_action: str = "") -> dict[str, Any]:
    """Build a traceable planning result; never imply statutory approval."""
    status = status.upper()
    confidence = confidence.upper()
    if status not in STATUSES:
        raise ValueError(f"unsupported compliance status: {status}")
    if confidence not in CONFIDENCE:
        raise ValueError(f"unsupported confidence: {confidence}")
    return {
        "status": status,
        "rule": rule,
        "requirement": requirement,
        "why": why,
        "evidence": evidence,
        "reference": reference,
        "confidence": confidence,
        "planner_action": planner_action,
        "statutory_approval_claim": False,
        "decision_safe": confidence == "SUPPORTED" and bool(evidence and reference),
    }
