%% id=libro6
%% group=ejer
%% n=3.6
%% title=Libro de problemas · Capítulo 6 · Biestables
%% short=Libro · Cap. 6 Biestables
%% sub=Quince problemas de cronogramas y análisis de biestables R‑S, J‑K, D, T, maestro/esclavo y latch: cada cronograma sale de una simulación con puertas.

@box idea | Cómo se leen los cronogramas de esta sección
Son los problemas resueltos del capítulo 6 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y con entradas dibujadas sobre una **cuadrícula de ranuras de tiempo** (cada línea vertical está separada cuatro ranuras; un semiperíodo de reloj son 4 ranuras). La teoría está en [[t06|el tema 6]].

Convenio de los dibujos:
- **Banda gris clara**: valor desconocido a priori (la salida se ha parado, pero no se sabe en qué valor).
- **Banda gris oscura**: carrera (la salida bascula sin parar mientras dura la condición).
- **Trazo grueso**: entrada prohibida en ese momento.
- En un flanco se toma el valor de las entradas **justo antes** de él.

Cada latch (R‑S, J‑K, D, y los maestros/esclavos) se ha simulado como una red de puertas NAND: las puertas se disparan en cualquier orden y, si el resultado final depende de quién gana, la salida se marca como desconocida. Las carreras se detectan cuando la combinación J=K=1 realimenta la salida mientras el nivel está activo. Los flip‑flops por flanco se simulan con su tabla de excitación. Así los cronogramas no se dibujan a mano: salen del simulador y se contrastan con el razonamiento. Si el libro tiene un fallo, aparece en un recuadro de errata.
@end

@ej lb6-1|Báscula R‑S asíncrona con puertas NAND|Libro · Cap. 6 · P6.1|biestable,rs,cronograma|lb6.p61
@enun
Completa los dos cronogramas de una báscula R‑S asíncrona hecha con dos puertas NAND (entradas activas en bajo, $\overline S$ y $\overline R$). Marca con trazo grueso cuándo la entrada está prohibida y en gris cuándo no se puede saber el valor de salida.

@fig cron {"signals": [["S̄", "11100011110000111110"], ["R̄", "11111111110000000001"]], "title": "Primer cronograma: entradas", "rh": 40, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["S̄", "11110001111111000111"], ["R̄", "11111111110000000111"]], "title": "Segundo cronograma: entradas", "rh": 40, "w_slot": 12, "grid": 4}
@end
@antes
**Una tabla de cuatro filas basta.** Con $Q=\overline{\overline S\cdot\overline Q}$ y $\overline Q=\overline{\overline R\cdot Q}$: $\overline S\,\overline R=11$ mantiene; $01$ pone Q a 1; $10$ pone Q a 0; $00$ es la combinación prohibida y deja **las dos salidas a 1**.
@end
@paso Reglas
| $\overline S$ | $\overline R$ | Operación | Q | $\overline Q$ |
|---|---|---|---|---|
| 1 | 1 | mantiene | Q | $\overline Q$ |
| 0 | 1 | puesta a 1 | 1 | 0 |
| 1 | 0 | puesta a 0 | 0 | 1 |
| 0 | 0 | prohibida | 1 | 1 |
@end
@paso Primer cronograma
Q se pone a 1 con el primer pulso bajo de $\overline S$ y se mantiene. Cuando $\overline R$ baja mientras $\overline S$ también está bajo, la entrada es prohibida y las dos salidas valen 1 (trazo grueso). En cuanto $\overline S$ sube y $\overline R$ sigue bajo, Q pasa a 0: sale de la prohibida por **un solo lado**, y el resultado es único. Al final, $\overline R$ sube y $\overline S$ baja: Q vuelve a 1.
@end
@paso Segundo cronograma
Tras la puesta a 1 y la puesta a 0, las dos entradas bajan **a la vez** (prohibida: $Q=\overline Q=1$) y después suben también **a la vez**. Las dos puertas ven ahora «1, 1» y compiten: la que gane se queda a 0 y la otra a 1, pero no se sabe cuál. La salida queda desconocida (banda gris) hasta la siguiente puesta a 0 o a 1.
@end
@paso Qué enseña
Pasar de $00$ a $11$ por un solo lado es seguro; hacerlo por los dos a la vez deja la báscula en un estado imprevisible. Sea cual sea el estropicio (prohibida, desconocida), una orden clara de puesta a 0 o a 1 devuelve la báscula a la normalidad.
@end
@res
@fig cron {"signals": [["S̄", "11100011110000111110"], ["R̄", "11111111110000000001"], ["Q", "00011111111111000001", "..........####......"], ["Q̄", "11100000001111111110", "..........####......"]], "title": "Cronograma 1", "rh": 34, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["S̄", "11110001111111000111"], ["R̄", "11111111110000000111"], ["Q", "00001111110000111xxx", "..............###..."], ["Q̄", "11110000001111111xxx", "..............###..."]], "title": "Cronograma 2", "rh": 34, "w_slot": 12, "grid": 4}

En el primero toda la evolución es determinista (con una fase prohibida); en el segundo, la salida queda desconocida tras salir de la prohibida por los dos lados a la vez.
@end
@end

@ej lb6-2|Báscula J‑K asíncrona: normal, con carreras y con indeterminación|Libro · Cap. 6 · P6.2|biestable,jk,carreras,cronograma|lb6.p62
@enun
Completa los tres cronogramas de una báscula J‑K **asíncrona** (sin reloj: J y K actúan directamente sobre la salida). Señala dónde hay carreras (gris oscuro) y dónde la salida queda desconocida (gris claro).

