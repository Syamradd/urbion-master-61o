"use strict";
(() => {
  const BM_TO_EN = [
    ["Gambaran Keseluruhan", "Overview"], ["Kecerdasan Tapak", "Site Intelligence"], ["Penilaian AI", "AI Assessment"], ["Bagaimana Jika", "What-If Studio"], ["Pusat Keputusan", "Decision Centre"], ["Kecerdasan LCP", "LCP Intelligence"], ["Pihak Berkuasa Tempatan", "Local Authority"], ["Guna Tanah", "Land Use"], ["JALANKAN ANALISIS TAPAK", "RUN SITE ANALYSIS"], ["LAPISAN PETA", "MAP LAYERS"],
  ];
  const ensureVisualSafety = () => { if (!document.head || document.getElementById("urbion-horizon-visual-safety")) return; const style=document.createElement("style"); style.id="urbion-horizon-visual-safety"; style.textContent="body.horizon-ui .hero h1{height:auto!important;min-height:0!important;overflow:visible!important;display:block!important;}"; document.head.appendChild(style); };
  const ensureLayerDrawerScroll = () => {
    const drawer = document.querySelector("#cs-layer-drawer");
    if (!drawer) return;
    let target = drawer.querySelector(".horizon-layer-scroll");
    if (!target) {
      const candidates = Array.from(drawer.children).filter(el => el.querySelector?.(".fcc-layer-row"));
      if (candidates.length === 1) {
        target = candidates[0];
      } else if (candidates.length > 1) {
        target = document.createElement("div");
        target.className = "horizon-layer-scroll";
        drawer.insertBefore(target, candidates[0]);
        for (const child of candidates) target.appendChild(child);
      } else {
        const rows = drawer.querySelectorAll(".fcc-layer-row");
        if (rows.length < 4) return;
        target = document.createElement("div");
        target.className = "horizon-layer-scroll";
        const parent = rows[0].parentElement;
        if (!parent) return;
        parent.insertBefore(target, rows[0]);
        for (const child of Array.from(parent.children)) {
          if (child !== target && child.querySelector?.(".fcc-layer-row")) target.appendChild(child);
        }
      }
      target.classList.add("horizon-layer-scroll");
    }
    target.style.minHeight = "0";
    target.style.flex = "1 1 auto";
    target.style.overflowY = "auto";
    target.style.overflowX = "hidden";
    target.style.maxHeight = "calc(100% - 56px)";
  };
  const ensureFileIntakeButtonSemantics = () => {
    const backdrop = document.querySelector("#urbion-files-backdrop");
    if (!backdrop) return;
    const close = Array.from(backdrop.querySelectorAll("button.urbion-settings-close")).find(button => button.id !== "urbion-files-add" && button.id !== "urbion-files-clear" && button.textContent.trim().toLowerCase() === "close");
    if (!close) return;
    for (const id of ["urbion-files-add", "urbion-files-clear"]) {
      const button = backdrop.querySelector(`#${id}`);
      button?.classList.remove("urbion-settings-close");
    }
    close.classList.add("urbion-settings-close");
  };
  const sweepEnglishText = () => { if (document.documentElement.lang !== "en" || !document.body) return; const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); const nodes=[]; let node; while((node=walker.nextNode())) nodes.push(node); for(const textNode of nodes){let text=textNode.nodeValue||""; for(const [bm,en] of BM_TO_EN) text=text.split(bm).join(en); if(text!==textNode.nodeValue) textNode.nodeValue=text;} };
  const findActivePlannerTab=()=>document.querySelector(".workbench-nav button.active[data-tab]")?.dataset.tab||null;
  const clickPlannerTab=tab=>{if(!tab)return false; const target=document.querySelector(`.workbench-nav button[data-tab="${CSS.escape(tab)}"]`); if(!target)return false; target.click(); return true;};
  const bindPlannerTabRaceGuard=()=>{if(!document.body||window.__URBION_PLANNER_TAB_RACE_GUARD__)return; window.__URBION_PLANNER_TAB_RACE_GUARD__=true; let requestedTab=null,replaying=false; document.addEventListener("click",event=>{const button=event.target?.closest?.(".workbench-nav button[data-tab]"); if(!button||replaying)return; requestedTab=button.dataset.tab||null;},true); const reconcile=()=>{if(!requestedTab||replaying)return; const active=findActivePlannerTab(); if(active===requestedTab)return; replaying=true; try{clickPlannerTab(requestedTab);}finally{setTimeout(()=>{replaying=false;},0);}}; const observer=new MutationObserver(()=>{if(!replaying)requestAnimationFrame(reconcile);}); observer.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]}); window.__URBION_PLANNER_TAB_RACE_OBSERVER__=observer;};
  const bindAuthoritativeThemeToggle=()=>{if(!document.body||window.__URBION_AUTHORITATIVE_THEME_CAPTURE_GUARD__)return false; window.__URBION_AUTHORITATIVE_THEME_CAPTURE_GUARD__=true; const applyTheme=light=>{const html=document.documentElement; localStorage.setItem("urbion-theme",light?"light":"dark"); html.classList.toggle("cs-light",light); const logo=document.querySelector("#cs-logo"); if(logo)logo.src=light?"/urbion_logo_light.svg":"/urbion_logo_dark.svg";}; applyTheme(localStorage.getItem("urbion-theme")==="light"); document.addEventListener("click",event=>{const button=event.target?.closest?.("#cs-theme"); if(!button)return; event.preventDefault(); event.stopPropagation(); event.stopImmediatePropagation(); applyTheme(!document.documentElement.classList.contains("cs-light"));},true); return true;};
  const bindLanguageSweep=()=>{const setLang=window.__URBION_HORIZON_SET_LANG__; if(typeof setLang!=="function"||!document.body)return false; ensureVisualSafety(); ensureLayerDrawerScroll(); ensureFileIntakeButtonSemantics(); bindPlannerTabRaceGuard(); bindAuthoritativeThemeToggle(); const stored=String(localStorage.getItem("urbion-language")||"en").toLowerCase(); setLang(stored.startsWith("ms")?"ms":"en"); sweepEnglishText(); if(!window.__URBION_HORIZON_LANGUAGE_OBSERVER__){const observer=new MutationObserver(()=>{ensureVisualSafety(); ensureLayerDrawerScroll(); ensureFileIntakeButtonSemantics(); if(document.documentElement.lang==="en")sweepEnglishText();}); observer.observe(document.body,{childList:true,subtree:true,characterData:true}); window.__URBION_HORIZON_LANGUAGE_OBSERVER__=observer;} return true;};
  if(bindLanguageSweep())return; let tries=0; const timer=setInterval(()=>{tries+=1; if(bindLanguageSweep()||tries>=50)clearInterval(timer);},100);
})();
