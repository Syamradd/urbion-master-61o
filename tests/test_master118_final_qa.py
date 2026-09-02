def test_final_qa_marker():
    text=open('MASTER-118.md',encoding='utf-8').read()
    assert 'Final QA' in text
    assert 'evidence-safe messaging' in text
