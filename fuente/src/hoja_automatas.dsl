%% id=h-automatas
%% group=hojadata
%% n=2
%% title=Hoja de problemas · Autómatas síncronos con biestables JK
%% sub=8 problemas: tres o más unos o ceros, detectores de secuencia con solapamiento, sumador serie y contador reversible.
%% anio=Hojas
%% tipo=Hoja

@ej a1|A1 · Tres o más unos seguidos|Hoja autómatas · A1|sec,cont|a1.puertas,a1.exhaustivo
@enun
Diseña un autómata síncrono (Mealy, biestables JK) con una entrada serie $E$ y una salida $S$ que valga 1 mientras se hayan recibido **tres o más unos consecutivos** (desde el tercer uno y mientras sigan llegando unos). Un cero reinicia la cuenta.
@end
@antes
**Qué piden:** diagrama de estados, codificación, tablas de excitación y ecuaciones J-K y de salida.
**Teoría:** diseño de autómatas síncronos ([[t10|T10]]), excitación del JK ([[t06|T6]]).
@end
@paso Estados
$S_0$: ningún uno seguido. $S_1$: un uno. $S_2$: dos o más unos. Tres estados necesitan dos biestables: $S_0=00$, $S_1=01$, $S_2=10$ ($Q_1Q_0$); el $11$ es indiferente.
@end
@paso Transiciones (entrada $E$ / salida $S$)
| Estado | $E=0$ | $E=1$ |
|---|---|---|
| $S_0$ | $S_0/0$ | $S_1/0$ |
| $S_1$ | $S_0/0$ | $S_2/0$ |
| $S_2$ | $S_0/0$ | $S_2/1$ |
En $S_2$ con $E=1$ ya van tres o más unos: salida 1 y se queda.
@end
@paso Excitación y ecuaciones
Con la tabla de excitación del JK y Karnaugh con el estado 11 como indiferente:
$$J_1={{a1.J1}}\qquad K_1={{a1.K1}}$$
$$J_0={{a1.J0}}\qquad K_0={{a1.K0}}$$
$$S={{a1.S0}}$$
@end
@paso Comprobación
Simulado a nivel de puerta contra la definición («lleva tres o más unos seguidos») para **todas** las secuencias de hasta 12 bits.
@end
@res
$J_1={{a1.J1}}$, $K_1={{a1.K1}}$, $J_0={{a1.J0}}$, $K_0={{a1.K0}}$, $S={{a1.S0}}$ (Mealy).
@end
@end

@ej a2|A2 · Tres o más ceros seguidos|Hoja autómatas · A2|sec,cont|a2.puertas,a2.exhaustivo
@enun
El mismo problema que A1, pero con **tres o más ceros consecutivos**. Un uno reinicia la cuenta.
@end
@antes
**Qué piden:** el mismo diseño con la entrada negada.
**Teoría:** [[t10|T10]], [[t06|T6]].
@end
@paso Cambio respecto de A1
Es A1 con $E$ y $\overline{E}$ intercambiados: los mismos tres estados cuentan ceros en vez de unos.
@end
@paso Ecuaciones
$$J_1={{a2.J1}}\qquad K_1={{a2.K1}}$$
$$J_0={{a2.J0}}\qquad K_0={{a2.K0}}$$
$$S={{a2.S0}}$$
@end
@res
$J_1={{a2.J1}}$, $K_1={{a2.K1}}$, $J_0={{a2.J0}}$, $K_0={{a2.K0}}$, $S={{a2.S0}}$. Verificado con todas las secuencias de hasta 12 bits.
@end
@end

@ej a3|A3 · Detector de la secuencia 1011 (con solapamiento)|Hoja autómatas · A3|sec,cont|a3.puertas,a3.exhaustivo
@enun
Diseña un detector de la secuencia **1011** para una entrada serie $E$. La salida $S$ vale 1 en el ciclo en que llega el último bit de la secuencia. Las secuencias pueden **solaparse** (en 1011011 se detectan dos).
@end
@antes
**Qué piden:** autómata de Mealy con 4 estados y 2 biestables JK.
**Teoría:** detectores de secuencia ([[t10|T10]]).
@end
@paso Estados
Cada estado recuerda **el mayor prefijo de 1011** que es sufijo de lo recibido. $S_0$: ninguno. $S_1$: «1». $S_2$: «10». $S_3$: «101». Codificación $S_0=00,\ S_1=01,\ S_2=10,\ S_3=11$.
@end
@paso Diagrama
@fig fsm {"nodes":{"S0":[60,110,"ε"],"S1":[210,110,"1"],"S2":[360,110,"10"],"S3":[510,110,"101"]},"edges":[["S0","S0","0/0",0],["S0","S1","1/0",0],["S1","S1","1/0",0],["S1","S2","0/0",0],["S2","S3","1/0",0],["S2","S0","0/0",-70],["S3","S1","1/1",-70],["S3","S2","0/0",80]],"W":580,"H":240,"title":"Detector de 1011 con solapamiento. Etiquetas: E / S","cap":"Desde $S_3$ con un 1 se detecta la secuencia y el último 1 pasa a ser el primero de la siguiente ($S_1$). Con un 0 se queda «10» ($S_2$)."}
@end
@paso Ecuaciones
$$J_1={{a3.J1}}\qquad K_1={{a3.K1}}$$
$$J_0={{a3.J0}}\qquad K_0={{a3.K0}}$$
$$S={{a3.S0}}$$
@end
@box ojo | El solapamiento
Sin solapamiento, $S_3$ con $E=1$ volvería a $S_0$. Con solapamiento vuelve a $S_1$. Es el error más común en este tipo de problemas: **mira siempre qué parte del final de la secuencia vale como principio de la siguiente**.
@end
@res
$J_1={{a3.J1}}$, $K_1={{a3.K1}}$, $J_0={{a3.J0}}$, $K_0={{a3.K0}}$, $S={{a3.S0}}$ (Mealy). Verificado con todas las secuencias de hasta 12 bits.
@end
@end

