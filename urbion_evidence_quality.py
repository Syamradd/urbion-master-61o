"""Deterministic evidence-quality scoring for URBION planner review.

This module scores evidence completeness/verification quality only. It never
changes planning scores, rankings, compliance outcomes, or statutory status.
"""
from __future__ import annotations
from typing import Any

STATE_WEIGHTS = {
    "VERIFIED": 1.0,
    "CALCULATED": 0.85,
    "SOURCE_CONTEXT": 0.60,
    "USER_PROVIDED": 0.40,
    "UNVERIFIED": 0.0,
}


def _items(ledger: dict[str, Any] | None) -> list[dict[str, Any]]:
    raw = (ledger or {}).get("items", [])
    return [item for item in raw if isinstance(item, dict)]


def build_evidence_quality(ledger: dict[str, Any] | None) -> dict[str, Any]:
    """Return bounded evidence quality metrics with explicit review flags."""
    items = _items(ledger)
    total = len(items)
    if not total:
        return {
            "version": "PHASE-E.9",
            "score": 0.0,
            "grade": "NO_EVIDENCE",
            "coverage": 0.0,
            "verified_ratio": 0.0,
            "review_required": True,
            "risk_flags": ["NO_EVIDENCE_ITEMS"],
            "by_domain": {},
            "decision_authority": "NONE",
            "statutory_verification": "NOT_CLAIMED",
        }

    weighted = 0.0
    verified = 0
    review = 0
    domains: dict[str, list[float]] = {}
    risk_flags: list[str] = []
    for item in items:
        state = str(item.get("evidence_state", "UNVERIFIED")).upper()
        weight = STATE_WEIGHTS.get(state, 0.0)
        weighted += weight
        if state == "VERIFIED":
            verified += 1
        if state in {"UNVERIFIED", "SOURCE_CONTEXT", "USER_PROVIDED"}:
            review += 1
        domain = str(item.get("domain", "other"))
        domains.setdefault(domain, []).append(weight)
        if state == "UNVERIFIED":
            risk_flags.append(f"UNVERIFIED:{item.get('id', 'UNKNOWN')}")

    score = round(weighted / total * 100, 1)
    grade = "HIGH" if score >= 80 else "MODERATE" if score >= 55 else "LOW"
    if verified == 0:
        risk_flags.append("NO_VERIFIED_EVIDENCE")
    return {
        "version": "PHASE-E.9",
        "score": score,
        "grade": grade,
        "coverage": round((total - review) / total, 3),
        "verified_ratio": round(verified / total, 3),
        "review_required": review > 0,
        "review_required_items": review,
        "total_items": total,
        "risk_flags": risk_flags[:20],
        "by_domain": {domain: round(sum(values) / len(values) * 100, 1) for domain, values in domains.items()},
        "decision_authority": "NONE",
        "statutory_verification": "NOT_CLAIMED",
    }
