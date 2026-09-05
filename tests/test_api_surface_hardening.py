from championship_server import app


def _paths():
    return set(app.openapi().get("paths", {}))


def test_championship_api_exposes_core_planner_surfaces():
    paths = _paths()
    required = {
        "/health", "/assess", "/spatial/intelligence",
        "/workstation/analysis", "/intelligence/decision",
        "/agents/run", "/copilot/run", "/planner/handoff",
    }
    assert required <= paths


def test_championship_api_does_not_expose_statutory_decision_authority_route():
    paths = _paths()
    assert "/statutory/approve" not in paths
