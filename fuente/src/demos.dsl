%% id=demos
%% group=demo
%% n=1
%% title=Demostraciones
%% short=Demostraciones
%% sub=Por qué son ciertas las reglas que usas: De Morgan, consenso, C2, sumador, universalidad de NAND, JK, contadores, Johnson y LFSR.

Aquí se demuestran, paso a paso, las reglas que en los temas se usan sin discutir. En el examen no suelen pedir la demostración entera, pero **entender el porqué** te permite reconstruir la regla si la olvidas. Todos los enunciados se han comprobado además por código con todos los casos posibles.

@ej d1|D1 · Leyes de De Morgan|Demostración D1|demostración|d.demorgan
@enun
Demuestra que $\overline{A+B}=\overline{A}\cdot\overline{B}$ y que $\overline{A\cdot B}=\overline{A}+\overline{B}$.
@end
@antes
**Qué piden:** probar una igualdad entre funciones lógicas.
**Idea:** dos funciones son iguales si valen lo mismo para **todas** las combinaciones de entradas (inducción perfecta).
@end
@paso Tabla de verdad
| $A$ | $B$ | $\overline{A+B}$ | $\overline{A}\,\overline{B}$ | $\overline{AB}$ | $\overline{A}+\overline{B}$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 |
Las columnas 3 y 4 coinciden; las 5 y 6 también. Con dos variables hay solo 4 filas: la prueba es completa.
@end
@paso La idea en palabras
$\overline{A+B}$ vale 1 solo si **ninguna** de las dos vale 1, es decir, si $A=0$ **y** $B=0$. $\overline{AB}$ vale 0 solo si las dos valen 1, es decir, vale 1 si **alguna** vale 0.
@end
@paso Generalización
Se aplica a $n$ variables: $\overline{A+B+C}=\overline{A}\,\overline{B}\,\overline{C}$. La regla práctica: **cambia + por · (y al revés) y niega cada término**.
@end
@res
Demostrado por inducción perfecta (y comprobado también con tres variables).
@end
@end

@ej d2|D2 · Adyacencia, absorción y consenso|Demostración D2|demostración|d.adyacencia,d.absorcion,d.consenso
@enun
Demuestra: (a) $AB+A\overline{B}=A$; (b) $A+AB=A$; (c) $AB+\overline{A}C+BC=AB+\overline{A}C$.
@end
@antes
**Qué piden:** tres identidades que justifican los grupos de Karnaugh.
**Idea:** sacar factor común y usar $X+\overline{X}=1$.
@end
@paso (a) Adyacencia
$AB+A\overline{B}=A(B+\overline{B})=A\cdot1=A$. Es la regla que hace que **dos casillas vecinas** del mapa se simplifiquen: la variable que cambia desaparece.
@end
@paso (b) Absorción
$A+AB=A(1+B)=A\cdot1=A$. Si $A=1$ la suma ya vale 1, y si $A=0$ el término $AB$ también vale 0.
@end
@paso (c) Consenso
Se multiplica el término $BC$ por $(A+\overline{A})=1$:
$$BC=BC(A+\overline{A})=ABC+\overline{A}BC.$$
Entonces $AB+\overline{A}C+ABC+\overline{A}BC$. Pero $ABC$ está absorbido por $AB$ y $\overline{A}BC$ por $\overline{A}C$ (absorción). Queda $AB+\overline{A}C$.
@end
@box ojo | Para qué sirve el consenso
En un circuito con **aleas** (fallos momentáneos) a veces se **añade** el término de consenso a propósito. En el diseño con mínimos se **quita**.
@end
@res
Las tres identidades se demuestran con factor común y $X+\overline{X}=1$.
@end
@end

