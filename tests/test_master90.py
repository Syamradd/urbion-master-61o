from pathlib import Path

def test_evidence_workspace_is_explicitly_gated():
    html=Path('evidence-workspace.html').read_text(encoding='utf-8')
    assert '/evidence-summary' in html
    assert 'QUERY_UNAVAILABLE' in html
    assert 'DISCOVERY_COMPLETE' in html
    assert 'must not be presented as verified site evidence' in html
