"""Phase 1 copilot smoke: one route owner + canonical packet parity."""
from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.request

from landing_server import app

BASE_URL = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = {
    "assessment": {
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
}


def main() -> None:
    agent_source = (ROOT / "urbion_agent_api.py").read_text(encoding="utf-8")
    compatibility_source = (ROOT / "urbion_copilot_api.py").read_text(encoding="utf-8")
    assert agent_source.count('@router.post("/copilot/run")') == 1, "agent API must own exactly one /copilot/run route"
    assert '@router.post("/copilot/run")' not in compatibility_source, "compatibility copilot module must not register a duplicate route"
    assert "app.include_router(router)" not in compatibility_source, "compatibility copilot module must not mount a duplicate router"

    paths = (app.openapi() or {}).get("paths", {})
    assert "/copilot/run" in paths and "post" in paths["/copilot/run"], "runtime POST /copilot/run endpoint missing"

    request = urllib.request.Request(
        f"{BASE_URL}/copilot/run",
        data=json.dumps(PAYLOAD).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        assert response.status == 200, f"unexpected copilot status: {response.status}"
        result = json.loads(response.read().decode("utf-8"))

    packet = result.get("canonical_evidence_packet")
    assert isinstance(packet, dict), "copilot canonical_evidence_packet missing"
    assert packet.get("version") == "PHASE1.2", "copilot packet version drift"
    assert packet.get("statutory_verification") == "NOT_CLAIMED", "copilot statutory boundary drift"
    assert isinstance(packet.get("review_gaps"), list), "copilot review_gaps missing"
    explanation = result.get("explanation") or {}
    assert explanation.get("source") == "CANONICAL_EVIDENCE_PACKET", "copilot explanation source drift"
    assert explanation.get("review_gaps") == packet.get("review_gaps"), "copilot explanation review_gaps drift"
    assert explanation.get("statutory_verification") == packet.get("statutory_verification"), "copilot explanation statutory drift"
    assert result.get("generation_boundary", "").startswith("CANONICAL_PACKET_ONLY"), "copilot generation boundary drift"

    print("[PHASE1-COPILOT] single POST /copilot/run owner PASS")
    print(f"[PHASE1-COPILOT] packet version={packet['version']} gaps={len(packet['review_gaps'])}")
    print("[PHASE1-COPILOT] explanation ↔ canonical packet parity PASS")


if __name__ == "__main__":
    main()
