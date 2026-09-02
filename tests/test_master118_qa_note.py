def test_qa_note():
    text=open('MASTER-118-QA.md',encoding='utf-8').read()
    assert 'Final QA marker' in text and 'Render auto-deploy' in text
