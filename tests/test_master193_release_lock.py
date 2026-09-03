from pathlib import Path


def test_championship_release_lock_contains_non_negotiable_gates():
    text=Path('MASTER-193-CHAMPIONSHIP-RELEASE-LOCK.md').read_text(encoding='utf-8')
    for token in ('Site Assessment','Map Studio','Evidence','What-If','Decision Center','Planner Review','LCP Intelligence','KM/OSC','placeholders rejected','review gaps','Recommendations remain planner-review outputs','KM/OSC remains workflow readiness support, never approval','GREEN'):
        assert token in text


def test_core_release_files_are_present():
    for path in ('server.py','urbion_ui.js','urbion_lcp_intelligence.py','urbion_recommendation_engine.py','urbion_policy_graph.py','urbion_live_stations.py'):
        assert Path(path).is_file(), path
