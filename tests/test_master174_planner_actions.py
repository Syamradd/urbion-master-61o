from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_master318_planner_review_exposes_evidence_to_action_workflow():
    text = (ROOT / 'planner-review.html').read_text(encoding='utf-8')
    for token in [
        'MASTER-318',
        'Evidence → Score → Why → Decision → Review → Action',
        'BLOCKERS / REVIEW ITEMS',
        'NEXT EVIDENCE / ACTION',
        'SCORE DRIVERS',
        'EVIDENCE STATE',
        'blockers',
        'review_gaps',
        'score_breakdown',
        'evidence_coverage',
        'next_actions',
        'Resolve listed blocker',
        'PBT-specific checklist confirmation',
    ]:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'const esc=' in text
    assert 'not statutory approval' in text
    assert 'no decision fabricated' in text
