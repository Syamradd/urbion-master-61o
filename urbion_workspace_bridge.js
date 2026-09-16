/* URBION HORIZON — canonical core/runtime bridge.
   Stable writable bridge to the existing workspace function layer.
   No planning engine duplication; no replacement of canonical workspace. */
(()=>{
  'use strict';
  if(window.__URBION_WORKSPACE_BRIDGE_V2__) return;
  window.__URBION_WORKSPACE_BRIDGE_V2__=true;
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  let canonicalLast=null;
  let canonicalAnalysisError=null;
  const publish=data=>{
    if(!data||typeof data!=='object')return;
    canonicalLast=data;
    canonicalAnalysisError=null;
    try{window.URBION_LAST=data;}catch(_){ }
    try{window.dispatchEvent(new CustomEvent('urbion-analysis-captured',{detail:{status:data.__http_status||200,data}}));}catch(_){ }
    try{window.dispatchEvent(new CustomEvent('urbion:analysis-ready',{detail:data}));}catch(_){ }
  };
  const publishError=(error,status=0)=>{
    const message=String(error?.message||error||'Analysis request failed');
    canonicalAnalysisError={message,status:Number(status||0)};
    try{window.dispatchEvent(new CustomEvent('urbion-analysis-error',{detail:canonicalAnalysisError}));}catch(_){ }
  };
  const captureResponse=async(response,statusHint=0)=>{
    try{
      if(!response)return;
      const status=Number(statusHint||response.status||0);
      const clone=response.clone();
      let data=null;
      try{data=await clone.json();}
      catch(_){
        const text=await response.clone().text().catch(()=>"");
        if(text.trim())data={__analysis_error_text:text.slice(0,1000)};
      }
      if(status>=200&&status<300&&data&&typeof data==='object'){
        try{Object.defineProperty(data,'__http_status',{value:status,enumerable:false});}catch(_){data.__http_status=status;}
        publish(data);
      }else if(status>=400){
        const detail=data?.detail?.message||data?.detail?.code||data?.message||data?.detail||data?.__analysis_error_text||`HTTP ${status}`;
        publishError(String(detail),status);
      }
    }catch(error){publishError(error,statusHint);}
  };
  const originalFetch=window.fetch?.bind(window);
  if(originalFetch){
    window.fetch=(input,init)=>{
      const url=typeof input==='string'?input:(input?.url||'');
      const promise=originalFetch(input,init);
      if(String(url).includes('/workstation/analysis'))promise.then(r=>captureResponse(r)).catch(error=>publishError(error));
      return promise;
    };
  }
  const OriginalXHR=window.XMLHttpRequest;
  if(OriginalXHR?.prototype){
    const originalOpen=OriginalXHR.prototype.open;
    const originalSend=OriginalXHR.prototype.send;
    OriginalXHR.prototype.open=function(method,url){
      try{this.__urbionAnalysisUrl=String(url||'');}catch(_){this.__urbionAnalysisUrl='';}
      return originalOpen.apply(this,arguments);
    };
    OriginalXHR.prototype.send=function(){
      const xhr=this;
      if(String(xhr.__urbionAnalysisUrl||'').includes('/workstation/analysis')){
        const onLoad=()=>{
          if(xhr.status>=200&&xhr.status<300){
            let data=null;
            try{data=JSON.parse(xhr.responseText||'{}');}catch(_){data={__analysis_error_text:String(xhr.responseText||'').slice(0,1000)};}
            if(data&&typeof data==='object'){try{Object.defineProperty(data,'__http_status',{value:xhr.status,enumerable:false});}catch(_){data.__http_status=xhr.status;}publish(data);}
          }else if(xhr.status>=400){publishError(xhr.responseText||`HTTP ${xhr.status}`,xhr.status);}
        };
        const onError=()=>publishError('XMLHttpRequest network error',xhr.status||0);
        const onAbort=()=>publishError('XMLHttpRequest aborted',xhr.status||0);
        xhr.addEventListener('load',onLoad,{once:true});
        xhr.addEventListener('error',onError,{once:true});
        xhr.addEventListener('abort',onAbort,{once:true});
      }
      return originalSend.apply(this,arguments);
    };
  }
  function loadOwner(src,guard){
    if(window[guard]||document.querySelector(`script[data-urbion-owner=\"${src}\"]`))return;
    const s=document.createElement('script');s.src=src;s.dataset.urbionOwner=src;s.async=false;s.onerror=()=>console.warn(`URBION owner unavailable: ${src}`);(document.head||document.documentElement).appendChild(s);
  }
  function loadOwners(){
    loadOwner('/urbion_workspace_lcp_readiness_owner.js','__URBION_LCP_READINESS_OWNER_V1__');
    loadOwner('/urbion_workspace_concurrency_guard.js','__URBION_CONCURRENCY_GUARD_V1__');
  }
  async function waitFor(pred,tries=180,delay=100){for(let i=0;i<tries;i++){try{if(pred())return true}catch(_){}await sleep(delay)}return false}
  async function waitForCore(){
    for(let i=0;i<160;i++){
      if(typeof taxonomy!=='undefined' && typeof runAnalysis==='function' && typeof whatIfModal==='function' && typeof decisionModal==='function' && typeof outputModal==='function' && typeof loadLayers==='function'){
        try{
          Object.defineProperty(window,'URBION_LAST',{
            configurable:true,
            enumerable:true,
            get:()=>canonicalLast ?? (typeof lastResult!=='undefined'?lastResult:null),
            set:value=>{canonicalLast=value;canonicalAnalysisError=null;try{window.dispatchEvent(new CustomEvent('urbion-analysis-captured',{detail:{status:value?.__http_status||200,data:value}}));}catch(_){ }try{window.dispatchEvent(new CustomEvent('urbion:analysis-ready',{detail:value}));}catch(_){ }}
          });
        }catch(_){
          try{if(typeof lastResult!=='undefined' && lastResult)window.URBION_LAST=lastResult;}catch(__){}
        }
        const canonicalAnalyse=async()=>{
          canonicalLast=null;
          canonicalAnalysisError=null;
          try{if(typeof lastResult!=='undefined')lastResult=null;}catch(_){ }
          try{
            await runAnalysis();
          }catch(error){
            publishError(error);
            throw error;
          }
          if(typeof lastResult!=='undefined' && lastResult)window.URBION_LAST=lastResult;
          if(!window.URBION_LAST){
            await waitFor(()=>!!canonicalLast||!!canonicalAnalysisError,180,100);
          }
          if(window.URBION_LAST)return window.URBION_LAST;
          if(canonicalAnalysisError)throw Error(`Canonical analysis failed${canonicalAnalysisError.status?` (HTTP ${canonicalAnalysisError.status})`:''}: ${canonicalAnalysisError.message}`);
          throw Error('Analysis response was not captured by canonical bridge');
        };
        window.URBION_FINAL={
          GT:taxonomy,
          analyse:canonicalAnalyse,
          whatif:whatIfModal,
          decision:decisionModal,
          output:outputModal,
          loadLayers:loadLayers,
          refreshMap:()=>{try{if(typeof map!=='undefined'&&map)map.invalidateSize(true)}catch(_){} }
        };
        loadOwners();
        return;
      }
      await sleep(50);
    }
    console.warn('URBION bridge: core function layer did not become available');
  }
  function mountWorkspaceBrief(){
    if(window.__URBION_WORKSPACE_BRIEF_V1__||document.getElementById('urbionWorkspaceBrief'))return;
    window.__URBION_WORKSPACE_BRIEF_V1__=true;
    const addStyle=()=>{if(document.getElementById('urbionWorkspaceBriefStyle'))return;const s=document.createElement('style');s.id='urbionWorkspaceBriefStyle';s.textContent=`#urbionWorkspaceBrief{position:fixed;inset:0;z-index:2400;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(1,8,13,.62);backdrop-filter:blur(10px);animation:urbBriefFade .35s ease both;pointer-events:none}.urbBriefCard{position:relative;width:min(760px,92vw);border:1px solid rgba(47,225,233,.32);border-radius:20px;padding:30px;background:linear-gradient(145deg,rgba(5,24,34,.97),rgba(2,12,18,.985));box-shadow:0 28px 100px rgba(0,0,0,.55),0 0 60px rgba(47,225,233,.08);overflow:hidden;animation:urbBriefIn .55s cubic-bezier(.2,.8,.2,1) both;pointer-events:auto}.light #urbionWorkspaceBrief{background:rgba(226,241,245,.68)}.light .urbBriefCard{background:linear-gradient(145deg,rgba(255,255,255,.985),rgba(239,248,250,.985));box-shadow:0 28px 80px rgba(12,52,67,.2)}.urbBriefGrid{position:absolute;inset:0;background-image:linear-gradient(rgba(47,225,233,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(47,225,233,.045) 1px,transparent 1px);background-size:28px 28px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.9),transparent)}.urbBriefSweep{position:absolute;left:-10%;right:-10%;top:-20%;height:2px;background:linear-gradient(90deg,transparent,rgba(88,232,196,.0),rgba(47,225,233,.65),transparent);filter:blur(.2px);animation:urbBriefSweep 3.8s linear infinite}.urbBriefGlow{position:absolute;width:220px;height:220px;border-radius:50%;right:-80px;top:-80px;background:radial-gradient(circle,rgba(47,225,233,.16),transparent 65%);animation:urbBriefPulse 3.5s ease-in-out infinite}.urbBriefTop{position:relative;display:flex;align-items:center;gap:14px}.urbBriefTop img{width:178px;height:auto}.urbBriefEyebrow{font-size:8px;letter-spacing:.14em;color:var(--mint);font-weight:900}.urbBriefTitle{position:relative;margin:25px 0 7px;font:700 clamp(27px,4vw,43px)/1.04 'Space Grotesk',Inter,system-ui,sans-serif;letter-spacing:-.035em}.urbBriefCopy{position:relative;max-width:620px;font-size:10px;line-height:1.7;color:#a8c0c9}.light .urbBriefCopy{color:#5c727e}.urbBriefFlow{position:relative;display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:21px 0 24px}.urbBriefNode{padding:8px 11px;border:1px solid rgba(47,225,233,.24);border-radius:9px;background:rgba(47,225,233,.04);font-size:7px;font-weight:900;letter-spacing:.08em;animation:urbBriefNode 1s ease both}.urbBriefNode:nth-child(1){animation-delay:.22s}.urbBriefNode:nth-child(2){animation-delay:.38s}.urbBriefNode:nth-child(3){animation-delay:.54s}.urbBriefNode:nth-child(4){animation-delay:.7s}.urbBriefNode:nth-child(5){animation-delay:.86s}.urbBriefArrow{font-size:12px;color:var(--cyan);opacity:.55}.urbBriefMeta{position:relative;display:flex;justify-content:space-between;gap:12px;align-items:center;padding-top:14px;border-top:1px solid rgba(47,225,233,.13)}.urbBriefBoundary{font-size:6.5px;line-height:1.5;color:var(--muted);max-width:500px}.urbBriefBtn{border:1px solid rgba(47,225,233,.4);background:linear-gradient(100deg,rgba(88,232,196,.14),rgba(47,225,233,.1));color:var(--text);border-radius:9px;padding:9px 13px;font-size:7px;font-weight:900;letter-spacing:.08em;white-space:nowrap}.urbBriefBtn:hover{border-color:rgba(47,225,233,.75);box-shadow:0 0 20px rgba(47,225,233,.12)}@keyframes urbBriefFade{from{opacity:0}to{opacity:1}}@keyframes urbBriefIn{from{opacity:0;transform:translateY(18px) scale(.985)}to{opacity:1;transform:none}}@keyframes urbBriefSweep{0%{transform:translateY(-10px);opacity:0}15%{opacity:1}100%{transform:translateY(520px);opacity:0}}@keyframes urbBriefPulse{0%,100%{transform:scale(1);opacity:.65}50%{transform:scale(1.12);opacity:1}}@keyframes urbBriefNode{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}@media(max-width:680px){.urbBriefCard{padding:22px}.urbBriefTop img{width:155px}.urbBriefCopy{font-size:9px}.urbBriefFlow{gap:5px}.urbBriefMeta{align-items:flex-end;flex-direction:column}.urbBriefBtn{width:100%}}`;document.head.appendChild(s)};
    const show=()=>{addStyle();const wrap=document.createElement('div');wrap.id='urbionWorkspaceBrief';wrap.setAttribute('role','dialog');wrap.setAttribute('aria-modal','true');wrap.setAttribute('aria-labelledby','urbionBriefTitle');wrap.innerHTML=`<div class="urbBriefCard"><div class="urbBriefGrid"></div><div class="urbBriefSweep"></div><div class="urbBriefGlow"></div><div class="urbBriefTop"><img src="/urbion_logo_dark.svg" alt="URBION HORIZON"><span class="urbBriefEyebrow">PLANNING INTELLIGENCE WORKSPACE</span></div><div class="urbBriefTitle" id="urbionBriefTitle">FROM SPATIAL DATA TO PLANNING DECISIONS.</div><div class="urbBriefCopy">URBION brings together spatial evidence, planning policies, live environmental context and development parameters into one evidence-grounded planning workflow.</div><div class="urbBriefFlow"><span class="urbBriefNode">DEFINE</span><span class="urbBriefArrow">→</span><span class="urbBriefNode">ANALYSE</span><span class="urbBriefArrow">→</span><span class="urbBriefNode">TRACE EVIDENCE</span><span class="urbBriefArrow">→</span><span class="urbBriefNode">WHAT-IF</span><span class="urbBriefArrow">→</span><span class="urbBriefNode">DECISION</span></div><div class="urbBriefMeta"><div class="urbBriefBoundary">URBION supports planning analysis and evidence preparation. Final planning decisions remain with the responsible authority and professional planner.</div><button type="button" class="urbBriefBtn" id="urbionBriefEnter">ENTER WORKSPACE →</button></div></div>`;document.body.appendChild(wrap);const close=()=>{wrap.style.animation='urbBriefFade .22s ease reverse both';setTimeout(()=>wrap.remove(),190);};wrap.querySelector('#urbionBriefEnter')?.addEventListener('click',close);wrap.addEventListener('click',e=>{if(e.target===wrap)close()});document.addEventListener('keydown',function onKey(e){if(e.key==='Escape'&&document.getElementById('urbionWorkspaceBrief')){close();document.removeEventListener('keydown',onKey)}})};
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',show,{once:true});else show();
  }
  mountWorkspaceBrief();
  waitForCore().catch(e=>console.error('URBION bridge initialization failed',e));
})();