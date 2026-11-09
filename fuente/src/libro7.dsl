%% id=libro7
%% group=ejer
%% n=3.7
%% title=Libro de problemas · Capítulo 7 · Registros y contadores
%% short=Libro · Cap. 7 Registros y contadores
%% sub=Veintidós problemas de registros, contadores síncronos y asíncronos, 74160/74163 y aplicaciones: cada circuito se ha simulado y comprobado.

@box idea | Cómo leer esta sección
Son los problemas resueltos del capítulo 7 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Los esquemas del libro **no se copian**: cada circuito se describe en texto (qué entradas lleva cada puerta o multiplexor) y se simula con un modelo propio; los cronogramas y las tablas salen de esa simulación. La teoría está en [[t07|el tema 7]].

Modelo de los contadores integrados que usa el capítulo (cuenta en cada flanco de subida del reloj):

| CLEAR | LOAD | ENP·ENT | Efecto en el flanco | RCO |
|---|---|---|---|---|
| 0 | × | × | borra a 0000 (sin esperar al reloj) | 0 |
| 1 | 0 | × | carga $D_3..D_0$ | — |
| 1 | 1 | 0 | mantiene | — |
| 1 | 1 | 1 | cuenta $+1$ (74160: de 9 pasa a 0; 74163: de 15 pasa a 0) | 1 si el valor es el último (9 ó 15) y ENT=1 |

El 74160 es un contador **BCD** (módulo 10) y el 74163 es un contador **binario** de cuatro bits (módulo 16). El borrado se trata como asíncrono, la carga es síncrona (necesita flanco) y las entradas de habilitación ENP y ENT se usan juntas como una sola.
@end

@ej lb7-1|Registro universal de 4 bits con multiplexores 4:1|Libro · Cap. 7 · P7.1|registro,mux,tri-estado|lb7.p71
@enun
Dibuja un registro de 4 bits con biestables D cuya operación se elige con dos líneas de control $S_1S_0$: $11$ carga en paralelo la entrada $E_3..E_0$, $10$ invierte el contenido, $01$ lo pone a cero de forma **síncrona** y $00$ lo deja como está. Añade una línea $EO$ (enable de salida) que ponga las salidas en alta impedancia mediante buffers triestado. Hay también una entrada de borrado asíncrono $\overline{INICIO}$.
@end
@antes
**Un multiplexor delante de cada D.** El biestable D copia lo que le llegue; si lo que le llega es una de cuatro posibilidades elegidas por $S_1S_0$, se consigue cada operación sin tocar el biestable.
@end
@paso Qué lleva cada entrada del multiplexor
Para el bit $i$, el mux 4:1 recibe: entrada 0 → $Q_i$; entrada 1 → el valor constante 0; entrada 2 → $\overline{Q_i}$; entrada 3 → $E_i$. Las líneas $S_1S_0$ van a las entradas de selección de **los cuatro multiplexores a la vez**.
@end
@paso Por qué funciona
$S_1S_0=00$: $D_i=Q_i$, y el flanco vuelve a escribir lo mismo (**inhibición**). $01$: $D_i=0$ (**borrado síncrono**, distinto del asíncrono $\overline{INICIO}$, que no espera al reloj). $10$: $D_i=\overline{Q_i}$ (**volteo**). $11$: $D_i=E_i$ (**carga**).
@end
@paso Salida con triestados
Cada $Q_i$ pasa por un buffer triestado gobernado por $EO$: con $EO=1$ la salida muestra el valor y con $EO=0$ queda desconectada (Z), de modo que varios registros pueden compartir los mismos hilos de un bus.
@end
@res
| $S_1S_0$ | Entrada del mux que se elige | $D_i$ | Operación |
|---|---|---|---|
| 00 | 0 | $Q_i$ | inhibición |
| 01 | 1 | 0 | borrado síncrono |
| 10 | 2 | $\overline{Q_i}$ | volteo |
| 11 | 3 | $E_i$ | carga en paralelo |

Comprobado de forma exhaustiva: las $16\cdot16\cdot4=1024$ combinaciones de estado, entrada y selección coinciden con la descripción funcional (conservar, 0, $n\oplus1111$, $E$).
@end
@end

@ej lb7-2|Registro de 4 bits con desplazamientos circulares|Libro · Cap. 7 · P7.2|registro,mux,rotacion|lb7.p72
@enun
Implementa un registro de 4 bits con biestables D y cuatro operaciones elegidas por $S_1S_0$: $11$ carga en paralelo; $10$ desplaza una posición **a la izquierda con recirculación** (el bit que sale por arriba entra por abajo); $01$ desplaza **a la derecha con recirculación**; $00$ inhibe.
@end
@antes
**Cada bit toma el valor de un vecino.** Desplazar es que $D_i$ valga el bit vecino de antes del flanco; recircular es que los extremos se cierren en anillo.
@end
@paso Qué lleva cada multiplexor
Para el bit $i$ (los índices se toman módulo 4): entrada 0 → $Q_i$; entrada 1 → $Q_{i+1}$ (el vecino de más peso: **derecha**); entrada 2 → $Q_{i-1}$ (el de menos peso: **izquierda**); entrada 3 → $E_i$. El bit 3 recibe $Q_0$ en la entrada 1 y el bit 0 recibe $Q_3$ en la entrada 2, y eso es la recirculación.
@end
@paso Lectura de las operaciones
$01$: cada $D_i=Q_{i+1}$, el contenido se mueve hacia el bit 0 y el bit $Q_0$ vuelve al bit 3 (rotación a la derecha). $10$: cada $D_i=Q_{i-1}$ y $Q_3$ vuelve a $Q_0$ (rotación a la izquierda).
@end
@paso Propiedades comprobadas
Cuatro rotaciones seguidas devuelven el valor inicial. Rotar a la izquierda equivale a **multiplicar por 2 módulo 15** (con el 15 como punto fijo): por ejemplo $1011\to0111\to1110\to1101\to1011$ ($11\to7\to14\to13\to11$).
@end
@res
Rotación a la izquierda de $1011$ en cuatro flancos: 1011 → 0111 → 1110 → 1101 → 1011.

| $S_1S_0$ | Mux del bit $i$ elige | Operación |
|---|---|---|
| 00 | $Q_i$ | inhibición |
| 01 | $Q_{i+1}$ | rotación a la derecha |
| 10 | $Q_{i-1}$ | rotación a la izquierda |
| 11 | $E_i$ | carga en paralelo |

Verificado con las 1024 combinaciones de estado, entrada y selección.
@end
@end

@ej lb7-3|Registro con dos buses bidireccionales|Libro · Cap. 7 · P7.3|registro,tri-estado,bus|lb7.p73
@enun
Diseña un registro de 4 bits con dos buses de datos bidireccionales, $A_3..A_0$ y $B_3..B_0$. El registro se carga desde uno de los buses y se lee por el otro. Una línea $C$ fija el sentido: con $C=1$ la transferencia es de $A$ a $B$ y con $C=0$ de $B$ a $A$.
@end
@antes
**Un par de triestados por cada cara del biestable.** Se necesitan dos buffers que lleven datos hacia la entrada D (uno desde $A$ y otro desde $B$) y otros dos que saquen $Q$ hacia cada bus. Se habilitan por parejas para que nunca dos salidas empujen el mismo hilo.
@end
@paso Cableado por bit
Entrada D: un buffer desde $A_i$ habilitado con $C=1$ y otro desde $B_i$ habilitado con $C=0$ (la línea $C$ llega invertida al segundo). Salida $Q_i$: un buffer hacia $B_i$ habilitado con $C=1$ y otro hacia $A_i$ habilitado con $C=0$.
@end
@paso Con $C=1$
El registro captura $A$ en el flanco y $Q$ se pone en $B$: transferencia $A\to B$. El buffer $Q\to A$ está en alta impedancia y por eso $A$ puede ser conducido desde fuera sin conflicto.
@end
@paso Con $C=0$
Es la imagen en espejo: se captura $B$ y se muestra en $A$.
@end
@paso Qué puede salir mal
El diseño **supone que quien conduce el bus cumple el sentido**. Si con $C=1$ otro dispositivo conduce $B$ con un valor distinto del que presenta $Q$, hay un cortocircuito lógico (conflicto). El modelo con valores $0$, $1$, $Z$ y $X$ lo detecta en los dos casos posibles.
@end
@res
| $C$ | Se captura | Se muestra | Buffers activos |
|---|---|---|---|
| 1 | $A$ | $Q$ en $B$ | $A\to D$ y $Q\to B$ |
| 0 | $B$ | $Q$ en $A$ | $B\to D$ y $Q\to A$ |

