from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workstation_ui_uses_canonical_scenario_override_shape():
    source = (ROOT / 'urbion_championship_workstation_v2.js').read_text(encoding='utf-8')
    assert "overrides:{plot_ratio:" in source
    assert "variants:[{id:'LOWER_DENSITY'" in source
    assert "plot_ratio:Math.max" in source
