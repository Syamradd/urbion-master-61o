from urbion_gemini_redteam import build_redteam_prompt, review_with_gemini


def test_gemini_adapter_is_advisory_and_bounded(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = review_with_gemini({"final_status": "CONDITIONAL RISK", "evidence_state": "CALCULATED"})
    assert result["status"] == "NOT_CONFIGURED"
    assert result["decision_authority"] == "NONE"
    prompt = build_redteam_prompt({"final_status": "COMPLY", "api_key": "should-not-leak"})
    assert "should-not-leak" not in prompt
    assert "must never approve development" in prompt
    assert "SOURCE_CONTEXT" in prompt
    assert "VERIFIED" in prompt


def test_gemini_model_has_safe_default(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    result = review_with_gemini({})
    assert result["provider"] == "Google Gemini"
    assert result["role"] == "RED_TEAM_ADVISORY"
