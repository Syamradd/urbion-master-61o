from urbion_multi_source import build_spatial_intelligence


def test_master183_does_not_fabricate_missing_metrics():
    result = build_spatial_intelligence()
    assert {m['id'] for m in result['metrics']} == {'road_access', 'elevation', 'flood_exposure'}
    assert result['review_gaps'] == ['road_access', 'elevation', 'flood_exposure']
    assert result['statutory_verification'] == 'NOT_CLAIMED'


def test_master183_explicit_metrics_are_calculated_only_from_inputs():
    result = build_spatial_intelligence(road_distance_m=120, elevation_m=8.5, flood_exposure=True)
    by_id = {m['id']: m for m in result['metrics']}
    assert by_id['road_access']['evidence'] == 'CALCULATED'
    assert by_id['elevation']['value_m'] == 8.5
    assert by_id['flood_exposure']['status'] == 'FLAGGED'
    assert result['review_gaps'] == []


def test_master183_live_and_portal_sources_remain_source_context():
    result = build_spatial_intelligence(source_context={
        'iplan': {'status': 'LIVE_QUERY'},
        'jps': {'status': 'PUBLIC_REAL_TIME_PORTAL'},
        'mylot': {'status': 'PORTAL_REFERENCE'},
    })
    assert all(s['evidence'] == 'SOURCE_CONTEXT' for s in result['sources'])
