from urbion_environment_live import build_live_environment_evidence

import urbion_environment_live


def fake_query_environment_context(lat, lon, radius_m=1000, state="Melaka"):
    return {
        "provider": "PLANMalaysia DPFDN",
        "state": state,
        "scope": "MELAKA_FOCUSED",
        "site": {"latitude": lat, "longitude": lon},
        "radius_m": radius_m,
        "statutory_verification": "NOT_CLAIMED",
        "layers": {
            "flood": {"status": "LIVE_QUERY", "feature_count": 1, "features": []},
            "slope": {"status": "NO_FEATURE", "feature_count": 0, "features": []},
            "geohazard": {"status": "QUERY_UNAVAILABLE", "error": "fixture", "feature_count": 0},
        },
    }


def main():
    original = urbion_environment_live.query_environment_context
    urbion_environment_live.query_environment_context = fake_query_environment_context
    try:
        result = build_live_environment_evidence(
            latitude=2.285,
            longitude=102.196,
            state="Melaka",
            radius_m=1000,
        )
    finally:
        urbion_environment_live.query_environment_context = original

    assert result["statutory_verification"] == "NOT_CLAIMED"
    assert result["live_query"]["provider"] == "PLANMalaysia DPFDN"
    assert result["live_query"]["query_error_count"] == 1
    assert "geohazard" in result["live_query"]["query_error_layers"]
    statuses = {item["id"]: item["status"] for item in result["metrics"]}
    assert statuses["flood"] == "RISK_FLAG"
    assert statuses["geohazard"] == "QUERY_ERROR"
    assert "environment:geohazard" in result["review_gaps"]
    assert result["decision_boundary"] == "ENVIRONMENTAL_SCREENING_SUPPORT"
    print({"status": "PASS", "query_errors": result["live_query"]["query_error_count"], "review_gaps": len(result["review_gaps"])})


if __name__ == "__main__":
    main()
