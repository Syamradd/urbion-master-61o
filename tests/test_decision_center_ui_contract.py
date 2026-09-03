from pathlib import Path


def test_decision_center_uses_same_origin_and_shared_ui():
    text = (Path(__file__).resolve().parents[1] / 'decision-center.html').read_text(encoding='utf-8')
    assert "const API=location.origin" in text
    assert "fetch(API+'/health')" in text
    assert '<script src="/urbion_ui.js"></script>' in text
    assert 'urbion-master-61o-1.onrender.com' not in text
    assert 'urbion-master-61o.onrender.com' not in text


def test_decision_center_keeps_judge_pathway_navigation():
    text = (Path(__file__).resolve().parents[1] / 'decision-center.html').read_text(encoding='utf-8')
    for token in ('SITE ASSESSMENT', 'MAP STUDIO', 'WHAT-IF', 'index.html', 'map-studio.html', 'what-if.html'):
        assert token in text
