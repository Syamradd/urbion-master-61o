from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_v3_popup_suppression_and_layer_guard():
    text=(ROOT/'urbion_championship_ux_v3.js').read_text(encoding='utf-8')
    assert 'closeMapPopups' in text
    assert '_urbionEvidenceId===id' in text
