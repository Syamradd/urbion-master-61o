from pathlib import Path
from fastapi.testclient import TestClient
from server import app


def test_deployment_health_and_key_routes():
    client=TestClient(app)
    health=client.get('/health')
    assert health.status_code==200
    assert health.json()['status']=='healthy'
    assert health.json()['engine']=='URBION PHASE-E.8'
    assert health.json()['frontend']=='SERVING_INDEX_HTML'
    assert client.get('/metadata').status_code==200
    assert client.get('/sources').status_code==200
    assert client.get('/map/layers?state=Melaka').status_code==200
    assert any(getattr(r,'path',None)=='/lcp/intelligence' for r in app.routes)


def test_deployment_frontend_surfaces_exist():
    for name in ('index.html','map-studio.html','what-if.html','decision-center.html','planner-review.html','lcp-intelligence.html'):
        assert Path(name).is_file(), name
