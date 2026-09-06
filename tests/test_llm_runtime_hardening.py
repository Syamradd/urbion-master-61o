import json

import urbion_llm_provider as llm


def test_prompt_is_bounded_for_large_deterministic_packets():
    packet = {"assessment": {"x": "A" * 50000}, "evidence_ledger": {"total_items": 2}}
    prompt = llm._prompt(packet)
    assert len(prompt) <= llm.MAX_PROMPT_CHARS + 2000
    assert "CONTEXT_TRUNCATED_BY_URBION" in prompt


def test_gemini_response_is_bounded(monkeypatch):
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return json.dumps({"candidates": [{"content": {"parts": [{"text": "X" * 10000}]}}]}).encode()

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(llm, "urlopen", lambda *args, **kwargs: Response())
    result = llm.generate_planner_explanation({"assessment": {"final_status": "REQUIRES REVIEW"}})
    assert result["status"] == "GENERATED"
    assert len(result["text"]) <= llm.MAX_OUTPUT_CHARS + 1
    assert result["deterministic_source"] is False


def test_network_style_oserror_falls_back(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(llm, "urlopen", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("offline")))
    result = llm.generate_planner_explanation({"assessment": {"final_status": "REQUIRES REVIEW"}, "evidence_ledger": {"total_items": 1}})
    assert result["status"] == "FALLBACK"
    assert result["deterministic_source"] is True
    assert result["error_type"] == "OSError"
