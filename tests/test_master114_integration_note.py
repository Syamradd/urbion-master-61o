def test_integration_note():
    text=open('MASTER-114-INTEGRATION.md',encoding='utf-8').read()
    assert 'Site Assessment' in text and 'Planner Brief' in text
