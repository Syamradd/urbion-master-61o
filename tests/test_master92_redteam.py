from fastapi.testclient import TestClient
from server import app

client=TestClient(app)
BASE={"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"Commercial Shop Frontage","development_class":"Commercial","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"REDTEAM-01","landscaped_pedestrian_walkway":1.5,"shop_frontage_verified":True}

def test_redteam_invalid_coordinate_rejected():
    p=dict(BASE);p["site_lat"]=999
    assert client.post('/assess',json=p).status_code==422

def test_redteam_non_mbmb_never_promotes_to_comply():
    p=dict(BASE);p.update({"state":"Selangor","district":"Klang","pbt":"Majlis Bandaraya DiRaja Klang","development_type":"Urban Mixed Use","development_class":"Mixed Use"})
    assert client.post('/assess',json=p).json()["final_status"]=="REQUIRES REVIEW"

def test_redteam_outside_tod_tod_scheme_is_not_applicable():
    p=dict(BASE);p.update({"tod_lat":3.0,"tod_lon":102.9,"development_type":"TOD Development / Mixed Use","development_class":"Mixed Use"})
    assert client.post('/assess',json=p).json()["final_status"]=="NOT APPLICABLE"

def test_redteam_failed_shop_frontage_blocks():
    p=dict(BASE);p["landscaped_pedestrian_walkway"]=0.5
    assert client.post('/assess',json=p).json()["final_status"]=="NON-COMPLIANCE"
