from urbion_site_intelligence import build_site_analysis


def test_high_confidence_positive_recommendation():
    result = build_site_analysis(
        state="Melaka", district="Melaka Tengah",
        pbt="Majlis Bandaraya Melaka Bersejarah", lot_no="11213",
        latitude=2.30, longitude=102.20, tod_distance_m=220,
        development_class="Mixed Use", development_type="TOD Development / Mixed Use",
        policy_status="COMPLY", final_status="COMPLY",
    )
    assert result["recommendation"]["level"] == "POSITIVE"
    assert result["decision_confidence"]["band"] == "HIGH"
    assert len(result["indicators"]) == 5


def test_non_compliance_recommends_redesign():
    result = build_site_analysis(
        state="Melaka", district="Melaka Tengah",
        pbt="Majlis Bandaraya Melaka Bersejarah", lot_no="11213",
        latitude=2.30, longitude=102.20, tod_distance_m=220,
        development_class="Commercial", development_type="Commercial Shop-Office",
        policy_status="NON-COMPLIANCE", final_status="NON-COMPLIANCE",
    )
    assert result["recommendation"]["level"] == "BLOCKED"
    assert "REDESIGN" in result["recommendation"]["headline"]


def test_other_pbt_stays_review():
    result = build_site_analysis(
        state="Selangor", district="Petaling",
        pbt="Majlis Bandaraya Petaling Jaya", lot_no="",
        latitude=3.10, longitude=101.60, tod_distance_m=500,
        development_class="Commercial", development_type="Free-Standing Commercial",
        policy_status="REQUIRES REVIEW", final_status="REQUIRES REVIEW",
    )
    assert result["recommendation"]["level"] == "REVIEW"
    assert result["decision_confidence"]["band"] in {"LOW", "MEDIUM"}
