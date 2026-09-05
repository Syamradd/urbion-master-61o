from pathlib import Path
from fastapi.testclient import TestClient
from server import app


def test_judge_run_has_complete_core_path():
    client=TestClient(app)
    health=client.get('/health').json()
    assert health['engine']=='URBION PHASE-E.8'
    judge=client.get('/judge-mode')
    assert judge.status_code==200
    body=judge.json()
    assert body['version']=='PHASE-E.8'
    assert body['scenario_count'] >= 1
    assert body['decision_boundary']
    assert body['statutory_verification']=='NOT_CLAIMED'


def test_judge_run_frontend_chain_is_present():
    for path in ('map-studio.html','what-if.html','decision-center.html','planner-review.html','lcp-intelligence.html'):
        assert Path(path).is_file(), path


def test_judge_mode_is_a_90_second_decision_story():
    text=Path('judge-mode.html').read_text(encoding='utf-8')
    for token in ('90-SECOND JUDGE STORY','EVIDENCE','SCORE','WHY','DECISION','REVIEW','ACTION','DECISION STORY','SCORE DRIVERS','REVIEW BEFORE ACTION','OPEN DECISION CENTER','RUN WHAT-IF','PLANNER REVIEW','NOT_CLAIMED','not approval probability','No decision has been fabricated'):
        assert token in text
    assert 'fetch(\'/judge-mode\'' in text
    assert 'cache:\'no-store\'' in text
    assert 'textContent' in text
    assert 'innerHTML' in text
