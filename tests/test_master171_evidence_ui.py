from pathlib import Path


def test_decision_center_surfaces_evidence_and_boundary():
    text = (Path(__file__).resolve().parents[1] / 'decision-center.html').read_text(encoding='utf-8')
    for token in ['EVIDENCE · PROVENANCE', 'evidence_state', 'decision_trace', 'Source summary', 'NOT STATUTORY APPROVAL', 'Statutory verification is not claimed']:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'urbion-master-61o.onrender.com' not in text
    assert 'urbion-master-61o-1.onrender.com' not in text


def test_decision_center_escapes_remote_values():
    text = (Path(__file__).resolve().parents[1] / 'decision-center.html').read_text(encoding='utf-8')
    assert 'function esc(v)' in text
    assert "replace(/[&<>\\\"']/g" in text
