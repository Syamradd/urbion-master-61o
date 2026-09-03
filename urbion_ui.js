/* URBION shared UI controller: bilingual labels + resilient light/dark/system theme. */
(function(){
  const KEY_LANG='urbion-lang',KEY_THEME='urbion-theme';
  const dict={en:{language:'Language',dark:'Dark mode',light:'Light mode',system:'System',layers:'Map layers',basemap:'Basemap',planning:'Planning',cadastre:'Cadastre',terrain:'Terrain',geology:'Geology',environment:'Environment',source:'Source context',verify:'Planner verification required',current:'Current land use',zoning:'Zoning',committed:'Committed land use',lot:'Cadastral lot',contour:'5m contours'},ms:{language:'Bahasa',dark:'Mod gelap',light:'Mod cerah',system:'Sistem',layers:'Lapisan peta',basemap:'Peta asas',planning:'Perancangan',cadastre:'Kadaster',terrain:'Bentuk muka bumi',geology:'Geologi',environment:'Alam sekitar',source:'Konteks sumber',verify:'Pengesahan perancang diperlukan',current:'Guna tanah semasa',zoning:'Zon guna tanah',committed:'Guna tanah komited',lot:'Lot kadaster',contour:'Kontur 5m'}};
  function lang(){return localStorage.getItem(KEY_LANG)||'en'}
  function theme(){return localStorage.getItem(KEY_THEME)||'system'}
  function apply(){const l=lang(),t=theme();document.documentElement.dataset.lang=l;document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t==='system'?'light dark':t;document.dispatchEvent(new CustomEvent('urbion-ui',{detail:{lang:l,theme:t,t:dict[l]}}))}
  window.URBION_UI={dict,get lang(){return lang()},get theme(){return theme()},t(k){return dict[lang()][k]||k},setLang(v){localStorage.setItem(KEY_LANG,v==='en'?'en':'ms');apply()},setTheme(v){localStorage.setItem(KEY_THEME,['dark','light','system'].includes(v)?v:'system');apply()},apply};
  apply();
})();