@fig cron {"signals": [["J", "001110000111000001110000"], ["K", "000000000000111100000111"]], "title": "Cronograma 1: entradas", "rh": 40, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["J", "00011100011100000001111000"], ["K", "00000000000000111111111111"]], "title": "Cronograma 2: entradas", "rh": 40, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["J", "00111000111000001111100000"], ["K", "00000000000011111111100000"]], "title": "Cronograma 3: entradas", "rh": 40, "w_slot": 12, "grid": 4}
@end
@antes
**Sin reloj no hay nada que la proteja:** un J‑K asíncrono con $J=K=1$ realimenta su propia salida y bascula sin parar. Eso es una carrera. Cuando termina, si lo hace en $00$, la salida queda parada en un valor desconocido; si termina en $10$ o $01$, el valor es el de esa orden.
@end
@paso Reglas
| J | K | Efecto |
|---|---|---|
| 0 | 0 | mantiene |
| 1 | 0 | Q = 1 |
| 0 | 1 | Q = 0 |
| 1 | 1 | carrera: Q bascula continuamente |
@end
@paso Cronograma 1
Nunca coinciden J y K: la evolución es normal. Cada pulso de J pone Q a 1 y cada pulso de K lo pone a 0; los pulsos de J con Q ya a 1 no cambian nada.
@end
@paso Cronograma 2
En la parte final J sube mientras K sigue a 1: $JK=11$ y la salida entra en carreras. Cuando J baja queda $JK=01$ y Q se queda en **0**, sin ambigüedad: se sale de la carrera por un solo lado. En el dibujo el basculeo se ve lento y ordenado, pero en realidad se produce a una frecuencia de megahercios, con efectos muy malos sobre el resto del circuito.
@end
@paso Cronograma 3
Se repite la carrera, pero ahora J y K bajan **a la vez** (de $11$ a $00$). No se sabe en qué momento exacto se paró la oscilación, así que la salida queda parada en un valor desconocido hasta la siguiente orden. Evolución completa: normal, mala (carreras), peor (indeterminación) y, con una orden nueva, otra vez normal.
@end
@res
@fig cron {"signals": [["J", "001110000111000001110000"], ["K", "000000000000111100000111"], ["Q", "001111111111000001111000"], ["Q̄", "110000000000111110000111"]], "title": "Cronograma 1", "rh": 34, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["J", "00011100011100000001111000"], ["K", "00000000000000111111111111"], ["Q", "0001111111111100000rrrr000"], ["Q̄", "1110000000000011111rrrr111"]], "title": "Cronograma 2", "rh": 34, "w_slot": 12, "grid": 4}

@fig cron {"signals": [["J", "00111000111000001111100000"], ["K", "00000000000011111111100000"], ["Q", "0011111111110000rrrrrxxxxx"], ["Q̄", "1100000000001111rrrrrxxxxx"]], "title": "Cronograma 3", "rh": 34, "w_slot": 12, "grid": 4}

Las dos salidas son siempre complementarias salvo en las bandas grises, donde ninguna de las dos tiene un valor utilizable.
@end
@end

@ej lb6-3|R‑S síncrona por nivel alto y por nivel bajo|Libro · Cap. 6 · P6.3|biestable,rs,nivel,cronograma|lb6.p63
@enun
Completa el cronograma de dos biestables R‑S síncronos: $Q_{NA}$, activo con el reloj a nivel alto, y $Q_{NB}$, activo con el reloj a nivel bajo.

@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["S", "000000000001111111111111110000000000"], ["R", "000000000000011111000011111111111111"]], "title": "Entradas", "rh": 40, "w_slot": 12, "grid": 4}
@end
@antes
**Un síncrono por nivel es un asíncrono con una puerta que se abre y se cierra.** Mientras el reloj está en su nivel activo, S y R actúan como en la báscula asíncrona; fuera de él, la salida se mantiene. Se usa la realización clásica con NAND: con $S=R=1$ activos las dos salidas valen 1 (prohibido).
@end
@paso Nivel alto ($Q_{NA}$)
Primer pulso: $S=0$, $R=0$, se mantiene (0). Segundo pulso: S pasa a 1 y R a 1 un poco después: primero Q=1 y luego **prohibido** (trazo grueso). Al bajar el reloj, la puerta se cierra con $S=R=1$: las dos salidas quedan desconocidas (gris). El tercer pulso empieza con $S=1$, $R=0$: Q=1; de nuevo R sube y sale otra prohibida, que al cerrar el reloj deja otra vez la salida desconocida. En el cuarto pulso $S=0$, $R=1$ y Q se pone a 0.
@end
@paso Nivel bajo ($Q_{NB}$)
Es lo mismo con el reloj invertido. Q pasa a 1 cuando $S=1$ y $R=0$ con el reloj a nivel bajo. Cuando R sube aparece una prohibida breve (las dos salidas a 1) que se deshace por un solo lado (R baja) y Q sigue en 1. Después, con el reloj bajo, vuelve a haber $S=R=1$, y termina por un solo lado (cae S): Q pasa a 0 sin ambigüedad. Como las dos prohibidas **terminan por un solo lado**, la salida no queda desconocida.
@end
@paso Qué enseña
Añadir sincronismo por nivel a un R‑S no lo mejora, lo empeora: hay más ocasiones de situaciones prohibidas y de indeterminación a la salida.
@end
@res
@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["S", "000000000001111111111111110000000000"], ["R", "000000000000011111000011111111111111"], ["Q_NA", "0000000000001111xxxx1111xxxx00000000", ".............###......##............"], ["Q_NB", "000000000001111111111111110000000000", "................##......##.........."]], "title": "R‑S por nivel", "rh": 34, "w_slot": 10, "grid": 4}

Trazo grueso: entrada prohibida con la puerta abierta. Gris claro: salida desconocida a priori.
@end
@end

