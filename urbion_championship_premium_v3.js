(()=>{
'use strict';
if(window.__URBION_PREMIUM_V3)return;window.__URBION_PREMIUM_V3=true;
function boot(){
 const root=document.getElementById('urbion-final-command-centre');if(!root)return;
 if(document.getElementById('urbion-premium-v3-style'))return;
 const s=document.createElement('style');s.id='urbion-premium-v3-style';
 s.textContent=`
#urbion-final-command-centre{font-family:Inter,ui-sans-serif,system-ui,sans-serif;font-size:14px;color:#eaf5f7}
#urbion-final-command-centre .fcc-kicker{font-size:10px!important;letter-spacing:.14em!important;font-weight:800!important;color:#67d9c0}
#urbion-final-command-centre .fcc-muted{font-size:12px!important;line-height:1.7!important;color:#8fa8b5!important}
#urbion-final-command-centre .fcc-header{height:72px!important;padding:0 28px!important}
#urbion-final-command-centre .fcc-brand img{width:192px!important}
#urbion-final-command-centre .fcc-brand b{font-size:15px!important;font-weight:750!important}
#urbion-final-command-centre .fcc-brand small{font-size:8px!important;letter-spacing:.16em!important}
#urbion-final-command-centre .fcc-system{font-size:9px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-head-actions button{font-size:12px!important}
#urbion-final-command-centre .fcc-case h1,#urbion-final-command-centre .fcc-rail h2{font-size:26px!important;font-weight:750!important;letter-spacing:-.035em!important}
#urbion-final-command-centre .fcc-step{margin-top:20px!important;margin-bottom:10px!important;font-size:11px!important}
#urbion-final-command-centre .fcc-step b{font-size:10px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-case label{font-size:10px!important;font-weight:650!important;letter-spacing:.01em!important}
#urbion-final-command-centre .fcc-case input,#urbion-final-command-centre .fcc-case select{font-size:12px!important;min-height:40px!important;padding:10px 12px!important}
#urbion-final-command-centre .fcc-readiness span{font-size:9px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-readiness b{font-size:19px!important}
#urbion-final-command-centre .fcc-readiness small{font-size:10px!important;line-height:1.5!important}
#urbion-final-command-centre .fcc-run{font-size:10px!important;font-weight:850!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-reset{font-size:9px!important;letter-spacing:.06em!important}
#urbion-final-command-centre .fcc-status{font-size:10px!important;line-height:1.6!important}
#urbion-final-command-centre .fcc-commandbar h2{font-size:31px!important;font-weight:700!important;letter-spacing:-.04em!important;max-width:880px}
#urbion-final-command-centre .fcc-tabs button{font-size:10px!important;font-weight:750!important;letter-spacing:.02em!important}
#urbion-final-command-centre .fcc-map-head b{font-size:10px!important;letter-spacing:.04em!important}
#urbion-final-command-centre .fcc-map-head span{font-size:10px!important}
#urbion-final-command-centre .fcc-map-actions button{font-size:9px!important;font-weight:700!important}
#urbion-final-command-centre .fcc-layer-row b{font-size:10px!important}.fcc-layer-row small{font-size:9px!important}
#urbion-final-command-centre .fcc-card-head span{font-size:10px!important;letter-spacing:.06em!important}.fcc-card-head>b{font-size:17px!important}
#urbion-final-command-centre .fcc-card strong{font-size:19px!important}.fcc-card p{font-size:11px!important;line-height:1.7!important}
#urbion-final-command-centre .fcc-chain span{font-size:10px!important;padding:12px!important}.fcc-chain small{font-size:9px!important;line-height:1.55!important}
#urbion-final-command-centre .fcc-signal{font-size:10px!important}.fcc-signal b{font-size:8px!important}.fcc-health-list span{font-size:9px!important}.fcc-health-list small{font-size:8px!important}
#urbion-final-command-centre .fcc-next strong{font-size:15px!important}
#urbion-final-command-centre .e-row{padding:12px 0!important}.e-row b{font-size:10px!important}.e-row small{font-size:9px!important}.e-row>strong,.e-row>span{font-size:9px!important}
#urbion-final-command-centre .scenario strong{font-size:32px!important}.scenario span{font-size:10px!important}.scenario button{font-size:9px!important}
#urbion-final-command-centre .fcc-decision-list div{font-size:10px!important;padding:10px!important}.output-grid strong{font-size:10px!important}.output-grid span{font-size:8px!important}
#urbion-final-command-centre .fcc-footer{font-size:9px!important}.fcc-footer b{font-size:9px!important}.fcc-footer button{font-size:9px!important}
#urbion-final-command-centre .fcc-modal-box h2{font-size:30px!important}.fcc-modal-box p{font-size:11px!important;line-height:1.8!important}
#urbion-final-command-centre .fcc-header{backdrop-filter:none!important}
#urbion-final-command-centre::after{display:none!important}
@media(max-width:900px){#urbion-final-command-centre .fcc-commandbar h2{font-size:27px!important}}
@media(max-width:600px){#urbion-final-command-centre .fcc-commandbar h2{font-size:23px!important}}
`;
 document.head.appendChild(s);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(boot,0),{once:true});else setTimeout(boot,0);
})();
