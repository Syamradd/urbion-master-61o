def test_redteam_note():
    text=open('MASTER-115-REDTEAM.md',encoding='utf-8').read()
    assert 'invalid coordinates' in text and 'evidence gaps' in text
