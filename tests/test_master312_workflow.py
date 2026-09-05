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
    assert 'MASTER-316' in text
    assert 'no-store' in text
