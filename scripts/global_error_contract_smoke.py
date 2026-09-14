"""Smoke-test canonical URBION_ERROR_V1 responses for common downstream failure paths."""
from __future__ import annotations
import json, os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")


def request(path: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method=method)
    try:
        with urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


def assert_error(path: str, *, method: str = "GET", payload: dict | None = None, expected_code: str | tuple[str, ...]):
    status, body = request(path, method, payload)
    assert status >= 400, f"{path}: expected error, got {status}"
    assert body.get("error") is True, f"{path}: missing error flag"
    assert body.get("version") == "URBION_ERROR_V1", f"{path}: wrong error version"
    allowed = (expected_code,) if isinstance(expected_code, str) else expected_code
    assert body.get("code") in allowed, f"{path}: expected one of {allowed}, got {body.get('code')}"
    assert body.get("statutory_verification") == "NOT_CLAIMED"
    assert body.get("decision_authority") == "NONE"


def main() -> None:
    # FastAPI validation may be surfaced by the downstream application as a
    # generic HTTP_422 envelope rather than an exception, so the contract
    # accepts either the semantic validation code or the canonical HTTP code.
    assert_error(
        "/iplan/context?site_lat=not-a-number&site_lon=102.196",
        expected_code=("REQUEST_VALIDATION_ERROR", "HTTP_422"),
    )
    assert_error("/planning-value", method="POST", payload=None, expected_code=("REQUEST_VALIDATION_ERROR", "HTTP_422"))
    # Unknown routes must still be visible as canonical HTTP 404 errors.
    assert_error("/demo-scenarios/does-not-exist", method="POST", expected_code="HTTP_404")
    print("GLOBAL ERROR CONTRACT PASS")


if __name__ == "__main__":
    main()
