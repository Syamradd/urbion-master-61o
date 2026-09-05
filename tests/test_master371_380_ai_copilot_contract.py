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
    assert packet["agents"]["handoff"]["knowledge_to_policy"]["evidence_boundary"] == packet["knowledge"]["evidence_boundary"]


def test_copilot_scenarios_are_executed_and_ranked():
    packet = build_copilot_packet(_inputs(), variants=[
        {"id": "A", "name": "Lower intensity", "overrides": {"plot_ratio": 3.0}},
        {"id": "B", "name": "Higher intensity", "overrides": {"plot_ratio": 6.0}},
    ])
    scenarios = packet["scenario_intelligence"]
    assert scenarios["status"] == "COMPLETE"
    assert scenarios["count"] == 2
    assert len(scenarios["scenarios"]) == 2
    assert set(scenarios["ranked_scenarios"]) == {"A", "B"}
    assert packet["preferred_scenario"] == scenarios["best_candidate"]
    assert packet["decision"]["scenario_intelligence"]["best_candidate"] == scenarios["best_candidate"]
    assert packet["agents"]["handoff"]["scenario_to_decision"]["best_candidate"] == scenarios["best_candidate"]
    assert packet["statutory_verification"] == "NOT_CLAIMED"


def test_copilot_rejects_more_than_twelve_variants():
    variants = [{"id": str(i), "overrides": {"plot_ratio": 1.0 + i / 10}} for i in range(13)]
    try:
        build_copilot_packet(_inputs(), variants=variants)
    except ValueError as exc:
        assert "at most 12" in str(exc)
    else:
        raise AssertionError("Expected bounded scenario validation")


def test_copilot_api_is_reachable_from_production_entrypoint():
    client = TestClient(app)
    response = client.post("/copilot/run", json=_inputs())
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "BOUNDED_PLANNER_COPILOT"
    assert body["decision_authority"] == "NONE"
    assert body["statutory_verification"] == "NOT_CLAIMED"
