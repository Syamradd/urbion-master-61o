from urbion_demo_scenarios import demo_scenarios
from urbion_evidence import summarise_sources, decision_trace


def test_demo_catalog_is_deterministic_and_unique():
    items = demo_scenarios()
    assert len(items) == 5
    ids = [x['id'] for x in items]
    assert len(ids) == len(set(ids))
    assert {'TOD-COMPLY','SHOP-COMPLY','SHOP-FAIL','OFFICE-REVIEW','NON-MBMB'} == set(ids)


def test_evidence_policy_never_promotes_unsafe_states():
    registry = [
        {'source':'A','status':'AVAILABLE','evidence':['PARCEL']},
        {'source':'B','status':'PLANNED','evidence':[]},
        {'source':'C','status':'QUERY_UNAVAILABLE','evidence':[]},
        {'source':'D','status':'DISCOVERY_COMPLETE','evidence':['ROUTE']},
    ]
    out = summarise_sources(registry)
    safe = {x['source'] for x in out['items'] if x['safe_for_decision']}
    assert safe == {'A'}


def test_decision_trace_always_closes_with_decision():
    trace = decision_trace('COMPLY', [{'rule_id':'R1'}], [{'rule_id':'R1'}], [{'rule_id':'R1','status':'COMPLY'}])
    assert trace[-1]['stage'] == 'DECISION'
    assert trace[-1]['status'] == 'COMPLY'
