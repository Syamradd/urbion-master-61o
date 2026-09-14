"""Isolated JPS Public Infobanjir station adapter.

The official JPS site exposes station-detail pages containing station identity,
status and coordinates. This adapter normalizes those details into URBION's
existing station contract without pretending that the rainfall HTML page is a
machine-query API.

Current boundary: geometry/station metadata can be normalized; live rainfall
values remain SOURCE_CONTEXT until a stable machine-query contract is proven.
"""
from __future__ import annotations

from html import unescape
from io import StringIO
import re
from typing import Any, Callable, Iterable
from urllib.parse import parse_qsl, urljoin, urlparse

import pandas as pd

JPS_RAINFALL_URL = "https://publicinfobanjir.water.gov.my/hujan/data-hujan/"
JPS_STATION_INFO_URL = "https://publicinfobanjir.water.gov.my/cari-station/"
JPS_HOST = "publicinfobanjir.water.gov.my"


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = unescape(re.sub(r"<[^>]+>", " ", str(value)))
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_official_station_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc.casefold() == JPS_HOST
        and parsed.path.rstrip("/").casefold() == "/cari-station"
        and any(key.casefold() == "station_id" and value for key, value in parse_qsl(parsed.query))
    )


def discover_station_info_urls(html: str) -> list[str]:
    """Discover only official JPS station-detail links carrying ``station_id``."""
    found: list[str] = []
    hrefs = re.findall(r"href\s*=\s*[\"']([^\"']+)[\"']", html or "", flags=re.I)
    for href in hrefs:
        href = unescape(href.strip())
        if href.startswith("/"):
            candidate = urljoin(JPS_STATION_INFO_URL, href)
        elif href.startswith(("http://", "https://")):
            candidate = href
        else:
            continue
        if _is_official_station_url(candidate) and candidate not in found:
            found.append(candidate)
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


def _regex_table_values(html: str) -> dict[str, str]:
    """Fallback parser so deterministic CI does not depend on optional HTML engines."""
    values: dict[str, str] = {}
    row_pattern = re.compile(r"<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", re.I | re.S)
    for label, value in row_pattern.findall(html or ""):
        key = _clean(label)
        val = _clean(value)
        if key and val:
            values[key.casefold()] = val
    return values


def _detail_value(tables: list[pd.DataFrame], label: str, pairs: dict[str, str]) -> str | None:
    return _table_value(tables, label) or pairs.get(label.casefold())


def parse_station_detail(html: str, source_url: str | None = None) -> dict[str, Any] | None:
    """Normalize one official JPS station-detail page."""
    try:
        tables = pd.read_html(StringIO(html))
    except (ValueError, ImportError):
        tables = []

    pairs = _regex_table_values(html)
    name = _detail_value(tables, "Station Name", pairs)
    code = _detail_value(tables, "Station Code", pairs)
    district = _detail_value(tables, "District", pairs)
    state = _detail_value(tables, "State", pairs)
    status = _detail_value(tables, "Status", pairs)
    lat = _number(_detail_value(tables, "Latitude", pairs))
    lon = _number(_detail_value(tables, "Longitude", pairs))
    last_rain = _detail_value(tables, "Last Updated (Rainfall)", pairs)

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
