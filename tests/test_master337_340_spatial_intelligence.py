from fastapi.testclient import TestClient

from championship_server import app
from urbion_spatial_intelligence import bearing_deg, build_spatial_intelligence, haversine_m, nearest_feature


def test_spatial_engine_geometry_is_deterministic():
    distance = haversine_m(2.285, 102.196, 2.286, 102.197)
    assert 100 < distance < 200
    assert 40 < bearing_deg(2.285, 102.196, 2.286, 102.197) < 60
    result = build_spatial_intelligence(2.285, 102.196, 2.286, 102.197)
    assert result['tod']['classification'] == 'TOD 400m'
    assert len(result['catchments']['features']) == 2
    assert result['catchments']['features'][0]['properties']['radius_m'] == 400.0
    assert result['catchments']['features'][1]['properties']['radius_m'] == 800.0
    assert result['evidence_model']['geometry'] == 'CALCULATED'


def test_spatial_nearest_and_matrix_are_ranked():
    nearest = nearest_feature(2.285, 102.196, [
        {'name': 'Far', 'latitude': 2.30, 'longitude': 102.21},
        {'name': 'Near', 'latitude': 2.286, 'longitude': 102.197},
    ])
    assert nearest['feature']['name'] == 'Near'
    client = TestClient(app)
    response = client.post('/spatial/matrix', json={
        'origins': [{'latitude': 2.285, 'longitude': 102.196}],
        'destinations': [
            {'latitude': 2.286, 'longitude': 102.197},
            {'latitude': 2.295, 'longitude': 102.205},
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body['count'] == 2
    assert body['matrix'][0]['distance_m'] < body['matrix'][1]['distance_m']
    assert all(item['evidence'] == 'CALCULATED' for item in body['matrix'])


def test_spatial_api_exposes_catchment_and_constraint_evidence():
    client = TestClient(app)
    intelligence = client.post('/spatial/intelligence', json={
        'site_lat': 2.285,
        'site_lon': 102.196,
        'tod_lat': 2.286,
        'tod_lon': 102.197,
        'radii': [400, 800],
        'constraints': {'flood': True, 'ksas': False, 'heritage': 'review'},
    })
    assert intelligence.status_code == 200
    body = intelligence.json()
    assert body['version'] == 'PHASE-E.8'
    assert body['tod']['distance_m'] > 0
    assert body['constraints']['flagged_count'] == 1
    assert body['statutory_verification'] == 'NOT_CLAIMED'
    catchments = client.get('/spatial/catchments?site_lat=2.285&site_lon=102.196&radii=400,800')
    assert catchments.status_code == 200
    assert catchments.json()['evidence'] == 'CALCULATED'
    assert 'authoritative statutory boundaries' in catchments.json()['disclaimer']


def test_spatial_api_rejects_bad_coordinates():
    client = TestClient(app)
    response = client.post('/spatial/intelligence', json={'site_lat': -90, 'site_lon': -180})
    assert response.status_code == 422
    assert response.json()['detail']['code'] == 'INVALID_SPATIAL_INPUT'
