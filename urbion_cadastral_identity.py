"""Cadastral identity state contract for URBION HORIZON.

This module is pure: it never treats portal visibility as statutory cadastral
verification and never performs an external query. Live i-Plan results can be
attached by a caller and remain SOURCE_CONTEXT until an authoritative parcel
verification is explicitly supplied.
"""
from __future__ import annotations

from typing import Any


STATE_PROJECT_REFERENCE = "PROJECT_REFERENCE"
STATE_IPLAN_CANDIDATE = "IPLAN_CANDIDATE"
STATE_JUPEM_VERIFICATION = "JUPEM_VERIFICATION"


def _text(value: Any) -> str | None:
    value = str(value).strip() if value is not None else ""
    return value or None


def build_cadastral_identity(
    *,
    state: str | None = None,
    district: str | None = None,
    mukim: str | None = None,
    lot_no: str | None = None,
    iplan_result: dict[str, Any] | None = None,
    jupem_verification: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a safe three-stage cadastral identity chain."""
    lot = _text(lot_no)
    iplan = iplan_result if isinstance(iplan_result, dict) else None
    jupem = jupem_verification if isinstance(jupem_verification, dict) else None

    project_reference = {
        "state": _text(state),
        "district": _text(district),
        "mukim": _text(mukim),
        "lot_no": lot,
        "status": "AVAILABLE" if lot else "NOT_PROVIDED",
        "evidence_state": "USER_PROVIDED" if lot else "UNVERIFIED",
    }

    candidate_lot = None
    candidate_upi = None
    candidate_source = None
    candidate_status = "PENDING"
    candidate_evidence = "UNVERIFIED"
    if iplan:
        candidate_status = str(iplan.get("status") or "UNVERIFIED").upper()
        candidate_evidence = str(iplan.get("evidence") or "SOURCE_CONTEXT").upper()
        nearest = iplan.get("nearest_feature") if isinstance(iplan.get("nearest_feature"), dict) else None
        features = iplan.get("features") if isinstance(iplan.get("features"), list) else []
        feature = nearest or (features[0] if features else None)
        props = feature.get("properties", {}) if isinstance(feature, dict) else {}
        candidate_lot = _text(props.get("LOT")) or _text(props.get("lot_no"))
        candidate_upi = _text(props.get("UPI")) or _text(props.get("upi"))
        candidate_source = _text(iplan.get("source"))
        if candidate_status in {"LIVE_QUERY", "NO_FEATURE"}:
            candidate_evidence = "SOURCE_CONTEXT"

    iplan_candidate = {
        "lot_no": candidate_lot,
        "upi": candidate_upi,
        "status": candidate_status,
        "evidence_state": candidate_evidence if candidate_status != "PENDING" else "UNVERIFIED",
        "source": candidate_source,
        "decision_safe": False,
    }

    verification_status = "PENDING"
    verification_evidence = "UNVERIFIED"
    verification_source = None
    verification_lot = None
    verification_upi = None
    if jupem:
        verification_status = str(jupem.get("status") or "UNVERIFIED").upper()
        verification_evidence = str(jupem.get("evidence_state") or jupem.get("evidence") or "UNVERIFIED").upper()
        verification_source = _text(jupem.get("source"))
        verification_lot = _text(jupem.get("lot_no"))
        verification_upi = _text(jupem.get("upi"))
        if verification_status == "VERIFIED":
            verification_evidence = "VERIFIED"

    jupem_state = {
        "status": verification_status,
        "lot_no": verification_lot,
        "upi": verification_upi,
        "evidence_state": verification_evidence,
        "source": verification_source,
        "decision_safe": verification_status == "VERIFIED" and verification_evidence == "VERIFIED",
    }

    return {
        "chain": [STATE_PROJECT_REFERENCE, STATE_IPLAN_CANDIDATE, STATE_JUPEM_VERIFICATION],
        "project_reference": project_reference,
        "iplan_candidate": iplan_candidate,
        "jupem_verification": jupem_state,
        "identity_boundary": "i-Plan / portal visibility is candidate source context only; statutory cadastral verification is not claimed.",
    }


__all__ = ["STATE_PROJECT_REFERENCE", "STATE_IPLAN_CANDIDATE", "STATE_JUPEM_VERIFICATION", "build_cadastral_identity"]
