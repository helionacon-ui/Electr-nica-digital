%% id=h-karnaugh
%% group=hojadata
%% n=1
%% title=Hoja de problemas · Diseño combinacional con Karnaugh
%% sub=10 problemas: mayoría, divisor, multiplicador, producción en serie, barco, decodificadores a 7 segmentos, comparador, máquina de monedas y binario a BCD.
%% anio=Hojas
%% tipo=Hoja

@ej k1|K1 · Mayoría de tres entradas|Hoja Karnaugh · K1|comb|k1
@enun
Diseña un circuito con tres entradas $S_2,S_1,S_0$ cuya salida $S$ vale 1 cuando **al menos dos** de las entradas valen 1 (circuito de mayoría, por ejemplo para un votador de tres sensores).
@end
@antes
**Qué piden:** tabla de verdad, ecuación mínima y esquema.
**Teoría:** minterms, mapa de Karnaugh de 3 variables y grupos de 2 y 4 casillas ([[t03|T3]]).
@end
@paso Tabla de verdad
$S=1$ en las combinaciones con dos o tres unos: $011,101,110,111$, es decir $S=\sum m(3,5,6,7)$.
@end
@paso Mapa de Karnaugh
@fig kmap {"key":"k1.S","n":3,"names":["S2","S1","S0"],"title":"Mayoría de tres","cap":"Tres grupos de dos casillas. Cada par de entradas forma un producto."}
Los tres grupos son $S_1S_0$, $S_2S_0$ y $S_2S_1$.
@end
@paso Ecuación y puertas
$S={{k1.S}}$: tres AND de dos entradas y una OR de tres. En NAND-NAND: tres NAND de dos entradas y una NAND de tres.
@end
@res
$S={{k1.S}}$ (verificada con las 8 combinaciones).
@end
@end

@ej k2|K2 · Divisor de dos números de 2 bits|Hoja Karnaugh · K2|comb,arit|k2
@enun
Diseña un circuito combinacional que divida el número $A=A_1A_0$ entre $B=B_1B_0$ (ambos de 2 bits, sin signo). Salidas: cociente $C_1C_0$ y resto $R_1R_0$. El caso $B=0$ no puede darse (indiferente).
@end
@antes
**Qué piden:** cuatro funciones de cuatro variables con indiferentes.
**Teoría:** Karnaugh de 4 variables con indiferentes ([[t03|T3]]).
@end
@paso Qué hace el circuito
Es la división entera: $A=B\cdot C+R$ con $0\le R<B$. Como $A\le3$, el cociente cabe en 2 bits. Ejemplos: $3/2\to C=1,R=1$; $3/1\to C=3,R=0$; $2/3\to C=0,R=2$.
@end
@paso Un mapa por salida
Las cuatro filas con $B_1B_0=00$ son indiferentes (4 casillas «X» en cada mapa). El mapa de $C_1$:
@fig kmap {"key":"k2.C1","n":4,"names":["A1","A0","B1","B0"],"title":"C1 (cociente, bit alto)","cap":"$C_1=1$ solo si $A\\ge2B$ con cociente $\\ge2$: $A=2$ o $3$ y $B=1$."}
@end
@paso Ecuaciones
$$C_1={{k2.C1}}\qquad C_0={{k2.C0}}$$
$$R_1={{k2.R1}}\qquad R_0={{k2.R0}}$$
@end
@res
Las cuatro ecuaciones anteriores. Comprobadas contra la división entera en las 12 combinaciones válidas.
@end
@end

