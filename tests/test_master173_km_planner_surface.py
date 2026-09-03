from pathlib import Path


def test_master173_km_planner_surface():
    doc = Path('MASTER-173-KM-PLANNER-ACTION-SURFACE.md').read_text()
    assert 'KM Readiness' in doc
    assert 'Blockers' in doc
    assert 'Next evidence/action' in doc
    assert 'statutory approval' in doc
