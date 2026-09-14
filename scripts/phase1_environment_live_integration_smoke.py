import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000")


def main():
    query = urlencode({"site_lat": 2.285, "site_lon": 102.196, "state": "Melaka", "radius_m": 1000})
    with urlopen(f"{BASE}/environment/live?{query}", timeout=30) as response:
        assert response.status == 200
        payload = json.loads(response.read().decode("utf-8"))
    assert payload["decision_boundary"] == "ENVIRONMENTAL_SCREENING_SUPPORT"
    assert payload["statutory_verification"] == "NOT_CLAIMED"
    assert payload["live_query"]["provider"] == "PLANMalaysia DPFDN"
    assert payload["live_query"]["radius_m"] == 1000
    assert payload["summary"]["domain_count"] >= 1
    assert isinstance(payload["review_gaps"], list)
    print({"status": "PASS", "domains": payload["summary"]["domain_count"], "review_gaps": len(payload["review_gaps"])})


if __name__ == "__main__":
    main()
