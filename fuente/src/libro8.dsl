%% id=libro8
%% group=ejer
%% n=3.8
%% title=Libro de problemas · Capítulo 8 · Autómatas
%% short=Libro · Cap. 8 Autómatas
%% sub=Treinta y cinco problemas de diseño de autómatas de Moore y de Mealy: detectores de secuencias, aritmética serie, contadores, registros y automatismos industriales. Cada máquina se ha simulado contra un modelo de referencia y cada ecuación se ha comprobado.

@box idea | Cómo leer esta sección
Son los problemas resueltos del capítulo 8 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Los diagramas del libro **no se copian**: cada autómata se da como tabla de transición y, cuando es pequeño, como diagrama dibujado aquí. Las ecuaciones J‑K y D que imprime el libro se comprueban **una a una** contra la tabla de estados, y las máquinas se simulan frente a un modelo de referencia con miles de entradas aleatorias. Si algo del libro no cuadra, se anota en un cuadro de *Errata*. La teoría está en [[t10|el tema 10]].

Método común de todos los problemas (flujo de diseño):

1. **Diagrama de transición de estados**: qué hay que recordar y cómo cambia con cada entrada (Mealy: salida en la transición; Moore: salida en el estado).
2. **Tabla de transición** y reducción de estados (estados equivalentes se fusionan).
3. **Codificación** de estados con $n$ biestables, $2^n\ge$ número de estados; los códigos sobrantes y las entradas imposibles son **indiferentes** ($\times$).
4. **Tabla de excitación** del biestable elegido. Para el J‑K: $0\to0$ pide $J=0,K=\times$; $0\to1$ pide $J=1,K=\times$; $1\to0$ pide $J=\times,K=1$; $1\to1$ pide $J=\times,K=0$. Para el D: $D=Q^+$.
5. **Minimización** (Karnaugh o Quine‑McCluskey) de $J$, $K$ (o $D$) y de la salida, y **circuito**.

En este capítulo el orden de las variables es siempre *entradas primero, estado después* ($E\,q_1q_0$), y el estado inicial lo fija el RESET asíncrono de los biestables.
@end

@ej lb8-1|Detector de tres unos seguidos (Mealy)|Libro · Cap. 8 · P8.1|mealy,detector,jk|lb8.p81
@enun
Diseña un autómata de **Mealy** que vigile una línea serie $E_0$ y ponga su salida a 1 cuando lleguen **tres o más unos consecutivos**: la salida vale 1 en cada uno que completa o prolonga una racha de al menos tres. Impleméntalo con biestables J‑K.
@end
@antes
**Un autómata recuerda sólo lo imprescindible del pasado.** Aquí basta saber cuántos unos seguidos acaban de llegar: ninguno, uno, o dos o más. Eso son **tres estados**. Como la salida depende de la entrada actual (el tercer 1 se detecta *al llegar*), es natural un Mealy.
@end
@paso Estados
$Q_0$: la racha de unos es de longitud 0. $Q_1$: acaba de llegar un 1. $Q_2$: llevamos dos o más unos seguidos.
@end
@paso Transiciones
Un 0 rompe la racha desde cualquier estado y devuelve a $Q_0$. Un 1 avanza: $Q_0\to Q_1\to Q_2$ y $Q_2$ se queda en $Q_2$. La salida vale 1 sólo en la transición $Q_2\xrightarrow{1}Q_2$ (es el tercer 1 o posterior). Se permiten solapamientos: 1111 da dos detecciones.
@end
@paso Codificación
Con tres estados hacen falta dos biestables: $Q_0=00$, $Q_1=01$, $Q_2=10$. El código $11$ no se usa y es indiferente.
@end
@paso Tabla de excitación y minimización
Para cada fila $(E_0,q_1q_0)$ se anota qué pide cada biestable J‑K según el cambio $q\to Q$. Minimizando con los códigos libres como indiferentes sale el resultado de abajo.
@end
@paso Circuito
Dos biestables J‑K con el mismo reloj. $J_1$ es una AND de $E_0$ y $q_0$; $K_1$ es $\overline{E_0}$ (un inversor); $J_0$ es una AND de $E_0$ y $\overline{q_1}$; $K_0$ está a nivel alto fijo; la salida es una AND de $E_0$ y $q_1$.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""]}, "edges": [["Q0", "Q0", "0/0", 0], ["Q0", "Q1", "1/0", 38], ["Q1", "Q0", "0/0", 38], ["Q1", "Q2", "1/0", 0], ["Q2", "Q0", "0/0", -70], ["Q2", "Q2", "1/1", 0]], "W": 430, "H": 180, "title": "Detector de 111 (Mealy). Etiquetas: E0/S"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q0/0 | Q1/0 |
| Q1 | Q0/0 | Q2/0 |
| Q2 | Q0/0 | Q2/1 |

| Estado | Código $q_1q_0$ |
|---|---|
| Q0 | 00 |
| Q1 | 01 |
| Q2 | 10 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $E_{0}\cdot q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $1$ |
| $S$ | $E_{0}\cdot q_{1}$ |

Las ecuaciones impresas en el libro se han comprobado en **las seis transiciones definidas** y reproducen la tabla. Mi propia minimización coincide con ellas término a término.

Coste de la lógica combinacional: 3 puertas AND, 0 OR y 2 inversores (sin contar los biestables).

Simulación: 200 flujos aleatorios de 60 bits comparados con el modelo «los tres últimos bits son 111»; coinciden en todos.
@end
@end

@ej lb8-2|Detector de tres ceros seguidos (Mealy, con J‑K y con D)|Libro · Cap. 8 · P8.2|mealy,detector,jk,d|lb8.p82
@enun
Igual que el problema anterior pero detectando **tres o más ceros seguidos**. Impleméntalo con biestables J‑K y después con biestables D.
@end
@antes
**Es el mismo autómata con los papeles de 0 y 1 intercambiados.** Sólo cambian las ecuaciones: donde antes aparecía $E_0$ ahora aparece $\overline{E_0}$. Lo interesante es comparar las dos tecnologías de biestable.
@end
@paso Autómata
Tres estados que cuentan los ceros seguidos (0, 1, 2 o más). Un 1 devuelve a $Q_0$. La salida es 1 en $Q_2\xrightarrow{0}Q_2$.
@end
@paso Con biestables D
Como $D=Q^+$, basta mirar en qué filas el código siguiente tiene cada bit a 1: $D_0$ sólo vale 1 al pasar de $Q_0$ a $Q_1$ con un 0, y $D_1$ vale 1 al ir a $Q_2$.
@end
@paso Con biestables J‑K
Las ecuaciones tienen más términos de partida (hay dos funciones por biestable) pero se simplifican mucho gracias a los indiferentes: $K_0=1$ siempre.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""]}, "edges": [["Q0", "Q0", "1/0", 0], ["Q0", "Q1", "0/0", 38], ["Q1", "Q0", "1/0", 38], ["Q1", "Q2", "0/0", 0], ["Q2", "Q0", "1/0", -70], ["Q2", "Q2", "0/1", 0]], "W": 430, "H": 180, "title": "Detector de 000 (Mealy). Etiquetas: E0/S"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q1/0 | Q0/0 |
| Q1 | Q2/0 | Q0/0 |
| Q2 | Q2/1 | Q0/0 |

**Con biestables J‑K**

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{E_{0}}\cdot q_{0}$ |
| $K_{1}$ | $E_{0}$ |
| $J_{0}$ | $\overline{E_{0}}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $1$ |
| $S$ | $\overline{E_{0}}\cdot q_{1}$ |

**Con biestables D**

| Función | Ecuación |
|---|---|
| $D_{1}$ | $\overline{E_{0}}\cdot q_{0}  +  \overline{E_{0}}\cdot q_{1}$ |
| $D_{0}$ | $\overline{E_{0}}\cdot \overline{q_{1}}\cdot \overline{q_{0}}$ |
| $S$ | $\overline{E_{0}}\cdot q_{1}$ |

Ambos juegos de ecuaciones, los del libro y los míos, se han comprobado contra la tabla. Con D se necesitan dos funciones y con J‑K cuatro, pero las del J‑K son mucho más cortas: es el compromiso habitual (el J‑K simplifica la lógica a cambio de más hilos).
@end
@end

@ej lb8-3|Detector de la secuencia 1011 con solapamiento|Libro · Cap. 8 · P8.3|mealy,detector,jk,secuencia|lb8.p83
@enun
Diseña un autómata de Mealy que detecte la secuencia **1011** en una línea serie, permitiendo que dos apariciones se solapen (el último 1 de una puede ser el primero de la siguiente).
@end
@antes
**Cada estado representa «lo que llevo escrito del patrón»**: nada ($Q_0$), «1» ($Q_1$), «10» ($Q_2$) y «101» ($Q_3$). Lo difícil son las transiciones que *no* avanzan: hay que volver al **sufijo más largo que siga siendo prefijo del patrón**.
@end
@paso Transiciones que avanzan
$Q_0\xrightarrow{1}Q_1$, $Q_1\xrightarrow{0}Q_2$, $Q_2\xrightarrow{1}Q_3$ y $Q_3\xrightarrow{1}$ (se completa 1011: salida 1).
@end
@paso Transiciones que retroceden
En $Q_1$ («1») un nuevo 1 deja «1»: se queda en $Q_1$. En $Q_2$ («10») un 0 da «100»: sin prefijo útil, a $Q_0$. En $Q_3$ («101») un 0 da «1010» y su sufijo «10» es prefijo del patrón: a $Q_2$. Tras detectar (1011) el último 1 queda como primer 1 de otra posible aparición: a $Q_1$ (solapamiento).
@end
@paso Codificación y ecuaciones
Cuatro estados, dos biestables, código natural. Al estar los cuatro códigos usados no hay indiferentes por códigos libres.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""], "Q3": [475, 70, ""]}, "edges": [["Q0", "Q0", "0/0", 0], ["Q0", "Q1", "1/0", 0], ["Q1", "Q2", "0/0", 0], ["Q1", "Q1", "1/0", 0], ["Q2", "Q0", "0/0", -70], ["Q2", "Q3", "1/0", 38], ["Q3", "Q2", "0/0", 38], ["Q3", "Q1", "1/1", -70]], "W": 560, "H": 180, "title": "Detector de 1011. Etiquetas: E0/S"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q0/0 | Q1/0 |
| Q1 | Q2/0 | Q1/0 |
| Q2 | Q0/0 | Q3/0 |
| Q3 | Q2/0 | Q1/1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{E_{0}}\cdot q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}\cdot \overline{q_{0}}  +  E_{0}\cdot q_{0}$ |
| $J_{0}$ | $E_{0}$ |
| $K_{0}$ | $\overline{E_{0}}$ |
| $S$ | $E_{0}\cdot q_{1}\cdot q_{0}$ |

Comprobadas las ocho transiciones y simulados 200 flujos aleatorios de 60 bits contra «los cuatro últimos bits son 1011».
@end
@end

@ej lb8-4|Tres bits iguales seguidos, ceros o unos (Mealy, 5 estados)|Libro · Cap. 8 · P8.4|mealy,detector,jk|lb8.p84
@enun
Diseña un autómata de Mealy que active su salida cuando en la línea $E_0$ lleguen **tres o más bits iguales seguidos**, sean tres ceros o tres unos.
@end
@antes
**Ahora el estado debe recordar dos cosas:** cuál fue el último bit y cuántas veces seguidas se repite. Hay que distinguir «un 0 suelto», «dos ceros», «tres o más ceros» y lo mismo para los unos; pero el primer bit de la secuencia, que aún no tiene antecesor, es el estado inicial $Q_0$. Total: **cinco estados**.
@end
@paso Estados
$Q_0$ inicial. $Q_1$: un 0 (racha de ceros de longitud 1). $Q_2$: dos o más ceros. $Q_3$: un 1. $Q_4$: dos o más unos.
@end
@paso Transiciones
Un bit igual al de la racha la alarga (y si ya era de longitud 2 o más, la salida es 1); un bit distinto empieza una racha nueva de longitud 1 (de $Q_1$, $Q_2$ o $Q_4$ se pasa a $Q_3$ con un 1; de $Q_3$ o $Q_4$ a $Q_1$ con un 0).
@end
@paso Tres biestables
Cinco estados necesitan $\lceil\log_2 5\rceil=3$ biestables. Los códigos 101, 110 y 111 son indiferentes: eso permite simplificar mucho las ecuaciones.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""], "Q3": [150, 190, ""], "Q4": [280, 190, ""]}, "edges": [["Q0", "Q1", "0/0", 0], ["Q0", "Q3", "1/0", 0], ["Q1", "Q2", "0/0", 0], ["Q1", "Q3", "1/0", 38], ["Q2", "Q2", "0/1", 0], ["Q2", "Q3", "1/0", 0], ["Q3", "Q1", "0/0", 38], ["Q3", "Q4", "1/0", 0], ["Q4", "Q1", "0/0", 0], ["Q4", "Q4", "1/1", 0]], "W": 430, "H": 300, "title": "Tres bits iguales seguidos (Mealy)"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q1/0 | Q3/0 |
| Q1 | Q2/0 | Q3/0 |
| Q2 | Q2/1 | Q3/0 |
| Q3 | Q1/0 | Q4/0 |
| Q4 | Q1/0 | Q4/1 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $E_{0}\cdot q_{1}\cdot q_{0}$ |
| $K_{2}$ | $\overline{E_{0}}$ |
| $J_{1}$ | $q_{0}  +  E_{0}\cdot \overline{q_{2}}$ |
| $K_{1}$ | $q_{0}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{2}}  +  \overline{E_{0}}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $\overline{E_{0}}\cdot \overline{q_{1}}  +  E_{0}\cdot q_{1}$ |
| $S$ | $\overline{E_{0}}\cdot q_{1}\cdot \overline{q_{0}}  +  E_{0}\cdot q_{2}$ |

Se han comprobado las ecuaciones del libro en las 10 transiciones definidas (las combinaciones con códigos 101‑111 son indiferentes) y se ha simulado contra el modelo «los tres últimos bits son iguales». Reducción de estados: el algoritmo de particiones no fusiona ninguno, así que cinco es el mínimo.
@end
@end

@ej lb8-5|Detectar 1111 y 11011 con solapamiento (Moore y Mealy)|Libro · Cap. 8 · P8.5|mealy,moore,detector,secuencia|lb8.p85
@enun
Diseña, como autómata de **Mealy** y como autómata de **Moore**, un detector de **dos** secuencias a la vez: 1111 y 11011. Se permite que las apariciones se solapen y que se pase de una secuencia a otra sin volver al principio.
@end
@antes
**El estado recuerda el sufijo más largo de lo recibido que todavía puede convertirse en alguna de las dos secuencias.** Los prefijos propios de los patrones son $\varepsilon$, 1, 11, 111, 110 y 1101: **seis estados**. El Moore necesita dos más porque «detecté ahora» debe vivir en el estado y no en la transición.
@end
@paso Mealy
Se construye por «longest suffix»: desde el prefijo $p$ y la entrada $b$ se forma $pb$; si acaba en algún patrón completo la salida vale 1; el estado siguiente es el sufijo más largo de $pb$ que sea prefijo propio de algún patrón. Por ejemplo, de «111» con un 1 se completa 1111 y queda «111» (solapamiento).
@end
@paso Moore
Cada estado Mealy se **duplica** si se puede llegar a él tanto con salida 0 como con salida 1. Aquí le pasa a «111» (tras 1111) y a «11» (tras 11011): 6 + 2 = **8 estados**, sin fusiones posibles.
@end
@paso Comprobación
Ambas máquinas se simulan contra «los cuatro últimos bits son 1111 o los cinco últimos 11011» con 200 flujos aleatorios de 60 bits.
@end
@res
**Mealy (6 estados)** — estado = sufijo útil

| Estado | Sufijo |
|---|---|
| Q0 | $\varepsilon$ |
| Q1 | 1 |
| Q2 | 11 |
| Q3 | 110 |
| Q4 | 111 |
| Q5 | 1101 |

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q0/0 | Q1/0 |
| Q1 | Q0/0 | Q2/0 |
| Q2 | Q3/0 | Q4/0 |
| Q3 | Q0/0 | Q5/0 |
| Q4 | Q3/0 | Q4/1 |
| Q5 | Q0/0 | Q2/1 |

**Moore (8 estados)**

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| Q0 | Q0 | Q1 | 0 |
| Q1 | Q0 | Q2 | 0 |
| Q2 | Q3 | Q4 | 0 |
| Q3 | Q0 | Q5 | 0 |
| Q4 | Q3 | Q6 | 0 |
| Q5 | Q0 | Q7 | 0 |
| Q6 | Q3 | Q6 | 1 |
| Q7 | Q3 | Q4 | 1 |

@box ojo | Errata en el libro
En el dibujo del libro del Mealy hay una flecha desde $Q_5$ con entrada 1 cuyo destino es ambiguo en la figura (acaba en un nudo de trazos). Por eso aquí se construye el autómata a partir de los sufijos y se verifica por simulación, en lugar de copiar esa flecha. El número de estados (6 y 8) sí coincide con el del libro.
@end
@end
@end

@ej lb8-6|Recordar cuál fue la última secuencia detectada: 010 o 110|Libro · Cap. 8 · P8.6|moore,mealy,detector,secuencia|lb8.p86
@enun
Una línea serie $E_0$ puede contener las secuencias 010 y 110. Diseña un autómata cuya salida valga **1 si la última secuencia detectada fue 010** y **0 si fue 110** (al empezar vale 0). Hazlo de Moore y de Mealy.
@end
@antes
**La salida es una memoria de un bit** (cuál fue la última detección), y además hay que seguir buscando los patrones en la línea. El estado debe contener ambas cosas: el valor de la salida y la parte útil de los dos últimos bits.
@end
@paso Modelo de referencia
Se parte de un modelo que lleva la salida $o$ y los dos últimos bits: si los tres últimos son 010, $o=1$; si son 110, $o=0$; en otro caso $o$ no cambia.
@end
@paso Reducción
El modelo tiene 14 estados posibles (2 valores de $o$ por 7 contextos). El algoritmo de equivalencia de estados lo reduce a **6 estados**, que son los de la tabla.
@end
@paso Cuidado con el solapamiento
Después de detectar 110, el 0 final **ya es el primer símbolo** de un posible 010 (110 10 → detecta 010). Un autómata que, tras 110, vuelva al estado de «nada recibido» pierde esa detección.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, "0"], "Q1": [215, 70, "0"], "Q4": [345, 70, "0"], "Q7": [85, 190, "1"], "Q9": [215, 190, "1"], "Q10": [345, 190, "1"]}, "edges": [["Q0", "Q1", "0", 0], ["Q0", "Q0", "1", 0], ["Q1", "Q1", "0", 0], ["Q1", "Q4", "1", 0], ["Q4", "Q7", "0", 0], ["Q4", "Q0", "1", -70], ["Q7", "Q7", "0", 0], ["Q7", "Q9", "1", 38], ["Q9", "Q7", "0", 38], ["Q9", "Q10", "1", 0], ["Q10", "Q1", "0", 0], ["Q10", "Q10", "1", 0]], "W": 430, "H": 300, "title": "Última secuencia: 010→1, 110→0 (Moore)"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| Q0 | Q1 | Q0 | 0 |
| Q1 | Q1 | Q4 | 0 |
| Q4 | Q7 | Q0 | 0 |
| Q7 | Q7 | Q9 | 1 |
| Q9 | Q7 | Q10 | 1 |
| Q10 | Q1 | Q10 | 1 |