@ej d3|D3 · Por qué invertir y sumar 1 da el opuesto en C2|Demostración D3|demostración|d.c2.4
@enun
Demuestra que en complemento a 2 de $n$ bits el opuesto de $N$ es $\overline{N}+1$.
@end
@antes
**Qué piden:** justificar la regla de «invertir y sumar 1».
**Idea:** el C2 de $N$ se define como $2^n-N$. Sumar $N$ y su C2 da $2^n$, que en $n$ bits es 0.
@end
@paso Un número más su inverso
Si inviertes todos los bits de $N$, cada posición suma $1$ con la de $N$: $N+\overline{N}=11\dots1=2^n-1$.
@end
@paso Despejar el opuesto
$$-N\equiv2^n-N=(2^n-1-N)+1=\overline{N}+1.$$
Eso es exactamente «invertir y sumar 1». En $n$ bits, $2^n$ se descarta (es el acarreo final), así que $N+(\overline{N}+1)=0$.
@end
@paso Ejemplo
Con 4 bits, $N=0101=5$: $\overline{N}=1010$, $+1=1011$. Comprobación: $0101+1011=1\,0000$; el acarreo se descarta y queda $0000$. Entonces $1011=-5$.
@end
@res
$-N=\overline{N}+1$ porque $N+\overline{N}=2^n-1$. Comprobado con todos los números de 3, 4, 5 y 8 bits.
@end
@end

@ej d4|D4 · Por qué restar es sumar el inverso y un 1|Demostración D4|demostración|d.resta.4
@enun
Demuestra que $A-B=A+\overline{B}+1$ en un sumador de $n$ bits (módulo $2^n$).
@end
@antes
**Qué piden:** justificar que un sumador sirve también como restador.
**Teoría:** D3.
@end
@paso Aplicar D3
Por D3, $-B=\overline{B}+1$ módulo $2^n$.
@end
@paso Sumar
$A-B=A+(-B)=A+\overline{B}+1$. El «+1» se introduce como **acarreo de entrada** $C_{in}=1$, sin gastar otro sumador.
@end
@res
Un sumador con $B$ invertida y $C_{in}=1$ calcula $A-B$. Comprobado con las $2^{8}$ combinaciones de 4 bits y con 8 bits.
@end
@end

@ej d5|D5 · Ecuaciones del sumador completo|Demostración D5|demostración|d.fa,d.fa2
@enun
Demuestra que un sumador completo tiene $S=A\oplus B\oplus C_{in}$ y $C_{out}=AB+C_{in}(A\oplus B)$.
@end
@antes
**Qué piden:** pasar de «suma de tres bits» a ecuaciones lógicas.
**Idea:** la suma $A+B+C_{in}$ va de 0 a 3 y se escribe $C_{out}S$ en binario.
@end
@paso Tabla
| $A+B+C_{in}$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $C_{out}S$ | 00 | 01 | 10 | 11 |
$S$ vale 1 cuando el número de unos es **impar**: es la XOR de tres entradas. $C_{out}$ vale 1 cuando hay **dos o más** unos: es la mayoría de tres.
@end
@paso Mayoría de tres
La mayoría de tres es $AB+AC_{in}+BC_{in}$ (ver K1 en las hojas). Se agrupa: $AB+C_{in}(A+B)$. Y como $AB$ ya cubre el caso $A=B=1$, se puede cambiar $A+B$ por $A\oplus B$: $C_{out}=AB+C_{in}(A\oplus B)$. También es válida $AB+C_{in}(A+B)$.
@end
@res
$S=A\oplus B\oplus C_{in}$; $C_{out}=AB+C_{in}(A\oplus B)$. Comprobadas las 8 combinaciones.
@end
@end

@ej d6|D6 · NAND y NOR son puertas universales|Demostración D6|demostración|d.nand_not,d.nand_and,d.nand_or,d.nor_universal
@enun
Demuestra que con solo NAND se puede construir NOT, AND y OR (y por tanto cualquier función). Haz lo mismo con NOR.
@end
@antes
**Qué piden:** construir las tres puertas básicas a partir de una sola.
**Teoría:** De Morgan (D1).
@end
@paso NOT
$\text{NAND}(A,A)=\overline{A\cdot A}=\overline{A}$. Se unen las dos entradas.
@end
@paso AND
$\text{NAND}(A,B)=\overline{AB}$. Se niega con una NAND con las entradas unidas: $\overline{\overline{AB}}=AB$.
@end
@paso OR
Por De Morgan, $A+B=\overline{\overline{A}\cdot\overline{B}}=\text{NAND}(\overline{A},\overline{B})$: se niegan $A$ y $B$ con NAND y luego otra NAND.
@end
@paso NOR
Por dualidad: $\text{NOR}(A,A)=\overline{A}$; $A+B=\overline{\text{NOR}(A,B)}$; $AB=\text{NOR}(\overline{A},\overline{B})$.
@end
@res
Con NAND (o con NOR) se obtiene NOT, AND y OR, y con ellas cualquier función. Comprobado con todas las combinaciones.
@end
@end

