from pathlib import Path


def test_judge_flow_has_complete_product_path():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-144-JUDGE-FLOW.md').read_text(encoding='utf-8')
    for token in ('Dashboard', 'Site Assessment', 'Map Studio', 'Evidence', 'What-If', 'Decision Center', 'Planner Review'):
        assert token in text


def test_judge_flow_protects_evidence_and_statutory_boundaries():
    text = (Path(__file__).resolve().parents[1] / 'MASTER-144-JUDGE-FLOW.md').read_text(encoding='utf-8')
    assert 'cannot mistake decision support for statutory approval' in text
    assert 'project-reference GIS' in text
    assert 'verified' in text
