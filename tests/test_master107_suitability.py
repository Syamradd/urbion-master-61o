from urbion_suitability_engine import score_suitability


def test_high_potential_weighted_score():
    result = score_suitability(planning_fit=95, transit_access=90, data_confidence=85, site_completeness=90, environment_evidence=80)
    assert result["score"] >= 80
    assert result["band"] == "HIGH POTENTIAL"


def test_score_is_bounded():
    result = score_suitability(planning_fit=150, transit_access=-5, data_confidence=50, site_completeness=50, environment_evidence=50)
    assert 0 <= result["score"] <= 100
