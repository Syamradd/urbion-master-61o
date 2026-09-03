from pathlib import Path


def test_championship_loop_is_complete():
    text = Path('MASTER-177-CHAMPIONSHIP-READINESS.md').read_text(encoding='utf-8')
    for token in ['Site', 'Spatial', 'Policy', 'Evidence', 'Compliance', 'What-If', 'Decision', 'Planner Review', 'KM/OSC', 'Actual GitHub Actions success']:
        assert token in text
    assert 'statutory approval' in text
