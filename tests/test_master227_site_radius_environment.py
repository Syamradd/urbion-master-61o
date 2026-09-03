"""MASTER-227 tests: site-radius environmental evidence and LCP wiring."""
from urbion_environment_intelligence import build_environment_intelligence
from urbion_iplan import query_environment_context


def test_environment_query_maps_melaka_radius_hits(monkeypatch):
    def fake(url, timeout=8.0):
        if "/2/query" in url:
            return {"features":[{"attributes":{"ESA":"ESA RANK 2"}}]}
        if "/3/query" in url:
            return {"features":[{"attributes":{"DEGREES":"25 - 35"}}]}
        return {"features":[]}
    monkeypatch.setattr("urbion_iplan._request_json", fake)
    result = query_environment_context(2.285, 102.196, 1500, "Melaka")
    assert result["scope"] == "MELAKA_FOCUSED"
    assert result["radius_m"] == 1500
    assert result["layers"]["flood"]["feature_count"] == 1
    assert result["layers"]["ksas"]["feature_count"] == 1
    assert result["decision_boundary"] == "ENVIRONMENTAL_SCREENING_SUPPORT"


def test_environment_intelligence_derives_explicit_risk_flags():
    context = {"site":{"latitude":2.285,"longitude":102.196},"radius_m":1000,"layers":{
        "flood":{"feature_count":1,"features":[{}]},
        "ksas":{"feature_count":0,"features":[]},
        "slope":{"feature_count":1,"features":[{"DEGREES":"25 - 35"}]},
        "geohazard":{"feature_count":0,"features":[]},
        "seismic":{"feature_count":0,"features":[]},
        "ecology":{"feature_count":0,"features":[]},
        "river":{"feature_count":0,"features":[]},
    }}
    result = build_environment_intelligence(context)
    by_id = {item["id"]: item for item in result["metrics"]}
    assert by_id["flood"]["risk_flag"] is True
    assert by_id["slope"]["status"] == "SLOPE_RISK"
    assert result["status"] == "RISK_FLAGGED"
    assert result["statutory_verification"] == "NOT_CLAIMED"