@ej d7|D7 · Ecuación característica del JK y tabla de excitación|Demostración D7|demostración|d.jk,d.excitacion_jk,d.excitacion_fn
@enun
Demuestra que el JK cumple $Q^+=J\overline{Q}+\overline{K}Q$ y deduce la tabla de excitación.
@end
@antes
**Qué piden:** pasar del comportamiento del JK a una ecuación y de ahí al diseño.
**Teoría:** [[t06|T6]].
@end
@paso La ecuación
El JK **pone a 1** ($J$) cuando $Q=0$ y **mantiene** el 1 si $K=0$ cuando $Q=1$:
- $Q=0$: sube solo si $J=1$. Término $J\overline{Q}$.
- $Q=1$: se queda en 1 solo si $K=0$. Término $\overline{K}Q$.
Sumando: $Q^+=J\overline{Q}+\overline{K}Q$.
@end
@paso Tabla de excitación
Se despejan $J,K$ para cada transición $Q\to Q^+$:
| $Q$ | $Q^+$ | $J$ | $K$ |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | X |
| 1 | 0 | X | 1 |
| 1 | 1 | X | 0 |
Si $Q=0$ la $K$ no influye; si $Q=1$ la $J$ no influye. Esas X son los indiferentes que simplifican las ecuaciones.
@end
@res
$Q^+=J\overline{Q}+\overline{K}Q$ y la tabla de arriba. Comprobada con las 8 combinaciones $(Q,J,K)$ y con las 4 transiciones.
@end
@end

@ej d8|D8 · Un contador módulo N divide la frecuencia entre N|Demostración D8|demostración|d.divN,d.bits
@enun
Demuestra que la salida de un contador módulo $N$ (con una señal que vale 1 en un estado) tiene frecuencia $f_{clk}/N$ y que se necesitan $n=\lceil\log_2N\rceil$ biestables.
@end
@antes
**Qué piden:** relacionar cuenta, periodo y número de biestables.
**Teoría:** [[t08|T8]].
@end
@paso Frecuencia
El contador pasa por $N$ estados y vuelve al inicial **una vez cada $N$ flancos**. Si una señal vale 1 en un solo estado, esa señal se repite cada $N$ ciclos de reloj: periodo $N\,T_{clk}$, frecuencia $f_{clk}/N$. Un biestable T con $T=1$ es el caso $N=2$.
@end
@paso Número de biestables
Con $n$ biestables hay $2^n$ combinaciones. Hacen falta $N$ estados distintos: $2^n\ge N$, es decir $n\ge\log_2N$. El mínimo entero es $n=\lceil\log_2N\rceil$. Si $N$ no es potencia de 2 sobran $2^n-N$ estados: hay que decidir adónde van (ver el **bloqueo** en los simulacros).
@end
@res
$f_{out}=f_{clk}/N$ y $n=\lceil\log_2N\rceil$. Comprobado para $N=3,5,6,10$.
@end
@end

@ej d9|D9 · Contador síncrono binario: $T_i=Q_{i-1}\cdots Q_0$|Demostración D9|demostración|d.contsync
@enun
Demuestra que un contador binario síncrono de $n$ bits con biestables T usa $T_i=Q_{i-1}Q_{i-2}\cdots Q_0$ (con $T_0=1$).
@end
@antes
**Qué piden:** justificar cuándo conmuta cada bit al sumar 1.
**Teoría:** [[t08|T8]].
@end
@paso Sumar 1 en binario
Al sumar 1 el bit 0 siempre cambia. El bit $i$ cambia solo si **todos los inferiores valían 1** (hay acarreo hasta él), como en $0111+1=1000$.
@end
@paso Biestable T
Un T conmuta cuando $T=1$. Así que $T_i=Q_{i-1}\cdots Q_0$, una AND de todos los bits menores. $T_0=1$ (AND vacía).
@end
@res
$T_0=1$, $T_1=Q_0$, $T_2=Q_1Q_0$, $T_3=Q_2Q_1Q_0$, … Comprobado con los 16 valores de un contador de 4 bits.
@end
@end