@ej lb6-4|R‑S síncrona por flanco ascendente y por flanco descendente|Libro · Cap. 6 · P6.4|biestable,rs,flanco,cronograma|lb6.p64
@enun
Con las mismas entradas que el problema anterior, completa el cronograma de dos biestables R‑S síncronos por flanco: $Q_\uparrow$ (flanco de subida) y $Q_\downarrow$ (flanco de bajada).
@end
@antes
**En un flanco solo importa una cosa:** el valor de $S$ y $R$ justo antes de él. Si es $00$, mantiene; $10$ pone a 1; $01$ pone a 0; $11$ deja la salida **desconocida** hasta el siguiente flanco que dé una orden clara.
@end
@paso Flanco de subida
Los cuatro flancos de subida encuentran $SR=00$ (mantiene), $10$ (pone a 1), $10$ (sigue a 1) y $01$ (pone a 0). Ninguno coincide con $11$, así que la evolución es normal.
@end
@paso Flanco de bajada
Los cuatro flancos de bajada encuentran $SR=00$ (mantiene), $11$, $11$ y $01$. Con el primer $11$ la salida queda desconocida y con el segundo sigue desconocida; solo se aclara con el último flanco, que trae $S=0$, $R=1$ y pone Q a 0.
@end
@paso Qué enseña
Al añadir el sincronismo por flanco a un R‑S, toda situación prohibida genera directamente una salida indeterminada. El sincronismo ha **degradado** al R‑S.
@end
@res
@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["S", "000000000001111111111111110000000000"], ["R", "000000000000011111000011111111111111"], ["Q↑", "000000000000111111111111111100000000"], ["Q↓", "0000000000000000xxxxxxxxxxxxxxxx0000"]], "title": "R‑S por flanco", "rh": 34, "w_slot": 10, "grid": 4}

Gris claro: salida desconocida a priori. Los flancos de bajada de este ejemplo son justo los que caen sobre $SR=11$.
@end
@end

@ej lb6-5|J‑K síncrona por nivel alto y por nivel bajo|Libro · Cap. 6 · P6.5|biestable,jk,nivel,cronograma|lb6.p65
@enun
Con las mismas entradas ($J$ en lugar de $S$ y $K$ en lugar de $R$), completa el cronograma de dos J‑K síncronos por nivel: $Q_{NA}$ (nivel alto) y $Q_{NB}$ (nivel bajo).

@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["J", "000000000001111111111111110000000000"], ["K", "000000000000011111000011111111111111"]], "title": "Entradas", "rh": 40, "w_slot": 12, "grid": 4}
@end
@antes
**$JK=11$ ya no es «prohibida» sino «bascula».** Pero si el nivel activo dura más que el retardo de las puertas, la salida cambia más de una vez: carrera. Al terminar el nivel, la salida queda parada en un valor imposible de predecir.
@end
@paso Nivel alto ($Q_{NA}$)
Con $J=1$, $K=0$ al principio del segundo pulso, Q pasa a 1; cuando K sube se da $JK=11$ con el reloj alto: **carrera** durante el resto del nivel; al bajar el reloj, la salida queda desconocida. En el siguiente pulso, $J=1$, $K=0$ pone Q a 1 de forma determinista y poco después K sube otra vez: otra carrera y otra indeterminación. Al final, con $J=0$, $K=1$, Q a 0.
@end
@paso Nivel bajo ($Q_{NB}$)
La primera vez que coinciden $J=K=1$ con el reloj bajo (carrera breve) se sale con $J=1$, $K=0$ y Q queda a 1. La segunda vez termina con $J=0$, $K=1$ y Q se pone a 0: las dos carreras se resuelven por un solo lado.
@end
@paso Qué enseña
Igual que con el R‑S, el sincronismo por nivel degrada al J‑K: aparece la indeterminación con mucha más facilidad.
@end
@res
@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["J", "000000000001111111111111110000000000"], ["K", "000000000000011111000011111111111111"], ["Q_NA", "0000000000001rrrxxxx11rrxxxx00000000"], ["Q_NB", "0000000000011111rr111111rr0000000000"]], "title": "J‑K por nivel", "rh": 34, "w_slot": 10, "grid": 4}

Gris oscuro: carreras. Gris claro: salida desconocida a priori.
@end
@end

@ej lb6-6|J‑K síncrona por flanco ascendente y descendente|Libro · Cap. 6 · P6.6|biestable,jk,flanco,cronograma|lb6.p66
@enun
Completa el cronograma de dos J‑K síncronos por flanco: $Q_\uparrow$ (flanco de subida) y $Q_\downarrow$ (flanco de bajada), con las mismas entradas que el problema anterior.
@end
@antes
**Un flanco es un instante, y un instante no puede tener carrera.** En cada flanco se mira $JK$ y se aplica la tabla (00 mantiene, 10 pone a 1, 01 pone a 0, 11 invierte). Entre flancos, la salida no se entera de nada.
@end
@paso Flanco de subida
Los cuatro flancos de subida encuentran $JK=00$, $10$, $10$ y $01$: nada, Q a 1, Q sigue a 1 y Q a 0. La salida sube en el primer flanco con $J=1$ y baja en el último.
@end
@paso Flanco de bajada
Aquí llegan $JK=00$, $11$, $11$ y $01$: nada, **inversión** (Q pasa a 1), **inversión** (Q vuelve a 0, de ahí el pulso corto) y 0. Es la única vez en el capítulo en que el $11$ hace algo con sentido.
@end
@paso Qué enseña
El sincronismo por flanco le ha sentado bien al J‑K: **no hay carreras ni indeterminaciones**, solo una inversión por flanco con $JK=11$. Es el J‑K que se usa en la práctica; el R‑S y el J‑K por nivel y el R‑S por flanco solo tienen interés teórico.
@end
@res
@fig cron {"signals": [["Ck", "000011110000111100001111000011110000"], ["J", "000000000001111111111111110000000000"], ["K", "000000000000011111000011111111111111"], ["Q↑", "000000000000111111111111111100000000"], ["Q↓", "000000000000000011111111000000000000"]], "title": "J‑K por flanco", "rh": 34, "w_slot": 10, "grid": 4}

@box ojo | Errata en el libro
El primer comentario del libro afirma que «el J‑K síncrono por nivel no presenta situaciones ni de carreras ni indeterminadas». Es al revés: el J‑K por nivel del problema anterior sí las presenta; lo que no las tiene es el J‑K **por flanco**. Es una errata de palabra.
@end
@end
@end

