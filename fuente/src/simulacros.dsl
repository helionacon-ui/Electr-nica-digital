%% id=simulacros
%% group=ejer
%% n=3
%% title=Simulacros de examen
%% short=Simulacros
%% sub=Dos exámenes de cuatro problemas con las soluciones ocultas. Cronométrate 2 horas.

## Cómo usarlos

1. Prepara papel, calculadora y el formulario de una página ([[formulario]]). Nada más.
2. Pon un cronómetro de **2 horas** por simulacro. Son cuatro problemas de 2,5 puntos, como en los exámenes reales ([[examen]]).
3. Resuelve **sin abrir** las soluciones. Los desplegables están cerrados a propósito.
4. Corrige con la regla de los exámenes: se valoran la **simplicidad** y la **claridad**. Un cronograma sin explicación no cuenta.
5. Anota qué tipo de problema has fallado y vuelve a su tema en la guía ([[plan]]).

@box idea | Todo está comprobado
Cada solución se ha simulado a nivel de puerta con todas las combinaciones posibles (o con todas las secuencias de entrada de hasta 8 a 12 bits, en los autómatas). Los problemas son originales de esta guía, pero del mismo tipo que los de examen.
@end

## Simulacro 1

### Problema 1 · Código Gray a binario (2,5 puntos)

Un sensor de posición angular entrega su lectura en **código Gray de 3 bits** $G_2G_1G_0$. Diseña el circuito combinacional que la convierte a binario natural $B_2B_1B_0$: tabla de verdad, ecuaciones simplificadas y esquema con puertas.

@details Ver la solución del problema 1
**Teoría:** código Gray (solo cambia un bit entre valores consecutivos) y Karnaugh o XOR ([[t02|T2]], [[t03|T3]]).

La secuencia Gray de 0 a 7 es {{s1p1.seqbin}}. Se invierte la tabla: para cada valor Gray se busca el binario.

| $G_2G_1G_0$ | 000 | 001 | 011 | 010 | 110 | 111 | 101 | 100 |
|---|---|---|---|---|---|---|---|---|
| $B_2B_1B_0$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |

Ecuaciones simplificadas por Karnaugh:
$$B_2={{s1p1.B2}}\qquad B_1={{s1p1.B1}}$$
$$B_0={{s1p1.B0}}$$
$B_1$ es una XOR y $B_0$ es la XOR de tres entradas. Con puertas XOR queda:
$$B_2=G_2\qquad B_1=G_2\oplus G_1\qquad B_0=G_2\oplus G_1\oplus G_0=B_1\oplus G_0$$
Son **dos XOR en cascada**: la forma más simple. Cada bit binario es la XOR de todos los bits Gray de igual o mayor peso.
@end

### Problema 2 · Sumador BCD de un dígito (2,5 puntos)

Diseña con bloques estándar un sumador de dos dígitos BCD ($A$ y $B$, cada uno de 0 a 9) con acarreo de entrada. La salida debe ser un dígito BCD y un acarreo de salida. Explica cómo se detecta que hace falta corregir y por qué se suma 6.

@details Ver la solución del problema 2
**Teoría:** BCD y aritmética en BCD ([[t02|T2]]), sumador de 4 bits ([[t05|T5]]).

1. Un sumador de 4 bits suma $A+B+C_{in}$ en binario. El máximo es $9+9+1={{s1p2.max}}$, que cabe en 5 bits (acarreo $K$ y suma $S_3S_2S_1S_0$).
2. Si la suma vale $\le9$ ya es un dígito BCD. Si vale de 10 a 19, el resultado BCD correcto es **«1» y el dígito $S-10$**. Pero el binario ha contado 16 por cada acarreo, no 10. Se **suma 6** (la diferencia entre 16 y 10) y se descartan los 16.
3. Hace falta corregir cuando la suma es mayor que 9: $K=1$ (suma $\ge16$) o $S_3S_2=1$ o $S_3S_1=1$ (suma de 10 a 15):
$$\text{Corregir}=K+S_3S_2+S_3S_1$$
4. Un segundo sumador de 4 bits suma $0\,(\text{Corregir})(\text{Corregir})0$, es decir $0110$ o $0000$, a $S_3S_2S_1S_0$. Su resultado es el dígito BCD. El acarreo de salida es «Corregir».

Ejemplos: $7+8=15=01111_2$; hay que corregir; $1111+0110=10101$: dígito $0101$ y acarreo $1$, es decir **15**. $9+9+1=19=10011_2$: el binario da $K=1$ y $0011$; $0011+0110=1001$ con acarreo 1: **19**. $4+3=0111$: no se corrige.

