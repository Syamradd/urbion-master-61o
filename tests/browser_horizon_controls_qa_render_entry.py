"""Run HORIZON controls QA against the canonical workstation URL."""
from __future__ import annotations

import os
from urllib.parse import urlsplit, urlunsplit

import browser_horizon_controls_qa as qa


def _origin() -> str:
    raw = os.getenv("URBION_APP_URL", "http://127.0.0.1:8765")
    parsed = urlsplit(raw)
    if parsed.scheme and parsed.netloc:
        return urlunsplit((parsed.scheme, parsed.netloc, "", "", "")).rstrip("/")
    return raw.rstrip("/")


qa.BASE_URL = _origin() + "/championship.html"

if __name__ == "__main__":
    qa.main()
