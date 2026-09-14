"""Validate the public /what-if route returns canonical evidence packets."""
from __future__ import annotations
import json
import os
from urllib.request import Request, urlopen

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")
PAYLOAD={
    "baseline":{
        "site_lat":2.285,"site_lon":102.196,"tod_lat":2.286,"tod_lon":102.196,
        "plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"TOD Development / Mixed Use",
        "development_class":"Mixed Use","state":"Melaka","district":"Melaka Tengah",
        "pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":""
    },
    "variants":[{"id":"OPTION-A","name":"Higher Intensity","overrides":{"plot_ratio":5.0}}]
}

def main():
    req=Request(BASE+"/what-if",data=json.dumps(PAYLOAD).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=60) as response:
        assert response.status==200, f"expected 200, got {response.status}"
        result=json.loads(response.read().decode())
    packet=result.get("canonical_evidence_packet") or result.get("baseline_canonical_evidence_packet") or {}
    assert isinstance(packet,dict),"baseline canonical packet missing"
    assert packet.get("statutory_verification")=="NOT_CLAIMED", "statutory boundary changed"
    scenarios=result.get("scenarios") or []
    assert len(scenarios)==1,"expected one What-If scenario"
    scenario_packet=scenarios[0].get("canonical_evidence_packet") or {}
    assert isinstance(scenario_packet,dict),"scenario canonical packet missing"
    for key in ("spatial","development_impact","policy_graph"):
        assert key in (scenario_packet.get("evidence") or {}), f"scenario packet missing evidence.{key}"
    print("WHAT-IF CANONICAL CONTRACT PASS")

if __name__=="__main__":main()
