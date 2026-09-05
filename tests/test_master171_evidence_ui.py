from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_decision_center_surfaces_evidence_and_boundary():
    text = (ROOT / 'decision-center.html').read_text(encoding='utf-8')
    for token in ['DECISION WORKFLOW · LIVE', 'renderDecision(j)', 'renderChain(j)', 'j.decision_trace', 'j.spatial_intelligence', 'j.review_gaps', 'j.next_actions', 'EVIDENCE COVERAGE', 'PLANNER DECISION SUPPORT ONLY', 'Statutory approval or compliance is not claimed.', 'No decision output was fabricated.']:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'urbion-master-61o.onrender.com' not in text
    assert 'urbion-master-61o-1.onrender.com' not in text


def test_decision_center_escapes_remote_values():
    text = (ROOT / 'decision-center.html').read_text(encoding='utf-8')
    assert 'function esc(v)' in text
    assert 'replace(' in text
    assert '&amp;' in text and '&#39;' in text
