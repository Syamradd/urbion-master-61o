from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_visual_overhaul_assets_and_routes_are_wired():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    visual = (ROOT / 'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    cleanup = (ROOT / 'urbion_championship_visual_cleanup.js').read_text(encoding='utf-8')
    assert 'urbion_championship_visual_cleanup.js' in server
    assert 'urbion_championship_visual_overhaul.js' in server
    assert 'urbion_logo_dark.svg' in server
    assert 'urbion_logo_light.svg' in server
    assert 'image/svg+xml' in server
    assert 'MAP EVIDENCE OVERLAYS' in visual
    assert '400 m screening catchment' in visual
    assert '800 m screening catchment' in visual
    assert '1 km context ring' in visual
    assert '1.5 km context ring' in visual
    assert 'ZONING / LAND USE' in visual
    assert 'ENVIRONMENT' in visual
    assert 'MOBILITY' in visual
    assert '#urbion-workstation-v2,#urbion-decision-os{display:none!important}' in visual
    assert 'm.eachLayer' in cleanup


def test_logo_lockups_are_scalable_svg():
    for name in ('urbion_logo_dark.svg', 'urbion_logo_light.svg'):
        text = (ROOT / name).read_text(encoding='utf-8')
        assert text.startswith('<svg ')
        assert 'URBION' in text
        assert 'HORIZON' in text
        assert 'SPATIAL' in text
