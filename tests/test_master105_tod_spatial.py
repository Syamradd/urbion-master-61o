from urbion_tod_spatial import haversine_m, tod_catchment


def test_same_point_zero_distance():
    assert haversine_m(lat1=2.3, lon1=102.2, lat2=2.3, lon2=102.2) == 0


def test_tod_400_band():
    result = tod_catchment(site_lat=2.3, site_lon=102.2, tod_lat=2.302, tod_lon=102.2)
    assert result["within_400m"] is True
    assert result["band"] == "TOD 400m"


def test_outside_800_band():
    result = tod_catchment(site_lat=2.3, site_lon=102.2, tod_lat=2.32, tod_lon=102.2)
    assert result["within_800m"] is False
    assert result["band"] == "OUTSIDE 800m"
