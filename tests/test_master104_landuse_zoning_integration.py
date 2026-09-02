from urbion_landuse_zoning import landuse_summary

def test_source_status_is_visible():
    r=landuse_summary(land_use="Commercial",zoning="Commercial",source_status="DISCOVERY_COMPLETE")
    assert r["source_status"]=="DISCOVERY_COMPLETE"
    assert r["evidence_required"] is False
