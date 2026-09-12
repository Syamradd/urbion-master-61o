/* URBION HORIZON — planning input data adapter.
   Purpose: populate the Local Authority (PBT) control from one authoritative
   2026 KPKT-derived catalog without creating another workspace or planning engine.
   This adapter owns only PBT option population; canonical UI remains the owner
   of the broader planning workflow.
*/
(()=>{
  'use strict';
  if(window.__URBION_PBT_CATALOG_V1__) return;
  window.__URBION_PBT_CATALOG_V1__=true;

  const PBT_BY_STATE={
    'Johor':[
      'Majlis Bandaraya Iskandar Puteri','Majlis Bandaraya Johor Bahru','Majlis Bandaraya Pasir Gudang',
      'Majlis Daerah Kota Tinggi','Majlis Daerah Labis','Majlis Daerah Mersing','Majlis Daerah Simpang Renggam','Majlis Daerah Tangkak','Majlis Daerah Yong Peng',
      'Majlis Perbandaran Batu Pahat','Majlis Perbandaran Kluang','Majlis Perbandaran Kulai','Majlis Perbandaran Muar','Majlis Perbandaran Pengerang','Majlis Perbandaran Pontian','Majlis Perbandaran Segamat'
    ],
    'Kedah':[
      'Majlis Bandaraya Alor Setar','Majlis Perbandaran Kulim','Majlis Perbandaran Sungai Petani','Majlis Perbandaran Langkawi Bandaraya Pelancongan','Majlis Perbandaran Kubang Pasu',
      'Majlis Daerah Baling','Majlis Daerah Bandar Baharu','Majlis Daerah Padang Terap','Majlis Daerah Pendang','Majlis Daerah Sik','Majlis Daerah Yan'
    ],
    'Kelantan':[
      'Majlis Perbandaran Kota Bharu Bandaraya Islam','Majlis Daerah Bachok','Majlis Daerah Gua Musang','Majlis Daerah Ketereh','Majlis Daerah Dabong','Majlis Daerah Kuala Krai','Majlis Daerah Machang','Majlis Daerah Pasir Mas','Majlis Daerah Pasir Puteh','Majlis Daerah Tanah Merah','Majlis Daerah Tumpat','Majlis Daerah Jeli'
    ],
    'Melaka':[
      'Majlis Bandaraya Melaka Bersejarah','Majlis Perbandaran Alor Gajah','Majlis Perbandaran Hang Tuah Jaya','Majlis Perbandaran Jasin'
    ],
    'Negeri Sembilan':[
      'Majlis Bandaraya Seremban','Majlis Perbandaran Port Dickson','Majlis Perbandaran Jempol','Majlis Daerah Jelebu','Majlis Daerah Kuala Pilah','Majlis Daerah Rembau','Majlis Daerah Tampin'
    ],
    'Pahang':[
      'Majlis Bandaraya Kuantan','Majlis Perbandaran Temerloh','Majlis Perbandaran Bentong','Majlis Perbandaran Pekan','Majlis Daerah Cameron Highlands','Majlis Daerah Jerantut','Majlis Daerah Lipis','Majlis Daerah Maran','Majlis Daerah Raub','Majlis Daerah Rompin','Majlis Daerah Bera'
    ],
    'Pulau Pinang':['Majlis Bandaraya Pulau Pinang','Majlis Bandaraya Seberang Perai'],
    'Perak':[
      'Majlis Bandaraya Ipoh','Majlis Perbandaran Manjung','Majlis Perbandaran Kuala Kangsar','Majlis Perbandaran Taiping','Majlis Perbandaran Teluk Intan',
      'Majlis Daerah Kampar','Majlis Daerah Gerik','Majlis Daerah Kerian','Majlis Daerah Batu Gajah','Majlis Daerah Lenggong','Majlis Daerah Pengkalan Hulu','Majlis Daerah Perak Tengah','Majlis Daerah Selama','Majlis Daerah Tanjong Malim','Majlis Daerah Tapah'
    ],
    'Perlis':['Majlis Perbandaran Kangar'],
    'Selangor':[
      'Majlis Bandaraya Diraja Klang','Majlis Bandaraya Petaling Jaya','Majlis Bandaraya Shah Alam','Majlis Bandaraya Subang Jaya',
      'Majlis Daerah Sabak Bernam','Majlis Perbandaran Ampang Jaya','Majlis Perbandaran Hulu Selangor','Majlis Perbandaran Kajang','Majlis Perbandaran Kuala Langat','Majlis Perbandaran Kuala Selangor','Majlis Perbandaran Selayang','Majlis Perbandaran Sepang'
    ],
    'Terengganu':[
      'Majlis Bandaraya Kuala Terengganu','Majlis Perbandaran Kemaman','Majlis Perbandaran Dungun','Majlis Daerah Besut','Majlis Daerah Hulu Terengganu','Majlis Daerah Marang','Majlis Daerah Setiu'
    ],
    'Sabah':[
      'Dewan Bandaraya Kota Kinabalu','Majlis Perbandaran Sandakan','Majlis Perbandaran Tawau',
      'Majlis Daerah Beaufort','Majlis Daerah Beluran','Majlis Daerah Keningau','Majlis Daerah Kinabatangan','Majlis Daerah Kota Belud','Majlis Daerah Kota Marudu','Majlis Daerah Kuala Penyu','Majlis Daerah Kunak','Majlis Daerah Lahad Datu','Majlis Daerah Nabawan','Majlis Daerah Papar','Majlis Daerah Penampang','Majlis Daerah Ranau','Majlis Daerah Semporna','Majlis Daerah Sipitang','Majlis Daerah Tambunan','Majlis Daerah Tenom','Majlis Daerah Tuaran','Lembaga Bandaran Kudat','Majlis Daerah Pitas','Majlis Daerah Putatan','Majlis Daerah Tongod','Majlis Daerah Telupid'
    ],
    'Sarawak':[
      'Dewan Bandaraya Kuching Utara','Majlis Bandaraya Kuching Selatan','Majlis Bandaraya Miri',
      'Majlis Perbandaran Padawan','Majlis Perbandaran Sibu','Majlis Perbandaran Kota Samarahan','Lembaga Kemajuan Bintulu (Perbandaran)',
      'Majlis Daerah Bau','Majlis Daerah Betong','Majlis Daerah Dalat & Mukah','Majlis Daerah Kanowit','Majlis Daerah Kapit','Majlis Daerah Lawas','Majlis Daerah Luar Bandar Sibu','Majlis Daerah Lubok Antu','Majlis Daerah Maradong & Julau','Majlis Daerah Lundu','Majlis Daerah Marudi','Majlis Daerah Matu & Daro','Majlis Daerah Saratok','Majlis Daerah Sarikei','Majlis Daerah Serian','Majlis Daerah Simunjan','Majlis Daerah Sri Aman','Majlis Daerah Subis','Majlis Daerah Limbang','Majlis Daerah Gedong'
    ],
    'W.P. Kuala Lumpur':['Dewan Bandaraya Kuala Lumpur'],
    'W.P. Labuan':['Perbadanan Labuan (Wilayah Persekutuan)'],
    'W.P. Putrajaya':['Perbadanan Putrajaya (Wilayah Persekutuan)']
  };

  const STATE_ALIASES={
    'Wilayah Persekutuan':'W.P. Kuala Lumpur',
    'W.Persekutuan':'W.P. Kuala Lumpur',
    'W.P. Kuala Lumpur':'W.P. Kuala Lumpur',
    'W.P. Labuan':'W.P. Labuan',
    'W.P. Putrajaya':'W.P. Putrajaya',
    'N.Sembilan':'Negeri Sembilan'
  };

  function labelInput(text){
    const needle=text.toLowerCase();
    for(const row of document.querySelectorAll('.sec .row')){
      const lab=row.querySelector('.lab');
      if(lab && lab.textContent.trim().toLowerCase().includes(needle)) return row.querySelector('input,select,textarea');
    }
    return null;
  }

  function ensureSelect(){
    let pbt=labelInput('local authority');
    if(!pbt) return null;
    if(pbt.tagName!=='SELECT'){
      const select=document.createElement('select');
      for(const name of ['id','name','class','required','disabled','autocomplete','aria-label']) if(pbt.hasAttribute(name)) select.setAttribute(name,pbt.getAttribute(name));
      select.className=pbt.className||'select';
      select.dataset.pbtCatalogOwned='1';
      pbt.parentNode.replaceChild(select,pbt);
      pbt=select;
    }
    pbt.dataset.pbtCatalogOwned='1';
    return pbt;
  }

  function stateValue(){
    const s=document.getElementById('state')||labelInput('state');
    return s?.value||'';
  }

  function optionsFor(state){
    const key=STATE_ALIASES[state]||state;
    return PBT_BY_STATE[key]||[];
  }

  function setOptions(select,items){
    if(!select) return;
    const previous=select.value;
    select.innerHTML='<option value="">Select Local Authority</option>'+items.map(x=>`<option value="${String(x).replace(/[&<>\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[m]))}">${String(x).replace(/[&<>\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[m]))}</option>`).join('');
    if(previous && items.includes(previous)) select.value=previous;
  }

  function sync(){
    const pbt=ensureSelect(); if(!pbt) return;
    const items=optionsFor(stateValue());
    setOptions(pbt,items);
    pbt.dataset.pbtCount=String(items.length);
    if(items.length) pbt.removeAttribute('disabled');
  }

  async function boot(){
    for(let i=0;i<120;i++){
      const state=document.getElementById('state')||labelInput('state');
      const pbt=ensureSelect();
      if(state&&pbt){
        sync();
        if(!state.dataset.urbionPbtBound){
          state.dataset.urbionPbtBound='1';
          state.addEventListener('change',sync,false);
        }
        console.info('URBION PBT CATALOG READY',state.value,optionsFor(state.value).length);
        return;
      }
      await new Promise(r=>setTimeout(r,100));
    }
    console.warn('URBION PBT catalog: planning controls not ready');
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot,{once:true}); else boot();
})();
