from urbion_scenario_ranking import rank_scenarios


def test_compliant_scenario_ranks_first():
    result = rank_scenarios({"scenarios": [
        {"id": "FAIL", "status": "NON-COMPLIANCE", "score": 90, "blockers": ["walkway"], "evidence_gaps": []},
        {"id": "PASS", "status": "COMPLY", "score": 72, "blockers": [], "evidence_gaps": []},
    ]})
    assert result["best_candidate"] == "PASS"
    assert result["scenarios"][0]["rank"] == 1
    assert result["decision_pathway"]


def test_review_with_evidence_gap_does_not_beat_clean_review():
    result = rank_scenarios({"scenarios": [
        {"id": "GAP", "status": "REQUIRES REVIEW", "score": 95, "blockers": [], "evidence_gaps": ["local policy"]},
        {"id": "CLEAN", "status": "REQUIRES REVIEW", "score": 70, "blockers": [], "evidence_gaps": []},
    ]})
    assert result["best_candidate"] == "CLEAN"


def test_non_compliance_pathway_requires_redesign():
    result = rank_scenarios({"scenarios": [{"id": "X", "status": "NON-COMPLIANCE", "score": 50, "blockers": ["rule"], "evidence_gaps": []}]})
    assert "redesign" in result["decision_pathway"][0].lower()
