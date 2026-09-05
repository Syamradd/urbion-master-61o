from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_legacy_decision_surface_is_fallback_only_when_intelligence_surface_exists():
    legacy = read("urbion_championship_decision_layer.js")
    server = read("championship_server.py")
    assert "document.getElementById('intel-upgrade')" in legacy
    assert "id='decision-layer'" in legacy
    assert "urbion_championship_intelligence_upgrade.js" in server
    assert "urbion_championship_decision_layer.js" in server
    assert "urbion_championship_intelligence_upgrade.js\",\"urbion_championship_decision_layer.js" in server


def test_fallback_keeps_legacy_guardrail_and_assessment_path():
    legacy = read("urbion_championship_decision_layer.js")
    for token in ["PLANNER GUARDRAIL", "Screening support only", "window.URBION?.assess", "/assess", "urbion:analysis"]:
        assert token in legacy
