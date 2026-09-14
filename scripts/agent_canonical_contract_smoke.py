"""Validate /agents/run and /copilot/run use the same canonical packet contract."""
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
    result=post("/agents/run",{"assessment":PAYLOAD,"variants":[{"id":"OPTION-A","name":"Higher Intensity","overrides":{"plot_ratio":5.0}}]})
    packet=result.get("canonical_evidence_packet") or {}
    assert result.get("mode")=="BOUNDED_PLANNER_AGENT_WORKFLOW","agent mode mismatch"
    assert packet.get("convergence",{}).get("status")=="CANONICAL","agent packet not canonical"
    assert packet.get("statutory_verification")=="NOT_CLAIMED","statutory boundary changed"
    assert result.get("agents") is not None,"agent output missing"
    comparison=result.get("scenario_intelligence") or {}
    assert comparison.get("count")==1,"expected one scenario"
    assert (comparison.get("scenarios") or [{}])[0].get("canonical_evidence_packet"),"scenario packet missing"
    copilot=post("/copilot/run",{"assessment":PAYLOAD,"variants":[{"id":"OPTION-A","name":"Higher Intensity","overrides":{"plot_ratio":5.0}}]})
    cpacket=copilot.get("canonical_evidence_packet") or {}
    assert cpacket.get("convergence",{}).get("status")=="CANONICAL","copilot packet not canonical"
    assert cpacket.get("statutory_verification")=="NOT_CLAIMED","copilot statutory boundary changed"
    print("AGENT CANONICAL CONTRACT PASS")

if __name__=="__main__":main()
