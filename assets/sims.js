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
