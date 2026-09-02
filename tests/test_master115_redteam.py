def test_final_redteam_contract():
    text=open('MASTER-115.md',encoding='utf-8').read()
    for token in ['invalid coordinates','unsupported PBT','TOD boundary','failed frontage','evidence-state']:
        assert token in text
