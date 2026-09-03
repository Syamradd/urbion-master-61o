from fastapi.testclient import TestClient
from server import app
from urbion_release_packet import build_release_packet


def test_release_packet_is_auditable_and_bounded():
    body = build_release_packet({
        "trace": "SITE → SPATIAL → IMPACT → POLICY → RECOMMENDATION",
        "evidence_summary": {"counts": {"CALCULATED": 2}, "review_gap_count": 1},
        "review_gaps": ["policy:REFERENCE_REQUIRED"],
        "recommendations": {"recommendations": [{"action": "Review mitigation", "status": "PLANNER_REVIEW", "reason": "Evidence gap"}]},
        "statutory_verification": "NOT_CLAIMED",
    })
    assert body["version"] == "MASTER-195"
    assert body["statutory_verification"] == "NOT_CLAIMED"
    assert body["review_gap_count"] == 1
    assert body["top_recommendations"][0]["status"] == "PLANNER_REVIEW"


def test_release_packet_endpoint_rejects_missing_lcp():
    client = TestClient(app)
    response = client.post("/lcp/release-packet", json={})
    assert response.status_code == 422


def test_release_packet_endpoint_returns_safe_handoff():
    client = TestClient(app)
    response = client.post("/lcp/release-packet", json={"lcp": {"trace": "TRACE", "statutory_verification": "NOT_CLAIMED"}})
    assert response.status_code == 200
    assert response.json()["version"] == "MASTER-195"
    assert response.json()["statutory_verification"] == "NOT_CLAIMED"
