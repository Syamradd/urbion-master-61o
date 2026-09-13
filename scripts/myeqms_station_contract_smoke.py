import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000")


def main():
    query = urlencode({"site_lat": 2.285, "site_lon": 102.196, "state": "Melaka", "limit": 10})
    with urlopen(f"{BASE}/mobility/stations?{query}", timeout=30) as response:
        assert response.status == 200
        payload = json.loads(response.read().decode("utf-8"))
    eqmp = payload.get("eqmp_water") or {}
    assert eqmp.get("provider") == "JAS MyEQMS / EQMP"
    assert eqmp.get("dataset") == "Stesen_EQMP"
    assert eqmp.get("evidence") == "SOURCE_CONTEXT"
    assert payload.get("statutory_verification") == "NOT_CLAIMED"
    assert isinstance(eqmp.get("stations"), list)
    for station in eqmp.get("stations", []):
        assert "distance_m" in station
        assert "latitude" in station and "longitude" in station
    print({"status": "PASS", "provider": eqmp.get("provider"), "stations": len(eqmp.get("stations", [])), "source_state": eqmp.get("status")})


if __name__ == "__main__":
    main()
