def test_integrated_dashboard_contract():
    html=open('integrated-dashboard.html',encoding='utf-8').read()
    for token in ['GIS Workspace','What-If','Evidence','Planner Brief','RT + i-Plan','ENVIRONMENT','SUITABILITY','RECOMMENDATION']:
        assert token in html
    assert 'Decision-support only' in html
    assert 'never promoted to statutory evidence' in html
