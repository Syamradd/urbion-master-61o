from urbion_landuse_evidence import landuse_evidence, compatibility_signal


def test_discovery_landuse_is_not_decision_safe():
    items = landuse_evidence(land_use="Mixed Use", zoning="Urban Mixed Use")
    assert len(items) == 2
    assert all(x["decision_safe"] is False for x in items)


def test_verified_alignment_is_only_a_signal():
    result = compatibility_signal(development_class="Mixed Use", land_use="Mixed Use", zoning="Urban Mixed Use")
    assert result["signal"] == "POTENTIAL_ALIGNMENT"


def test_missing_evidence_is_unknown():
    result = compatibility_signal(development_class="Commercial", land_use=None, zoning=None)
    assert result["signal"] == "UNKNOWN"