@ej lb6-7|Maestro/esclavo J‑K en sus dos versiones|Libro · Cap. 6 · P6.7|biestable,jk,maestro-esclavo,cronograma|lb6.p67
@enun
Completa el cronograma de dos biestables J‑K maestro/esclavo. En el primero (versión A) el maestro es activo con el reloj a nivel alto y el esclavo a nivel bajo; en el segundo (versión B), al revés.

El maestro es un R‑S síncrono por nivel cuyas entradas son $S_M=J\cdot\overline{Q_S}$ y $R_M=K\cdot Q_S$; el esclavo es otro R‑S síncrono por nivel, con el nivel contrario, cuyas entradas son $S_S=Q_M$ y $R_S=\overline{Q_M}$. La salida del conjunto es $Q_S$.

@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000"], ["J", "00000111111111111000000000111111111111111111"], ["K", "00000000000000000001111111111111111111000000"]], "title": "Entradas", "rh": 34, "w_slot": 9, "grid": 4}
@end
@antes
**El maestro piensa y el esclavo copia.** En cada semiperíodo solo uno de los dos está abierto: mientras el maestro mira a J y K, el esclavo duerme, y al revés. Las dos tareas se separan en el tiempo, y por eso no hay carreras ni indeterminaciones.
@end
@paso Qué hace el maestro
Con $JK=00$ mantiene $Q_M$. Con $JK=11$ **toma el opuesto del esclavo**: $Q_M=\overline{Q_S}$ (por eso se realimenta $Q_S$). Con $10$ y $01$ se pone a 1 o a 0 si el esclavo no lo tiene ya así.
@end
@paso Versión A
El maestro mira durante el nivel alto; el esclavo copia durante el nivel bajo siguiente. $Q_M$ sube en el primer pulso (con $J=1$), el esclavo lo copia al bajar el reloj, $Q_M$ baja con $K=1$, el esclavo lo copia, etc. La salida $Q_S$ cambia en los flancos de bajada.
@end
@paso Versión B
Igual con los niveles intercambiados. La salida $Q_S$ cambia en los flancos de subida y es **idéntica** a la de un J‑K por flanco ascendente. En el dibujo se ha superpuesto $Q_\uparrow$ para comprobarlo.
@end
@paso El caso difícil
En el último pulso alto de la versión A cambian J y K **durante el nivel activo del maestro**: primero $JK=11$ (el maestro toma el opuesto de $Q_S=1$, es decir, 0) y luego $JK=10$. Con $JK=10$: $S_M=1\cdot\overline{Q_S}=0$ y $R_M=0\cdot Q_S=0$, el maestro **mantiene su 0**, y por eso $Q_S$ copia 0, no 1. Un J‑K por flanco de bajada habría visto $JK=10$ en el flanco y habría puesto 1: ahí **no coinciden**. La equivalencia M/S ≡ J‑K por flanco solo es obligada si J y K no cambian durante el nivel activo del maestro.
@end
@res
@fig cron {"signals": [["Ck", "00001111000011110000111100001111000011110000"], ["J", "00000111111111111000000000111111111111111111"], ["K", "00000000000000000001111111111111111111000000"], ["Q_M (A)", "00000111111111111111000000001111111100000000"], ["Q_S (A)", "00000000111111111111111100000000111111110000"], ["Q↓ (J‑K)", "00000000111111111111111100000000111111111111"], ["Q_M (B)", "00000000111111111110000000111111000000001111"], ["Q_S (B)", "00000000000011111111000000001111111100000000"], ["Q↑ (J‑K)", "00000000000011111111000000001111111100000000"]], "title": "Maestro/esclavo", "rh": 30, "w_slot": 9, "grid": 4}

La salida del conjunto es la del esclavo. En la versión A, $Q_S$ y $Q_\downarrow$ solo difieren en el último tramo (el caso difícil); en la versión B coinciden siempre.
@end
@end

@ej lb6-8|Dos maestros/esclavos J‑K y sus equivalentes por flanco|Libro · Cap. 6 · P6.8|biestable,jk,maestro-esclavo,cronograma|lb6.p68
@enun
Completa los dos cronogramas con cuidado. En el primero el maestro es activo con el reloj a nivel bajo y el esclavo a nivel alto; en el segundo, al revés. Añade en cada uno la salida del J‑K síncrono por flanco que corresponda.

@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J", "11110000000011111111100001111000"], ["K", "00000000000011111111100000000000"]], "title": "Cronograma 1: entradas", "rh": 34, "w_slot": 10, "grid": 4}

@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J", "11111111100000000000000001000000"], ["K", "00000000011111111111100111110000"]], "title": "Cronograma 2: entradas", "rh": 34, "w_slot": 10, "grid": 4}
@end
@antes
**Hay que ir paso a paso** porque el maestro depende de la salida del esclavo y el esclavo del maestro: $S_M=J\overline{Q_S}$, $R_M=K\,Q_S$. No se resuelve primero todo el maestro y luego todo el esclavo, sino a la vez, semiperíodo a semiperíodo.
@end
@paso Cronograma 1
El maestro (nivel bajo) ve a $J=1$ al principio y pone $Q_M=1$; el esclavo lo copia en el primer nivel alto. Con $JK=11$ en el nivel bajo siguiente, el maestro toma el opuesto del esclavo (0), y el esclavo lo copia después. Luego queda a 0 hasta que J sube con $K=0$. La salida $Q_S$ cambia **en los flancos de subida**.
@end
@paso Cronograma 2
Maestro de nivel alto. Pone $Q_M=1$ mientras J vale 1 y K 0, y se pone a 0 cuando K sube. El esclavo copia en el nivel bajo siguiente; los pequeños pulsos de J y K que caen con el maestro cerrado no tienen ningún efecto. $Q_S$ cambia **en los flancos de bajada**.
@end
@paso Equivalencias
Un maestro/esclavo con maestro de nivel bajo equivale a un J‑K por flanco ascendente, y con maestro de nivel alto a un J‑K por flanco descendente: en los dos cronogramas la salida del esclavo y la del J‑K por flanco coinciden. Pero eso solo vale mientras J y K no cambien durante el nivel activo del maestro.
@end
@res
@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J", "11110000000011111111100001111000"], ["K", "00000000000011111111100000000000"], ["Q_M", "11111111111111000000000001111111"], ["Q_S", "00111111111111111100000000011111"], ["Q↑", "00111111111111111100000000011111"]], "title": "Cronograma 1: maestro bajo, esclavo alto", "rh": 34, "w_slot": 10, "grid": 4}