Se ha comprobado con las 200 combinaciones de $(A,B,C_{in})$.
@end

### Problema 3 · Contador síncrono 0, 2, 5, 7 (2,5 puntos)

Diseña con biestables JK un contador síncrono de 3 bits que repita la secuencia **0, 2, 5, 7, 0, 2, 5, 7…** (en decimal). Los estados 1, 3, 4 y 6 no se usan. Da las ecuaciones $J$ y $K$ de cada biestable y una señal $F$ que valga 1 en el estado 7. Comenta qué pasa si el circuito arranca en un estado no usado.

@details Ver la solución del problema 3
**Teoría:** diseño de contadores con JK ([[t08|T8]], [[t06|T6]]).

Tabla de transición (los estados no usados son indiferentes):

| Estado actual $Q_2Q_1Q_0$ | Siguiente |
|---|---|
| 000 | 010 |
| 010 | 101 |
| 101 | 111 |
| 111 | 000 |

Con la tabla de excitación del JK y Karnaugh con indiferentes:
$$J_2=K_2={{s1p3.J2}}\qquad J_1=K_1={{s1p3.J1}}\qquad J_0=K_0={{s1p3.J0}}$$
$$F={{s1p3.S0}}$$
Todos los biestables trabajan en modo **toggle** ($J=K$): $Q_1$ conmuta siempre, $Q_2$ y $Q_0$ conmutan cuando $Q_1=1$. Se ha simulado a nivel de puerta y repite $0,2,5,7,0,\dots$

@box ojo | El circuito no se recupera solo
Los estados no usados forman un **ciclo cerrado**: $1\to3\to4\to6\to1$. Si al encender el circuito los biestables arrancan en uno de ellos, el contador **nunca entra** en la secuencia buena. Solución: poner un **reset** asíncrono (clear) que lleve a 000 al arrancar, o elegir las indiferentes para que los estados no usados desemboquen en la secuencia (autoarranque).
@end
@end

### Problema 4 · Detector de la secuencia 0110 (2,5 puntos)

Diseña con biestables JK un autómata (Mealy) con una entrada serie $E$ y una salida $S$ que valga 1 cuando los últimos cuatro bits recibidos sean **0110**. Puede haber solapamiento. Da el diagrama de estados, la tabla de transición y las ecuaciones.

@details Ver la solución del problema 4
**Teoría:** autómatas síncronos ([[t10|T10]]).

**Estados:** el mayor prefijo de 0110 que es sufijo de lo recibido. $S_0$: ninguno. $S_1$: «0». $S_2$: «01». $S_3$: «011». Codificación $00,01,10,11$.

| Estado | $E=0$ | $E=1$ |
|---|---|---|
| $S_0$ | $S_1/0$ | $S_0/0$ |
| $S_1$ | $S_1/0$ | $S_2/0$ |
| $S_2$ | $S_1/0$ | $S_3/0$ |
| $S_3$ | $S_1/1$ | $S_0/0$ |

Con un 0 siempre se pasa a «0» ($S_1$), salvo en $S_3$ donde ese 0 completa 0110 (salida 1) y vale como inicio de la siguiente ($S_1$).
$$J_1={{s1p4.J1}}\qquad K_1={{s1p4.K1}}$$
$$J_0={{s1p4.J0}}\qquad K_0={{s1p4.K0}}$$
$$S={{s1p4.S0}}$$
Verificado con todas las secuencias de hasta 12 bits.
@end

## Simulacro 2

### Problema 1 · Codificador de prioridad (2,5 puntos)

Diseña un codificador de prioridad de cuatro entradas $I_3I_2I_1I_0$ ($I_3$ es la más prioritaria). Salidas: $A_1A_0$ (número de la entrada activa más prioritaria) y $V$, que indica si hay alguna entrada activa. Da las ecuaciones simplificadas.

@details Ver la solución del problema 1
**Teoría:** codificadores de prioridad ([[t05|T5]]), Karnaugh ([[t03|T3]]).

| Entradas activas | $A_1A_0$ | $V$ |
|---|---|---|
| ninguna | 00 | 0 |
| solo $I_0$ | 00 | 1 |
| $I_1$ (y quizá $I_0$) | 01 | 1 |
| $I_2$ (y quizá menores) | 10 | 1 |
| $I_3$ (y cualquier otra) | 11 | 1 |

