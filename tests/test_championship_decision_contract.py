from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_decision_center_exposes_evidence_boundary():
    payload = {
        "site_lat": 2.3,
        "site_lon": 102.2,
        "tod_lat": 2.302,
        "tod_lon": 102.202,
        "development_type": "TOD Development / Mixed Use",
        "development_class": "Mixed Use",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
        "state": "Melaka",
    }
    response = client.post("/decision-center", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "PHASE-E.7"
    assert "evidence_state" in body
    assert body["statutory_verification"] == "NOT_CLAIMED"
    assert "decision_trace" in body


def test_judge_mode_exposes_deterministic_boundary():
    response = client.get("/judge-mode")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "PHASE-E.7"
    assert body["scenario_count"] >= 1
    assert "decision_boundary" in body
    assert "statutory approval" in body["decision_boundary"]
    assert all("evidence_state" in row for row in body["scoreboard"])
