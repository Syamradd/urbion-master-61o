from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_visual_overhaul_scope_is_bounded():
    text = (ROOT / 'BATCH_VISUAL_OVERHAUL.md').read_text(encoding='utf-8')
    assert 'No fabricated zoning, flood or environmental boundaries.' in text
    assert 'No change to statutory decision authority.' in text
    assert 'No automatic production deployment.' in text
