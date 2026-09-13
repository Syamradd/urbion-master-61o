"""Phase 1 integration smoke for the canonical evidence envelope.

The check uses the running local FastAPI server and verifies that /assess and
/workstation/analysis expose the same deterministic assessment packet.
"""
from __future__ import annotations

import json
import os
import urllib.request

BASE_URL = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PAYLOAD = {
    "site_lat": 2.285,
    "site_lon": 102.196,
    "tod_lat": 2.286,
    "tod_lon": 102.197,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
}


def _post(path: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 200, f"unexpected {path} status: {response.status}"
        return json.loads(response.read().decode("utf-8"))


def _assert_packet(packet: dict, assessment: dict, label: str) -> None:
    assert isinstance(packet, dict), f"canonical_evidence_packet missing from {label}"
    assert packet.get("version") == "PHASE1.2", f"unexpected {label} packet version"
    assert packet.get("assessment", {}).get("final_status") == assessment.get("final_status"), f"{label} packet/result status mismatch"
    assert packet.get("site", {}).get("latitude") == assessment.get("site", {}).get("latitude"), f"{label} packet/result site mismatch"
    assert packet.get("statutory_verification") == "NOT_CLAIMED", f"{label} statutory verification boundary changed"
    assert isinstance(packet.get("review_gaps"), list), f"{label} review_gaps contract missing"
    states = set(packet.get("evidence_states", {}).values())
    allowed = {"USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED", "NOT_CLAIMED"}
    assert states <= allowed, f"unknown {label} evidence state(s): {states - allowed}"


def main() -> None:
    result = _post("/assess", PAYLOAD)
    packet = result.get("canonical_evidence_packet")
    _assert_packet(packet, result, "/assess")

    workstation_request = {"assessment": PAYLOAD}
    workstation = _post("/workstation/analysis", workstation_request)
    ws_packet = workstation.get("canonical_evidence_packet")
    ws_assessment = workstation.get("assessment")
    assert isinstance(ws_assessment, dict), "workstation assessment payload missing"
    _assert_packet(ws_packet, ws_assessment, "/workstation/analysis")

    assert len(ws_packet["review_gaps"]) == len(packet["review_gaps"]), "assessment/workstation review gap drift"
    assert ws_packet["assessment"] == packet["assessment"], "assessment/workstation canonical assessment drift"
    print("[PHASE1-CANONICAL] /assess packet present")
    print(f"[PHASE1-CANONICAL] /assess packet version={packet['version']} status={packet['assessment']['final_status']} gaps={len(packet['review_gaps'])}")
    print(f"[PHASE1-CANONICAL] /workstation/analysis packet version={ws_packet['version']} gaps={len(ws_packet['review_gaps'])}")
    print("[PHASE1-CANONICAL] /assess ↔ /workstation/analysis packet parity PASS")


if __name__ == "__main__":
    main()
