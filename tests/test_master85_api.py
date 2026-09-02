from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def base():
    return {"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"development_type":"Commercial Shop Frontage","development_class":"Commercial","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"DEMO-COM-02","landscaped_pedestrian_walkway":0.5,"shop_frontage_verified":True}


def test_what_if_executes_isolated_variants():
    payload={"baseline":base(),"variants":[{"id":"FIX-WALKWAY","name":"Fix walkway","overrides":{"landscaped_pedestrian_walkway":1.5}}]}
    response=client.post('/what-if',json=payload)
    assert response.status_code==200
    data=response.json()
    assert data["version"]=="PHASE-D.2"
    assert data["best_candidate"]=="FIX-WALKWAY"
    assert data["scenarios"][0]["status"]=="COMPLY"
    assert data["scenarios"][0]["status_changed"] is True


def test_what_if_preserves_non_mbmb_evidence_gate():
    b=base(); b.update({"state":"Selangor","district":"Klang","pbt":"Majlis Bandaraya DiRaja Klang","development_type":"Urban Mixed Use","development_class":"Mixed Use"})
    response=client.post('/what-if',json={"baseline":b,"variants":[{"id":"ALT","overrides":{"plot_ratio":3.5}}]})
    assert response.status_code==200
    assert response.json()["scenarios"][0]["status"]=="REQUIRES REVIEW"
