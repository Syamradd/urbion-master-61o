from pathlib import Path


def test_what_if_exposes_full_decision_delta_surface():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    for token in ['BASELINE SCORE', 'BEST SCENARIO', 'DECISION DELTA', 'decision_delta', 'input_changes', 'indicator_deltas', 'INPUT CHANGES', 'INDICATOR DELTAS', 'WHY', 'RECOMMENDATION', 'best_candidate']:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'Decision support only' in text
    assert 'not walking-network' in text


def test_what_if_escapes_remote_values():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    assert 'const esc=' in text
    assert 'esc(s.name)' in text
    assert 'esc(e.message)' in text
