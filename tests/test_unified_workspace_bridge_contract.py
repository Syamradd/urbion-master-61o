from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_unified_workspace_bridge_is_wired_without_new_popup_surface():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    bridge = (ROOT / 'urbion_championship_unified_bridge.js').read_text(encoding='utf-8')
    assert 'urbion_championship_unified_bridge.js' in server
    assert 'urbion:inputs-change' in bridge
    assert 'urbion:lot-resolved' in bridge
    assert 'urbion:spatial-context-ready' in bridge
    assert 'urbion:analysis' in bridge
    assert 'ux5-readiness-note' in bridge
    assert 'ux5-next-title' in bridge
    assert 'L.geoJSON' in bridge
    assert 'window.__URBION_UNIFIED_STATE' in bridge
    assert 'alert(' not in bridge
    assert 'window.open(' not in bridge


def test_unified_workspace_keeps_legacy_surfaces_out_of_visual_hierarchy():
    visual = (ROOT / 'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    assert '#urbion-workstation-v2,#urbion-decision-os{display:none!important}' in visual
