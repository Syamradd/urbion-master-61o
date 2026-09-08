from pathlib import Path
from fastapi.testclient import TestClient
from server import app
from urbion_copilot import build_copilot_packet


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


def test_judge_demo_blank_tod_preserves_score_and_unverified_dimensions():
    client=TestClient(app)
    payload={
        'project_name':'Browser QA · Sg. Udang',
        'site_lat':2.285,
        'site_lon':102.196,
        'tod_lat':None,
        'tod_lon':None,
        'state':'Melaka',
        'pbt':'Majlis Bandaraya Melaka Bersejarah',
        'district':'Melaka Tengah',
        'lot_no':'',
        'project_reference':'',
        'land_use':'Komersial',
        'landuse':'Komersial',
        'development_class':'Pembangunan Penggunaan Bercampur',
        'category':'Pembangunan Penggunaan Bercampur',
        'activity':'TOD / Mixed Use',
        'development_type':'New Development',
        'development':'New Development',
        'plot_ratio':4.5,
    }
    response=client.post('/judge/demo',json={'assessment':payload})
    assert response.status_code==200
    body=response.json()
    assert body['demo_mode']=='CHAMPIONSHIP_JUDGE_DEMO'
    assert 'snapshot' in body and body['snapshot']
    assert body['guardrails']['statutory_verification']=='NOT_CLAIMED'

    packet=build_copilot_packet(payload)
    site_analysis=packet['assessment']['site_analysis']
    assert isinstance(site_analysis['score'],(int,float))
    environment=next(item for item in site_analysis['indicators'] if item['name']=='Environment Evidence')
    assert environment['score'] is None
    assert environment['status']=='UNVERIFIED'
    assert site_analysis['score_coverage']['excluded_unverified']==['Transit Access','Environment Evidence']
    assert packet['statutory_verification']=='NOT_CLAIMED'
