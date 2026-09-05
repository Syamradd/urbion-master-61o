from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_run_once_shared_assessment_contract():
    sync = read('urbion_championship_input_sync.js')
    intel = read('urbion_championship_intelligence_upgrade.js')
    assert 'window.URBION.assess=sharedAssess' in sync
    assert 'cachedVersion===version&&cachedKey===key&&cached' in sync
    assert 'inflight&&inflight.version===version&&inflight.key===key' in sync
    assert "fetch('/assess'" in sync
    assert 'window.__urbionAssessment=data' in sync
    assert 'window.URBION?.assess' in intel


def test_workflow_matches_planning_journey():
    workflow = read('urbion_championship_workflow.js')
    for token in ['SITE', 'CONTEXT', 'EVIDENCE', 'ASSESS', 'WHAT-IF', 'DECIDE', 'DOCUMENT', 'RUN ONCE · EXPLORE MANY']:
        assert token in workflow


def test_spatial_workstation_is_map_and_evidence_oriented():
    spatial = read('urbion_spatial_workstation_upgrade.js')
    for token in ['MAP FOCUS', 'PLANNING', 'RISK', 'ENVIRONMENT', 'EVIDENCE SNAPSHOT', 'source context only']:
        assert token in spatial


def test_what_if_remains_new_computation_surface():
    what_if = read('urbion_what_if_upgrade.js')
    html = read('what-if.html')
    for token in ['EXPERIMENT PRESETS', 'ACCESS UPGRADE', 'STRONG ACCESS', 'BASELINE']:
        assert token in what_if
    assert "fetch(API+'/what-if'" in html
    assert 'score_delta' in html and 'indicator_deltas' in html


def test_decision_surface_preserves_explainability_and_boundary():
    decision = read('decision-center.html')
    engine = read('urbion_decision_center.py')
    for token in ['SCORE DRIVERS', 'WHY THIS DECISION', 'EVIDENCE COVERAGE', 'DECISION TRACE', 'REVIEW GAPS', 'NEXT ACTIONS']:
        assert token in decision
    assert 'PLANNER_DECISION_SUPPORT_ONLY' in engine
    assert 'NOT_CLAIMED' in engine


def test_judge_mode_stays_separate():
    server = read('championship_server.py')
    judge = read('judge-mode.html')
    assert '/judge-mode' in server
    assert 'SCORE DRIVERS' in judge
    assert 'Assessment dimensions' in judge
