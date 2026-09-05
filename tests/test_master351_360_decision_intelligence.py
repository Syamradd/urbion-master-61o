from fastapi.testclient import TestClient
from championship_server import app

BASE = {
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
}


def test_decision_intelligence_returns_explainable_evidence_and_priorities():
    client = TestClient(app)
    response = client.post("/intelligence/decision", json=BASE)
    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] == "DI-1"
    assert payload["decision_intelligence"]["decision_boundary"] == "DECISION_SUPPORT_ONLY"
    assert payload["decision_intelligence"]["evidence_breakdown"]["spatial_distance_calculated"] is True
    assert payload["decision_intelligence"]["evidence_breakdown"]["statutory_verification"] == "NOT_CLAIMED"
    assert isinstance(payload["sensitivity"]["dimensions"], list)


def test_decision_intelligence_batch_is_bounded_and_deterministic():
    client = TestClient(app)
    second = dict(BASE, plot_ratio=6.0)
    response = client.post("/intelligence/decision/batch", json=[BASE, second])
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert len(payload["results"]) == 2
    assert payload["statutory_verification"] == "NOT_CLAIMED"


def test_decision_intelligence_batch_rejects_empty_and_oversized_payloads():
    client = TestClient(app)
    assert client.post("/intelligence/decision/batch", json=[]).status_code == 422
    assert client.post("/intelligence/decision/batch", json=[BASE] * 13).status_code == 422
