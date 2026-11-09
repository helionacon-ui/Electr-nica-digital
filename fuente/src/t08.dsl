%% id=t08
%% group=tema
%% n=8
%% title=Tema 8 · Contadores
%% short=T8 · Contadores
%% sub=Contadores asíncronos y síncronos, módulo N, carga y puesta a cero, divisores de frecuencia.

@box idea | Desde cero
Un **contador** es un circuito secuencial cuyo estado **avanza una cuenta** con cada pulso de reloj: 0, 1, 2, 3… y vuelve a empezar. Se usa para medir tiempo, dividir frecuencias, generar direcciones y controlar secuencias. Un contador de **módulo $N$** recorre $N$ estados distintos y necesita $n=\lceil\log_2N\rceil$ biestables.
@end

## Contador binario asíncrono (*ripple*)

Es una cadena de biestables T (o JK con $J=K=1$) donde la salida de cada uno es el **reloj del siguiente**. Solo el primero recibe el reloj externo. Cada etapa divide la frecuencia por 2.

@fig contador {"kind": "async", "n": 3, "cap": "Contador asíncrono de 3 bits: cada biestable se dispara con la salida del anterior."}

- Ventaja: muy simple.
- Inconveniente: los cambios **se propagan en cadena** (de ahí *ripple*). Un contador de 4 bits con $t_{pd}=12$ ns por etapa tarda $4\cdot12=48$ ns en estabilizarse, así que el reloj máximo es unos $1/48\text{ ns}\approx20{,}8$ MHz, y mientras se propaga hay valores intermedios erróneos (*glitches*).

## Contador síncrono

**Todos los biestables comparten el mismo reloj.** El biestable $i$ debe conmutar cuando **todos los bits menores valen 1**:

@fig contador {"kind": "sync", "n": 3, "cap": "Contador síncrono de 3 bits: todos comparten el reloj y cada T es el producto de las salidas de menor peso."}

$$T_i=Q_{i-1}\cdot Q_{i-2}\cdots Q_0$$

Es más rápido (no hay propagación en cadena) y no tiene glitches. Se ha comprobado por código que con $T_0=1$, $T_1=Q_0$, $T_2=Q_1Q_0$ la secuencia de 3 bits es $0,1,2,3,4,5,6,7,0,\dots$

@fig timing {"signals":[["CLK",null],["Q0",[0,1,0,1,0,1,0,1]],["Q1",[0,0,1,1,0,0,1,1]],["Q2",[0,0,0,0,1,1,1,1]]],"title":"Contador binario de 3 bits (cuenta ascendente)","slots":8,"cap":"Q0 divide por 2, Q1 por 4 y Q2 por 8. Cada bit conmuta cuando todos los de menor peso valen 1."}

@sim counter

## Contadores de módulo distinto de $2^n$

Para contar $N$ estados que no sean potencia de 2, hay tres maneras:

1. **Puesta a cero cuando se alcanza $N$:** detecta el estado $N$ con una puerta y activa el *reset* (asíncrono: el estado $N$ dura un instante y es un *glitch*; síncrono: el reset actúa en el siguiente flanco).
2. **Carga paralela:** al llegar al último estado, carga el valor inicial.
3. **Diseño directo como autómata** ([[t10|Tema 10]]): tabla de transiciones y ecuaciones de entrada de los biestables. Es lo que se pide en examen.

Contador módulo 10 (BCD): $0\to1\to\dots\to9\to0$. Módulo 12: $0\to\dots\to11\to0$ y a 1 MHz la salida más lenta sale a $1\ \text{MHz}/12\approx83{,}33$ kHz.

