from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ux_v3_has_professional_case_hierarchy():
    text = (ROOT / 'urbion_championship_ux_v3.js').read_text(encoding='utf-8')
    assert '01 · START / CASE' in text
    assert '02 · MAP / EVIDENCE' in text
    assert '03 · WHAT-IF' in text
    assert '04 · DECISION / LCP' in text
    assert 'Land use category' in text
    assert 'Land use activity' in text
    assert 'Development / proposal type' in text
    assert 'W.P. Kuala Lumpur' in text
    assert 'Majlis Bandaraya Shah Alam' in text
    assert 'Majlis Bandaraya Melaka Bersejarah' in text


def test_ux_v3_binds_real_layer_opacity_and_removes_floating_panels():
    text = (ROOT / 'urbion_championship_ux_v3.js').read_text(encoding='utf-8')
    assert '_urbionEvidenceId===id' in text
    assert 'setOpacity?.(v)' in text
    assert "['urbion-workstation-v2','urbion-decision-os']" in text
    assert "input.ss-opacity" in text


def test_ux_v3_is_wired_before_release_identity_guard():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_ux_v3.js' in server
    assert 'app.state.frontend_release="MASTER-330"' in server
