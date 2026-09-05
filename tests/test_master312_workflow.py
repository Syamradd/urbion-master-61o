from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def test_workflow_navigator_contract():
    text = read('urbion_championship_workflow.js')
    for token in ['01','SITE','02','MAP','03','ANALYSE','04','WHY','05','WHAT-IF','06','DECISION','07','ACTION','urbion:analysis','urbion:site-change']:
        assert token in text
    assert 'data-uw-view' in text
    assert 'DECISION WORKFLOW' in text


def test_workflow_is_served_by_championship_entrypoint():
    text = read('championship_server.py')
    assert 'urbion_championship_workflow.js' in text
    assert 'MASTER-323' in text
    assert 'no-store' in text
    assert 'urbion_championship_decision_chain.js' in text


def test_spatial_studio_evidence_contract():
    text = read('urbion_championship_spatial_studio.js')
    for token in ['MASTER-320','SITE RELATIONSHIP','LIVE SOURCE CONTEXT','EVIDENCE / PROVENANCE','🟢 VERIFIED','🔵 SOURCE CONTEXT','🟣 CALCULATED','🟡 USER PROVIDED','🔴 EVIDENCE GAP','Haversine','not walking-network','source_status','renderProvenance','GEOSERVER_WMS','ARCGIS_MAP']:
        assert token in text


def test_judge_packet_exposes_real_score_drivers():
    backend = read('urbion_judge_mode.py')
    frontend = read('judge-mode.html')
    for token in ['score_breakdown','_dimension_drivers','dimension','method']:
        assert token in backend
    for token in ['r.score_breakdown','Assessment dimensions','SCORE DRIVERS','not approval probability']:
        assert token in frontend