@ej k4|K4 · Multiplicador de 2 × 2 bits|Hoja Karnaugh · K4|comb,arit|k4
@enun
Diseña un multiplicador combinacional de dos números de 2 bits $A=A_1A_0$ y $B=B_1B_0$. El producto tiene 4 bits $S_3S_2S_1S_0$.
@end
@antes
**Qué piden:** cuatro funciones de cuatro variables, sin indiferentes.
**Teoría:** Karnaugh de 4 variables ([[t03|T3]]); producto binario como suma de productos parciales ([[t02|T2]]).
@end
@paso Rango del producto
$3\times3=9$ cabe en 4 bits. Todas las combinaciones son válidas.
@end
@paso Mapas
@fig kmap {"key":"k4.S1","n":4,"names":["A1","A0","B1","B0"],"title":"S1 del producto","cap":"$S_1$ es la función más complicada: cuatro grupos de dos casillas."}
@end
@paso Ecuaciones
$$S_3={{k4.S3}}\qquad S_2={{k4.S2}}$$
$$S_1={{k4.S1}}\qquad S_0={{k4.S0}}$$
$S_0=A_0B_0$ es la AND de los bits menos significativos. $S_3=1$ solo con $3\times3=9$.
@end
@res
Las cuatro ecuaciones anteriores, verificadas con las 16 combinaciones. Alternativa sin Karnaugh: cuatro AND de partida y dos semisumadores.
@end
@end

@ej k5|K5 · Cuatro máquinas en serie: estado de la producción|Hoja Karnaugh · K5|comb|k5
@enun
Una línea de producción tiene cuatro máquinas $S_3S_2S_1S_0$ (1 = funcionando). Un panel tiene cuatro indicadores: **TA** (las cuatro funcionan), **MA** (al menos tres funcionan), **I** (funcionan exactamente dos) y **MR** (funciona una o ninguna). Diseña el circuito que los activa. Este es el reparto que se usa aquí.
@end
@antes
**Qué piden:** cuatro funciones de cuatro variables según el **número de unos**.
**Teoría:** Karnaugh de 4 variables y grupos de 2, 4 y 8 casillas ([[t03|T3]]).
@end
@paso Contar los unos
Sea $n$ el número de máquinas que funcionan. TA: $n=4$. MA: $n\ge3$. I: $n=2$. MR: $n\le1$. Los indicadores MA y TA se solapan (con $n=4$ ambos valen 1) pero I y MR no.
@end
@paso Ecuaciones
$$TA={{k5.TA}}$$
$$MA={{k5.MA}}$$
$$MR={{k5.MR}}$$
$$I={{k5.I}}$$
I necesita seis productos de cuatro variables: los seis unos del mapa son todas las casillas aisladas, ninguna se puede agrupar con otra. Es el caso típico donde **no** simplifica el mapa.
@end
@box ojo | I (exactamente 2) no se simplifica
Los unos de «exactamente dos» están en las casillas de peso 2: cada una tiene como vecinas casillas de peso 1 o 3, que valen 0. Por eso ningún grupo mayor que 1 es posible. Tras Karnaugh, la ecuación sigue siendo la suma de seis minterms.
@end
@res
TA, MA, MR e I con las ecuaciones anteriores. Verificadas con las 16 combinaciones.
@end
@end

@ej k6|K6 · Indicador de rumbo de un barco (4 entradas, 7 segmentos)|Hoja Karnaugh · K6|comb,msi|k6
@enun
Una brújula electrónica da cuatro señales $N,S,E,O$ (1 = el barco apunta en esa dirección). Se muestra en un display de 7 segmentos: N enciende $a$; S enciende $d$; E enciende $b,c$; O enciende $e,f$; y las direcciones intermedias combinan las dos (NE: $a,b$; NO: $a,f$; SE: $c,d$; SO: $d,e$). No pueden valer 1 a la vez $N$ y $S$, ni $E$ y $O$. Si todas valen 0, no se encuentra nada (indiferente).
@end
@antes
**Qué piden:** siete funciones (a–g) con muchos indiferentes.
**Teoría:** indiferentes en Karnaugh ([[t03|T3]]), displays de 7 segmentos ([[t05|T5]]).
@end
@paso Indiferentes
Las combinaciones con $N=S=1$ o $E=O=1$ y la combinación 0000 son indiferentes: 8 de las 16.
@end
@paso Ecuaciones
$$a={{k6.a}}\qquad b={{k6.b}}\qquad c={{k6.c}}\qquad d={{k6.d}}$$
$$e={{k6.e}}\qquad f={{k6.f}}\qquad g={{k6.g}}$$
Con tantos indiferentes cada segmento queda con **un solo literal** o dos: $a=N$ (el segmento de arriba se enciende siempre que hay norte), $d=S$.
@end
@box idea | Por qué sale tan simple
Una combinación indiferente se usa como 1 si ayuda a hacer un grupo mayor. Aquí las prohibidas ($N=S=1$, $E=O=1$) permiten agrupar casillas lejanas y el segmento $g$ no se enciende nunca.
@end
@res
$a=N$; $b=\overline{S}E$; $c=\overline{N}E$; $d=S$; $e=\overline{N}O$; $f=\overline{S}O$; $g=0$.
@end
@end

