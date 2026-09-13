"""Phase 1 integration smoke for the canonical evidence envelope.

The check uses the running local FastAPI server and does not mutate planning
calculations. It verifies that the presentation gateway exposes the same
assessment result together with the canonical evidence packet contract.
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


def _post(path: str) -> dict:
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(PAYLOAD).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 200, f"unexpected {path} status: {response.status}"
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    result = _post("/assess")
    packet = result.get("canonical_evidence_packet")
    assert isinstance(packet, dict), "canonical_evidence_packet missing from /assess"
    assert packet.get("version") == "PHASE1.2", "unexpected packet version"
    assert packet.get("assessment", {}).get("final_status") == result.get("final_status"), "packet/result status mismatch"
    assert packet.get("site", {}).get("latitude") == result.get("site", {}).get("latitude"), "packet/result site mismatch"
    assert packet.get("statutory_verification") == "NOT_CLAIMED", "statutory verification boundary changed"
    assert "review_gaps" in packet and isinstance(packet["review_gaps"], list), "review_gaps contract missing"
    states = set(packet.get("evidence_states", {}).values())
    allowed = {"USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED", "NOT_CLAIMED"}
    assert states <= allowed, f"unknown evidence state(s): {states - allowed}"

    workstation = _post("/workstation/analysis")
    ws_packet = workstation.get("canonical_evidence_packet")
    assert isinstance(ws_packet, dict), "canonical_evidence_packet missing from /workstation/analysis"
    assert ws_packet.get("version") == "PHASE1.2", "workspace packet version mismatch"
    assert isinstance(ws_packet.get("review_gaps"), list), "workspace review_gaps missing"
    assert ws_packet.get("statutory_verification") == "NOT_CLAIMED", "workspace statutory boundary changed"
    assert ws_packet.get("assessment", {}).get("final_status") == workstation.get("final_status"), "workspace packet/result mismatch"

    assert len(ws_packet["review_gaps"]) == len(packet["review_gaps"]), "assessment/workstation review gap drift"
    print("[PHASE1-CANONICAL] /assess packet present")
    print(f"[PHASE1-CANONICAL] /assess packet version={packet['version']} status={packet['assessment']['final_status']} gaps={len(packet['review_gaps'])}")
    print(f"[PHASE1-CANONICAL] /workstation/analysis packet version={ws_packet['version']} gaps={len(ws_packet['review_gaps'])}")
    print("[PHASE1-CANONICAL] /assess ↔ /workstation/analysis packet parity PASS")


if __name__ == "__main__":
    main()
