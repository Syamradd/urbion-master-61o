import os

from fastapi.testclient import TestClient

from championship_server import app


PAYLOAD = {
    "site_lat": 2.285,
    "site_lon": 102.196,
    "tod_lat": 2.286,
    "tod_lon": 102.197,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
    "lot_no": "11213",
}


def test_llm_explanation_has_deterministic_boundary(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    client = TestClient(app)
    response = client.post("/copilot/explain", json={"assessment_inputs": PAYLOAD})
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "BOUNDED_PLANNER_COPILOT_LLM"
    assert body["explanation"]["status"] == "DISABLED_NO_API_KEY"
    assert body["explanation"]["deterministic_source"] is True
    assert body["decision_authority"] == "NONE"
    assert body["statutory_verification"] == "NOT_CLAIMED"
    assert body["generation_boundary"].startswith("LLM_NARRATIVE_ONLY")
    assert body["deterministic_packet"]["evidence_ledger"]["total_items"] >= 1


def test_llm_route_rejects_missing_site():
    client = TestClient(app)
    response = client.post("/copilot/explain", json={"assessment_inputs": {"plot_ratio": 2.0}})
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "SITE_INPUT_REQUIRED"
