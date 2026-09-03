from pathlib import Path


def test_autonomous_release_runbook_is_present_and_safe():
    text = Path("MASTER-133-AUTONOMOUS-RUNBOOK.md").read_text(encoding="utf-8")
    for marker in (
        "Execution order",
        "highest-value incomplete",
        "deterministic regression contract",
        "green CI",
        "must not present an automated result as statutory approval",
        "applicant-specific OSC approval",
    ):
        assert marker in text


def test_release_rule_requires_ci_and_regression_contract():
    text = Path("MASTER-133-AUTONOMOUS-RUNBOOK.md").read_text(encoding="utf-8")
    assert "A release is not considered complete merely because code exists" in text
    assert "green CI result" in text
