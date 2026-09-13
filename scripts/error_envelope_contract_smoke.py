"""Smoke-test the canonical decision error envelope."""
from __future__ import annotations
import json
import os
from urllib.request import Request, urlopen

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")

def main():
    req=Request(BASE+"/decision-center",data=json.dumps({}).encode(),headers={"Content-Type":"application/json"},method="POST")
    try:
        with urlopen(req,timeout=20) as response:
            status=response.status; payload=json.loads(response.read().decode())
    except Exception as exc:
        status=getattr(exc,"code",None)
        body=getattr(exc,"read",lambda:b"{}")()
        payload=json.loads(body.decode() or "{}")
    assert status==422, f"expected 422, got {status}"
    assert payload.get("error") is True, "canonical error flag missing"
    assert payload.get("version")=="URBION_ERROR_V1", "error version mismatch"
    assert payload.get("code")=="ASSESSMENT_INPUT_REQUIRED", "unexpected error code"
    assert payload.get("route")=="/decision-center", "route missing"
    assert payload.get("stage")=="DECISION_CENTER", "stage missing"
    assert payload.get("statutory_verification")=="NOT_CLAIMED", "statutory guard missing"
    assert payload.get("decision_authority")=="NONE", "authority boundary missing"
    print("CANONICAL ERROR ENVELOPE PASS")

if __name__=="__main__": main()
