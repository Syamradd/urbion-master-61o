from fastapi.testclient import TestClient

from urbion_gateway import app


client = TestClient(app)


def test_gemini_status_is_advisory_only(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.get("/gemini/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "Google Gemini"
    assert payload["role"] == "RED_TEAM_ADVISORY"
    assert payload["decision_authority"] == "NONE"
    assert payload["configured"] is False


def test_gemini_endpoint_fails_open_when_unconfigured(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.post("/gemini/red-team", json={"final_status": "CONDITIONAL RISK"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "NOT_CONFIGURED"
    assert payload["decision_authority"] == "NONE"