@ej t8-e1|Contador módulo 12 y su frecuencia de salida|Ejemplo T8|cont|t8.bits,t8.fdiv,t8.mod12
@enun
Se quiere un contador síncrono de módulo 12 con reloj de 1 MHz. (a) ¿Cuántos biestables hacen falta? (b) ¿Cuál es el último estado? (c) ¿A qué frecuencia se repite el ciclo completo?
@end
@antes
Teoría: $n=\lceil\log_2N\rceil$ biestables; un contador de módulo $N$ repite su ciclo cada $N$ pulsos; $f_{out}=f_{clk}/N$.
@end
@paso Número de biestables
$2^3=8<12\le2^4=16$ $\Rightarrow$ **4 biestables**.
@end
@paso Último estado
Cuenta $0,1,\dots,11$. El último es $11=1011_2$ y el siguiente es $0000$. Los estados $12$ a $15$ **no se usan**.
@end
@paso Frecuencia del ciclo
$f=\dfrac{1\ \text{MHz}}{12}=83{,}33$ kHz.
@end
@res
(a) 4. (b) $1011_2$ (11). (c) $83{,}33$ kHz.
@end
@end

## Contadores en circuito integrado

Los contadores comerciales (74x161, 74x163…) incorporan: **carga paralela** (*LOAD*), **puesta a cero** (*CLR*), habilitación de cuenta (*ENP, ENT*), sentido ascendente/descendente (*UP/DOWN*) y una salida de **fin de cuenta** (*RCO/carry*) para **cascadear** varios. Lee siempre en la hoja si cada entrada es **síncrona o asíncrona** y si es **activa a nivel bajo**.

@box mas | Más a fondo: contador reversible
Un contador ascendente/descendente con una señal $X$ ($X=1$ sube, $X=0$ baja) tiene $T_i=\overline{X}\cdot\overline{Q_{i-1}}\cdots+X\cdot Q_{i-1}\cdots$. Una versión útil es la de los **contadores en código no binario**, como el de secuencia $0,2,4,6,1,3,5,7$.
@end

@box falla | Qué suele fallar
- Contar mal los biestables: para módulo $N$ son $\lceil\log_2N\rceil$, no $N$.
- Olvidar que el reset **asíncrono** produce un estado intermedio fugaz.
- En un contador asíncrono, calcular la frecuencia máxima con el retardo de **una** etapa en vez de **todas**.
- Cascadear sin usar la salida de fin de cuenta o la habilitación.
- Confundir *carga síncrona* (espera al flanco) con *carga asíncrona* (inmediata).
@end

@box formula | Fórmulas clave
- $n=\lceil\log_2N\rceil$; estados no usados: $2^n-N$.
- $f_{out}=f_{clk}/N$.
- Síncrono binario: $T_i=Q_{i-1}\cdots Q_0$.
- Asíncrono: $t_{total}=n\cdot t_{pd}$.
@end

@card ¿Cuántos biestables necesita un contador de módulo 60? || 6 ($2^5=32<60\le64$).
@card ¿Ecuación de $T_2$ en un contador síncrono binario? || $T_2=Q_1Q_0$.
@card ¿Ventaja del contador síncrono? || No acumula retardos de propagación y no genera glitches.
@card ¿Qué es un glitch? || Un valor erróneo fugaz mientras los biestables de un contador asíncrono cambian en cadena.
@card ¿Frecuencia de salida de un divisor por $N$? || $f_{clk}/N$.
@gloss Contador módulo N | Contador que recorre N estados y vuelve al inicial.
@gloss Contador síncrono | Contador en el que todos los biestables reciben el mismo reloj.
@gloss Contador asíncrono | Contador en el que cada biestable usa como reloj la salida del anterior.
@gloss Carga paralela | Entrada que fuerza al contador a un valor dado.
@gloss Fin de cuenta | Salida que avisa de que el contador llega a su último estado, para encadenar contadores.

@q t8
¿Cuántos biestables necesita un contador de módulo 100?
+ 7
- 6
- 10
- 100
> $2^6=64<100\le2^7=128$.
@end
@q t8
Un contador binario síncrono de 4 bits tiene $Q_3Q_2Q_1Q_0=0111$. Tras el siguiente flanco:
+ $1000$
- $0000$
- $0110$
- $1111$
> $T_3=Q_2Q_1Q_0=1$, $T_2=Q_1Q_0=1$, $T_1=Q_0=1$, $T_0=1$: todos conmutan.
@end
@q t8
Un contador asíncrono de 5 bits con $t_{pd}=10$ ns por etapa: ¿cuánto tarda en estabilizarse como máximo?
+ 50 ns
- 10 ns
- 5 ns
- 32 ns
> $5\cdot10=50$ ns.
@end
