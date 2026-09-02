from urbion_site_intelligence import build_site_analysis


def _analysis(status="COMPLY", pbt="Majlis Bandaraya Melaka Bersejarah", lot="L-01", distance=222.4):
    return build_site_analysis(
        state="Melaka",
        district="Melaka Tengah",
        pbt=pbt,
        lot_no=lot,
        latitude=2.3,
        longitude=102.2,
        tod_distance_m=distance,
        development_class="Mixed Use",
        development_type="TOD Development / Mixed Use",
        policy_status=status,
        final_status=status,
    )


def test_positive_decision_has_recommendation_and_confidence():
    result = _analysis()
    assert result["recommendation"]["level"] == "POSITIVE"
    assert result["decision_confidence"]["band"] == "HIGH"
    assert result["decision_confidence"]["score"] >= 80


def test_non_compliance_is_blocked():
    result = _analysis(status="NON-COMPLIANCE")
    assert result["recommendation"]["level"] == "BLOCKED"
    assert "REDESIGN" in result["recommendation"]["headline"]


def test_other_pbt_requires_evidence():
    result = _analysis(pbt="Majlis Bandaraya Shah Alam")
    assert result["recommendation"]["level"] == "REVIEW"
    assert result["decision_confidence"]["band"] in {"MEDIUM", "LOW"}