Con Karnaugh sobre las 16 combinaciones:
$$A_1={{s2p1.A1}}\qquad A_0={{s2p1.A0}}\qquad V={{s2p1.V}}$$
$V$ es una OR de las cuatro entradas. Fíjate en que $A_0$ **no** es «$I_3+I_1$»: si $I_2=1$ y $I_1=1$, gana $I_2$ y $A_0$ debe ser 0. Por eso aparece $\overline{I_2}I_1$.
@end

### Problema 2 · Multiplicar por 5 (2,5 puntos)

Un número $X$ de 4 bits sin signo debe multiplicarse por 5. Diseña el circuito con un solo sumador y sin multiplicador. ¿Cuántos bits tiene el resultado?

@details Ver la solución del problema 2
**Teoría:** numeración y desplazamientos ([[t02|T2]]), sumadores ([[t05|T5]]).

$5X=4X+X$. Multiplicar por 4 es **desplazar dos posiciones a la izquierda** (cableado, sin puertas): $X\ll2$ es $X_3X_2X_1X_0\,00$ (6 bits). Un sumador de 7 bits suma $X\ll2$ y $X$ (ampliados con ceros).

El máximo es $5\cdot15={{s2p2.max}}$. Como $2^6=64<75<128=2^7$, hacen falta **{{s2p2.bits}} bits**. Se ha comprobado con los 16 valores de $X$.
@end

### Problema 3 · Temporización con un reloj de 50 MHz (2,5 puntos)

Una placa tiene un reloj de 50 MHz. (a) Obtén una señal de 1 Hz con ciclo de trabajo del 50 %: ¿hasta qué valor cuenta el contador y cuántos bits tiene? (b) Un display de 4 dígitos multiplexado se refresca con un contador de 17 bits cuyos dos bits altos eligen el dígito. ¿Cuál es la frecuencia de barrido y la de refresco de cada dígito? ¿Se verá parpadear? (c) ¿Cuántos bits necesita un contador que mide 10 ms (antirrebote) con ese reloj?

@details Ver la solución del problema 3
**Teoría:** divisores de frecuencia, multiplexado de displays y antirrebote ([[t08|T8]], [[t12|T12]]).

**(a)** Una señal de 1 Hz con ciclo del 50 % cambia cada **medio segundo**: $25\,000\,000$ ciclos de reloj. El contador cuenta de 0 a {{s2p3.cuenta}} y entonces invierte un biestable de salida. Como $2^{24}<25\,000\,000\le2^{25}$, necesita **{{s2p3.bits1hz}} bits**.

**(b)** El contador de 17 bits desborda cada $2^{17}$ ciclos: $50\,000\,000/2^{17}\approx{{s2p3.fbarrido}}$ Hz. Los dos bits altos recorren cuatro dígitos, así que cada dígito se enciende $\approx{{s2p3.fdigito}}$ Hz. Es más que 60 Hz: **no se ve parpadear**.

**(c)** 10 ms $=0{,}01\cdot50\,000\,000=500\,000$ ciclos. Como $2^{18}=262\,144<500\,000\le524\,288=2^{19}$, hacen falta **19 bits**.
@end

### Problema 4 · Máquina de 30 céntimos con cambio (2,5 puntos)

Una máquina vende un producto de 30 céntimos y acepta monedas de 10 y de 20 céntimos, una por ciclo. Las entradas son $M_{20}M_{10}$: 00 (nada), 01 (moneda de 10), 10 (moneda de 20); 11 no se da. Cuando el total llega a 30 o más, la salida $Z$ entrega el producto y se vuelve a empezar. Si el total es 40, la salida $C$ devuelve 10 céntimos de cambio. Diseña el autómata de Mealy con JK.

@details Ver la solución del problema 4
**Teoría:** autómatas de Mealy ([[t10|T10]]).

Estados: $S_0$ (0 céntimos), $S_1$ (10), $S_2$ (20). Codificación $00,01,10$; el $11$ es indiferente, y la entrada 11 también.

| Estado | $M_{20}M_{10}=00$ | 01 (10 cts) | 10 (20 cts) |
|---|---|---|---|
| $S_0$ | $S_0/ZC=00$ | $S_1/00$ | $S_2/00$ |
| $S_1$ | $S_1/00$ | $S_2/00$ | $S_0/Z=1$ (30) |
| $S_2$ | $S_2/00$ | $S_0/Z=1$ (30) | $S_0/Z=1,C=1$ (40) |

$$J_1={{s2p4.J1}}\qquad K_1={{s2p4.K1}}$$
$$J_0={{s2p4.J0}}\qquad K_0={{s2p4.K0}}$$
$$Z={{s2p4.S0}}\qquad C={{s2p4.S1}}$$
Verificado con todas las secuencias de monedas de hasta 8 ciclos.
@end
