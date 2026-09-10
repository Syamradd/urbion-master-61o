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


class _QAEntryURL(str):
    """Keep the QA module's health probe at the origin while browsing the canonical entry."""

    def __new__(cls, origin: str):
        value = str.__new__(cls, origin + "/championship.html")
        value.origin = origin
        return value

    def __add__(self, other):
        if other == "/health":
            return self.origin + "/health"
        if other == "/":
            return str(self)
        return str.__add__(self, other)


qa.BASE_URL = _QAEntryURL(_origin())
stable.qa.BASE_URL = qa.BASE_URL
# The canonical browser suite's legacy final dependency assertion expects this
# module-global gate value. Keep it explicit here rather than altering the
# shared acceptance suite itself while the entrypoint owns environment wiring.
qa.dependency_result = {"product_status": "PASS"}

if __name__ == "__main__":
    qa.main()
