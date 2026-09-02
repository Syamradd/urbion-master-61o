from urbion_gis_binding import bind_gis_layers


def test_verified_layers_are_decision_ready():
    evidence = [
        {"layer": "PARCEL", "status": "VERIFIED", "decision_safe": True},
        {"layer": "LAND_USE", "status": "VERIFIED", "decision_safe": True},
        {"layer": "ZONING", "status": "VERIFIED", "decision_safe": True},
    ]
    result = bind_gis_layers(evidence=evidence, required_layers=["PARCEL", "LAND_USE", "ZONING"])
    assert result["decision_ready"] is True


def test_discovery_does_not_become_verified():
    evidence = [{"layer": "ZONING", "status": "DISCOVERY_COMPLETE", "decision_safe": False}]
    result = bind_gis_layers(evidence=evidence, required_layers=["ZONING"])
    assert result["layers"][0]["status"] == "GAP"
    assert result["decision_ready"] is False