@ej d10|D10 · Estados de los registros anillo, Johnson y LFSR|Demostración D10|demostración|d.anillo,d.johnson,d.lfsr
@enun
Demuestra: (a) un registro en anillo de $n$ biestables tiene $n$ estados; (b) un contador Johnson tiene $2n$; (c) un LFSR de $n$ bits tiene **como máximo** $2^n-1$.
@end
@antes
**Qué piden:** contar los estados que visita cada registro.
**Teoría:** [[t09|T9]].
@end
@paso (a) Anillo
Un único 1 que circula: hay $n$ posiciones posibles y tras $n$ desplazamientos vuelve al inicio. $n$ estados.
@end
@paso (b) Johnson
La salida se realimenta **negada**. Empezando en $0\dots0$ se van llenando de unos desde un lado ($n$ estados) y luego se van vaciando ($n$ estados más). Total $2n$.
@end
@paso (c) LFSR
La realimentación es una XOR de algunos bits. Con $n$ bits hay $2^n$ valores, pero el estado $00\dots0$ **se queda atascado** (la XOR de ceros es 0). Los demás $2^n-1$ valores son el máximo posible. Se alcanza solo con ciertas posiciones de realimentación (polinomios primitivos).
@end
@res
Anillo $n$, Johnson $2n$, LFSR $\le2^n-1$. Comprobados por simulación para $n=1\dots8$ (anillo y Johnson) y con $n=3$ a $7$ (LFSR, ciclo máximo de $2^n-1$).
@end
@end

@ej d11|D11 · Cuántas funciones hay de n variables y por qué un MUX universal|Demostración D11|demostración|d.nfun.3,d.mux
@enun
Demuestra que hay $2^{2^n}$ funciones de $n$ variables y que un multiplexor $2^k{:}1$ puede implementar cualquier función de $k+1$ variables.
@end
@antes
**Qué piden:** dos conteos con el mismo truco: tabla de verdad.
**Teoría:** [[t03|T3]], [[t05|T5]].
@end
@paso Número de funciones
La tabla de verdad tiene $2^n$ filas y en cada una la salida es 0 o 1, de forma independiente. Total $2\cdot2\cdots2=2^{2^n}$. Con $n=2$: $2^4=16$; con $n=4$: $2^{16}=65\,536$.
@end
@paso MUX 4:1 y tres variables
Se eligen $A,B$ como selección. Para cada valor de $(A,B)$ la función es una función de **solo $C$**, y solo hay cuatro: $0$, $1$, $C$ y $\overline{C}$. Basta cablear una de ellas a cada entrada de datos.
@end
@paso Generalización
Un MUX $2^k{:}1$ usa $k$ variables como selección. Para cada valor, la función restante depende de **una** variable más y solo puede ser $0$, $1$, $x$ o $\overline{x}$.
@end
@res
$2^{2^n}$ funciones; MUX $2^k{:}1$ implementa cualquier función de $k+1$ variables (comprobado con las 256 funciones de 3 variables).
@end
@end

@ej d12|D12 · Número de chips de memoria|Demostración D12|demostración|d.chips
@enun
Una memoria de $16\text{K}\times16$ se construye con chips de $4\text{K}\times8$. ¿Cuántos chips hacen falta y cómo se conectan?
@end
@antes
**Qué piden:** ampliar palabras y ampliar profundidad.
**Teoría:** [[t07|T7]].
@end
@paso Anchura
Se necesitan 16 bits de ancho con chips de 8: $16/8=2$ chips **en paralelo** (comparten dirección, aportan 8 bits cada uno).
@end
@paso Profundidad
$16\text{K}/4\text{K}=4$ bloques. Se unen los 12 bits bajos de dirección a todos los chips y los 2 bits altos entran en un **decodificador 2:4** que activa la selección de un bloque.
@end
@paso Total
$4\cdot2=8$ chips. Equivale a $\dfrac{2^{14}\cdot16}{2^{12}\cdot8}=8$.
@end
@res
8 chips: 4 bloques de profundidad con 2 chips en paralelo cada uno. Dirección: 14 bits (12 a los chips + 2 al decodificador).
@end
@end
