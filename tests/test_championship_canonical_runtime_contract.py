from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "championship_server.py"
SHELL = ROOT / "urbion_championship_command_shell.js"


def test_canonical_shell_is_the_only_public_root_runtime_asset():
    server = SERVER.read_text(encoding="utf-8")
    assert 'CANONICAL_ASSET = "urbion_championship_command_shell.js"' in server
    assert '<div id="urbion-championship-shell"></div>' in server
    assert '<script src="/urbion_championship_command_shell.js"></script>' in server
    assert "_frontend_root()" in server
    assert "championship.html" in server
    assert "source = target.read_text" not in server
    assert "runtime_assets" not in server


def test_legacy_dashboard_is_not_executed_by_the_root_html_template():
    server = SERVER.read_text(encoding="utf-8")
    root_start = server.index('def _frontend_root()')
    root_end = server.index('def _frontend_asset', root_start)
    root = server[root_start:root_end]
    assert '<div class="app">' not in root
    assert '<script src="/urbion_championship_final_command_center.js"></script>' not in root
    assert '<script src="/urbion_championship_ui_repair.js"></script>' not in root
    assert '<script src="/urbion_championship_ui_repair_v2.js"></script>' not in root
    assert '<script src="/urbion_championship_premium_v2.js"></script>' not in root
    assert '<script src="/urbion_championship_premium_v4.js"></script>' not in root
    assert 'value="2.285"' not in root
    assert 'value="102.196"' not in root
    assert 'value="4.5"' not in root


def test_canonical_shell_has_no_global_mutation_or_polling_loops():
    js = SHELL.read_text(encoding="utf-8")
    assert "MutationObserver" not in js
    assert "setInterval(" not in js
    assert 'value="2.285"' not in js
    assert 'value="4.5"' not in js
    for endpoint in (
        "/assess",
        "/spatial/site-context",
        "/what-if",
        "/lcp/intelligence",
        "/copilot/run",
        "/copilot/explain",
        "/station-intelligence",
        "/judge/demo",
    ):
        assert endpoint in js


def test_canonical_shell_exposes_single_map_and_required_case_flow():
    js = SHELL.read_text(encoding="utf-8")
    assert "window.__URBION_FCC_MAP__=map" in js
    for token in (
        "State",
        "Pihak Berkuasa Tempatan (PBT)",
        "District / Daerah",
        "Lot / UPI Reference",
        "Project Reference",
        "Guna Tanah 1",
        "Guna Tanah 2",
        "Guna Tanah 3",
        "Development / Proposal",
        "Intensity / Plot Ratio",
        "CASE HISTORY",
        "STREET",
        "SATELLITE",
        "HYBRID",
        "DECISION",
        "OUTPUT",
    ):
        assert token in js


def test_canonical_shell_passes_node_syntax_check_when_available():
    node = shutil.which("node")
    if not node:
        return
    subprocess.run([node, "--check", str(SHELL)], check=True, capture_output=True, text=True)
