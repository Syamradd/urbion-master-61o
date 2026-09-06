from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_visual_overhaul_v2_is_evidence_first():
    text = (ROOT / 'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    assert 'MAP EVIDENCE' in text
    assert 'iplan-current' in text
    assert 'GEOSERVER_WMS' in text
    assert 'ENVIRONMENT / HAZARD' in text
    assert 'TERRAIN / GEOLOGY' in text
    assert '400 m' in text and '800 m' in text and '1 km' in text and '1.5 km' in text
    assert 'SOURCE LAYERS' in text
    assert 'EVIDENCE BOUNDARY' in text
    assert 'fabricated' in text


def test_visual_overhaul_v2_reduces_duplicate_controls():
    text = (ROOT / 'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    assert "if(b.id==='ss-clear')b.style.display='none'" in text
    assert "const layerPanel=document.querySelector('#spatial-studio #ss-layers')" in text
