"""Source/provenance contract for URBION planning rules.

This layer records what URBION can safely claim about a rule. It does not
upgrade a rule to statutory verification. Missing page/clause/amendment
metadata deliberately remains REQUIRES_REVIEW.
"""
from __future__ import annotations

from typing import Any

RULE_SOURCE_DEFAULT = {
    "jurisdiction": "Majlis Bandaraya Melaka Bersejarah",
    "document": "RT MBMB 2035 Jilid I",
    "document_family": "Rancangan Tempatan MBMB 2035",
    "version_status": "CURRENT_PLAN_REFERENCE",
    "adopted_amendment_status": "PENGUBAHAN_5_LISTED_BY_OFFICIAL_PORTAL",
    "latest_official_amendment_check": "2026-09-14",
    "latest_official_notice": "https://www.mbmb.gov.my/en/mbmb/media-centre/news/mesyuarat-majlis-penuh-mbmb-terima-taklimat-draf-blueprint-sm-wez-2-0-rt-mbmb-2035",
    "latest_official_notice_status": "PENGUBAHAN_6_PRESENTED_AS_DRAFT",
    "latest_draft_note": "MBMB reported a briefing on the Draft RT MBMB 2035 (Pengubahan 6) on 30 April 2026; do not treat it as adopted statutory text.",
    "source_status": "PRIMARY_REFERENCE_PARTIAL",
    "verification_status": "REQUIRES_REVIEW",
    "citation_locator": None,
    "page": None,
    "clause": None,
    "table": None,
}


def enrich_rule_provenance(rule: dict[str, Any]) -> dict[str, Any]:
    """Return a rule with explicit source-status fields."""
    out = dict(rule)
    provenance = {**RULE_SOURCE_DEFAULT}
    provenance.update(rule.get("provenance") or {})
    # A rule with no page/table/clause citation must not be presented as
    # fully traceable, even when the source document family is known.
    if not any(provenance.get(k) for k in ("page", "clause", "table", "citation_locator")):
        provenance["verification_status"] = "REQUIRES_REVIEW"
        provenance["source_status"] = "PRIMARY_REFERENCE_PARTIAL"
    out["provenance"] = provenance
    out["source_status"] = provenance["source_status"]
    out["verification_status"] = provenance["verification_status"]
    return out


def audit_rule_set(rules: list[dict[str, Any]]) -> dict[str, Any]:
    """Audit rule provenance without changing deterministic rule values."""
    audited = []
    for rule in rules:
        item = enrich_rule_provenance(rule)
        p = item["provenance"]
        audited.append(
            {
                "rule_id": item.get("rule_id"),
                "document": p["document"],
                "version_status": p["version_status"],
                "adopted_amendment_status": p["adopted_amendment_status"],
                "latest_official_amendment_check": p["latest_official_amendment_check"],
                "latest_official_notice_status": p["latest_official_notice_status"],
                "page": p["page"],
                "clause": p["clause"],
                "table": p["table"],
                "source_status": p["source_status"],
                "verification_status": p["verification_status"],
            }
        )
    return {
        "audit_version": "P0.2.2",
        "jurisdiction": RULE_SOURCE_DEFAULT["jurisdiction"],
        "rules": audited,
        "statutory_verification": "NOT_CLAIMED",
        "decision_boundary": "RULE_PROVENANCE_AUDIT",
    }
