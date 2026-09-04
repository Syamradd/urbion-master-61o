from pathlib import Path


def test_master277_uses_official_melaka_iplan_services():
    js = Path("urbion_championship_v277.js").read_text(encoding="utf-8")
    assert "GTsemasa_04/MapServer" in js
    assert "GTzoning_04/MapServer" in js
    assert "LOT_04/MapServer" in js
    assert "KONTUR5M_04/MapServer" in js


def test_master277_integrates_full_planning_chain():
    js = Path("urbion_championship_v277.js").read_text(encoding="utf-8")
    for endpoint in [
        "/health",
        "/iplan/context",
        "/assess",
        "/environment/intelligence",
        "/station-intelligence",
        "/decision-center",
        "/what-if",
        "/lcp/intelligence",
        "/championship-gate",
    ]:
        assert endpoint in js
    assert "Promise.allSettled" in js
    assert "statutory_verification" in js or "NOT_CLAIMED" in js
