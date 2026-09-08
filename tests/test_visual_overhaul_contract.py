from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_visual_overhaul_requirements_are_preserved_by_current_premium_surface():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    visual = (ROOT / 'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    cleanup = (ROOT / 'urbion_championship_visual_cleanup.js').read_text(encoding='utf-8')
    premium_v3 = (ROOT / 'urbion_championship_premium_v3.js').read_text(encoding='utf-8')
    premium_v4 = (ROOT / 'urbion_championship_premium_v4.js').read_text(encoding='utf-8')
    assert 'urbion_logo_dark.svg' in server
    assert 'urbion_logo_light.svg' in server
    assert 'image/svg+xml' in server
    for token in ('MAP EVIDENCE', '400 m', '800 m', '1 km', '1.5 km', 'PLANNING / LAND USE', 'ENVIRONMENT / HAZARD', 'MOBILITY'):
        assert token in visual or token in premium_v3 or token in premium_v4
    assert '#urbion-workstation-v2,#urbion-decision-os{display:none!important}' in visual
    for token in ('m.eachLayer', 'SATELLITE · ESRI', 'HYBRID · ESRI', 'TOPO · ESRI', 'LIGHT · CARTO', 'DARK · CARTO', 'TERRAIN · OTM', 'urbion-basemap-dock'):
        assert token in cleanup
    assert 'urbion_championship_premium_v3.js' in server
    assert 'urbion_championship_premium_v4.js' in server


def test_logo_lockups_are_scalable_svg():
    for name in ('urbion_logo_dark.svg', 'urbion_logo_light.svg'):
        text = (ROOT / name).read_text(encoding='utf-8')
        assert text.startswith('<svg ')
        assert 'URBION' in text
        assert 'HORIZON' in text
        assert 'SPATIAL' in text
