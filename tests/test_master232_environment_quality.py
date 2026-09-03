from urbion_environment_intelligence import build_environment_intelligence


def test_missing_environment_evidence_is_explicitly_unverified():
    result = build_environment_intelligence({})
    assert result["version"] == "MASTER-226"
    assert result["status"] == "EVIDENCE_REQUIRED"
    assert result["summary"]["review_gap_count"] == 11
    assert result["evidence_quality"]["counts"]["unverified"] == 11
    assert result["evidence_quality"]["evidence_sources"] == []


def test_source_context_is_counted_as_evidence():
    result = build_environment_intelligence({"layers": {"flood": {"feature_count": 2}}})
    assert result["status"] == "RISK_FLAGGED"
    assert result["evidence_quality"]["counts"]["source_context"] == 1
    assert result["evidence_quality"]["evidence_sources"] == ["PLANMalaysia DPFDN — Banjir 100 tahun"]
