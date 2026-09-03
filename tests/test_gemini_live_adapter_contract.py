import json

from urbion_gemini_redteam import review_with_gemini


def test_gemini_configured_path_is_advisory_and_parses_json(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({
                "candidates": [{
                    "content": {
                        "parts": [{
                            "text": json.dumps({
                                "verdict": "REVIEW",
                                "risks": ["evidence gap"],
                                "evidence_gaps": ["planning source needs confirmation"],
                                "recommended_corrections": ["keep confidence bounded"],
                                "statutory_boundary": "NOT_APPROVAL",
                            })
                        }]
                    }
                }]
            }).encode("utf-8")

    def fake_urlopen(request, timeout=20.0):
        assert "key=test-key" in request.full_url
        assert timeout == 20.0
        return FakeResponse()

    monkeypatch.setattr("urbion_gemini_redteam.urllib.request.urlopen", fake_urlopen)
    result = review_with_gemini({
        "assessment": {"final_status": "CONDITIONAL RISK"},
        "api_key": "must-not-be-forwarded",
    })

    assert result["status"] == "LIVE"
    assert result["provider"] == "Google Gemini"
    assert result["model"] == "gemini-2.5-flash"
    assert result["role"] == "RED_TEAM_ADVISORY"
    assert result["decision_authority"] == "NONE"
    assert result["review"]["verdict"] == "REVIEW"
    assert result["review"]["statutory_boundary"] == "NOT_APPROVAL"
