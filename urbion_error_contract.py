"""Canonical API/browser error envelope for URBION HORIZON."""
from __future__ import annotations
from typing import Any

ERROR_VERSION = "URBION_ERROR_V1"


def canonical_error(*, code: str, message: str, route: str, stage: str = "UNKNOWN", source: str | None = None, evidence_state: str = "UNVERIFIED", review_required: bool = True, retryable: bool = False, canonical_packet_available: bool = False, details: Any = None) -> dict[str, Any]:
    """Return one stable error envelope with top-level canonical fields and a compatibility detail alias."""
    canonical_code = "INCOMPLETE_TOD_INPUT" if str(code) == "OPTIONAL_TOD_INPUT_ERROR" else str(code)
    out = {
        "error": True,
        "version": ERROR_VERSION,
        "code": canonical_code,
        "message": str(message),
        "route": str(route),
        "stage": str(stage),
        "source": source,
        "evidence_state": str(evidence_state),
        "review_required": bool(review_required),
        "retryable": bool(retryable),
        "canonical_packet_available": bool(canonical_packet_available),
        "statutory_verification": "NOT_CLAIMED",
        "decision_authority": "NONE",
        "detail": {"code": canonical_code, "message": str(message)},
    }
    if details is not None:
        out["details"] = details
    return out


__all__ = ["ERROR_VERSION", "canonical_error"]
