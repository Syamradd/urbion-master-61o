from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_spatial_implication_bridge_is_wired_after_map_workstation():
    server = read('championship_server.py')
    bridge = read('urbion_spatial_implication_bridge.js')
    assert 'urbion_spatial_implication_bridge.js' in server
    assert server.index('urbion_spatial_workstation_upgrade.js') < server.index('urbion_spatial_implication_bridge.js')
    for token in ['SPATIAL → PLANNING IMPLICATION', 'PLANNING', 'RISK', 'ENVIRONMENT', 'not statutory determinations', 'source or authority verification']:
        assert token in bridge


def test_spatial_bridge_only_uses_active_declared_layers():
    bridge = read('urbion_spatial_implication_bridge.js')
    assert '#ss-layers input[data-i]:checked' in bridge
    assert 'planner prompts derived from the active layer names' in bridge or 'Implications are planner prompts' in bridge
    assert 'NO ACTIVE GROUP' in bridge
