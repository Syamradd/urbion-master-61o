from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_workspace_and_source_contracts_exist():
    server = (ROOT / "landing_server.py").read_text(encoding="utf-8")
    workspace = (ROOT / "workspace_v5.html").read_text(encoding="utf-8")
    about = (ROOT / "urbion_horizon_about.html").read_text(encoding="utf-8")

    assert "WORKSPACE_FILE = BASE_DIR / \"workspace_v5.html\"" in server
    assert 'if path == "/workspace": return _workspace()' in server
    assert "<script src=\"/urbion_workspace_bridge.js\"></script>" in server
    assert "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms" in workspace
    for token in ("GTzoning", "KONTUR5M", "LOT", "STATE_CODES", "SOURCE UNAVAILABLE"):
        assert token in workspace
    assert "Turning spatial evidence into" in about


def test_finalization_does_not_expose_temporary_probe_files():
    probe_files = list(ROOT.glob("tmp_probe*.js"))
    assert probe_files == []
