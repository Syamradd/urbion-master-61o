from urbion_demo_scenarios import demo_scenarios

def test_demo_scenarios_are_deterministic_and_complete():
    items=demo_scenarios()
    assert [x['id'] for x in items]==['TOD-COMPLY','SHOP-COMPLY','SHOP-FAIL','OFFICE-REVIEW','NON-MBMB']
    assert all(x.get('inputs') for x in items)
    assert all(x.get('tag') for x in items)
