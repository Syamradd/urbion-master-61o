from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workstation_exposes_bounded_ai_explain_control():
    source = (ROOT / "urbion_championship_workstation_v2.js").read_text(encoding="utf-8")
    assert "AI EXPLAIN" in source
    assert "fetch('/copilot/explain'" in source
    assert "Deterministic source" in source
    assert "narrative-only" in source
