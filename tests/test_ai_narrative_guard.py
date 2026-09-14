from urbion_llm_provider import _validate_generated_text, generate_planner_explanation


def test_ai_guard_accepts_bounded_sections():
    ok, reason = _validate_generated_text(
        "FINDING — Screening remains conditional. "
        "EVIDENCE — SOURCE_CONTEXT is available and some inputs remain unverified. "
        "ACTION — Continue planner review."
    )
    assert ok is True
    assert reason is None


def test_ai_guard_rejects_statutory_claims():
    ok, reason = _validate_generated_text(
        "FINDING — The proposal is fully compliant. "
        "EVIDENCE — Evidence reviewed. "
        "ACTION — Proceed."
    )
    assert ok is False
    assert reason == "forbidden_statutory_claim"


def test_ai_guard_requires_context_for_not_claimed():
    ok, reason = _validate_generated_text(
        "FINDING — Screening complete. "
        "EVIDENCE — NOT_CLAIMED. "
        "ACTION — Planner review."
    )
    assert ok is False
    assert reason == "uncontextualized_not_claimed"


def test_ai_fallback_is_deterministic_without_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = generate_planner_explanation(
        {
            "assessment": {"final_status": "REQUIRES REVIEW", "site_analysis": {"band": "REQUIRES FURTHER STUDY"}},
            "evidence_ledger": {"total_items": 2, "review_required_items": 1},
        }
    )
    assert result["deterministic_source"] is True
    assert result["validation"] == "FALLBACK_SAFE"
    assert "FINDING" in result["text"]
    assert "EVIDENCE" in result["text"]
    assert "ACTION" in result["text"]