@ej k7|K7 · Decodificador BCD a 7 segmentos|Hoja Karnaugh · K7|comb,msi|k7
@enun
Diseña el decodificador de un dígito BCD $ABCD$ ($A$ es el bit de más peso) a las siete señales $a,\dots,g$ de un display de ánodo/cátodo común activas a 1. Las combinaciones 10 a 15 no existen (indiferentes). Los dígitos se dibujan con la forma habitual: el 6 lleva el segmento $a$, el 7 solo $a,b,c$ y el 9 lleva el segmento $d$.
@end
@antes
**Qué piden:** siete funciones de cuatro variables con 6 indiferentes.
**Teoría:** Karnaugh con indiferentes ([[t03|T3]]), display de 7 segmentos ([[t05|T5]]).
@end
@paso Tabla de segmentos
| Dígito | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 4 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 6 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| 7 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 8 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
@end
@paso Un mapa por segmento
@fig kmap {"key":"k7.e","n":4,"names":["A","B","C","D"],"title":"Segmento e","cap":"El segmento $e$ solo se enciende en 0, 2, 6 y 8. Con los indiferentes se agrupa en dos grupos."}
@end
@paso Ecuaciones
$$a={{k7.a}}\qquad b={{k7.b}}\qquad c={{k7.c}}$$
$$d={{k7.d}}$$
$$e={{k7.e}}\qquad f={{k7.f}}\qquad g={{k7.g}}$$
@end
@res
Las siete ecuaciones anteriores, comprobadas con los 10 dígitos válidos (los indiferentes no se comprueban).
@end
@end

@ej k8|K8 · Comparador de dos números de 2 bits|Hoja Karnaugh · K8|comb,msi|k8
@enun
Diseña un comparador de $A=A_1A_0$ y $B=B_1B_0$ con tres salidas: $GT$ ($A>B$), $EQ$ ($A=B$) y $LT$ ($A<B$).
@end
@antes
**Qué piden:** tres funciones de cuatro variables.
**Teoría:** comparadores y Karnaugh ([[t03|T3]], [[t05|T5]]).
@end
@paso Mapas
@fig kmap {"key":"k8.GT","n":4,"names":["A1","A0","B1","B0"],"title":"GT: A > B","cap":"Seis casillas en escalera: tres grupos de dos."}
$EQ$ vale 1 en la diagonal: cuatro casillas que no se pueden agrupar. $LT$ es simétrica a $GT$.
@end
@paso Ecuaciones
$$GT={{k8.GT}}$$
$$LT={{k8.LT}}$$
$$EQ={{k8.EQ}}$$
@end
@box idea | Atajo para EQ
$EQ=\overline{(A_1\oplus B_1)+(A_0\oplus B_0)}$: dos XOR y una NOR. Es lo mismo que la suma de cuatro minterms, con menos puertas. También se obtiene como $EQ=\overline{GT+LT}$.
@end
@res
Las tres ecuaciones anteriores (con $EQ$ en minterms o con XOR), verificadas con las 16 combinaciones.
@end
@end