Simulado con las ocho combinaciones de $C$, valor previo de $Q$ y dato externo: el dato llega siempre al registro y aparece en el otro bus, sin conflictos mientras se respete el sentido.
@end
@end

@ej lb7-4|Registro con un solo bus de datos|Libro · Cap. 7 · P7.4|registro,tri-estado,bus|lb7.p74
@enun
Diseña un registro de 4 bits con **un único** bus de datos $D_3..D_0$ que sirve a la vez para escribirlo y para leerlo. La línea $E/\overline L$ decide: a 1 el registro se carga desde el bus y a 0 vuelca su contenido sobre el bus.
@end
@antes
**Es el caso anterior con un solo bus**: cada bit del bus se conecta a la vez a la entrada del biestable (a través de un triestado) y a su salida (a través de otro).
@end
@paso Por bit
El buffer de escritura va del bus a la entrada D y se habilita con $E/\overline L=1$. El buffer de lectura va de $Q$ al bus y se habilita con $E/\overline L=0$ (llega invertido). Nunca están activos a la vez.
@end
@paso Escritura
Con $E/\overline L=1$ el bus es conducido por quien escribe y en el flanco el registro lo captura; $Q$ no se envía al bus.
@end
@paso Lectura
Con $E/\overline L=0$ el registro conduce el bus con su contenido y nadie más debe conducirlo. Durante la lectura también llega un flanco al reloj, pero el biestable captura lo que él mismo está poniendo en el bus, y por tanto no cambia.
@end
@res
| $E/\overline L$ | Operación | Quién conduce el bus |
|---|---|---|
| 1 | se carga $D_i\to Q_i$ | el exterior |
| 0 | se descarga $Q_i\to D_i$ | el registro |

La lectura es idempotente: si el registro conduce el bus, lo que captura es lo que ya contenía. Comprobado para los dos valores de $Q$ y de dato externo, incluyendo el caso de conflicto (alguien más conduce el bus durante la lectura).
@end
@end

@ej lb7-5|Contador de Johnson de tres bits|Libro · Cap. 7 · P7.5|contador,johnson,cronograma|lb7.p75
@enun
Tres biestables D con el mismo reloj están enlazados así: $D_0=\overline{Q_2}$, $D_1=Q_0$, $D_2=Q_1$. Completa el cronograma partiendo de $Q_2Q_1Q_0=000$ e indica de qué contador se trata.
@end
@antes
**Un registro de desplazamiento realimentado con el último bit negado.** Cada bit copia al anterior y el primero recibe lo contrario del último, de modo que el registro se va llenando de unos y después de ceros.
@end
@paso Cada flanco
El contenido se desplaza una posición hacia $Q_2$ y entra por $Q_0$ el complemento de lo que salía por $Q_2$. Partiendo de 000 los unos entran uno a uno (001, 011, 111) y a continuación los ceros (110, 100, 000).
@end
@paso Qué contador es
Es un **contador de Johnson** (o de anillo retorcido) de 3 bits: $2\cdot3=6$ estados de los $2^3=8$ posibles, **módulo 6**. Entre dos estados consecutivos cambia un solo bit.
@end
@paso Estados sobrantes
Los estados 010 y 101 no pertenecen a la secuencia y forman un ciclo aparte (010 → 101 → 010). Si el contador arranca en uno de ellos no entra solo en la secuencia útil; hay que inicializarlo.
@end
@res
@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "00001111111111111111111111110000000000000000000000001111111111111111"], ["Q1", "00000000000011111111111111111111111100000000000000000000000011111111"], ["Q2", "00000000000000000000111111111111111111111111000000000000000000000000"]], "title": "Contador de Johnson de 3 bits", "rh": 34, "w_slot": 8, "grid": 8}

Secuencia $Q_2Q_1Q_0$: 000 → 001 → 011 → 111 → 110 → 100 → 000.

Cada estado se identifica con una puerta de **solo dos entradas** (por ser un código con un único cambio entre estados):

| Estado | Decodificador |
|---|---|
| 000 | $\overline{Q_0}$·$\overline{Q_2}$ |
| 001 | $Q_0$·$\overline{Q_1}$ |
| 011 | $Q_1$·$\overline{Q_2}$ |
| 111 | $Q_0$·$Q_2$ |
| 110 | $\overline{Q_0}$·$Q_1$ |
| 100 | $\overline{Q_1}$·$Q_2$ |
@end
@end

@ej lb7-6|Dos contadores con biestables D: uno asíncrono y otro «aberrante»|Libro · Cap. 7 · P7.6|contador,asincrono,cronograma|lb7.p76
@enun
Completa los cronogramas de dos circuitos de dos biestables D e indica qué secuencia generan. **Circuito 1:** cada biestable tiene $D=\overline Q$ (se carga con lo contrario de lo que tenía); el primero recibe $Ck$ y el segundo recibe $Q_0$ como reloj, ambos activos por flanco de subida. **Circuito 2:** el primero es igual (D $=\overline{Q_0}$, flanco de subida de $Ck$); el segundo tiene $D=Q_0$ y es activo por **flanco de bajada** de $Ck$.
@end
@antes
**Hay que preguntar a cada biestable qué hace y cuándo lo hace.** Lo primero lo dice el valor de D; lo segundo, la señal que mueve su reloj.
@end
@paso Circuito 1 (asíncrono)
$Q_0$ cambia en cada flanco de subida de $Ck$. $Q_1$ cambia en cada flanco de subida de **$Q_0$**, que no es el reloj general: por eso el circuito es asíncrono. Como los flancos de subida de $Q_0$ llegan cada dos relojes, $Q_1$ cambia más despacio.
@end
@paso Secuencia del circuito 1
En el primer flanco $Q_0$ pasa de 0 a 1 y arrastra a $Q_1$, que también pasa a 1: se va de 00 a **11**. Después 10, 01, 00: es un contador **descendente de módulo 4** ($Q_1Q_0$: 00, 11, 10, 01, 00…).
@end
@paso Circuito 2
$Q_0$ cambia en cada flanco de subida; $Q_1$ copia a $Q_0$ en cada flanco de **bajada**. Con medio periodo de desfase, la secuencia es 00, 01, 11, 10, 00…: el **código Gray** de dos bits. Cada cambio de estado tiene lugar en un flanco distinto, subida o bajada.
@end
@paso Valoración
Los biestables del circuito 2 son síncronos pero respecto de **flancos diferentes** del mismo reloj. El circuito funciona, pero es el tipo de truco que se evita en un diseño síncrono: su interés es teórico.
@end
@res
@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "00001111111100000000111111110000000011111111000000001111111100000000"], ["Q1", "00001111111111111111000000000000000011111111111111110000000000000000"]], "title": "Circuito 1: contador descendente asíncrono", "rh": 30, "w_slot": 8, "grid": 8}

@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "00001111111100000000111111110000000011111111000000001111111100000000"], ["Q1", "00000000111111110000000011111111000000001111111100000000111111110000"]], "title": "Circuito 2: secuencia Gray de dos bits", "rh": 30, "w_slot": 8, "grid": 4}

Secuencia $Q_1Q_0$ del circuito 1: 00 → 11 → 10 → 01 → 00. Del circuito 2 (un estado por cada medio periodo): 00 → 01 → 11 → 10 → 00.
@end
@end

