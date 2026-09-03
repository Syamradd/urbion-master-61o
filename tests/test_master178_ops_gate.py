from pathlib import Path


def test_master178_ops_gate():
    text = Path('MASTER-178-CHAMPIONSHIP-OPS.md').read_text(encoding='utf-8')
    for token in ['Site Assessment','Map Studio','Evidence / Provenance','What-If baseline vs scenario','Decision Center','Planner Review','KM/OSC','placeholder coordinates','statutory approval','successful full GitHub Actions']:
        assert token in text
