(function(){
'use strict';
var S=window.__sims=window.__sims||{};
function h(t,a,c){var e=document.createElement(t);if(a)for(var k in a){if(k==='html')e.innerHTML=a[k];else if(k==='text')e.textContent=a[k];else e.setAttribute(k,a[k])}if(c)c.forEach(function(x){e.appendChild(x)});return e}
function head(el,t){el.appendChild(h('h5',{text:t}))}
function pad(s,n){s=String(s);while(s.length<n)s='0'+s;return s}
/* ---------- Quine-McCluskey (mismo método que el verificador en Python) ---------- */
function qm(n,on,dc){
  dc=dc||[]; if(!on.length)return [];
  var terms={}, all=on.concat(dc); all.forEach(function(m){terms[m+':0']=[m,0]});
  var primes={};
  while(Object.keys(terms).length){
    var next={},used={},tl=Object.keys(terms).map(function(k){return terms[k]});
    for(var i=0;i<tl.length;i++)for(var j=i+1;j<tl.length;j++){
      var a=tl[i],b=tl[j]; if(a[1]!==b[1])continue; var d=a[0]^b[0];
      if(d&&(d&(d-1))===0){var v=a[0]&~d,m=a[1]|d; next[v+':'+m]=[v,m]; used[a[0]+':'+a[1]]=1; used[b[0]+':'+b[1]]=1}
    }
    tl.forEach(function(t){if(!used[t[0]+':'+t[1]])primes[t[0]+':'+t[1]]=t});
    terms=next;
  }
  var P=Object.keys(primes).map(function(k){return primes[k]});
  function cov(p,m){return (m&~p[1])===(p[0]&~p[1])}
  var chosen=[],left=on.slice();
  on.forEach(function(m){var c=P.filter(function(p){return cov(p,m)}); if(c.length===1&&chosen.indexOf(c[0])<0)chosen.push(c[0])});
  chosen.forEach(function(p){left=left.filter(function(m){return !cov(p,m)})});
  var rest=P.filter(function(p){return chosen.indexOf(p)<0});
  if(left.length){
    var best=null;
    for(var k=1;k<=rest.length&&!best;k++){
      var sols=[];(function rec(st,cur){ if(cur.length===k){ if(left.every(function(m){return cur.some(function(p){return cov(p,m)})}))sols.push(cur.slice()); return }
        for(var i=st;i<rest.length;i++){cur.push(rest[i]);rec(i+1,cur);cur.pop()}})(0,[]);
      if(sols.length){function lits(s){return s.reduce(function(a,p){return a+n-bitc(p[1])},0)}
        best=sols.sort(function(a,b){return lits(a)-lits(b)})[0]}
    }
    chosen=chosen.concat(best||[]);
  }
  return chosen;
}
function bitc(x){var c=0;while(x){c+=x&1;x>>=1}return c}
function sopStr(n,imps,names){
  if(!imps.length)return '0';
  return imps.map(function(p){var s='';for(var i=0;i<n;i++){var b=n-1-i; if((p[1]>>b)&1)continue; s+=names[i]+(((p[0]>>b)&1)?'':"'")} return s||'1'}).join(' + ');
}
function evalImps(imps,m){return imps.some(function(p){return (m&~p[1])===(p[0]&~p[1])})?1:0}
function svgWave(sigs,n,w){
  w=w||34;var ox=64,rh=34,H=sigs.length*rh+14,W=ox+n*w+8,s='<svg viewBox="0 0 '+W+' '+H+'" width="'+W+'" style="max-width:100%;height:auto" class="fig timing">';
  for(var i=0;i<=n;i++)s+='<line x1="'+(ox+i*w)+'" y1="4" x2="'+(ox+i*w)+'" y2="'+(H-6)+'" class="grid"/>';
  sigs.forEach(function(sg,k){var y0=k*rh+rh-6,y1=k*rh+8; s+='<text x="'+(ox-6)+'" y="'+((y0+y1)/2+4)+'" class="t m" text-anchor="end">'+sg[0]+'</text>';
    var d='',prev=null; sg[1].forEach(function(v,i){var x=ox+i*w,y=v?y1:y0; if(prev===null)d+='M'+x+' '+y; else if(prev!==v)d+='V'+y; d+='H'+(x+w); prev=v});
    s+='<path d="'+d+'" class="wave'+(sg[2]?' a':'')+'"/>';
    if(sg[3]){sg[3].forEach(function(lb,i){s+='<text x="'+(ox+i*w+w/2)+'" y="'+(y1+(y0-y1)/2+4)+'" class="t tiny" text-anchor="middle">'+lb+'</text>'})}});
  return s+'</svg>';
}
/* ================= 1. Conversor numérico ================= */
S.conv=function(el){
  head(el,'Simulador · conversor de sistemas de numeración');
  var inp=h('input',{type:'text',value:'-37',inputmode:'text'}), sel=h('select',{html:'<option value="10">decimal</option><option value="2">binario</option><option value="8">octal</option><option value="16">hexadecimal</option>'});
  var nb=h('select',{html:'<option>4</option><option selected>8</option><option>12</option><option>16</option>'});
  var out=h('div',{class:'out'});
  el.appendChild(h('label',{text:'Número (con signo si es decimal) y base de entrada'}));
  el.appendChild(h('div',{class:'row'},[inp,sel]));
  el.appendChild(h('label',{text:'Nº de bits para complemento a 2'})); el.appendChild(nb); el.appendChild(out);
  function run(){
    var base=+sel.value,txt=inp.value.trim(),v=parseInt(txt,base);
    if(isNaN(v)){out.textContent='Introduce un número válido en la base elegida.';return}
    var n=+nb.value,min=-Math.pow(2,n-1),max=Math.pow(2,n-1)-1,L=[];
    L.push('Valor decimal : '+v);
    L.push('Binario puro  : '+(v<0?'-':'')+Math.abs(v).toString(2));
    L.push('Octal / Hex   : '+(v<0?'-':'')+Math.abs(v).toString(8)+' / '+(v<0?'-':'')+Math.abs(v).toString(16).toUpperCase());
    if(v>=min&&v<=max){var u=(v<0)?(Math.pow(2,n)+v):v; L.push('C2 ('+n+' bits)   : '+pad(u.toString(2),n)+'  [rango '+min+' a '+max+']')}
    else L.push('C2 ('+n+' bits)   : fuera de rango ['+min+', '+max+'] → desbordamiento');
    if(v>=0){L.push('BCD natural   : '+String(v).split('').map(function(d){return pad((+d).toString(2),4)}).join(' '));
             L.push('BCD exceso 3  : '+String(v).split('').map(function(d){return pad((+d+3).toString(2),4)}).join(' '));}
    out.textContent=L.join('\n');
  }
  [inp,sel,nb].forEach(function(x){x.addEventListener('input',run)}); run();
};
/* ================= 2. Tabla de verdad + Karnaugh -> SOP/POS/NAND ================= */
S.kmap=function(el){
  head(el,'Simulador · minimizador de funciones (2-4 variables)');
  var nsel=h('select',{html:'<option>2</option><option>3</option><option selected>4</option>'});
  var names=['A','B','C','D'], state=[], out=h('div',{class:'out'}), box=h('div',{class:'tt'});
  el.appendChild(h('label',{text:'Nº de variables · clic en una salida: 0 → 1 → × (indiferente)'})); el.appendChild(nsel);
  var preset=h('select',{html:'<option value="">— ejemplos —</option><option value="maj">Mayoría de 3</option><option value="bcd">BCD ≥ 5 (4 vars, ×10-15)</option><option value="par">Paridad de 4 bits</option><option value="inv">Invernadero T+V+H</option>'});
  el.appendChild(preset); el.appendChild(box); el.appendChild(out);
  function build(){
    var n=+nsel.value; state=[]; for(var i=0;i<Math.pow(2,n);i++)state.push(0); draw();
  }
  function draw(){
    var n=+nsel.value,t='<table class="k"><thead><tr>'+names.slice(0,n).map(function(x){return '<th>'+x+'</th>'}).join('')+'<th>F</th></tr></thead><tbody>';
    for(var i=0;i<state.length;i++){var b=pad(i.toString(2),n).split('');t+='<tr>'+b.map(function(x){return '<td>'+x+'</td>'}).join('')+'<td data-i="'+i+'" class="'+(state[i]===1?'t1':state[i]===2?'tx':'t0')+'">'+(state[i]===1?'1':state[i]===2?'×':'0')+'</td></tr>'}
    box.innerHTML=t+'</tbody></table>';
    Array.prototype.forEach.call(box.querySelectorAll('td[data-i]'),function(td){td.addEventListener('click',function(){var i=+td.getAttribute('data-i');state[i]=(state[i]+1)%3;draw()})});
    solve();
  }
  function solve(){
    var n=+nsel.value,on=[],dc=[],off=[];state.forEach(function(v,i){if(v===1)on.push(i);else if(v===2)dc.push(i);else off.push(i)});
    var s=qm(n,on,dc), p=qm(n,off,dc);
    var sop=sopStr(n,s,names), pos=p.length?p.map(function(q){var t=[];for(var i=0;i<n;i++){var b=n-1-i;if((q[1]>>b)&1)continue;t.push(names[i]+(((q[0]>>b)&1)?"'":''))}return '('+t.join(' + ')+')'}).join(''):'1';
    var lit=function(x){return x.length};
    out.textContent='Minterms (1): '+(on.join(', ')||'—')+'\nIndiferentes: '+(dc.join(', ')||'—')+'\n\nSuma de productos : F = '+sop+'\nProducto de sumas : F = '+pos+'\n\nPuertas: '+s.length+' producto(s) + 1 OR  ·  '+s.reduce(function(a,q){return a+n-bitc(q[1])},0)+' literales\nNAND-NAND: se obtiene negando dos veces la SOP (De Morgan); inversores solo para las variables que aparezcan negadas.';
  }
  preset.addEventListener('change',function(){
    var v=preset.value; if(!v)return;
    if(v==='maj'){nsel.value='3';build();[3,5,6,7].forEach(function(i){state[i]=1})}
    if(v==='bcd'){nsel.value='4';build();for(var i=5;i<10;i++)state[i]=1;for(i=10;i<16;i++)state[i]=2}
    if(v==='par'){nsel.value='4';build();for(var i=0;i<16;i++)state[i]=bitc(i)%2?1:0}
    if(v==='inv'){nsel.value='3';build();for(var i=1;i<8;i++)state[i]=1}
    draw();
  });
  nsel.addEventListener('change',build); build();
};
/* ================= 3. Contador síncrono: secuencia -> ecuaciones JK + cronograma ================= */
S.counter=function(el){
  head(el,'Simulador · diseño de contadores síncronos con biestables JK');
  var up=h('input',{type:'text',value:'0,2,4,6,1,3,5,7'}), down=h('input',{type:'text',placeholder:'(opcional) secuencia con X=1; vacío = misma secuencia en sentido inverso'});
  var useX=h('input',{type:'checkbox'}); var ncyc=h('input',{type:'number',value:'12',min:'4',max:'30'}), out=h('div',{class:'out'}), wave=h('div',{class:'tt'});
  el.appendChild(h('label',{text:'Secuencia de cuenta (estados en decimal, separados por comas)'})); el.appendChild(up);
  el.appendChild(h('label',{},[useX,document.createTextNode(' Añadir entrada X (X=0 sube, X=1 baja por la secuencia inversa)')]));
  el.appendChild(h('label',{text:'Ciclos de reloj a dibujar'})); el.appendChild(ncyc); el.appendChild(out); el.appendChild(wave);
  function run(){
    var seq=up.value.split(',').map(function(x){return parseInt(x.trim(),10)}).filter(function(x){return !isNaN(x)});
    if(seq.length<2){out.textContent='Escribe al menos 2 estados.';return}
    var uniq=seq.filter(function(v,i){return seq.indexOf(v)===i}); if(uniq.length!==seq.length){out.textContent='Hay estados repetidos: este simulador solo admite secuencias con estados distintos.';return}
    var mx=Math.max.apply(null,seq),nq=Math.max(1,Math.ceil(Math.log(mx+1)/Math.LN2)), X=useX.checked, nv=nq+(X?1:0), N=seq.length;
    var qn=[];for(var i=nq-1;i>=0;i--)qn.push('Q'+i); var names=qn.concat(X?['X']:[]);
    var fn={};for(i=nq-1;i>=0;i--){fn['J'+i]={on:[],dc:[]};fn['K'+i]={on:[],dc:[]}}
    var used={};seq.forEach(function(s){used[s]=1});
    for(var s=0;s<Math.pow(2,nq);s++)for(var x=0;x<(X?2:1);x++){
      var idx=(s<<(X?1:0))|x, pos=seq.indexOf(s);
      if(pos<0){for(var k in fn)fn[k].dc.push(idx);continue}
      var ns=x? seq[(pos-1+N)%N] : seq[(pos+1)%N];
      for(var b=0;b<nq;b++){var q=(s>>b)&1,qq=(ns>>b)&1,J,K;
        if(q===0&&qq===0){J=0;K=-1}else if(q===0&&qq===1){J=1;K=-1}else if(q===1&&qq===0){J=-1;K=1}else{J=-1;K=0}
        if(J===1)fn['J'+b].on.push(idx);else if(J===-1)fn['J'+b].dc.push(idx);
        if(K===1)fn['K'+b].on.push(idx);else if(K===-1)fn['K'+b].dc.push(idx);}
    }
    var L=['Estados: '+N+' → '+nq+' biestables JK (2^'+nq+' = '+Math.pow(2,nq)+' ≥ '+N+')','Estados no usados: '+(Math.pow(2,nq)-N)+' (indiferentes en los mapas)',''];
    for(i=nq-1;i>=0;i--){['J','K'].forEach(function(t){var f=fn[t+i];L.push(t+i+' = '+sopStr(nv,qm(nv,f.on,f.dc),names))})}
    out.textContent=L.join('\n');
    var cyc=+ncyc.value||12,st=[],cur=seq[0],sx=0;for(i=0;i<cyc;i++){st.push(cur);cur=seq[(seq.indexOf(cur)+1)%N]}
    var sigs=[['CLK',[]]];for(i=0;i<cyc;i++){sigs[0][1].push(1,0)}
    var sg=[];for(i=nq-1;i>=0;i--)(function(i){sg.push(['Q'+i,st.map(function(v){return (v>>i)&1}),true])})(i);
    var lbl=st.map(String);
    var clkSig=['CLK',st.map(function(){return 1}),false]; // reloj dibujado como pulso por ciclo
    wave.innerHTML=svgWave(sg.concat([['estado',st.map(function(){return 0}),false,lbl]]),cyc,36);
  }
  [up,useX,ncyc].forEach(function(x){x.addEventListener('input',run)}); run();
};
/* ================= 4. Caja fuerte (Mealy, 8 estados) ================= */
S.caja=function(el){
  head(el,'Simulador · caja fuerte A, A, B, A (autómata de Mealy)');
  var names=['S0 reposo','S1 A1 pulsada','S2 A1 soltada','S3 A2 pulsada','S4 A2 soltada','S5 B pulsada','S6 B soltada','S7 A3 pulsada (abierta)'];
  var s=0,hist=[],stEl=h('div',{class:'out'}),row=h('div',{class:'row'}),log=h('div',{class:'out'});
  function nxt(s,a,b){var A=a&&!b,B=b&&!a,N=!a&&!b;
    switch(s){case 0:return A?[1,0]:[0,0];case 1:return A?[1,0]:N?[2,0]:[0,0];case 2:return N?[2,0]:A?[3,0]:[0,0];case 3:return A?[3,0]:N?[4,0]:[0,0];
      case 4:return N?[4,0]:B?[5,0]:[0,0];case 5:return B?[5,0]:N?[6,0]:[0,0];case 6:return N?[6,0]:A?[7,1]:[0,0];default:return A?[7,0]:[0,0]}}
  function press(a,b,lab){var r=nxt(s,a,b);hist.push(lab+'  →  '+names[r[0]]+'   Z='+r[1]+(r[1]?'   ✔ ¡ABRE!':''));s=r[0];if(hist.length>14)hist.shift();show()}
  function show(){stEl.textContent='Estado actual: '+names[s]+'\nCódigo Q2Q1Q0 = '+pad(s.toString(2),3);log.textContent=hist.join('\n')||'(pulsa las teclas; cada pulsación es un ciclo de reloj)'}
  [['Tecla A',1,0],['Tecla B',0,1],['Soltar (ninguna)',0,0],['Error: A y B',1,1]].forEach(function(b){var bt=h('button',{class:'btn',type:'button',text:b[0]});bt.addEventListener('click',function(){if(b[1]&&b[2]){s=0;hist.push('A+B a la vez → reinicio (S0)');show();return}press(b[1],b[2],b[0])});row.appendChild(bt)});
  var rs=h('button',{class:'btn',type:'button',text:'Reiniciar'});rs.addEventListener('click',function(){s=0;hist=[];show()});row.appendChild(rs);
  el.appendChild(h('p',{class:'small',text:'Para repetir una tecla hay que soltarla antes (un ciclo en reposo). La secuencia correcta es: A, soltar, A, soltar, B, soltar, A.'}));
  el.appendChild(row);el.appendChild(stEl);el.appendChild(log);show();
};
/* ================= 5. Familias lógicas: márgenes de ruido ================= */
S.familias=function(el){
  head(el,'Simulador · niveles lógicos y márgenes de ruido');
  var fam={TTL:[2.4,2.0,0.8,0.4,5],'CMOS 5 V (HC)':[4.4,3.5,1.5,0.33,5],'CMOS 3,3 V (LV)':[3.0,2.0,0.8,0.36,3.3]};
  var sel=h('select',{html:Object.keys(fam).map(function(k){return '<option>'+k+'</option>'}).join('')+'<option>personalizada</option>'});
  var f=['VOH min','VIH min','VIL max','VOL max'],inp=f.map(function(n){return h('input',{type:'number',step:'0.01'})}),out=h('div',{class:'out'});
  el.appendChild(h('label',{text:'Familia (driver → carga)'}));el.appendChild(sel);
  var sel2=h('select',{html:Object.keys(fam).map(function(k){return '<option>'+k+'</option>'}).join('')});sel2.selectedIndex=1;el.appendChild(h('label',{text:'Carga conectada a la salida'}));el.appendChild(sel2);
  var g=h('div',{class:'row'});f.forEach(function(n,i){var w=h('div',{style:'flex:1;min-width:110px'});w.appendChild(h('label',{text:n+' (V)'}));w.appendChild(inp[i]);g.appendChild(w)});el.appendChild(g);el.appendChild(out);
  function load(){var k=sel.value;if(fam[k]){inp.forEach(function(x,i){x.value=fam[k][i]})}run()}
  function run(){
    var d=inp.map(function(x){return +x.value}),L=fam[sel2.value],nmh=d[0]-L[1],nml=L[2]-d[3];
    var ok=nmh>0&&nml>0, vcc=fam[sel.value]?fam[sel.value][4]:5, vcc2=L[4];
    out.textContent='Carga: '+sel2.value+'  (VIH min = '+L[1]+' V, VIL max = '+L[2]+' V)\n\nNMH = VOH(driver) − VIH(carga) = '+d[0]+' − '+L[1]+' = '+nmh.toFixed(2)+' V\nNML = VIL(carga) − VOL(driver) = '+L[2]+' − '+d[3]+' = '+nml.toFixed(2)+' V\n\n'+(ok?'✔ Se pueden conectar directamente (ambos márgenes positivos).':'✘ NO se pueden conectar directamente: algún margen es negativo.')+(vcc!==vcc2?'\n⚠ Alimentaciones distintas ('+vcc+' V y '+vcc2+' V): hace falta adaptador de niveles.':'');
  }
  sel.addEventListener('change',load);sel2.addEventListener('change',run);inp.forEach(function(x){x.addEventListener('input',run)});load();
};
/* ================= 6. Biestables: D, T, JK ================= */
S.ff=function(el){
  head(el,'Simulador · biestable activo por flanco de subida');
  var kind=h('select',{html:'<option>JK</option><option>T</option><option>D</option>'}),cyc=8,in1=[],in2=[],r1=h('div',{class:'row'}),r2=h('div',{class:'row'}),out=h('div',{class:'tt'});
  var rnd=h('button',{class:'btn',type:'button',text:'Entradas aleatorias'});
  el.appendChild(h('label',{text:'Tipo de biestable'}));el.appendChild(kind);
  for(var i=0;i<cyc;i++){in1.push(h('input',{type:'checkbox'}));in2.push(h('input',{type:'checkbox'}))}
  function lab(txt,arr,row){row.appendChild(h('span',{class:'small',text:txt,style:'min-width:26px'}));arr.forEach(function(c){row.appendChild(c)})}
  var l1=h('span');el.appendChild(h('label',{text:'Valor de la entrada J (o T / D) antes de cada flanco'}));lab('J/T/D',in1,r1);el.appendChild(r1);
  var kl=h('label',{text:'Valor de la entrada K (solo JK)'});el.appendChild(kl);lab('K',in2,r2);el.appendChild(r2);el.appendChild(rnd);el.appendChild(out);
  function run(){
    var k=kind.value,q=0,Q=[],A=[],B=[];kl.style.display=r2.style.display=k==='JK'?'':'none';
    for(var i=0;i<cyc;i++){var a=in1[i].checked?1:0,b=in2[i].checked?1:0;A.push(a);B.push(b);
      if(k==='D')q=a;else if(k==='T')q=q^a;else q=(a&(1-q))|((1-b)&q);Q.push(q)}
    var sg=[['CLK',A.map(function(){return 1})]];
    out.innerHTML=svgWave([[k==='D'?'D':k==='T'?'T':'J',A],].concat(k==='JK'?[['K',B]]:[]).concat([['Q',Q,true]]),cyc,40);
  }
  kind.addEventListener('change',run);in1.concat(in2).forEach(function(c){c.addEventListener('change',run)});
  rnd.addEventListener('click',function(){in1.concat(in2).forEach(function(c){c.checked=Math.random()<.5});run()});run();
};
/* ================= 7. Sumador BCD con corrección +6 ================= */
S.bcdadd=function(el){
  head(el,'Simulador · suma BCD paso a paso');
  var a=h('input',{type:'number',min:'0',max:'99',value:'47'}),b=h('input',{type:'number',min:'0',max:'99',value:'38'}),out=h('div',{class:'out'});
  el.appendChild(h('label',{text:'Sumando A (0-99)'}));el.appendChild(a);el.appendChild(h('label',{text:'Sumando B (0-99)'}));el.appendChild(b);el.appendChild(out);
  function nib(x){return pad(x.toString(2),4)}
  function run(){
    var A=Math.min(99,Math.max(0,+a.value|0)),B=Math.min(99,Math.max(0,+b.value|0)),da=[Math.floor(A/10),A%10],db=[Math.floor(B/10),B%10],L=[];
    L.push('A = '+da.map(nib).join(' ')+'   ('+A+')');L.push('B = '+db.map(nib).join(' ')+'   ('+B+')');L.push('');
    var c=0,res=[];
    for(var i=1;i>=0;i--){var s=da[i]+db[i]+c,raw=s;L.push('Dígito '+(i?'unidades':'decenas')+': '+nib(da[i])+' + '+nib(db[i])+' + '+c+' (acarreo) = '+pad(raw.toString(2),5)+' ('+raw+')');
      if(s>9){s+=6;L.push('   > 9 → sumar 0110: '+pad(s.toString(2),5)+'  → dígito '+nib(s&15)+', acarreo 1');c=1;res.unshift(s&15)}else{c=0;res.unshift(s);L.push('   ≤ 9 → sin corrección')}}
    if(c)res.unshift(1);L.push('');L.push('Resultado BCD = '+res.map(nib).join(' ')+'   ('+res.join('')+')  '+(+res.join('')===A+B?'✔':'✘'));out.textContent=L.join('\n');
  }
  a.addEventListener('input',run);b.addEventListener('input',run);run();
};
/* ================= 8. Simulador de prácticas (lógica de las funciones clave) ================= */
S.prac=function(el){
  head(el,'Simulador de prácticas · código equivalente, salida de consola y cronograma');
  var P={
   sum4:{t:'Sumador de 4 bits (Práctica 2)',vhdl:"entity sum4 is\n  port(a,b: in std_logic_vector(3 downto 0); cin: in std_logic;\n       s: out std_logic_vector(3 downto 0); cout: out std_logic);\nend sum4;\narchitecture rtl of sum4 is\n  signal t: unsigned(4 downto 0);\nbegin\n  t    <= ('0'&unsigned(a)) + unsigned(b) + (\"0000\"&cin);\n  s    <= std_logic_vector(t(3 downto 0));\n  cout <= t(4);\nend rtl;",
     inputs:[['a',0,15,9],['b',0,15,8],['cin',0,1,0]],
     run:function(v){var t=v.a+v.b+v.cin;return {c:['a='+pad(v.a.toString(2),4)+'  b='+pad(v.b.toString(2),4)+'  cin='+v.cin,'s='+pad((t&15).toString(2),4)+'  cout='+(t>>4)+'   ('+v.a+' + '+v.b+' + '+v.cin+' = '+t+')'],w:null}}},
   cmp4:{t:'Comparador de 4 bits (Práctica 2)',vhdl:"gt <= '1' when unsigned(a) > unsigned(b) else '0';\neq <= '1' when a = b else '0';\nlt <= '1' when unsigned(a) < unsigned(b) else '0';",
     inputs:[['a',0,15,5],['b',0,15,9]],run:function(v){return {c:['A='+v.a+'  B='+v.b,'A>B='+(v.a>v.b?1:0)+'  A=B='+(v.a===v.b?1:0)+'  A<B='+(v.a<v.b?1:0)],w:null}}},
   mux4:{t:'Multiplexor 4:1 (Práctica 2)',vhdl:"with sel select\n  y <= d0 when \"00\",\n       d1 when \"01\",\n       d2 when \"10\",\n       d3 when others;",
     inputs:[['d',0,15,6],['sel',0,3,2]],run:function(v){var bit=(v.d>>v.sel)&1;return {c:['d3d2d1d0='+pad(v.d.toString(2),4)+'  sel='+pad(v.sel.toString(2),2),'y = d'+v.sel+' = '+bit],w:null}}},
   seg7:{t:'Decodificador BCD a 7 segmentos (Práctica 2)',vhdl:"with d select\n  seg <= \"0000001\" when x\"0\",   -- abcdefg, activo a 0 en Basys\n         \"1001111\" when x\"1\",\n         \"0010010\" when x\"2\",\n         ... \n         \"1111111\" when others;",
     inputs:[['d',0,15,7]],run:function(v){var T=['1111110','0110000','1101101','1111001','0110011','1011011','1011111','1110000','1111111','1111011'],s=T[v.d]||'0000000';var a='abcdefg'.split('').filter(function(c,i){return s[i]==='1'}).join('');return {c:['d='+v.d,'segmentos activos (a..g): '+s+'  → '+(a||'ninguno'),'Basys (activo a 0): '+s.split('').map(function(x){return x==='1'?'0':'1'}).join('')],w:null}}},
   cnt:{t:'Contador módulo N con reloj (Práctica 3)',vhdl:"process(clk, rst)\nbegin\n  if rst = '1' then q <= (others => '0');\n  elsif rising_edge(clk) then\n    if q = N-1 then q <= (others => '0');\n    else q <= q + 1; end if;\n  end if;\nend process;",
     inputs:[['N',2,16,10],['ciclos',4,30,16]],run:function(v){var q=0,Q=[];for(var i=0;i<v.ciclos;i++){Q.push(q);q=(q+1)%v.N}return {c:['módulo '+v.N+' → '+Math.ceil(Math.log(v.N)/Math.LN2)+' bits','q = '+Q.join(', ')],w:[['q0',Q.map(function(x){return x&1}),true],['q1',Q.map(function(x){return (x>>1)&1}),true],['q2',Q.map(function(x){return (x>>2)&1}),true],['q3',Q.map(function(x){return (x>>3)&1}),true]],n:v.ciclos}}},
   div:{t:'Divisor de frecuencia (Práctica 3)',vhdl:"process(clk)\nbegin\n  if rising_edge(clk) then\n    if cnt = DIV/2 - 1 then cnt <= 0; clk_out <= not clk_out;\n    else cnt <= cnt + 1; end if;\n  end if;\nend process;",
     inputs:[['f_in (MHz)',1,100,50],['f_out (Hz)',1,1000,1]],run:function(v){var d=Math.round(v['f_in (MHz)']*1e6/v['f_out (Hz)']),half=Math.floor(d/2),bits=Math.ceil(Math.log(half)/Math.LN2);return {c:['DIV = f_in / f_out = '+d,'se cuenta hasta DIV/2 − 1 = '+(half-1),'contador de '+bits+' bits','Basys: reloj de 50 MHz → 1 Hz necesita contar hasta 24 999 999'],w:null}}},
   deb:{t:'Antirrebote de pulsador (Práctica 3)',vhdl:"-- se acepta el nuevo valor si la entrada se mantiene estable T ms\nprocess(clk)\nbegin\n  if rising_edge(clk) then\n    if btn /= prev then cnt <= 0; prev <= btn;\n    elsif cnt = LIM then clean <= prev;\n    else cnt <= cnt + 1; end if;\n  end if;\nend process;",
     inputs:[['rebotes',1,6,3],['LIM (ciclos)',2,6,4]],run:function(v){var n=v.rebotes,lim=v['LIM (ciclos)'],raw=[0,0],k;for(k=0;k<n;k++){raw.push(1,0)}raw.push(1,1,1,1,1,1,1,1,1,1);var clean=[],cnt=0,prev=0,cl=0;raw.forEach(function(x){if(x!==prev){cnt=0;prev=x}else if(cnt===lim){cl=prev}else cnt++;clean.push(cl)});return {c:['la señal se acepta tras '+lim+' ciclos estables','pulsos espurios en la entrada: '+n+' → pulsos en la salida: '+clean.reduce(function(a,x,i){return a+((x&&!clean[i-1])?1:0)},0)],w:[['btn',raw,false],['clean',clean,true]],n:raw.length}}}
,
   leds:{t:'Interruptores y LEDs (Práctica 1)',vhdl:"led(3 downto 0) <= sw(3 downto 0);\nled(4) <= sw(0) and sw(1);\nled(5) <= sw(0) or  sw(1);\nled(6) <= sw(0) xor sw(1);\nled(7) <= btn(0);",
     inputs:[['sw',0,255,3],['btn0',0,1,0]],run:function(v){var s0=v.sw&1,s1=(v.sw>>1)&1,l=(v.sw&15)|((s0&s1)<<4)|((s0|s1)<<5)|((s0^s1)<<6)|((v.btn0&1)<<7);return {c:['sw  = '+pad(v.sw.toString(2),8)+'   btn0 = '+v.btn0,'led = '+pad(l.toString(2),8)],w:null}}},
   det:{t:'Detector de la secuencia 101 (Práctica 3)',vhdl:"-- Mealy, 3 estados: S0, S1, S2\nwhen S2 =>\n  if x = '1' then sig <= S1; z <= '1';\n  else sig <= S0; end if;",
     inputs:[['x (8 bits como número)',0,255,173]],run:function(v){var x=[],i;for(i=7;i>=0;i--)x.push((v['x (8 bits como número)']>>i)&1);var e=0,z=[],T={'00':0,'01':1,'10':2,'11':1,'20':0,'21':1};x.forEach(function(b){z.push(e===2&&b===1?1:0);e=T[''+e+b]});return {c:['x = '+x.join(''),'z = '+z.join(''),'detecciones: '+z.reduce(function(a,b){return a+b},0)],w:[['x',x,false],['z',z,true]],n:8}}},
   alarma:{t:'Alarma con histéresis (Prácticas 5-7, ejemplo)',vhdl:"if    t >= T_ALTA        then a <= '1';\nelsif t <  T_ALTA - HIST then a <= '0';\nend if;",
     inputs:[['T_ALTA',300,450,375],['HIST',0,20,5]],run:function(v){var M=[365,370,374,375,376,373,371,369,366,362],a=0,L=[];M.forEach(function(t){if(t>=v.T_ALTA)a=1;else if(t<v.T_ALTA-v.HIST)a=0;L.push(t+' → al_alta='+a)});return {c:L,w:null}}}
  };
  var sel=h('select',{html:Object.keys(P).map(function(k){return '<option value="'+k+'">'+P[k].t+'</option>'}).join('')}),box=h('div'),vh=h('pre',{class:'code',style:'border-radius:10px;margin-top:10px'}),out=h('div',{class:'out'}),wv=h('div',{class:'tt'});
  el.appendChild(h('label',{text:'Elige la función'}));el.appendChild(sel);el.appendChild(box);el.appendChild(h('label',{text:'Código VHDL equivalente'}));el.appendChild(vh);el.appendChild(h('label',{text:'Salida de consola'}));el.appendChild(out);el.appendChild(wv);
  var ins={};
  function mk(){var p=P[sel.value];box.innerHTML='';ins={};vh.textContent=p.vhdl;
    p.inputs.forEach(function(d){var w=h('div');w.appendChild(h('label',{text:d[0]+'  ('+d[1]+' – '+d[2]+')'}));var i=h('input',{type:'number',min:d[1],max:d[2],value:d[3]});ins[d[0]]=i;i.addEventListener('input',run);w.appendChild(i);box.appendChild(w)});run()}
  function run(){var p=P[sel.value],v={};p.inputs.forEach(function(d){var x=parseInt(ins[d[0]].value,10);if(isNaN(x))x=d[3];v[d[0]]=Math.min(d[2],Math.max(d[1],x))});
    var r=p.run(v);out.textContent=r.c.join('\n');wv.innerHTML=r.w?svgWave(r.w,r.n,r.n>20?20:30):''}
  sel.addEventListener('change',mk);mk();
};
})();

