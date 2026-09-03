from pathlib import Path


def test_what_if_exposes_baseline_variant_delta_and_reason():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    for token in ['BASELINE SCORE', 'BEST SCENARIO', 'DECISION DELTA', 'Why the decision moved', 'score_delta', 'best_candidate']:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'Decision support only' in text
    assert 'not be treated as statutory GIS evidence' in text


def test_what_if_escapes_remote_values():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    assert 'function esc(v)' in text
    assert 'esc(s.name)' in text
    assert 'esc(e.message)' in text
