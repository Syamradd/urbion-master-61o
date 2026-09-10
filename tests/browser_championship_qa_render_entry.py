"""Run canonical workstation browser QA through the production entrypoint."""
from __future__ import annotations

import os
from urllib.parse import urlsplit, urlunsplit

import browser_championship_qa as qa
import browser_championship_qa_stable as stable


def _origin() -> str:
    raw = os.getenv("URBION_APP_URL", "http://127.0.0.1:8765")
    parsed = urlsplit(raw)
    if parsed.scheme and parsed.netloc:
        return urlunsplit((parsed.scheme, parsed.netloc, "", "", "")).rstrip("/")
    return raw.rstrip("/")


qa.BASE_URL = _origin() + "/championship.html"
stable.qa.BASE_URL = qa.BASE_URL

if __name__ == "__main__":
    qa.main()