@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J", "11111111100000000000000001000000"], ["K", "00000000011111111111100111110000"], ["Q_M", "00111111110000000000000000000000"], ["Q_S", "00000011111111000000000000000000"], ["Q↓", "00000011111111000000000000000000"]], "title": "Cronograma 2: maestro alto, esclavo bajo", "rh": 34, "w_slot": 10, "grid": 4}
@end
@end

@ej lb6-9|Báscula D por flanco y latch D por nivel|Libro · Cap. 6 · P6.9|biestable,d,latch,cronograma|lb6.p69
@enun
Completa los cronogramas de una báscula D síncrona por flanco (de subida, $Q_\uparrow$, y de bajada, $Q_\downarrow$) y de una báscula D síncrona por nivel (un latch o cerrojo, $Q_{NA}$) cuya señal de reloj es una línea ENABLE aperiódica.

@fig cron {"signals": [["Ck", "0000111100001111000011110000111100001111000011110000"], ["D", "0000001111111100000111000011111111000110000000011111"]], "title": "Por flanco: entradas", "rh": 30, "w_slot": 7, "grid": 4}

@fig cron {"signals": [["Enable", "0001111111111000000000000011111110000001111111111"], ["D", "1110011011100111001110011100110110011010011011101"]], "title": "Latch: entradas", "rh": 30, "w_slot": 7, "grid": 4}
@end
@antes
**Una báscula D no puede tener situaciones prohibidas ni indeterminadas** sea cual sea el sincronismo: solo tiene una entrada. Por flanco copia a D en ese instante; por nivel copia a D mientras esté abierta y lo guarda cuando se cierra.
@end
@paso Por flanco
Se anota el valor de D justo antes de cada flanco: en $Q_\uparrow$ sale 0, 1, 1, 1, **0** (D baja justo antes del quinto flanco) y 0; en $Q_\downarrow$ sale 1, 0, 0, 1, 0, 1. Los cambios de D entre flancos no se ven.
@end
@paso Latch
Mientras ENABLE vale 1 la salida **sigue** a D, con todos sus pulsos cortos; cuando ENABLE baja, la salida se queda con el último valor de D. Se parece a la anterior solo en el nombre: aquí cada glitch de D con ENABLE alto llega a la salida.
@end
@paso Comprobación
El latch D se simuló también como un R‑S con puertas NAND con $S=D$, $R=\overline D$ y una puerta de habilitación: da la misma salida. Y no hay indeterminaciones, porque $S$ y $R$ nunca valen 1 a la vez.
@end
@res
@fig cron {"signals": [["Ck", "0000111100001111000011110000111100001111000011110000"], ["D", "0000001111111100000111000011111111000110000000011111"], ["Q↑", "0000000000001111111111111111111111110000000000000000"], ["Q↓", "0000000011111111000000000000000011111111000000001111"]], "title": "D por flanco", "rh": 30, "w_slot": 7, "grid": 4}

@fig cron {"signals": [["Enable", "0001111111111000000000000011111110000001111111111"], ["D", "1110011011100111001110011100110110011010011011101"], ["Q_NA", "0000011011100000000000000000110111111110011011101"]], "title": "Latch D (ENABLE aperiódica)", "rh": 30, "w_slot": 7, "grid": 4}

Una línea ENABLE aperiódica y no un reloj: por eso se habla de latch o cerrojo, y no de biestable.
@end
@end

@ej lb6-10|Un mismo cronograma para J‑K y para R‑S de todos los sincronismos|Libro · Cap. 6 · P6.10|biestable,jk,rs,cronograma|lb6.p610
@enun
Completa el cronograma dado. Las dos entradas se aplican a un J‑K (J, K) y a un R‑S (S=J, R=K). Para cada uno hay que dibujar la salida de las versiones por nivel alto ($Q_{NA}$), por nivel bajo ($Q_{NB}$), por flanco de subida ($Q_\uparrow$) y por flanco de bajada ($Q_\downarrow$); en el R‑S, además, las de maestro/esclavo con maestro a nivel alto ($Q_{MS(NA)}$) y bajo ($Q_{MS(NB)}$).

