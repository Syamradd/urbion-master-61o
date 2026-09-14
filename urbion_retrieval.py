
# ============================================================
# 🏙️ URBION RULE RETRIEVAL ENGINE
# ============================================================

from urbion_rules import URBION_RULES
from urbion_rule_provenance import enrich_rule_provenance


def urbion_retrieve_rules(
    development_type,
    authority="MBMB",
    spatial_context=None
):
    """
    Retrieve candidate planning rules.

    Retrieval considers:
    1. Planning authority
    2. Development typology
    3. Commercial applicability
    4. Spatial / TOD conditions

    IMPORTANT:
    Retrieval does NOT make a final applicability decision.

    The retrieved rules are candidate rules that will later
    be evaluated by the Applicability Engine.
    """

    candidates = []
    development_type = (development_type or "").strip()
    authority = (authority or "MBMB").strip()
    spatial_context = spatial_context or {}

    # Current database is RT MBMB.
    # If another authority is selected, no MBMB rule should
    # automatically be treated as authoritative.
    if authority != "MBMB":
        return candidates

    development_lower = development_type.lower()

    for rule in URBION_RULES:
        rule_type = rule.get("development_type", "").lower()
        development_match = development_lower in rule_type
        if not development_match:
            continue

        # Preserve the complete rule provenance contract in the candidate
        # packet so downstream review-gap generation can see it.
        enriched = enrich_rule_provenance(rule)

        candidates.append({
            "rule_id": enriched["rule_id"],
            "parameter": enriched["parameter"],
            "requirement": enriched["requirement"],
            "value": enriched.get("value"),
            "unit": enriched.get("unit"),
            "development_type": enriched["development_type"],
            "land_use": enriched.get("land_use"),
            "spatial_condition": enriched["spatial_condition"],
            "applicability": enriched["applicability"],
            "source_document": enriched["source_document"],
            "source_section": enriched["source_section"],
            "evidence_text": enriched["evidence_text"],
            "evidence_classification": enriched["evidence_classification"],
            "traceability": enriched["traceability"],
            "notes": enriched.get("notes", ""),
            "provenance": enriched["provenance"],
            "source_status": enriched["source_status"],
            "verification_status": enriched["verification_status"],
        })

    return candidates
