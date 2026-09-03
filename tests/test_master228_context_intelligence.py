from urbion_agency_intelligence import build_agency_intelligence, classify_distance
from urbion_guideline_intelligence import build_guideline_intelligence

def test_agency_radius_ranks_assets():
    result=build_agency_intelligence(2.285,102.196,{"JPS":[{"id":"near","latitude":2.286,"longitude":102.197},{"id":"far","latitude":2.31,"longitude":102.22}]},5000)
    jps=next(x for x in result["agencies"] if x["id"]=="JPS")
    assert jps["nearest"][0]["id"]=="near"
    assert jps["nearest"][0]["distance_m"]>0
    assert classify_distance(jps["nearest"][0]["distance_m"]).startswith("WITHIN_")

def test_guideline_catalog_matches_mixed_use():
    result=build_guideline_intelligence("TOD Development / Mixed Use","Mixed Use",["parking"],"Majlis Bandaraya Melaka Bersejarah")
    ids={x["id"] for x in result["guidelines"]}
    assert "GPP_PERDAGANGAN" in ids
    assert "GPP_TLK" in ids
    assert result["statutory_verification"]=="NOT_CLAIMED"
