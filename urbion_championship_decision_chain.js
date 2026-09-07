(function(){
  function mount(){
    var panel=document.getElementById('decisionPanel'); if(!panel) return;
    var box=document.getElementById('chain')||document.getElementById('decision-chain');
    if(!box) return;
    function val(id){var e=document.getElementById(id);return e?e.textContent.trim():''}
    var score=val('score').replace('/ 100','').trim(), why=val('justification'), decision=val('decisionStatus');
    var gaps=document.querySelectorAll('#gaps .gap').length, actions=document.querySelectorAll('#actions .action').length;
    var map={EVIDENCE:val('context')?'Evidence linked':'Qualified',SCORE:score&&score!=='—'?score+'/100':'Not scored',WHY:why?why.slice(0,34):'Not returned',DECISION:decision||'Review',REVIEW:gaps?gaps+' gap(s)':'Review checklist',ACTION:actions?actions+' action(s)':'Confirm next step'};
    box.querySelectorAll('[data-dc]').forEach(function(n){var k=n.getAttribute('data-dc');var span=n.querySelector('span');if(span)span.textContent=map[k]||'Awaiting'});
    box.querySelectorAll('.node[data-k]').forEach(function(n){var k=n.getAttribute('data-k');var span=n.querySelector('span');if(span)span.textContent=map[{evidence:'EVIDENCE',score:'SCORE',why:'WHY',decision:'DECISION',review:'REVIEW',action:'ACTION'}[k]]||'Awaiting'});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
