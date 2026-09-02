EVIDENCE_STATES={'USER_PROVIDED','CALCULATED','SOURCE_CONTEXT','VERIFIED','UNVERIFIED'}
DECISION_EVIDENCE={'AVAILABLE','VERIFIED','REFERENCE_REGISTERED'}
SOURCE_CONTEXT={'LIVE_QUERY_AVAILABLE','LIVE_QUERY'}

def summarise_sources(registry):
 counts={};items=[]
 for source in registry or []:
  state=str(source.get('status','UNKNOWN')).upper();counts[state]=counts.get(state,0)+1
  items.append({'source':source.get('source'),'status':state,'evidence':source.get('evidence',[]),'safe_for_decision':state in DECISION_EVIDENCE,'source_context_available':state in SOURCE_CONTEXT})
 return {'counts':counts,'items':items,'verification_policy':'Only AVAILABLE, VERIFIED or REFERENCE_REGISTERED sources are eligible as decision evidence. LIVE_QUERY_AVAILABLE / LIVE_QUERY provides source context but still requires verification before decision use. PLANNED, QUERY_UNAVAILABLE, DISCOVERY_COMPLETE and NO_EVIDENCE remain disclosed gaps.','evidence_states':sorted(EVIDENCE_STATES)}

def decision_trace(final_status,retrieved_rules,applicability_results,compliance_results):
 return [{'stage':'SITE','status':'COMPLETE','detail':'Site identity and coordinates received'},{'stage':'SPATIAL','status':'COMPLETE','detail':'TOD distance and spatial band calculated'},{'stage':'POLICY','status':'COMPLETE' if retrieved_rules else 'GAP','detail':f'{len(retrieved_rules)} rule(s) retrieved'},{'stage':'APPLICABILITY','status':'COMPLETE' if applicability_results else 'GAP','detail':f'{len(applicability_results)} applicability result(s)'},{'stage':'COMPLIANCE','status':'COMPLETE' if compliance_results else 'GAP','detail':f'{len(compliance_results)} compliance result(s)'},{'stage':'DECISION','status':final_status,'detail':'Explainable decision produced by URBION'}]
