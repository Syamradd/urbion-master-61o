def test_judge_note():
    text=open('MASTER-117-JUDGE.md',encoding='utf-8').read()
    for token in ['Integrated Dashboard','GIS Workspace','Evidence','What-If','Planner Brief']:
        assert token in text
