def test_rt_iplan_binding_contract():
    text=open('MASTER-113.md',encoding='utf-8').read()
    assert 'RT + i-Plan' in text
    assert 'no live lot verification is fabricated' in text
