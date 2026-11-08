(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
function ls(op,k,v){try{return op==='g'?localStorage.getItem(k):localStorage.setItem(k,v)}catch(e){return null}}
/* ---- tema */
var root=document.documentElement, saved=ls('g','ed-theme');
if(saved) root.setAttribute('data-theme',saved);
var tb=$('#theme'); if(tb) tb.addEventListener('click',function(){
  var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  var nx=cur==='dark'?'light':'dark'; root.setAttribute('data-theme',nx); ls('s','ed-theme',nx);});
/* ---- navegación móvil */
var hb=$('#hamb'); if(hb) hb.addEventListener('click',function(){document.body.classList.toggle('nav')});
$$('.side a').forEach(function(a){a.addEventListener('click',function(){document.body.classList.remove('nav')})});
/* ---- scroll-spy (documento maestro) */
var secs=$$('section.blk'), links={};
$$('.side a[data-blk]').forEach(function(a){links[a.getAttribute('data-blk')]=a});
if(secs.length>1&&'IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){$$('.side a.on').forEach(function(x){x.classList.remove('on')});var a=links[e.target.id]; if(a)a.classList.add('on');}
  })},{rootMargin:'-20% 0px -70% 0px'});
  secs.forEach(function(s){io.observe(s)});
}
/* ---- quiz */
$$('.quiz').forEach(function(q){
  $$('.opt',q).forEach(function(b){b.addEventListener('click',function(){
    if(q.getAttribute('data-done'))return; q.setAttribute('data-done','1');
    $$('.opt',q).forEach(function(o){ if(o.getAttribute('data-ok')==='1') o.classList.add('good'); });
    if(b.getAttribute('data-ok')!=='1') b.classList.add('bad');
    $('.qx',q).hidden=false; updateScore();
  })});
});
function updateScore(){
  var t=$$('.quiz').length, d=$$('.quiz[data-done]').length;
  var good=$$('.quiz[data-done]').filter(function(q){return !$('.opt.bad',q)}).length;
  var s=$('#score'); if(s) s.textContent=good+' correctas de '+d+' respondidas (de '+t+')';
}
var rs=$('#resetq'); if(rs) rs.addEventListener('click',function(){
  $$('.quiz').forEach(function(q){q.removeAttribute('data-done');$$('.opt',q).forEach(function(o){o.classList.remove('good','bad')});$('.qx',q).hidden=true});updateScore();});
/* ---- tarjetas */
$$('.card').forEach(function(c){c.addEventListener('click',function(){c.classList.toggle('flip')});
  c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();c.classList.toggle('flip')}})});
