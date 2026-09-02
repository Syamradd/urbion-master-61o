/* URBION shared UI controller: bilingual labels + light/dark theme. */
(function(){
  const KEY_LANG='urbion-lang', KEY_THEME='urbion-theme';
  const dict={en:{language:'Language',dark:'Dark mode',light:'Light mode',system:'System',layers:'Map layers',basemap:'Basemap',planning:'Planning',cadastre:'Cadastre',terrain:'Terrain',geology:'Geology',environment:'Environment',source:'Source context',verify:'Planner verification required',current:'Current land use',zoning:'Zoning',committed:'Committed land use',lot:'Cadastral lot',contour:'5m contours'},ms:{language:'Bahasa',dark:'Mod gelap',light:'Mod cerah',system:'Sistem',layers:'Lapisan peta',basemap:'Peta asas',planning:'Perancangan',cadastre:'Kadaster',terrain:'Bentuk muka bumi',geology:'Geologi',environment:'Alam sekitar',source:'Konteks sumber',verify:'Pengesahan perancang diperlukan',current:'Guna tanah semasa',zoning:'Guna tanah zoning',committed:'Guna tanah komited',lot:'Lot kadaster',contour:'Kontur 5m'}};
  function lang(){return localStorage.getItem(KEY_LANG)||'ms'}
  function theme(){return localStorage.getItem(KEY_THEME)||'dark'}
  function apply(){document.documentElement.dataset.lang=lang();document.documentElement.dataset.theme=theme();document.dispatchEvent(new CustomEvent('urbion-ui',{detail:{lang:lang(),theme:theme(),t:dict[lang()]}}))}
  window.URBION_UI={dict,get lang(){return lang()},get theme(){return theme()},t(k){return dict[lang()][k]||k},setLang(v){localStorage.setItem(KEY_LANG,v==='en'?'en':'ms');apply()},setTheme(v){localStorage.setItem(KEY_THEME,['dark','light','system'].includes(v)?v:'dark');apply()},apply};
  apply();
})();