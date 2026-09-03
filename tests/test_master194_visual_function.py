from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_championship_surfaces_are_present():
    required = ["index.html","map-studio.html","what-if.html","decision-center.html","planner-review.html","lcp-intelligence.html"]
    for name in required:
        assert (ROOT / name).exists(), name


def test_major_frontends_use_same_origin_api():
    for name in ["map-studio.html", "what-if.html", "decision-center.html", "lcp-intelligence.html"]:
        text = read(name)
        assert "location.origin" in text, name
        assert "urbion-master-61o.onrender.com" not in text, name
        assert "urbion-master-61o-1.onrender.com" not in text, name


def test_lcp_surface_preserves_safe_rendering_and_boundary():
    text = read("lcp-intelligence.html")
    assert "const esc=" in text
    assert "replace(/[&<>\"']" in text
    assert "NOT_CLAIMED" in text
    assert "REVIEW" in text
    assert "/lcp/intelligence" in text


def test_release_contract_documents_the_real_chain():
    text = read("MASTER-193-CHAMPIONSHIP-RELEASE-LOCK.md")
    for token in ["Site Assessment","Map Studio","Evidence","What-If","Decision Center","Planner Review","LCP Intelligence","KM/OSC","GREEN"]:
        assert token in text
