from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_champion_review_layer_is_wired_to_canonical_entrypoint():
    server = (ROOT / "championship_server.py").read_text(encoding="utf-8")
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "urbion_championship_champion_review.js" in server
    assert "#fcc-champion-review" in layer
    assert "KM / OSC READINESS" in layer
    assert "SPATIAL → PLANNING IMPLICATION" in layer
    assert "CONTROLLED WHAT-IF" in layer
    assert "NEXT ACTION / DECISION" in layer


def test_champion_review_layer_preserves_planning_boundaries():
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "not approvals" in layer
    assert "does not grant or predict statutory approval" in layer
    assert "Do not represent it as pedestrian network travel time" in layer
    assert "without inventing geometry" in layer
