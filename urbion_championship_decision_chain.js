(function(){
  function mount(){
    var panel=document.getElementById('decisionPanel'); if(!panel) return;
    var box=document.getElementById('chain')||document.getElementById('decision-chain');
    if(!box) return;
    if(box.id==='chain'){
      box.classList.add('urbion-live-chain');
      var style=document.createElement('style'); style.id='decision-chain-style';
      if(!document.getElementById(style.id)){
        style.textContent='.urbion-live-chain .node{transition:border-color .15s ease,box-shadow .15s ease}.urbion-live-chain .node.live{border-color:#5ee7c2aa;box-shadow:inset 0 0 0 1px #5ee7c222}.urbion-live-chain .node.warn{border-color:#ffc85788}.urbion-live-chain span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}';
        document.head.appendChild(style);
      }
    }
    function val(id){var e=document.getElementById(id);return e?e.textContent.trim():''}
    function refresh(){
      var score=val('score').replace('/ 100','').trim(),why=val('justification'),decision=val('decisionStatus');
      var gaps=document.querySelectorAll('#gaps .gap').length,actions=document.querySelectorAll('#actions .action').length;
      var isNew=box.id==='decision-chain';
      var map={EVIDENCE:val('context')?'Evidence linked':'Qualified',SCORE:score&&score!=='—'?score+'/100':'Not scored',WHY:why?why.slice(0,34):'Not returned',DECISION:decision||'Review',REVIEW:gaps?gaps+' gap(s)':'Review checklist',ACTION:actions?actions+' action(s)':'Confirm next step'};
      if(isNew){box.querySelectorAll('[data-dc]').forEach(function(n){var k=n.getAttribute('data-dc');n.classList.toggle('current',k==='DECISION'&&decision&&decision!=='EVIDENCE UNAVAILABLE');n.classList.toggle('warn',k==='REVIEW'&&gaps>0);n.querySelector('span').textContent=map[k]||'Awaiting'});}
      else {var keys=['evidence','score','why','decision','review','action'];box.querySelectorAll('.node[data-k]').forEach(function(n){var k=n.getAttribute('data-k');n.classList.toggle('live',!!map[k]);n.classList.toggle('warn',k==='review'&&gaps>0);var span=n.querySelector('span');if(span)span.textContent=map[{evidence:'EVIDENCE',score:'SCORE',why:'WHY',decision:'DECISION',review:'REVIEW',action:'ACTION'}[k]]||'Awaiting'});}
    }
    refresh(); new MutationObserver(refresh).observe(panel,{subtree:true,childList:true,characterData:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();