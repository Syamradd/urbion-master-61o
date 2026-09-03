from pathlib import Path


def test_map_studio_exposes_judge_controls():
    text = (Path(__file__).resolve().parents[1] / 'map-studio.html').read_text(encoding='utf-8')
    for token in ['legendBtn', 'share', 'navigator.clipboard', 'URLSearchParams', 'measureDist', 'measureArea']:
        assert token in text


def test_map_studio_preserves_same_origin_and_evidence_boundary():
    text = (Path(__file__).resolve().parents[1] / 'map-studio.html').read_text(encoding='utf-8')
    assert 'const API=location.origin' in text
    assert 'SOURCE_CONTEXT' in text
    assert 'not statutory verification' in text
    assert 'urbion-master-61o.onrender.com' not in text
    assert 'urbion-master-61o-1.onrender.com' not in text
