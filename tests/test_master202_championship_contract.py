from pathlib import Path

from fastapi.testclient import TestClient

from server import AssessmentRequest, assess_core
from urbion_release_contract import audit_deployment_manifest, audit_lcp_contract, build_championship_gate
from urbion_lcp_intelligence import build_lcp_intelligence


def sample_assessment():
    return AssessmentRequest(site_lat=2.285, site_lon=102.196, tod_lat=2.286, tod_lon=102.197)


def sample_lcp():
    return build_lcp_intelligence(assessment=assess_core(sample_assessment()))


def test_lcp_contract_passes_current_integrated_output():
    audit = audit_lcp_contract(sample_lcp())
    assert audit["status"] == "PASS"
    assert audit["failures"] == []
    assert audit["statutory_verification"] == "NOT_CLAIMED"


def test_lcp_contract_rejects_statutory_upgrade():
    result = sample_lcp()
    result["statutory_verification"] = "VERIFIED"
    audit = audit_lcp_contract(result)
    assert audit["status"] == "FAIL"
    assert "statutory_verification:NOT_CLAIMED_REQUIRED" in audit["failures"]


def test_deployment_manifest_matches_declared_stack():
    import json
    manifest = json.loads(Path("DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"))
    audit = audit_deployment_manifest(manifest)
    assert audit["status"] == "PASS"
    assert audit["failures"] == []


def test_championship_gate_combines_both_contracts():
    import json
    manifest = json.loads(Path("DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"))
    gate = build_championship_gate(lcp=sample_lcp(), manifest=manifest)
    assert gate["status"] == "PASS"
    assert gate["failures"] == []
    assert gate["decision_authority"] == "NONE"


def test_championship_gate_endpoint_is_available():
    client = TestClient(__import__("urbion_gateway").app)
    response = client.get("/championship-gate")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "PASS"
    assert body["release"] == "CHAMPIONSHIP"
