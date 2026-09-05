from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_decision_center_exposes_evidence_to_action_chain():
    html = read("decision-center.html")
    for token in (
        "EVIDENCE",
        "SCORE",
        "WHY",
        "DECISION",
        "REVIEW",
        "ACTION",
        "EVIDENCE COVERAGE",
        "SCORE DRIVERS",
        "DECISION TRACE",
        "NEXT ACTIONS",
        "evidence_coverage",
        "score_breakdown",
        "review_gaps",
        "next_actions",
        "Decision support only",
        "Statutory approval or compliance is not claimed",
        "cache:'no-store'",
    ):
        assert token in html


def test_decision_center_does_not_fabricate_missing_scores():
    html = read("decision-center.html")
    assert "s===null?'—'" in html
    assert "No scored dimensions returned." in html
    assert "No decision output was fabricated." in html


def test_decision_center_escapes_dynamic_content():
    html = read("decision-center.html")
    assert "function esc(v)" in html
    assert "replace(/[&<>\"']/g" in html
