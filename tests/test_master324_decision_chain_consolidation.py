from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_decision_center_has_single_canonical_chain():
    html = (ROOT / 'decision-center.html').read_text(encoding='utf-8')
    js = (ROOT / 'urbion_championship_decision_chain.js').read_text(encoding='utf-8')
    assert 'id="chain"' in html
    assert 'id="decision-chain"' not in html
    assert "document.getElementById('chain')||document.getElementById('decision-chain')" in js
    assert "panel.insertBefore(box" not in js


def test_decision_chain_updates_existing_dom_without_duplicate_mount():
    js = (ROOT / 'urbion_championship_decision_chain.js').read_text(encoding='utf-8')
    assert "var box=document.getElementById('chain')||document.getElementById('decision-chain')" in js
    assert "document.createElement('section')" not in js
    assert 'DECISION PATHWAY' not in js
