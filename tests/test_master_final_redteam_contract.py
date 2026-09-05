from pathlib import Path

from fastapi.testclient import TestClient

from championship_server import app


def _inputs():
    return {
        "site_lat": 2.285,
        "site_lon": 102.196,
        "tod_lat": 2.286,
        "tod_lon": 102.197,
        "plot_ratio": 4.5,
        "development_type": "TOD Development / Mixed Use",
        "development_class": "Mixed Use",
        "state": "Melaka",
        "district": "Melaka Tengah",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
        "lot_no": "REDTEAM-01",
    }


def test_final_redteam_rejects_non_finite_coordinates():
    client = TestClient(app)
    payload = _inputs() | {"site_lat": "NaN"}
    response = client.post("/assess", json=payload)
    assert response.status_code == 422


def test_final_redteam_rejects_placeholder_coordinates():
    client = TestClient(app)
    payload = _inputs() | {"site_lat": -90, "site_lon": -180}
    response = client.post("/assess", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_SPATIAL_INPUT"


def test_final_redteam_copilot_stays_bounded():
    client = TestClient(app)
    response = client.post("/copilot/run", json=_inputs())
    assert response.status_code == 200
    body = response.json()
    assert body["decision_authority"] == "NONE"
    assert body["statutory_verification"] == "NOT_CLAIMED"
    assert body["mode"] == "BOUNDED_PLANNER_COPILOT"
    assert body["evidence_ledger"]["verification_boundary"]


def test_final_redteam_validation_cases_are_real_production_paths():
    client = TestClient(app)
    cases = client.get("/validation/cases")
    assert cases.status_code == 200
    ids = [case["id"] for case in cases.json()["cases"]]
    assert ids == ["TC-01", "TC-02", "TC-03"]
    for case_id in ids:
        response = client.post(f"/validation/run/{case_id}")
        assert response.status_code == 200
        assert response.json()["evidence_card"]


def test_final_redteam_frontend_does_not_overwrite_fetch():
    text = Path("urbion_championship_input_sync.js").read_text(encoding="utf-8")
    assert "window.fetch=" not in text
    assert "payloadKey=payload=>JSON.stringify(payload)" in text


# Final-release retarget trigger: rerun this isolated red-team suite against current main.
