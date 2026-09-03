from urbion_environment_implications import build_environment_implications


def test_flagged_environment_becomes_planning_implication():
    result = build_environment_implications({"metrics": [{"id": "flood", "value": True, "status": "RISK_FLAG", "risk_flag": True, "evidence": "SOURCE_CONTEXT", "source": "PLANMalaysia DPFDN — Banjir 100 tahun"}]})
    assert result["version"] == "MASTER-233"
    assert result["count"] == 1
    assert result["flagged_count"] == 1
    item = result["implications"][0]
    assert item["domain"] == "flood"
    assert item["risk_flag"] is True
    assert item["evidence"] == "SOURCE_CONTEXT"
    assert item["status"] == "PLANNER_REVIEW"


def test_unverified_environment_does_not_create_fake_implication():
    result = build_environment_implications({"metrics": [{"id": "flood", "value": None, "status": "REVIEW_REQUIRED", "risk_flag": None, "evidence": "UNVERIFIED"}]})
    assert result["implications"] == []
    assert result["review_gaps"] == ["ENVIRONMENT_NO_TRACEABLE_PLANNING_IMPLICATION"]
