from pathlib import Path


def test_red_team_matrix_covers_high_risk_boundaries():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-145-RED-TEAM-MATRIX.md').read_text(encoding='utf-8')
    for token in ('Missing coordinates', 'Non-finite coordinates', 'Placeholder coordinates', 'Project-reference GIS conflict', 'Unsupported PBT rule', 'KM request', 'Stale deployment', 'Dead navigation'):
        assert token in text


def test_red_team_matrix_requires_bounded_decisions():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-145-RED-TEAM-MATRIX.md').read_text(encoding='utf-8')
    assert 'never approval' in text
    assert 'never fabricate' in text
    assert 'traceable' in text
