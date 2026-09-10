from fastapi.testclient import TestClient

from championship_server import app


DEMO = {
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
    "lot_no": "",
    "building_height": None,
    "perimeter_planting": None,
    "landscaped_pedestrian_walkway": None,
    "shop_frontage_verified": False,
    "shop_office_verified": False,
}


def test_canonical_planning_chain_executes_end_to_end():
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    metadata = client.get("/metadata")
    assert metadata.status_code == 200
    assert metadata.json()["version"] == "PHASE-E.8"
    assert "Melaka" in metadata.json()["states"]

    iplan = client.get("/iplan/context", params={"site_lat": 2.285, "site_lon": 102.196, "state": "Melaka"})
    assert iplan.status_code == 200
    iplan_payload = iplan.json()
    assert iplan_payload["provider"] == "PLANMalaysia i-Plan"
    assert "current_land_use" in iplan_payload
    assert "environment" in iplan_payload

    assessment = client.post("/assess", json=DEMO)
    assert assessment.status_code == 200
    assessment_payload = assessment.json()
    assert assessment_payload["project"] == "URBION"
    assert assessment_payload["version"] == "PHASE-E.8"
    assert "final_status" in assessment_payload
    assert "recommendation" in assessment_payload
    assert "decision_trace" in assessment_payload
    assert assessment_payload["decision_trace"]
    assert assessment_payload["evidence_state"]["statutory_verification"] == "NOT_CLAIMED"

    what_if = client.post(
        "/what-if",
        json={
            "baseline": DEMO,
            "variants": [
                {
                    "id": "SELECTED",
                    "name": "Selected controlled scenario",
                    "overrides": {"plot_ratio": 5.0},
                }
            ],
        },
    )
    assert what_if.status_code == 200
    what_if_payload = what_if.json()
    assert "ranked_scenarios" in what_if_payload
    assert len(what_if_payload["ranked_scenarios"]) <= 12

    decision = client.post("/decision-center", json=DEMO)
    assert decision.status_code == 200
    decision_payload = decision.json()
    assert decision_payload

    lcp = client.get("/championship-gate")
    assert lcp.status_code == 200
    lcp_payload = lcp.json()
    assert lcp_payload
    assert lcp_payload.get("decision_authority") in (None, "NONE") or lcp_payload.get("statutory_verification") == "NOT_CLAIMED"


def test_canonical_workstation_contains_runtime_chain_and_no_legacy_popup_mount():
    client = TestClient(app)
    response = client.get("/championship.html")
    assert response.status_code == 200
    html = response.text
    assert 'release:"MASTER-331"' in html
    assert "/urbion_championship_command_shell.js" in html
    assert "/urbion_map_identify_runtime.js" in html
    assert "/urbion_championship_horizon_ui.js" in html
    assert 'id="urbion-championship-shell"' in html
    assert "MASTER-270 · CHAMPIONSHIP EXECUTION" not in html
    assert 'id="uhx"' not in html
    assert "#uhx" not in html
    for marker in ("Site + Development Inputs", "Planner Workstation", "Decision OS"):
        assert marker not in html


def test_critical_chain_assets_are_reachable_without_wildcard_fallback():
    client = TestClient(app)
    for asset in (
        "urbion_championship_final_command_center.js",
        "urbion_championship_final_command_center_hotfix.js",
        "urbion_championship_final_command_center_polish.js",
        "urbion_championship_final_command_center_policy.js",
        "urbion_championship_champion_review.js",
        "urbion_championship_final_runtime_enforcer.js",
    ):
        response = client.get(f"/{asset}")
        assert response.status_code == 200, asset
        assert response.headers["content-type"].startswith("application/javascript")
        assert response.text.strip(), asset