(function(){
'use strict';
var S=window.__sims=window.__sims||{};
function h(t,a,c){var e=document.createElement(t);if(a)for(var k in a){if(k==='html')e.innerHTML=a[k];else if(k==='text')e.textContent=a[k];else e.setAttribute(k,a[k])}if(c)c.forEach(function(x){e.appendChild(x)});return e}
function head(el,t){el.appendChild(h('h5',{text:t}))}
function pad(s,n){s=String(s);while(s.length<n)s='0'+s;return s}
function bitc(x){var c=0;while(x){c+=x&1;x>>=1}return c}
function lamp(txt,on){return '<span class="lamp'+(on?' on':'')+'">'+txt+'</span>'}
function wave(sigs,n,w){
  w=w||30;var ox=52,rh=30,H=sigs.length*rh+12,W=ox+n*w+6,s='<svg viewBox="0 0 '+W+' '+H+'" width="'+W+'" style="max-width:100%;height:auto" class="fig timing">';
  for(var i=0;i<=n;i++)s+='<line x1="'+(ox+i*w)+'" y1="3" x2="'+(ox+i*w)+'" y2="'+(H-5)+'" class="grid"/>';
  sigs.forEach(function(sg,k){var y0=k*rh+rh-5,y1=k*rh+7;s+='<text x="'+(ox-5)+'" y="'+((y0+y1)/2+4)+'" class="t m" text-anchor="end">'+sg[0]+'</text>';
    var d='',prev=null;sg[1].forEach(function(v,i){var x=ox+i*w,y=v?y1:y0;if(prev===null)d+='M'+x+' '+y;else if(prev!==v)d+='V'+y;d+='H'+(x+w);prev=v});
    s+='<path d="'+d+'" class="wave'+(sg[2]?' a':'')+'"/>'});
  return s+'</svg>';
}
/* ---------- Quine-McCluskey (igual que en el verificador) ---------- */
function qm(n,on,dc){
  dc=dc||[];if(!on.length)return [];
  var terms={},all=on.concat(dc);all.forEach(function(m){terms[m+':0']=[m,0]});var primes={};
  while(Object.keys(terms).length){
    var next={},used={},tl=Object.keys(terms).map(function(k){return terms[k]});
    for(var i=0;i<tl.length;i++)for(var j=i+1;j<tl.length;j++){var a=tl[i],b=tl[j];if(a[1]!==b[1])continue;var d=a[0]^b[0];
      if(d&&(d&(d-1))===0){var v=a[0]&~d,m=a[1]|d;next[v+':'+m]=[v,m];used[a[0]+':'+a[1]]=1;used[b[0]+':'+b[1]]=1}}
    tl.forEach(function(t){if(!used[t[0]+':'+t[1]])primes[t[0]+':'+t[1]]=t});terms=next}
  var P=Object.keys(primes).map(function(k){return primes[k]});
  function cov(p,m){return (m&~p[1])===(p[0]&~p[1])}
  var chosen=[],left=on.slice();
  on.forEach(function(m){var c=P.filter(function(p){return cov(p,m)});if(c.length===1&&chosen.indexOf(c[0])<0)chosen.push(c[0])});
  chosen.forEach(function(p){left=left.filter(function(m){return !cov(p,m)})});
  var rest=P.filter(function(p){return chosen.indexOf(p)<0});
  if(left.length){var best=null;
    for(var k=1;k<=rest.length&&!best;k++){var sols=[];(function rec(st,cur){if(cur.length===k){if(left.every(function(m){return cur.some(function(p){return cov(p,m)})}))sols.push(cur.slice());return}
      for(var i=st;i<rest.length;i++){cur.push(rest[i]);rec(i+1,cur);cur.pop()}})(0,[]);
      if(sols.length){function lits(s){return s.reduce(function(a,p){return a+n-bitc(p[1])},0)}best=sols.sort(function(a,b){return lits(a)-lits(b)})[0]}}
    chosen=chosen.concat(best||[])}
  return chosen;
}
function sopStr(n,imps,names){if(!imps.length)return '0';
  return imps.map(function(p){var s='';for(var i=0;i<n;i++){var b=n-1-i;if((p[1]>>b)&1)continue;s+=names[i]+(((p[0]>>b)&1)?'':"'")}return s||'1'}).join(' + ')}

/* ================= Expresiones booleanas y tablas de verdad ================= */
function parseExpr(src){
  var s=src.replace(/\s+/g,'').toUpperCase(),i=0;
  function peek(){return s[i]}
  function orE(){var l=xorE();while(peek()==='+'||peek()==='|'){i++;var r=xorE();l=(function(a,b){return function(e){return a(e)|b(e)}})(l,r)}return l}
  function xorE(){var l=andE();while(peek()==='^'||peek()==='⊕'){i++;var r=andE();l=(function(a,b){return function(e){return a(e)^b(e)}})(l,r)}return l}
  function andE(){var l=notE();for(;;){var c=peek();
      if(c==='*'||c==='·'||c==='&'||c==='.'){i++}
      else if(c&&(/[A-D01(!~¬]/.test(c))){}else break;
      var r=notE();l=(function(a,b){return function(e){return a(e)&b(e)}})(l,r)}return l}
  function notE(){var c=peek();
    if(c==='!'||c==='~'||c==='¬'){i++;var f=notE();return function(e){return 1-f(e)}}
    var f=atom();while(peek()==="'"){i++;f=(function(g){return function(e){return 1-g(e)}})(f)}return f}
  function atom(){var c=peek();
    if(c==='('){i++;var f=orE();if(peek()!==')')throw new Error('Falta cerrar un paréntesis');i++;return f}
    if(c==='0'||c==='1'){i++;var v=+c;return function(){return v}}
    if(c&&/[A-D]/.test(c)){i++;return function(e){return e[c]}}
    throw new Error(c?('Símbolo no válido: «'+c+'». Usa A, B, C, D, 0, 1, +, ·, !, \', ^ y paréntesis'):'La expresión está incompleta')}
  var f=orE();if(i<s.length)throw new Error('Sobra «'+s[i]+'» en la posición '+(i+1));
  var vars=[];'ABCD'.split('').forEach(function(v){if(s.indexOf(v)>=0)vars.push(v)});
  return {f:f,vars:vars};
}
S._parse=parseExpr;
S.truth=function(el){
  head(el,'Simulador · expresiones booleanas y tablas de verdad');
  var e1=h('input',{type:'text',value:"!(A+B)",id:'tx1',autocomplete:'off',spellcheck:'false'}),e2=h('input',{type:'text',value:"!A·!B",id:'tx2',autocomplete:'off',spellcheck:'false'});
  var ex=h('select',{id:'txs',html:'<option value="0">Ejemplos…</option><option>De Morgan 1|!(A+B)|!A·!B</option><option>De Morgan 2|!(A·B)|!A+!B</option><option>Absorción|A+A·B|A</option><option>Consenso|A·B+!A·C+B·C|A·B+!A·C</option><option>XOR|A^B|A·!B+!A·B</option><option>Mayoría|A·B+A·C+B·C|(A+B)·(A+C)·(B+C)</option><option>Una expresión no equivalente|A+B·C|(A+B)·C</option>'});
  var out=h('div',{class:'out'}),tb=h('div',{class:'tt'});
  el.appendChild(h('label',{text:'Expresión 1 (A, B, C, D; + suma, · producto, ! o \' negación, ^ XOR)'}));el.appendChild(e1);
  el.appendChild(h('label',{text:'Expresión 2 (opcional, para comprobar si son equivalentes)'}));el.appendChild(e2);el.appendChild(ex);el.appendChild(tb);el.appendChild(out);
  function run(){
    var a,b=null,err='';
    try{a=parseExpr(e1.value)}catch(x){out.textContent=x.message;tb.innerHTML='';return}
    if(e2.value.trim()){try{b=parseExpr(e2.value)}catch(x){out.textContent='Expresión 2: '+x.message;tb.innerHTML='';return}}
    var vs=a.vars.slice();if(b)b.vars.forEach(function(v){if(vs.indexOf(v)<0)vs.push(v)});vs.sort();
    if(!vs.length){vs=['A']}
    var n=vs.length,rows='',on=[],eq=true,on2=[];
    for(var m=0;m<(1<<n);m++){var env={};vs.forEach(function(v,k){env[v]=(m>>(n-1-k))&1});
      var f1=a.f(env),f2=b?b.f(env):null;if(f1)on.push(m);if(f2)on2.push(m);if(b&&f1!==f2)eq=false;
      rows+='<tr'+(b&&f1!==f2?' style="background:var(--warn-soft)"':'')+'>'+vs.map(function(v){return '<td>'+env[v]+'</td>'}).join('')+'<td'+(f1?' class="t1"':'')+'>'+f1+'</td>'+(b?'<td'+(f2?' class="t1"':'')+'>'+f2+'</td>':'')+'</tr>'}
    tb.innerHTML='<table class="k"><tr>'+vs.map(function(v){return '<th>'+v+'</th>'}).join('')+'<th>F1</th>'+(b?'<th>F2</th>':'')+'</tr>'+rows+'</table>';
    var all=[];for(var m=0;m<(1<<n);m++)all.push(m);
    var off=all.filter(function(m){return on.indexOf(m)<0});
    var t='F1 = Σm('+on.join(', ')+')\nF1 = ΠM('+off.join(', ')+')\nForma mínima: F1 = '+sopStr(n,qm(n,on),vs)+'\n';
    if(b)t+='\n'+(eq?'✔ Son EQUIVALENTES: la misma tabla de verdad en las '+(1<<n)+' combinaciones.':'✘ NO son equivalentes. Se diferencian en las filas marcadas.');
    out.textContent=t;
  }
  [e1,e2].forEach(function(x){x.addEventListener('input',run)});
  ex.addEventListener('change',function(){if(ex.selectedIndex<1)return;var p=ex.value.split('|');e1.value=p[1];e2.value=p[2];run()});run();
};
/* ================= Suma en C2 con desbordamiento ================= */
S.ovf=function(el){
  head(el,'Simulador · suma en complemento a 2 y desbordamiento');
  var nb=h('select',{id:'ovn',html:'<option>4</option><option selected>8</option>'}),a=h('input',{type:'number',value:'100',id:'ova'}),b=h('input',{type:'number',value:'50',id:'ovb'}),out=h('div',{class:'out'});
  el.appendChild(h('label',{text:'Número de bits'}));el.appendChild(nb);el.appendChild(h('label',{text:'Sumando A (decimal con signo)'}));el.appendChild(a);el.appendChild(h('label',{text:'Sumando B (decimal con signo)'}));el.appendChild(b);el.appendChild(out);
  function bin(v,n){return pad(((v%(1<<n))+(1<<n))%(1<<n)).toString?pad((((v%(1<<n))+(1<<n))%(1<<n)).toString(2),n):''}
  function run(){
    var n=+nb.value,lo=-(1<<(n-1)),hi=(1<<(n-1))-1,A=Math.round(+a.value),B=Math.round(+b.value);
    if(isNaN(A)||isNaN(B)){out.textContent='Escribe dos números enteros.';return}
    if(A<lo||A>hi||B<lo||B>hi){out.textContent='Con '+n+' bits solo se representan los valores de '+lo+' a '+hi+'. Cambia A o B.';return}
    var M=1<<n,ua=(A+M)%M,ub=(B+M)%M,s=ua+ub,r=s%M,cout=s>=M?1:0,cin=((ua&(M/2-1))+(ub&(M/2-1)))>=(M/2)?1:0,V=cin^cout,rv=r>=M/2?r-M:r;
    var t='A = '+pad(ua.toString(2),n)+'  ('+A+')\nB = '+pad(ub.toString(2),n)+'  ('+B+')\n';
    t+='A+B = '+pad(r.toString(2),n)+'  → se lee '+rv+(cout?'  (se descarta el acarreo final)':'')+'\n\n';
    t+='Acarreo que entra al bit de signo: '+cin+'\nAcarreo que sale del bit de signo: '+cout+'\nDesbordamiento V = '+cin+' ⊕ '+cout+' = '+V+'\n\n';
    t+=V?'✘ DESBORDAMIENTO: la suma real es '+(A+B)+' y no cabe en '+n+' bits ('+lo+' a '+hi+').':'✔ Correcto: '+A+' + '+B+' = '+(A+B)+' cabe en '+n+' bits.';
    out.textContent=t;
  }
  [nb,a,b].forEach(function(x){x.addEventListener('input',run);x.addEventListener('change',run)});run();
};
/* ================= Bloques MSI: MUX, decodificador, comparador y sumador ================= */
S.msi=function(el){
  head(el,'Simulador · bloques combinacionales MSI');
  var sel=h('select',{id:'msis',html:'<option value="mux">Multiplexor 4:1</option><option value="dec">Decodificador 2:4 con habilitación</option><option value="cmp">Comparador de 2 bits</option><option value="add">Sumador de 4 bits (acarreo en cascada)</option>'}),box=h('div');
  el.appendChild(sel);el.appendChild(box);
  function num(id,mx,v){return h('input',{type:'number',min:'0',max:String(mx),value:String(v),id:id})}
  function chk(id,lab,on){var c=h('input',{type:'checkbox',id:id});c.checked=!!on;var l=h('label',{style:'display:inline-flex;gap:6px;align-items:center;margin-right:12px'});l.appendChild(c);l.appendChild(h('span',{text:lab}));return [c,l]}
  function build(){
    box.innerHTML='';var k=sel.value,out=h('div',{class:'out'}),vis=h('div',{style:'margin-top:8px'});
    if(k==='mux'){
      var cs=[0,1,2,3].map(function(i){return chk('mxi'+i,'I'+i,i===1||i===2)}),s=num('mxs',3,2);
      box.appendChild(h('label',{text:'Entradas de datos'}));var r=h('div',{class:'row'});cs.forEach(function(c){r.appendChild(c[1])});box.appendChild(r);
      box.appendChild(h('label',{text:'Selección S1S0 (0 a 3)'}));box.appendChild(s);box.appendChild(vis);box.appendChild(out);
      var run=function(){var v=Math.max(0,Math.min(3,+s.value|0)),d=cs.map(function(c){return c[0].checked?1:0});
        vis.innerHTML=d.map(function(x,i){return lamp('I'+i+'='+x,i===v)}).join('')+' → '+lamp('Y='+d[v],d[v]);
        out.textContent='S1S0 = '+pad(v.toString(2),2)+' elige I'+v+'.\nY = I'+v+' = '+d[v]+'\nY = S1\'S0\'·I0 + S1\'S0·I1 + S1S0\'·I2 + S1S0·I3'};
      cs.forEach(function(c){c[0].addEventListener('change',run)});s.addEventListener('input',run);run();
    }else if(k==='dec'){
      var a=num('dca',3,2),en=chk('dce','EN (habilitación)',true);
      box.appendChild(h('label',{text:'Entrada A1A0 (0 a 3)'}));box.appendChild(a);box.appendChild(en[1]);box.appendChild(vis);box.appendChild(out);
      var run2=function(){var v=Math.max(0,Math.min(3,+a.value|0)),e=en[0].checked?1:0;
        vis.innerHTML=[0,1,2,3].map(function(i){return lamp('Y'+i+'='+(e&&i===v?1:0),e&&i===v)}).join('');
        out.textContent='A1A0 = '+pad(v.toString(2),2)+', EN = '+e+'\n'+(e?'Solo se activa Y'+v+' (es el minterm m'+v+').':'Con EN = 0 todas las salidas valen 0.')+'\nYi = EN · mi'};
      a.addEventListener('input',run2);en[0].addEventListener('change',run2);run2();
    }else if(k==='cmp'){
      var A=num('cpa',3,2),B=num('cpb',3,1);
      box.appendChild(h('label',{text:'A (0 a 3)'}));box.appendChild(A);box.appendChild(h('label',{text:'B (0 a 3)'}));box.appendChild(B);box.appendChild(vis);box.appendChild(out);
      var run3=function(){var a=Math.max(0,Math.min(3,+A.value|0)),b=Math.max(0,Math.min(3,+B.value|0)),gt=a>b?1:0,eq=a===b?1:0,lt=a<b?1:0;
        vis.innerHTML=lamp('A>B',gt)+lamp('A=B',eq)+lamp('A<B',lt);
        out.textContent='A = '+pad(a.toString(2),2)+', B = '+pad(b.toString(2),2)+'\nEQ = (A1⊙B1)·(A0⊙B0) = '+eq+'\nGT = A1·B1\' + (A1⊙B1)·A0·B0\' = '+gt+'\nLT = '+lt};
      A.addEventListener('input',run3);B.addEventListener('input',run3);run3();
    }else{
      var X=num('adx',15,9),Y=num('ady',15,7),ci=chk('adc','Acarreo de entrada',false);
      box.appendChild(h('label',{text:'A (0 a 15)'}));box.appendChild(X);box.appendChild(h('label',{text:'B (0 a 15)'}));box.appendChild(Y);box.appendChild(ci[1]);box.appendChild(vis);box.appendChild(out);
      var run4=function(){var a=Math.max(0,Math.min(15,+X.value|0)),b=Math.max(0,Math.min(15,+Y.value|0)),c=ci[0].checked?1:0,t='bit  Ai Bi Ci | Si Ci+1\n',res=[];
        for(var i=0;i<4;i++){var ai=(a>>i)&1,bi=(b>>i)&1,s=ai^bi^c,co=(ai&bi)|(c&(ai^bi));t+='  '+i+'   '+ai+'  '+bi+'  '+c+' |  '+s+'    '+co+'\n';res[i]=s;c=co}
        var tot=a+b+(ci[0].checked?1:0);
        vis.innerHTML=lamp('C4='+c,c)+res.slice().reverse().map(function(x,i){return lamp('S'+(3-i)+'='+x,x)}).join('');
        out.textContent=t+'\n'+pad(a.toString(2),4)+' + '+pad(b.toString(2),4)+' + '+(ci[0].checked?1:0)+' = '+c+pad(tot.toString(2).slice(-4),4)+'  ('+tot+')\nEl acarreo "viaja" de un bit al siguiente: por eso es lento (retardo en cascada).'};
      X.addEventListener('input',run4);Y.addEventListener('input',run4);ci[0].addEventListener('change',run4);run4();
    }
  }
  sel.addEventListener('change',build);build();
};
/* ================= Registros: desplazamiento, anillo, Johnson, LFSR ================= */
S.shreg=function(el){
  head(el,'Simulador · registros de desplazamiento, anillo, Johnson y LFSR');
  var sel=h('select',{id:'srt',html:'<option value="shift">Registro de desplazamiento (entrada serie)</option><option value="anillo">Contador en anillo</option><option value="johnson">Contador Johnson</option><option value="lfsr">LFSR de 4 bits (XOR de Q3 y Q2)</option>'});
  var inb=h('input',{type:'checkbox',id:'sri'});inb.checked=true;var inl=h('label',{style:'display:inline-flex;gap:6px;align-items:center'},[inb,h('span',{text:'Entrada serie = 1'})]);
  var b1=h('button',{class:'btn',type:'button',text:'Pulso de reloj'}),b2=h('button',{class:'btn',type:'button',text:'Reiniciar'}),b3=h('button',{class:'btn',type:'button',text:'Auto'});
  var cells=h('div',{style:'margin:10px 0'}),out=h('div',{class:'out'}),wv=h('div',{class:'tt'}),row=h('div',{class:'row'},[b1,b2,b3]);
  [sel,inl,row,cells,wv,out].forEach(function(x){el.appendChild(x)});
  var q,hist,timer=null;
  function init(){var k=sel.value;q=k==='shift'?[0,0,0,0]:k==='anillo'?[1,0,0,0]:k==='johnson'?[0,0,0,0]:[0,0,0,1];hist=[q.slice()];inl.style.display=k==='shift'?'':'none'}
  function step(){var k=sel.value,fb;
    if(k==='shift')fb=inb.checked?1:0;else if(k==='anillo')fb=q[3];else if(k==='johnson')fb=1-q[3];else fb=q[3]^q[2];
    q=[fb,q[0],q[1],q[2]];hist.push(q.slice());if(hist.length>40)hist.shift()}
  function draw(){
    cells.innerHTML=[0,1,2,3].map(function(i){return lamp('Q'+i+'='+q[i],q[i])}).join('')+'<span class="small"> (entra por Q0 y sale por Q3)</span>';
    var per=0,k=sel.value;if(k!=='shift'){for(var i=1;i<hist.length;i++)if(hist[i].join('')===hist[0].join('')){per=i;break}}
    wv.innerHTML=wave([0,1,2,3].map(function(i){return ['Q'+i,hist.map(function(s){return s[i]}),i===0]}),hist.length,Math.max(10,Math.min(26,Math.floor(300/hist.length))));
    var tn={shift:'Registro de desplazamiento',anillo:'Contador en anillo: 4 estados',johnson:'Contador Johnson: 2·4 = 8 estados',lfsr:'LFSR de 4 bits: hasta 2^4 − 1 = 15 estados (nunca el 0000)'}[k];
    out.textContent=tn+'\nHistorial de estados (Q3Q2Q1Q0): '+hist.map(function(s){return s.slice().reverse().join('')}).slice(-16).join(' ')+(per?'\n✔ Periodo medido: vuelve al estado inicial tras '+per+' pulsos.':'')}
  b1.addEventListener('click',function(){step();draw()});b2.addEventListener('click',function(){init();draw()});
  b3.addEventListener('click',function(){if(timer){clearInterval(timer);timer=null;b3.textContent='Auto'}else{b3.textContent='Parar';timer=setInterval(function(){if(!document.body.contains(el)){clearInterval(timer);return}step();draw()},450)}});
  sel.addEventListener('change',function(){init();draw()});init();draw();
};
/* ================= Detector de secuencia (Mealy) ================= */
S.fsmdet=function(el){
  head(el,'Simulador · detector de secuencia serie (autómata de Mealy)');
  var sel=h('select',{id:'fds',html:'<option>101</option><option selected>1011</option><option>0110</option><option>1111</option><option>11011</option><option>1010</option>'});
  var ov=h('input',{type:'checkbox',id:'fdo'});ov.checked=true;var ovl=h('label',{style:'display:inline-flex;gap:6px;align-items:center'},[ov,h('span',{text:'Con solapamiento'})]);
  var b0=h('button',{class:'btn',type:'button',text:'Enviar 0'}),b1=h('button',{class:'btn',type:'button',text:'Enviar 1'}),br=h('button',{class:'btn',type:'button',text:'Reiniciar'}),bz=h('button',{class:'btn',type:'button',text:'16 bits aleatorios'});
  var tab=h('div',{class:'tt'}),st=h('div',{style:'margin:8px 0'}),wv=h('div',{class:'tt'}),out=h('div',{class:'out'});
  [h('label',{text:'Secuencia que se detecta'}),sel,ovl,tab,h('div',{class:'row'},[b0,b1,bz,br]),st,wv,out].forEach(function(x){el.appendChild(x)});
  var s,cur,xs,ys,sts;
  function auto(){var k=s.length,T=[];
    function nxt(t){var l=Math.min(t.length,k-1);if(t===s&&!ov.checked)return 0;
      for(;l>0;l--){if(t.slice(t.length-l)===s.slice(0,l)&&(ov.checked||l===t.length))return l}return 0}
    for(var j=0;j<k;j++){T[j]=[];for(var x=0;x<2;x++){var t=s.slice(0,j)+x;T[j][x]=[nxt(t),t===s?1:0]}}return T}
  S._fsm=function(seq,over,stream){s=seq;ov.checked=over;var T=auto(),c=0,o=[];stream.forEach(function(x){var r=T[c][x];c=r[0];o.push(r[1])});return o};
  function init(){s=sel.value;cur=0;xs=[];ys=[];sts=[0];draw()}
  function send(x){var T=auto(),r=T[cur][x];xs.push(x);ys.push(r[1]);cur=r[0];sts.push(cur);if(xs.length>24){xs.shift();ys.shift();sts.shift()}draw()}
  function draw(){
    var T=auto(),k=s.length,nb=Math.max(1,Math.ceil(Math.log2(k)));
    var t='<table class="k"><tr><th>Estado</th><th>Recuerda</th><th>E=0</th><th>E=1</th></tr>';
    for(var j=0;j<k;j++)t+='<tr'+(j===cur?' style="background:var(--ok-soft)"':'')+'><td>S'+j+' ('+pad(j.toString(2),nb)+')</td><td>'+(j?('«'+s.slice(0,j)+'»'):'nada')+'</td><td>S'+T[j][0][0]+' / '+T[j][0][1]+'</td><td>S'+T[j][1][0]+' / '+T[j][1][1]+'</td></tr>';
    tab.innerHTML=t+'</table>';
    st.innerHTML=lamp('Estado actual: S'+cur+' ('+pad(cur.toString(2),nb)+')',1)+' <span class="small">'+k+' estados → '+nb+' biestable'+(nb>1?'s':'')+'</span>';
    wv.innerHTML=xs.length?wave([['E',xs],['S',ys,true]],xs.length,Math.max(12,Math.min(26,Math.floor(320/xs.length)))):'';
    out.textContent='Entrada: '+(xs.join('')||'—')+'\nSalida : '+(ys.join('')||'—')+'\n'+(ys.some(function(v){return v})?'✔ La salida vale 1 en el ciclo en que llega el último bit de «'+s+'».':'Envía bits hasta formar «'+s+'».')};
  b0.addEventListener('click',function(){send(0)});b1.addEventListener('click',function(){send(1)});br.addEventListener('click',init);
  bz.addEventListener('click',function(){init();for(var i=0;i<16;i++)send(Math.random()<.5?1:0)});
  sel.addEventListener('change',init);ov.addEventListener('change',init);init();
};
/* ================= Memoria: RAM y cálculo de capacidad ================= */
S.mem=function(el){
  head(el,'Simulador · memoria RAM de 8 palabras de 4 bits y cálculo de chips');
  var ad=h('input',{type:'number',min:'0',max:'7',value:'3',id:'mea'}),dt=h('input',{type:'number',min:'0',max:'15',value:'10',id:'med'}),w=h('button',{class:'btn',type:'button',text:'Escribir (WE = 1)'}),r=h('button',{class:'btn',type:'button',text:'Leer (WE = 0)'});
  var tb=h('div',{class:'tt'}),out=h('div',{class:'out'}),mem=[0,0,0,0,0,0,0,0];
  el.appendChild(h('label',{text:'Dirección (0 a 7, 3 bits)'}));el.appendChild(ad);el.appendChild(h('label',{text:'Dato de entrada (0 a 15, 4 bits)'}));el.appendChild(dt);el.appendChild(h('div',{class:'row',style:'margin-top:8px'},[w,r]));el.appendChild(tb);el.appendChild(out);
  function A(){return Math.max(0,Math.min(7,+ad.value|0))}
  function draw(sel){var t='<table class="k"><tr><th>Dirección</th><th>Contenido</th><th>Hex</th></tr>';
    for(var i=0;i<8;i++)t+='<tr'+(i===sel?' style="background:var(--ok-soft)"':'')+'><td>'+pad(i.toString(2),3)+' ('+i+')</td><td>'+pad(mem[i].toString(2),4)+'</td><td>'+mem[i].toString(16).toUpperCase()+'</td></tr>';tb.innerHTML=t+'</table>'}
  w.addEventListener('click',function(){var a=A(),d=Math.max(0,Math.min(15,+dt.value|0));mem[a]=d;draw(a);out.textContent='Escritura: en la dirección '+a+' se guarda '+pad(d.toString(2),4)+'.'+rest()});
  r.addEventListener('click',function(){var a=A();draw(a);out.textContent='Lectura: la dirección '+a+' contiene '+pad(mem[a].toString(2),4)+' ('+mem[a]+').'+rest()});
  function rest(){return '\n\nCapacidad: 2^3 palabras × 4 bits = 32 bits.'}
  var cwords=h('input',{type:'number',min:'1',value:'16384',id:'cw'}),cwid=h('input',{type:'number',min:'1',value:'16',id:'cwi'}),kw=h('input',{type:'number',min:'1',value:'4096',id:'kw'}),kwi=h('input',{type:'number',min:'1',value:'8',id:'kwi'}),co=h('div',{class:'out'});
  el.appendChild(h('h5',{text:'Cálculo de chips',style:'margin-top:16px'}));
  [['Palabras de la memoria que se quiere',cwords],['Bits por palabra que se quiere',cwid],['Palabras de cada chip',kw],['Bits por palabra de cada chip',kwi]].forEach(function(p){el.appendChild(h('label',{text:p[0]}));el.appendChild(p[1])});el.appendChild(co);
  function calc(){var W=+cwords.value,M=+cwid.value,w2=+kw.value,m2=+kwi.value;if(!(W>0&&M>0&&w2>0&&m2>0)){co.textContent='Escribe números positivos.';return}
    var fil=Math.ceil(W/w2),col=Math.ceil(M/m2),ab=Math.ceil(Math.log2(W)),ac=Math.ceil(Math.log2(w2));
    co.textContent='Direcciones de la memoria: '+ab+' bits  (cada chip usa '+ac+')\nBloques en profundidad: '+fil+' → decodificador de '+(ab-ac>0?(ab-ac)+' → '+fil:'no hace falta')+'\nChips en paralelo por bloque: '+col+'\nTotal: '+fil+' × '+col+' = '+(fil*col)+' chips\nCapacidad: '+(W*M)+' bits'}
  [cwords,cwid,kw,kwi].forEach(function(x){x.addEventListener('input',calc)});calc();draw(-1);
};
/* ================= Divisor de frecuencia y refresco de displays ================= */
S.divf=function(el){
  head(el,'Simulador · divisor de frecuencia y refresco de displays');
  var fc=h('input',{type:'number',value:'50',min:'0.001',step:'any',id:'dfc'}),fo=h('input',{type:'number',value:'1',min:'0.0001',step:'any',id:'dfo'}),out=h('div',{class:'out'});
  var nb=h('input',{type:'number',value:'18',min:'2',max:'30',id:'dfn'}),nd=h('input',{type:'number',value:'4',min:'1',max:'8',id:'dfd'}),o2=h('div',{class:'out'});
  [h('label',{text:'Frecuencia del reloj (MHz)'}),fc,h('label',{text:'Frecuencia que quieres obtener (Hz)'}),fo,out,h('h5',{text:'Refresco de displays multiplexados',style:'margin-top:16px'}),h('label',{text:'Bits del contador de refresco'}),nb,h('label',{text:'Número de dígitos'}),nd,o2].forEach(function(x){el.appendChild(x)});
  function dc(x){return String(x).replace('.',',')}
  function run(){var f=+fc.value*1e6,g=+fo.value;if(!(f>0&&g>0)){out.textContent='Escribe valores positivos.';return}
    var div=f/g,cnt=Math.max(1,Math.round(div/2)),bits=Math.max(1,Math.ceil(Math.log2(cnt))),real=f/(2*cnt),err=Math.abs(real-g)/g*100;
    out.textContent='Factor de división = f_clk / f_out = '+dc(+fc.value)+' MHz / '+dc(g)+' Hz = '+(div<1e12?div.toLocaleString('es-ES'):div.toExponential(3))+'\nLa salida conmuta cada medio periodo: '+cnt.toLocaleString('es-ES')+' ciclos de reloj.\nEl contador cuenta de 0 a '+(cnt-1).toLocaleString('es-ES')+' → '+bits+' bits.\nFrecuencia real obtenida: '+dc(real.toPrecision(6))+' Hz'+(err<1e-9?' (exacta)':' (error '+dc(err.toPrecision(3))+' %)')+'\nCiclo de trabajo: 50 %'}
  function run2(){var f=+fc.value*1e6,n=Math.round(+nb.value),d=Math.round(+nd.value);if(!(f>0&&n>=2&&d>=1)){o2.textContent='Datos no válidos.';return}
    var sb=Math.max(1,Math.ceil(Math.log2(d)));if(sb>=n){o2.textContent='El contador necesita más bits que los que usa la selección ('+sb+').';return}
    var cambio=f/Math.pow(2,n-sb),dig=f/Math.pow(2,n);
    o2.textContent='Los '+sb+' bits altos del contador eligen el dígito.\nCambio de dígito = f_clk / 2^'+(n-sb)+' = '+dc(cambio.toFixed(1))+' Hz\nRefresco de cada dígito = f_clk / 2^'+n+' = '+dc(dig.toFixed(1))+' Hz\n'+(dig>=60?'✔ Por encima de 60 Hz: el ojo no ve parpadeo.':dig>=25?'⚠ Entre 25 y 60 Hz: se nota parpadeo.':'✘ Por debajo de 25 Hz: parpadeo evidente.')+(dig>1000?'\n⚠ Muy rápido: el brillo baja porque cada dígito está encendido muy poco tiempo.':'')}
  [fc,fo].forEach(function(x){x.addEventListener('input',function(){run();run2()})});[nb,nd].forEach(function(x){x.addEventListener('input',run2)});run();run2();
};
/* ================= LUT de 4 entradas ================= */
S.lut=function(el){
  head(el,'Simulador · tabla de búsqueda (LUT) de 4 entradas');
  var pre=h('select',{id:'lup',html:'<option value="xor">XOR de 4 entradas (paridad)</option><option value="and">AND de 4 entradas</option><option value="maj">Mayoría de A, B y C (D no se usa)</option><option value="bcd">BCD no válido (ABCD ≥ 10)</option><option value="cero">Todo ceros</option>'});
  var tg=h('div',{class:'row'}),tb=h('div',{class:'tt'}),out=h('div',{class:'out'}),bits=[],inp={A:0,B:1,C:1,D:0};
  ['A','B','C','D'].forEach(function(v){var c=h('input',{type:'checkbox',id:'lu'+v});c.checked=!!inp[v];c.addEventListener('change',function(){inp[v]=c.checked?1:0;draw()});tg.appendChild(h('label',{style:'display:inline-flex;gap:6px;align-items:center;margin-right:12px'},[c,h('span',{text:v+' = 1'})]))});
  for(var i=0;i<16;i++)bits.push(0);
  function load(){var k=pre.value;for(var m=0;m<16;m++){var a=(m>>3)&1,b=(m>>2)&1,c=(m>>1)&1,d=m&1;
    bits[m]=k==='xor'?(a^b^c^d):k==='and'?(a&b&c&d):k==='maj'?(a+b+c>=2?1:0):k==='bcd'?(m>=10?1:0):0}draw()}
  function draw(){var idx=(inp.A<<3)|(inp.B<<2)|(inp.C<<1)|inp.D,t='<table class="k"><tr><th>ABCD</th><th>Valor guardado</th></tr>';
    for(var m=0;m<16;m++)t+='<tr'+(m===idx?' style="background:var(--ok-soft)"':'')+'><td>'+pad(m.toString(2),4)+'</td><td class="'+(bits[m]?'t1':'t0')+'" data-m="'+m+'">'+bits[m]+'</td></tr>';
    tb.innerHTML=t+'</table>';
    [].forEach.call(tb.querySelectorAll('td[data-m]'),function(td){td.addEventListener('click',function(){bits[+td.getAttribute('data-m')]^=1;draw()})});
    var on=[];bits.forEach(function(v,m){if(v)on.push(m)});
    out.textContent='Entradas ABCD = '+pad(idx.toString(2),4)+' → la LUT lee la posición '+idx+' → salida = '+bits[idx]+'\nF = Σm('+on.join(', ')+')\nForma mínima: F = '+sopStr(4,qm(4,on),['A','B','C','D'])+'\n\nHaz clic en un valor de la tabla para cambiarlo: así se "programa" la LUT. Una LUT de 4 entradas guarda 16 bits y sirve para cualquier función de 4 variables.'}
  pre.addEventListener('change',load);el.appendChild(pre);el.appendChild(tg);el.appendChild(tb);el.appendChild(out);load();
};
})();
