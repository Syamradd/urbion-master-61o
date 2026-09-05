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
    marker = 'for asset in ("urbion_championship_input_sync.js","urbion_championship_spatial_studio.js","urbion_championship_intelligence_upgrade.js","urbion_championship_decision_layer.js","urbion_championship_workflow.js"):'
    assert marker in text
    assert 'app.state.frontend_release="MASTER-316"' in text
    assert 'Cache-Control' in text
