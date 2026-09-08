from fastapi.testclient import TestClient

from championship_server import app


client = TestClient(app)


def _base_case():
    return {
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


def test_assess_accepts_missing_tod_and_keeps_transit_unverified():
    payload = _base_case()
    response = client.post("/assess", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["tod"]["latitude"] is None
    assert body["tod"]["longitude"] is None
    assert body["tod_distance_m"] is None
    transit = next(x for x in body["site_analysis"]["indicators"] if x["name"] == "Transit Access")
    assert transit["score"] is None
    assert transit["status"] == "UNVERIFIED"
    assert "Transit Access" in body["site_analysis"]["score_coverage"]["excluded_unverified"]


def test_assess_rejects_half_defined_tod():
    payload = _base_case() | {"tod_lat": 2.286}
    response = client.post("/assess", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INCOMPLETE_TOD_INPUT"


def test_assess_preserves_existing_tod_path():
    payload = _base_case() | {"tod_lat": 2.286, "tod_lon": 102.197}
    response = client.post("/assess", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["tod_distance_m"] is not None
    transit = next(x for x in body["site_analysis"]["indicators"] if x["name"] == "Transit Access")
    assert transit["score"] is not None
    assert transit["status"] == "CALCULATED"
