"""Isolated JPS Public Infobanjir station adapter.

The official JPS site exposes station-detail pages containing station identity,
status and coordinates. This adapter normalizes those details into URBION's
existing station contract without pretending that the rainfall HTML page is a
machine-query API.

Current boundary: geometry/station metadata can be normalized; live rainfall
values remain SOURCE_CONTEXT until a stable machine-query contract is proven.
"""
from __future__ import annotations

from io import StringIO
import re
from typing import Any, Callable, Iterable

import pandas as pd

JPS_RAINFALL_URL = "https://publicinfobanjir.water.gov.my/hujan/data-hujan/"
JPS_STATION_INFO_URL = "https://publicinfobanjir.water.gov.my/cari-station/"


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def discover_station_info_urls(html: str) -> list[str]:
    """Discover official station-detail links from a JPS state page.

    The function is deliberately schema-light: only official ``cari-station``
    links carrying a station_id query parameter are accepted.
    """
    pattern = re.compile(
        r'https?://publicinfobanjir\.water\.gov\.my/cari-station/[^"\'<>]*station_id=[^"\'&#<>]+'
        r'|/cari-station/[^"\'<>]*station_id=[^"\'&#<>]+'
    )
    found = []
    for match in pattern.findall(html or ""):
        url = match.replace("&amp;", "&")
        if url.startswith("/"):
            url = "https://publicinfobanjir.water.gov.my" + url
        if url not in found:
            found.append(url)
    return found


def _table_value(tables: list[pd.DataFrame], label: str) -> str | None:
    wanted = label.casefold()
    for table in tables:
        for _, row in table.iterrows():
            values = [_clean(v) for v in row.tolist()]
            values = [v for v in values if v]
            if not values:
                continue
            if values[0].casefold() == wanted and len(values) > 1:
                return values[1]
    return None


def parse_station_detail(html: str, source_url: str | None = None) -> dict[str, Any] | None:
    """Normalize one official JPS station-detail page."""
    try:
        tables = pd.read_html(StringIO(html))
    except (ValueError, ImportError):
        tables = []

    name = _table_value(tables, "Station Name")
    code = _table_value(tables, "Station Code")
    district = _table_value(tables, "District")
    state = _table_value(tables, "State")
    status = _table_value(tables, "Status")
    lat = _number(_table_value(tables, "Latitude"))
    lon = _number(_table_value(tables, "Longitude"))
    last_rain = _table_value(tables, "Last Updated (Rainfall)")

    if not name or lat is None or lon is None:
        return None
    return {
        "name": name,
        "station_id": code or name,
        "lat": lat,
        "lon": lon,
        "last_updated": last_rain if last_rain and last_rain.casefold() != "no data" else None,
        "source": "JPS Public Infobanjir",
        "source_url": source_url or JPS_STATION_INFO_URL,
        "evidence_state": "VERIFIED",
        "status": status,
        "district": district,
        "state": state,
        "reading": None,
        "review_note": "LIVE_READING_NOT_MACHINE_VERIFIED",
    }


def fetch_jps_station_geometry(
    station_urls: Iterable[str],
    *,
    http_get: Callable[[str], str] | None = None,
) -> list[dict[str, Any]]:
    """Fetch a bounded set of official station-detail pages.

    ``http_get`` is injectable for deterministic CI. This function intentionally
    does not scrape or infer rainfall readings from the public HTML table.
    """
    import httpx

    records = []
    urls = list(dict.fromkeys(station_urls))
    if http_get is None:
        with httpx.Client(timeout=8.0, follow_redirects=True) as client:
            for url in urls:
                response = client.get(url)
                response.raise_for_status()
                record = parse_station_detail(response.text, url)
                if record:
                    records.append(record)
    else:
        for url in urls:
            record = parse_station_detail(http_get(url), url)
            if record:
                records.append(record)
    return records
