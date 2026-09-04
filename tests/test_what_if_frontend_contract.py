from pathlib import Path


def test_what_if_uses_same_origin_and_current_release():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    assert 'const API' in text
    assert 'location.origin' in text
    assert "fetch(API+'/health')" in text
    assert "fetch(API+'/what-if'" in text
    assert 'PHASE-E.8' in text
    assert 'urbion-master-61o-1.onrender.com' not in text
    assert 'urbion-master-61o.onrender.com' not in text


def test_what_if_loads_shared_ui_controller():
    text = (Path(__file__).resolve().parents[1] / 'what-if.html').read_text(encoding='utf-8')
    assert '<script src="/urbion_ui.js"></script>' in text