@ej a5a|A5a · Detector de cuatro unos (1111)|Hoja autómatas · A5a|sec,cont|a5a.puertas,a5a.exhaustivo
@enun
Diseña un detector de la secuencia **1111** con solapamiento (la salida vale 1 cada vez que los cuatro últimos bits recibidos son unos).
@end
@antes
**Qué piden:** Mealy con 4 estados.
**Teoría:** [[t10|T10]].
@end
@paso Estados
Los estados cuentan los unos seguidos: $S_0$ (0), $S_1$ (1), $S_2$ (2), $S_3$ (3 o más). Con $E=1$ en $S_3$ se activa la salida y se **permanece** en $S_3$ (solapamiento). Con $E=0$ siempre se vuelve a $S_0$.
@end
@paso Ecuaciones
$$J_1={{a5a.J1}}\qquad K_1={{a5a.K1}}$$
$$J_0={{a5a.J0}}\qquad K_0={{a5a.K0}}$$
$$S={{a5a.S0}}$$
@end
@res
$J_1={{a5a.J1}}$, $K_1={{a5a.K1}}$, $J_0={{a5a.J0}}$, $K_0={{a5a.K0}}$, $S={{a5a.S0}}$. Verificado con todas las secuencias de hasta 12 bits.
@end
@end

@ej a5b|A5b · Detector de la secuencia 11011|Hoja autómatas · A5b|sec,cont|a5b.puertas,a5b.exhaustivo
@enun
Diseña un detector de la secuencia **11011** con solapamiento.
@end
@antes
**Qué piden:** Mealy con 5 estados, es decir 3 biestables.
**Teoría:** [[t10|T10]].
@end
@paso Estados
Prefijos de 11011: $S_0$ (ninguno), $S_1$ («1»), $S_2$ («11»), $S_3$ («110»), $S_4$ («1101»). Cinco estados necesitan 3 biestables ($000$ a $100$); los otros tres códigos son indiferentes.
@end
@paso Transiciones
| Estado | $E=0$ | $E=1$ |
|---|---|---|
| $S_0$ | $S_0/0$ | $S_1/0$ |
| $S_1$ | $S_0/0$ | $S_2/0$ |
| $S_2$ | $S_3/0$ | $S_2/0$ |
| $S_3$ | $S_0/0$ | $S_4/0$ |
| $S_4$ | $S_0/0$ | $S_2/1$ |
En $S_2$ con $E=1$ (tres unos seguidos) se sigue en «11»: se queda en $S_2$. En $S_4$ con $E=1$ se detecta la secuencia y los dos últimos unos valen como «11»: se pasa a $S_2$.
@end
@paso Ecuaciones
$$J_2={{a5b.J2}}\qquad K_2={{a5b.K2}}$$
$$J_1={{a5b.J1}}\qquad K_1={{a5b.K1}}$$
$$J_0={{a5b.J0}}\qquad K_0={{a5b.K0}}$$
$$S={{a5b.S0}}$$
@end
@res
Las siete ecuaciones anteriores. Verificado con todas las secuencias de hasta 12 bits.
@end
@end

