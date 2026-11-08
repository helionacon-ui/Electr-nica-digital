%% id=t06
%% group=tema
%% n=6
%% title=Tema 6 · Biestables (flip-flops) y dispositivos relacionados
%% short=T6 · Biestables
%% sub=La memoria de 1 bit: latch, flip-flop SR, JK, D y T, tablas características y de excitación.

@box idea | Desde cero
Un **biestable** es un circuito con dos estados estables que **recuerda un bit**. Un **flip-flop** cambia de estado solo cuando llega un **flanco** del reloj (el instante en que la señal de reloj pasa de 0 a 1, o de 1 a 0). Entre flanco y flanco no escucha a las entradas. Esa disciplina es lo que permite que un circuito con miles de biestables funcione ordenado: todos cambian a la vez, en el mismo instante.
@end

## Latch frente a flip-flop

- **Latch** (cerrojo): es **transparente** mientras el reloj (o *enable*) está activo: la salida sigue a la entrada todo ese tiempo.
- **Flip-flop disparado por flanco:** muestrea las entradas **solo en el flanco** y mantiene la salida el resto del ciclo.

Usa flip-flops para diseñar secuenciales síncronos. Los latches dan problemas de temporización.

## Los cuatro tipos y sus tablas

$Q$ es el estado actual y $Q^+$ el estado después del flanco.

| Tipo | Ecuación característica | Qué hace |
|---|---|---|
| **SR** | $Q^+=S+\overline{R}\,Q$ (con $SR=0$) | $S=1$ pone a 1; $R=1$ pone a 0; $S=R=0$ mantiene; $S=R=1$ **prohibido** |
| **JK** | $Q^+=J\overline{Q}+\overline{K}\,Q$ | Como SR, pero $J=K=1$ **conmuta** |
| **D** | $Q^+=D$ | Copia $D$ en cada flanco |
| **T** | $Q^+=T\oplus Q$ | $T=1$ conmuta; $T=0$ mantiene |

@fig ffsym {"kind":"JK","cap":"Símbolo del flip-flop JK. El triángulo en la entrada de reloj indica que se dispara por flanco."}

Se ha comprobado por código que la tabla del JK, la del D y la del T cumplen estas ecuaciones para todas las combinaciones.

## Tabla de excitación: lo que necesitas para diseñar

La tabla característica dice «con estas entradas, ¿qué pasa?». Al **diseñar** preguntas lo contrario: «quiero pasar de $Q$ a $Q^+$, ¿qué entradas pongo?». Es la **tabla de excitación**:

| $Q\to Q^+$ | $J$ | $K$ | $D$ | $T$ |
|---|---|---|---|---|
| $0\to0$ | 0 | X | 0 | 0 |
| $0\to1$ | 1 | X | 1 | 1 |
| $1\to0$ | X | 1 | 0 | 1 |
| $1\to1$ | X | 0 | 1 | 0 |

El JK tiene muchos **indiferentes (X)**: eso suele dar ecuaciones más simples que con D, a costa de dos entradas por biestable.

@box idea | Por qué hay una X en el JK
Para pasar de $0$ a $1$ puedes poner $J=1$ y $K=0$ (poner a 1) **o** $J=1$ y $K=1$ (conmutar). El valor de $K$ da igual. Pasa lo mismo en los otros tres casos.
@end

@sim ff

## Biestables como divisores de frecuencia

Un JK con $J=K=1$ (o un T con $T=1$, o un D con $D=\overline{Q}$) **conmuta en cada flanco**: la salida cambia cada ciclo, así que su frecuencia es la **mitad** de la del reloj. Encadenar $n$ así da una división por $2^n$. Es la base de los contadores.

@fig timing {"signals":[["CLK",null],["Q",[0,1,1,0,0,1,1,0]]],"title":"Salida de un biestable T con T=1: periodo doble","slots":8,"cap":"Q cambia solo en los flancos de subida del reloj y completa un ciclo cada dos del reloj."}

## Temporización

- **Tiempo de preparación** (*setup*, $t_{su}$): la entrada debe estar estable **antes** del flanco.
- **Tiempo de mantenimiento** (*hold*, $t_h$): debe seguir estable **después** del flanco.
- **Retardo de salida** ($t_{cq}$): tarda un poco en reflejarse la salida tras el flanco.

Si no se respetan, el biestable cae en un estado **metaestable** (ni 0 ni 1, durante un tiempo impredecible). Por eso las entradas asíncronas (un pulsador) se sincronizan con dos biestables en serie.

**Frecuencia máxima:** el periodo debe cubrir el viaje completo entre dos flancos:

$$T_{clk}\;\ge\; t_{cq}+t_{pd,\,comb}+t_{su}$$

@box falla | Qué suele fallar
- Usar la tabla característica para diseñar (hay que usar la de excitación).
- Escribir 0 en una X: las X son libertad, no valores.
- Confundir latch (transparente) con flip-flop (flanco).
- Olvidar que $S=R=1$ está prohibido en un SR.
- No distinguir **flanco de subida** de **bajada** al dibujar un cronograma.
@end

@box formula | Fórmulas clave
- $Q^+_{JK}=J\overline{Q}+\overline{K}Q$; $Q^+_D=D$; $Q^+_T=T\oplus Q$.
- $T_{clk}\ge t_{cq}+t_{pd}+t_{su}$.
- Divisor por 2: $f_{out}=f_{clk}/2$.
@end

@card ¿Ecuación característica del JK? || $Q^+=J\overline{Q}+\overline{K}Q$.
@card ¿Qué hace un JK con J=K=1? || Conmuta en cada flanco.
@card ¿Entradas del JK para pasar de 1 a 0? || $J=X$ (cualquiera) y $K=1$.
@card ¿Qué es el tiempo de setup? || Tiempo que la entrada debe estar estable antes del flanco de reloj.
@card ¿Qué diferencia hay entre latch y flip-flop? || El latch es transparente mientras está habilitado; el flip-flop muestrea solo en el flanco.
@gloss Flanco | Instante en que la señal de reloj pasa de 0 a 1 (subida) o de 1 a 0 (bajada).
@gloss Biestable | Circuito de dos estados estables que almacena un bit.
@gloss Tabla de excitación | Dice qué entradas del biestable hacen falta para ir de $Q$ a $Q^+$.
@gloss Metaestabilidad | Estado intermedio e impredecible tras violar los tiempos de setup o hold.
@gloss Setup / hold | Tiempos de preparación y mantenimiento de las entradas alrededor del flanco.

@q t6
Un biestable JK tiene $Q=1$ y recibe $J=0$, $K=0$. Tras el flanco:
+ $Q=1$ (mantiene)
- $Q=0$
- $Q=1$ y luego conmuta
- Estado prohibido
> $J=K=0$ mantiene. Con $Q^+=J\overline{Q}+\overline{K}Q=1$.
@end
@q t6
Quieres pasar de $Q=1$ a $Q^+=0$ con un biestable T. ¿Qué pones en $T$?
+ $T=1$
- $T=0$
- $T=X$
- No es posible
> Para cambiar de estado, $T=1$.
@end
@q t6
Un biestable T con $T=1$ recibe un reloj de 8 MHz. La salida tiene frecuencia:
+ 4 MHz
- 8 MHz
- 16 MHz
- 2 MHz
> Conmuta en cada flanco: la frecuencia se divide por 2.
@end
