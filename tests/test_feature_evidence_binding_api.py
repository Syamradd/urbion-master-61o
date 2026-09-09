from fastapi.testclient import TestClient

from championship_server import app


def test_feature_evidence_binding_returns_candidate_rules_and_never_decision_safe():
    feature = {
        "layer_id": "iplan-zoning",
        "feature_id": "ZONE-123",
        "layer_name": "i-Plan Zoning",
        "source": "https://example.test/iplan",
        "query_status": "LIVE_QUERY",
        "evidence_state": "SOURCE_CONTEXT",
        "properties": {"KELAS_GUNA_TANAH": "Commercial"},
    }
    response = TestClient(app).post(
        "/spatial/feature-evidence/bind",
        json={"feature": feature, "development_type": "Free-Standing Building", "authority": "MBMB"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence"]["eligible_for_rule_binding"] is True
    assert payload["binding_status"] in {"BOUND_CANDIDATES", "ELIGIBLE_NO_RULE_MATCH"}
    assert payload["decision_safe"] is False
    assert payload["statutory_approval_claim"] is False
    assert isinstance(payload["rules"], list)


def test_feature_evidence_binding_blocks_gap_from_rule_binding():
    response = TestClient(app).post(
        "/spatial/feature-evidence/bind",
        json={
            "feature": {
                "layer_id": "iplan-flood",
                "feature_id": "FLOOD-1",
                "source": "https://example.test/iplan",
                "query_status": "QUERY_ERROR",
                "evidence_state": "REVIEW",
            },
            "development_type": "Free-Standing Building",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence"]["eligible_for_rule_binding"] is False
    assert payload["binding_status"] == "REVIEW"
    assert payload["rules"] == []
    assert payload["decision_safe"] is False
