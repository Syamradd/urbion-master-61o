from urbion_site_intelligence import DEVELOPMENT_CLASSES, STATE_PBT, build_site_analysis, policy_coverage


def test_official_pbt_registry_contains_melaka():
    assert "Majlis Bandaraya Melaka Bersejarah" in STATE_PBT["Melaka"]
    assert len(STATE_PBT["Melaka"]) == 4


def test_development_classes_are_typology_aware():
    assert "Commercial Shop Frontage" in DEVELOPMENT_CLASSES["Commercial"]
    assert "TOD Development / Mixed Use" in DEVELOPMENT_CLASSES["Mixed Use"]
    assert "Light Industry" in DEVELOPMENT_CLASSES["Industrial"]


def test_mbmb_policy_coverage_is_rule_engine():
    result = policy_coverage("Majlis Bandaraya Melaka Bersejarah")
    assert result["coverage"] == "FULL_RULE_ENGINE"
    assert result["reference"] == "RT MBMB 2035"


def test_other_pbt_does_not_fake_local_rules():
    result = policy_coverage("Majlis Bandaraya Shah Alam")
    assert result["coverage"] == "SPATIAL_DEMO_ONLY"
    assert "not loaded" in result["message"]


def test_suitability_profile_returns_chart_indicators():
    result = build_site_analysis(
        state="Melaka",
        district="Melaka Tengah",
        pbt="Majlis Bandaraya Melaka Bersejarah",
        lot_no="Demo-001",
        latitude=2.3,
        longitude=102.2,
        tod_distance_m=222.4,
        development_class="Mixed Use",
        development_type="TOD Development / Mixed Use",
        policy_status="COMPLY",
        final_status="COMPLY",
    )
    assert result["score"] > 0
    assert len(result["indicators"]) == 5
    assert result["spatial_summary"]["lot_no"] == "Demo-001"
