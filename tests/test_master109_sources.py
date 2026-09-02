from urbion_planning_sources import planning_source_summary


def test_planning_sources_disclose_query_gaps():
    result = planning_source_summary()
    ids = {x["id"] for x in result["sources"]}
    assert {"RT_MBMB", "IPLAN", "MELGIS", "JUPEM"}.issubset(ids)
    assert "IPLAN" in result["evidence_gaps"]
    assert "MELGIS" in result["evidence_gaps"]


def test_registry_does_not_fake_verified_sources():
    result = planning_source_summary()
    assert result["verified_query_sources"] == []
