from pathlib import Path


def test_master179_release_path_is_locked():
    text = Path('MASTER-179-CHAMPIONSHIP-LOCK.md').read_text(encoding='utf-8')
    for token in ['Site Assessment', 'Map Studio', 'Evidence', 'What-If', 'Decision Center', 'Planner Review', 'KM/OSC']:
        assert token in text
    assert 'never statutory approval' in text
    assert 'full GitHub Actions regression gate' in text
