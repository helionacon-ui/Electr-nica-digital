%% id=t10
%% group=tema
%% n=10
%% title=Tema 10 · Análisis y síntesis de circuitos secuenciales síncronos
%% short=T10 · Autómatas síncronos
%% sub=Máquinas de Moore y de Mealy: del enunciado al diagrama de estados, a la tabla y al circuito. El tema que más cae.

@box idea | Desde cero
Un **autómata** (máquina de estados finitos) es un circuito que **recuerda en qué situación está** (su *estado*) y, según esa situación y las entradas, decide la salida y a qué estado pasa en el siguiente flanco. Un semáforo, una caja fuerte, un ascensor o un detector de secuencias son autómatas. Diseñar uno es siempre el mismo recorrido:

**palabras → diagrama de estados → tabla de transiciones → ecuaciones → circuito**.
@end

## Moore y Mealy

@fig mm {"kind":"moore"}
@fig mm {"kind":"mealy","cap":"Los dos modelos comparten la parte secuencial (biestables). Se diferencian en de qué depende la salida."}

| | Moore | Mealy |
|---|---|---|
| Salida | $Z=f(Q)$ | $Z=f(Q,X)$ |
| En el diagrama | Dentro del estado | En la flecha (entrada/salida) |
| Cambia | Solo en el flanco | En cuanto cambia la entrada |
| Estados | Suele necesitar más | Suele necesitar menos |
| Peligro | Sin glitches de entrada | La salida hereda ruidos de la entrada |

## El método de diseño, paso a paso

1. **Entiende el enunciado:** qué entradas hay, qué salidas, cuándo se activa cada una. Decide Moore o Mealy.
2. **Diagrama de estados:** un estado por cada «situación que hay que recordar». Para cada estado y cada valor de la entrada, una flecha.
3. **Número de biestables:** $n=\lceil\log_2(\text{estados})\rceil$.
4. **Codificación de estados:** asigna un código binario a cada estado. Afecta al tamaño del circuito.
5. **Tabla de transiciones:** para cada ($Q$, entradas) escribe $Q^+$ y la salida.
6. **Tabla de excitación:** con la tabla del tipo de biestable (JK, D, T) escribe qué entradas hacen falta.
7. **Simplifica** con Karnaugh. Los estados sin usar y las entradas imposibles son **indiferentes**.
8. **Dibuja** el circuito y **comprueba** con una secuencia de prueba.

## Ejemplo completo: detector de la secuencia 101 (Mealy)

Una entrada serie $X$ y una salida $Z$. Debe dar $Z=1$ cuando los **tres últimos** bits recibidos sean $1,0,1$ (las secuencias pueden solaparse: $10101$ contiene dos).

@sim fsmdet

@fig fsm {"nodes":{"S0":[70,100,"sin avance"],"S1":[240,100,"visto 1"],"S2":[410,100,"visto 10"]},"edges":[["S0","S0","0/0",0],["S0","S1","1/0",-30],["S1","S1","1/0",0],["S1","S2","0/0",-30],["S2","S0","0/0",-90],["S2","S1","1/1",30]],"W":520,"H":200,"title":"Detector 101 (Mealy): etiqueta entrada/salida","cap":"Tres estados. En S2 (hemos visto 10), un 1 completa la secuencia (Z=1) y además sirve como primer 1 de la siguiente."}

@ej t10-e1|Detector de la secuencia 101 con biestables D|Ejemplo T10|sec|t10.det101,t10.det_gates,t10.ej_out
@enun
Diseña un detector Mealy de la secuencia 101 con solape y biestables D. Comprueba con la entrada $X=1,0,1,0,1,1,0,1$.
@end
@antes
Teoría: Mealy, tabla de transiciones, biestable D ($D=Q^+$), Karnaugh con la combinación $Q_1Q_0=11$ sin usar como indiferente.
@end
@paso Estados y codificación
$S_0$: ningún avance. $S_1$: último bit 1. $S_2$: últimos bits 10. Son 3 estados: $n=2$ biestables. Codifico $S_0=00$, $S_1=01$, $S_2=10$. La combinación $11$ queda sin usar.
@end
@paso Tabla de transiciones
| $Q_1Q_0$ | $X$ | $Q_1^+Q_0^+$ | $Z$ |
|---|---|---|---|
| 00 | 0 | 00 | 0 |
| 00 | 1 | 01 | 0 |
| 01 | 0 | 10 | 0 |
| 01 | 1 | 01 | 0 |
| 10 | 0 | 00 | 0 |
| 10 | 1 | 01 | 1 |
@end
@paso Ecuaciones
Con D, $D=Q^+$. $Q_0^+=1$ siempre que $X=1$: $D_0=X$. $Q_1^+=1$ solo en ($01$, $X=0$): $D_1=Q_0\overline{X}$. La salida vale 1 solo en ($10$, $X=1$): $Z=Q_1X$.
@end
@paso Comprueba con la secuencia
Estado inicial $00$. $X=1$: $01$, $Z=0$. $X=0$: $10$, $Z=0$. $X=1$: $01$, **$Z=1$**. $X=0$: $10$, $Z=0$. $X=1$: $01$, **$Z=1$**. $X=1$: $01$, $Z=0$. $X=0$: $10$, $Z=0$. $X=1$: $01$, **$Z=1$**.
@end
@res
$D_1=Q_0\overline{X}$, $D_0=X$, $Z=Q_1X$. Para $X=1,0,1,0,1,1,0,1$ la salida es $0,0,1,0,1,0,0,1$. Verificado contra una especificación independiente con las $2^{10}$ secuencias de hasta 10 bits.
@end
@end

