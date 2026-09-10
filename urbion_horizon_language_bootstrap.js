"use strict";
(() => {
  const BM_TO_EN = [
    ["Gambaran Keseluruhan", "Overview"],
    ["Kecerdasan Tapak", "Site Intelligence"],
    ["Penilaian AI", "AI Assessment"],
    ["Bagaimana Jika", "What-If Studio"],
    ["Pusat Keputusan", "Decision Centre"],
    ["Kecerdasan LCP", "LCP Intelligence"],
    ["Pihak Berkuasa Tempatan", "Local Authority"],
    ["Guna Tanah", "Land Use"],
    ["JALANKAN ANALISIS TAPAK", "RUN SITE ANALYSIS"],
    ["LAPISAN PETA", "MAP LAYERS"],
  ];

  const ensureVisualSafety = () => {
    if (!document.head || document.getElementById("urbion-horizon-visual-safety")) return;
    const style = document.createElement("style");
    style.id = "urbion-horizon-visual-safety";
    style.textContent = [
      "body.horizon-ui .hero h1{height:auto!important;min-height:0!important;overflow:visible!important;display:block!important;}"
    ].join("");
    document.head.appendChild(style);
  };

  const sweepEnglishText = () => {
    if (document.documentElement.lang !== "en" || !document.body) return;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    let node;
    while ((node = walker.nextNode())) nodes.push(node);
    for (const textNode of nodes) {
      let text = textNode.nodeValue || "";
      for (const [bm, en] of BM_TO_EN) text = text.split(bm).join(en);
      if (text !== textNode.nodeValue) textNode.nodeValue = text;
    }
  };

  const findActivePlannerTab = () =>
    document.querySelector(".workbench-nav button.active[data-tab]")?.dataset.tab || null;

  const clickPlannerTab = (tab) => {
    if (!tab) return false;
    const target = document.querySelector(`.workbench-nav button[data-tab="${CSS.escape(tab)}"]`);
    if (!target) return false;
    target.click();
    return true;
  };

  // Keep the latest explicit user tab choice authoritative over asynchronous
  // station/data callbacks. A later user click replaces this preference.
  const bindPlannerTabRaceGuard = () => {
    if (!document.body || window.__URBION_PLANNER_TAB_RACE_GUARD__) return;
    window.__URBION_PLANNER_TAB_RACE_GUARD__ = true;
    let requestedTab = null;
    let replaying = false;

    document.addEventListener("click", (event) => {
      const button = event.target?.closest?.(".workbench-nav button[data-tab]");
      if (!button || replaying) return;
      requestedTab = button.dataset.tab || null;
    }, true);

    const reconcile = () => {
      if (!requestedTab || replaying) return;
      const active = findActivePlannerTab();
      if (active === requestedTab) return;
      replaying = true;
      try {
        clickPlannerTab(requestedTab);
      } finally {
        setTimeout(() => { replaying = false; }, 0);
      }
    };

    const observer = new MutationObserver(() => {
      if (!replaying) requestAnimationFrame(reconcile);
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class"],
    });
    window.__URBION_PLANNER_TAB_RACE_OBSERVER__ = observer;
  };

  const bindLanguageSweep = () => {
    const setLang = window.__URBION_HORIZON_SET_LANG__;
    if (typeof setLang !== "function" || !document.body) return false;
    ensureVisualSafety();
    bindPlannerTabRaceGuard();
    const stored = String(localStorage.getItem("urbion-language") || "en").toLowerCase();
    setLang(stored.startsWith("ms") ? "ms" : "en");
    sweepEnglishText();

    if (!window.__URBION_HORIZON_LANGUAGE_OBSERVER__) {
      const observer = new MutationObserver(() => {
        ensureVisualSafety();
        if (document.documentElement.lang === "en") sweepEnglishText();
      });
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
      window.__URBION_HORIZON_LANGUAGE_OBSERVER__ = observer;
    }
    return true;
  };

  if (bindLanguageSweep()) return;
  let tries = 0;
  const timer = setInterval(() => {
    tries += 1;
    if (bindLanguageSweep() || tries >= 50) clearInterval(timer);
  }, 100);
})();
