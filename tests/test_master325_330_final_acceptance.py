from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_master325_decision_trace_is_live_and_guardrailed():
    html = read('decision-center.html')
    assert 'DECISION TRACE' in html
    assert 'renderTrace(j.decision_trace)' in html
    assert 'Evidence gaps remain disclosed' in html
    assert 'Statutory approval or compliance is not claimed' in html


def test_master326_spatial_chain_is_wired_without_false_statutory_claims():
    server = read('championship_server.py')
    bridge = read('urbion_spatial_implication_bridge.js')
    assert 'urbion_championship_spatial_studio.js' in server
    assert 'urbion_spatial_workstation_upgrade.js' in server
    assert 'urbion_spatial_implication_bridge.js' in server
    assert 'not statutory determinations' in bridge
    assert 'source or authority verification' in bridge


def test_master327_what_if_exposes_real_deltas_and_same_engine_path():
    html = read('what-if.html')
    assert "fetch(API+'/what-if'" in html
    assert 'baseline_score' in html
    assert 'best_candidate' in html
    assert 'score_delta' in html
    assert 'input_changes' in html
    assert 'indicator_deltas' in html
    assert 'Decision support only' in html
    assert 'not walking-network' in html


def test_master328_judge_mode_keeps_decision_boundary_explicit():
    decision = read('urbion_decision_center.py')
    assert 'PLANNER_DECISION_SUPPORT_ONLY' in decision
    assert 'NOT_CLAIMED' in decision
    assert 'approval probability' not in decision.lower()


def test_master329_frontend_asset_registry_has_no_duplicate_chain_asset():
    server = read('championship_server.py')
    registry = server.split('ALLOWED_ASSETS = {', 1)[1].split('}', 1)[0]
    assets = re.findall(r'"([^"]+\.js)"', registry)
    assert len(assets) == len(set(assets))
    assert assets.count('urbion_championship_decision_chain.js') == 1


def test_master330_release_lock_and_workflow_gate():
    server = read('championship_server.py')
    workflow = read('.github/workflows/urbion-ci.yml')
    assert 'app.state.frontend_release="MASTER-330"' in server
    assert 'tests/test_master324_decision_chain_consolidation.py' in workflow
    assert 'tests/test_master325_330_final_acceptance.py' in workflow
    assert 'full-regression' in workflow
    assert 'python -m pytest -q' in workflow
