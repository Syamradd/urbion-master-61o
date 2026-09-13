"""Validate that bounded copilot outputs converge into the canonical packet."""
from __future__ import annotations
import json, os
from urllib.request import Request, urlopen

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")
PAYLOAD={
    "site_lat":2.285,"site_lon":102.196,"tod_lat":2.286,"tod_lon":102.196,
    "plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"TOD Development / Mixed Use",
    "development_class":"Mixed Use","state":"Melaka","district":"Melaka Tengah",
    "pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":""
}

def post(path,payload):
    req=Request(BASE+path,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=60) as response:return json.loads(response.read().decode())

def main():
    result=post("/copilot/run",{
        "assessment":PAYLOAD,
        "variants":[{"id":"OPTION-A","name":"Higher Intensity","overrides":{"plot_ratio":5.0}}],
    })
    packet=result.get("canonical_evidence_packet") or {}
    assert packet.get("convergence",{}).get("status")=="CANONICAL","canonical convergence status missing"
    for key in ("spatial","development_impact","policy_graph"):
        assert key in (packet.get("evidence") or {}),f"canonical packet missing evidence.{key}"
    assert "what_if" in packet and "decision_center" in packet,"canonical packet missing downstream decision surfaces"
    scenarios=packet.get("what_if",{}).get("scenario_packets",{}) or packet.get("what_if",{}).get("scenario_packets",{})
    comparison=result.get("scenario_intelligence") or {}
    assert comparison.get("count")==1,"expected one What-If scenario"
    assert "canonical_evidence_packet" in (comparison.get("scenarios") or [{}])[0],"scenario packet missing"
    assert result.get("statutory_verification")=="NOT_CLAIMED","statutory boundary changed"
    print("CANONICAL CONVERGENCE PASS")

if __name__=="__main__":main()
