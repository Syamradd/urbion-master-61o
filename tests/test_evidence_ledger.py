from urbion_evidence_ledger import build_evidence_ledger


def test_evidence_ledger_is_explicit_and_conservative():
    ledger = build_evidence_ledger(
        assessment={
            "site": {"latitude": 2.3},
            "tod_distance_m": 250.0,
            "retrieved_rules": [{"rule_id": "R1"}],
            "final_status": "REQUIRES REVIEW",
            "evidence_state": {"site_coordinates": "USER_PROVIDED", "tod_distance": "CALCULATED", "planning_rules": "SOURCE_CONTEXT", "final_decision": "CALCULATED"},
        },
        knowledge={"retrieval_count": 1, "evidence_state": "SOURCE_CONTEXT"},
        impact={"signal_count": 2, "evidence_state": "SOURCE_CONTEXT"},
        scenarios={"count": 2},
        decision={"decision": {"status": "REQUIRES REVIEW"}},
    )
    assert ledger["total_items"] >= 8
    assert ledger["counts"]["SOURCE_CONTEXT"] >= 2
    assert ledger["decision_authority"] == "NONE"
    assert ledger["statutory_verification"] == "NOT_CLAIMED"
    assert "verification" in ledger["verification_boundary"].lower()
