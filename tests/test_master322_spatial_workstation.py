from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_spatial_workstation_upgrade_is_served():
    server = read('championship_server.py')
    upgrade = read('urbion_spatial_workstation_upgrade.js')
    assert 'urbion_spatial_workstation_upgrade.js' in server
    for token in ['MAP FOCUS', 'PLANNING', 'RISK', 'ENVIRONMENT', 'COPY COORDINATES', 'active visual layers', 'OFF', 'EVIDENCE SNAPSHOT']:
        assert token in upgrade


def test_what_if_upgrade_is_actually_injected():
    server = read('championship_server.py')
    upgrade = read('urbion_what_if_upgrade.js')
    assert 'urbion_what_if_upgrade.js' in server
    assert 'def _what_if_page' in server
    assert '<script src="/urbion_what_if_upgrade.js"></script>' in server
    for token in ['EXPERIMENT PRESETS', 'ACCESS UPGRADE', 'STRONG ACCESS', 'BASELINE']:
        assert token in upgrade


def test_spatial_upgrade_is_loaded_after_spatial_studio():
    server = read('championship_server.py')
    assert server.index('urbion_championship_spatial_studio.js') < server.index('urbion_spatial_workstation_upgrade.js')


def test_spatial_upgrade_reacts_to_property_based_checkbox_changes():
    upgrade = read('urbion_spatial_workstation_upgrade.js')
    assert "addEventListener('change'" in upgrade
    assert "matches('input[data-i]')" in upgrade
    assert "MutationObserver(updateCount)" in upgrade


def test_spatial_evidence_snapshot_uses_live_assessment_state():
    upgrade = read('urbion_spatial_workstation_upgrade.js')
    assert 'renderEvidence(window.__urbionAssessment)' in upgrade
    assert 'retrieved_rules' in upgrade
    assert 'evidence_state' in upgrade
    assert "window.addEventListener('urbion:analysis'" in upgrade
