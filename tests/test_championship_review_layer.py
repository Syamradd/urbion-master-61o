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
    assert "canonical What-If" in layer
    assert "urbion:unified-state" in layer
    assert "urbion:what-if" in layer
    assert "urbion:km-readiness" in layer
    assert "fetch('/km/readiness?" in layer


def test_champion_review_layer_preserves_planning_boundaries():
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "not approval" in layer
    assert "does not grant or predict statutory approval" in layer
    assert "Do not represent it as pedestrian network travel time" in layer
    assert "without inventing geometry" in layer


def test_hotfix_routes_controlled_scenarios_to_canonical_what_if_api():
    hotfix = (ROOT / "urbion_championship_final_command_center_hotfix.js").read_text(encoding="utf-8")
    assert "fetch('/what-if'" in hotfix
    assert "variants:[{id:'SELECTED'" in hotfix
    assert "urbion:what-if" in hotfix
    assert "fetch('/assess'" in hotfix


def test_km_readiness_requires_explicit_category_and_passes_it_to_backend():
    layer = (ROOT / "urbion_championship_champion_review.js").read_text(encoding="utf-8")
    assert "fcr-km-category" in layer
    assert "KECIL" in layer and "SEDERHANA" in layer and "BESAR" in layer
    assert "km_category" in layer
    assert "q.set('km_category',cat)" in layer
