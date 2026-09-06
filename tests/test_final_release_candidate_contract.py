from fastapi.testclient import TestClient

from championship_server import app


INPUTS = {
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


def test_integrated_release_candidate_contract():
    client = TestClient(app)
    payload = {
        "assessment_inputs": INPUTS,
        "variants": [
            {"id": "LOW", "name": "Lower density", "overrides": {"plot_ratio": 4.0}},
            {"id": "HIGH", "name": "Higher density", "overrides": {"plot_ratio": 5.0}},
        ],
    }
    response = client.post("/copilot/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "BOUNDED_PLANNER_COPILOT"
    assert body["evidence_ledger"]["total_items"] >= 1
    assert 0 <= body["evidence_quality"]["score"] <= 100
    assert body["decision"]["statutory_verification"] == "NOT_CLAIMED"
    assert body["scenario_intelligence"]["count"] == 2

    explain = client.post("/copilot/explain", json={"assessment_inputs": INPUTS})
    assert explain.status_code == 200
    explain_body = explain.json()
    assert explain_body["decision_authority"] == "NONE"
    assert explain_body["statutory_verification"] == "NOT_CLAIMED"
    assert explain_body["generation_boundary"].startswith("LLM_NARRATIVE_ONLY")

    handoff = client.post("/planner/handoff", json={"assessment_inputs": INPUTS})
    assert handoff.status_code == 200
    assert handoff.json()["guardrails"]["decision_authority"] == "NONE"

    judge = client.post("/judge/demo", json={"assessment_inputs": INPUTS})
    assert judge.status_code == 200
    assert judge.json()["guardrails"]["statutory_verification"] == "NOT_CLAIMED"


def test_championship_assets_remain_reachable():
    client = TestClient(app)
    for asset in (
        "urbion_championship_workstation_v2.js",
        "urbion_decision_intelligence_ui.js",
        "urbion_championship_workflow.js",
        "urbion_championship_decision_chain.js",
    ):
        response = client.get("/" + asset)
        assert response.status_code == 200
