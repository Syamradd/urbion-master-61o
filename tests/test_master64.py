from urbion_site_intelligence import build_site_analysis


def test_master64_exposes_decision_visuals():
    result = build_site_analysis(
        state="Melaka", district="Melaka Tengah",
        pbt="Majlis Bandaraya Melaka Bersejarah", lot_no="L-01",
        latitude=2.3, longitude=102.2, tod_distance_m=222.4,
        development_class="Mixed Use",
        development_type="TOD Development / Mixed Use",
        policy_status="COMPLY", final_status="COMPLY",
    )
    assert result["recommendation"]["headline"]
    assert result["decision_confidence"]["score"] >= 80