Simulados 200 flujos aleatorios contra el modelo de referencia: coinciden. La versión de Mealy se obtiene con la misma tabla pasando la salida a las transiciones.

@box ojo | Errata en el libro
Según se lee en el diagrama del libro, desde el estado que ya había visto 110 con salida 1 (en la figura $Q_5$) el cero final lleva a $Q_0$ («nada»). Con entrada 0 1 0 1 1 0 1 0 el autómata así leído **no** detecta el último 010 (da 0, y debería dar 1), mientras que si ese cero lleva a $Q_1$ («un 0») sí lo detecta. Ambas versiones se han simulado.
@end
@end
@end

@ej lb8-7|Detectar 1010 o 110 y reducir estados (Mealy)|Libro · Cap. 8 · P8.7|mealy,detector,reduccion|lb8.p87
@enun
Diseña un autómata de Mealy que detecte las secuencias **1010** y **110** con solapamiento. Después comprueba si se pueden **fusionar estados** y analiza a mano el comportamiento con las entradas 1010, 110 y 110101000110.
@end
@antes
**El primer diseño es el de los sufijos útiles**, y sale con cinco estados. La pregunta clave es si dos estados son **equivalentes**: mismas salidas y, para cada entrada, siguientes equivalentes. Si lo son, se fusionan sin cambiar el comportamiento externo.
@end
@paso Cinco estados
$Q_0$ ($\varepsilon$), $Q_1$ (1), $Q_2$ (10), $Q_3$ (101) y $Q_4$ (11). En $Q_3$ y en $Q_4$ un 0 da salida 1 y lleva a $Q_2$ (1010 o 110); y con un 1 los dos van a $Q_4$.
@end
@paso Fusión
$Q_3$ y $Q_4$ **son equivalentes**: ante un 0 ambos emiten 1 y pasan a $Q_2$; ante un 1 ambos emiten 0 y pasan a $Q_4$ (equivalente a sí mismo). El algoritmo de particiones lo confirma. Queda un autómata de **cuatro estados**, con dos biestables.
@end
@paso Análisis a mano
Con 1010 el autómata recorre $Q_0\to Q_1\to Q_2\to Q_3\to Q_2$ y emite 1 en el último paso. Con 110 recorre $Q_0\to Q_1\to Q_3\to Q_2$ y emite 1 también al final. La secuencia larga 110101000110 produce **cuatro** detecciones (en los símbolos 3, 5, 7 y 12).
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""], "Q3": [475, 70, ""]}, "edges": [["Q0", "Q0", "0/0", 0], ["Q0", "Q1", "1/0", 0], ["Q1", "Q2", "0/0", 0], ["Q1", "Q3", "1/0", -70], ["Q2", "Q0", "0/0", -70], ["Q2", "Q3", "1/0", 38], ["Q3", "Q2", "0/1", 38], ["Q3", "Q3", "1/0", 0]], "W": 560, "H": 180, "title": "Detector de 1010 o 110 (4 estados)"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q0/0 | Q1/0 |
| Q1 | Q2/0 | Q3/0 |
| Q2 | Q0/0 | Q3/0 |
| Q3 | Q2/1 | Q3/0 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}\cdot \overline{q_{0}}$ |
| $J_{0}$ | $E_{0}$ |
| $K_{0}$ | $\overline{E_{0}}$ |
| $S$ | $\overline{E_{0}}\cdot q_{1}\cdot q_{0}$ |

Recorrido del libro, comprobado con la máquina de 4 estados:

| Entrada | Estados visitados | Detecciones |
|---|---|---|
| 1010 | Q0 → Q1 → Q2 → Q3 → Q2 | 1 |
| 110 | Q0 → Q1 → Q3 → Q2 | 1 |
| 110101000110 | Q0 → Q1 → Q3 → Q2 → Q3 → Q2 → Q3 → Q2 → Q0 → Q0 → Q1 → Q3 → Q2 | 4 |
@end
@end

@ej lb8-8|Detección de errores en código Manchester|Libro · Cap. 8 · P8.8|moore,manchester,reset,jk|lb8.p88
@enun
Un mensaje llega por una línea serie $E_0$ codificado en **Manchester**: cada bit se envía como dos símbolos, el 0 como 01 y el 1 como 10. Diseña un autómata que active una salida ERROR si en algún par llegan dos símbolos iguales (00 u 11). Sólo se sale del error con el RESET asíncrono. Después rehaz el diseño sustituyendo el RESET por un pulsador **P** de inicio/reinicio, que además marca el primer símbolo de cada par.
@end
@antes
**Es un detector de secuencias prohibidas (00 y 11) alineado por parejas.** El autómata sólo necesita saber en qué mitad del par está y cuál fue el primer símbolo. Una vez en ERROR no hay vuelta atrás: la entrada deja de importar (la «X» de la flecha).
@end
@paso Versión con RESET
Seis estados si se quiere saber qué bit llegó (Q0, Q1, Q2, R0, R1, ERROR): $R_0$ y $R_1$ significan «acabo de recibir un 0 / un 1». Como la única salida es ERROR, $R_0$, $R_1$ y $Q_0$ son **equivalentes** (mismas transiciones y misma salida): quedan **cuatro estados**.
@end
@paso Versión con pulsador P
Entradas ordenadas $P\,E_0$. Con $P=0$ en INICI el autómata espera. Con $P=1$ la entrada $E_0$ es el primer símbolo: va a $S_0$ si es 0 y a $S_1$ si es 1. En $S_0$ se espera un 1 (vuelve a INICI) y un 0 es error; en $S_1$ al revés. Para recibir el segundo símbolo no hace falta mantener $P$. De ERROR sólo se sale con $P=1$.
@end
@paso Códigos libres y condiciones libres
Con cuatro estados y dos biestables no hay códigos libres. En cambio, con $P$ y $E_0$ las transiciones tienen muchos «no importa» sobre la entrada (X), que se escriben como una sola flecha para varias combinaciones.
@end
@res
**Versión con RESET**

@fig fsm {"nodes": {"Q0": [85, 70, "0"], "Q1": [215, 70, "0"], "Q2": [345, 70, "0"], "ERROR": [475, 70, "1"]}, "edges": [["Q0", "Q1", "0", 38], ["Q0", "Q2", "1", 38], ["Q1", "Q0", "1", 38], ["Q1", "ERROR", "0", -70], ["Q2", "Q0", "0", 38], ["Q2", "ERROR", "1", 0], ["ERROR", "ERROR", "0, 1", 0]], "W": 560, "H": 180, "title": "Manchester con RESET (4 estados)"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| Q0 | Q1 | Q2 | 0 |
| Q1 | ERROR | Q0 | 0 |
| Q2 | Q0 | ERROR | 0 |
| ERROR | ERROR | ERROR | 1 |

Q0, R0 y R1 se han fusionado en Q0. Simulados 300 flujos aleatorios contra «hay algún par igual en las posiciones pares» y cien mensajes Manchester correctos (ninguno da error).

**Versión con pulsador $P$** (entradas $P\,E_0$)

@fig fsm {"nodes": {"INICI": [85, 70, "0"], "S0": [215, 70, "0"], "S1": [345, 70, "0"], "ERROR": [475, 70, "1"]}, "edges": [["INICI", "INICI", "0X", 0], ["INICI", "S0", "10", 38], ["INICI", "S1", "11", 38], ["S0", "INICI", "X1", 38], ["S0", "ERROR", "X0", -70], ["S1", "INICI", "X0", 38], ["S1", "ERROR", "X1", 0], ["ERROR", "ERROR", "0X", 0], ["ERROR", "INICI", "1X", -70]], "W": 560, "H": 180, "title": "Manchester con pulsador P"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| INICI | INICI | INICI | S0 | S1 | 0 |
| S0 | ERROR | INICI | ERROR | INICI | 0 |
| S1 | INICI | ERROR | INICI | ERROR | 0 |
| ERROR | ERROR | ERROR | INICI | INICI | 1 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| INICI | 00 | 0 |
| S0 | 01 | 0 |
| S1 | 10 | 0 |
| ERROR | 11 | 1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $P\cdot E_{0}\cdot \overline{q_{0}}  +  \overline{E_{0}}\cdot q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}\cdot \overline{q_{0}}  +  P\cdot q_{0}$ |
| $J_{0}$ | $E_{0}\cdot q_{1}  +  P\cdot \overline{E_{0}}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $E_{0}\cdot \overline{q_{1}}  +  P\cdot q_{1}$ |
| $S$ | $q_{1}\cdot q_{0}$ |

Las ecuaciones del libro se han comprobado en las 16 transiciones; además se han verificado propiedades por simulación: un mensaje correcto no da error, un par repetido sí, el error permanece con $P=0$ y se limpia con $P=1$.
@end
@end

@ej lb8-9|Sumador serie con biestable de acarreo (Mealy)|Libro · Cap. 8 · P8.9|mealy,aritmetica-serie,jk,d|lb8.p89
@enun
Dos números llegan **en serie**, bit a bit y empezando por el menos significativo, por las líneas $E_1$ y $E_0$. Diseña el autómata que entrega en serie la suma, un bit por ciclo de reloj. Impleméntalo con un biestable J‑K y con uno D.
@end
@antes
**Sumar en serie es repetir un sumador completo con una memoria de un bit:** el acarreo. Basta un estado por cada valor del acarreo (0 ó 1): **dos estados y un solo biestable**. La salida es la suma de los tres bits $E_1,E_0$ y acarreo, y depende de la entrada actual, por lo que se trata de un Mealy.
@end
@paso Estados
$C_0$: el acarreo pendiente es 0. $C_1$: el acarreo pendiente es 1.
@end
@paso Transiciones y salida
La suma de tres bits $E_1+E_0+q$ da salida $S=E_1\oplus E_0\oplus q$ y nuevo acarreo $=E_1E_0+E_1q+E_0q$ (mayoría). Con $q=0$ sólo hay acarreo si ambos bits son 1. Con $q=1$ lo hay salvo que ambos sean 0.
@end
@paso Con J‑K
El acarreo se pone a 1 cuando $E_1E_0=11$ ($J_0=E_1E_0$) y se pone a 0 cuando $E_1E_0=00$ ($K_0=\overline{E_1}\,\overline{E_0}$); en los demás casos se mantiene.
@end
@paso Con D
$D_0$ es la función mayoría de $E_1$, $E_0$ y $q_0$, la misma de la etapa de acarreo de un sumador completo.
@end
@res
@fig fsm {"nodes": {"C0": [85, 70, ""], "C1": [215, 70, ""]}, "edges": [["C0", "C0", "00/0, 01/1, 10/1", 0], ["C0", "C1", "11/0", 38], ["C1", "C0", "00/1", 38], ["C1", "C1", "01/0, 10/0, 11/1", 0]], "W": 300, "H": 180, "title": "Sumador serie. Etiquetas: E1E0/S"}

| Estado | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| C0 | C0/0 | C0/1 | C0/1 | C1/0 |
| C1 | C0/1 | C1/0 | C1/0 | C1/1 |

**J‑K:** $J_0=E_1E_0$, $K_0=\overline{E_1}\,\overline{E_0}$. **D:** $D_0=E_0q_0+E_1q_0+E_1E_0$. **Salida:** $S=E_1\oplus E_0\oplus q_0$ (3 puertas XOR en cadena de dos).

Ejemplo $13+11$ (01101 y 01011, bit menos significativo primero): 

| Ciclo | $E_1$ | $E_0$ | Acarreo previo | Salida $S$ | Acarreo nuevo |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 1 | 0 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 1 |
| 4 | 0 | 0 | 1 | 1 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 |

La salida leída de abajo arriba es 11000 = 24, y el ciclo extra con entradas a 0 saca el acarreo final. Comprobado con 300 pares aleatorios de 8 bits.
@end
@end

@ej lb8-10|Sumador serie como autómata de Moore|Libro · Cap. 8 · P8.10|moore,aritmetica-serie,jk|lb8.p810
@enun
Rehaz el sumador serie del problema anterior como autómata de **Moore**: la salida debe depender sólo del estado. Los operandos llegan por $E_1$ y $E_0$, bit menos significativo primero. Impleméntalo con biestables J‑K y analiza si se pueden reducir estados y qué diferencia hay con la versión de Mealy.
@end
@antes
**En un Moore la salida es parte del estado**, así que el estado tiene que recordar, además del acarreo, el último bit de suma que se calculó. Las combinaciones (acarreo, suma) son cuatro: $C_0S_0$, $C_0S_1$, $C_1S_0$ y $C_1S_1$.
@end
@paso Transiciones
Desde un estado con acarreo $c$ y entradas $E_1E_0$ se calcula la suma $s=E_1\oplus E_0\oplus c$ y el acarreo nuevo $c'=E_1E_0+E_1c+E_0c$; el estado siguiente es $C_{c'}S_s$. La transición **no depende del bit de suma almacenado**: $C_0S_0$ y $C_0S_1$ tienen las mismas filas, y lo mismo $C_1S_0$ y $C_1S_1$.
@end
@paso ¿Se pueden fusionar?
A pesar de esa simetría **no son equivalentes**: tienen distinta salida (el bit $S$). Un Moore necesita pues cuatro estados y dos biestables, frente a los dos estados y un biestable del Mealy. El algoritmo de particiones confirma que cuatro es el mínimo.
@end
@paso Codificación y ecuaciones
Con el código $q_1q_0=(\text{acarreo},\text{suma})$ la salida es $S=q_0$. El biestable $q_1$ hace de acarreo exactamente como en el Mealy ($J_1=E_1E_0$, $K_1=\overline{E_1}\,\overline{E_0}$) y $q_0$ guarda la suma: $J_0=E_1\oplus E_0\oplus q_1$ y $K_0$ es su negación.
@end
@paso Retardo
En un circuito real la suma aparece **un ciclo más tarde** que en el Mealy (se lee en el estado, tras el flanco). Por eso, después de los $n$ bits de los operandos, hace falta un ciclo extra con entradas 00 para sacar el último bit.
@end
@res
@fig fsm {"nodes": {"C0S0": [85, 70, "0"], "C0S1": [215, 70, "1"], "C1S0": [345, 70, "0"], "C1S1": [475, 70, "1"]}, "edges": [["C0S0", "C0S0", "00", 0], ["C0S0", "C0S1", "01, 10", 38], ["C0S0", "C1S0", "11", -70], ["C0S1", "C0S0", "00", 38], ["C0S1", "C0S1", "01, 10", 0], ["C0S1", "C1S0", "11", 38], ["C1S0", "C0S1", "00", 38], ["C1S0", "C1S0", "01, 10", 0], ["C1S0", "C1S1", "11", 38], ["C1S1", "C0S1", "00", -70], ["C1S1", "C1S0", "01, 10", 38], ["C1S1", "C1S1", "11", 0]], "W": 560, "H": 180, "title": "Sumador serie de Moore. Cada estado: C (acarreo) y S (suma)"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| C0S0 | C0S0 | C0S1 | C0S1 | C1S0 | 0 |
| C0S1 | C0S0 | C0S1 | C0S1 | C1S0 | 1 |
| C1S0 | C0S1 | C1S0 | C1S0 | C1S1 | 0 |
| C1S1 | C0S1 | C1S0 | C1S0 | C1S1 | 1 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| C0S0 | 00 | 0 |
| C0S1 | 01 | 1 |
| C1S0 | 10 | 0 |
| C1S1 | 11 | 1 |

| Función | Ecuación (libro, corregida) |
|---|---|
| $J_{1}$ | $E_{1}\cdot E_{0}$ |
| $K_{1}$ | $\overline{E_{1}}\cdot \overline{E_{0}}$ |
| $J_{0}$ | $E_{1}\oplus E_{0}\oplus q_{1}$ |
| $K_{0}$ | $\overline{E_{1}}\cdot \overline{E_{0}}\cdot \overline{q_{1}}  +  \overline{E_{1}}\cdot E_{0}\cdot q_{1}  +  E_{1}\cdot \overline{E_{0}}\cdot q_{1}  +  E_{1}\cdot E_{0}\cdot \overline{q_{1}}$ |
| $S$ | $q_{0}$ |

Mi propia minimización coincide con ellas como función.

Simulados 300 pares de números de 8 bits: la salida da $a+b$ y es, ciclo a ciclo, idéntica a la del Mealy.

@box ojo | Errata en el libro
En la ecuación de $K_0$ el primer sumando aparece impreso como $\overline{E_1}\,\overline{E_0}\,q_1$, pero debe ser $\overline{E_1}\,\overline{E_0}\,\overline{q_1}$. $K_0=\overline{E_1\oplus E_0\oplus q_1}$ vale 1 cuando entre $E_1$, $E_0$ y $q_1$ hay un número **par** de unos: para 000 sí, para 001 no. Con el término impreso fallan exactamente dos transiciones, ambas con entrada 00: en $C_0S_1$ el biestable $q_0$ no se pone a 0 (debería, pues la suma es 0) y en $C_1S_1$ sí se pone a 0 (debería quedarse en 1, pues la suma es 1). Se ha comprobado contra la tabla.
@end
@end
@end

@ej lb8-11|Contador módulo 4 reversible (Moore, 8 estados)|Libro · Cap. 8 · P8.11|moore,contador,jk|lb8.p811
@enun
Diseña un contador de Moore **módulo 4 reversible**: con $E_0=1$ cuenta hacia arriba (0, 1, 2, 3, 0, …) y con $E_0=0$ hacia abajo (3, 2, 1, 0, 3, …). La salida son dos bits con el valor de la cuenta. Al cambiar el sentido, la nueva secuencia **empieza por su primer valor** (por ejemplo, al pasar de subir a bajar se sale con el 3).
@end
@antes
**El valor de la cuenta no basta para decidir el siguiente**: si la salida es 2, lo que viene depende de si se estaba subiendo (2→3) o bajando (2→1). Hay que recordar el sentido, y por eso se necesitan **dos copias de cada valor**: ocho estados.
@end
@paso Estados
$A_0\dots A_3$: cuenta ascendente (salida 0…3). $D_3\dots D_0$: cuenta descendente (salida 3…0). El estado inicial es $A_0$.
@end
@paso Transiciones
Dentro de una secuencia se avanza con el mismo valor de $E_0$ (en $A_k$, $E_0=1$ da $A_{k+1}$; en $D_k$, $E_0=0$ da $D_{k-1}$, con vuelta módulo 4). Al cambiar de sentido: desde cualquier $A_k$ con $E_0=0$ se salta a $D_3$, y desde cualquier $D_k$ con $E_0=1$ se salta a $A_0$.
@end
@paso ¿Bastarían cuatro estados?
No. El algoritmo de particiones deja los ocho estados separados: por ejemplo $A_2$ y $D_2$ tienen la misma salida pero llevan a salidas distintas (3 ó 3 frente a 1 ó 0).
@end
@paso Codificación
Se codifica con $q_2$ = sentido (0 ascendente, 1 descendente) y $q_1q_0$ = el valor en las ascendentes; en las descendentes se numeran $D_3=100$, $D_2=101$, $D_1=110$, $D_0=111$. Con esa elección las salidas son sencillas: $S_1=q_2\oplus q_1$, $S_0=q_2\oplus q_0$ (una XOR convierte los códigos descendentes en el valor de la cuenta).
@end
@res
@fig fsm {"nodes": {"A0": [85, 70, "00"], "A1": [215, 70, "01"], "A2": [345, 70, "10"], "A3": [475, 70, "11"], "D3": [85, 190, "11"], "D2": [215, 190, "10"], "D1": [345, 190, "01"], "D0": [475, 190, "00"]}, "edges": [["A0", "D3", "0", 38], ["A0", "A1", "1", 0], ["A1", "D3", "0", 0], ["A1", "A2", "1", 0], ["A2", "D3", "0", 0], ["A2", "A3", "1", 0], ["A3", "D3", "0", 0], ["A3", "A0", "1", -70], ["D3", "D2", "0", 0], ["D3", "A0", "1", 38], ["D2", "D1", "0", 0], ["D2", "A0", "1", 0], ["D1", "D0", "0", 0], ["D1", "A0", "1", 0], ["D0", "D3", "0", 70], ["D0", "A0", "1", 0]], "W": 560, "H": 300, "title": "Contador reversible mod 4 (Moore). Estado: salida"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| A0 | D3 | A1 | 00 |
| A1 | D3 | A2 | 01 |
| A2 | D3 | A3 | 10 |
| A3 | D3 | A0 | 11 |
| D3 | D2 | A0 | 11 |
| D2 | D1 | A0 | 10 |
| D1 | D0 | A0 | 01 |
| D0 | D3 | A0 | 00 |

| Estado | Código $q_2q_1q_0$ | Salida |
|---|---|---|
| A0 | 000 | 00 |
| A1 | 001 | 01 |
| A2 | 010 | 10 |
| A3 | 011 | 11 |
| D3 | 100 | 11 |
| D2 | 101 | 10 |
| D1 | 110 | 01 |
| D0 | 111 | 00 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $\overline{E_{0}}$ |
| $K_{2}$ | $E_{0}$ |
| $J_{1}$ | $E_{0}\cdot \overline{q_{2}}\cdot q_{0}  +  \overline{E_{0}}\cdot q_{2}\cdot q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}\cdot \overline{q_{2}}  +  q_{0}  +  E_{0}\cdot q_{2}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{2}}  +  \overline{E_{0}}\cdot q_{2}$ |
| $K_{0}$ | $1$ |
| $S_{1}$ | $q_{2}\oplus q_{1}$ |
| $S_{0}$ | $q_{2}\oplus q_{0}$ |

