from urbion_site_intelligence import _evidence_aware_score, build_site_analysis


def test_missing_environment_evidence_is_excluded_not_fabricated():
    result = build_site_analysis(
        "Melaka", "Melaka Tengah", "Majlis Bandaraya Melaka Bersejarah", "LOT-01",
        2.285, 102.196, 300, "Mixed Use", "TOD Development / Mixed Use",
        "COMPLY", "COMPLY", retrieved_rules=1,
    )
    env = next(item for item in result["indicators"] if item["name"] == "Environment Evidence")
    assert env["score"] is None
    assert env["status"] == "UNVERIFIED"
    assert "Environment Evidence" in result["score_coverage"]["excluded_unverified"]
    assert result["score_coverage"]["assessed_dimensions"] == 4


def test_evidence_aware_score_renormalizes_weights():
    score, count = _evidence_aware_score([
        ("A", 100, 0.5),
        ("B", None, 0.5),
    ])
    assert score == 100
    assert count == 1


def test_tod_distance_discloses_method():
    result = build_site_analysis(
        "Melaka", "Melaka Tengah", "Majlis Bandaraya Melaka Bersejarah", "LOT-01",
        2.285, 102.196, 350, "Mixed Use", "TOD Development / Mixed Use",
        "COMPLY", "COMPLY", retrieved_rules=1,
    )
    assert "Haversine" in result["spatial_summary"]["tod_distance_method"]
    assert "network" in result["spatial_summary"]["tod_distance_method"]
