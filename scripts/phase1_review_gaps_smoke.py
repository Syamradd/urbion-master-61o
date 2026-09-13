from urbion_rules import URBION_RULES
from urbion_rule_provenance import audit_rule_set
from urbion_canonical_evidence import build_canonical_evidence_packet


def main() -> None:
    audit = audit_rule_set(URBION_RULES)
    review_rules = [
        item["rule_id"]
        for item in audit["rules"]
        if item["verification_status"] == "REQUIRES_REVIEW"
    ]
    assert review_rules, "At least one currently unlocatable rule must remain review-bound"

    assessment = {
        "project": "URBION",
        "site": {"state": "Melaka", "district": "Melaka Tengah", "pbt": "Majlis Bandaraya Melaka Bersejarah"},
        "final_status": "REQUIRES REVIEW",
        "classification": "TOD 400m",
        "decision_confidence": {"level": "REVIEW"},
        "recommendation": {"status": "REQUIRES REVIEW"},
        "policy_coverage": {},
        "retrieved_rules": URBION_RULES,
        "applicability_results": [],
        "compliance_results": [],
        "evidence_state": {"planning_rules": "SOURCE_CONTEXT"},
        "source_registry": [],
        "decision_trace": [],
        "review_gaps": [],
        "planning_value": {},
    }
    packet = build_canonical_evidence_packet(assessment=assessment)
    assert "review_gaps" in packet
    assert packet["statutory_verification"] == "NOT_CLAIMED"
    assert len(packet["review_gaps"]) == len(review_rules)
    assert all(rule_id in gap for rule_id, gap in zip(review_rules, packet["review_gaps"]))
    assert all("exact page/clause/table locator" in gap.lower() for gap in packet["review_gaps"])

    print({"status": "PASS", "rules_requiring_review": len(review_rules), "packet_review_gaps": len(packet["review_gaps"])})


if __name__ == "__main__":
    main()
