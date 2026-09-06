from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v4_is_wired_and_preserves_release_identity():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_ux_v4.js' in server
    assert 'app.state.frontend_release="MASTER-330"' in server


def test_v4_has_guided_case_information_architecture():
    text = (ROOT / 'urbion_championship_ux_v4.js').read_text(encoding='utf-8')
    for label in ('01 · GOVERNANCE','02 · LOCAL AUTHORITY','03 · LAND USE','04 · ACTIVITY','05 · PROPOSAL','06 · INTENSITY'):
        assert label in text
    for control in ('state','pbt','landuse','activity','development','ratio'):
        assert control in text
    assert 'READY TO ANALYSE' in text
    assert 'COMPLETE CASE TO RUN' in text


def test_v4_coordinates_navigation_and_button_hierarchy():
    text = (ROOT / 'urbion_championship_ux_v4.js').read_text(encoding='utf-8')
    for tab in ('command','evidence','scenarios','decision','judge'):
        assert 'data-view="'+tab+'"' in text
    for colour in ('--tab:#5ee7c2','--tab:#49c8e8','--tab:#f2c45c','--tab:#b08cff','--tab:#7faef8'):
        assert colour in text


def test_v4_keeps_intrusive_panels_out_of_the_main_workspace():
    text = (ROOT / 'urbion_championship_ux_v4.js').read_text(encoding='utf-8')
    assert "['urbion-workstation-v2','urbion-decision-os']" not in text
    assert 'CASE → EVIDENCE → OPTIONS → DECISION' in text
