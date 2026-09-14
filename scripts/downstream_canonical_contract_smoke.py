"""Validate downstream decision, planner handoff and judge-demo surfaces keep the canonical packet boundary."""
from __future__ import annotations
import json, os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
PAYLOAD = {
    "site_lat": 2.285, "site_lon": 102.196, "tod_lat": 2.286, "tod_lon": 102.196,
    "plot_ratio": 4.5, "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use", "development_class": "Mixed Use",
    "state": "Melaka", "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": ""
}


def post(path: str, payload: dict) -> dict:
    req = Request(BASE + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=90) as response:
            assert response.status == 200, f"{path}: expected 200, got {response.status}"
            return json.loads(response.read().decode())
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AssertionError(f"{path}: HTTP {exc.code} body={body}") from exc


def _canonical_packet(payload: dict) -> dict:
    """Locate the one canonical packet regardless of approved wrapper nesting."""
    direct = payload.get("canonical_evidence_packet")
    if isinstance(direct, dict) and direct:
        return direct
    copilot = payload.get("copilot")
    if isinstance(copilot, dict):
        nested = copilot.get("canonical_evidence_packet")
        if isinstance(nested, dict) and nested:
            return nested
    deterministic = payload.get("deterministic_packet")
    if isinstance(deterministic, dict) and deterministic:
        nested = deterministic.get("canonical_evidence_packet")
        if isinstance(nested, dict) and nested:
            return nested
    return {}


def _canonical_status(payload: dict) -> str | None:
    packet = _canonical_packet(payload)
    status = packet.get("convergence", {}).get("status")
    if status:
        return status
    handoff = payload.get("handoff")
    if isinstance(handoff, dict):
        status = (handoff.get("canonical_convergence") or {}).get("status")
        if status:
            return status
    return None


def main() -> None:
    decision = post("/intelligence/decision-os", {"assessment": PAYLOAD})
    packet = decision.get("deterministic_packet") or {}
    assert packet.get("convergence", {}).get("status") == "CANONICAL"
    assert decision.get("statutory_verification") == "NOT_CLAIMED"
    decision_os = decision.get("decision_os") or {}
    assert decision_os.get("decision_authority") == "NONE"
    assert decision_os.get("statutory_verification") == "NOT_CLAIMED"

    handoff = post("/planner/handoff", {"assessment": PAYLOAD})
    assert _canonical_status(handoff) == "CANONICAL"
    assert (handoff.get("handoff") or {}).get("decision_authority") == "NONE"
    assert (handoff.get("handoff") or {}).get("statutory_verification") == "NOT_CLAIMED"

    demo = post("/judge/demo", {"assessment": PAYLOAD})
    assert demo.get("guardrails", {}).get("decision_authority") == "NONE"
    assert demo.get("guardrails", {}).get("statutory_verification") == "NOT_CLAIMED"
    assert _canonical_status(demo) == "CANONICAL"

    print("DOWNSTREAM CANONICAL CONTRACT PASS")


if __name__ == "__main__":
    main()