Las ecuaciones del libro se han comprobado en las 16 transiciones (los ocho códigos están usados, no hay indiferentes). Simulados 300 flujos aleatorios de 40 entradas contra un modelo que lleva la cuenta y el sentido.
@end
@end

@ej lb8-12|Contador módulo 8 con habilitación (Moore)|Libro · Cap. 8 · P8.12|moore,contador,jk|lb8.p812
@enun
Diseña un contador de Moore **módulo 8** con una entrada de habilitación $E_0$: con $E_0=1$ cuenta un valor en cada flanco de reloj y con $E_0=0$ se mantiene. La salida son tres bits con el valor de la cuenta.
@end
@antes
**Ocho estados, uno por valor, y la salida es el propio código del estado**, así que no hace falta lógica de salida. Todo el trabajo está en las funciones de excitación, y con J‑K sale una estructura muy regular.
@end
@paso Autómata
$Q_n\xrightarrow{E_0=0}Q_n$ y $Q_n\xrightarrow{E_0=1}Q_{(n+1)\bmod 8}$. Es un anillo de ocho estados con un lazo en cada uno.
@end
@paso Codificación
Se asigna a $Q_n$ el binario de $n$ en $q_2q_1q_0$; así $S_2S_1S_0=q_2q_1q_0$.
@end
@paso Excitación
Un bit cambia de valor cuando el contador está habilitado **y todos los bits inferiores valen 1** (acarreo del incremento). Para ese bit se necesita conmutar: $J=K=1$; en caso contrario, mantener: $J=K=0$. De ahí $J_0=K_0=E_0$, $J_1=K_1=E_0q_0$ y $J_2=K_2=E_0q_1q_0$: es un contador con biestables que **conmutan** (tipo T).
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, "000"], "Q1": [215, 70, "001"], "Q2": [345, 70, "010"], "Q3": [475, 70, "011"], "Q4": [85, 190, "100"], "Q5": [215, 190, "101"], "Q6": [345, 190, "110"], "Q7": [475, 190, "111"]}, "edges": [["Q0", "Q0", "0", 0], ["Q0", "Q1", "1", 0], ["Q1", "Q1", "0", 0], ["Q1", "Q2", "1", 0], ["Q2", "Q2", "0", 0], ["Q2", "Q3", "1", 0], ["Q3", "Q3", "0", 0], ["Q3", "Q4", "1", 0], ["Q4", "Q4", "0", 0], ["Q4", "Q5", "1", 0], ["Q5", "Q5", "0", 0], ["Q5", "Q6", "1", 0], ["Q6", "Q6", "0", 0], ["Q6", "Q7", "1", 0], ["Q7", "Q7", "0", 0], ["Q7", "Q0", "1", 0]], "W": 560, "H": 300, "title": "Contador módulo 8 con habilitación. Etiqueta: E0"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| Q0 | Q0 | Q1 | 000 |
| Q1 | Q1 | Q2 | 001 |
| Q2 | Q2 | Q3 | 010 |
| Q3 | Q3 | Q4 | 011 |
| Q4 | Q4 | Q5 | 100 |
| Q5 | Q5 | Q6 | 101 |
| Q6 | Q6 | Q7 | 110 |
| Q7 | Q7 | Q0 | 111 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $E_{0}\cdot q_{1}\cdot q_{0}$ |
| $K_{2}$ | $E_{0}\cdot q_{1}\cdot q_{0}$ |
| $J_{1}$ | $E_{0}\cdot q_{0}$ |
| $K_{1}$ | $E_{0}\cdot q_{0}$ |
| $J_{0}$ | $E_{0}$ |
| $K_{0}$ | $E_{0}$ |
| $S_{2}$ | $q_{2}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

Mi minimización coincide con las del libro como función. Simulados 200 flujos de 50 entradas: la salida es siempre «número de unos recibidos módulo 8». Coste: dos AND de dos y tres entradas ($E_0q_0$ y $E_0q_1q_0$; la AND de tres puede hacerse en cascada con la anterior).
@end
@end

@ej lb8-13|Registro de desplazamiento de 3 bits visto como autómata (Moore)|Libro · Cap. 8 · P8.13|moore,registro,jk,d|lb8.p813
@enun
Un registro de desplazamiento de tres bits, con entrada serie $E_0$ y desplazamiento hacia la izquierda, es también un autómata. Diséñalo como autómata de Moore (salida = contenido del registro) con biestables J‑K y con biestables D.
@end
@antes
**Ejercicio de cambio de punto de vista:** el estado es el contenido del registro, así que hay ocho estados $Q_n$ ($n$ = valor binario). Al desplazar a la izquierda el valor se duplica y entra $E_0$ por la derecha. Ya se sabe cómo debe quedar el circuito; la gracia es que el método general lo reconstruye.
@end
@paso Transiciones
$Q_n\xrightarrow{0}Q_{2n\bmod 8}$ y $Q_n\xrightarrow{1}Q_{(2n+1)\bmod 8}$. El bit más significativo se pierde (sale del registro) y el nuevo bit entra por el menos significativo.
@end
@paso Con biestables D
$D=Q^+$: el bit $q_2$ pasa a valer el que tenía $q_1$, $q_1$ el de $q_0$ y $q_0$ el de la entrada: $D_2=q_1$, $D_1=q_0$, $D_0=E_0$. Son cables directos, sin puertas.
@end
@paso Con biestables J‑K
El método da $J_2=q_1$, $K_2=\overline{q_1}$, $J_1=q_0$, $K_1=\overline{q_0}$, $J_0=E_0$, $K_0=\overline{E_0}$: cada J‑K se comporta como un D (con un inversor entre J y K). Es la forma de convertir un J‑K en D.
@end
@res
| Estado | 0 | 1 | Salida |
|---|---|---|---|
| Q0 | Q0 | Q1 | 000 |
| Q1 | Q2 | Q3 | 001 |
| Q2 | Q4 | Q5 | 010 |
| Q3 | Q6 | Q7 | 011 |
| Q4 | Q0 | Q1 | 100 |
| Q5 | Q2 | Q3 | 101 |
| Q6 | Q4 | Q5 | 110 |
| Q7 | Q6 | Q7 | 111 |

**J‑K**

| Función | Ecuación |
|---|---|
| $J_{2}$ | $q_{1}$ |
| $K_{2}$ | $\overline{q_{1}}$ |
| $J_{1}$ | $q_{0}$ |
| $K_{1}$ | $\overline{q_{0}}$ |
| $J_{0}$ | $E_{0}$ |
| $K_{0}$ | $\overline{E_{0}}$ |
| $S_{2}$ | $q_{2}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

**D**

| Función | Ecuación |
|---|---|
| $D_{2}$ | $q_{1}$ |
| $D_{1}$ | $q_{0}$ |
| $D_{0}$ | $E_{0}$ |
| $S_{2}$ | $q_{2}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

Las ecuaciones del libro coinciden con las mías como funciones y reproducen las 16 transiciones. Simulados 200 flujos: la salida es siempre «los tres últimos bits recibidos» (con ceros al principio). El diagrama completo tiene 16 flechas y se omite aquí por ser poco legible.
@end
@end

@ej lb8-14|Bit de paridad par de un mensaje de 3 bits (Mealy, 7→5 estados)|Libro · Cap. 8 · P8.14|mealy,paridad,reduccion,jk|lb8.p814
@enun
Un mensaje de **tres bits** llega en serie por $E_0$, sin pausas, y se repite sin parar. Diseña un autómata de Mealy que ponga su salida a 0 en los dos primeros bits de cada mensaje y, en el tercero, entregue el **bit de paridad par** (1 si el número de unos del mensaje es impar). Después de cada tercer bit, el autómata vuelve al principio.
@end
@antes
**El primer diseño es un árbol de decisión de tres niveles**: tras el primer bit (2 casos), tras el segundo (4 casos) y tras el tercero se vuelve a $Q_0$. Salen siete estados. Pero para calcular la paridad **no importa qué bits llegaron, sólo cuántos unos**, y eso permite reducir.
@end
@paso Diseño en árbol (7 estados)
$Q_1$/$Q_2$: el primer bit fue 0/1. $Q_3,\dots,Q_6$: los dos primeros bits fueron 00, 01, 10 y 11. En el tercer bit la salida es el OR exclusivo de los tres. Desde $Q_3\dots Q_6$ se vuelve a $Q_0$.
@end
@paso Reducción
El algoritmo de particiones fusiona $Q_3$ con $Q_6$ (ambos con paridad par hasta ahora: salida 0 con un 0 y 1 con un 1) y $Q_4$ con $Q_5$ (paridad impar). Quedan **cinco estados**: $Q_0$, dos para «primer bit visto» y dos para «paridad par/impar».
@end
@paso Estados del diseño reducido
$Q_0$ inicio. $Q_1$ primer bit 1 y $Q_2$ primer bit 0 (el nombre es de la tabla de abajo). $Q_3$: paridad par tras dos bits. $Q_4$: paridad impar tras dos bits. En el tercer bit: $Q_3$ emite lo que llega y $Q_4$ lo invierte.
@end
@paso Mealy y Moore
En el Mealy la paridad sale **durante** el tercer ciclo (depende de la entrada actual); en el Moore equivalente sale tras el tercer flanco. Pasar a Moore exige duplicar $Q_0$ según lleguemos con salida 0 ó 1: **6 estados** y ninguna fusión posible.
@end
@res
**Árbol de 7 estados**

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q1/0 | Q2/0 |
| Q1 | Q3/0 | Q4/0 |
| Q2 | Q5/0 | Q6/0 |
| Q3 | Q0/0 | Q0/1 |
| Q4 | Q0/1 | Q0/0 |
| Q5 | Q0/1 | Q0/0 |
| Q6 | Q0/0 | Q0/1 |

**Reducido a 5 estados** (los estados se renombran)

@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""], "Q3": [150, 190, ""], "Q4": [280, 190, ""]}, "edges": [["Q0", "Q2", "0/0", -70], ["Q0", "Q1", "1/0", 0], ["Q1", "Q4", "0/0", 0], ["Q1", "Q3", "1/0", 0], ["Q2", "Q3", "0/0", 0], ["Q2", "Q4", "1/0", 0], ["Q3", "Q0", "0/0, 1/1", 0], ["Q4", "Q0", "0/1, 1/0", 0]], "W": 430, "H": 300, "title": "Paridad de 3 bits, 5 estados. E0/S"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q2/0 | Q1/0 |
| Q1 | Q4/0 | Q3/0 |
| Q2 | Q3/0 | Q4/0 |
| Q3 | Q0/0 | Q0/1 |
| Q4 | Q0/1 | Q0/0 |

| Estado | Código $q_2q_1q_0$ |
|---|---|
| Q0 | 000 |
| Q1 | 001 |
| Q2 | 010 |
| Q3 | 011 |
| Q4 | 100 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $\overline{E_{0}}\cdot \overline{q_{1}}\cdot q_{0}  +  E_{0}\cdot q_{1}\cdot \overline{q_{0}}$ |
| $K_{2}$ | $1$ |
| $J_{1}$ | $\overline{E_{0}}\cdot \overline{q_{2}}\cdot \overline{q_{0}}  +  E_{0}\cdot q_{0}$ |
| $K_{1}$ | $q_{0}  +  E_{0}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{2}}\cdot \overline{q_{1}}  +  \overline{E_{0}}\cdot q_{1}$ |
| $K_{0}$ | $\overline{E_{0}}  +  q_{1}$ |
| $S$ | $E_{0}\cdot q_{1}\cdot q_{0}  +  \overline{E_{0}}\cdot q_{2}$ |

Las ecuaciones del libro se han comprobado en las 10 transiciones (los códigos 101, 110 y 111 son indiferentes). Las dos versiones, la de 7 y la de 5 estados, se han simulado con 200 flujos aleatorios de 60 bits contra el modelo «cada tres bits, el OR exclusivo de los tres». Mi propia minimización coincide con ellas como función.
@end
@end

@ej lb8-15|Codificador de prioridad 4:2 serie (Mealy)|Libro · Cap. 8 · P8.15|mealy,codificador,jk|lb8.p815
@enun
Las cuatro entradas $d_0,d_1,d_2,d_3$ de un codificador de prioridad 4:2 llegan **en serie** por $E_0$, en ese orden (primero $d_0$), repitiéndose en grupos de cuatro bits. Diseña un autómata de Mealy que, al llegar el cuarto bit, entregue por dos salidas $S_1S_0$ el código de la entrada activa de mayor índice ($d_0$ no importa: si sólo está activa $d_0$ o ninguna, sale 00). En los otros ciclos las salidas valen 00. Estudia después si tiene ventaja recibir los bits en orden inverso.
@end
@antes
**La prioridad manda sobre el orden de llegada:** la entrada de mayor índice llega la última, así que cuando se recibe $d_3$ ya se conoce todo lo anterior. Cada estado debe resumir «cuál es la entrada activa más alta de las vistas hasta ahora». Con un contador de posición implícito (que sólo avanza) los estados forman un árbol que se reúne en $Q_0$.
@end
@paso Primer bit
$d_0$ no influye en el resultado: de $Q_0$ se pasa a $Q_1$ con cualquier entrada (la «X» de la flecha).
@end
@paso Segundo y tercer bit
$Q_1\to Q_2$ si $d_1=0$ y $Q_1\to Q_3$ si $d_1=1$. Después, $d_2=1$ lleva a $Q_5$ («la mayor vista es $d_2$», que domina a $d_1$) en cualquiera de los dos casos; con $d_2=0$ se llega a $Q_4$ (ninguna activa: 00) o a $Q_6$ (sólo $d_1$: 01).
@end
@paso Cuarto bit
Desde $Q_4$, $Q_5$ y $Q_6$ se vuelve a $Q_0$ y se emite el código: con $d_3=1$ siempre 11; con $d_3=0$, 00, 10 ó 01 según el estado.
@end
@paso Orden inverso (el más significativo primero)
Se puede, pero **no es más sencillo**: hay que decidir ya con $d_3$ y seguir contando los bits restantes sin cambiar de opinión, con cadenas de estados «X» hasta el final del grupo. Salen **10 estados** (el más significativo primero, la prioridad no deja ahorrar ninguno); el algoritmo de particiones confirma que son todos distintos.
@end
@res
**Orden $d_0$ primero** (7 estados)

