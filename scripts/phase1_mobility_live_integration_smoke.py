"""Live integration contract for canonical mobility station evidence."""
from __future__ import annotations
import os, urllib.parse, urllib.request, json

base=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")
q=urllib.parse.urlencode({"site_lat":2.285,"site_lon":102.196,"state":"Melaka","limit":5})
with urllib.request.urlopen(f"{base}/mobility/stations?{q}",timeout=20) as r:
    assert r.status == 200
    payload=json.loads(r.read().decode())
assert payload.get("statutory_verification") == "NOT_CLAIMED"
assert payload.get("version")
assert "jps_rainfall" in payload and "air_quality" in payload
assert isinstance(payload.get("lcp_fields"),list)
print("[PHASE1] mobility live integration PASS")
