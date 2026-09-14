import json
import os
import urllib.request

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000")

PAYLOAD = {
    "site_lat": 2.285,
    "site_lon": 102.196,
    "tod_lat": 2.287,
    "tod_lon": 102.198,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
    "lot_no": "",
    "shop_frontage_verified": False,
    "shop_office_verified": False,
}


def main() -> None:
    request = urllib.request.Request(
        BASE + "/assess",
        data=json.dumps(PAYLOAD).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 200
        payload = json.loads(response.read().decode("utf-8"))

    packet = payload.get("canonical_evidence_packet")
    assert isinstance(packet, dict), "Canonical evidence packet missing"
    assert packet.get("version") == "PHASE1.2"
    gaps = packet.get("review_gaps") or []
    rules = packet.get("assessment", {}).get("retrieved_rules") or []
    expected_review = sum(1 for rule in rules if str(rule.get("verification_status", "")).upper() == "REQUIRES_REVIEW")
    assert expected_review > 0, "Fixture should expose review-bound rule provenance"
    assert len(gaps) >= expected_review
    assert packet.get("statutory_verification") == "NOT_CLAIMED"
    assert payload.get("final_status") == packet.get("assessment", {}).get("final_status")

    print({"status": "PASS", "rules": len(rules), "review_gaps": len(gaps), "packet_version": packet.get("version")})


if __name__ == "__main__":
    main()
