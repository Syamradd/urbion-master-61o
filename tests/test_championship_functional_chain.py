from fastapi.testclient import TestClient

from landing_server import app


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
    assert assessment_payload["canonical_evidence_packet"]["version"] == "PHASE1.2"

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
    assert what_if_payload["canonical_evidence_packet"]["version"] == "PHASE1.2"

    decision = client.post("/decision-center", json={"assessment": DEMO})
    assert decision.status_code == 200
    decision_payload = decision.json()
    assert decision_payload["canonical_evidence_packet"]["version"] == "PHASE1.2"
    assert decision_payload["decision_os"]["decision_authority"] == "NONE"

    gate = client.get("/championship-gate")
    assert gate.status_code == 200
    gate_payload = gate.json()
    assert gate_payload


def test_canonical_workstation_contains_runtime_chain_and_no_legacy_popup_mount():
    client = TestClient(app)
    response = client.get("/workspace")
    assert response.status_code == 200
    html = response.text
    assert '<title>URBION HORIZON — Planning Workspace</title>' in html
    assert 'X-URBION-UI' not in html
    for asset in (
        "/urbion_workspace_bridge.js",
        "/urbion_workspace_runtime.js",
        "/urbion_layer_runtime_fix.js",
        "/urbion_workspace_canonical_ui.js",
        "/urbion_workspace_modal_owner.js",
        "/urbion_workspace_pbt_catalog.js",
        "/urbion_workspace_utility_owner.js",
        "/urbion_workspace_review_gaps_owner.js",
        "/urbion_workspace_environment_owner.js",
        "/urbion_workspace_mobility_owner.js",
        "/urbion_workspace_development_impact_owner_v4.js",
        "/urbion_workspace_ratio_owner.js",
        "/urbion_workspace_road_intelligence_owner.js",
        "/urbion_workspace_analysis_summary_owner.js",
        "/urbion_workspace_station_map_owner.js",
    ):
        assert asset in html
    for marker in (
        "workspace_v2.html",
        "workspace_v3.html",
        "workspace_v4.html",
        "MASTER-270 · CHAMPIONSHIP EXECUTION",
        'id="uhx"',
        "Site + Development Inputs",
        "Planner Workstation",
    ):
        assert marker not in html


def test_critical_canonical_assets_are_reachable_without_legacy_fallback():
    client = TestClient(app)
    for asset in (
        "urbion_workspace_bridge.js",
        "urbion_workspace_runtime.js",
        "urbion_layer_runtime_fix.js",
        "urbion_workspace_canonical_ui.js",
        "urbion_workspace_modal_owner.js",
        "urbion_workspace_pbt_catalog.js",
        "urbion_workspace_utility_owner.js",
        "urbion_workspace_review_gaps_owner.js",
        "urbion_workspace_environment_owner.js",
        "urbion_workspace_mobility_owner.js",
        "urbion_workspace_development_impact_owner_v4.js",
        "urbion_workspace_ratio_owner.js",
        "urbion_workspace_road_intelligence_owner.js",
        "urbion_workspace_analysis_summary_owner.js",
        "urbion_workspace_station_map_owner.js",
    ):
        response = client.get(f"/{asset}")
        assert response.status_code == 200, asset
        assert response.headers["content-type"].startswith("application/javascript")
        assert response.text.strip(), asset
