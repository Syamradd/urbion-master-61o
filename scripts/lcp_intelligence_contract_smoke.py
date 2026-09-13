"""Contract smoke for optional integrated LCP intelligence."""
from __future__ import annotations

from urbion_lcp_intelligence import build_lcp_intelligence


def main() -> None:
    assessment = {
        "development_type": "Commercial",
        "development_class": "Shop Office",
        "pbt": "Majlis Bandaraya Melaka Bersejarah",
        "site": {"latitude": 2.2, "longitude": 102.25},
        "review_gaps": [],
    }
    result = build_lcp_intelligence(
        assessment=assessment,
        spatial_inputs={"road_distance_m": 850, "source_context": {"test": True}},
        environment_context={"status": "QUERY_ERROR", "review_gaps": ["environment:TEST_REVIEW"]},
    )
    assert result["project"] == "URBION HORIZON"
    assert result["decision_boundary"] == "INTEGRATED_LCP_PLANNING_SUPPORT"
    assert result["statutory_verification"] == "NOT_CLAIMED"
    assert "development_impact" in result
    assert "environment_intelligence" in result
    assert "policy_graph" in result
    assert "review_gaps" in result
    print("LCP INTELLIGENCE CONTRACT PASS")
    print({"version": result["version"], "review_gap_count": result["evidence_summary"]["review_gap_count"]})


if __name__ == "__main__":
    main()
