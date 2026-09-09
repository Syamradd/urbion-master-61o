from urbion_jps_adapter import discover_station_info_urls, parse_station_detail


HTML = '''
<table>
<tr><td>Station Name</td><td>Parit Sidang Seman (F2)</td></tr>
<tr><td>Station Code</td><td>MJSN0007</td></tr>
<tr><td>District</td><td>Jasin</td></tr>
<tr><td>State</td><td>Melaka</td></tr>
<tr><td>Status</td><td>ON</td></tr>
<tr><td>Last Updated (Rainfall)</td><td>27/08/2026 02:45:00</td></tr>
<tr><td>Latitude</td><td>2.126878</td></tr>
<tr><td>Longitude</td><td>102.501283</td></tr>
</table>
'''


def test_discover_station_urls_only_accepts_official_station_links():
    html = '''<a href="/cari-station/?lang=en&state=MLK&station_id=26195">Station</a>
    <a href="https://example.com/cari-station/?station_id=999">bad</a>'''
    assert discover_station_info_urls(html) == [
        "https://publicinfobanjir.water.gov.my/cari-station/?lang=en&state=MLK&station_id=26195"
    ]


def test_parse_station_detail_returns_geometry_and_no_fabricated_reading():
    record = parse_station_detail(HTML, "https://publicinfobanjir.water.gov.my/cari-station/?station_id=26195")
    assert record is not None
    assert record["station_id"] == "MJSN0007"
    assert record["lat"] == 2.126878
    assert record["lon"] == 102.501283
    assert record["reading"] is None
    assert record["review_note"] == "LIVE_READING_NOT_MACHINE_VERIFIED"
    assert record["evidence_state"] == "VERIFIED"


def test_parse_station_detail_rejects_missing_geometry():
    html = '<table><tr><td>Station Name</td><td>Example</td></tr></table>'
    assert parse_station_detail(html) is None
