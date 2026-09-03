from urbion_decision_center import build_decision_center


def test_decision_center_exposes_multi_source_spatial_intelligence():
    payload = build_decision_center(assessment={
        'site': {'latitude': 2.3, 'longitude': 102.2, 'lot_no': 'TEST'},
        'final_status': 'REQUIRES REVIEW',
        'site_analysis': {},
    })
    spatial = payload['spatial_intelligence']
    ids = {m['id'] for m in spatial['metrics']}
    assert {'road_access', 'elevation', 'flood_exposure', 'slope', 'environment', 'geohazard', 'cadastral', 'ecology'} <= ids
    assert spatial['decision_boundary'] == 'SCREENING_ONLY'
    assert spatial['statutory_verification'] == 'NOT_CLAIMED'


def test_missing_spatial_measurements_remain_review_gaps():
    payload = build_decision_center(assessment={
        'site': {'latitude': 2.3, 'longitude': 102.2, 'lot_no': 'TEST'},
        'final_status': 'REQUIRES REVIEW',
        'site_analysis': {},
    })
    assert 'road_access' in payload['spatial_intelligence']['review_gaps']
    assert 'elevation' in payload['spatial_intelligence']['review_gaps']
    assert 'flood_exposure' in payload['spatial_intelligence']['review_gaps']
