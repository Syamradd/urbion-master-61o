from pathlib import Path


JS = (Path(__file__).resolve().parents[1] / "urbion_championship_intelligence_upgrade.js").read_text(encoding="utf-8")


def test_intelligence_ui_does_not_publish_stale_fixed_score_weights():
    assert "Dimension weights are taken from the assessment response" in JS
    assert "Environment Evidence 15%" not in JS
    assert "missing/unverified dimensions are excluded" in JS


def test_intelligence_ui_represents_missing_scores_as_unknown():
    assert "Number.isFinite(n)?n.toFixed(1):'—'" in JS
    assert "const width=Number.isFinite(n)?" in JS
    assert "Number(x.score||0).toFixed(1)" not in JS


def test_intelligence_ui_preserves_decision_support_guardrail():
    assert "not statutory approval" in JS
    assert "never interprets the score as approval probability" in JS
    assert "coordinate-based screening calculations" in JS