@ej a7|A7 · Detector de 1010 o de 110|Hoja autómatas · A7|sec,cont|a7.puertas,a7.exhaustivo
@enun
Diseña un autómata con una entrada serie $E$ cuya salida vale 1 cuando los últimos bits recibidos son **1010 o 110** (con solapamiento).
@end
@antes
**Qué piden:** un autómata que detecta **dos** secuencias a la vez.
**Teoría:** [[t10|T10]].
@end
@paso Estados
Cada estado es el mayor sufijo de lo recibido que es prefijo de alguna de las dos secuencias. Los prefijos útiles son: ε, «1», «10», «101», «11». Son 5 estados ($S_\varepsilon,S_1,S_{10},S_{11},S_{101}$), 3 biestables. Codificación: $S_\varepsilon=000$, $S_1=001$, $S_{10}=010$, $S_{11}=011$, $S_{101}=100$.
@end
@paso Transiciones
| Estado | $E=0$ | $E=1$ |
|---|---|---|
| $S_\varepsilon$ | $S_\varepsilon/0$ | $S_1/0$ |
| $S_1$ | $S_{10}/0$ | $S_{11}/0$ |
| $S_{10}$ | $S_\varepsilon/0$ | $S_{101}/0$ |
| $S_{11}$ | $S_{10}/1$ | $S_{11}/0$ |
| $S_{101}$ | $S_{10}/1$ | $S_{11}/0$ |
Con 110 el último 0 deja «10» (vale como inicio de 1010). Con 1010 también queda «10».
@end
@paso Ecuaciones
$$J_2={{a7.J2}}\qquad K_2={{a7.K2}}$$
$$J_1={{a7.J1}}\qquad K_1={{a7.K1}}$$
$$J_0={{a7.J0}}\qquad K_0={{a7.K0}}$$
$$S={{a7.S0}}$$
@end
@res
Las siete ecuaciones anteriores. Verificado con todas las secuencias de hasta 12 bits.
@end
@end

@ej a9|A9 · Sumador serie|Hoja autómatas · A9|sec,cont,arit|a9.puertas,a9.suma
@enun
Diseña un **sumador serie**: dos números llegan bit a bit, empezando por el menos significativo, por las entradas $E_1$ y $E_0$. En cada ciclo la salida $S$ da el bit correspondiente de la suma. Un biestable JK guarda el acarreo.
@end
@antes
**Qué piden:** autómata de Mealy de dos estados (acarreo 0 o 1).
**Teoría:** sumador completo ([[t05|T5]]), autómatas ([[t10|T10]]).
@end
@paso Estados
Dos estados: $A$ (acarreo 0, $Q_0=0$) y $B$ (acarreo 1, $Q_0=1$). Un solo biestable.
@end
@paso Transiciones
Con $t=E_1+E_0+\text{acarreo}$: salida $=t\bmod2$ y nuevo acarreo $=\lfloor t/2\rfloor$.
@fig fsm {"nodes":{"A":[110,100,"acarreo 0"],"B":[390,100,"acarreo 1"]},"edges":[["A","A","00/0, 01/1, 10/1",0],["A","B","11/0",0],["B","A","00/1",-70],["B","B","01/0, 10/0, 11/1",0]],"W":500,"H":220,"title":"Sumador serie. Etiquetas: $E_1E_0$ / S","cap":"El estado recuerda el acarreo; la salida es el bit de suma."}
@end
@paso Ecuaciones
$$J_0={{a9.J0}}\qquad K_0={{a9.K0}}$$
$$S={{a9.S0}}$$
El acarreo se activa solo si las dos entradas valen 1 ($J_0=E_1E_0$) y se desactiva solo si las dos valen 0 ($K_0=\overline{E_1}\,\overline{E_0}$). En el resto de casos se mantiene. La salida es la **XOR de tres bits**: $S=Q_0\oplus E_1\oplus E_0$.
@end
@res
$J_0={{a9.J0}}$, $K_0={{a9.K0}}$, $S=Q_0\oplus E_1\oplus E_0$. Probado con 400 sumas aleatorias de hasta 10 bits.
@end
@end

@ej a11|A11 · Contador reversible módulo 4|Hoja autómatas · A11|sec,cont|a11.puertas,a11.traza
@enun
Diseña un contador módulo 4 **reversible** (autómata de Moore). La entrada $E$ elige el sentido: $E=1$ cuenta hacia arriba ($0,1,2,3,0\dots$) y $E=0$ hacia abajo ($0,3,2,1,0\dots$). La salida es el valor de la cuenta en binario de dos bits.
@end
@antes
**Qué piden:** un contador de dos biestables JK con entrada de sentido.
**Teoría:** contadores ([[t08|T8]]), autómatas de Moore ([[t10|T10]]).
@end
@paso Estados y salida
Cuatro estados $S_0,\dots,S_3$ con codificación igual al valor ($00,01,10,11$). Como es Moore, **la salida depende solo del estado**: $S_1S_0=Q_1Q_0$.
@end
@paso Ecuaciones
Para contar: $Q_0$ cambia siempre; $Q_1$ cambia cuando $Q_0=1$ si sube y cuando $Q_0=0$ si baja.
$$J_0=K_0={{a11.J0}}\qquad J_1=K_1={{a11.J1}}$$
$J_1=K_1=\overline{Q_0\oplus E}$: se activa cuando $Q_0=E$ (con $E=1$ sube y $Q_0=1$ acarrea; con $E=0$ baja y $Q_0=0$ pide préstamo).
@end
@paso Comprobación
Con $E=1,1,1,1,1,0,0,0,0$ desde el estado 0 las salidas, tras cada flanco de reloj, son {{a11.traza}}.
@end
@res
$J_0=K_0={{a11.J0}}$; $J_1=K_1={{a11.J1}}$; salidas $S_1=Q_1$, $S_0=Q_0$ (Moore).
@end
@end
