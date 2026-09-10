"use strict";
(() => {
  const apply = () => {
    const setLang = window.__URBION_HORIZON_SET_LANG__;
    if (typeof setLang !== "function") return false;
    const stored = String(localStorage.getItem("urbion-language") || "en").toLowerCase();
    setLang(stored.startsWith("ms") ? "ms" : "en");
    return true;
  };
  if (apply()) return;
  let tries = 0;
  const timer = setInterval(() => {
    tries += 1;
    if (apply() || tries >= 50) clearInterval(timer);
  }, 100);
})();
