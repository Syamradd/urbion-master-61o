from urbion_release_contract import REQUIRED_LCP_KEYS, REQUIRED_TRACE, audit_lcp_contract

def _minimal_lcp(trace):
    return {"version":"MASTER-199","project":"URBION HORIZON","statutory_verification":"NOT_CLAIMED","decision_boundary":"INTEGRATED_LCP_PLANNING_SUPPORT","trace":trace,"evidence_summary":{"counts":{},"review_gap_count":0},"review_gaps":[],"site":{},"assessment":{},"spatial_intelligence":{},"station_intelligence":{},"development_impact":{},"policy_graph":{},"recommendations":{},"what_if":{},"decision_center":{},"km_readiness":{}}

def test_master237_championship_contract_locks_integrated_trace():
    trace="SITE → RADIUS → SPATIAL → ENVIRONMENT/HAZARD → ENVIRONMENT IMPLICATIONS → STATIONS/AGENCIES → IMPACT → GUIDELINES/POLICY → COMPLIANCE → RECOMMENDATION → RECOMMENDATION GROUNDING → WHAT-IF → DECISION CENTER → LCP/PLANNER REVIEW"
    audit=audit_lcp_contract(_minimal_lcp(trace))
    assert audit["status"]=="PASS"
    assert audit["version"]=="MASTER-199"
    assert all(token in trace for token in REQUIRED_TRACE)

def test_master237_championship_contract_rejects_wrong_boundary():
    result=_minimal_lcp("SITE SPATIAL STATION IMPACT RECOMMENDATION WHAT-IF DECISION CENTER LCP/PLANNER REVIEW POLICY/SDG")
    result["decision_boundary"]="STATUTORY_APPROVAL"
    assert audit_lcp_contract(result)["status"]=="FAIL"
    assert "recommendations" in REQUIRED_LCP_KEYS
