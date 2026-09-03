from datetime import datetime, timezone

import pytest

from urbion_station_intelligence import build_lcp_snapshot, build_station_intelligence, classify_api, freshness_minutes, nearest_station


def test_nearest_station_and_distance():
    result = nearest_station(2.20, 102.25, [
        {"station_id": "FAR", "name": "Far", "lat": 2.30, "lon": 102.25},
        {"station_id": "NEAR", "name": "Near", "lat": 2.201, "lon": 102.251},
    ])
    assert result["station_id"] == "NEAR"
    assert result["distance_m"] > 0


def test_api_classification():
    assert classify_api(50) == "Good"
    assert classify_api(100) == "Moderate"
    assert classify_api(150) == "Unhealthy"
    assert classify_api(250) == "Very Unhealthy"
    assert classify_api(301) == "Hazardous"


def test_freshness_is_deterministic_with_reference_time():
    now = datetime(2026, 9, 3, 8, 0, tzinfo=timezone.utc)
    assert freshness_minutes("2026-09-03T07:30:00+00:00", now) == 30.0


def test_lcp_snapshot_keeps_source_and_reading_provenance():
    rows = build_lcp_snapshot({"rainfall": {"station_id": "JPS1", "name": "Rain Station", "distance_m": 420.5, "reading": 12.3, "last_updated": "2026-09-03T07:45:00+00:00", "status": "Moderate", "source": "JPS", "evidence_state": "SOURCE_CONTEXT"}})
    assert rows[0]["reading"] == 12.3
    assert rows[0]["source"] == "JPS"
    assert rows[0]["evidence_state"] == "SOURCE_CONTEXT"


def test_builder_never_fabricates_unconfigured_station_data():
    result = build_station_intelligence(2.20, 102.25)
    assert result["status"] == "LIVE_STATION_INTELLIGENCE"
    assert result["lcp_snapshot"] == []
    assert result["review_gaps"]
    assert result["statutory_verification"] == "NOT_CLAIMED"


def test_builder_uses_only_injected_station_records():
    def rainfall(**_):
        return [{"station_id": "R1", "name": "Rain", "lat": 2.201, "lon": 102.251, "reading": 18.0, "last_updated": "2026-09-03T07:45:00+00:00", "source": "JPS"}]

    result = build_station_intelligence(2.20, 102.25, fetchers={"rainfall": rainfall})
    assert result["nearest"]["rainfall"]["station_id"] == "R1"
    assert result["nearest"]["rainfall"]["reading"] == 18.0
    assert result["nearest"]["rainfall"]["evidence_state"] == "SOURCE_CONTEXT"
    assert any(g.startswith("air_quality:") for g in result["review_gaps"])


def test_invalid_site_is_rejected():
    with pytest.raises(ValueError, match="INVALID_SPATIAL_INPUT"):
        build_station_intelligence(-90, -180)