@fig fsm {"nodes": {"Q0": [85, 70, ""], "Q1": [215, 70, ""], "Q2": [345, 70, ""], "Q3": [475, 70, ""], "Q4": [150, 190, ""], "Q5": [280, 190, ""], "Q6": [410, 190, ""]}, "edges": [["Q0", "Q1", "X/00", 0], ["Q1", "Q2", "0/00", 0], ["Q1", "Q3", "1/00", -70], ["Q2", "Q4", "0/00", 0], ["Q2", "Q5", "1/00", 0], ["Q3", "Q6", "0/00", 0], ["Q3", "Q5", "1/00", 0], ["Q4", "Q0", "0/00, 1/11", 0], ["Q5", "Q0", "0/10, 1/11", 0], ["Q6", "Q0", "0/01, 1/11", 0]], "W": 560, "H": 300, "title": "Codificador 4:2 serie (d0 primero). E0/S1S0"}

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q1/00 | Q1/00 |
| Q1 | Q2/00 | Q3/00 |
| Q2 | Q4/00 | Q5/00 |
| Q3 | Q6/00 | Q5/00 |
| Q4 | Q0/00 | Q0/11 |
| Q5 | Q0/10 | Q0/11 |
| Q6 | Q0/01 | Q0/11 |

| Estado | Código $q_2q_1q_0$ |
|---|---|
| Q0 | 000 |
| Q1 | 001 |
| Q2 | 010 |
| Q3 | 011 |
| Q4 | 100 |
| Q5 | 101 |
| Q6 | 110 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $q_{1}$ |
| $K_{2}$ | $1$ |
| $J_{1}$ | $\overline{q_{2}}\cdot q_{0}$ |
| $K_{1}$ | $\overline{q_{0}}  +  E_{0}$ |
| $J_{0}$ | $\overline{q_{2}}\cdot \overline{q_{1}}  +  E_{0}\cdot \overline{q_{2}}$ |
| $K_{0}$ | $\overline{E_{0}}  +  q_{2}$ |
| $S_{1}$ | $q_{2}\cdot q_{0}  +  E_{0}\cdot q_{2}$ |
| $S_{0}$ | $q_{2}\cdot q_{1}  +  E_{0}\cdot q_{2}$ |

Las ecuaciones del libro reproducen las 14 transiciones (código 111 indiferente). Simulados 300 flujos de 48 bits contra el modelo de prioridad: coinciden las dos versiones.

**Orden inverso** (10 estados)

| Estado | 0 | 1 |
|---|---|---|
| Q0 | Q2/00 | Q1/00 |
| Q1 | Q3/00 | Q3/00 |
| Q2 | Q5/00 | Q4/00 |
| Q3 | Q6/00 | Q6/00 |
| Q4 | Q7/00 | Q7/00 |
| Q5 | Q9/00 | Q8/00 |
| Q6 | Q0/11 | Q0/11 |
| Q7 | Q0/10 | Q0/10 |
| Q8 | Q0/01 | Q0/01 |
| Q9 | Q0/00 | Q0/00 |

Mi propia minimización coincide con ellas como función.
@end
@end