@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J ó S", "11111111000000000000000001110000"], ["K ó R", "00000000111111111110011111000000"]], "title": "Entradas", "rh": 34, "w_slot": 10, "grid": 4}
@end
@antes
**Es el mismo método ocho veces.** Para cada dispositivo se aplica la regla que corresponde: por nivel, lo que valgan las entradas mientras esté abierto; por flanco, lo que valgan justo antes del flanco; maestro/esclavo, el nivel activo del maestro y luego la copia del esclavo.
@end
@paso J‑K
Solo coinciden $J=K=1$ una vez, con el reloj a nivel bajo: el J‑K de nivel bajo entra en carrera una ranura (de ahí la banda oscura) y, como J se queda en 1 después, se resuelve poniéndose a 1. Los demás dispositivos no ven nunca $JK=11$.
@end
@paso R‑S
La misma situación $S=R=1$ con el R‑S de nivel bajo es una combinación prohibida (las dos salidas valen 1) y también se sale por un solo lado: Q queda a 1 sin ambigüedad, igual que en el J‑K. El resto de dispositivos coincide con sus equivalentes de J‑K.
@end
@paso Equivalencias
La salida del R‑S maestro/esclavo con maestro a nivel alto coincide con la del R‑S por flanco de bajada ($Q_\downarrow$), y con maestro a nivel bajo con la de flanco de subida ($Q_\uparrow$). Las versiones por nivel alto de J‑K y R‑S coinciden aquí con $Q_\uparrow$ de J‑K porque en los niveles altos no se dan ni $JK=11$ ni $SR=11$.
@end
@res
@fig cron {"signals": [["Ck", "00111100001111000011110000011111"], ["J ó S", "11111111000000000000000001110000"], ["K ó R", "00000000111111111110011111000000"], ["JK Q_NA", "00111111110000000000000000011111"], ["JK Q_NB", "1111111100000000000000000r111111"], ["JK Q↑", "00111111110000000000000000011111"], ["JK Q↓", "00000011111111000000000000000000"], ["RS Q_NA", "00111111110000000000000000011111"], ["RS Q_NB", "11111111000000000000000001111111", ".........................#......"], ["RS Q_MS(NA)", "00000011111111000000000000000000"], ["RS Q↓", "00000011111111000000000000000000"], ["RS Q_MS(NB)", "00111111110000000000000000011111"], ["RS Q↑", "00111111110000000000000000011111"]], "title": "Todos los sincronismos", "rh": 28, "w_slot": 10, "grid": 4}

Gris oscuro: carreras. Trazo grueso: entrada prohibida. Los R‑S maestro/esclavo y por flanco dan la misma salida cuando las entradas no cambian durante el nivel activo del maestro.
@end
@end

@ej lb6-11|R‑S y J‑K con prohibidas, carreras e indeterminaciones|Libro · Cap. 6 · P6.11|biestable,jk,rs,cronograma|lb6.p611
@enun
Completa el cronograma para biestables R‑S (S=J, R=K) y J‑K. Señala con trazo grueso lo prohibido, con gris oscuro las carreras y con gris claro lo desconocido. Hay que dibujar las salidas de nivel alto ($Q_{NA}$), nivel bajo ($Q_{NB}$), flanco de subida ($Q_\uparrow$) y, para el R‑S, flanco de bajada ($Q_\downarrow$).

@fig cron {"signals": [["Ck", "001111000011110000111100001111"], ["J ó S", "000000000000111111110000111000"], ["K ó R", "001111110000111100000011111110"]], "title": "Entradas", "rh": 34, "w_slot": 10, "grid": 4}
@end
@antes
**Es el cronograma más completo del capítulo:** en él aparecen las prohibidas del R‑S, las carreras del J‑K por nivel y las indeterminaciones de los dos. Se resuelve igual que los anteriores, fila a fila y con cuidado, porque un fallo se arrastra a lo largo de todo el cronograma.
@end
@paso R‑S por nivel alto
En el segundo pulso S y R suben a la vez con el reloj alto: prohibida (las dos salidas a 1). Al cerrarse el reloj con $SR=11$ la salida queda **desconocida**. El tercer pulso trae $S=1$, $R=0$ y Q=1. En el cuarto vuelve a darse $SR=11$ (prohibida) y a continuación $S=0$, $R=1$: Q pasa a 0.
@end
@paso R‑S por nivel bajo y por flanco
En nivel bajo hay dos prohibidas: la primera se resuelve por un solo lado ($R$ baja y Q sigue en 1); luego, con $S=0$, $R=1$, Q pasa a 0, y viene otra prohibida que, al subir el reloj (la puerta se cierra con $SR=11$), deja la salida desconocida. Por flanco de subida el R‑S queda desconocido solo en el último flanco (llega con $SR=11$); por flanco de bajada, el primer flanco pone Q a 0, el segundo llega con $SR=11$ y la salida ya no se aclara.
@end
@paso J‑K
Por nivel alto: carrera (J y K suben a la vez), desconocida (el reloj baja), set, carrera breve y reset. Por nivel bajo: carrera, set, reset, carrera y desconocida. Por flanco de subida el J‑K no tiene ningún problema: el flanco que llega con $JK=11$ solo invierte la salida.
@end
@paso Qué enseña
Con el mismo patrón de entradas, el J‑K por flanco es un dispositivo limpio y todos los demás tienen alguna situación indefinida. El sincronismo por flanco ha degradado al R‑S, pero ha sentado bien al J‑K.
@end
@res
@fig cron {"signals": [["Ck", "001111000011110000111100001111"], ["J ó S", "000000000000111111110000111000"], ["K ó R", "001111110000111100000011111110"], ["RS Q_NA", "00000000000011xxxx111111111000", "............##............#..."], ["RS Q_NB", "00000000000000111111110011xxxx", "..............##........##...."], ["RS Q↑", "00000000000000000011111111xxxx"], ["RS Q↓", "00000000000000xxxxxxxxxxxxxxxx"], ["JK Q_NA", "000000000000rrxxxx11111111r000"], ["JK Q_NB", "00000000000000rr11111100rrxxxx"], ["JK Q↑", "000000000000000000111111110000"]], "title": "R‑S y J‑K", "rh": 28, "w_slot": 11, "grid": 4}

Trazo grueso: prohibido. Gris oscuro: carreras. Gris claro: valor desconocido a priori.

@box ojo | Errata en el libro
En el dibujo del libro, la salida del J‑K de nivel alto ($Q_{NA}$) queda a 1 después de la última carrera, pero ahí $J$ ya vale 0 y $K$ vale 1 con el reloj aún en nivel alto: la salida debe bajar a 0, como en el R‑S. Es un fallo de dibujo.
@end
@end
@end

@ej lb6-12|Tres circuitos con puertas: ¿qué biestable es?|Libro · Cap. 6 · P6.12|biestable,analisis|lb6.p612
@enun
Completa las tablas de verdad de tres circuitos con puertas y realimentación de la salida. Indica a qué biestable corresponde cada uno y qué señales son $A$, $B$ y $C$.

