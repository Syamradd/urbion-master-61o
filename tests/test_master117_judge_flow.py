def test_judge_flow():
    text=open('MASTER-117.md',encoding='utf-8').read()
    for token in ['Integrated Dashboard','Site Assessment','GIS Workspace','Evidence','What-If','Planner Brief']:
        assert token in text
