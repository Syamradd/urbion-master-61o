from urbion_landuse_zoning import zoning_signal

def test_non_matching_evidence_stays_review():
    r=zoning_signal(development_class="Industrial",land_use="Residential",zoning="Residential")
    assert r["signal"]=="REVIEW"
    assert r["decision_safe"] is False
