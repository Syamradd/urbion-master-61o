from fastapi.testclient import TestClient
from server import app


def test_decision_center_endpoint_returns_championship_payload():
    client = TestClient(app)
    payload = {
        "site_lat": 2.3, "site_lon": 102.2,
        "tod_lat": 2.302, "tod_lon": 102.2,
        "plot_ratio": 4.5,
        "development_type": "TOD Development / Mixed Use",
        "development_class": "Mixed Use",
        "state": "Melaka", "district": "Melaka Tengah",
        "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "11213",
    }
    response = client.post("/decision-center", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "PHASE-E.8"
    assert body["decision"]["status"] == "COMPLY"
    assert body["map"]["type"] == "FeatureCollection"
    assert body["statutory_verification"] == "NOT_CLAIMED"
