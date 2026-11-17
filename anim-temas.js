/* Electrónica Digital: una animación por bloque de temas */
(function(){var M=window.MANIM;if(!M)return;var U=M.util,C=M.C,nf=U.nf,lerp=U.lerp,ease=U.ease,seg=U.seg,clamp=U.clamp,RG=U.RG,W=640;

/* T0-3 mapa de Karnaugh */
var KM=[[1,1,0,0],[1,1,0,1],[0,0,0,1],[1,1,0,0]],GR=['00','01','11','10'];
M.reg('ed-k',M.base({title:'Simplificar con un mapa de Karnaugh',H:580,dur:18,caps:[[5,'Cada casilla es un minitérmino. Filas y columnas siguen el código Gray (00, 01, 11, 10): casillas vecinas difieren en un solo bit.'],[11,'Se agrupan los unos en rectángulos de 1, 2, 4 u 8 casillas, lo más grandes posible. El mapa se «cierra» por los bordes: la fila de arriba es vecina de la de abajo.'],[99,'Cada grupo da un producto con las variables que no cambian dentro de él. La suma de los grupos es la expresión mínima.']]},
 function(D,t){var x0=200,y0=120,c=70,show=Math.floor(seg(t,0.5,5)*16);D.text('AB \\ CD',x0-20,y0-18,{s:15,c:C.mut,a:'right'});
  GR.forEach(function(g,i){D.text(g,x0+i*c+c/2,y0-12,{s:16,a:'center',c:C.f,mono:true});D.text(g,x0-14,y0+i*c+c/2+6,{s:16,a:'right',c:C.f,mono:true});});
  for(var r=0;r<4;r++)for(var k=0;k<4;k++){D.rect(x0+k*c,y0+r*c,c,c,C.grid,null,1.2);if(r*4+k<show)D.text(KM[r][k]+'',x0+k*c+c/2,y0+r*c+c/2+8,{s:22,a:'center',c:KM[r][k]?C.m:C.mut,bold:!!KM[r][k]});}
  var G=[[[[0,0,2,2]],C.ok,"A'C'",6],[[[3,0,2,1],[0,0,2,1]],C.hl,"B'C'",9],[[[1,3,1,2]],C.bad,"BCD'",12]];var expr=[];
  G.forEach(function(g,gi){var a=ease(seg(t,g[3],g[3]+1.5));if(a<=0)return;expr.push(g[2]);D.ctx.save();D.ctx.globalAlpha=a;g[0].forEach(function(r){var in_=gi===1?9:5;D.rect(x0+r[1]*c+in_,y0+r[0]*c+in_,r[2]*c-2*in_,r[3]*c-2*in_,g[1],RG(g[1],.12),3);});D.ctx.restore();});
  U.readout(D,[expr.length?'F = '+expr.join(' + '):'F(A,B,C,D) = Σm(0,1,4,5,6,8,9,14) (rellenando)'],y0+4*c+60);}));

/* T4-5 sumador de 4 bits con acarreo en serie */
M.reg('ed-sum',M.base({title:'Sumador de 4 bits: el acarreo se propaga',H:560,dur:16,caps:[[5,'Cada sumador completo suma dos bits y el acarreo que le llega: <i>S = A ⊕ B ⊕ C<sub>in</sub></i>, <i>C<sub>out</sub> = AB + C<sub>in</sub>(A ⊕ B)</i>.'],[10,'El acarreo de cada etapa entra en la siguiente: el resultado final tiene que esperar a que el acarreo recorra todas las etapas.'],[99,'Por eso el retardo crece con el número de bits. Los sumadores con acarreo anticipado (carry look-ahead) calculan los acarreos en paralelo.']]},
 function(D,t){var A=[1,0,1,1],B=[0,1,1,1],n=Math.floor(seg(t,1,12)*4.999),c=0,S=[],Cs=[0],x0=470,w=110;for(var i=0;i<4;i++){var a=A[3-i],b=B[3-i],s=a^b^c;c=(a&b)|(c&(a^b));S.push(s);Cs.push(c);}
  D.text('A =',40,140,{s:20,c:C.f,mono:true});D.text('B =',40,190,{s:20,c:C.f,mono:true});
  for(var j=0;j<4;j++){var x=x0-j*w;D.text(A[3-j]+'',x,140,{s:24,a:'center',c:C.f,mono:true,bold:true});D.text(B[3-j]+'',x,190,{s:24,a:'center',c:C.f,mono:true,bold:true});
   D.rect(x-38,220,76,64,j<n?C.m:C.grid,j<n?RG(C.m,.12):null,2);D.text('SC',x,258,{s:15,a:'center',c:j<n?C.m:C.mut});
   if(j<n){D.text(S[j]+'',x,330,{s:26,a:'center',c:C.m,mono:true,bold:true});if(j<3||n>3)D.arrow(x-38,268,x-w+38,268,Cs[j+1]?C.bad:C.mut,2.4);D.text('C='+Cs[j+1],x-w/2,300,{s:14,a:'center',c:Cs[j+1]?C.bad:C.mut,mono:true});}
   else D.text('?',x,330,{s:24,a:'center',c:C.mut});}
  if(n>=4)D.text(Cs[4]+'',x0-4*w,330,{s:26,a:'center',c:C.bad,mono:true,bold:true});D.line(60,300+12,W-40,300+12,C.ax,1.4);
  U.readout(D,['1011 (11) + 0111 (7) = '+(n>=4?'10010 (18)':'…'),'etapas resueltas: '+Math.min(n,4)+' de 4'],430);}));

/* T6-9 contador binario asíncrono */
M.reg('ed-cont',M.base({title:'Contador binario de 4 bits: cronograma',H:580,dur:18,caps:[[6,'Cada biestable T cambia de estado cuando su entrada de reloj recibe un flanco. Q₀ cambia con cada flanco del reloj.'],[12,'Cada salida tiene la mitad de frecuencia que la anterior: Q₁ = f/4, Q₂ = f/8, Q₃ = f/16. Es un divisor de frecuencia.'],[99,'Leyendo Q₃Q₂Q₁Q₀ en cada instante se obtiene la cuenta en binario, de 0000 a 1111, y vuelta a empezar.']]},
 function(D,t){var N=16,x0=110,w=28,u=seg(t,0.5,17)*N,rows=['CLK','Q₀','Q₁','Q₂','Q₃'];rows.forEach(function(r,k){var y=130+k*70,p=[];D.text(r,x0-14,y-8,{s:16,a:'right',c:k?C.m:C.f});
   for(var i=0;i<N*2;i++){var tt=i/2;if(tt>u)break;var v=k===0?(i%2===0?1:0):((Math.floor(i/2+(i%2?0.5:0)+0.5)>>(k-1))&1);var cnt=Math.floor((i+1)/2);v=k===0?(i%2===0?1:0):((cnt>>(k-1))&1);var yy=y-v*34;p.push([x0+tt*w,yy]);p.push([x0+Math.min(tt+0.5,u)*w,yy]);}
   D.path(p,k?C.m:C.f,2.4);D.line(x0,y,x0+N*w,y,C.grid,1);});
  var cnt=Math.floor((Math.floor(u*2)+1)/2)%16,b=('000'+cnt.toString(2)).slice(-4);D.rect(x0+Math.floor(u)*w,90,w,370,null,RG(C.y,.08));
  U.readout(D,['Q₃Q₂Q₁Q₀ = '+b+'  →  '+cnt],520);}));

/* T10-11 máquina de estados de Moore que detecta 101 */
var IN='1101011010'.split('').map(Number),TR={S0:['S0','S1'],S1:['S2','S1'],S2:['S0','S3'],S3:['S2','S1']};
var SQ=(function(){var s='S0',o=[s];IN.forEach(function(b){s=TR[s][b];o.push(s);});return o;})();
M.reg('ed-fsm',M.base({title:'Autómata de Moore: detector de la secuencia 101',H:580,dur:20,caps:[[6,'Cada estado recuerda qué parte de la secuencia se ha visto: S0 nada, S1 «1», S2 «10», S3 «101» (salida Z = 1).'],[13,'En cada flanco de reloj se lee un bit y se sigue la flecha correspondiente. La salida depende solo del estado (Moore).'],[99,'Las secuencias solapadas también se detectan: desde S3, un «0» lleva a S2 porque ese «10» ya sirve para la siguiente detección.']]},
 function(D,t){var P={S0:[110,240],S1:[260,140],S2:[410,240],S3:[260,350]},k=Math.min(IN.length,Math.floor(seg(t,1,19)*(IN.length+0.999))),cur=SQ[k];
  var E=[['S0','S1','1',170,178],['S1','S2','0',350,178],['S2','S3','1',368,328],['S3','S2','0',298,326],['S3','S1','1',232,300],['S2','S0','0',180,228]];
  E.forEach(function(e){var a=P[e[0]],b=P[e[1]],ang=Math.atan2(b[1]-a[1],b[0]-a[0]),off=-14,nx=-Math.sin(ang)*off,ny=Math.cos(ang)*off,x1=a[0]+36*Math.cos(ang)+nx,y1=a[1]+36*Math.sin(ang)+ny,x2=b[0]-36*Math.cos(ang)+nx,y2=b[1]-36*Math.sin(ang)+ny;
   var on=k>0&&SQ[k-1]===e[0]&&cur===e[1];D.arrow(x1,y1,x2,y2,on?C.hl:C.ax,on?3:1.6);D.text(e[2],e[3],e[4],{s:15,a:'center',c:on?C.hl:C.mut,mono:true});});
  Object.keys(P).forEach(function(s){var p=P[s],on=s===cur;D.dot(p[0],p[1],34,on?RG(C.m,.25):RG(C.f,.08));D.ring(p[0],p[1],34,on?C.m:C.f,on?3:1.6);D.text(s,p[0],p[1]-2,{s:17,a:'center',c:on?C.m:C.f,bold:true});D.text('Z='+(s==='S3'?1:0),p[0],p[1]+18,{s:12,a:'center',c:C.mut});});
  D.ring(80,212,16,C.ax,1.6);D.text('0',58,200,{s:15,c:C.mut,mono:true});D.ring(290,112,16,C.ax,1.6);D.text('1',308,100,{s:15,c:C.mut,mono:true});
  var x0=470;D.text('entrada:',x0,330,{s:14,c:C.mut});IN.forEach(function(b,i){D.text(b+'',x0+i*14,355,{s:17,c:i<k?(i===k-1?C.hl:C.w):C.mut,mono:true,bold:i===k-1});});
  U.readout(D,['estado '+cur+'    Z = '+(cur==='S3'?'1  ← 101 detectado':'0')],480);}));

/* T12-13 VHDL: un registro con reset síncrono */
var VH=['process (clk) begin','  if rising_edge(clk) then','    if rst = \'1\' then q <= x"00";','    elsif en = \'1\' then q <= d;','    end if;','  end if;','end process;'];
var VD=[[0,0,0x00],[1,0,0x3A],[0,1,0x3A],[0,1,0x7F],[0,0,0x7F],[0,1,0x15],[1,1,0x15],[0,1,0x42]];
M.reg('ed-vhdl',M.base({title:'VHDL: un registro y su simulación',H:600,dur:20,caps:[[6,'El proceso solo hace algo en el flanco de subida del reloj: describe un registro de 8 bits con reset síncrono y habilitación.'],[13,'En cada flanco: si rst = 1, q se pone a 00; si no y en = 1, q copia d; si en = 0, q conserva su valor.'],[99,'La simulación lo confirma: q solo cambia en los flancos. El sintetizador infiere 8 biestables D con un multiplexor de carga.']]},
 function(D,t){var n=Math.min(8,Math.floor(seg(t,0.5,19)*8.999)),x0=150,cw=55,q=0,Q=[];for(var i=0;i<8;i++){var v=VD[i];if(v[0])q=0;else if(v[1])q=v[2];Q.push(q);}
  var cur=n>0?VD[n-1]:null,line=cur?(cur[0]?2:(cur[1]?3:4)):1;VH.forEach(function(l,i){var y=90+i*24,on=i===line||(i===1&&n>0);D.text(l,40,y,{s:14,c:on&&i===line?C.y:C.w,mono:true,bold:on&&i===line});});
  var rows=[['clk',C.f],['rst',C.bad],['en',C.ok],['d',C.hl],['q',C.m]],y0=300;rows.forEach(function(r,k){var y=y0+k*44;D.text(r[0],x0-14,y+4,{s:15,a:'right',c:r[1],mono:true});
   for(var i=0;i<8;i++){var x=x0+i*cw;if(i>=n&&k>0)break;if(k===0){D.path([[x,y+10],[x,y-10],[x+cw/2,y-10],[x+cw/2,y+10],[x+cw,y+10]],r[1],2);continue;}
    if(k<3){var b=VD[i][k-1];D.line(x,y+(b?-10:10),x+cw,y+(b?-10:10),r[1],2.2);if(i&&VD[i-1][k-1]!==b)D.line(x,y-10,x,y+10,r[1],2.2);}
    else{var val=k===3?VD[i][2]:(i?Q[i-1]:0);if(k===4&&i<n)val=Q[i];var hx=('0'+val.toString(16).toUpperCase()).slice(-2);D.path([[x+4,y-10],[x+cw-4,y-10],[x+cw,y],[x+cw-4,y+10],[x+4,y+10],[x,y],[x+4,y-10]],r[1],1.6);D.text(hx,x+cw/2,y+5,{s:13,a:'center',c:r[1],mono:true});}}});
  if(n>0)D.rect(x0+(n-1)*cw,y0-20,4,5*44,null,RG(C.y,.6));}));

M.reg('ed-c2',M.base({title:'Complemento a dos: la rueda de 4 bits',H:600,dur:18,caps:[[6,'Con 4 bits hay 16 combinaciones. En complemento a dos, las que empiezan por 1 representan negativos: van de −8 (1000) a +7 (0111).'],[12,'Sumar es avanzar por la rueda. Pasar de 0111 (+7) a 1000 (−8) es un desbordamiento: el resultado no cabe en 4 bits.'],[99,'Para cambiar de signo: invertir los bits y sumar 1. Por ejemplo, +3 = 0011 → 1100 + 1 = 1101 = −3.']]},
 function(D,t){var cx=W/2,cy=300,R=170,k=Math.floor(t*1.2)%16;for(var i=0;i<16;i++){var a=-Math.PI/2+i*2*Math.PI/16,x=cx+R*Math.cos(a),y=cy+R*Math.sin(a),v=i<8?i:i-16,on=i===k;
   D.dot(x,y,on?26:20,on?RG(C.m,.3):RG(v<0?C.bad:C.f,.12));D.text(('000'+i.toString(2)).slice(-4),x,y-1,{s:on?15:13,a:'center',c:on?C.m:C.w,mono:true,bold:on});D.text((v>0?'+':'')+v,x,y+15,{s:12,a:'center',c:v<0?C.bad:C.f});}
  D.ctx.save();D.ctx.setLineDash([5,4]);var a7=-Math.PI/2+7.5*2*Math.PI/16;D.line(cx+0.7*R*Math.cos(a7),cy+0.7*R*Math.sin(a7),cx+1.25*R*Math.cos(a7),cy+1.25*R*Math.sin(a7),C.hl,2);D.ctx.restore();D.text('desbordamiento',cx+1.05*R*Math.cos(a7)-20,cy+1.05*R*Math.sin(a7)+30,{s:14,c:C.hl,a:'right'});
  var v=k<8?k:k-16;D.text(('000'+k.toString(2)).slice(-4)+' = '+(v>0?'+':'')+v,cx,cy+8,{s:24,a:'center',c:C.m,mono:true,bold:true});}));
})();
