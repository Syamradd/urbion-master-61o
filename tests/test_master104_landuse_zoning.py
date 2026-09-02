from urbion_landuse_zoning import layer_feature, zoning_signal, landuse_summary

def test_layer_feature_geojson_order():
    f=layer_feature(latitude=2.3,longitude=102.2,layer="ZONING",value="Mixed Use",lot_no="11213")
    assert f["geometry"]["coordinates"] == [102.2,2.3]

def test_missing_evidence_is_not_decision_safe():
    r=zoning_signal(development_class="Commercial",land_use=None,zoning=None)
    assert r["signal"]=="UNKNOWN" and r["decision_safe"] is False

def test_alignment_is_only_potential():
    r=zoning_signal(development_class="Mixed Use",land_use="Mixed Use",zoning="Mixed Use")
    assert r["signal"]=="POTENTIAL_ALIGNMENT" and r["decision_safe"] is False

def test_summary_discloses_source_gap():
    assert landuse_summary(land_use=None,zoning=None)["evidence_required"] is True
