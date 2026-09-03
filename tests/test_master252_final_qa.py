from pathlib import Path
import json

from fastapi.testclient import TestClient

from server import AssessmentRequest, app, assess_core
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_release_contract import audit_deployment_manifest, audit_lcp_contract, build_championship_gate


def sample_assessment():
    return AssessmentRequest(site_lat=2.285, site_lon=102.196, tod_lat=2.286, tod_lon=102.197)


def sample_lcp():
    return build_lcp_intelligence(assessment=assess_core(sample_assessment()))


def test_final_qa_contract_keeps_identity_and_boundary():
    lcp = sample_lcp()
    audit = audit_lcp_contract(lcp)
    assert audit["status"] == "PASS"
    assert lcp["version"] == "MASTER-199"
    assert lcp["decision_boundary"] == "INTEGRATED_LCP_PLANNING_SUPPORT"
    assert lcp["statutory_verification"] == "NOT_CLAIMED"


def test_final_qa_manifest_and_gate_pass():
    manifest = json.loads(Path("DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"))
    assert audit_deployment_manifest(manifest)["status"] == "PASS"
    gate = build_championship_gate(lcp=sample_lcp(), manifest=manifest)
    assert gate["status"] == "PASS"
    assert gate["failures"] == []
    assert gate["decision_authority"] == "NONE"


def test_final_qa_review_packet_endpoint_is_discoverable():
    client = TestClient(app)
    response = client.post("/lcp/review-packet", json={"lcp": sample_lcp()})
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "MASTER-251"
    assert body["release_identity"] == "MASTER-199"
    assert body["statutory_verification"] == "NOT_CLAIMED"
    assert body["decision_boundary"] == "INTEGRATED_LCP_PLANNING_SUPPORT"


def test_final_qa_review_packet_rejects_missing_lcp():
    client = TestClient(app)
    response = client.post("/lcp/review-packet", json={})
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "LCP_RESULT_REQUIRED"
