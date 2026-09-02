from pathlib import Path

def test_decision_center_wires_both_workspaces():
    html = Path('decision-center.html').read_text(encoding='utf-8')
    assert 'index.html' in html
    assert 'what-if.html' in html
    assert '/health' in html
    assert 'SITE ASSESSMENT' in html
    assert 'WHAT-IF' in html