@ej lb7-7|Contador asíncrono con una línea TIPO|Libro · Cap. 7 · P7.7|contador,asincrono,cronograma,jk|lb7.p77
@enun
Tres biestables J‑K activos por flanco de bajada están encadenados: el primero recibe $Ck$, el segundo recibe $Q_0$ y el tercero recibe $Q_1$ como reloj. Las entradas $J_1=K_1=J_2=K_2=1$, mientras que $J_0=K_0=TIPO$. Completa el cronograma para $TIPO=1$ y para $TIPO=0$ e indica la secuencia en cada caso.
@end
@antes
**Con $J=K=1$ un J‑K voltea en cada flanco; con $J=K=0$ no hace nada.** El primer biestable manda: si no voltea, tampoco lo harán los siguientes, porque no recibirán flancos.
@end
@paso $TIPO=1$
Los tres biestables voltean. $Q_0$ cambia en cada bajada de $Ck$; $Q_1$ lo hace en cada bajada de $Q_0$ y $Q_2$ en cada bajada de $Q_1$. Al ser flancos de bajada encadenados el conjunto cuenta **hacia arriba**: 000, 001, 010, …, 111, 000. Es un **contador asíncrono ascendente de módulo 8**.
@end
@paso $TIPO=0$
$J_0=K_0=0$: el primero **mantiene** su valor, $Q_0$ no cambia y el segundo no recibe flancos. Como tampoco los recibe el tercero, el contador **se queda donde estaba** (aquí, en 000).
@end
@paso Resumen
La línea TIPO funciona como un **enable** de la cuenta: con TIPO a 0 el contador está parado y con TIPO a 1 cuenta en binario natural.
@end
@res
@fig cron {"signals": [["Ck", "0000111100001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "0000000011111111000000001111111100000000111111110000000011111111000000001111"], ["Q1", "0000000000000000111111111111111100000000000000001111111111111111000000000000"], ["Q2", "0000000000000000000000000000000011111111111111111111111111111111000000000000"]], "title": "TIPO = 1: cuenta ascendente módulo 8", "rh": 30, "w_slot": 8, "grid": 8}

@fig cron {"signals": [["Ck", "0000111100001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "0000000000000000000000000000000000000000000000000000000000000000000000000000"], ["Q1", "0000000000000000000000000000000000000000000000000000000000000000000000000000"], ["Q2", "0000000000000000000000000000000000000000000000000000000000000000000000000000"]], "title": "TIPO = 0: el contador no cuenta", "rh": 30, "w_slot": 8, "grid": 8}
@end
@end

@ej lb7-8|Contador BCD síncrono ascendente con biestables J‑K|Libro · Cap. 7 · P7.8|contador,sincrono,diseño,jk|lb7.p78
@enun
Diseña un contador síncrono ascendente BCD (0, 1, …, 9, 0, …) con biestables J‑K activos por flanco de subida.
@end
@antes
**Método de diseño síncrono:** se escribe la tabla de estados (estado actual → siguiente), se traduce a las entradas J y K que hacen falta en cada biestable mediante la tabla de excitación, se simplifica con Karnaugh y se cablean las funciones. Los seis estados 1010…1111 no existen en BCD y se toman como indiferentes.
@end
@paso Tabla de excitación del J‑K
Para cada biestable: $0\to0$ pide $J=0,K=\times$; $0\to1$ pide $J=1,K=\times$; $1\to0$ pide $J=\times,K=1$; $1\to1$ pide $J=\times,K=0$.
@end
@paso Tabla del contador
Se calcula J y K de cada bit para cada una de las diez filas del BCD (tabla del resultado). Las seis filas restantes valen $\times$ en todas las entradas.
@end
@paso Simplificación
Con Karnaugh y las indiferencias: $J_3=Q_2Q_1Q_0$, $K_3=Q_0$, $J_2=K_2=Q_1Q_0$, $J_1=\overline{Q_3}Q_0$, $K_1=Q_0$, $J_0=K_0=1$. El bit 0 siempre voltea y los demás voltean cuando todos los de menor peso valen 1, con la salvedad de que $Q_1$ no debe subir cuando $Q_3=1$ (para no pasar de 9 a 10).
@end
@paso Comprobación
Se ha simulado el contador con esas ecuaciones: 0, 1, …, 9, 0. Además se ha comprobado qué pasa en los estados no usados: **todos entran solos en la secuencia** en un máximo de dos ciclos (10 → 11 → 4; 12 → 13 → 4; 14 → 15 → 0): el contador es **autocorrector**. Es una propiedad que el libro no analiza.
@end
@res
| $Q_3Q_2Q_1Q_0$ | $J_3$ | $K_3$ | $J_2$ | $K_2$ | $J_1$ | $K_1$ | $J_0$ | $K_0$ |
|---|---|---|---|---|---|---|---|---|
| 0000 | 0 | X | 0 | X | 0 | X | 1 | X |
| 0001 | 0 | X | 0 | X | 1 | X | X | 1 |
| 0010 | 0 | X | 0 | X | X | 0 | 1 | X |
| 0011 | 0 | X | 1 | X | X | 1 | X | 1 |
| 0100 | 0 | X | X | 0 | 0 | X | 1 | X |
| 0101 | 0 | X | X | 0 | 1 | X | X | 1 |
| 0110 | 0 | X | X | 0 | X | 0 | 1 | X |
| 0111 | 1 | X | X | 1 | X | 1 | X | 1 |
| 1000 | X | 0 | 0 | X | 0 | X | 1 | X |
| 1001 | X | 1 | 0 | X | 0 | X | X | 1 |

Funciones: $J_3=Q_2Q_1Q_0$; $K_3=Q_0$; $J_2=K_2=Q_1Q_0$; $J_1=\overline{Q_3}\,Q_0$; $K_1=Q_0$; $J_0=K_0=1$.

Estados no usados: 10 → 11 → 4; 11 → 4; 12 → 13 → 4; 13 → 4; 14 → 15 → 0; 15 → 0.

@box ojo | Errata en el libro
En las formas canónicas el libro escribe dos veces «J3»: la segunda lista ($\Sigma(3)$) corresponde a $J_2$, como indican la tabla y el diagrama de Karnaugh.
@end
@end
@end

@ej lb7-9|Contador Gray síncrono de módulo 16|Libro · Cap. 7 · P7.9|contador,sincrono,diseño,gray,jk|lb7.p79
@enun
Diseña un contador síncrono ascendente de módulo 16 que recorra los estados en código Gray, con biestables J‑K.
@end
@antes
**Mismo método que el contador BCD, con otra tabla de estados.** Cada estado pasa al siguiente código Gray (0000, 0001, 0011, 0010, 0110, …, 1000, 0000). Como hay 16 estados, no queda ninguna indiferencia en las filas: solo las que aporta la tabla de excitación del J‑K.
@end
@paso Tabla de estados y excitación
Se asigna a cada estado el siguiente de la secuencia Gray y se calculan J y K de cada bit con la misma tabla de excitación del problema anterior.
@end
@paso Funciones
Las formas canónicas ($\Sigma$ de las filas, numeradas por el valor binario del estado) son $J_3=\Sigma(4)$, $K_3=\Sigma(8)$, $J_2=\Sigma(2)$, $K_2=\Sigma(14)$, $J_1=\Sigma(1,13)$, $K_1=\Sigma(7,11)$, $J_0=\Sigma(0,6,10,12)$ y $K_0=\Sigma(3,5,9,15)$. Con las indiferencias salen: $J_3=Q_2\overline{Q_1}\,\overline{Q_0}$, $K_3=\overline{Q_2}\,\overline{Q_1}\,\overline{Q_0}$, $J_2=\overline{Q_3}Q_1\overline{Q_0}$, $K_2=Q_3Q_1\overline{Q_0}$, $J_1=Q_3Q_2Q_0+\overline{Q_3}\,\overline{Q_2}Q_0$, $K_1=\overline{Q_3}Q_2Q_0+Q_3\overline{Q_2}Q_0$ y los de $J_0$ y $K_0$ con cuatro términos cada uno.
@end
@paso Una simplificación más
Los cuatro términos de $J_0$ y de $K_0$ son los de la **paridad** de $Q_3Q_2Q_1$: $K_0=Q_3\oplus Q_2\oplus Q_1$ y $J_0=\overline{K_0}$. Es lógico: en una secuencia Gray el bit menos significativo cambia siempre que haga falta mantener la paridad total, y se comprueba al simular. (Es una observación propia, no del libro.)
@end
@paso Comprobación
Con las funciones simplificadas el contador recorre los 16 estados en el orden Gray y vuelve al inicio; entre dos estados consecutivos cambia exactamente un bit.
@end
@res
| $Q_3..Q_0$ (t) | $Q_3..Q_0$ (t+1) | $J_3$ | $K_3$ | $J_2$ | $K_2$ | $J_1$ | $K_1$ | $J_0$ | $K_0$ |
|---|---|---|---|---|---|---|---|---|---|
| 0000 | 0001 | 0 | X | 0 | X | 0 | X | 1 | X |
| 0001 | 0011 | 0 | X | 0 | X | 1 | X | X | 0 |
| 0011 | 0010 | 0 | X | 0 | X | X | 0 | X | 1 |
| 0010 | 0110 | 0 | X | 1 | X | X | 0 | 0 | X |
| 0110 | 0111 | 0 | X | X | 0 | X | 0 | 1 | X |
| 0111 | 0101 | 0 | X | X | 0 | X | 1 | X | 0 |
| 0101 | 0100 | 0 | X | X | 0 | 0 | X | X | 1 |
| 0100 | 1100 | 1 | X | X | 0 | 0 | X | 0 | X |
| 1100 | 1101 | X | 0 | X | 0 | 0 | X | 1 | X |
| 1101 | 1111 | X | 0 | X | 0 | 1 | X | X | 0 |
| 1111 | 1110 | X | 0 | X | 0 | X | 0 | X | 1 |
| 1110 | 1010 | X | 0 | X | 1 | X | 0 | 0 | X |
| 1010 | 1011 | X | 0 | 0 | X | X | 0 | 1 | X |
| 1011 | 1001 | X | 0 | 0 | X | X | 1 | X | 0 |
| 1001 | 1000 | X | 0 | 0 | X | 0 | X | X | 1 |
| 1000 | 0000 | X | 1 | 0 | X | 0 | X | 0 | X |

Secuencia: 0000 → 0001 → 0011 → 0010 → 0110 → 0111 → 0101 → 0100 → 1100 → 1101 → 1111 → 1110 → 1010 → 1011 → 1001 → 1000 → 0000.
@end
@end

@ej lb7-10|Contadores módulo 60, módulo 1000 y módulo 12 con circuitos integrados|Libro · Cap. 7 · P7.10|contador,74160,74163,modulo|lb7.p710
@enun
Con contadores síncronos BCD 74160 diseña un contador de **módulo 60**; haz lo mismo para uno de **módulo 1000** y otro de **módulo 12** en BCD. Para el módulo 12 estudia también una versión con un 74163 binario y un convertidor.
@end
@antes
**Se encadenan contadores** de modo que cada uno cuente solo cuando todos los anteriores están en su último valor (conexión de RCO a ENP·ENT), y se recorta la cuenta cargando 0 cuando se llega al valor que se quiere evitar.
@end
@paso Módulo 60
Dos 74160: **unidades** (0 a 9) y **decenas**. Las decenas cuentan solo cuando las unidades valen 9 (RCO a ENP·ENT). Hay que impedir que lleguen a 6: una NAND de $Q_2$ y $Q_0$ de las decenas (valor 5) y del RCO de las unidades (valor 9) detecta 59 y se lleva a LOAD de las decenas, que carga 0 con el siguiente flanco. Así después de 59 se pasa a 00, y no a 60.
@end
@paso Qué pasa si falta el RCO en la NAND
Si la puerta solo mirase el valor 5 de las decenas, el contador **no llegaría nunca a 51**: al llegar a 50 las decenas cargarían 0 en el flanco siguiente mientras las unidades siguen contando, y la secuencia pasaría de 50 a **01** (la cuenta quedaría en 1…50). El libro dice «de 50 a 00»; la simulación da 01. El RCO asegura que se espera a que las unidades lleguen a 9.
@end
@paso Módulo 1000
Tres 74160 en serie y sin recorte (todos son módulo 10): unidades siempre habilitadas; decenas con RCO de unidades; **centenas con RCO·RCO**. No hace falta usar LOAD. Una propiedad curiosa del cronograma: el valor del contador coincide con el **número de flancos recibidos**, porque al llegar el primer flanco el contador ya vale 000 y pasa a 001.
@end
@paso Módulo 12, opción A
Dos 74160 con una NAND de $Q_0$ de decenas y $Q_0$ de unidades (valor 11). Su salida va a los dos LOAD (con $D=0000$). Las decenas cuentan solo con el RCO de las unidades. Secuencia 00, 01, …, 09, 10, 11, 00.
@end
@paso Módulo 12, opción B
Un 74163 binario con una NAND de $Q_3Q_1Q_0$ (valor 1011) que carga 0. Solo hace falta un integrado, pero la salida está en **binario** (0000 a 1011) y no en BCD. Para visualizarla en dos dígitos hay que convertirla con un conversor binario‑BCD (74185): para valores hasta 11 el bit menos significativo pasa sin cambios, porque 10 es par.
@end
@res
| Contador | Integrados | Recorte | Secuencia |
|---|---|---|---|
| módulo 60 | 2 × 74160 | NAND ($Q_2$, $Q_0$ decenas, RCO unidades) → LOAD decenas | 00 … 59, 00 |
| módulo 1000 | 3 × 74160 | ninguno | 000 … 999, 000 |
| módulo 12 (A) | 2 × 74160 | NAND ($Q_0$ dec., $Q_0$ uni.) → LOAD ambos | 00 … 11, 00 |
| módulo 12 (B) | 74163 + conversor | NAND ($Q_3,Q_1,Q_0$) → LOAD | 0000 … 1011, 0000 |

Simulados los cuatro circuitos durante varios ciclos (130 flancos el de 60, 2100 el de 1000, 40 los de 12): el valor coincide en cada flanco con el contador teórico módulo $N$.
@end
@end

@ej lb7-11|Reloj digital de 12 horas con un reloj de 1 kHz|Libro · Cap. 7 · P7.11|contador,74160,aplicacion,reloj|lb7.p711
@enun
Diseña un reloj partiendo de una señal de 1 kHz y visualiza horas, minutos y segundos en displays de siete segmentos. Añade una indicación AM/PM.
@end
@antes
**Una cadena de divisores:** cada contador cuenta solo cuando el anterior ha llegado a su último valor y ahí se pone a cero para empezar de nuevo. Todos los contadores comparten el mismo reloj de 1 kHz y se encadenan con los **enables**, no con relojes distintos (diseño síncrono).
@end
@paso Milésimas
Tres 74160 en serie forman un contador de **módulo 1000**: 1000 flancos a 1 kHz son 1 s. Su fin de cuenta $RCO\cdot RCO\cdot RCO$ vale 1 una vez por segundo y es el enable de los segundos.
@end
@paso Segundos y minutos
Cada pareja de 74160 es un **módulo 60** como el del problema anterior: unidades hasta 9; decenas hasta 5. Para que una pareja cuente deben cumplirse a la vez el enable de la anterior, el fin de las unidades (9) y las decenas (5) cuando toca saltar.
@end
@paso Una misma puerta, dos usos
La puerta AND que detecta «decenas = 5, unidades = 9 y enable de la etapa anterior» sirve dos veces: da el **enable** de la etapa siguiente (minutos suman uno más) y, invertida, el **LOAD** de las decenas propias, que cargan 0 en ese mismo flanco. Es decir, cada contador se pone a cero justo cuando el siguiente cuenta.
@end
@paso Horas y AM/PM
Para las horas se decodifica el valor 12 (decenas $Q_0$ y unidades $Q_1$) y se lleva, invertido, a los LOAD de las dos cifras. Es el recorte a módulo 12: el valor 12 solo existe durante un flanco y se pasa a 00. Esa misma señal se lleva a un **biestable T** cuyo estado es la indicación PM, que cambia cada 12 horas.
@end
@paso Comprobación
Se ha simulado el circuito completo (9 contadores y el biestable T) en los instantes críticos precargando justo antes de cada desbordamiento: milésimas, segundos, minutos, horas, y paso por las 12 en los dos sentidos (AM→PM y PM→AM). Además, un día entero con reloj de 1 Hz (86 400 flancos) sale exacto.
@end
@res
| Etapa | Contador | Cuenta cuando… | Recorte |
|---|---|---|---|
| milésimas | 3 × 74160 | siempre | ninguno (mod 1000) |
| segundos | 2 × 74160 | RCO·RCO·RCO de milésimas | 59 → 00 |
| minutos | 2 × 74160 | fin de segundos (59 s y 999 ms) | 59 → 00 |
| horas | 2 × 74160 | fin de minutos | 12 → 00 (módulo 12) y toggle de PM |

Ejemplo de paso por mediodía (milésimas en la última columna, de $11{:}59{:}59.995$ AM): 11:59:59.999 AM · 12:00:00.000 AM · 00:00:00.001 PM · 00:00:00.002 PM · 00:00:00.003 PM.

Se observa que el 12 aparece un solo milisegundo antes de volver a 00; la indicación PM cambia en ese flanco y no se vuelve a tocar durante 12 horas.
@end
@end

@ej lb7-12|Contador módulo 10 que cuenta con el reloj o con un pulsador|Libro · Cap. 7 · P7.12|contador,74160,pulsador,deteccion-flancos|lb7.p712
@enun
Diseña un contador síncrono módulo 10 que cuente al ritmo de un reloj o bien una vez por cada pulsación de un pulsador. Con el interruptor $I=0$ debe contar con el reloj; con $I=1$ debe contar al ritmo del pulsador, una vez por pulsación sea cual sea su duración.
@end
@antes
**Hay dos formas de hacerlo y la buena no toca el reloj.** Se puede escoger la señal de reloj del contador con un multiplexor (reloj o pulsador), o se puede dejar siempre el mismo reloj y escoger si el contador está **habilitado**.
@end
@paso Primera solución: multiplexor en el reloj
Un mux 2:1 elige entre $Ck$ ($I=0$) y el pulsador ($I=1$) como reloj de un 74160. Funciona solo si el pulsador está **filtrado** (red RC, báscula R‑S…): un pulsador real rebota y cada rebote es un flanco. Con un pulso de entrada sucio de cuatro subidas el contador salta de cuatro en cuatro (simulado). Y la solución tiene un defecto de método: la señal de reloj ya no es siempre $Ck$.
@end
@paso Segunda solución: reloj único y detector de flancos
Dos biestables D con el reloj $Ck$ copian el pulsador: $Q_1$ el valor actual y $Q_2$ el anterior. La salida $Q_1\cdot\overline{Q_2}$ vale 1 **exactamente un periodo** después de cada subida del pulsador, sea cual sea el tiempo que se mantenga pulsado. Un mux 2:1 escoge ENP·ENT: con $I=0$ vale 1 (cuenta con el reloj) y con $I=1$ vale ese pulso.
@end
@paso Comprobación
Con $I=1$ se han simulado 300 secuencias aleatorias de pulsaciones (de 2 a 12 relojes de duración): el contador avanza **una unidad por pulsación**. Con $I=0$ avanza una por reloj. Las dos soluciones requieren que el pulsador esté filtrado de rebotes; la segunda además cumple que la única señal de reloj es $Ck$.
@end
@res
@fig cron {"signals": [["Ck", "000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111"], ["Pulsador", "000000000000000000000000111111111111111111111111111111111111111100000000000000000000000011111111111111111111111100000000000000000000000000000000"], ["Q1", "000000000000000000000000000011111111111111111111111111111111111111110000000000000000000000001111111111111111111111110000000000000000000000000000"], ["Q2", "000000000000000000000000000000000000111111111111111111111111111111111111111100000000000000000000000011111111111111111111111100000000000000000000"], ["Habilita", "000000000000000000000000000011111111000000000000000000000000000000000000000000000000000000001111111100000000000000000000000000000000000000000000"]], "title": "Solución 2 con I = 1 (cada pulsación suma uno)", "rh": 30, "w_slot": 6, "grid": 8}

La señal «Habilita» ($Q_1\cdot\overline{Q_2}$) dura exactamente un periodo de reloj y aparece **dos veces** para las dos pulsaciones: la primera, aunque se mantenga pulsado durante cinco relojes, y la segunda de tres. El contador suma uno en cada uno de esos dos periodos.
@end
@end

@ej lb7-13|Cerradura que se abre con la secuencia 1011|Libro · Cap. 7 · P7.13|registro,desplazamiento,secuencia,aplicacion|lb7.p713
@enun
Una puerta se abre automáticamente cuando recibe, de forma síncrona por una línea de entrada, la secuencia 1, 0, 1, 1: debe darse en los **cuatro últimos flancos de reloj**. Diséñala con un registro de desplazamiento.
@end
@antes
**Un registro de 4 bits «recuerda» los cuatro últimos bits.** Si el bit nuevo entra por $Q_0$, en $Q_3$ está el más antiguo y en $Q_0$ el más reciente. La clave, leída en el orden de llegada $1,0,1,1$, corresponde al contenido $Q_3Q_2Q_1Q_0=1011$.
@end
@paso Opción A: puerta AND
Una AND de cuatro entradas con $Q_2$ negado: $Abre=Q_3\cdot\overline{Q_2}\cdot Q_1\cdot Q_0$. Requiere un inversor y una AND.
@end
@paso Opción B: comparador
Un comparador de cuatro bits (tipo 7485) con una entrada fija a $1011$ y la otra conectada a $Q_3..Q_0$: la salida «igual» abre la puerta. Es más potente porque **cambiar la clave** es solo cambiar interruptores.
@end
@paso Comparación
La opción A es más sencilla pero menos clara; la B es más versátil. En coste no hay una ventaja grande: un 7485 frente a un 7408 y un 7404.
@end
@paso Solapamiento
La puerta se abre **cada vez** que los cuatro últimos bits valen 1011, aunque se solapen con una secuencia anterior: con la entrada 0 1 0 1 1 0 1 1 1 0 1 1 se abre en el cuarto, en el séptimo y en el último flanco (la secuencia 1011 y la siguiente comparten los dos últimos bits).
@end
@res
Comprobado con 400 secuencias aleatorias de longitud 4 a 40: las dos opciones dan la misma salida y se abren exactamente cuando los cuatro últimos bits son 1011.

| Flanco | Bit | $Q_3Q_2Q_1Q_0$ | Abre |
|---|---|---|---|
| 1 | 0 | 0000 | 0 |
| 2 | 1 | 0001 | 0 |
| 3 | 0 | 0010 | 0 |
| 4 | 1 | 0101 | 0 |
| 5 | 1 | 1011 | 1 |
| 6 | 0 | 0110 | 0 |
| 7 | 1 | 1101 | 0 |
| 8 | 1 | 1011 | 1 |
| 9 | 1 | 0111 | 0 |
| 10 | 0 | 1110 | 0 |
| 11 | 1 | 1101 | 0 |
| 12 | 1 | 1011 | 1 |
@end
@end

@ej lb7-14|Visualizar un dígito BCD recibido en serie|Libro · Cap. 7 · P7.14|registro,desplazamiento,7-segmentos,comparador|lb7.p714
@enun
Visualiza en un display de siete segmentos el dígito BCD que llega **en serie** y sincronizado con un reloj. Si el dígito recibido es erróneo (no es BCD), no debe visualizarse.
@end
@antes
**Registro de desplazamiento + decodificador BCD‑7 segmentos + comparador.** El registro convierte los cuatro bits de la entrada serie en un número de cuatro bits; el decodificador lo muestra; y un comparador vigila que no pase de 9.
@end
@paso Cableado
Las salidas $Q_3..Q_0$ del registro van a las entradas 8‑4‑2‑1 del decodificador y a la entrada $A$ de un comparador cuya entrada $B$ vale $1001$ (9). La salida $A>B$ se lleva a la línea de **apagado** del decodificador (BI), que es activa en bajo: la señal debe llegar invertida (o usarse la salida complementaria) para que el display se apague cuando el número es mayor que 9.
@end
@paso Funcionamiento
Si el número recibido es mayor que 9 se activa BI y el display queda en blanco; si es ≤ 9 se ve el dígito. Se ha comprobado con los 16 valores posibles.
@end
@paso Un matiz
Como el display está conectado al registro, durante la recepción **se ven valores intermedios**: con la entrada 1 0 0 1 (el 9, bit más significativo primero) se verá sucesivamente 1 → 2 → 4 → 9. Solo después del cuarto flanco hay un valor válido. Para un montaje serio convendría un registro de captura en la salida.
@end
@res
| Flanco | Bit recibido | $Q_3Q_2Q_1Q_0$ | Display |
|---|---|---|---|
| 1 | 1 | 0001 | 1 |
| 2 | 0 | 0010 | 2 |
| 3 | 0 | 0100 | 4 |
| 4 | 1 | 1001 | 9 |

Tabla completa: los valores 0000 a 1001 se muestran; 1010 a 1111 dejan el display en blanco.
@end
@end

@ej lb7-15|Nota de un alumno a partir de tres partes de examen|Libro · Cap. 7 · P7.15|registro,desplazamiento,contador,aplicacion|lb7.p715
@enun
Un circuito recibe **en serie** bloques de tres bits: cada bit dice si el alumno ha superado la primera, la segunda y la tercera parte de un examen. Debe encenderse uno solo de tres diodos (o ninguno): NOTA5 si solo se ha superado la primera parte, NOTA7 si se han superado la primera y la segunda, y NOTA10 si se han superado las tres.
@end
@antes
**Registro de desplazamiento y tres puertas AND.** El registro guarda los tres últimos bits recibidos. Si el bit nuevo entra por $Q_0$, tras tres flancos $Q_2$ guarda la primera parte, $Q_1$ la segunda y $Q_0$ la tercera.
@end
@paso Funciones
NOTA10 $=Q_2Q_1Q_0$; NOTA7 $=Q_2Q_1\overline{Q_0}$; NOTA5 $=Q_2\overline{Q_1}\,\overline{Q_0}$. Los inversores no se pueden eliminar: sin ellos, un alumno con las tres partes superadas encendería los tres diodos a la vez.
@end
@paso Defecto de la primera versión
El registro se evalúa en **todos** los flancos, y en los dos que siguen a cada alumno contiene bits de dos alumnos distintos. Con la entrada 0 1 1 | 1 0 0 (el primero no obtiene nota; el segundo aprueba solo la primera parte) los diodos que se encienden son NOTA10 en el flanco 4, NOTA7 en el flanco 5, NOTA5 en el flanco 6: las dos primeras notas son **falsas**, mezcla de dos alumnos.
@end
@paso Solución con contador
Un 74160 cargado con 0001 por LOAD cuenta 1, 2, 3, 1, 2, 3…; una AND de $Q_1$ y $Q_0$ da 1 solo cuando vale 3, es decir, **una vez cada tres flancos**. Esa señal habilita las tres puertas (que pasan a ser de cuatro entradas) y, invertida, activa el LOAD del contador que recarga 1.
@end
@paso Las inicializaciones
Tras INICIO el contador está a **0**, no a 1, y aun así el montaje es correcto: de 0 a 3 hay tres flancos, igual que de 1 a 3 tras la recarga (2 flancos de cuenta más el de carga). Se ha comprobado con 40 alumnos aleatorios: la nota correcta sale una sola vez por alumno y solo en el tercer flanco del bloque.
@end
@res
| Flanco | Bit recibido | Contenido $Q_2Q_1Q_0$ | Diodo encendido (versión sin contador) |
|---|---|---|---|
| 1 | 0 | 000 | — |
| 2 | 1 | 001 | — |
| 3 | 1 | 011 | — |
| 4 | 1 | 111 | NOTA10 |
| 5 | 0 | 110 | NOTA7 |
| 6 | 0 | 100 | NOTA5 |

Con el contador, la secuencia de valores del 74160 es $0,1,2,3,1,2,3,\dots$ y la nota solo se muestra cuando vale 3.

@box ojo | Errata en el libro
En el esquema del libro los rótulos $P1,P2,P3$ de la salida del registro aparecen en un orden que no coincide con el cableado de las puertas (según se lee el dibujo, las puertas de NOTA7 y NOTA5 invierten la línea rotulada $P1$, cuando el enunciado exige invertir la **última** parte). La solución de arriba toma la convención coherente: $Q_2$ es la primera parte, y reproduce la tabla de notas del enunciado.
@end
@end
@end

@ej lb7-16|Multiplexado de cuatro displays de siete segmentos|Libro · Cap. 7 · P7.16|contador,multiplexado,7-segmentos,aplicacion|lb7.p716
@enun
Diseña un circuito que multiplexe sobre cuatro displays de siete segmentos el contenido de cuatro dígitos BCD. Para los cuatro displays hay solo siete líneas de segmentos y cuatro líneas de enable, una por display. El reloj disponible es de 200 Hz.
@end
@antes
**Un solo decodificador BCD‑7 segmentos para los cuatro dígitos, repartido en el tiempo.** Cada $T$ segundos se enciende un display distinto con el dígito que le corresponde; si el cambio es suficientemente rápido el ojo ve los cuatro encendidos a la vez.
@end
@paso Contador de barrido
Un 74160 cuenta 0, 1, 2, 3, 0… porque una NAND de $Q_1$ y $Q_0$ (valor 3) carga 0 con LOAD. Solo se usan sus dos bits bajos.
@end
@paso Selección del dígito
Los cuatro dígitos pasan por **buffers triestado** hacia el decodificador común. Un decodificador 2:4 con $Q_1Q_0$ activa un único enable: el del buffer del dígito que toca y, a la vez, el del transistor que alimenta a su display. El triestado puede sustituirse por un multiplexor 4:1 de cuatro bits.
@end
@paso Frecuencias
Cada display se enciende uno de cada cuatro ciclos: $200\ Hz/4=50\ Hz$ de refresco **por display**, con $T=5$ ms por dígito. No conviene subir mucho la frecuencia de barrido (1 kHz, 1 MHz): los transistores y el propio display no responden. Entre 50 y 100 Hz por display es lo adecuado, por lo que 200 Hz es una buena elección. Es el mismo principio con el que se barre una pantalla de televisión.
@end
@res
| Flanco | Contador | Display activo | Dígito mostrado |
|---|---|---|---|
| 0 | 0 | UNI | 4 |
| 1 | 1 | DEC | 3 |
| 2 | 2 | CEN | 2 |
| 3 | 3 | MIL | 1 |
| 4 | 0 | UNI | 4 |
| 5 | 1 | DEC | 3 |
| 6 | 2 | CEN | 2 |
| 7 | 3 | MIL | 1 |

Con el número 1234 de ejemplo (unidades = 4, decenas = 3, …): en cada flanco hay **exactamente un enable activo** (simulado durante 16 flancos) y el patrón se repite cada cuatro.
@end
@end

@ej lb7-17|Divisor entre 1, 2, 4 u 8 con un registro universal|Libro · Cap. 7 · P7.17|registro,contador,division,aplicacion|lb7.p717
@enun
Diseña un divisor cuyo dividendo es un número binario de 4 bits cargado en un registro y cuyo divisor vale 1, 2, 4 u 8 según cuál de cuatro microinterruptores esté activado. El divisor tiene un interruptor $I$ para marcar el inicio de la división.
@end
@antes
**Dividir por $2^k$ es desplazar $k$ posiciones hacia el bit de menor peso.** Se usa un registro universal 74179 (que carga en paralelo, desplaza e inhibe) y un contador que cuenta los desplazamientos hechos; un comparador dice si ya se han hecho tantos como pide el divisor.
@end
@paso Codificar el divisor
Los cuatro microinterruptores (1, 2, 4, 8) pasan por un codificador 4:2 que da $k$ en dos bits: 1 → 00, 2 → 01, 4 → 10, 8 → 11.
@end
@paso Procedimiento
Se activa INICIO (contador a 0), se pone el dividendo en los cuatro microinterruptores y se da un pulso a CARGA DIVIDENDO. Después se pone $I=1$: mientras el contador es **menor** que $k$ (salida $m$) el registro desplaza y el contador suma uno; al llegar a $k$ se detiene. El cociente queda estable en las salidas $Q_3..Q_0$. Para otra división hay que volver a $I=0$ e INICIO.
@end
@paso Control del registro
Con $C$ = carga, $I$ = división y $m$ = «contador menor que $k$», las líneas $S_1S_0$ valen: $C=1$ → 01 (carga); $C=0,I=1,m=1$ → 11 (desplaza); $C=0,I=1,m=0$ → 10 (inhibe, final); $C=0,I=0$ → 10 (no divide). Por Karnaugh: $S_1=\overline C$ y $S_0=C+I\cdot m$, con $ENP\cdot ENT=I\cdot m$.
@end
@paso Comprobación
Se han probado las $16\cdot4=64$ divisiones posibles: el cociente es siempre $\lfloor dividendo/divisor\rfloor$ y se hacen exactamente $k$ desplazamientos. Los bits que salen por el extremo son el resto, que este circuito **no conserva**.
@end
@res
| $C$ | $I$ | $m$ | $S_1S_0$ | Operación |
|---|---|---|---|---|
| 1 | × | × | 01 | carga el dividendo |
| 0 | 1 | 1 | 11 | desplaza y cuenta |
| 0 | 1 | 0 | 10 | final: inhibe |
| 0 | 0 | × | 10 | no divide |

Ejemplo: dividendo 1101 (13) entre 4 ($k=2$): dos desplazamientos dan $1101\to0110\to0011$, es decir, 3 = $\lfloor13/4\rfloor$ (el resto, 1, sale por la derecha).

@box ojo | Errata en el libro
Dos detalles del libro no concuerdan entre sí: el comentario dice que durante la división $S_1=1$ y $S_0=0$, pero la tabla del propio ejercicio da $S_1S_0=11$ (y $S_0=C+I\cdot m$). Además, la salida del comparador que se usa debe ser «código mayor que contador» (con $A$ = código y $B$ = contador, la salida **M**), mientras que el texto habla de «contador menor» (m). Lo importante es que el registro desplace hacia el bit de menor peso mientras queden desplazamientos por hacer.
@end
@end
@end

@ej lb7-18|Alarma de exceso de velocidad de una rueda|Libro · Cap. 7 · P7.18|contador,74160,74163,aplicacion|lb7.p718
@enun
Un microbot lleva en una rueda cuatro marcas ópticas. Hay que activar una alarma cuando la rueda dé **más de tres vueltas por segundo**. El reloj es de 100 Hz. Diseña el circuito.
@end
@antes
**Medir una frecuencia es contar pulsos durante un intervalo conocido.** Tres vueltas por segundo con cuatro marcas son 12 pulsos por segundo; la alarma debe saltar si en una ventana de 1 s se cuentan más de 12.
@end
@paso Base de tiempos
Dos 74160 en cascada forman un contador de módulo 100 que cuenta los relojes de 100 Hz: la ventana dura 100 relojes, es decir, **1 s**. Cuando los dos valen 9 (99 relojes) una NAND de sus fin‑de‑cuenta borra el contador de pulsos.
@end
@paso Contador de pulsos
Un 74163 (binario de 4 bits) cuenta los pulsos de la rueda. Para que cada marca cuente **una vez** aunque sea larga, la señal de la rueda pasa antes por dos biestables D y una AND ($Q_1\cdot\overline{Q_2}$), el detector de flancos del problema 7.12.
@end
@paso Alarma
Un comparador compara la cuenta con $1100$ (12) y su salida «mayor que» enciende la alarma: se activa en cuanto se supera el 12 y se apaga con el borrado de la siguiente ventana.
@end
@paso Límites
Un pulso de rueda debe durar al menos un periodo de reloj (0,01 s) para ser detectado; si dura menos hay que subir la frecuencia base (1 kHz o más). Como el 74163 es de módulo 16, a partir de 16 pulsos por segundo (4 vueltas por segundo) la cuenta **da la vuelta**: la alarma se enciende al pasar por 13, 14 y 15, pero se apaga cuando el contador vuelve a 0. Para medir velocidades mayores hay que ampliar el módulo conectando más 74163 en cascada.
@end
@res
| Vueltas por segundo | Pulsos por segundo | Cuenta máxima en la ventana | Alarma |
|---|---|---|---|
| 1 | 4 | 4 | no |
| 2 | 8 | 8 | no |
| 2.5 | 10 | 10 | no |
| 3.5 | 14 | 14 | sí |
| 4 | 16 | 15 | sí |
| 5 | 20 | 15 | sí |

Simulación a nivel de reloj durante cuatro ventanas por velocidad (se descarta la primera, de arranque). A 4 y 5 vueltas por segundo el contador ya ha dado la vuelta: la alarma se enciende un instante, pero no queda fija. Con 3 vueltas por segundo la cuenta está justo en el límite (12 pulsos, ±1 por el desfase entre ventana y rueda).
@end
@end

@ej lb7-19|Marcador de tenis con dos pulsadores|Libro · Cap. 7 · P7.19|contador,74163,comparador,aplicacion|lb7.p719
@enun
Diseña un marcador de tenis controlado por dos pulsadores, uno por jugador. En principio basta con un marcador de puntos que tenga en cuenta el empate (iguales) y la ventaja. Los números pueden visualizarse como 0, 1, 2, 3… en lugar de 0, 15, 30, 40.
@end
@antes
**Un contador de puntos por jugador y un circuito que decide cuándo termina el juego.** Un juego se gana al alcanzar **al menos cuatro puntos con una diferencia de al menos dos**.
@end
@paso Entradas
Cada pulsador pasa por un detector de flancos de dos biestables D y una AND, de modo que cada pulsación suma **un único** punto aunque se mantenga pulsada. Cada jugador tiene un 74163; se supone que un juego nunca pasa de 15 puntos.
@end
@paso Quién gana y por cuánto
Un comparador dice cuál de los dos contadores es mayor y dos multiplexores 4×2:1 colocan el mayor como **minuendo** y el menor como **sustraendo**. Un restador calcula la diferencia.
@end
@paso Fin de juego
Un comparador contra $0011$ da $MD=1$ si el mayor supera 3 (tiene al menos 4) y otro contra $0001$ da $MR=1$ si la diferencia supera 1 (es al menos 2). $JUEGO=MD\cdot MR$.
@end
@paso Qué hace JUEGO
Activa, invertida, la línea LOAD de los dos contadores (con $D=0$) para ponerlos a 0; se lleva a un demultiplexor 1:2 que enciende el led del ganador (la señal de «A mayor» elige el led) y podría habilitar un contador de juegos ganados por cada jugador. Todo el circuito comparte la misma línea de reloj.
@end
@paso Comprobación
La lógica combinacional coincide con la regla del tenis para las $16\cdot16=256$ combinaciones de puntos. Además se han simulado 500 partidos aleatorios de 4 a 40 puntos y los juegos (quién gana y con qué tanteo) coinciden con una simulación directa de la regla.
@end
@res
| Puntos A | Puntos B | Mayor | Diferencia | MD | MR | JUEGO |
|---|---|---|---|---|---|---|
| 3 | 0 | 3 | 3 | 0 | 1 | 0 |
| 4 | 0 | 4 | 4 | 1 | 1 | 1 |
| 4 | 2 | 4 | 2 | 1 | 1 | 1 |
| 4 | 3 | 4 | 1 | 1 | 0 | 0 |
| 3 | 3 | 3 | 0 | 0 | 0 | 0 |
| 5 | 3 | 5 | 2 | 1 | 1 | 1 |
| 5 | 4 | 5 | 1 | 1 | 0 | 0 |
| 6 | 4 | 6 | 2 | 1 | 1 | 1 |

Ejemplo con los puntos A A B B A A A B B B B A A B B B (A y B alternan): juegos terminados gana A por 4‑2, gana B por 1‑4.
@end
@end

@ej lb7-20|Contador asíncrono de 0 a 5 con puesta a cero|Libro · Cap. 7 · P7.20|contador,asincrono,glitch,cronograma|lb7.p720
@enun
Diseña un contador **asíncrono** activo por flanco de bajada cuya secuencia sea 0, 1, 2, 3, 4, 5, 0, 1… Completa el cronograma sin tener en cuenta los retardos.
@end
@antes
**Se deja contar libremente hasta el primer estado que no se quiere y se obliga a volver a cero.** Con tres biestables J‑K con $J=K=1$ se tiene un contador asíncrono de módulo 8; el estado 6 (110) es el primero no deseado.
@end
@paso Contador base
Tres J‑K con $J=K=1$: $Ck$ al primero y cada salida $Q$ al reloj del siguiente. Con flancos de bajada así encadenados la cuenta es ascendente de módulo 8.
@end
@paso Recorte
Una puerta NAND decodifica 110 ($Q_2\cdot Q_1\cdot\overline{Q_0}$) y su salida, activa en bajo, se lleva a los **CLEAR** de los tres biestables. En cuanto el contador llega a 6 se pone a 0 de forma asíncrona. La NAND no necesita $\overline{Q_0}$: basta $Q_2\cdot Q_1$, porque el 7 nunca se alcanza (se comprobó que la secuencia es la misma).
@end
@paso El «glitch»
En el flanco que debería llevar el contador de 5 a 6, el contador **llega a tomar el valor 6** durante un breve lapso, el que tarda la NAND y el borrado en actuar. Es un estado transitorio no deseado (un *glitch*) que puede alterar los circuitos que lean las salidas. Por eso estos contadores tienen interés sobre todo teórico.
@end
@res
@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "00000000111111110000000011111111000000001111111100000000111111110000"], ["Q1", "00000000000000001111111111111111000000000000000000000000000000001111"], ["Q2", "00000000000000000000000000000000111111111111111100000000000000000000"], ["Clear", "00000000000000000000000000000000000000000000000010000000000000000000"]], "title": "Cuenta 0‑5 (el pulso «Clear» está exagerado en anchura)", "rh": 28, "w_slot": 8, "grid": 8}

Secuencia: 0 → 1 → 2 → 3 → 4 → 5 → 0. En cada vuelta aparece el estado transitorio 6 (110) antes de volver a 0.
@end
@end

@ej lb7-21|Contador BCD asíncrono con flancos de bajada|Libro · Cap. 7 · P7.21|contador,asincrono,bcd,glitch,cronograma|lb7.p721
@enun
Diseña un contador ascendente BCD **asíncrono** activo por flanco de bajada y completa el cronograma, sin tener en cuenta los retardos.
@end
@antes
**Mismo método que el problema anterior con cuatro biestables.** Un contador asíncrono ascendente de cuatro J‑K con $J=K=1$ es de módulo 16; se decodifica el primer estado que no es BCD, 1010, y se lleva a los CLEAR.
@end
@paso Decodificar el 10
NAND de $Q_3\cdot\overline{Q_2}\cdot Q_1\cdot\overline{Q_0}$ hacia los cuatro CLEAR. Basta con $Q_3\cdot Q_1$ (en una cuenta de 0 a 9 solo el 10 las cumple primero); el libro lo señala y la simulación lo confirma.
@end
@paso Resultado
El contador pasa por 0, 1, …, 9 y, al llegar a 10, vuelve a 0. Como en el caso anterior hay un instante en que el contador vale 10 antes del borrado (glitch).
@end
@paso Comprobación
Se simula el encadenamiento de flancos con retardo cero entre biestables: se comprueba que durante los rizados no se cumple la condición de borrado en ningún estado intermedio salvo en el 10.
@end
@res
@fig cron {"signals": [["Ck", "0000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "0000000011111111000000001111111100000000111111110000000011111111000000001111111100000000111111110000"], ["Q1", "0000000000000000111111111111111100000000000000001111111111111111000000000000000000000000000000001111"], ["Q2", "0000000000000000000000000000000011111111111111111111111111111111000000000000000000000000000000000000"], ["Q3", "0000000000000000000000000000000000000000000000000000000000000000111111111111111100000000000000000000"], ["Clear", "0000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000"]], "title": "Cuenta BCD asíncrona", "rh": 26, "w_slot": 7, "grid": 8}

Secuencia: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 0.
@end
@end

@ej lb7-22|Secuencia de un contador asíncrono con preset|Libro · Cap. 7 · P7.22|contador,asincrono,preset,cronograma|lb7.p722
@enun
Tres biestables J‑K con $J=K=1$ están conectados así: el reloj $Ck$ va al primero, la salida $Q_0$ al reloj del segundo y $Q_1$ al reloj del tercero, todos activos por flanco de **subida**. Una puerta NAND recibe $\overline{Q_2}$, $Q_1$ y $\overline{Q_0}$ y su salida va a los **PRESET** de los tres. Indica la secuencia que genera y completa el cronograma, sin tener en cuenta los retardos.
@end
@antes
**Es un circuito secuencial asíncrono, un contador.** Hay que decidir si cuenta hacia arriba o hacia abajo, cuál es su módulo máximo y qué hace la puerta.
@end
@paso Sentido
Cada $Q$ va al reloj del siguiente y el reloj es de subida: el contador es **descendente** (la salida del primero sube cuando le toca bajar al segundo: 7, 6, 5, …).
@end
@paso Máximo
Con tres biestables el módulo máximo es 8.
@end
@paso La puerta
La NAND decodifica $\overline{Q_2}\,Q_1\,\overline{Q_0}=010$, el valor **2**, que es el primer estado no deseado de la cuenta descendente. Su salida va a los PRESET: fuerza **111 = 7**.
@end
@paso Resultado
El contador se recorta a 5 estados y genera 7, 6, 5, 4, 3, 7, 6, … Es un contador asíncrono descendente de **módulo 5**. En cada vuelta aparece brevemente el 2 antes del preset (glitch).
@end
@res
@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000111100001111000011110000"], ["Q0", "11110000000011111111000000001111111111111111000000001111111100000000"], ["Q1", "11111111111100000000000000001111111111111111111111110000000000000000"], ["Q2", "11111111111111111111111111110000000011111111111111111111111111111111"], ["Preset", "00000000000000000000000000000000000010000000000000000000000000000000"]], "title": "Cuenta asíncrona descendente módulo 5", "rh": 28, "w_slot": 8, "grid": 8}

Secuencia: 7 → 6 → 5 → 4 → 3 → 7 (y se repite).

@box ojo | Errata en el libro
En el último punto del comentario el libro llama a este contador «ascendente de módulo 5», pero la secuencia que escribe a continuación (7, 6, 5, 4, 3, 7) es **descendente**, como dice él mismo unas líneas antes.
@end
@end
@end