- **Circuito 1:** $Q=A+\overline B\cdot Q$ (una AND de $\overline B$ con la propia salida, y una OR con $A$).
- **Circuito 2:** $Q=A\cdot B+\overline A\cdot Q$ (una AND de $A$ y $B$, otra de $\overline A$ con la propia salida, y una OR).
- **Circuito 3:** $Q=A\cdot B+\overline A\cdot Q+\overline C\cdot Q$ (tres AND y una OR de tres entradas).
@end
@antes
**Un circuito con realimentación se analiza poniendo una entrada, siguiendo su efecto y anotando la salida;** si hace falta, se supone un valor inicial para $Q_{t-1}$. Si el resultado depende de él, la operación es de mantenimiento.
@end
@paso Circuito 1
| A | B | Q(t) | Operación |
|---|---|---|---|
| 0 | 0 | $Q_{t-1}$ | mantiene |
| 0 | 1 | 0 | puesta a 0 |
| 1 | 0 | 1 | puesta a 1 |
| 1 | 1 | 1 | prohibida |

**R‑S asíncrono**: $A=S$, $B=R$. Con $A=B=1$, la OR da 1: $Q=1$ (prohibida).
@end
@paso Circuito 2
| A | B | Q(t) | Operación |
|---|---|---|---|
| 0 | 0 | $Q_{t-1}$ | mantiene |
| 0 | 1 | $Q_{t-1}$ | mantiene |
| 1 | 0 | 0 | puesta a 0 |
| 1 | 1 | 1 | puesta a 1 |

**D síncrono por nivel (latch D)**: $A=Ck$ (habilita) y $B=D$. Con $A=0$ mantiene y con $A=1$ copia B.
@end
@paso Circuito 3
| A | B | C | Q(t) | Operación |
|---|---|---|---|---|
| 0 | 0 | 0 | $Q_{t-1}$ | mantiene |
| 0 | 0 | 1 | $Q_{t-1}$ | mantiene |
| 0 | 1 | 0 | $Q_{t-1}$ | mantiene |
| 0 | 1 | 1 | $Q_{t-1}$ | mantiene |
| 1 | 0 | 0 | $Q_{t-1}$ | mantiene |
| 1 | 0 | 1 | 0 | puesta a 0 |
| 1 | 1 | 0 | 1 | puesta a 1 |
| 1 | 1 | 1 | 1 | prohibida |

**R‑S síncrono por nivel**: $A=Ck$, $B=S$, $C=R$. La fila $111$ es la prohibida (queda $Q=1$).
@end
@paso Comprobación
Las tres tablas se han calculado resolviendo la ecuación de cada circuito para $Q_{t-1}=0$ y para $Q_{t-1}=1$: si salen valores distintos la fila es «mantiene».
@end
@res
Circuito 1: R‑S asíncrono. Circuito 2: latch D. Circuito 3: R‑S síncrono por nivel.

@box ojo | Errata en el libro
El libro dice que el circuito 3 es «un biestable R‑S o J‑K síncrono por nivel». Pero su tabla tiene una fila prohibida ($111$, que da $Q=1$), y un J‑K no tiene ninguna combinación prohibida (con $J=K=1$ invertiría la salida). Es un R‑S; la mención al J‑K sobra.
@end
@end
@end

@ej lb6-13|Un T y un D con realimentación: ¿qué biestable resulta?|Libro · Cap. 6 · P6.13|biestable,analisis,jk|lb6.p613
@enun
Completa las tablas de verdad de dos circuitos formados por un flip‑flop por flanco de subida, dos AND, una OR y la realimentación de sus salidas. Indica qué biestable resulta y qué señales son $A$ y $B$.

- **Circuito 1:** un T con $T=A\cdot\overline Q+B\cdot Q$.
- **Circuito 2:** un D con $D=A\cdot\overline Q+\overline B\cdot Q$.
@end
@antes
**Basta con excitar el circuito con una entrada y anotar la salida.** Para cada fila ($A$, $B$, $Q_{t-1}$) se calcula la entrada del flip‑flop y, con ella y con la tabla del flip‑flop, la salida tras el flanco.
@end
@paso Circuito 1
| A | B | $Q_{t-1}$ | T | Q(t) |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

T vale 1 cuando $A=1$ y $Q=0$ (hay que subir), o cuando $B=1$ y $Q=1$ (hay que bajar). Con $T=1$ invierte y con $T=0$ mantiene.
@end
@paso Circuito 2
| A | B | $Q_{t-1}$ | D | Q(t) |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 |

D vale 1 si hay que subir ($A=1$, $Q=0$) o si hay que mantener a 1 ($B=0$, $Q=1$).
@end
@paso Qué biestable es
Los dos son un **J‑K por flanco de subida**, con $A=J$ y $B=K$: $Q_t=J\overline{Q_{t-1}}+\overline K\,Q_{t-1}$ en los dos. Un T o un D con dos puertas y realimentación forma un J‑K. Estos circuitos son clásicos en los libros de teoría.
@end
@paso Fuera del flanco
Con el reloj en nivel alto o bajo (sin flanco de subida) la salida **mantiene** su valor: en las dos tablas del libro la última fila es «todo X, $Q_t=Q_{t-1}$».
@end
@res
Circuitos 1 y 2: J‑K por flanco de subida, con $A=J$ y $B=K$.

@box ojo | Errata en el libro
En la tabla del circuito 2, la fila con $A=0$, $B=0$, $Q_{t-1}=1$ lleva $D=0$ pero $Q(t)=1$, lo que es incoherente: con $B=0$ y $Q=1$ la puerta da $\overline B\cdot Q=1$, luego $D=1$.
@end
@end
@end

@ej lb6-14|Tabla de verdad de un D por flanco hecho con seis NAND|Libro · Cap. 6 · P6.14|biestable,d,flanco,analisis|lb6.p614
@enun
Completa la tabla de verdad de un circuito con seis puertas NAND (1 a 6) que forma un biestable. Se anotan los valores internos $Q_1$ (salida de la 1), $Q_4$ (salida de la 4), $\overline S$ (salida de la 2) y $\overline R$ (salida de la 3), y las salidas $Q$ y $\overline Q$ (puertas 5 y 6).

