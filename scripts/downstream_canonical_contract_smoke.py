"""Validate downstream decision, planner handoff and judge-demo surfaces keep the canonical packet boundary."""
from __future__ import annotations
import json, os
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
    with urlopen(req, timeout=90) as response:
        assert response.status == 200, f"{path}: expected 200, got {response.status}"
        return json.loads(response.read().decode())


def main() -> None:
    decision = post("/intelligence/decision-os", {"assessment": PAYLOAD})
    packet = decision.get("deterministic_packet") or {}
    assert packet.get("convergence", {}).get("status") == "CANONICAL"
    assert decision.get("statutory_verification") == "NOT_CLAIMED"
    decision_os = decision.get("decision_os") or {}
    assert decision_os.get("decision_authority") == "NONE"
    assert decision_os.get("statutory_verification") == "NOT_CLAIMED"

    handoff = post("/planner/handoff", {"assessment": PAYLOAD})
    handoff_packet = handoff.get("canonical_evidence_packet") or {}
    assert handoff_packet.get("convergence", {}).get("status") == "CANONICAL"
    assert (handoff.get("handoff") or {}).get("canonical_convergence", {}).get("status") == "CANONICAL"
    assert (handoff.get("handoff") or {}).get("decision_authority") == "NONE"
    assert (handoff.get("handoff") or {}).get("statutory_verification") == "NOT_CLAIMED"

    demo = post("/judge/demo", {"assessment": PAYLOAD})
    demo_packet = demo.get("canonical_evidence_packet") or demo.get("deterministic_packet") or {}
    assert demo.get("guardrails", {}).get("decision_authority") == "NONE"
    assert demo.get("guardrails", {}).get("statutory_verification") == "NOT_CLAIMED"
    assert demo_packet.get("convergence", {}).get("status") == "CANONICAL"

    print("DOWNSTREAM CANONICAL CONTRACT PASS")


if __name__ == "__main__":
    main()