/* ---- progreso */
var KEY='ed-progress', prog={}; try{prog=JSON.parse(ls('g',KEY)||'{}')}catch(e){}
function saveProg(){ls('s',KEY,JSON.stringify(prog)); refreshProg();}
$$('input[data-chk]').forEach(function(i){
  i.checked=!!prog[i.getAttribute('data-chk')];
  i.addEventListener('change',function(){prog[i.getAttribute('data-chk')]=i.checked;saveProg()});
});
function refreshProg(){
  var all=$$('input[data-chk]'), tot=all.length||1, done=all.filter(function(i){return i.checked}).length;
  var g=$('#gprog'); if(g){g.style.width=(100*done/tot)+'%'; var gt=$('#gprogt'); if(gt) gt.textContent=done+' de '+tot+' tareas ('+Math.round(100*done/tot)+' %)';}
  var by={}; all.forEach(function(i){var k=i.getAttribute('data-grp'); (by[k]=by[k]||[0,0])[1]++; if(i.checked)by[k][0]++;});
  $$('.side .pct').forEach(function(p){var k=p.getAttribute('data-grp'); if(by[k]) p.textContent=Math.round(100*by[k][0]/by[k][1])+'%';});
}
/* ---- filtros de exámenes */
var fch=$$('.chip[data-f]'), fin=$('#exq'), active={};
function applyEx(){
  var q=(fin&&fin.value||'').toLowerCase().trim();
  $$('.exgroup').forEach(function(g){
    var any=false;
    $$('.ej',g).forEach(function(e){
      var tg=(e.getAttribute('data-tags')||'').split(' '), ok=true;
      Object.keys(active).forEach(function(k){ if(active[k] && tg.indexOf(k)<0 && (e.getAttribute('data-origen')||'').toLowerCase().indexOf(k)<0) ok=false; });
      if(q && e.textContent.toLowerCase().indexOf(q)<0) ok=false;
      e.style.display=ok?'':'none'; if(ok)any=true;
    });
    g.style.display=any?'':'none'; if((q||Object.keys(active).some(function(k){return active[k]}))&&any) g.open=true;
  });
}
fch.forEach(function(c){c.addEventListener('click',function(){var k=c.getAttribute('data-f'); active[k]=!active[k]; c.classList.toggle('on',active[k]); applyEx();})});
if(fin) fin.addEventListener('input',applyEx);
/* ---- buscador global */
var si=$('#q'), hits=$('#hits'), idx=null;
function buildIdx(){
  if(idx) return Promise.resolve(idx);
  if(window.SEARCH_URL){return fetch(window.SEARCH_URL).then(function(r){return r.json()}).then(function(j){idx=j;return idx})}
  idx=[]; $$('section.blk').forEach(function(s){
    var bt=($('.bhead h1',s)||{}).textContent||s.id;
    idx.push({p:'',id:s.id,t:bt,x:s.textContent.replace(/\s+/g,' ')});
    $$('.ej',s).forEach(function(e){idx.push({p:'',id:e.id,t:(e.querySelector('h4')||e).textContent.slice(0,90),b:bt,x:e.textContent.replace(/\s+/g,' ')})});
  }); return Promise.resolve(idx);
}
function doSearch(){
  var q=si.value.toLowerCase().trim(); hits.innerHTML=''; if(q.length<2)return;
  buildIdx().then(function(ix){
    var res=[]; for(var i=0;i<ix.length&&res.length<18;i++){var e=ix[i],xx=(e.x||'').toLowerCase(),p=xx.indexOf(q); if(p>=0&&e.id){res.push([e,p])}}
    if(!res.length){hits.innerHTML='<small>Sin resultados</small>';return}
    res.forEach(function(r){var e=r[0],a=document.createElement('a');a.href=(e.p||'')+'#'+e.id;
      var s=Math.max(0,r[1]-30), sn=(e.x||'').slice(s,s+90).replace(/</g,'&lt;');
      a.innerHTML='<b>'+(e.t||e.id).replace(/</g,'&lt;')+'</b><small>'+(e.b?e.b+' · ':'')+'…'+sn+'…</small>'; hits.appendChild(a)});
  });
}
if(si){si.addEventListener('input',doSearch);}
/* ---- expandir / colapsar todo */
var ex=$('#expand'); if(ex) ex.addEventListener('click',function(){var any=$$('details:not([open])').length>0; $$('details').forEach(function(d){d.open=any}); ex.textContent=any?'Plegar todo':'Desplegar todo';});
/* ---- abrir el grupo del ejercicio enlazado */
function openHash(){var h=location.hash.slice(1); if(!h)return; var e=document.getElementById(h); if(!e)return; var p=e.closest('details'); while(p){p.open=true;p=p.parentElement&&p.parentElement.closest('details')} setTimeout(function(){e.scrollIntoView()},30);}
window.addEventListener('hashchange',openHash); openHash(); refreshProg();
/* ---- simuladores */
window.__sims=window.__sims||{};
$$('.sim').forEach(function(el){var n=el.getAttribute('data-sim'); if(window.__sims[n]){try{window.__sims[n](el)}catch(e){console.error('sim '+n,e);el.insertAdjacentHTML('beforeend','<p class="small">Error en el simulador.</p>')}} else {el.insertAdjacentHTML('beforeend','<p class="small">Simulador no disponible.</p>')}});
/* ---- botón «Abrir en el simulador» */
(function(){var sp=$('.sim[data-sim="prac"]'); if(sp&&!sp.id) sp.id='sim-prac';
$$('.simgo').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();var s=$('#sim-prac'); if(!s) return; var sel=s.querySelector('select'); if(sel){sel.value=b.getAttribute('data-simsel'); sel.dispatchEvent(new Event('change'));} var d=s.closest('details'); while(d){d.open=true; d=d.parentElement&&d.parentElement.closest('details')} s.scrollIntoView({behavior:'smooth',block:'start'});})});})();
/* ---- PWA */
if('serviceWorker' in navigator && location.protocol.indexOf('http')===0 && window.SW_URL){navigator.serviceWorker.register(window.SW_URL).catch(function(){});}
})();
