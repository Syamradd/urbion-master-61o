from pathlib import Path


def test_master179_release_boundary():
    text = Path('MASTER-178-CHAMPIONSHIP-OPS.md').read_text(encoding='utf-8')
    assert 'statutory approval must never be implied' in text
    assert 'Only an actual successful full GitHub Actions regression run' in text
