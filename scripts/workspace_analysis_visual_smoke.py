"""Browser contract for site suitability, AI answer and station-map UI owners."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv('URBION_BASE_URL','http://127.0.0.1:8000')
PAYLOAD={
 'site_lat':2.285,'site_lon':102.196,'tod_lat':2.286,'tod_lon':102.196,
 'plot_ratio':4.5,'precinct':'Terminal Sg. Udang','development_type':'TOD Development / Mixed Use',
 'development_class':'Mixed Use','state':'Melaka','district':'Melaka Tengah',
 'pbt':'Majlis Bandaraya Melaka Bersejarah','lot_no':''
}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    page.goto(BASE+'/workspace',wait_until='domcontentloaded')
    result=page.evaluate("""async ({base,payload})=>{const r=await fetch(base+'/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const d=await r.json();Object.defineProperty(window,'URBION_LAST',{configurable:true,get:()=>d});window.dispatchEvent(new CustomEvent('urbion:assessment-ready'));return d}""",{'base':BASE,'payload':PAYLOAD})
    assert result.get('canonical_evidence_packet'),'canonical packet missing'
    sa=result['canonical_evidence_packet'].get('site_analysis') or {}
    assert isinstance(sa.get('score'),(int,float)),'site suitability score missing'
    assert len(sa.get('indicators') or [])>=4,'site suitability indicators missing'
    page.wait_for_timeout(1000)
    assert page.locator('[data-testid="development-impact"]').count()==1,'development impact card missing'
    assert page.locator('#urbionAnalysisSummary').count()==1,'site analysis summary missing'
    summary=page.locator('#urbionAnalysisSummary').inner_text()
    assert 'SITE SUITABILITY' in summary and '%' in summary,'suitability percentage not rendered'
    assert 'AI PLANNING ANSWER' in summary,'AI answer surface missing'
    assert page.locator('#urbionStationMapCard').count()==1,'station map control missing'
    assert page.locator('#urbionRoadLaunch').count()==1,'road access control missing'
    print('WORKSPACE ANALYSIS VISUAL CONTRACT PASS')
    print({'suitability_score':sa.get('score'),'dimensions_assessed':(sa.get('score_coverage') or {}).get('assessed_dimensions'),'indicators':len(sa.get('indicators') or [])})
    browser.close()
