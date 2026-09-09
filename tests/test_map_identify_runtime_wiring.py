from pathlib import Path


SERVER = Path('championship_server.py').read_text(encoding='utf-8')
RUNTIME = Path('urbion_map_identify_runtime.js').read_text(encoding='utf-8')


def test_identify_runtime_is_allowlisted_and_loaded_by_production_root():
    assert '"urbion_map_identify_runtime.js"' in SERVER
    assert '<script src="/urbion_map_identify_runtime.js"></script>' in SERVER


def test_identify_runtime_contains_live_query_and_conservative_evidence_guards():
    assert "'/spatial/site-context?'" in RUNTIME
    assert "credentials:'same-origin'" in RUNTIME
    assert "'LIVE_QUERY'" in RUNTIME
    assert "decision_safe:false" in RUNTIME
    assert "rule_binding_required:true" in RUNTIME
    assert "statutory_approval_claim:false" in RUNTIME
    assert "'/identify?'" not in RUNTIME


def test_identify_runtime_surfaces_multiple_layer_results_and_selection():
    for token in ('lastResults', 'FEATURE', 'data-umi-result', 'renderSelected', 'results.length'):
        assert token in RUNTIME
