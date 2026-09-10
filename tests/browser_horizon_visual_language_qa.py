"""Browser acceptance for HORIZON visual, language and interaction behavior."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765"
BM_MARKERS = ("Gambaran Keseluruhan","Kecerdasan Tapak","Penilaian AI","Bagaimana Jika","Pusat Keputusan","Kecerdasan LCP","Pihak Berkuasa Tempatan","Guna Tanah","JALANKAN ANALISIS TAPAK","LAPISAN PETA")
EN_MARKERS = ("Command Centre","Site Intelligence","AI Assessment","What-If Studio","Decision Centre","LCP Intelligence","Local Authority (PBT)","Land Use","RUN SITE ANALYSIS","MAP LAYERS")
def visible_text(page): return page.locator("body").inner_text()
def main():
    screenshots=Path("/tmp/urbion-browser-qa"); screenshots.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(); page=browser.new_page(viewport={"width":1440,"height":1000},device_scale_factor=1)
        page.add_init_script("localStorage.removeItem('urbion-language'); localStorage.removeItem('urbion-lang'); localStorage.removeItem('urbion-theme');")
        page.goto(BASE+"/",wait_until="networkidle"); page.wait_for_timeout(1400)
        assert page.evaluate("document.documentElement.lang")=="en"
        text=visible_text(page); assert "Command Centre" in text; assert "Site Intelligence" in text; assert "RUN SITE ANALYSIS" in text; assert "About" in text or "About Us" in text; assert "Help" in text
        leaked=[m for m in BM_MARKERS if m in text]; assert not leaked, leaked
        page.screenshot(path=str(screenshots/"horizon-en.png"),full_page=True)
        overflow=page.evaluate("document.documentElement.scrollWidth-window.innerWidth"); assert overflow<=2,overflow
        for selector in ("h1",".hero h1","h2","button"):
            for box in page.locator(selector).all():
                if box.is_visible():
                    metrics=box.evaluate("el=>{const cs=getComputedStyle(el);return{w:el.getBoundingClientRect().width,sh:el.scrollHeight,ch:el.clientHeight,overflowY:cs.overflowY,overflowX:cs.overflowX}}")
                    assert metrics["w"]>0
                    if metrics["ch"]>0 and metrics["overflowY"] in ("hidden","clip"):
                        assert metrics["sh"]<=metrics["ch"]+2,(selector,metrics)
        for label in page.locator("label").all():
            if label.is_visible(): assert 8<=label.evaluate("el=>parseFloat(getComputedStyle(el).fontSize)")<=12
        for field in page.locator("input,select,textarea").all():
            if field.is_visible(): assert 12<=field.evaluate("el=>parseFloat(getComputedStyle(el).fontSize)")<=15
        for selector in ("#urbion-championship-shell","#cs-map","#cs-run","#cs-layer-drawer"):
            assert page.locator(selector).count()==1, selector
        primary=page.locator("#cs-run")
        assert primary.count()==1 and primary.is_visible()
        # The workspace hydrates asynchronously; wait for the canonical English
        # CTA after late Station/data renders rather than sampling a transient state.
        page.wait_for_function("""() => {
            const el = document.querySelector('#cs-run');
            return document.documentElement.lang === 'en' && el && el.innerText.trim() === 'RUN SITE ANALYSIS';
        }""", timeout=5000)
        assert primary.inner_text().strip() == "RUN SITE ANALYSIS"
        primary_style=primary.evaluate("el=>{const cs=getComputedStyle(el);return{backgroundImage:cs.backgroundImage,backgroundColor:cs.backgroundColor,borderColor:cs.borderTopColor,boxShadow:cs.boxShadow}}")
        assert primary_style["backgroundImage"]!="none" or primary_style["backgroundColor"] not in ("rgba(0, 0, 0, 0)","transparent")
        assert primary_style["boxShadow"]!="none"
        drawer=page.locator("#cs-layer-drawer"); assert drawer.count()==1 and drawer.is_visible(); checkbox=drawer.locator("input[data-layer]").first; assert checkbox.count()==1
        before=checkbox.is_checked(); checkbox.click(force=True); page.wait_for_timeout(500); assert checkbox.is_checked() is (not before); checkbox.click(force=True); page.wait_for_timeout(300); assert checkbox.is_checked() is before
        scroll_state=page.evaluate("""()=>{const d=document.querySelector('#cs-layer-drawer');if(!d)return null;const all=[...d.querySelectorAll('*')];const s=all.map(el=>({el,rows:el.querySelectorAll('.fcc-layer-row').length})).sort((a,b)=>b.rows-a.rows)[0]?.el;if(!s)return null;return{rows:s.querySelectorAll('.fcc-layer-row').length,scrollHeight:s.scrollHeight,clientHeight:s.clientHeight,overflowY:getComputedStyle(s).overflowY}}""")
        assert scroll_state and scroll_state["rows"]>=4 and scroll_state["overflowY"] in ("auto","scroll")
        close=drawer.locator("button.horizon-drawer-close"); assert close.count()==1; close.click(); page.wait_for_timeout(220); assert drawer.get_attribute("aria-hidden")=="true"
        layer_toggle=page.locator("button").filter(has_text="LAYERS").first
        if layer_toggle.count()==0: layer_toggle=page.locator("button").filter(has_text="LAPISAN").first
        assert layer_toggle.count()==1; layer_toggle.click(); page.wait_for_timeout(220); assert drawer.get_attribute("aria-hidden")=="false"
        toggle=page.locator('button,a,[role="button"]').filter(has_text="BM").first
        if toggle.count()==0: toggle=page.locator('button,a,[role="button"]').filter(has_text="EN").first
        assert toggle.count()==1 and toggle.is_visible(); toggle.click(); page.wait_for_timeout(800); assert page.evaluate("document.documentElement.lang")=="ms"
        bm_text=visible_text(page); assert any(m in bm_text for m in BM_MARKERS); assert not any(m in bm_text for m in EN_MARKERS); assert "Tentang Kami" in bm_text and "Bantuan" in bm_text and "Help" not in bm_text; page.screenshot(path=str(screenshots/"horizon-bm.png"),full_page=True)
        toggle=page.locator('button,a,[role="button"]').filter(has_text="EN").first; assert toggle.count()==1; toggle.click(); page.wait_for_timeout(800); assert page.evaluate("document.documentElement.lang")=="en"; en_text=visible_text(page); assert "Command Centre" in en_text; assert not any(m in en_text for m in BM_MARKERS); assert "Help" in en_text; page.screenshot(path=str(screenshots/"horizon-en-restored.png"),full_page=True)
        browser.close()
if __name__=="__main__": main()