- Puertas 1 y 2 forman un primer latch R‑S de NAND: $Q_1=\overline{\overline S\cdot Q_4}$, $\overline S=\overline{Ck\cdot Q_1}$.
- Puerta 3: $\overline R=\overline{Ck\cdot\overline S\cdot Q_4}$. Puerta 4: $Q_4=\overline{\overline R\cdot D}$.
- Puertas 5 y 6 forman el latch de salida: $Q=\overline{\overline S\cdot\overline Q}$, $\overline Q=\overline{\overline R\cdot Q}$.
@end
@antes
**El circuito es complicado de analizar: solo vale la paciencia y escribir sobre un dibujo.** Hay que empezar por la primera fila y seguir los cambios de entrada junto con sus efectos en la salida. Se puede ver como **tres latches R‑S asíncronos**: (1,2), (3,4) y (5,6).
@end
@paso Con Ck = 0
Las puertas 2 y 3 valen 1 ($\overline S=\overline R=1$): el latch de salida mantiene. Q4 = $\overline D$ y $Q_1=D$ por la puerta 1: el circuito **sigue a D por dentro** pero sin tocar la salida.
@end
@paso En el flanco de subida
Con $Ck=1$, si $D=1$ ($Q_4=0$, $Q_1=1$): $\overline S=0$ y $\overline R=1$: se pone Q a 1. Si $D=0$ ($Q_4=1$, $Q_1=0$): $\overline S=1$ y $\overline R=0$: Q a 0. En los dos casos, una de las dos puertas 2 o 3 se activa.
@end
@paso Con Ck = 1 después del flanco
Si se capturó un 1, $\overline S=0$ mantiene $Q_1=1$ y **bloquea** a la puerta 3 ($\overline R$ no puede bajar aunque $Q_4$ cambie). Si se capturó un 0, $\overline R=0$ fija $Q_4=1$ sea cual sea D. En los dos casos los cambios de D ya no llegan al latch de salida. Por eso el último comportamiento de la tabla es el interesante: D pasa a 0 pero la salida sigue en 1.
@end
@paso Tabla
| Ck | D | $Q_{t-1}$ | Q1 | Q4 | $\overline S$ | $\overline R$ | Q(t) |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 |
| ↑ | 1 |  | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 |  | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
| ↑ | 1 |  | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 |  | 1 | 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 |
| ↑ | 0 |  | 0 | 1 | 1 | 0 | 0 |
| 1 | 0 |  | 0 | 1 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| ↑ | 0 |  | 0 | 1 | 1 | 0 | 0 |
| 1 | 0 |  | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 |
| ↑ | 1 |  | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 |  | 1 | 1 | 0 | 1 | 1 |
@end
@res
El circuito es un **biestable D síncrono por flanco de subida**: solo captura el valor de D en el flanco; los cambios posteriores de D no llegan a la salida. Hay cinco comportamientos (uno por flanco): los cuatro primeros son los normales; el quinto es el que muestra que el circuito ignora a D después del flanco. Comprobado con 3000 cambios aleatorios de reloj y de D contra un D por flanco ideal.
@end
@end

@ej lb6-15|Un circuito con dos D: detector de flancos descendentes|Libro · Cap. 6 · P6.15|biestable,d,aplicacion,cronograma|lb6.p615
@enun
Completa el cronograma del circuito siguiente y di cuál es su cometido. Son dos biestables D por flanco de subida con el mismo reloj: el primero recibe $Ent$ en D; el segundo recibe $Q_1$ en D; y una puerta AND da la salida $Sal=\overline{Q_1}\cdot Q_2$.

@fig cron {"signals": [["Ck", "0011001100110011001100110011001100110011"], ["Ent", "0001111111110000000011110000000000000000"]], "title": "Entradas", "rh": 34, "w_slot": 8, "grid": 4}
@end
@antes
**Dos biestables en cadena retrasan la entrada dos relojes:** $Q_1$ es $Ent$ retrasada un flanco y $Q_2$ es $Q_1$ retrasada otro. La salida mira la diferencia entre ellos.
@end
@paso $Q_1$ y $Q_2$
En cada flanco de subida $Q_1$ copia a $Ent$ y $Q_2$ copia el valor **anterior** de $Q_1$. Cada uno repite la entrada con un flanco de reloj de retraso respecto al anterior.
@end
@paso La salida
$Sal=\overline{Q_1}\cdot Q_2$ vale 1 solo cuando $Q_1$ ya ha bajado (la entrada fue 0 en el último flanco) pero $Q_2$ aún recuerda un 1: es decir, **justo el periodo de reloj siguiente a que la entrada baje**. Dura exactamente un periodo $T$.
@end
@paso Cometido
El circuito **detecta los flancos descendentes** de la entrada y los convierte en un pulso de duración $T$ (un periodo de reloj). Un pulso largo de duración $t$ de la entrada se transforma en uno corto de duración $T$. El pulso de salida se da cuando la entrada baja a 0, no cuando sube.
@end
@paso Variante
Para detectar flancos **ascendentes** (pulso al principio) basta con usar $Sal=Q_1\cdot\overline{Q_2}$ (se toma $Q_1$ y $\overline{Q_2}$ en la puerta).
@end
@res
@fig cron {"signals": [["Ck", "0011001100110011001100110011001100110011"], ["Ent", "0001111111110000000011110000000000000000"], ["Q1", "0000001111111100000000111100000000000000"], ["Q2", "0000000000111111110000000011110000000000"], ["Sal", "0000000000000011110000000011110000000000"]], "title": "Detector de flanco descendente", "rh": 34, "w_slot": 8, "grid": 4}

Sal vale 1 durante exactamente un periodo de reloj tras cada flanco descendente de Ent.
@end
@end

