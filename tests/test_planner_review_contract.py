from pathlib import Path


def test_planner_review_is_live_and_same_origin():
    text = (Path(__file__).resolve().parents[1] / 'planner-review.html').read_text(encoding='utf-8')
    assert "const API=location.origin;" in text
    assert "fetch(API+'/health')" in text
    assert "fetch(API+'/decision-center')" in text
    assert "fetch(API+'/km/readiness'" in text


def test_planner_review_has_judge_pathway_and_boundary():
    text = (Path(__file__).resolve().parents[1] / 'planner-review.html').read_text(encoding='utf-8')
    for token in ('SITE ASSESSMENT', 'MAP STUDIO', 'WHAT-IF', 'DECISION CENTER', 'not statutory approval'):
        assert token in text
    assert 'urbion-master-61o.onrender.com' not in text
    assert 'urbion-master-61o-1.onrender.com' not in text