@box idea | Moore equivalente
El mismo detector en Moore necesita **4 estados** (hay que añadir un estado «visto 101» donde la salida vale 1), pero la salida solo cambia en el flanco. Se ha verificado por código que es equivalente a la versión Mealy.
@end

## Análisis: de un circuito a su comportamiento

Es el camino inverso, y suele ser más corto:

1. Escribe las **ecuaciones de entrada** de los biestables y de la salida a partir del circuito.
2. Construye la **tabla de transiciones** con la tabla característica del biestable.
3. Dibuja el **diagrama de estados**.
4. Con una secuencia de entradas, dibuja el **cronograma**.

Ejemplo de análisis con T: si $T_2=Q_1\oplus Q_0$, $T_1=Q_0$ y $T_0=\overline{Q_2}$, desde $000$ la secuencia de estados es $0,1,6,2,7,5,3,0$ (período 7). Verificado por código.

@sim caja

## Antirrebote y sincronización de entradas

Un pulsador real **rebota** unos milisegundos al pulsarse. Si lo conectas directamente a un contador, cuenta decenas de pulsaciones. Soluciones: (a) un **filtro**: esperar a que la entrada permanezca estable, por ejemplo, 20 ms; a 50 MHz son $50\cdot10^6\cdot0{,}02=10^6$ ciclos, es decir, un contador de **20 bits**. (b) Pasar la señal por **dos biestables D** para sincronizarla con el reloj y evitar la metaestabilidad.

@box mas | Más a fondo: reducción de estados
Dos estados son **equivalentes** si dan las mismas salidas ante todas las secuencias posibles. Fusionarlos reduce biestables y puertas. Se usa la **tabla de implicación** o el método de particiones. Antes de codificar, revisa si hay estados que se pueden unir.
@end

@box falla | Qué suele fallar
- Poner la salida de Mealy dentro del estado (o la de Moore en la flecha).
- Olvidar el estado inicial y un modo de forzarlo (reset).
- Contar mal los biestables: con 5 estados hacen falta 3 (no 5).
- Usar la tabla característica en lugar de la de excitación al derivar $J,K$.
- Olvidar que las combinaciones de código sin usar y las entradas imposibles son **indiferentes**.
- No comprobar el circuito con una secuencia: es la forma más rápida de pillar un error.
@end

@box formula | Fórmulas clave
- $n=\lceil\log_2(\#\text{estados})\rceil$.
- Moore: $Z=f(Q)$. Mealy: $Z=f(Q,X)$.
- D: $D=Q^+$. T: $T=Q\oplus Q^+$. JK: usar tabla de excitación.
@end

@card ¿Diferencia entre Moore y Mealy? || En Moore la salida solo depende del estado; en Mealy, del estado y de la entrada.
@card ¿Cuántos biestables para 9 estados? || 4 ($2^3=8<9\le16$).
@card ¿Entradas D para un estado destino $Q^+$? || $D=Q^+$.
@card ¿Entrada T para pasar de $Q$ a $Q^+$? || $T=Q\oplus Q^+$.
@card ¿Qué haces con las combinaciones de código sin usar? || Las marcas como indiferentes (X) en Karnaugh.
@gloss Autómata síncrono | Circuito secuencial cuyos biestables cambian todos con el mismo reloj.
@gloss Estado | Resumen de la historia del circuito que basta para decidir qué hará.
@gloss Diagrama de estados | Grafo con un nodo por estado y una flecha por transición.
@gloss Codificación de estados | Asignación de un código binario a cada estado.
@gloss Rebote | Oscilaciones breves de un contacto mecánico al abrir o cerrar.

@q t10
Un autómata tiene 6 estados. ¿Cuántos biestables necesita como mínimo?
+ 3
- 2
- 6
- 4
> $2^2=4<6\le2^3=8$.
@end
@q t10
En una máquina de Mealy, la salida:
+ Depende del estado y de la entrada actual
- Depende solo del estado
- Depende solo de la entrada
- Es siempre síncrona
> Esa es la definición; en Moore depende solo del estado.
@end
@q t10
Con biestables D, ¿cuál es la entrada $D$ de un biestable que debe pasar de 0 a 1?
+ $D=1$
- $D=0$
- $D=X$
- $D=\overline{Q}$
> En un biestable D, $D=Q^+$.
@end
@q t10
Un pulsador rebota 10 ms. Con reloj de 100 MHz, ¿cuántos ciclos debe esperar el filtro para ser fiable?
+ Al menos $10^6$
- 100
- $10^3$
- $10^9$
> $10\cdot10^{-3}\ \text{s}\cdot100\cdot10^{6}\ \text{Hz}=10^6$ ciclos.
@end
