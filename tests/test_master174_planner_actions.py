from pathlib import Path


def test_master174_planner_review_exposes_actionable_km_state():
    text = (Path(__file__).resolve().parents[1] / 'planner-review.html').read_text(encoding='utf-8')
    for token in ['BLOCKERS / REVIEW ITEMS', 'NEXT EVIDENCE / ACTION', 'blockers', 'Resolve listed blockers', 'PBT-specific checklist confirmation']:
        assert token in text
    assert 'const API=location.origin' in text
    assert 'const esc=' in text
    assert 'not statutory approval' in text
