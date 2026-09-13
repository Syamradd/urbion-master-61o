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


def post(path: str, payload: dict) -> dict:
    req = Request(BASE + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=30) as r:
        assert r.status == 200
        return json.load(r)


def main() -> None:
    payload = post("/assess", PAYLOAD)
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

    # The presentation decision flow consumes an assessment wrapper. The route
    # returns a decision-center envelope, so the canonical packet is accepted
    # either at the envelope level or inside the nested decision-center object.
    decision_payload = post("/decision-center", {"assessment": PAYLOAD})
    decision = decision_payload.get("decision_center") if isinstance(decision_payload.get("decision_center"), dict) else decision_payload
    assert isinstance(decision, dict), "decision center response missing"
    assert isinstance(decision.get("canonical_evidence_packet"), dict), "decision center canonical packet missing"
    assert isinstance(decision.get("development_impact"), dict), "decision center missing development impact"
    assert decision.get("canonical_evidence_packet", {}).get("version") == "PHASE1.2"
    print("DEVELOPMENT IMPACT CONVERGENCE PASS")
    print("domains: physical, social, economic")
    print("statutory_verification: NOT_CLAIMED")
    print("canonical_packet_version:", packet.get("version"))


if __name__ == "__main__":
    main()
