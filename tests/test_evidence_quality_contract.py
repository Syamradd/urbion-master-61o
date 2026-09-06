from urbion_evidence_quality import build_evidence_quality


def test_evidence_quality_is_bounded_and_does_not_claim_authority():
    ledger = {
        "items": [
            {"id": "A", "domain": "site", "evidence_state": "VERIFIED"},
            {"id": "B", "domain": "spatial", "evidence_state": "CALCULATED"},
            {"id": "C", "domain": "policy", "evidence_state": "SOURCE_CONTEXT"},
            {"id": "D", "domain": "impact", "evidence_state": "UNVERIFIED"},
        ]
    }
    result = build_evidence_quality(ledger)
    assert 0 <= result["score"] <= 100
    assert result["grade"] == "MODERATE"
    assert result["review_required"] is True
    assert "UNVERIFIED:D" in result["risk_flags"]
    assert result["decision_authority"] == "NONE"
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_empty_evidence_is_explicitly_unsafe():
    result = build_evidence_quality({"items": []})
    assert result["grade"] == "NO_EVIDENCE"
    assert result["review_required"] is True
    assert result["risk_flags"] == ["NO_EVIDENCE_ITEMS"]
