from urbion_development_impact import build_development_impact


def test_impact_engine_covers_three_lcp_style_domains():
    result = build_development_impact(development_type='Mixed Development', units=500, site_area_ha=2, commercial_gfa_m2=12000, jobs=300, population=1400, daily_trips=1800, road_distance_m=80, flood_exposure=True, nearby_facilities={'school': 650})
    assert set(result['impacts']) == {'physical', 'social', 'economic'}
    assert result['impact_summary']['physical']['review_required'] is False
    assert result['impact_summary']['social']['review_required'] is False
    assert result['impact_summary']['economic']['review_required'] is False
    assert result['statutory_verification'] == 'NOT_CLAIMED'


def test_impact_calculations_are_traceable():
    result = build_development_impact(units=500, site_area_ha=2, daily_trips=1800)
    physical = {m['id']: m for m in result['impacts']['physical']}
    assert physical['development_intensity']['value'] == 250.0
    assert physical['development_intensity']['evidence'] == 'CALCULATED'
    assert physical['trip_generation']['value'] == 1800.0
    assert 'economic:EMPLOYMENT_INPUT' in result['review_gaps']


def test_missing_inputs_are_not_fabricated():
    result = build_development_impact(development_type='Residential')
    assert result['review_gaps']
    assert all(m['evidence'] == 'UNVERIFIED' for d in result['impacts'].values() for m in d if m['status'] == 'REVIEW_REQUIRED')
