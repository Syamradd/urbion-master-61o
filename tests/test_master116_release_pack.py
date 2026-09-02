def test_release_pack_exists():
    text=open('MASTER-116.md',encoding='utf-8').read()
    assert 'Release checklist' in text
    assert 'Render auto-deploy' in text
