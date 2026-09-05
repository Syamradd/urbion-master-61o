from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_d8_workflow_is_canonical_and_run_once_oriented():
    text = read('urbion_championship_workflow.js')
    assert "const steps=[['01','SITE','Define'],['02','MAP','Context'],['03','ANALYSE','Run'],['04','WHY','Explain'],['05','WHAT-IF','Test'],['06','DECISION','Decide'],['07','ACTION','Next']]" in text
    assert "const targets=['#lat','#spatial-studio','#intel-upgrade','.iu-score','#intel-upgrade','#intel-upgrade','.judge']" in text
    assert 'RUN ONCE · EXPLORE MANY' in text
    assert 'urbion:analysis' in text
    assert 'urbion:site-change' in text


def test_d8_shared_assessment_state_is_payload_keyed():
    text = read('urbion_championship_input_sync.js')
    assert 'payloadKey=payload=>JSON.stringify(payload)' in text
    assert 'cachedVersion===version&&cachedKey===key&&cached' in text
    assert 'inflight&&inflight.version===version&&inflight.key===key' in text
    assert 'window.fetch=' not in text


def test_d9_decision_surface_is_consolidated_and_guardrailed():
    html = read('decision-center.html')
    chain = read('urbion_championship_decision_chain.js')
    legacy = read('urbion_championship_decision_layer.js')
    assert html.count('id="chain"') == 1
    assert 'id="decision-chain"' not in html
    assert "document.getElementById('chain')||document.getElementById('decision-chain')" in chain
    assert 'panel.insertBefore(box' not in chain
    assert 'intel-upgrade' in legacy
    assert 'PLANNER DECISION SUPPORT ONLY' in html


def test_d9_production_entrypoint_preserves_single_frontend_path():
    server = read('championship_server.py')
    assert 'app.state.frontend_entrypoint="championship.html"' in server
    assert 'Cache-Control' in server
    assert 'urbion_championship_input_sync.js' in server
    assert 'urbion_championship_intelligence_upgrade.js' in server
    assert 'urbion_championship_workflow.js' in server


def test_d9_spatial_evidence_is_not_presented_as_statutory_determination():
    bridge = read('urbion_spatial_implication_bridge.js')
    spatial = read('urbion_championship_spatial_studio.js')
    assert 'not statutory determinations' in bridge
    assert 'source or authority verification' in bridge
    assert 'Haversine' in spatial
    assert 'not walking-network' in spatial
    assert 'EVIDENCE / PROVENANCE' in spatial
