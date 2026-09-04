from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_shared_assessment_state_contract():
    text = read('urbion_championship_input_sync.js')
    assert 'window.URBION' in text
    assert 'getAssessmentPayload' in text
    assert 'window.URBION.assess=sharedAssess' in text
    assert 'assessment-invalidated' in text
    assert "nativeFetch('/assess'" in text
    assert "method:'POST'" in text
    assert 'nativeFetch' in text
    assert 'cachedVersion' in text
    assert 'cachedKey' in text
    assert 'payloadKey=payload=>JSON.stringify(payload)' in text
    assert 'cachedVersion===version&&cachedKey===key' in text
    assert 'inflight.version===version&&inflight.key===key' in text
    assert 'requestVersion=version' in text
    assert 'requestKey=key' in text
    assert 'location.origin' not in text
    assert 'window.fetch=' not in text


def test_decision_layer_consumes_shared_assessment():
    text = read('urbion_championship_decision_layer.js')
    assert 'window.URBION?.getAssessmentPayload' in text
    assert 'window.URBION?.assess' in text


def test_intelligence_layer_consumes_shared_assessment():
    text = read('urbion_championship_intelligence_upgrade.js')
    assert 'window.URBION?.getAssessmentPayload' in text
    assert 'window.URBION?.assess' in text
    assert 'async function assess(extra={})' in text
    assert 'return window.URBION.assess(extra)' in text


def test_championship_wires_shared_state_after_decision_layers():
    text = read('championship_server.py')
    assert 'urbion_championship_input_sync.js' in text
    assert 'urbion_championship_decision_layer.js' in text
    assert 'urbion_championship_intelligence_upgrade.js' in text
