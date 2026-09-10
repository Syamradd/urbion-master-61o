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

  const bindLanguageSweep = () => {
    const setLang = window.__URBION_HORIZON_SET_LANG__;
    if (typeof setLang !== "function" || !document.body) return false;
    const stored = String(localStorage.getItem("urbion-language") || "en").toLowerCase();
    setLang(stored.startsWith("ms") ? "ms" : "en");
    sweepEnglishText();

    if (!window.__URBION_HORIZON_LANGUAGE_OBSERVER__) {
      const observer = new MutationObserver(() => {
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
