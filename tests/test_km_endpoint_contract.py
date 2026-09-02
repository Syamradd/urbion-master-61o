from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_km_readiness_ready_contract():
    response = client.post(
        "/km/readiness",
        params={
            "pbt": "Majlis Bandaraya Melaka Bersejarah",
            "development_type": "TOD Development / Mixed Use",
            "km_category": "SEDERHANA",
        },
        json={
            "documents": [
                "Location Plan",
                "Site Plan",
                "Development Proposal Report",
            ],
            "technical_reviews": {"JPS": "CLEAR"},
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["readiness"] == "READY_FOR_WORKFLOW_REVIEW"
    assert payload["km_category_state"] == "EXPLICIT"
    assert "statutory approval" in payload["decision_boundary"]


def test_km_readiness_missing_evidence_requires_review():
    response = client.post(
        "/km/readiness",
        params={
            "pbt": "MBMB",
            "development_type": "Mixed Use",
        },
        json={"documents": []},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["readiness"] == "REQUIRES_REVIEW"
    assert "Core submission evidence missing" in payload["blockers"]
    assert "KM category not explicitly classified" in payload["blockers"]
