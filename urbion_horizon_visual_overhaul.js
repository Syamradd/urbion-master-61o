(()=>{
'use strict';
if(document.getElementById('urbion-horizon-visual-overhaul')) return;
const style=document.createElement('style');
style.id='urbion-horizon-visual-overhaul';
style.textContent=`
:root{--hz-cyan:#43e7ee;--hz-mint:#61efc6;--hz-blue:#62a9ff;--hz-bg:#04131d;--hz-panel:#071b27;--hz-line:rgba(87,214,230,.20);--hz-text:#eefaff;--hz-muted:#91aab7}
html,body{font-size:14px!important}
/* FORM SCALE: hierarchy-first, compact controls, no oversized values */
.sidebar .side-title{font-size:15px!important;line-height:1.25!important;font-weight:700!important;color:var(--hz-text)!important}
.sidebar .side-copy{font-size:11px!important;line-height:1.55!important}
.sidebar .label{font-size:8.5px!important;line-height:1.2!important;letter-spacing:.14em!important;margin:13px 0 6px!important}
.sidebar .input,.sidebar .select{font-size:13px!important;line-height:1.2!important;min-height:44px!important;padding:10px 12px!important;border-radius:10px!important}
.sidebar .input::placeholder{font-size:12px!important;color:#7894a2!important}
.sidebar .run{font-size:10px!important;min-height:44px!important}
.sidebar .reset{font-size:9px!important;min-height:38px!important}
.sidebar .side-status{font-size:9px!important}
/* RIGHT RAIL: readable, balanced with the form */
.main .card h2{font-size:18px!important;line-height:1.15!important}
.main .card h3{font-size:14px!important}
.main .muted{font-size:10px!important;line-height:1.55!important}
.main .row{font-size:10px!important;padding:10px!important}
.main .row span{font-size:10px!important}
.main .site-name{font-size:22px!important}
.main .site-meta{font-size:10px!important;line-height:1.6!important}
.main .kpi label{font-size:8px!important}
.main .kpi strong{font-size:25px!important}
.main .kpi em{font-size:8px!important}
.main .e b{font-size:10px!important}.main .e small{font-size:8px!important}
.main .tag{font-size:7px!important}.main .bullet{font-size:9px!important;line-height:1.55!important}
.main .indicator-top{font-size:9px!important}.main .metric b{font-size:13px!important}.main .metric small{font-size:8px!important}
.main .scenario h3{font-size:15px!important}.main .scenario p{font-size:9px!important}.main .scenario .big{font-size:28px!important}
.main .table{font-size:9px!important}.main .table th{font-size:8px!important}.main .table td{font-size:9px!important}
.main .notice{font-size:8px!important}
.main .nav button{font-size:9px!important;padding:9px 12px!important}
.main .btn{font-size:9px!important}
/* Premium contrast + spacing */
.hero-card,.card{box-shadow:0 18px 55px rgba(0,0,0,.28),0 0 28px rgba(67,231,238,.035)!important}
.sidebar{background:linear-gradient(180deg,rgba(5,18,28,.97),rgba(5,18,28,.90))!important}
/* CINEMATIC VISUAL LAYER */
.hz-visual{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden;opacity:.78}
.hz-grid{position:absolute;inset:-10%;background-image:linear-gradient(rgba(77,218,228,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(77,218,228,.035) 1px,transparent 1px);background-size:54px 54px;mask-image:radial-gradient(circle at 67% 38%,#000 0 34%,transparent 76%)}
.hz-glow{position:absolute;width:62vw;height:62vw;right:-22vw;top:-26vw;border-radius:50%;background:radial-gradient(circle,rgba(61,230,236,.12),transparent 62%);filter:blur(10px);animation:hzPulse 7s ease-in-out infinite}
.hz-orbit{position:absolute;right:-11vw;top:14vh;width:48vw;height:20vw;border:1px solid rgba(74,224,232,.16);border-radius:50%;transform:rotate(-14deg);box-shadow:0 0 60px rgba(67,231,238,.045);animation:hzFloat 11s ease-in-out infinite}
.hz-orbit.two{right:-16vw;top:24vh;width:57vw;height:25vw;opacity:.55;animation-duration:15s;animation-direction:reverse}
.hz-scan{position:absolute;left:0;right:0;top:12vh;height:1px;background:linear-gradient(90deg,transparent,rgba(97,239,198,.0),rgba(67,231,238,.58),rgba(97,239,198,.0),transparent);box-shadow:0 0 22px rgba(67,231,238,.32);animation:hzScan 8s linear infinite}
.hz-city{position:absolute;left:0;right:0;bottom:0;height:22vh;display:flex;align-items:flex-end;gap:4px;padding:0 2%;opacity:.28;background:linear-gradient(180deg,transparent,rgba(0,7,12,.68) 45%,rgba(0,6,11,.96))}
.hz-building{flex:1;max-width:70px;height:var(--h);border:1px solid rgba(72,210,225,.13);background:linear-gradient(180deg,rgba(23,80,101,.28),rgba(2,11,17,.94));clip-path:polygon(8% 0,92% 0,100% 100%,0 100%);transform-origin:bottom;animation:hzTower 8s ease-in-out infinite}
.hz-building:after{content:"";display:block;height:72%;margin:13% 18%;background:repeating-linear-gradient(180deg,rgba(116,230,240,.25) 0 2px,transparent 2px 12px);opacity:.45}
.hz-node{position:absolute;display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid rgba(74,221,231,.17);border-radius:999px;background:rgba(3,17,27,.66);backdrop-filter:blur(10px);font:800 8px Inter,sans-serif;letter-spacing:.09em;color:#9edfe5;box-shadow:0 10px 28px rgba(0,0,0,.18);animation:hzNode 5s ease-in-out infinite}
.hz-node i{width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,var(--hz-cyan),var(--hz-mint));box-shadow:0 0 11px rgba(67,231,238,.65)}
.hz-n1{right:7vw;top:18vh}.hz-n2{right:18vw;top:34vh;animation-delay:-1.4s}.hz-n3{left:39vw;bottom:12vh;animation-delay:-2.6s}.hz-n4{left:8vw;top:22vh;animation-delay:-3.8s}
.hz-data{position:absolute;right:5vw;bottom:26vh;width:210px;padding:12px;border:1px solid rgba(75,219,229,.16);border-radius:12px;background:rgba(4,18,28,.60);backdrop-filter:blur(11px);font:700 8px Inter,sans-serif;color:#8fb5c0;box-shadow:0 18px 45px rgba(0,0,0,.24)}
.hz-data b{display:block;color:#cfeaf0;font-size:9px;margin-bottom:8px;letter-spacing:.08em}.hz-data .bar{height:5px;margin:6px 0 9px;background:#102835;border-radius:9px;overflow:hidden}.hz-data .bar i{display:block;height:100%;width:var(--w);background:linear-gradient(90deg,var(--hz-cyan),var(--hz-mint));border-radius:9px;animation:hzData 2.6s ease-in-out infinite alternate}
/* keep controls above visual */
.app,.header,.sidebar,.main{position:relative;z-index:3}
@keyframes hzPulse{0%,100%{transform:scale(.96);opacity:.7}50%{transform:scale(1.04);opacity:1}}
@keyframes hzFloat{0%,100%{transform:rotate(-14deg) translate3d(0,0,0)}50%{transform:rotate(-11deg) translate3d(-12px,10px,0)}}
@keyframes hzScan{0%{transform:translateY(-4vh);opacity:0}14%,70%{opacity:1}100%{transform:translateY(80vh);opacity:0}}
@keyframes hzNode{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes hzTower{0%,100%{filter:brightness(.82)}50%{filter:brightness(1.18)}}
@keyframes hzData{from{width:calc(var(--w) - 10%)}to{width:var(--w)}}
@media(max-width:900px){.hz-data,.hz-n1,.hz-n2{display:none}.hz-orbit{right:-28vw;width:90vw;height:30vw}.hz-grid{opacity:.65}}
@media(prefers-reduced-motion:reduce){.hz-glow,.hz-orbit,.hz-scan,.hz-building,.hz-node,.hz-data .bar i{animation:none!important}}
`;
document.head.appendChild(style);
function addVisual(){
 const v=document.createElement('div');v.className='hz-visual';v.innerHTML=`<div class="hz-grid"></div><div class="hz-glow"></div><div class="hz-orbit"></div><div class="hz-orbit two"></div><div class="hz-scan"></div><div class="hz-node hz-n1"><i></i>SPATIAL SIGNAL</div><div class="hz-node hz-n2"><i></i>POLICY GRAPH</div><div class="hz-node hz-n3"><i></i>DECISION CHAIN</div><div class="hz-node hz-n4"><i></i>LIVE EVIDENCE</div><div class="hz-data"><b>HORIZON INTELLIGENCE FIELD</b><span>SPATIAL COVERAGE</span><div class="bar"><i style="--w:86%"></i></div><span>EVIDENCE READINESS</span><div class="bar"><i style="--w:72%"></i></div><span>DECISION TRACE</span><div class="bar"><i style="--w:94%"></i></div></div><div class="hz-city">${[46,71,54,83,38,64,78,52,69,44,88,58,74,47,67,56,82,49,61,76,43,72].map(h=>`<span class="hz-building" style="--h:${h}%"></span>`).join('')}</div>`;
 document.body.prepend(v);
}
addVisual();
})();