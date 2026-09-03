from fastapi.testclient import TestClient

from urbion_gateway import app


client = TestClient(app)


PAYLOAD = {
    "site_lat": 2.2,
    "site_lon": 102.2,
    "tod_lat": 2.2,
    "tod_lon": 102.204,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
}


def test_gemini_assessment_bridge_fails_open_without_secret(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.post("/gemini/red-team-assessment", json=PAYLOAD)
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "NOT_CONFIGURED"
    assert result["role"] == "RED_TEAM_ADVISORY"
    assert result["decision_authority"] == "NONE"
