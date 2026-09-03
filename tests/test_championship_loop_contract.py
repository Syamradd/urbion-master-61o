from pathlib import Path


def test_championship_loop_prioritises_judge_visible_product_surfaces():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-141-CHAMPIONSHIP-LOOP.md').read_text(encoding='utf-8')
    for token in ('Dashboard command centre', 'Map Studio', 'Evidence/provenance', 'What-If', 'Decision Center', 'KM/OSC', 'Judge Mode'):
        assert token in text


def test_championship_loop_preserves_statutory_boundary():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-141-CHAMPIONSHIP-LOOP.md').read_text(encoding='utf-8')
    assert 'must not fabricate statutory controls' in text
    assert 'must not' in text
    assert 'unverified GIS geometry' in text
