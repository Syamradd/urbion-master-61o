"""Traceable planning-policy and SDG relationships for URBION.

This graph links explicit impact findings to policy references only when a
caller supplies the reference. It never invents clause numbers or statutory
applicability. Unresolved links remain REVIEW_REQUIRED.
"""
from __future__ import annotations
from typing import Any

POLICY_DOMAINS = ("physical", "social", "economic")

def _clean(value: Any) -> str | None:
    text = str(value).strip() if value is not None else ""
    return text or None

def build_policy_graph(*, impacts: dict[str, Any] | None = None, policy_links: list[dict[str, Any]] | None = None, national_links: list[dict[str, Any]] | None = None, sdg_links: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Build an evidence-aware impact → policy → SDG trace graph."""
    impacts = impacts or {}
    links = []
    gaps = []
    supplied = list(policy_links or []) + list(national_links or []) + list(sdg_links or [])
    for item in supplied:
        if not isinstance(item, dict):
            gaps.append("POLICY_LINK_INVALID")
            continue
        domain = _clean(item.get("domain"))
        reference = _clean(item.get("reference"))
        if not domain or not reference:
            gaps.append("POLICY_REFERENCE_REQUIRED")
            continue
        links.append({
            "id": _clean(item.get("id")) or f"link-{len(links)+1}",
            "domain": domain,
            "impact": _clean(item.get("impact")),
            "issue": _clean(item.get("issue")),
            "level": _clean(item.get("level")) or "LOCAL",
            "reference": reference,
            "title": _clean(item.get("title")),
            "clause": _clean(item.get("clause")),
            "strategy": _clean(item.get("strategy")),
            "sdg": _clean(item.get("sdg")),
            "evidence": _clean(item.get("evidence")) or "SOURCE_CONTEXT",
            "status": _clean(item.get("status")) or "REVIEW_REQUIRED",
        })
    present_domains = {x.get("domain") for x in links}
    for domain in POLICY_DOMAINS:
        if domain in impacts and impacts.get(domain) and domain not in present_domains:
            gaps.append(f"{domain}:POLICY_LINK_REQUIRED")
    return {
        "version": "MASTER-186",
        "nodes": {"impacts": impacts, "links": links},
        "edge_count": len(links),
        "linked_domains": sorted(present_domains),
        "review_gaps": list(dict.fromkeys(gaps)),
        "traceability": "IMPACT → ISSUE → POLICY_REFERENCE → STRATEGY → SDG → EVIDENCE",
        "decision_boundary": "PLANNING_POLICY_TRACE_ONLY",
        "statutory_verification": "NOT_CLAIMED",
    }
