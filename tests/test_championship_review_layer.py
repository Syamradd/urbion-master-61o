from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_champion_review_layer_is_wired_to_one_canonical_entrypoint():
    server = (ROOT / "championship_server.py").read_text(encoding="utf-8")
    hotfix = (ROOT / "urbion_championship_final_command_center_hotfix.js").read_text(encoding="utf-8")
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "urbion_championship_champion_review.js" in server
    assert server.count('"urbion_championship_champion_review.js"') >= 2
    assert "urbion_championship_champion_review.js" not in hotfix
    assert "#fcc-champion-review" in layer
    assert "KM / OSC READINESS" in layer
    assert "SPATIAL → PLANNING IMPLICATION" in layer
    assert "CONTROLLED WHAT-IF" in layer
    assert "NEXT ACTION / DECISION" in layer


def test_champion_review_uses_shared_state_and_canonical_assessment_runner():
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "window.__URBION_UNIFIED_STATE" in layer
    assert "window.URBION_FINAL_RUN" in layer
    assert "canonical assessment path" in layer
    assert "urbion:unified-state" in layer


def test_champion_review_layer_preserves_planning_boundaries():
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "not approval" in layer
    assert "does not grant or predict statutory approval" in layer
    assert "Do not represent it as pedestrian network travel time" in layer
    assert "without inventing geometry" in layer
