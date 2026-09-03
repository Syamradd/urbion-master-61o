from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_master180_gap_audit_locks_championship_scope():
    text = (ROOT / 'MASTER-180-FINAL-GAP-AUDIT.md').read_text(encoding='utf-8')
    for token in [
        'Site Assessment → Map Studio → Evidence → What-If → Decision Center → Planner Review → KM/OSC',
        'PHASE-E.7',
        'bilingual',
        'statutory approval',
        'MASTER-181',
        'MASTER-186',
    ]:
        assert token in text


def test_live_frontend_and_release_docs_remain_same_origin_and_qualified():
    server = (ROOT / 'server.py').read_text(encoding='utf-8')
    assert "const API=location.origin;" in server
    assert 'statutory approval' in server.lower()
