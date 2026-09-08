from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v5_is_wired_without_changing_release_identity():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_ux_v5.js' in server
    assert 'app.state.frontend_release="MASTER-331"' in server


def test_v5_builds_command_center_information_hierarchy():
    text = (ROOT / 'urbion_championship_ux_v5.js').read_text(encoding='utf-8')
    for token in ('#ux-v5-rail', 'PLANNING INTELLIGENCE', 'DECISION READINESS', 'SPATIAL SIGNALS', 'NEXT ACTION', 'EVIDENCE SOURCES'):
        assert token in text
    for token in ('CASE', 'EVIDENCE', 'WHAT-IF', 'DECISION', 'OUTPUT'):
        assert token in text


def test_v5_preserves_deterministic_existing_controls():
    text = (ROOT / 'urbion_championship_ux_v5.js').read_text(encoding='utf-8')
    for control in ('lat', 'lon', 'state', 'pbt', 'landuse', 'activity', 'development', 'ratio', 'run', 'reset'):
        assert control in text
    assert "$('#run')?.click()" in text
    assert "$('#reset')?.click()" in text


def test_v5_supports_bilingual_theme_and_utility_actions():
    text = (ROOT / 'urbion_championship_ux_v5.js').read_text(encoding='utf-8')
    for token in ('localStorage', 'urbion-light', 'data-ux5-lang', 'data-ux5-theme', 'data-ux5-full', 'data-ux5-more', 'exportCase', 'window.print'):
        assert token in text
    assert "localStorage.getItem('urbion-lang')" in text


def test_v5_uses_progressive_decision_language_not_internal_engine_names():
    text = (ROOT / 'urbion_championship_ux_v5.js').read_text(encoding='utf-8')
    assert 'Planning Intelligence' in text
    assert 'Decision OS' not in text
    assert 'Planner Workstation' not in text


def test_v5_has_responsive_and_reduced_motion_guards():
    text = (ROOT / 'urbion_championship_ux_v5.js').read_text(encoding='utf-8')
    assert '@media(max-width:1180px)' in text
    assert '@media(max-width:820px)' in text
    assert 'prefers-reduced-motion:reduce' in text
