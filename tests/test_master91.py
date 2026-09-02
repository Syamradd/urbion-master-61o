from pathlib import Path

def test_planner_workspace_is_printable_and_uses_assessment():
    html=Path('planner-workspace.html').read_text(encoding='utf-8')
    assert '/assess' in html
    assert 'PRINT / SAVE PDF' in html
    assert 'planning_value' in html
    assert 'Next Actions' in html
