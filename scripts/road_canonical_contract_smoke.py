"""Validate the road intelligence contract remains source-context and non-statutory."""
from __future__ import annotations
import json, os
from urllib.request import Request, urlopen

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
PAYLOAD = {"site_lat": 2.285, "site_lon": 102.196}


def main() -> None:
    req = Request(BASE + "/road-intelligence", data=json.dumps(PAYLOAD).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=60) as response:
        assert response.status == 200
        result = json.loads(response.read().decode())
    nearest = ((result.get("road_access") or {}).get("nearest_road") or {})
    assert nearest.get("evidence_status") in {"SOURCE_CONTEXT", "UNVERIFIED"}
    assert result.get("evidence_boundary")
    print("ROAD CANONICAL CONTRACT PASS")


if __name__ == "__main__":
    main()
