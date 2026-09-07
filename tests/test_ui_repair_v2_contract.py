from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_repair_v2_is_wired_and_covers_interaction_guards():
    js = (ROOT / 'urbion_championship_ui_repair_v2.js').read_text(encoding='utf-8')
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    for token in (
        'STATE', 'PBT', 'DISTRICT', 'Guna Tanah 1', 'Guna Tanah 2', 'Guna Tanah 3',
        'CASE HISTORY', 'Selected site', 'STREET', 'SATELLITE', 'HYBRID',
        'What-If', 'urbion-theme', 'urbion-lang', 'resetCase', 'waitMap',
    ):
        assert token in js
    assert 'urbion_championship_ui_repair_v2.js' in server


def test_repair_v2_has_no_default_coordinate_or_ratio_literals():
    js = (ROOT / 'urbion_championship_ui_repair_v2.js').read_text(encoding='utf-8')
    assert 'value=\"2.285\"' not in js
    assert 'value=\"4.5\"' not in js
