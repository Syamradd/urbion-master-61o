from championship_server import app


def test_championship_api_exposes_core_planner_surfaces():
    paths = {route.path for route in app.routes}
    required = {
        "/health", "/assess", "/spatial/intelligence",
        "/workstation/analysis", "/intelligence/decision",
        "/agents/run", "/copilot/run", "/planner/handoff",
    }
    assert required <= paths


def test_championship_api_does_not_expose_statutory_decision_authority_route():
    paths = {route.path for route in app.routes}
    assert "/statutory/approve" not in paths
