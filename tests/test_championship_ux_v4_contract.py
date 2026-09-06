from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v4_is_wired_and_preserves_release_identity():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_ux_v4.js' in server
    assert 'app.state.frontend_release="MASTER-330"' in server


def test_v4_has_case_first_information_architecture():
    text = (ROOT / 'urbion_championship_ux_v4.js').read_text(encoding='utf-8')
    for label in ('01 · CASE','02 · EVIDENCE','03 · WHAT-IF','04 · DECISION','05 · OUTPUT'):
        assert label in text
    for control in ('STATE','LOCAL AUTHORITY / PBT','LAND USE CATEGORY','LAND USE ACTIVITY','DEVELOPMENT / PROPOSAL TYPE','PLOT RATIO'):
        assert control in text
    assert 'Melaka' in text and 'Selangor' in text and 'Johor' in text


def test_v4_removes_intrusive_floating_ui_and_site_popup():
    text = (ROOT / 'urbion_championship_ux_v4.js').read_text(encoding='utf-8')
    assert "['urbion-workstation-v2','urbion-decision-os']" in text
    assert 'URBION SCREENING SITE' in text
    assert 'map.closePopup()' in text
