from pathlib import Path


def test_lcp_judge_surface_exists_and_is_same_origin():
    text = Path('lcp-intelligence.html').read_text(encoding='utf-8')
    assert "const API=location.origin" in text
    assert "/lcp/intelligence" in text
    assert "Integrated LCP Intelligence" in text
    assert "SITE" in text and "SPATIAL" in text and "STATION" in text
    assert "POLICY / SDG" in text and "RECOMMENDATION" in text
    assert "const esc=" in text
    assert "replace(/[&<>\"']/g" in text