@ej k9|K9 · Máquina de monedas con cambio|Hoja Karnaugh · K9|comb|k9
@enun
Una máquina vende un producto de 40 céntimos. Admite hasta dos monedas de 25 ($E_{25A},E_{25B}$), una de 10 ($E_{10}$) y una de 5 ($E_5$): cada entrada vale 1 si esa moneda se ha introducido. La salida $P$ entrega el producto si la suma llega a 40 o más. El cambio se devuelve con dos dispensadores de 10 ($C_{10A}$, $C_{10B}$) y uno de 5 ($C_5$).
@end
@antes
**Qué piden:** cuatro funciones; hay que calcular el cambio $=\text{suma}-40$ y repartirlo en monedas de 10 y 5.
**Teoría:** Karnaugh ([[t03|T3]]), tabla de verdad a partir de un texto.
@end
@paso Tabla de casos relevantes
La suma máxima es 65 céntimos. El producto se entrega con suma $\ge40$.
| Monedas | Suma | $P$ | Cambio | Dispensadores |
|---|---|---|---|---|
| 25 + 25 | 50 | 1 | 10 | $C_{10A}$ |
| 25 + 25 + 10 | 60 | 1 | 20 | $C_{10A},C_{10B}$ |
| 25 + 25 + 5 | 55 | 1 | 15 | $C_{10A},C_5$ |
| 25 + 25 + 10 + 5 | 65 | 1 | 25 | $C_{10A},C_{10B},C_5$ |
| 25 + 10 + 5 | 40 | 1 | 0 | ninguno |
| 25 + 10 | 35 | 0 | 0 | ninguno |
Con una sola moneda de 25 y sin la de 10 y la de 5 juntas no se llega a 40.
@end
@paso Ecuaciones
$$P={{k9.P}}$$
$$C_{10A}={{k9.C10A}}\qquad C_{10B}={{k9.C10B}}\qquad C_5={{k9.C5}}$$
El cambio solo existe cuando se han metido **las dos** de 25 (50 céntimos): por eso las tres salidas contienen $E_{25A}E_{25B}$.
@end
@res
Las cuatro ecuaciones anteriores, verificadas con las 16 combinaciones (suma máxima {{k9.max}} céntimos).
@end
@end

@ej k10|K10 · Nota de 0 a 10 en un display de barras|Hoja Karnaugh · K10|comb,msi|k10
@enun
Una nota de 0 a 10 llega en binario ($N_3N_2N_1N_0$). Se visualiza en un display de 7 segmentos como una **barra que crece**: de 0 a 4 solo se enciende $g$ (un guion: suspenso); 5 enciende $a$; 6, $a,b$; 7 y 8, $a,b,c$; 9, $a,b,c,d$; y 10 enciende $a,\dots,f$. Las combinaciones 11 a 15 son indiferentes.
@end
@antes
**Qué piden:** siete funciones con 5 indiferentes.
**Teoría:** Karnaugh con indiferentes ([[t03|T3]]).
@end
@paso Ecuaciones
$$a={{k10.a}}\qquad b={{k10.b}}\qquad c={{k10.c}}$$
$$d={{k10.d}}\qquad e={{k10.e}}\qquad f={{k10.f}}\qquad g={{k10.g}}$$
Fíjate en que $e$ y $f$ valen lo mismo: solo se encienden con la nota 10.
@end
@res
Las siete ecuaciones anteriores, comprobadas para las notas 0 a 10.
@end
@end

@ej k17|K17 · Binario de 4 bits a dos dígitos BCD|Hoja Karnaugh · K17|comb,arit|k17
@enun
Un número binario $E_3E_2E_1E_0$ (0 a 15) se convierte a **dos dígitos BCD**: decenas $D$ (un solo bit, vale 0 o 1) y unidades $U_3U_2U_1U_0$.
@end
@antes
**Qué piden:** cinco funciones de cuatro variables.
**Teoría:** BCD y binario ([[t02|T2]]), Karnaugh ([[t03|T3]]).
@end
@paso Idea
Para $E\le9$ el BCD coincide con el binario. Para $10\le E\le15$ las decenas valen 1 y las unidades son $E-10$ (0 a 5). Por ejemplo, $13=0\,1101\to D=1$, unidades $=0011$.
@end
@paso Ecuaciones
$$D={{k17.D}}\qquad U_0={{k17.U0}}$$
$$U_3={{k17.U3}}\qquad U_2={{k17.U2}}\qquad U_1={{k17.U1}}$$
$U_0=E_0$: restar 10 no cambia la paridad.
@end
@res
Las cinco ecuaciones anteriores, verificadas con las 16 combinaciones.
@end
@end
