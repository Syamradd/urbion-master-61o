from pathlib import Path


def test_presentation_story_is_complete():
    text = Path('MASTER-197-CHAMPIONSHIP-PRESENTATION-READY.md').read_text(encoding='utf-8')
    for token in ('Input', 'Understand', 'Measure', 'Explain', 'Recommend', 'Compare', 'Review', 'Act'):
        assert token in text
    for token in ('spatial evidence', 'impact', 'policy/SDG', 'recommendation', 'What-If', 'Planner Review'):
        assert token in text


def test_presentation_preserves_integrity_rules():
    text = Path('MASTER-197-CHAMPIONSHIP-PRESENTATION-READY.md').read_text(encoding='utf-8')
    assert 'Never replace an unavailable source with a guessed value' in text
    assert 'Never present a planning-support recommendation as statutory approval' in text
