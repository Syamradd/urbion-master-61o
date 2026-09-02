def test_environment_disclosure():
    text=open('MASTER-112.md',encoding='utf-8').read()
    assert 'MyGEMS / MyEQMS' in text
    assert 'evidence gap' in text
