from urbion_kebenaran_merancang import build_km_readiness


def test_km_readiness_does_not_assume_category():
    result = build_km_readiness(pbt="MBMB", development_type="Mixed Use")
    assert result["km_category_state"] == "REQUIRES_REVIEW"
    assert result["readiness"] == "REQUIRES_REVIEW"
    assert "KM category not explicitly classified" in result["blockers"]


def test_km_readiness_can_be_ready_for_workflow_review():
    docs = ["Location Plan", "Site Plan", "Development Proposal Report"]
    result = build_km_readiness(
        pbt="MBMB",
        development_type="Mixed Use",
        documents=docs,
        km_category="kecil",
    )
    assert result["km_category_state"] == "EXPLICIT"
    assert result["core_document_check"]["state"] == "READY"
    assert result["readiness"] == "READY_FOR_WORKFLOW_REVIEW"
    assert "approval" not in result["readiness"].lower()


def test_technical_objection_is_a_blocker():
    result = build_km_readiness(
        pbt="MBMB",
        development_type="Mixed Use",
        documents=["Location Plan", "Site Plan", "Development Proposal Report"],
        km_category="besar",
        technical_reviews={"JPS": "OBJECTION"},
    )
    assert result["readiness"] == "REQUIRES_REVIEW"
    assert "Technical review requires resolution" in result["blockers"]