@ej lb8-16|Comparador serie de dos números (Moore)|Libro · Cap. 8 · P8.16|moore,comparador,aritmetica-serie,jk|lb8.p816
@enun
Dos números llegan en serie por $E_1$ ($A$) y $E_0$ ($B$), **empezando por el bit menos significativo**. Diseña un autómata de Moore que indique en tres salidas $S_2S_1S_0$ si, con los bits recibidos hasta el momento, $A>B$, $A=B$ o $A<B$. Impleméntalo con J‑K. Después piensa qué cambia si los bits llegan empezando por el más significativo.
@end
@antes
**Con el menos significativo primero manda siempre el último bit que difiere:** cada bit nuevo es más significativo que todos los anteriores, así que si $E_1\ne E_0$ decide él; si son iguales, se mantiene el veredicto anterior. Tres estados: IGUAL, MAYOR y MENOR.
@end
@paso Transiciones (LSB primero)
En cualquier estado, $E_1E_0=10$ lleva a MAYOR y $01$ a MENOR (el bit nuevo prevalece). Con $00$ ó $11$ se queda donde estaba. Desde IGUAL, $00$ y $11$ mantienen IGUAL.
@end
@paso Codificación y ecuaciones
IGUAL $=00$, MAYOR $=01$, MENOR $=10$ (el 11 es indiferente). Las salidas son simples: $S_2=q_0$ (mayor), $S_1=\overline{q_1}\,\overline{q_0}$ (igual), $S_0=q_1$ (menor).
@end
@paso Orden inverso (MSB primero)
Ahora el **primer bit que difiere** decide para siempre: MAYOR y MENOR se vuelven estados absorbentes (se quedan con cualquier entrada) y sólo IGUAL puede abandonarse. Las ecuaciones se simplifican: $K_1=K_0=0$, $J_1=\overline{E_1}E_0\overline{q_0}$, $J_0=E_1\overline{E_0}\,\overline{q_1}$. Esa versión necesita un reinicio para empezar otra comparación.
@end
@res
@fig fsm {"nodes": {"IGUAL": [85, 70, "010"], "MAYOR": [215, 70, "100"], "MENOR": [345, 70, "001"]}, "edges": [["IGUAL", "IGUAL", "00, 11", 0], ["IGUAL", "MENOR", "01", -70], ["IGUAL", "MAYOR", "10", 0], ["MAYOR", "MAYOR", "00, 10, 11", 0], ["MAYOR", "MENOR", "01", 38], ["MENOR", "MENOR", "00, 01, 11", 0], ["MENOR", "MAYOR", "10", 38]], "W": 430, "H": 180, "title": "Comparador serie, LSB primero (Moore). Estado: S2S1S0"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| IGUAL | IGUAL | MENOR | MAYOR | IGUAL | 010 |
| MAYOR | MAYOR | MENOR | MAYOR | MAYOR | 100 |
| MENOR | MENOR | MENOR | MAYOR | MENOR | 001 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| IGUAL | 00 | 010 |
| MAYOR | 01 | 100 |
| MENOR | 10 | 001 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{E_{1}}\cdot E_{0}$ |
| $K_{1}$ | $E_{1}\cdot \overline{E_{0}}$ |
| $J_{0}$ | $E_{1}\cdot \overline{E_{0}}$ |
| $K_{0}$ | $\overline{E_{1}}\cdot E_{0}$ |
| $S_{2}$ | $q_{0}$ |
| $S_{1}$ | $\overline{q_{1}}\cdot \overline{q_{0}}$ |
| $S_{0}$ | $q_{1}$ |

**Versión MSB primero**

@fig fsm {"nodes": {"IGUAL": [85, 70, "010"], "MAYOR": [215, 70, "100"], "MENOR": [345, 70, "001"]}, "edges": [["IGUAL", "IGUAL", "00, 11", 0], ["IGUAL", "MENOR", "01", -70], ["IGUAL", "MAYOR", "10", 0], ["MAYOR", "MAYOR", "XX", 0], ["MENOR", "MENOR", "XX", 0]], "W": 430, "H": 180, "title": "Comparador serie, MSB primero"}

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{E_{1}}\cdot E_{0}\cdot \overline{q_{0}}$ |
| $K_{1}$ | $0$ |
| $J_{0}$ | $E_{1}\cdot \overline{E_{0}}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $0$ |
| $S_{2}$ | $q_{0}$ |
| $S_{1}$ | $\overline{q_{1}}\cdot \overline{q_{0}}$ |
| $S_{0}$ | $q_{1}$ |

Simulados 300 pares de 8 bits en los dos órdenes, comprobando la salida **en cada ciclo** (en LSB primero, comparando los bits bajos recibidos; en MSB primero, los bits altos). Ejemplo con $A=001110_2=14$ y $B=100010_2=34$, LSB primero:

| Ciclo | $E_1E_0$ | Estado | Salida |
|---|---|---|---|
| 1 | 00 | IGUAL | 010 |
| 2 | 11 | IGUAL | 010 |
| 3 | 10 | MAYOR | 100 |
| 4 | 10 | MAYOR | 100 |
| 5 | 00 | MAYOR | 100 |
| 6 | 01 | MENOR | 001 |

Tras 5 bits ($A=01110=14$, $B=00010=2$) el resultado es MAYOR; el sexto bit, $A_5=0$ y $B_5=1$, lo cambia a MENOR, porque $B$ pasa a valer 34.

@box ojo | Errata en el libro
En el ejemplo numérico del libro el segundo número, 100010, aparece con valor decimal 18. Es 34 ($32+2$). La conclusión ($A<B$) no cambia.
@end
@end
@end

@ej lb8-17|Puerta automática con pulsador y topes (autómata «industrial»)|Libro · Cap. 8 · P8.17|moore,industrial,jk|lb8.p817
@enun
Una puerta se abre al activar un pulsador $P$. Se abre hasta que el sensor $A$ detecta el tope de apertura; entonces empieza a cerrarse hasta que el sensor $C$ detecta el tope de cierre, y se para. Dos salidas $S_1S_0$ controlan el motor: 00 para, 01 cierra, 10 abre. Las entradas se ordenan $PAC$. Diseña el autómata.
@end
@antes
**Los estados de un automatismo coinciden con los estados del aparato**: QUIETO, ABRIR y CERRAR (infinitivos o gerundios: una buena pista). La salida es el propio estado, así que es un Moore. Además, las entradas son **asíncronas** (las genera una persona o un sensor): antes de llegar al autómata se pasan por biestables D con el mismo reloj, que las sincronizan. El reloj despierta al autómata en cada flanco, y si va rápido es casi como si fuera continuo.
@end
@paso Método de las historias
En estos problemas se empieza **contando historias** (secuencias típicas de funcionamiento) y se escribe una tabla paso a paso. Después se completan las transiciones que faltan. Dos consejos del libro: en una historia, dos entradas consecutivas deben diferir en un solo bit (de 010 a 000 a 001, no de 101 a 000), y la transición de llegada a un estado debe **repetirse como lazo** en el estado de destino (si 010 lleva a CERRAR, 010 también mantiene CERRAR).
@end
@paso Entradas imposibles
Con tres entradas hay 8 combinaciones por estado, pero $A$ y $C$ no pueden valer 1 a la vez (la puerta no está abierta y cerrada a la vez): se descartan 011 y 111. Quedan **seis** transiciones por estado.
@end
@paso Completar los estados
QUIETO: con 001 se queda; con $P$ (100, 101, 110) se pone a abrir; con 000 ó 010 (en reposo pero sin el sensor de cerrado) pasa a cerrar, para dejar la puerta bien cerrada. ABRIR: con 001 sigue abriendo (extraño pero razonable); con 010 empieza a cerrar (tope de apertura); con 110 (pulsan y ya está abierta) también cierra. CERRAR: con 001 y con 101 llega al tope y queda quieto; con 100 (pulsan mientras cierra) vuelve a abrir; en el resto sigue cerrando.
@end
@res
| Estado | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 | Salida |
|---|---|---|---|---|---|---|---|---|---|
| QUIETO | CERRAR | QUIETO | CERRAR | × | ABRIR | ABRIR | ABRIR | × | 00 |
| ABRIR | ABRIR | ABRIR | CERRAR | × | ABRIR | ABRIR | CERRAR | × | 10 |
| CERRAR | CERRAR | QUIETO | CERRAR | × | ABRIR | QUIETO | CERRAR | × | 01 |

**Historia 1** (apertura y cierre completos)

| Paso | Entrada PAC | Estado | Salida $S_1S_0$ |
|---|---|---|---|
| 1 | 001 | QUIETO | 00 |
| 2 | 101 | ABRIR | 10 |
| 3 | 100 | ABRIR | 10 |
| 4 | 000 | ABRIR | 10 |
| 5 | 010 | CERRAR | 01 |
| 6 | 000 | CERRAR | 01 |
| 7 | 001 | QUIETO | 00 |

**Historia 2** (se pulsa $P$ mientras se cierra: vuelve a abrir)

| Paso | Entrada PAC | Estado | Salida $S_1S_0$ |
|---|---|---|---|
| 1 | 001 | QUIETO | 00 |
| 2 | 101 | ABRIR | 10 |
| 3 | 100 | ABRIR | 10 |
| 4 | 000 | ABRIR | 10 |
| 5 | 010 | CERRAR | 01 |
| 6 | 000 | CERRAR | 01 |
| 7 | 100 | ABRIR | 10 |
| 8 | 000 | ABRIR | 10 |
| 9 | 010 | CERRAR | 01 |
| 10 | 000 | CERRAR | 01 |
| 11 | 001 | QUIETO | 00 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| QUIETO | 00 | 00 |
| ABRIR | 10 | 10 |
| CERRAR | 01 | 01 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{1}$ | $P\cdot \overline{A}\cdot \overline{C} + P\cdot \overline{q_{0}}$ |
| $K_{1}$ | $A$ |
| $J_{0}$ | $\overline{P}\cdot \overline{C}\cdot \overline{q_{1}} + A\cdot q_{1}$ |
| $K_{0}$ | $C + P\cdot \overline{A}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

Las dos historias del libro se han reproducido exactamente con la tabla completada, y 300 ciclos aleatorios (abrir, esperar, cerrar, esperar) terminan siempre en QUIETO. El libro no desarrolla las ecuaciones de este ejemplo, que aquí se derivan por el método general, con el código 11 y las entradas imposibles como indiferentes; los resultados se han comprobado contra la tabla.
@end
@end

@ej lb8-18|Limpiaparabrisas con pulsadores de marcha y paro|Libro · Cap. 8 · P8.18|moore,industrial,jk|lb8.p818
@enun
Un limpiaparabrisas tiene un pulsador de marcha $M$ y otro de paro $P$. Al pulsar $M$ se pone en marcha y sigue funcionando al soltarlo; al pulsar $P$ se para. Si se pulsan los dos a la vez, **prevalece el paro**. Diseña el autómata con un biestable J‑K.
@end
@antes
**Dos estados, PARO y MARCHA, y la salida es el estado:** el motor está encendido sólo en MARCHA. La prioridad del paro se refleja en la fila 11 (los dos pulsadores): lleva a PARO desde cualquier estado.
@end
@paso Tabla de transición
Entradas ordenadas $MP$. En PARO: sólo 10 lleva a MARCHA. En MARCHA: sólo 01 y 11 llevan a PARO. En todo lo demás se mantiene el estado.
@end
@paso Ecuaciones
Con PARO $=0$ y MARCHA $=1$: $J_0$ debe valer 1 sólo desde PARO con $M=1,P=0$, y $K_0$ vale 1 siempre que $P=1$ (el paro manda). Resultado: $J_0=M\overline{P}$, $K_0=P$, $S_0=q_0$.
@end
@res
@fig fsm {"nodes": {"PARO": [85, 70, "0"], "MARCHA": [215, 70, "1"]}, "edges": [["PARO", "PARO", "00, 01, 11", 0], ["PARO", "MARCHA", "10", 38], ["MARCHA", "MARCHA", "00, 10", 0], ["MARCHA", "PARO", "01, 11", 38]], "W": 300, "H": 180, "title": "Limpiaparabrisas (entradas MP)"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| PARO | PARO | PARO | MARCHA | PARO | 0 |
| MARCHA | MARCHA | PARO | MARCHA | PARO | 1 |

| Función | Ecuación |
|---|---|
| $J_{0}$ | $M\cdot \overline{P}$ |
| $K_{0}$ | $P$ |
| $S$ | $q_{0}$ |

Comprobadas las ecuaciones del libro en las ocho transiciones, y simulados 200 flujos aleatorios de 40 pares $MP$ contra «el estado es PARO si $P$, si no MARCHA si $M$, si no el anterior».

@box ojo | Errata en el libro
El enunciado del libro pide un autómata de Mealy, pero la solución que se desarrolla tiene la salida en el estado y se rotula «resultados del autómata de Moore». Aquí se presenta como Moore, que es lo que de verdad se diseña (la salida es $q_0$ y no depende de las entradas).
@end
@end
@end

@ej lb8-19|Limpiaparabrisas con detector de posición de reposo (3 estados)|Libro · Cap. 8 · P8.19|moore,industrial,jk|lb8.p819
@enun
Se mejora el limpiaparabrisas anterior con un detector de reposo $R$ (vale 1 cuando la escobilla está en su posición inicial). Entradas ordenadas $MPR$. Al pulsar $P$ la escobilla **no se detiene donde esté**, sino que termina el recorrido y se para al llegar al reposo. Diseña el autómata con salida de Moore.
@end
@antes
**Ahora aparece un estado transitorio:** MAPA («marcha para paro»), en el que la escobilla sigue moviéndose pero ya se ha ordenado parar. MARCHA y PARO son estacionarios; MAPA dura hasta que $R=1$. El motor está activo en MARCHA y en MAPA.
@end
@paso Por qué no bastan dos estados
Con la entrada 001 (reposo, nada pulsado) la escobilla debe **seguir** si estaba en MARCHA (pasa por el reposo en cada ciclo) pero debe **parar** si estaba en MAPA (acaba de llegar al reposo). La misma entrada pide acciones distintas: hace falta memoria, o sea un tercer estado. El algoritmo de particiones lo confirma: MARCHA y MAPA tienen la misma salida pero no son equivalentes.
@end
@paso Transiciones
MARCHA: $P$ con $R=0$ (010) pasa a MAPA; $P$ con $R=1$ (011) a PARO; el resto sigue en MARCHA. MAPA: llegar al reposo sin $M$ (001, 011) lleva a PARO; si se vuelve a pulsar $M$ (100, 101) vuelve a MARCHA; si no, sigue. PARO: $M$ lleva a MARCHA; si la escobilla no está en reposo (000, 010) pasa a MAPA para volver a él; si lo está, se queda. Las combinaciones 110 y 111 ($M$ y $P$ a la vez) se consideran imposibles.
@end
@paso Codificación
PARO $=00$, MARCHA $=01$, MAPA $=11$ (el 10 es indiferente). Con esa elección la salida es $S=q_0$.
@end
@res
| Estado | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 | Salida |
|---|---|---|---|---|---|---|---|---|---|
| PARO | MAPA | PARO | MAPA | PARO | MARCHA | MARCHA | × | × | 0 |
| MARCHA | MARCHA | MARCHA | MAPA | PARO | MARCHA | MARCHA | × | × | 1 |
| MAPA | MAPA | PARO | MAPA | PARO | MARCHA | MARCHA | × | × | 1 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| PARO | 00 | 0 |
| MARCHA | 01 | 1 |
| MAPA | 11 | 1 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{1}$ | $\overline{M}\cdot \overline{R}\cdot \overline{q_{0}} + P\cdot \overline{R}$ |
| $K_{1}$ | $R + M$ |
| $J_{0}$ | $\overline{R} + M$ |
| $K_{0}$ | $\overline{M}\cdot R\cdot q_{1} + P\cdot R$ |
| $S$ | $q_{0}$ |

**Historia izquierda** (marcha, pasa por el reposo sin parar, se pulsa $P$ y se detiene al llegar al reposo)

| Paso | Entrada MPR | Estado | Salida |
|---|---|---|---|
| 1 | 001 | PARO | 0 |
| 2 | 101 | MARCHA | 1 |
| 3 | 100 | MARCHA | 1 |
| 4 | 000 | MARCHA | 1 |
| 5 | 001 | MARCHA | 1 |
| 6 | 000 | MARCHA | 1 |
| 7 | 010 | MAPA | 1 |
| 8 | 000 | MAPA | 1 |
| 9 | 001 | PARO | 0 |

**Historia derecha** (marcha y paro pulsando $P$ hasta el reposo)

| Paso | Entrada MPR | Estado | Salida |
|---|---|---|---|
| 1 | 100 | MARCHA | 1 |
| 2 | 000 | MARCHA | 1 |
| 3 | 010 | MAPA | 1 |
| 4 | 011 | PARO | 0 |

Simulados 300 casos aleatorios: sin pulsar $P$ la escobilla no se detiene nunca, y tras pulsar $P$ siempre acaba parada al llegar al reposo. El libro no incluye ecuaciones de este ejemplo; las de arriba son las mínimas que salen del método y se han comprobado contra la tabla.

@box ojo | Errata en el libro
En la historia de la izquierda, el paso 5 («tope») aparece con la entrada 010; debe ser 001: la escobilla **pasa por el reposo sin parar**, y con 010 iría a MAPA, lo que choca con el paso 7. En la de la derecha, «seguir pulsando $P$» y «reposo con $P$ pulsado» aparecen como 100 y 110; con el orden $MPR$ que usa el libro son 010 y 011. Por último, el estado del paso 9 se rotula QUIETO y es PARO.
@end
@end
@end

@ej lb8-20|Motor que se activa al soltar el pulsador (Moore, 4 estados)|Libro · Cap. 8 · P8.20|moore,industrial,jk|lb8.p820
@enun
Un motor se controla con un pulsador de marcha $M$ y otro de paro $P$, pero la orden **sólo se ejecuta al soltar** el pulsador (en el paso de 1 a 0). Diseña el autómata. Después hazlo con un **único pulsador** que alterne marcha y paro, también al soltar.
@end
@antes
**Hay que distinguir «pulsado» de «ya soltado».** Con la orden al soltar, cada pulsación produce dos situaciones distintas: mientras se mantiene el pulsador (el motor aún no ha cambiado) y después de soltarlo (ya cambió). Cuatro estados: P (parado), PM (parado, $M$ pulsado y pendiente de soltar), M (en marcha) y MP (en marcha, $P$ pulsado y pendiente).
@end
@paso Transiciones
P: con $M$ pulsado (10) pasa a PM; con $P$ (01) no hace nada. PM: mientras $M$ siga pulsado se queda; al soltarlo (00) pasa a M. M: con $P$ (01) pasa a MP; MP: al soltar $P$ (00) vuelve a P. Dos combinaciones, 11 y las que supondrían soltar uno y pulsar el otro en el mismo ciclo, no pueden ocurrir (indiferentes).
@end
@paso Salida
El motor está activo en M y en MP, y parado en P y PM. Con el código P $=00$, PM $=01$, M $=10$, MP $=11$ la salida es sencillamente $S_0=q_1$.
@end
@paso Un solo pulsador
Con el mismo cuarteto de estados, pero con una entrada: PM y MP **se alternan** cada vez que se pulsa. La tabla codificada es la de un contador que cambia con el flanco de bajada, y las ecuaciones tienen $J_1=K_1$ (el bit alto conmuta).
@end
@paso ¿Y con dos estados?
Con sólo «parado/marcha», la entrada 1 debería llevar de un estado al otro; pero entonces, mientras el pulsador siga a 1, el estado **conmutaría en cada flanco de reloj** (oscilaría). Hace falta recordar que «esta pulsación ya se ha contado», y eso son los otros dos estados.
@end
@res
**Dos pulsadores** (entradas $MP$; «—» = combinación imposible)

@fig fsm {"nodes": {"P": [85, 70, "0"], "PM": [215, 70, "0"], "M": [345, 70, "1"], "MP": [475, 70, "1"]}, "edges": [["P", "P", "00, 01", 0], ["P", "PM", "10", 0], ["PM", "M", "00", 0], ["PM", "PM", "10", 0], ["M", "M", "00, 10", 0], ["M", "MP", "01", 0], ["MP", "P", "00", -70], ["MP", "MP", "01", 0]], "W": 560, "H": 180, "title": "Motor con dos pulsadores. Estado: salida"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| P | P | P | PM | × | 0 |
| PM | M | — | PM | × | 0 |
| M | M | MP | M | × | 1 |
| MP | P | MP | — | × | 1 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| P | 00 | 0 |
| PM | 01 | 0 |
| M | 10 | 1 |
| MP | 11 | 1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{M}\cdot q_{0}$ |
| $K_{1}$ | $\overline{P}\cdot q_{0}$ |
| $J_{0}$ | $P\cdot q_{1}  +  M\cdot \overline{q_{1}}$ |
| $K_{0}$ | $\overline{M}\cdot \overline{P}$ |
| $S$ | $q_{1}$ |

Historia completa (reposo, pulso de $M$, soltar, pulso de $P$, soltar):

| Paso | Entrada $MP$ | Estado | Salida |
|---|---|---|---|
| 1 | 00 | P | 0 |
| 2 | 10 | PM | 0 |
| 3 | 00 | M | 1 |
| 4 | 01 | MP | 1 |
| 5 | 00 | P | 0 |

**Un solo pulsador** (entrada $P$)

@fig fsm {"nodes": {"P": [85, 70, "0"], "PM": [215, 70, "0"], "M": [345, 70, "1"], "MP": [475, 70, "1"]}, "edges": [["P", "P", "0", 0], ["P", "PM", "1", 0], ["PM", "PM", "1", 0], ["PM", "M", "0", 0], ["M", "M", "0", 0], ["M", "MP", "1", 0], ["MP", "MP", "1", 0], ["MP", "P", "0", -70]], "W": 560, "H": 180, "title": "Motor con un pulsador (alterna al soltar)"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| P | P | PM | 0 |
| PM | M | PM | 0 |
| M | M | MP | 1 |
| MP | P | MP | 1 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| P | 00 | 0 |
| PM | 01 | 0 |
| M | 10 | 1 |
| MP | 11 | 1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{P}\cdot q_{0}$ |
| $K_{1}$ | $\overline{P}\cdot q_{0}$ |
| $J_{0}$ | $P$ |
| $K_{0}$ | $\overline{P}$ |
| $S$ | $q_{1}$ |

Historia:

| Paso | Entrada $P$ | Estado | Salida |
|---|---|---|---|
| 1 | 0 | P | 0 |
| 2 | 1 | PM | 0 |
| 3 | 0 | M | 1 |
| 4 | 1 | MP | 1 |
| 5 | 0 | P | 0 |

Las ecuaciones del libro se han comprobado en todas las transiciones definidas de las dos versiones.

@box ojo | Errata en el libro
En la tabla de historias del problema con un solo pulsador, el paso 4 anota el estado MP con salida 0 y el paso 5 anota la entrada «soltar» como 1. El estado MP tiene salida 1 (el motor sigue en marcha mientras se mantiene el pulsador) y «soltar» es la entrada 0. La tabla de arriba es la correcta y reproduce el funcionamiento.
@end
@end
@end

@ej lb8-21|Depósito con dos bombas que se turnan|Libro · Cap. 8 · P8.21|moore,industrial,jk|lb8.p821
@enun
Un depósito se llena con dos bombas, $B_1$ y $B_2$, y tiene dos sensores de nivel: $I$ (inferior) y $S$ (superior), con las entradas ordenadas $IS$ (la combinación 01 es imposible: nivel alto sin nivel bajo). Con el nivel por encima de $S$ las bombas están paradas. Al bajar de $S$ se pone en marcha **una** bomba; si el nivel sigue bajando hasta quedar por debajo de $I$, se conectan **las dos**. Las bombas deben **turnarse** para desgastarse por igual. Diseña el autómata.
@end
@antes
**Para turnarse hay que recordar cuál fue la última en trabajar.** Eso duplica los estados «paradas» y «las dos en marcha»: hay que saber qué bomba toca después. Salen seis estados de Moore.
@end
@paso Estados
UB1 y UB2: bombas paradas con el depósito lleno; la siguiente bomba que se use será $B_1$ o $B_2$. B1 y B2: sólo trabaja esa bomba. B12a y B12b: trabajan las dos; hay dos copias porque al subir el nivel se debe continuar con la bomba **distinta** de la última usada.
@end
@paso Funcionamiento
De UB1 con $IS=10$ (nivel intermedio) se pasa a B1; desde B1, al llenarse (11), se pasa a UB2, de modo que la próxima vez toque $B_2$. Si con B1 el nivel baja de $I$ (00), se pasa a B12a; al volver a 10 sigue sólo $B_2$ (la que descansó) y al llenarse se vuelve a UB1.
@end
@paso Salidas
Las dos salidas $B_2B_1$ son 00 en UB1/UB2, 01 en B1, 10 en B2 y 11 en B12a/B12b.
@end
@paso ¿Bastan cuatro estados?
No. Con sólo «paradas», «$B_1$», «$B_2$» y «las dos» no se sabe cuál fue la última bomba en trabajar, y no se podría asegurar el turno. El algoritmo de particiones separa los seis estados.
@end
@res
@fig fsm {"nodes": {"UB1": [85, 70, "00"], "B1": [215, 70, "01"], "B12a": [345, 70, "11"], "UB2": [85, 190, "00"], "B2": [215, 190, "10"], "B12b": [345, 190, "11"]}, "edges": [["UB1", "B12a", "00", 38], ["UB1", "B1", "10", 0], ["UB1", "UB1", "11", 0], ["B1", "B12a", "00", 0], ["B1", "B1", "10", 0], ["B1", "UB2", "11", 0], ["B12a", "B12a", "00", 0], ["B12a", "B2", "10", 0], ["B12a", "UB1", "11", 38], ["UB2", "B12b", "00", 38], ["UB2", "B2", "10", 0], ["UB2", "UB2", "11", 0], ["B2", "B12b", "00", 0], ["B2", "B2", "10", 0], ["B2", "UB1", "11", 0], ["B12b", "B12b", "00", 0], ["B12b", "B1", "10", 0], ["B12b", "UB2", "11", 38]], "W": 430, "H": 300, "title": "Depósito con dos bombas (entradas IS). Estado: B2B1"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| UB1 | B12a | × | B1 | UB1 | 00 |
| B1 | B12a | × | B1 | UB2 | 01 |
| B12a | B12a | × | B2 | UB1 | 11 |
| UB2 | B12b | × | B2 | UB2 | 00 |
| B2 | B12b | × | B2 | UB1 | 10 |
| B12b | B12b | × | B1 | UB2 | 11 |

| Estado | Código $q_2q_1q_0$ | Salida |
|---|---|---|
| UB1 | 000 | 00 |
| B1 | 001 | 01 |
| B12a | 011 | 11 |
| UB2 | 100 | 00 |
| B2 | 010 | 10 |
| B12b | 111 | 11 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{2}$ | $\overline{I}\cdot q_{1}\cdot \overline{q_{0}} + S\cdot \overline{q_{1}}\cdot q_{0}$ |
| $K_{2}$ | $I\cdot \overline{S}$ |
| $J_{1}$ | $\overline{I} + \overline{S}\cdot q_{2}$ |
| $K_{1}$ | $S + I\cdot q_{2}$ |
| $J_{0}$ | $\overline{I} + \overline{S}\cdot \overline{q_{2}}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $S + I\cdot \overline{q_{2}}\cdot q_{1}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

Se reproducen las dos historias del libro: (izquierda) UB1, B1, UB2, UB2, B2, B12b, B1, UB2; (derecha) B1, B12a, B2, B12b, B1, UB2. Además, se ha simulado el depósito con un nivel que sube y baja de uno en uno, durante 200 trayectorias de 80 pasos, y se verifica que (i) las dos bombas sólo trabajan juntas con el nivel por debajo de $I$, (ii) están paradas sólo con el nivel lleno y (iii) la bomba que se usa al bajar de $S$ es siempre distinta de la última que trabajó sola. El libro desarrolla este ejemplo con el diagrama; las ecuaciones de aquí son las del método.
@end
@end

@ej lb8-22|Puertas de cristal de un edificio (Moore, entradas PCA)|Libro · Cap. 8 · P8.22|moore,industrial,jk|lb8.p822
@enun
Una puerta de cristal tiene un detector de persona $P$ y dos topes: abierta $A$ y cerrada $C$ (entradas ordenadas $PCA$). Debe cumplir: si llega una persona, se abre; si ha empezado a abrirse, **completa la apertura**; mientras haya gente, **permanece abierta**; si se está cerrando y aparece una persona, **vuelve a abrirse**. Sale una orden de dos bits (cerrando, abriendo).
@end
@antes
**Cuatro estados de la puerta:** CDA (cerrada, parada), ABDO (abriéndose), ABTA (abierta, parada) y CDO (cerrándose). Las salidas valen 00, 01, 00 y 10: CDA y ABTA son estacionarios y no se mueve el motor. $C=A=1$ es imposible (011 y 111 se descartan).
@end
@paso Lo que dice el enunciado
CDA con persona (100, 110) → ABDO. ABDO se mantiene con cualquier combinación sin $A$ (completa la apertura) y pasa a ABTA con $A=1$ y gente (101) o a CDO con $A=1$ sin gente (001). ABTA con gente y abierta (101) se queda; sin gente (001) pasa a CDO. CDO termina en CDA al llegar a $C$ (010); con persona vuelve a ABDO (100, 110) o a ABTA (101).
@end
@paso Lo que hay que completar
El dibujo no cubre todas las combinaciones. Las completo así: en CDA, sin $C$ (000) o con $A$ (001), la puerta no está donde debe: pasa a CDO (cerrar) como en el problema 8.17; en ABTA, si $A$ cae a 0 con gente (100, 110) se reabre (ABDO) y sin gente (000, 010) se cierra (CDO); CDO con 110 reabre (ABDO).
@end
@res
| Estado | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 | Salida |
|---|---|---|---|---|---|---|---|---|---|
| CDA | CDO | CDO | CDA | × | ABDO | ABTA | ABDO | × | 00 |
| ABDO | ABDO | CDO | ABDO | × | ABDO | ABTA | ABDO | × | 01 |
| ABTA | CDO | CDO | CDO | × | ABDO | ABTA | ABDO | × | 00 |
| CDO | CDO | CDO | CDA | × | ABDO | ABTA | ABDO | × | 10 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| CDA | 00 | 00 |
| ABDO | 01 | 01 |
| ABTA | 11 | 00 |
| CDO | 10 | 10 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{1}$ | $\overline{P}\cdot \overline{C}\cdot \overline{q_{0}} + A$ |
| $K_{1}$ | $C\cdot \overline{q_{0}} + P\cdot \overline{A}$ |
| $J_{0}$ | $P$ |
| $K_{0}$ | $\overline{P}\cdot q_{1} + \overline{P}\cdot A$ |
| $S_{1}$ | $q_{1}\cdot \overline{q_{0}}$ |
| $S_{0}$ | $\overline{q_{1}}\cdot q_{0}$ |

**Historias**

| Historia | Entradas $PCA$ (desde el estado inicial) | Estados |
|---|---|---|
| Ciclo completo | 010, 110, 100, 000, 001, 000, 010 | CDA → ABDO → ABDO → ABDO → CDO → CDO → CDA |
| Con gente al final | 100, 100, 101, 001, 000, 010 | ABDO → ABDO → ABTA → CDO → CDO → CDA |
| Alguien aparece al cerrar | 100, 101, 001, 100, 101, 001, 010 | ABDO → ABTA → CDO → ABDO → ABTA → CDO → CDA |

El libro presenta este ejemplo sólo con el diagrama de estados y sus comentarios (sin ecuaciones); la tabla completa y las ecuaciones son las del método, y se han comprobado frente a las historias y a tres propiedades simuladas (abriendo no se detiene, cerrando con persona reabre, abierta con gente permanece abierta).
@end
@end

@ej lb8-23|Desvío de trenes: un tren corto o uno largo|Libro · Cap. 8 · P8.23|moore,industrial,jk,reduccion|lb8.p823
@enun
En una vía hay un desvío con dos ramales: $A$ (corto) y $B$ (largo). Dos sensores, $E_1$ a la entrada y $E_0$ a la salida del tramo de aguja (entradas ordenadas $E_1E_0$), dicen por dónde va el tren: si **sólo $E_1$** está activo y luego se libera, el tren es corto y pasa por $A$; si **$E_1$ y $E_0$ están activos a la vez**, el tren es largo y debe ir por $B$. La salida $AB$ posiciona la aguja: 10 es el ramal $A$ y 01 el $B$. Por defecto, la aguja está en $A$.
@end
@antes
**Dos soluciones: la «natural» y la mínima.** La primera sigue el recorrido de un tren y tiene cinco estados; pero en realidad lo único que importa es **dónde está la aguja**, y eso sólo necesita saber si hay un tren largo cruzando. Esa idea da dos estados y un único biestable.
@end
@paso Primera solución: cinco estados
NADA (sin trenes), ENTRA (el tren acaba de entrar), VIAA (tren corto, sale por $A$), SALEA (saliendo) y VIAB (tren largo). Las dos historias del libro se recorren como sigue: corto, NADA→ENTRA→VIAA→SALEA→NADA; largo, NADA→ENTRA→VIAB→VIAB→NADA. Los saltos no previstos («—») no pueden ocurrir físicamente y son indiferentes.
@end
@paso Segunda solución: dos estados
VIAA (salida 10) y VIAB (01). Sólo se pasa a VIAB cuando se ven **los dos sensores a la vez** (11); se vuelve a VIAA cuando ya no hay tren (00). Con un biestable $q_0$ ($0$ = VIAA, $1$ = VIAB): $J_0=E_1E_0$ y $K_0=\overline{E_0}$, y las salidas $A=\overline{q_0}$, $B=q_0$.
@end
@paso Equivalencia
Para todos los pasos de trenes posibles (cortos y largos, con pausas) la aguja se coloca **exactamente igual** en las dos soluciones: se han comparado 300 secuencias aleatorias de hasta cinco trenes.
@end
@paso Una pega del diseño
Tras pasar un tren largo, en cuanto los dos sensores quedan libres la aguja vuelve a $A$, aunque el tren aún pudiera estar saliendo del ramal. El libro sugiere dejar la salida en $B$ un poco más; es un ajuste de diseño, no un fallo.
@end
@res
**Cinco estados** (« — »: no puede ocurrir)

@fig fsm {"nodes": {"NADA": [85, 70, "10"], "ENTRA": [215, 70, "10"], "VIAA": [345, 70, "10"], "SALEA": [150, 190, "10"], "VIAB": [280, 190, "01"]}, "edges": [["NADA", "NADA", "00", 0], ["NADA", "ENTRA", "10", 0], ["ENTRA", "ENTRA", "10", 0], ["ENTRA", "VIAA", "00", 0], ["ENTRA", "VIAB", "11", 0], ["VIAA", "VIAA", "00", 0], ["VIAA", "SALEA", "01", 0], ["SALEA", "SALEA", "01", 0], ["SALEA", "NADA", "00", 0], ["VIAB", "VIAB", "01, 11", 0], ["VIAB", "NADA", "00", 0]], "W": 430, "H": 300, "title": "Desvío: cinco estados. Estado: salida AB"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| NADA | NADA | — | ENTRA | — | 10 |
| ENTRA | VIAA | — | ENTRA | VIAB | 10 |
| VIAA | VIAA | SALEA | — | — | 10 |
| SALEA | NADA | SALEA | — | — | 10 |
| VIAB | NADA | VIAB | — | VIAB | 01 |

**Dos estados**

@fig fsm {"nodes": {"VIAA": [85, 70, "10"], "VIAB": [215, 70, "01"]}, "edges": [["VIAA", "VIAA", "00, 01, 10", 0], ["VIAA", "VIAB", "11", 38], ["VIAB", "VIAA", "00", 38], ["VIAB", "VIAB", "01, 11", 0]], "W": 300, "H": 180, "title": "Desvío: dos estados"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| VIAA | VIAA | VIAA | VIAA | VIAB | 10 |
| VIAB | VIAA | VIAB | — | VIAB | 01 |

| Función | Ecuación |
|---|---|
| $J_{0}$ | $E_{1}\cdot E_{0}$ |
| $K_{0}$ | $\overline{E_{0}}$ |
| $S_{1}$ | $\overline{q_{0}}$ |
| $S_{0}$ | $q_{0}$ |

En ambas el comportamiento del libro (historias de arriba) se reproduce.

@box ojo | Errata en el libro
Las ecuaciones de salida impresas en el libro son $A=q_0$ y $B=\overline{q_0}$. Eso contradice la propia codificación (VIAA $=0$ debe dar $AB=10$, es decir $A=\overline{q_0}$ y $B=q_0$). Las ecuaciones de excitación $J_0$ y $K_0$ son correctas; las salidas están intercambiadas. Con las salidas impresas, el sistema colocaría la aguja en $B$ cuando no hay tren.
@end
@end
@end

@ej lb8-24|Secador de manos con pulsador y detector de presencia|Libro · Cap. 8 · P8.24|moore,industrial,jk|lb8.p824
@enun
Un secador de manos arranca cuando se pulsa un pulsador $P$ **y** el detector de presencia $D$ ve unas manos, y sigue funcionando mientras $D$ siga detectando. Entradas ordenadas $PD$. Diseña el autómata con un biestable J‑K.
@end
@antes
**Dos estados, PARO y MARCHA**, y el motor es el estado. La condición para arrancar es un AND ($P\cdot D$) y la de seguir es sólo $D$: el pulsador deja de importar una vez en marcha.
@end
@paso Tabla
En PARO sólo $PD=11$ lleva a MARCHA. En MARCHA se continúa con $D=1$ (01 y 11) y se para con $D=0$ (00 y 10), aunque se esté pulsando.
@end
@paso Ecuaciones
$J_0=P\cdot D$ (arranque), $K_0=\overline D$ (se apaga al dejar de detectar), $S_0=q_0$.
@end
@res
@fig fsm {"nodes": {"PARO": [85, 70, "0"], "MARCHA": [215, 70, "1"]}, "edges": [["PARO", "PARO", "00, 01, 10", 0], ["PARO", "MARCHA", "11", 38], ["MARCHA", "PARO", "00, 10", 38], ["MARCHA", "MARCHA", "01, 11", 0]], "W": 300, "H": 180, "title": "Secador (entradas PD)"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| PARO | PARO | PARO | PARO | MARCHA | 0 |
| MARCHA | PARO | MARCHA | PARO | MARCHA | 1 |

| Función | Ecuación |
|---|---|
| $J_{0}$ | $P\cdot D$ |
| $K_{0}$ | $\overline{D}$ |
| $S$ | $q_{0}$ |

Las dos historias del libro (arranque y parada normales; salir sin soltar el pulsador) se reproducen. Simulados 200 flujos de 40 pares $PD$ contra «el estado siguiente es $D\cdot(P+\text{estado})$».
@end
@end

@ej lb8-25|Contador módulo 4 que cuenta al pulsar (8 estados)|Libro · Cap. 8 · P8.25|moore,contador,industrial,jk|lb8.p825
@enun
Un contador módulo 4 debe avanzar **un solo paso cada vez que se pulsa** un pulsador $E_0$ (en el flanco de subida de la pulsación), por mucho que dure la pulsación. La salida son dos bits con la cuenta. Diseña el autómata de Moore.
@end
@antes
**Un pulsador humano dura muchos ciclos de reloj**, así que hay que distinguir «he contado ya esta pulsación» de «aún no». Por cada valor de la cuenta hay un estado estacionario $C_n$ (pulsador suelto) y otro transitorio $C_nT$ (pulsador mantenido tras haber contado). Son ocho estados.
@end
@paso Transiciones
$C_n\xrightarrow{0}C_n$; $C_n\xrightarrow{1}C_{n+1}T$ (cuenta al pulsar y pasa a esperar). $C_nT\xrightarrow{1}C_nT$ (mantiene) y $C_nT\xrightarrow{0}C_n$ (se suelta).
@end
@paso Salida
Tanto $C_n$ como $C_nT$ dan el valor $n$.
@end
@paso Codificación y ecuaciones
Los estacionarios son 000 a 011 y los transitorios 100 a 111 ($q_2$ = «ya contado»). $J_2=E_0$, $K_2=\overline{E_0}$ (es una copia retrasada del pulsador). Los otros dos biestables **conmutan** sólo en el instante de la pulsación, es decir cuando $E_0=1$ y $q_2=0$: $J_0=K_0=E_0\overline{q_2}$ y $J_1=K_1=E_0\overline{q_2}q_0$ (el bit alto cambia si el bajo es 1).
@end
@res
@fig fsm {"nodes": {"C0": [85, 70, "00"], "C1": [215, 70, "01"], "C2": [345, 70, "10"], "C3": [475, 70, "11"], "C0T": [85, 190, "00"], "C1T": [215, 190, "01"], "C2T": [345, 190, "10"], "C3T": [475, 190, "11"]}, "edges": [["C0", "C0", "0", 0], ["C0", "C1T", "1", 0], ["C1", "C1", "0", 0], ["C1", "C2T", "1", 0], ["C2", "C2", "0", 0], ["C2", "C3T", "1", 0], ["C3", "C3", "0", 0], ["C3", "C0T", "1", 0], ["C0T", "C0", "0", 0], ["C0T", "C0T", "1", 0], ["C1T", "C1", "0", 0], ["C1T", "C1T", "1", 0], ["C2T", "C2", "0", 0], ["C2T", "C2T", "1", 0], ["C3T", "C3", "0", 0], ["C3T", "C3T", "1", 0]], "W": 560, "H": 300, "title": "Contador con pulsador. Etiqueta: E0; estado: cuenta"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| C0 | C0 | C1T | 00 |
| C1 | C1 | C2T | 01 |
| C2 | C2 | C3T | 10 |
| C3 | C3 | C0T | 11 |
| C0T | C0 | C0T | 00 |
| C1T | C1 | C1T | 01 |
| C2T | C2 | C2T | 10 |
| C3T | C3 | C3T | 11 |

| Estado | Código $q_2q_1q_0$ | Salida |
|---|---|---|
| C0 | 000 | 00 |
| C1 | 001 | 01 |
| C2 | 010 | 10 |
| C3 | 011 | 11 |
| C0T | 100 | 00 |
| C1T | 101 | 01 |
| C2T | 110 | 10 |
| C3T | 111 | 11 |

| Función | Ecuación |
|---|---|
| $J_{2}$ | $E_{0}$ |
| $K_{2}$ | $\overline{E_{0}}$ |
| $J_{1}$ | $E_{0}\cdot \overline{q_{2}}\cdot q_{0}$ |
| $K_{1}$ | $E_{0}\cdot \overline{q_{2}}\cdot q_{0}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{2}}$ |
| $K_{0}$ | $E_{0}\cdot \overline{q_{2}}$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

Mi minimización coincide con la del libro como función. Simulados 300 flujos aleatorios de 40 entradas contra «número de flancos de subida, módulo 4».

@box ojo | Errata en el libro
En el diagrama del libro el estado $C_2T$ aparece rotulado con la salida 01; debe ser 10, como indican la tabla de estados y el funcionamiento (cuenta 2). Se ha comprobado que con 01 el contador daría 1 en vez de 2 en ese estado.
@end
@end
@end

@ej lb8-26|Caja fuerte con combinación 1‑1‑0 y alarma|Libro · Cap. 8 · P8.26|moore,industrial,jk|lb8.p826
@enun
Una caja fuerte tiene dos pulsadores, $P_1$ y $P_0$ (entradas ordenadas $P_1P_0$, nivel alto al pulsar). Se abre al introducir la **combinación 1, 1, 0** (pulsar $P_1$, pulsar $P_1$, pulsar $P_0$; entre una pulsación y la siguiente hay que soltar). Cualquier pulsación equivocada dispara la **alarma**. Salidas $CA$: $C$ abre la caja, $A$ activa la alarma. Un RESET asíncrono la devuelve al estado inicial. Pulsar los dos a la vez es imposible.
@end
@antes
**Cada pulsación correcta es un par de estados**: «el botón está apretado» (esperando soltar) y «ya se ha aceptado» (esperando el siguiente). Eso da una cadena $Q_0\to Q_1\to S_1\to Q_3\to S_{11}\to Q_6\to S_{110}$, y de cada estado de espera un botón equivocado lleva a ALARM. Tanto la apertura como la alarma son **absorbentes**: sólo se sale con el RESET.
@end
@paso Cadena de aciertos
En $Q_0$ se espera un 1 (10 → $Q_1$); mientras se mantiene (10) se queda; al soltar (00) pasa a $S_1$ («un 1 aceptado»). Lo mismo para el segundo 1 ($S_1\to Q_3\to S_{11}$). En $S_{11}$ se espera el 0 (01 → $Q_6$), y al soltar se llega a $S_{110}$ (abierta, salida 10).
@end
@paso Errores
En $Q_0$ y en $S_1$ una pulsación de $P_0$ (01) es un error; en $S_{11}$ lo es una de $P_1$ (10). Esos tres saltos van a ALARM (salida 01).
@end
@paso Estados de la cadena
Los estados $Q_1$, $Q_3$ y $Q_6$ son los de «botón apretado». Con las entradas posibles, no se puede pasar de 10 a 01 de golpe (habría que soltar primero), por lo que algunas casillas quedan como indiferentes.
@end
@res
@fig fsm {"nodes": {"Q0": [85, 70, "00"], "Q1": [215, 70, "00"], "S1": [345, 70, "00"], "Q3": [475, 70, "00"], "S11": [85, 190, "00"], "Q6": [215, 190, "00"], "S110": [345, 190, "10"], "ALARM": [475, 190, "01"]}, "edges": [["Q0", "Q0", "00", 0], ["Q0", "Q1", "10", 0], ["Q0", "ALARM", "01", 0], ["Q1", "Q1", "10", 0], ["Q1", "S1", "00", 0], ["S1", "S1", "00", 0], ["S1", "Q3", "10", 0], ["S1", "ALARM", "01", 0], ["Q3", "Q3", "10", 0], ["Q3", "S11", "00", 0], ["S11", "S11", "00", 0], ["S11", "Q6", "01", 0], ["S11", "ALARM", "10", 70], ["Q6", "Q6", "01", 0], ["Q6", "S110", "00", 0], ["S110", "S110", "XX", 0], ["ALARM", "ALARM", "XX", 0]], "W": 560, "H": 300, "title": "Caja fuerte (entradas P1P0). Estado: salida CA"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| Q0 | Q0 | ALARM | Q1 | × | 00 |
| Q1 | S1 | — | Q1 | × | 00 |
| S1 | S1 | ALARM | Q3 | × | 00 |
| Q3 | S11 | — | Q3 | × | 00 |
| S11 | S11 | Q6 | ALARM | × | 00 |
| Q6 | S110 | Q6 | — | × | 00 |
| S110 | S110 | S110 | S110 | × | 10 |
| ALARM | ALARM | ALARM | ALARM | × | 01 |

| Estado | Código $q_2q_1q_0$ | Salida |
|---|---|---|
| Q0 | 000 | 00 |
| Q1 | 001 | 00 |
| S1 | 010 | 00 |
| Q3 | 011 | 00 |
| S11 | 100 | 00 |
| Q6 | 101 | 00 |
| S110 | 110 | 10 |
| ALARM | 111 | 01 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{2}$ | $\overline{P_{1}}\cdot q_{1}\cdot q_{0} + P_{0}$ |
| $K_{2}$ | $0$ |
| $J_{1}$ | $\overline{P_{1}}\cdot \overline{P_{0}}\cdot q_{0} + P_{0}\cdot \overline{q_{2}} + P_{1}\cdot q_{2}$ |
| $K_{1}$ | $\overline{P_{1}}\cdot \overline{q_{2}}\cdot q_{0}$ |
| $J_{0}$ | $P_{0}\cdot \overline{q_{2}} + P_{0}\cdot \overline{q_{1}} + P_{1}\cdot \overline{q_{2}} + P_{1}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $\overline{P_{1}}\cdot \overline{P_{0}}\cdot \overline{q_{1}} + \overline{P_{1}}\cdot \overline{q_{2}}$ |
| $S_{1}$ | $q_{2}\cdot q_{1}\cdot \overline{q_{0}}$ |
| $S_{0}$ | $q_{2}\cdot q_{1}\cdot q_{0}$ |

Historia de apertura correcta: pulsar 1, soltar, pulsar 1, soltar, pulsar 0, soltar → $Q_1,S_1,Q_3,S_{11},Q_6,S_{110}$. Simulados 400 intentos aleatorios (combinación correcta, incompleta, con errores y con pulsaciones de más): el resultado siempre es «abierta» sólo con 1‑1‑0 y «alarma» con cualquier otro primer error. El libro presenta este ejemplo con el diagrama y las historias; las ecuaciones de arriba son las del método.
@end
@end

@ej lb8-27|Juego de reflejos entre dos jugadores (con juez)|Libro · Cap. 8 · P8.27|moore,industrial,jk|lb8.p827
@enun
Dos jugadores, $A$ y $B$, tienen un pulsador cada uno ($E_1$ y $E_0$). Gana el que pulse primero; si pulsan a la vez, hay empate. Salidas $S_1S_0$: 10 gana $A$, 01 gana $B$, 11 empate. Diseña el autómata. Después mejóralo: un **juez** da la orden de salida con un pulsador $J$ (hay una luz $L_J$ encendida durante la partida), quien pulse **antes** de la orden pierde, y un pulsador de **inicio** $I$ prepara una nueva partida.
@end
@antes
**Versión simple: cuatro estados.** INICIO y tres estados absorbentes (GA, GB, GT) que registran el resultado. Su problema es doble: sólo se reinicia con RESET y se puede hacer trampa pulsando antes de empezar. La versión con juez lo resuelve añadiendo estados.
@end
@paso Versión simple
INICIO/00: con 00 espera; con 10 gana A, con 01 gana B, con 11 empate. Una vez decidido, el resultado se mantiene (la «X» de la flecha: cualquier entrada). Con el código INICIO $=00$, GB $=01$, GA $=10$, GT $=11$ las salidas son $S=q$ (sin lógica de salida).
@end
@paso Versión con juez
Entradas $I\,J\,E_1E_0$ y salidas $L_JS_1S_0$. Estados: REPOS (espera el primer inicio), INICIO (preparado, sin luz), JUGAN (juez ha dado la orden, luz encendida), PIERA y PIERB (un jugador pulsó antes de la orden y **pierde**: gana el otro), PIERT (los dos pulsaron antes), y GANA, GANB y GANT (resultado válido).
@end
@paso Reglas
En INICIO: sólo $J=1$ solo (0100) pasa a JUGAN; si un jugador pulsa sin que el juez haya dado la orden, pierde (PIERA con 0010, PIERB con 0001, PIERT con 0011); si la orden y la pulsación coinciden se acepta la pulsación (0110, 0101, 0111). En JUGAN el primero que pulse gana (0X10, 0X01, 0X11). Cualquier estado de resultado se mantiene hasta que $I=1$ lo devuelve a INICIO.
@end
@paso Sobre REPOS
REPOS sólo se usa después del RESET: se sale con $I=1$ y no se vuelve a entrar, porque los reinicios llevan a INICIO. El libro comenta que podría eliminarse.
@end
@res
**Versión simple**

@fig fsm {"nodes": {"INICIO": [85, 70, "00"], "GA": [215, 70, "10"], "GB": [345, 70, "01"], "GT": [475, 70, "11"]}, "edges": [["INICIO", "INICIO", "00", 0], ["INICIO", "GA", "10", 0], ["INICIO", "GB", "01", -70], ["INICIO", "GT", "11", -70], ["GA", "GA", "XX", 0], ["GB", "GB", "XX", 0], ["GT", "GT", "XX", 0]], "W": 560, "H": 180, "title": "Juego simple (entradas E1E0)"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| INICIO | INICIO | GB | GA | GT | 00 |
| GA | GA | GA | GA | GA | 10 |
| GB | GB | GB | GB | GB | 01 |
| GT | GT | GT | GT | GT | 11 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| INICIO | 00 | 00 |
| GA | 10 | 10 |
| GB | 01 | 01 |
| GT | 11 | 11 |

| Función | Ecuación (mía) |
|---|---|
| $J_{1}$ | $E_{1}\cdot \overline{q_{0}}$ |
| $K_{1}$ | $0$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $0$ |
| $S_{1}$ | $q_{1}$ |
| $S_{0}$ | $q_{0}$ |

**Versión con juez** (9 estados; entradas $I\,J\,E_1E_0$; estado: salida $L_JS_1S_0$)

| Estado | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 | 1000 | 1001 | 1010 | 1011 | 1100 | 1101 | 1110 | 1111 | Salida |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REPOS | REPOS | REPOS | REPOS | REPOS | REPOS | REPOS | REPOS | REPOS | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 000 |
| INICIO | INICIO | PIERB | PIERA | PIERT | JUGAN | GANB | GANA | GANT | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 000 |
| JUGAN | JUGAN | GANB | GANA | GANT | JUGAN | GANB | GANA | GANT | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 100 |
| PIERA | PIERA | PIERA | PIERA | PIERA | PIERA | PIERA | PIERA | PIERA | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 001 |
| PIERB | PIERB | PIERB | PIERB | PIERB | PIERB | PIERB | PIERB | PIERB | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 010 |
| PIERT | PIERT | PIERT | PIERT | PIERT | PIERT | PIERT | PIERT | PIERT | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 011 |
| GANA | GANA | GANA | GANA | GANA | GANA | GANA | GANA | GANA | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 110 |
| GANB | GANB | GANB | GANB | GANB | GANB | GANB | GANB | GANB | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 101 |
| GANT | GANT | GANT | GANT | GANT | GANT | GANT | GANT | GANT | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | INICIO | 111 |

Historia completa del libro: REPOS → INICIO → INICIO → JUGAN → JUGAN → GANA → GANA → INICIO, con salidas 000, 000, 000, 100, 100, 110, 110, 000. Gana B: 000, 000, 000, 100, 100, 101, 000. Pulsa A antes de la orden: PIERA con salida 001. Empate: GANT con salida 111. Se ha comprobado que desde cualquier estado $I=1$ lleva a INICIO. El libro no desarrolla ecuaciones de la versión con juez (cuatro biestables), que quedan como ejercicio.

@box ojo | Errata en el libro
En las historias y en el diagrama de la versión con juez hay varias erratas: (1) la historia anota «Gana B» con salida 110; la salida de GANB es 101. (2) El diagrama rotula PIER A con salida 010 y PIER B con 001, al revés que la historia y el texto: si $A$ se adelanta, gana $B$, y el código es 001 para PIERA. (3) La última historia anota el reinicio con entrada 0000; debe ser 1000 (el pulsador de inicio). Aquí se usan las salidas correctas.
@end
@end
@end

@ej lb8-28|Alarma de sobrecarga de un ascensor (peso en serie… de tres bits)|Libro · Cap. 8 · P8.28|moore,industrial,jk,contador|lb8.p828
@enun
Un sensor de peso entrega el peso del ascensor en tres bits $E_2E_1E_0$ (valor de 0 a 7). Debe sonar una **alarma** si el peso es **5 durante al menos 4 pulsos de reloj consecutivos**, **6 durante al menos 2** o **7 durante al menos 1**. Cualquier otro valor (0 a 4) borra la cuenta. Diseña el autómata de Moore.
@end
@antes
**El autómata cuenta cuántos pulsos seguidos lleva el mismo peso crítico.** Para el 5 se cuenta hasta 4, para el 6 hasta 2 y el 7 se detecta ya a la primera, así que hay ocho estados: INICI (nada), P51 a P54 (lleva 1, 2, 3 y 4 o más pulsos con peso 5), P61 y P62 (1 y 2 o más con peso 6) y P7. La alarma está en P54, P62 y P7.
@end
@paso Transiciones
Con peso de 0 a 4 se vuelve siempre a INICI. Con peso 5 se avanza P51→P52→P53→P54 (que se mantiene); desde cualquier otro estado (incluidos P6x y P7) se empieza una cuenta nueva en P51. Con peso 6 se avanza P61→P62 y desde el resto se entra en P61. Con peso 7 se va a P7 desde cualquier estado.
@end
@paso Qué significa «seguidos»
Es la cuenta de **pulsos consecutivos con exactamente el mismo peso**: si entre dos pesos 5 aparece un 6, la cuenta de 5 se pierde (y al volver el 5 se parte de 1). Es una decisión de diseño razonable, pero conviene saberla: tres pesos 5 seguidos de un 6 no dan alarma por ninguno de los dos.
@end
@paso Codificación
Natural: INICI $=000$, P51 $=001$, …, P54 $=100$, P61 $=101$, P62 $=110$, P7 $=111$. La salida es $S_0=q_2\overline{q_0}+q_2q_1$.
@end
@res
| Estado | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 | Salida |
|---|---|---|---|---|---|---|---|---|---|
| INICI | INICI | INICI | INICI | INICI | INICI | P51 | P61 | P7 | 0 |
| P51 | INICI | INICI | INICI | INICI | INICI | P52 | P61 | P7 | 0 |
| P52 | INICI | INICI | INICI | INICI | INICI | P53 | P61 | P7 | 0 |
| P53 | INICI | INICI | INICI | INICI | INICI | P54 | P61 | P7 | 0 |
| P54 | INICI | INICI | INICI | INICI | INICI | P54 | P61 | P7 | 1 |
| P61 | INICI | INICI | INICI | INICI | INICI | P51 | P62 | P7 | 0 |
| P62 | INICI | INICI | INICI | INICI | INICI | P51 | P62 | P7 | 1 |
| P7 | INICI | INICI | INICI | INICI | INICI | P51 | P61 | P7 | 1 |

| Función | Ecuación (libro) |
|---|---|
| $J_{2}$ | $E_{2}\cdot E_{0}\cdot q_{1}\cdot q_{0}  +  E_{2}\cdot E_{1}$ |
| $K_{2}$ | $\overline{E_{1}}\cdot \overline{E_{0}}  +  \overline{E_{1}}\cdot q_{0}  +  \overline{E_{1}}\cdot q_{1}  +  \overline{E_{2}}$ |
| $J_{1}$ | $E_{2}\cdot E_{0}\cdot \overline{q_{2}}\cdot q_{0}  +  E_{2}\cdot E_{1}\cdot q_{2}\cdot q_{0}  +  E_{2}\cdot E_{1}\cdot E_{0}$ |
| $K_{1}$ | $\overline{E_{0}}\cdot \overline{q_{2}}  +  \overline{E_{1}}\cdot q_{0}  +  \overline{E_{1}}\cdot q_{2}  +  \overline{E_{2}}  +  \overline{E_{0}}\cdot q_{0}$ |
| $J_{0}$ | $E_{2}\cdot E_{0}\cdot \overline{q_{2}}  +  E_{2}\cdot E_{0}\cdot q_{1}  +  E_{2}\cdot E_{1}\cdot \overline{q_{1}}  +  E_{2}\cdot E_{1}\cdot \overline{q_{2}}$ |
| $K_{0}$ | $\overline{E_{0}}\cdot q_{2}\cdot \overline{q_{1}}  +  \overline{E_{1}}\cdot \overline{q_{2}}  +  \overline{E_{1}}\cdot \overline{E_{0}}  +  \overline{E_{2}}$ |
| $S$ | $q_{2}\cdot \overline{q_{0}}  +  q_{2}\cdot q_{1}$ |

Salida: $S_0=q_2\overline{q_0}+q_2q_1$. Mi propia minimización coincide con ellas como función.

Las ecuaciones del libro (suma de productos) se han comprobado en las 64 transiciones: todas reproducen la tabla. Se ha simulado con 400 secuencias de 40 pesos, muchas de ellos críticos, contra el modelo directo «longitud de la racha de pesos iguales». También se reproduce la historia del libro: tres pesos bajos, luego cinco veces el 5 (con alarma al cuarto) y vuelta a INICI con el 2.
@end
@end

@ej lb8-29|Dispensador de leche con calentador (Moore, 10 estados)|Libro · Cap. 8 · P8.29|moore,industrial,secuencial|lb8.p829
@enun
Una máquina dispensa leche cuando se pulsa un pulsador $P$, **al soltarlo**. Durante cuatro segundos sale la leche y se recarga el depósito; después, durante otros cuatro segundos, se calienta la leche. En las ocho fases la máquina está ocupada y **no atiende nuevas pulsaciones**. Cuatro salidas $D\,R\,C\,L_R$: dispensador, recargador, calentador y led rojo de ocupado ($L_R$, a 1 durante las ocho fases). Hay un reloj de 1 Hz. Diseña el autómata de Moore.
@end
@antes
**Es una secuencia temporizada disparada por un pulsador:** una espera, una confirmación de que se soltó y ocho pasos de reloj fijos. Con un reloj de 1 Hz cada paso dura un segundo, así que se necesitan 4 estados para la fase de dispensar y 4 para la de calentar. Más los dos de espera: **10 estados**.
@end
@paso Esperar y confirmar
INICIO (todo a 0): con $P=1$ pasa a TRANS; TRANS espera a que se suelte ($P=0$) y entonces arranca el ciclo. Esto evita arrancar al pulsar y permite pulsaciones largas.
@end
@paso Dispensar y calentar
D1, D2, D3 y D4 con salidas 1101 ($D=R=L_R=1$), y C1, C2, C3 y C4 con salidas 0011 ($C=L_R=1$). En cada uno se pasa al siguiente con cualquier entrada (la «X»: no se atiende el pulsador durante el ciclo). Tras C4 se vuelve a INICIO.
@end
@paso Reducción
No se puede fusionar ningún par: los ocho estados del ciclo están a distancias distintas del final, y INICIO y TRANS difieren en cómo reaccionan a $P$. El algoritmo de particiones confirma que el autómata es mínimo.
@end
@res
| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | INICIO | TRANS | 0000 |
| TRANS | D1 | TRANS | 0000 |
| D1 | D2 | D2 | 1101 |
| D2 | D3 | D3 | 1101 |
| D3 | D4 | D4 | 1101 |
| D4 | C1 | C1 | 1101 |
| C1 | C2 | C2 | 0011 |
| C2 | C3 | C3 | 0011 |
| C3 | C4 | C4 | 0011 |
| C4 | INICIO | INICIO | 0011 |

El libro presenta sólo el diagrama y los comentarios, sin ecuaciones (cuatro biestables para 10 estados). Se ha simulado el funcionamiento: tras soltar el pulsador salen exactamente cuatro ciclos 1101, luego cuatro 0011 y se vuelve a 0000, sin importar lo que valga $P$ durante esos ocho ciclos (200 casos aleatorios).
@end
@end

@ej lb8-30|Barrera de un garaje (Moore, entradas SE SS SA SC)|Libro · Cap. 8 · P8.30|moore,industrial,jk|lb8.p830
@enun
Una barrera de garaje tiene cuatro sensores, ordenados $S_E\,S_S\,S_A\,S_C$: coche en la **entrada** (antes de la barrera), coche en la **salida** (ya pasó), barrera **abierta** y barrera **cerrada**. La orden al motor son dos bits $M_1M_0$: 00 parado, 01 abre, 10 cierra. Debe abrirse cuando llega un coche, esperar abierta hasta que haya pasado y cerrarse. $S_E$ y $S_S$ no pueden valer 1 a la vez, ni $S_A$ y $S_C$.
@end
@antes
**Cuatro estados de la barrera:** REPOS (cerrada y parada), ABDO (abriéndose), ABTO (abierta, parada, esperando que el coche pase) y CDO (cerrándose). De las 16 entradas quedan 9 posibles: se descartan 11XX y XX11.
@end
@paso Transiciones que dibuja el libro
REPOS con $S_E=1$ pasa a ABDO; ABDO se mantiene (1001, 1000, 0000) hasta que se completa la apertura (1010 → ABTO) o el coche ya ha pasado (0100, 0110 → CDO); ABTO se mantiene con 1010; CDO se mantiene (0010, 0110, 0100) y llega a REPOS con 0001.
@end
@paso Cómo se completan
ABDO: si $S_S=1$ (el coche ya pasó) cierra; si no, con $S_A=1$ queda abierta. ABTO: sale a CDO cuando el coche pasa ($S_S=1$). CDO: con $S_C=1$ llega a REPOS. REPOS: sólo $S_E$ la saca de ahí. Así quedan cubiertas las nueve combinaciones posibles de cada estado y se reproducen las dos historias del libro.
@end
@res
| Estado | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 | 1000 | 1001 | 1010 | 1011 | 1100 | 1101 | 1110 | 1111 | Salida |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REPOS | REPOS | REPOS | REPOS | × | REPOS | REPOS | REPOS | × | ABDO | ABDO | ABDO | × | × | × | × | × | 00 |
| ABDO | ABDO | ABDO | ABTO | × | CDO | CDO | CDO | × | ABDO | ABDO | ABTO | × | × | × | × | × | 01 |
| ABTO | ABTO | ABTO | ABTO | × | CDO | CDO | CDO | × | ABTO | ABTO | ABTO | × | × | × | × | × | 00 |
| CDO | CDO | REPOS | CDO | × | CDO | REPOS | CDO | × | CDO | REPOS | CDO | × | × | × | × | × | 10 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| REPOS | 00 | 00 |
| ABDO | 01 | 01 |
| ABTO | 11 | 00 |
| CDO | 10 | 10 |

| Función | Ecuación (mía, mínima) |
|---|---|
| $J_{1}$ | $\mathrm{SA}\cdot q_{0} + \mathrm{SS}\cdot q_{0}$ |
| $K_{1}$ | $\mathrm{SC}\cdot \overline{q_{0}}$ |
| $J_{0}$ | $\mathrm{SE}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $\mathrm{SS}$ |
| $S_{1}$ | $q_{1}\cdot \overline{q_{0}}$ |
| $S_{0}$ | $\overline{q_{1}}\cdot q_{0}$ |

Historia 1: REPOS, ABDO, ABDO, ABDO, CDO, CDO, CDO, REPOS. Historia 2 (coche que se adelanta con la barrera a medias, abierta del todo, pasa y cierra): REPOS, ABDO, ABDO, ABDO, ABDO, ABDO, ABDO, ABTO, CDO, CDO, CDO, REPOS.

El libro no da ecuaciones de este problema (sólo diagrama y comentarios). Las de arriba se derivan con el método general y se han comprobado.

@box ojo | Errata en el libro
Las flechas del diagrama no son coherentes con las historias del propio libro: el dibujo rotula con 1010 la salida de ABDO a ABTO y con 0010 la de ABTO a CDO, pero en las historias se llega a ABTO con 0010 (paso 10) y se pasa a CDO con 0110 (paso 11). Aquí se usa la tabla que cumple las historias (la que sale arriba).
@end
@end
@end

@ej lb8-31|Calificaciones recibidas en serie (Moore, 10 → 9 estados)|Libro · Cap. 8 · P8.31|moore,reduccion,serie|lb8.p831
@enun
Un sistema de corrección entrega la nota de cada examen en **tres bits seguidos** por una línea serie $E$: el primero dice si se supera la parte básica (BAS), el segundo si se llega a notable (NOT) y el tercero si se llega a sobresaliente (SOB). Interpretación: $0XX$ suspenso, $10X$ aprobado, $110$ notable y $111$ sobresaliente. Hay tres luces $L_AL_NL_S$ (aprobado, notable, sobresaliente) que se encienden **al llegar el tercer bit**. Diseña el autómata de Moore y reduce sus estados.
@end
@antes
**Hay que contar tres bits aunque no importen.** En un suspenso, el primer bit (0) decide, pero hay que dejar pasar los otros dos antes de aceptar el examen siguiente; por eso aparecen cadenas de estados «de relleno» (SUSP1, SUSP2, SUSP3 y APRO1, APRO2).
@end
@paso Estados
Suspenso: INICIO, SUSP1, SUSP2, SUSP3 (cuentan 3 bits sin salida). Aprobado: EMPIE, APRO1, APRO2 (luz $L_A$). Notable/sobresaliente: SIGUE (ha llegado «11»), NOTAB ($L_N$) y SOBRE ($L_S$). Desde los estados finales (SUSP3, APRO2, NOTAB, SOBRE) el siguiente bit es el primero de otro examen.
@end
@paso Reducción
INICIO y SUSP3 son **equivalentes**: la misma salida (000) y los mismos siguientes (0→SUSP1, 1→EMPIE). Se fusionan y quedan **nueve estados** (cuatro biestables). El algoritmo de particiones no encuentra más.
@end
@res
**Con diez estados**

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | SUSP1 | EMPIE | 000 |
| SUSP1 | SUSP2 | SUSP2 | 000 |
| SUSP2 | SUSP3 | SUSP3 | 000 |
| SUSP3 | SUSP1 | EMPIE | 000 |
| EMPIE | APRO1 | SIGUE | 000 |
| APRO1 | APRO2 | APRO2 | 000 |
| APRO2 | SUSP1 | EMPIE | 100 |
| SIGUE | NOTAB | SOBRE | 000 |
| NOTAB | SUSP1 | EMPIE | 010 |
| SOBRE | SUSP1 | EMPIE | 001 |

**Reducido a nueve** (INICIO y SUSP3 fusionados)

@fig fsm {"nodes": {"INICIO": [85, 70, "000"], "SUSP1": [215, 70, "000"], "SUSP2": [345, 70, "000"], "EMPIE": [85, 190, "000"], "APRO1": [215, 190, "000"], "APRO2": [345, 190, "100"], "SIGUE": [85, 310, "000"], "NOTAB": [215, 310, "010"], "SOBRE": [345, 310, "001"]}, "edges": [["INICIO", "SUSP1", "0", 0], ["INICIO", "EMPIE", "1", 0], ["SUSP1", "SUSP2", "X", 0], ["SUSP2", "INICIO", "X", -70], ["EMPIE", "APRO1", "0", 0], ["EMPIE", "SIGUE", "1", 0], ["APRO1", "APRO2", "X", 0], ["APRO2", "SUSP1", "0", 0], ["APRO2", "EMPIE", "1", 70], ["SIGUE", "NOTAB", "0", 0], ["SIGUE", "SOBRE", "1", 70], ["NOTAB", "SUSP1", "0", 0], ["NOTAB", "EMPIE", "1", 0], ["SOBRE", "SUSP1", "0", 0], ["SOBRE", "EMPIE", "1", 0]], "W": 430, "H": 420, "title": "Calificaciones (9 estados). Etiqueta: E; estado: LALNLS"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | SUSP1 | EMPIE | 000 |
| SUSP1 | SUSP2 | SUSP2 | 000 |
| SUSP2 | INICIO | INICIO | 000 |
| EMPIE | APRO1 | SIGUE | 000 |
| APRO1 | APRO2 | APRO2 | 000 |
| APRO2 | SUSP1 | EMPIE | 100 |
| SIGUE | NOTAB | SOBRE | 000 |
| NOTAB | SUSP1 | EMPIE | 010 |
| SOBRE | SUSP1 | EMPIE | 001 |

Simulados 300 flujos de entre 1 y 6 exámenes de tres bits aleatorios: las luces se encienden sólo tras el tercer bit y con el resultado correcto; las dos versiones se comportan igual. El libro desarrolla este ejemplo con diagrama y sin ecuaciones.
@end
@end

@ej lb8-32|Generar un reloj CK′ cuyo primer flanco tras CLEAR sea ascendente|Libro · Cap. 8 · P8.32|moore,reloj,industrial|lb8.p832
@enun
Se quiere generar a partir de un reloj $CK$ y una señal $CLEAR$ un reloj $CK'$ que, al activarse $CLEAR$ (nivel alto), se ponga a 0 y, tras liberarse, **empiece siempre con un flanco ascendente**: nunca debe aparecer un flanco o un pulso incompleto aunque $CLEAR$ se suelte con $CK=1$. Entradas $CLEAR\,CK$, salida $CK'$. Diseña el autómata.
@end
@antes
**Hay que esperar a ver un 0 de $CK$ antes de seguir al reloj.** Si $CLEAR$ se libera cuando $CK$ vale 1 y se copiara $CK$ sin más, saldría un pulso recortado. Basta un estado de espera (ACTIV) que no copie $CK$ hasta que $CK=0$.
@end
@paso Estados
INICIO: sin activar (sólo $CLEAR=1$ lo saca de ahí). ACTIV: $CLEAR$ aplicado; espera un 0 de $CK$ (con $CK=1$ se queda). CK0 y CK1: reproducen $CK$ (salida 0 y 1).
@end
@paso Transiciones
ACTIV con $CLEAR=0$ y $CK=0$ pasa a CK0. CK0 pasa a CK1 con $CK=1$ y CK1 a CK0 con $CK=0$. En CK0, CK1 y ACTIV, $CLEAR=1$ lleva (y mantiene) en ACTIV, con la salida a 0.
@end
@paso Garantía
Como se llega a CK0 antes que a CK1, el primer cambio de la salida es siempre $0\to1$, un flanco ascendente. Se ha comprobado en 300 secuencias aleatorias.
@end
@paso Ojo con el uso
Una señal generada así no debería usarse como reloj de otros biestables: es una señal derivada de un autómata y rompe el principio de no mezclar relojes. Es preferible usar el $CK$ original con una entrada de habilitación (**ENABLE**).
@end
@res
@fig fsm {"nodes": {"INICIO": [85, 70, "0"], "ACTIV": [215, 70, "0"], "CK0": [345, 70, "0"], "CK1": [475, 70, "1"]}, "edges": [["INICIO", "INICIO", "0X", 0], ["INICIO", "ACTIV", "1X", 0], ["ACTIV", "ACTIV", "01, 1X", 0], ["ACTIV", "CK0", "00", 38], ["CK0", "CK0", "00", 0], ["CK0", "CK1", "01", 38], ["CK0", "ACTIV", "1X", 38], ["CK1", "CK1", "01", 0], ["CK1", "CK0", "00", 38], ["CK1", "ACTIV", "1X", -70]], "W": 560, "H": 180, "title": "Generador de CK′ (entradas CLEAR CK). Estado: salida CK'"}

| Estado | 00 | 01 | 10 | 11 | Salida |
|---|---|---|---|---|---|
| INICIO | INICIO | INICIO | ACTIV | ACTIV | 0 |
| ACTIV | CK0 | ACTIV | ACTIV | ACTIV | 0 |
| CK0 | CK0 | CK1 | ACTIV | ACTIV | 0 |
| CK1 | CK0 | CK1 | ACTIV | ACTIV | 1 |

Simulados 400 flujos de 40 pares $CLEAR\,CK$ contra el modelo «0 hasta que haya habido un CLEAR y después un 0 de $CK$; a partir de ahí, la salida es $CK$». El libro presenta sólo el diagrama y los comentarios.
@end
@end

@ej lb8-33|Un pulso de un ciclo de reloj por cada pulso de entrada (3 variantes)|Libro · Cap. 8 · P8.33|moore,detector-de-flanco,jk,cronograma|lb8.p833
@enun
Una señal $E_0$, manual y mucho más lenta que el reloj (cada nivel dura **más de un periodo** de reloj), debe generar **un pulso de exactamente un ciclo de reloj**. Diséñalo de tres maneras: (1) que el pulso aparezca al **subir** $E_0$, (2) al **bajar**, (3) en **los dos** flancos (dos pulsos por cada pulso de entrada). Autómatas de Moore con J‑K.
@end
@antes
**Es un detector de flancos síncrono.** Un flanco no es un nivel: es un cambio. El autómata debe recordar dos cosas: que ya vio el flanco (para no repetir el pulso aunque $E_0$ siga a 1) y, en los dos últimos casos, qué nivel tenía $E_0$.
@end
@paso Opción 1: flanco de subida
INICIO (espera un 1) → PULSO (salida 1, dura un ciclo) → FINAL (espera a que $E_0$ baje, sin repetir). Código 00, 01, 10 y $S_0=q_0$. Ecuaciones: $J_1=q_0$, $K_1=\overline{E_0}$, $J_0=E_0\overline{q_1}$, $K_0=1$.
@end
@paso Opción 2: flanco de bajada
INICIO → EMPIE (hay un 1; espera que baje) → PULSO (salida 1) → INICIO. Código 00, 01, 10 y $S_0=q_1$. Ecuaciones: $J_1=\overline{E_0}q_0$, $K_1=1$, $J_0=E_0\overline{q_1}$, $K_0=\overline{E_0}$.
@end
@paso Opción 3: los dos flancos
INICIO → PULS1 (salida 1) → MANT (mantiene el nivel alto) → PULS0 (salida 1, tras caer) → INICIO. Código 00, 01, 10 y 11, con $S_0=q_0$. Ecuaciones: $J_1=K_1=q_0$, $J_0=E_0\overline{q_1}+\overline{E_0}q_1$, $K_0=1$.
@end
@paso Por qué se exige un nivel mayor que un periodo
El autómata sólo mira $E_0$ una vez por ciclo. Si el pulso de entrada durara menos de un ciclo, podría pasar inadvertido; y si los niveles duran un solo ciclo, las transiciones de espera (FINAL, PULSO, …) no llegan a ver el cambio siguiente. Con niveles de al menos dos ciclos funcionan las tres.
@end
@res
**Opción 1: flanco de subida**

@fig fsm {"nodes": {"INICIO": [85, 70, "0"], "PULSO": [215, 70, "1"], "FINAL": [345, 70, "0"]}, "edges": [["INICIO", "INICIO", "0", 0], ["INICIO", "PULSO", "1", 0], ["PULSO", "FINAL", "X", 0], ["FINAL", "FINAL", "1", 0], ["FINAL", "INICIO", "0", -70]], "W": 430, "H": 180, "title": "Pulso en el flanco de subida"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | INICIO | PULSO | 0 |
| PULSO | FINAL | FINAL | 1 |
| FINAL | INICIO | FINAL | 0 |

| Estado | Código $q_1q_0$ | Salida |
|---|---|---|
| INICIO | 00 | 0 |
| PULSO | 01 | 1 |
| FINAL | 10 | 0 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $q_{0}$ |
| $K_{1}$ | $\overline{E_{0}}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $1$ |
| $S$ | $q_{0}$ |

**Opción 2: flanco de bajada**

@fig fsm {"nodes": {"INICIO": [85, 70, "0"], "EMPIE": [215, 70, "0"], "PULSO": [345, 70, "1"]}, "edges": [["INICIO", "INICIO", "0", 0], ["INICIO", "EMPIE", "1", 0], ["EMPIE", "EMPIE", "1", 0], ["EMPIE", "PULSO", "0", 0], ["PULSO", "INICIO", "X", -70]], "W": 430, "H": 180, "title": "Pulso en el flanco de bajada"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | INICIO | EMPIE | 0 |
| EMPIE | PULSO | EMPIE | 0 |
| PULSO | INICIO | INICIO | 1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $\overline{E_{0}}\cdot q_{0}$ |
| $K_{1}$ | $1$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{1}}$ |
| $K_{0}$ | $\overline{E_{0}}$ |
| $S$ | $q_{1}$ |

**Opción 3: los dos flancos**

@fig fsm {"nodes": {"INICIO": [85, 70, "0"], "PULS1": [215, 70, "1"], "MANT": [345, 70, "0"], "PULS0": [475, 70, "1"]}, "edges": [["INICIO", "INICIO", "0", 0], ["INICIO", "PULS1", "1", 0], ["PULS1", "MANT", "X", 0], ["MANT", "PULS0", "0", 0], ["MANT", "MANT", "1", 0], ["PULS0", "INICIO", "X", -70]], "W": 560, "H": 180, "title": "Pulso en los dos flancos"}

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICIO | INICIO | PULS1 | 0 |
| PULS1 | MANT | MANT | 1 |
| MANT | PULS0 | MANT | 0 |
| PULS0 | INICIO | INICIO | 1 |

| Función | Ecuación |
|---|---|
| $J_{1}$ | $q_{0}$ |
| $K_{1}$ | $q_{0}$ |
| $J_{0}$ | $E_{0}\cdot \overline{q_{1}}  +  \overline{E_{0}}\cdot q_{1}$ |
| $K_{0}$ | $1$ |
| $S$ | $q_{0}$ |

**Cronograma** de las tres opciones con la misma entrada

@fig cron {"signals": [["E₀", "0011110001110000"], ["S↑", "0010000001000000"], ["S↓", "0000001000001000"], ["S↑↓", "0010001001001000"]], "title": "", "rh": 34, "w_slot": 10, "grid": 4}

Las ecuaciones del libro se han comprobado en todas las transiciones de las tres variantes, y se han simulado 400 secuencias con niveles de 2 a 4 ciclos contra «el estado actual difiere del anterior» (y sus dos casos particulares).

@box ojo | Errata en el libro
En el diagrama del libro de la opción 3, el estado PULS1 aparece con salida 0. Debe ser 1: sin ella no habría pulso en el flanco de subida, y contradice la tabla de estados codificada y el cronograma ($S_0=q_0$).
@end
@end
@end

@ej lb8-34|Transmisor serie de dos bits con arranque y parada|Libro · Cap. 8 · P8.34|moore,serie,industrial|lb8.p834
@enun
Un transmisor envía por una línea serie $S$ los dos bits $E_1E_0$ que tiene en sus entradas cuando se acciona un pulsador $P$ (entradas $P\,E_1\,E_0$). La línea en reposo está a 1. Cada transmisión es una trama de **cuatro símbolos**: un bit de arranque a 0, el bit $E_1$, el bit $E_0$ y un bit final a 0; después la línea vuelve a 1. Debe transmitirse al **soltar** el pulsador. Diseña el autómata de Moore.
@end
@antes
**El autómata es un secuenciador con ramificaciones sólo para copiar los datos.** Hay una espera, una confirmación de soltado y luego tres pasos fijos. En los pasos de datos hay que elegir entre dos estados según el bit que se copia (UNO0/UNO1 y DOS0/DOS1) porque la salida es parte del estado.
@end
@paso Esperar y arrancar
INICIO (línea a 1): con $P=1$ pasa a TRANS; TRANS espera a que $P$ se suelte; al soltar, EMPIE saca el bit de arranque (0).
@end
@paso Copiar los datos
De EMPIE se pasa a UNO0 o UNO1 según $E_1$ (salida igual al bit copiado); de ahí a DOS0 o DOS1 según $E_0$; y de DOS siempre a FINAL (salida 0).
@end
@paso Fin
En FINAL, si $P$ vuelve a estar pulsado se encadena otra trama (TRANS); si no, se vuelve a INICIO con la línea a 1. La salida recorre pues 1, 0, $E_1$, $E_0$, 0, 1.
@end
@res
| Estado | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 | Salida |
|---|---|---|---|---|---|---|---|---|---|
| INICIO | INICIO | INICIO | INICIO | INICIO | TRANS | TRANS | TRANS | TRANS | 1 |
| TRANS | EMPIE | EMPIE | EMPIE | EMPIE | TRANS | TRANS | TRANS | TRANS | 1 |
| EMPIE | UNO0 | UNO0 | UNO1 | UNO1 | UNO0 | UNO0 | UNO1 | UNO1 | 0 |
| UNO0 | DOS0 | DOS1 | DOS0 | DOS1 | DOS0 | DOS1 | DOS0 | DOS1 | 0 |
| UNO1 | DOS0 | DOS1 | DOS0 | DOS1 | DOS0 | DOS1 | DOS0 | DOS1 | 1 |
| DOS0 | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | 0 |
| DOS1 | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | FINAL | 1 |
| FINAL | INICIO | INICIO | INICIO | INICIO | TRANS | TRANS | TRANS | TRANS | 0 |

Simulado con 300 tramas de datos aleatorios y pulsaciones de longitud variable: la secuencia de salida tras soltar $P$ es siempre 0, $E_1$, $E_0$, 0, 1. El libro lo presenta sólo con diagrama y comentarios.
@end
@end

@ej lb8-35|Receptor serie de dos bits con detección de error|Libro · Cap. 8 · P8.35|moore,serie,industrial|lb8.p835
@enun
Un receptor recibe por una línea serie $E$ las tramas del problema anterior: la línea en reposo está a 1 y cada trama es 0 (arranque), dos bits de datos, 0 (final). Salidas $I_1I_0\,AL$: los dos bits recibidos y una alarma $AL$ que se activa si el bit final no vale 0. Diseña el autómata de Moore. Después modifícalo para que **mantenga los datos** en las salidas hasta que empiece la trama siguiente.
@end
@antes
**Es el recíproco del transmisor:** hay que recordar los dos bits conforme llegan. Los estados que recuerdan el primer bit (UNO0/UNO1) se ramifican otra vez con el segundo (DOS0, DOS1, TRES0, TRES1), y en todos ellos se comprueba el bit final. Si vale 1, el receptor cae en ERROR, que es **absorbente**.
@end
@paso Primer autómata
INICI espera el 0 de arranque; EMPIE lo ha recibido; UNO0/UNO1 recuerdan el primer dato ($I_1$ ya vale ese bit); DOS0, DOS1, TRES0 y TRES1 recuerdan los dos y presentan $I_1I_0$ (00, 01, 10 y 11) con $AL=0$. Con 0 de cierre se pasa a BIEN y con 1 a ERROR ($AL=1$).
@end
@paso Después de BIEN
Con 1 (reposo) a INICI; con 0, la trama siguiente empieza ya: a EMPIE.
@end
@paso Autómata que mantiene el dato
En lugar de BIEN se tienen cuatro estados FIJO0 a FIJO3, que **conservan los mismos valores de salida** durante el reposo (1 se queda; 0 es el arranque de la trama siguiente: EMPIE). Así los datos se mantienen estables hasta el siguiente 0.
@end
@res
**Primer autómata** (10 estados; las «X» de salida se toman como 0)

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICI | EMPIE | INICI | 000 |
| EMPIE | UNO0 | UNO1 | 000 |
| UNO0 | DOS0 | DOS1 | 000 |
| UNO1 | TRES0 | TRES1 | 100 |
| DOS0 | BIEN | ERROR | 000 |
| DOS1 | BIEN | ERROR | 010 |
| TRES0 | BIEN | ERROR | 100 |
| TRES1 | BIEN | ERROR | 110 |
| BIEN | EMPIE | INICI | 000 |
| ERROR | ERROR | ERROR | 001 |

**Autómata que mantiene el dato** (13 estados)

| Estado | 0 | 1 | Salida |
|---|---|---|---|
| INICI | EMPIE | INICI | 000 |
| EMPIE | UNO0 | UNO1 | 000 |
| UNO0 | DOS0 | DOS1 | 000 |
| UNO1 | TRES0 | TRES1 | 100 |
| DOS0 | FIJO0 | ERROR | 000 |
| DOS1 | FIJO1 | ERROR | 010 |
| TRES0 | FIJO2 | ERROR | 100 |
| TRES1 | FIJO3 | ERROR | 110 |
| ERROR | ERROR | ERROR | 001 |
| FIJO0 | EMPIE | FIJO0 | 000 |
| FIJO1 | EMPIE | FIJO1 | 010 |
| FIJO2 | EMPIE | FIJO2 | 100 |
| FIJO3 | EMPIE | FIJO3 | 110 |

Simuladas 300 secuencias de entre una y cinco tramas con datos aleatorios y algún final erróneo: los datos aparecen en el ciclo en que se recibe el segundo bit, la alarma se activa y permanece tras un final erróneo, y en el segundo autómata el dato se mantiene durante el reposo. El libro no incluye ecuaciones (diagramas y comentarios).

@box ojo | Errata en el libro
En el primer diagrama el estado DOS1 (los dos bits recibidos son 0 y 1) aparece con salida 110. Debe ser 010: $I_1=0$ e $I_0=1$, que es además lo que dice el segundo autómata para el estado equivalente FIJO1.
@end
@end
@end

