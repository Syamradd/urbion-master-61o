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
  function loadLcpOwner(){
    if(window.__URBION_LCP_READINESS_OWNER_V1__||document.querySelector('script[data-urbion-lcp-owner]'))return;
    const s=document.createElement('script');
    s.src='/urbion_workspace_lcp_readiness_owner.js';
    s.dataset.urbionLcpOwner='1';
    s.async=false;
    s.onerror=()=>console.warn('URBION LCP readiness owner unavailable; canonical analysis remains intact');
    (document.head||document.documentElement).appendChild(s);
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
        loadLcpOwner();
        return;
      }
      await sleep(50);
    }
    console.warn('URBION bridge: core function layer did not become available');
  }
  waitForCore().catch(e=>console.error('URBION bridge initialization failed',e));
})();