from pathlib import Path


RUNTIME = Path(__file__).resolve().parents[1] / "urbion_map_identify_runtime.js"


def test_map_identify_runtime_has_safe_source_and_evidence_contract():
    text = RUNTIME.read_text(encoding="utf-8")
    required = [
        "window.__URBION_MAP_IDENTIFY__",
        "__URBION_OFFICIAL_LAYERS__",
        "/identify?",
        "LIVE_QUERY",
        "QUERY_ERROR",
        "SOURCE_CONTEXT",
        "decision_safe:false",
        "requires_rule_binding:true",
        "statutory_approval_claim:false",
        "urbion-map-identify",
        "urbion-map-evidence",
    ]
    for marker in required:
        assert marker in text, f"missing identify runtime contract marker: {marker}"


def test_map_identify_runtime_does_not_claim_statutory_approval():
    text = RUNTIME.read_text(encoding="utf-8")
    assert "statutory_approval_claim:true" not in text
    assert "decision_safe:true" not in text
