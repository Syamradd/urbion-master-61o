"""Pure contract smoke for the cadastral identity chain."""
from __future__ import annotations

from urbion_cadastral_identity import build_cadastral_identity
from urbion_canonical_evidence import build_canonical_evidence_packet


def main() -> None:
    pending = build_cadastral_identity(
        state="Melaka", district="Melaka Tengah", mukim="Alor Gajah", lot_no="11213"
    )
    assert pending["chain"] == ["PROJECT_REFERENCE", "IPLAN_CANDIDATE", "JUPEM_VERIFICATION"]
    assert pending["project_reference"]["status"] == "AVAILABLE"
    assert pending["project_reference"]["evidence_state"] == "USER_PROVIDED"
    assert pending["iplan_candidate"]["status"] == "PENDING"
    assert pending["iplan_candidate"]["decision_safe"] is False
    assert pending["jupem_verification"]["status"] == "PENDING"
    assert pending["jupem_verification"]["decision_safe"] is False

    live_candidate = build_cadastral_identity(
        state="Melaka",
        district="Melaka Tengah",
        lot_no="11213",
        iplan_result={
            "status": "LIVE_QUERY",
            "source": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/LOT_04/MapServer/0",
            "evidence": "SOURCE_CONTEXT",
            "features": [{"properties": {"LOT": "11213", "UPI": "04-01-01-00011213"}}],
        },
    )
    assert live_candidate["iplan_candidate"]["lot_no"] == "11213"
    assert live_candidate["iplan_candidate"]["evidence_state"] == "SOURCE_CONTEXT"
    assert live_candidate["iplan_candidate"]["decision_safe"] is False

    verified = build_cadastral_identity(
        state="Melaka",
        district="Melaka Tengah",
        lot_no="11213",
        jupem_verification={
            "status": "VERIFIED",
            "evidence_state": "VERIFIED",
            "source": "JUPEM authoritative parcel verification",
            "lot_no": "11213",
            "upi": "04-01-01-00011213",
        },
    )
    assert verified["jupem_verification"]["decision_safe"] is True
    assert verified["jupem_verification"]["evidence_state"] == "VERIFIED"

    packet = build_canonical_evidence_packet(
        assessment={
            "site": {
                "state": "Melaka", "district": "Melaka Tengah", "pbt": "MBMB", "lot_no": "Not specified"
            },
            "evidence_state": {"site_coordinates": "USER_PROVIDED"},
        }
    )
    assert packet["cadastral_identity"]["project_reference"]["status"] == "NOT_PROVIDED"
    assert any("cadastral identity requires explicit project input" in gap for gap in packet["review_gaps"])
    assert packet["statutory_verification"] == "NOT_CLAIMED"

    print("[PHASE1-CADASTRAL] three-stage identity contract PASS")
    print("[PHASE1-CADASTRAL] i-Plan remains SOURCE_CONTEXT and JUPEM is the explicit verification boundary")


if __name__ == "__main__":
    main()
