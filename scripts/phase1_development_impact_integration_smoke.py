"""Canonical Phase 1 development-impact convergence smoke."""
from __future__ import annotations
import json
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8000"
PAYLOAD = {
    "site_lat": 2.285,
    "site_lon": 102.196,
    "tod_lat": 2.286,
    "tod_lon": 102.196,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
    "lot_no": "",
}

def main() -> None:
    req = Request(BASE + "/assess", data=json.dumps(PAYLOAD).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=30) as r:
        assert r.status == 200
        payload = json.load(r)
    packet = payload.get("canonical_evidence_packet")
    assert isinstance(packet, dict), "canonical_evidence_packet missing"
    assert packet.get("version") == "PHASE1.2"
    impact = packet.get("evidence", {}).get("development_impact")
    assert isinstance(impact, dict), "development impact missing from canonical evidence packet"
    assert impact.get("decision_boundary") == "PLANNING_SCREENING_ONLY"
    assert impact.get("statutory_verification") == "NOT_CLAIMED"
    assert set((impact.get("impacts") or {}).keys()) == {"physical", "social", "economic"}
    assert len(impact.get("review_gaps") or []) >= 1, "missing impact inputs must remain explicit review gaps"
    assert isinstance(payload.get("development_impact"), dict), "top-level development impact missing"

    dreq = Request(BASE + "/decision-center", data=json.dumps(PAYLOAD).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(dreq, timeout=30) as r:
        assert r.status == 200
        decision = json.load(r)
    assert isinstance(decision.get("canonical_evidence_packet"), dict)
    assert isinstance(decision.get("development_impact"), dict), "decision center missing development impact"
    print("DEVELOPMENT IMPACT CONVERGENCE PASS")
    print("domains: physical, social, economic")
    print("statutory_verification: NOT_CLAIMED")
    print("canonical_packet_version:", packet.get("version"))

if __name__ == "__main__":
    main()
