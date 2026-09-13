from urbion_rules import URBION_RULES
from urbion_rule_provenance import audit_rule_set, enrich_rule_provenance

ALLOWED_SOURCE_STATUS = {"PRIMARY_REFERENCE_PARTIAL", "PRIMARY_REFERENCE_VERIFIED"}
ALLOWED_VERIFICATION = {"REQUIRES_REVIEW", "VERIFIED"}


def main() -> None:
    assert URBION_RULES, "Rule database must not be empty"
    audit = audit_rule_set(URBION_RULES)
    assert audit["statutory_verification"] == "NOT_CLAIMED"
    assert audit["decision_boundary"] == "RULE_PROVENANCE_AUDIT"
    assert len(audit["rules"]) == len(URBION_RULES)

    rule_ids = {r["rule_id"] for r in URBION_RULES}
    audit_ids = {r["rule_id"] for r in audit["rules"]}
    assert audit_ids == rule_ids

    for rule in URBION_RULES:
        item = enrich_rule_provenance(rule)
        provenance = item["provenance"]
        assert provenance["document"] == "RT MBMB 2035 Jilid I"
        assert provenance["adopted_amendment_status"] == "PENGUBAHAN_5_LISTED_BY_OFFICIAL_PORTAL"
        assert provenance["latest_draft_note"]
        assert provenance["source_status"] in ALLOWED_SOURCE_STATUS
        assert provenance["verification_status"] in ALLOWED_VERIFICATION
        # No exact locator means the rule must remain review-bound.
        if not any(provenance.get(k) for k in ("page", "clause", "table", "citation_locator")):
            assert provenance["verification_status"] == "REQUIRES_REVIEW"

    print({"status": "PASS", "rules_audited": len(URBION_RULES), "statutory_verification": audit["statutory_verification"]})


if __name__ == "__main__":
    main()
