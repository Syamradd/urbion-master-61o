from urbion_evidence_ledger import build_evidence_ledger


def test_evidence_ledger_keeps_source_context_unverified():
    ledger = build_evidence_ledger(
        assessment={"evidence_state": {"site_coordinates": "SOURCE_CONTEXT"}},
        spatial={"evidence_model": {"flood": "SOURCE_CONTEXT"}},
        knowledge={"retrieval_count": 1, "evidence_state": "SOURCE_CONTEXT"},
    )
    states = {item["id"]: item["evidence_state"] for item in ledger["items"]}
    assert states["SITE-COORD"] == "SOURCE_CONTEXT"
    assert states["SPATIAL-FLOOD"] == "SOURCE_CONTEXT"
    assert ledger["statutory_verification"] == "NOT_CLAIMED"
    assert ledger["decision_authority"] == "NONE"
    assert "no statutory verification is inferred" in ledger["verification_boundary"]


def test_evidence_ledger_counts_review_required_states():
    ledger = build_evidence_ledger()
    assert ledger["total_items"] == len(ledger["items"])
    assert ledger["review_required_items"] >= ledger["counts"]["UNVERIFIED"]
