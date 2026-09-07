from fastapi.testclient import TestClient

from championship_server import app

client = TestClient(app)


def test_what_if_accepts_a_baseline_without_tod_context():
    baseline = {
        "site_lat": 2.285,
        "site_lon": 102.196,
        "plot_ratio": 4.5,
        "development_type": "New Development",
        "development_class": "Mixed Use",
        "state": "Melaka",
        "district": "Melaka Tengah",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
        "lot_no": "",
    }
    payload = {
        "baseline": baseline,
        "variants": [
            {"id": "LOWER", "name": "Lower intensity", "overrides": {"plot_ratio": 3.5}},
        ],
    }
    response = client.post("/what-if", json=payload)
    assert response.status_code == 200, response.text
