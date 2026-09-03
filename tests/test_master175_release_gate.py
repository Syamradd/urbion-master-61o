from pathlib import Path


def test_master175_judge_release_path():
    text = Path('MASTER-175-JUDGE-RELEASE-GATE.md').read_text(encoding='utf-8')
    for token in ['Site Assessment', 'Map Studio', 'Evidence', 'What-If', 'Decision Center', 'Planner Review', 'KM readiness']:
        assert token in text
    assert 'actual GitHub Actions success' in text
