from urbion_evidence import summarise_sources, decision_trace

def test_source_states_are_explicit():
    out=summarise_sources([{'source':'A','status':'AVAILABLE','evidence':['SITE']},{'source':'B','status':'PLANNED','evidence':[]}])
    assert out['counts']['AVAILABLE']==1
    assert out['items'][0]['safe_for_decision'] is True
    assert out['items'][1]['safe_for_decision'] is False

def test_trace_contains_decision():
    out=decision_trace('COMPLY',[{'rule_id':'R1'}],[{'x':1}],[{'status':'COMPLY'}])
    assert out[-1]['stage']=='DECISION'
    assert out[-1]['status']=='COMPLY'
