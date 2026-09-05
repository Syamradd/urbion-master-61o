from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_workflow_focuses_real_planning_states():
    text = read("urbion_championship_workflow.js")
    assert "const targets=" in text
    for token in ["#lat", "#spatial-studio", "#intel-upgrade", ".iu-score", "#decision-layer", ".judge"]:
        assert token in text
    assert "scrollIntoView" in text
    assert "uw-focus" in text
    assert "urbion:analysis" in text
    assert "urbion:site-change" in text


def test_shared_state_asset_loads_before_consumers():
    text = read("championship_server.py")
    assets = [
        "urbion_championship_input_sync.js",
        "urbion_championship_spatial_studio.js",
        "urbion_championship_intelligence_upgrade.js",
        "urbion_championship_decision_layer.js",
        "urbion_championship_workflow.js",
        "urbion_championship_decision_chain.js",
        "urbion_spatial_workstation_upgrade.js",
        "urbion_spatial_implication_bridge.js",
    ]
    for asset in assets:
        assert asset in text
    assert text.index("urbion_championship_spatial_studio.js") < text.index("urbion_spatial_workstation_upgrade.js") < text.index("urbion_spatial_implication_bridge.js")
    assert 'app.state.frontend_release="MASTER-323"' in text
    assert 'Cache-Control' in text


def test_decision_pathway_asset_is_allowlisted_and_loaded():
    text = read("championship_server.py")
    assert '"urbion_championship_decision_chain.js"' in text
    assert 'urbion_championship_decision_chain.js' in text


def test_judge_mode_uses_real_dimension_drivers_not_scenario_rows():
    judge = read("urbion_judge_mode.py")
    page = read("judge-mode.html")
    assert "def _dimension_drivers" in judge
    assert '"score_breakdown": _dimension_drivers(assessment)' in judge
    assert 'r.score_breakdown' in page
    assert 'rows.slice(0,4)' not in page
    for token in ["dimension", "status", "method", "Assessment dimensions", "SCORE DRIVERS"]:
        assert token in page
