from pathlib import Path


def test_release_candidate_has_complete_judge_story():
    text=Path('MASTER-194-CHAMPIONSHIP-RELEASE-CANDIDATE.md').read_text(encoding='utf-8')
    for token in ('Spatial context','Live station','Physical / social / economic','Policy and SDG','Recommendation','What-If','KM/OSC','Evidence gaps','parallel CI matrix','full regression'):
        assert token in text


def test_release_candidate_preserves_boundary():
    text=Path('MASTER-194-CHAMPIONSHIP-RELEASE-CANDIDATE.md').read_text(encoding='utf-8')
    assert 'does not grant, predict or replace statutory planning approval' in text
