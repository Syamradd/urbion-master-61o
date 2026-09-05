from fastapi.testclient import TestClient
from championship_server import app
from urbion_copilot import build_copilot_packet


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
    }


def test_copilot_packet_is_unified_and_guarded():
    packet = build_copilot_packet(_inputs())
    assert packet["mode"] == "BOUNDED_PLANNER_COPILOT"
    assert packet["decision_authority"] == "NONE"
    assert packet["statutory_verification"] == "NOT_CLAIMED"
    assert packet["knowledge"]["generation_ready"] is True
    assert packet["impact"]["status"] == "REVIEW_REQUIRED"
    assert len(packet["agents"]["agents"]) == 7


def test_copilot_scenarios_are_executed_and_ranked():
    packet = build_copilot_packet(_inputs(), variants=[
        {"id": "A", "name": "Lower intensity", "changes": {"plot_ratio": 3.0}},
        {"id": "B", "name": "Higher intensity", "changes": {"plot_ratio": 6.0}},
    ])
    scenarios = packet["scenario_intelligence"]
    assert scenarios["status"] == "COMPLETE"
    assert scenarios["count"] == 2
    assert len(scenarios["scenarios"]) == 2
    assert len(scenarios["ranked_scenarios"]) == 2
    assert packet["preferred_scenario"] is not None
    assert packet["agents"]["agents"][5]["agent"] == "SCENARIO"
    assert packet["agents"][5]["status"] == "COMPLETE"
    assert packet["statutory_verification"] == "NOT_CLAIMED"


def test_copilot_api_is_reachable_from_production_entrypoint():
    client = TestClient(app)
    response = client.post("/copilot/run", json=_inputs())
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "BOUNDED_PLANNER_COPILOT"
    assert body["decision_authority"] == "NONE"
    assert body["statutory_verification"] == "NOT_CLAIMED"
