from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_repair_v2_has_no_unbounded_root_mutation_observer():
    js = (ROOT / 'urbion_championship_ui_repair_v2.js').read_text(encoding='utf-8')
    assert 'MutationObserver' not in js
    assert 'setInterval' not in js
    assert 'waitMap' in js
    assert 'CASE HISTORY' in js
    assert 'resetCase' in js


def test_input_neutralizer_does_not_treat_stale_active_marker_as_case_state():
    js = (ROOT / 'urbion_championship_input_neutralizer.js').read_text(encoding='utf-8')
    assert 'localStorage.getItem(\'urbion-case-active\')' not in js
    assert 'Select state' in js
    assert 'Select PBT' in js
    assert 'Select district' in js


def test_runtime_enforcer_is_scoped_to_readiness_text_only():
    js = (ROOT / 'urbion_championship_final_runtime_enforcer.js').read_text(encoding='utf-8')
    assert 'fcc-ready-value' in js
    assert 'Object.getOwnPropertyDescriptor(Node.prototype,\'textContent\')' in js
