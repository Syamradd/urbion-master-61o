import json

import urbion_live_stations as live
from urbion_live_stations import build_live_station_snapshot, haversine_m


RAIN_HTML = '''<table><tr><th>No.</th><th>Station ID</th><th>Station</th><th>District</th><th>Last Updated</th><th>Daily</th><th>Midnight</th><th>1 Hour</th></tr><tr><td>1</td><td>1234567</td><td>Demo Station</td><td>Melaka Tengah</td><td>03/09/2026 10:00:00</td><td>12.5</td><td>8.0</td><td>3.0</td></tr></table>'''
INFO_HTML = '''Station Name Demo Station District Melaka Tengah State Melaka Status ON Last Updated (Rainfall) 03/09/2026 10:00:00 Last Updated (Water Level) No Data Latitude 2.3005 Longitude 102.2005'''


def fake_fetch(url: str, timeout: float = 12.0) -> str:
    return RAIN_HTML if 'data-hujan' in url else INFO_HTML


def test_master184_snapshot_contract_without_apims_configuration(monkeypatch):
    monkeypatch.setattr(live, '_fetch', fake_fetch)
    monkeypatch.setattr(live, 'APIMS_URL', '')
    result = build_live_station_snapshot(2.3, 102.2, 'Melaka', 3)
    assert result['version'] == 'MASTER-184'
    assert result['statutory_verification'] == 'NOT_CLAIMED'
    assert result['air_quality']['evidence'] == 'SOURCE_CONTEXT'
    assert result['jps_rainfall']['status'] == 'LIVE'
    assert result['jps_rainfall']['stations'][0]['station_id'] == '1234567'
    assert result['lcp_fields'] == ['station_name', 'station_id', 'distance_m', 'reading', 'unit', 'timestamp', 'status', 'source', 'evidence']


def test_master184_distance_is_deterministic():
    assert haversine_m(2.3, 102.2, 2.3, 102.2) == 0.0
    assert haversine_m(2.3, 102.2, 2.31, 102.2) > 0


def test_master184_provider_values_never_become_verified(monkeypatch):
    monkeypatch.setattr(live, '_fetch', fake_fetch)
    monkeypatch.setattr(live, 'APIMS_URL', '')
    result = build_live_station_snapshot(2.3, 102.2, 'Melaka', 1)
    assert result['jps_rainfall']['evidence'] == 'SOURCE_CONTEXT'
    assert result['air_quality']['evidence'] == 'SOURCE_CONTEXT'


def test_master184_api_adapter_is_json_only(monkeypatch):
    monkeypatch.setattr(live, 'APIMS_URL', 'https://example.test/apims.json')
    monkeypatch.setattr(live, '_fetch', lambda url, timeout=12.0: json.dumps({'stations': [{'name':'AQ Demo','latitude':2.31,'longitude':102.21,'api':42}]}))
    result = live.nearest_air_quality(2.3, 102.2, 1)
    assert result['status'] == 'LIVE'
    assert result['stations'][0]['api'] == 42
    assert result['stations'][0]['evidence'] == 'SOURCE_CONTEXT'
