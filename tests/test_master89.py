from pathlib import Path

def test_intervention_workspace_calls_what_if():
    html=Path('intervention-workspace.html').read_text(encoding='utf-8')
    assert '/what-if' in html
    assert 'Fix walkway' in html
    assert 'RUN ALL INTERVENTIONS' in html
    assert 'COMPLIANCE' in html
