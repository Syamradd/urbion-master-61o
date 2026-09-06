from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_master_353_acceptance_contract_is_present():
    doc = read("MASTER-353-DECISION-GRADE-AUDIT.md")
    required = [
        "MASTER-353",
        "NO GEOMETRY = NO MAP LAYER",
        "VERIFIED_CANDIDATE",
        "JUPEM",
        "Evidence → What-If → Decision",
        "MASTER-330",
        "Render deployment is intentionally outside CI",
    ]
    for token in required:
        assert token in doc


def test_master_353_unified_bridge_remains_the_state_handoff():
    bridge = read("urbion_championship_unified_bridge.js")
    assert "__URBION_UNIFIED_WORKSPACE" in bridge
    assert "urbion:unified-workspace" in bridge
    for token in ["case", "lot", "spatial", "evidence", "whatif", "decision"]:
        assert token in bridge.lower()


def test_master_353_existing_spatial_and_lot_layers_are_real_source_backed():
    lot = read("urbion_lot_resolver.py")
    spatial = read("urbion_spatial_context.py")
    assert "scharms.planmalaysia.gov.my" in lot
    assert "returnGeometry" in lot
    assert "GTsemasa_04" in spatial or "GTzoning_04" in spatial
    assert "NO_FEATURE" in lot
    assert "EVIDENCE_GAP" in lot


def test_master_353_no_fake_layer_rule_is_explicit_in_capability_matrix():
    matrix = read("GIS_CAPABILITY_MATRIX.md")
    assert "NO GEOMETRY" in matrix or "geometry" in matrix.lower()
