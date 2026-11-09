%% id=libro5
%% group=ejer
%% n=3.5
%% title=Libro de problemas · Capítulo 5 · Bloques MSI
%% short=Libro · Cap. 5 Bloques MSI
%% sub=Veinte problemas con codificadores, decodificadores, multiplexores, comparadores y sumadores: cada bloque se simula y se comprueba con todas las entradas.

@box idea | Cómo se usa esta sección
Son los problemas resueltos del capítulo 5 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Aquí no se diseña con puertas sino con **bloques funcionales**: sumadores, comparadores, multiplexores, codificadores y decodificadores BCD‑7 segmentos (teoría en [[t05|el tema 5]]). Cada bloque está programado como una función, el circuito entero se simula con **todas** las combinaciones de entrada y se compara con lo que debería hacer. Los esquemas no se copian: cada circuito se describe en texto, bloque a bloque. Si el libro tiene un fallo, aparece en un recuadro de errata.
@end

@ej lb5-1|Codificador decimal a BCD exceso 3 sin prioridad|Libro · Cap. 5 · P5.1|msi,codigos|lb5.p51
@enun
Completa la tabla de un codificador de 10 líneas a 4 bits que entregue el dígito decimal en BCD exceso 3, con entrada de habilitación EI, salida de habilitación EO y señal GS de «hay alguna tecla». No tiene prioridad.
@end
@antes
**Dos ideas:** (1) *sin prioridad* significa que el diseño solo garantiza el resultado cuando **una** línea está activa; (2) el exceso 3 de un dígito $d$ es simplemente $d+3$ en binario: $0\to0011$, $9\to1100$.
@end
@paso Qué hace cada señal
$EI$ habilita el bloque: si vale 0, todo queda en 0. $GS$ ($=1$) indica que hay alguna entrada activa. $EO$ vale 1 solo cuando el bloque está habilitado y **no** hay ninguna entrada activa: sirve para encadenar otro codificador detrás.
@end
@paso Tabla
| EI | Entrada activa | EO | S3S2S1S0 | GS |
|---|---|---|---|---|
| 1 | E9 | 0 | 1100 | 1 |
| 1 | E8 | 0 | 1011 | 1 |
| 1 | E7 | 0 | 1010 | 1 |
| 1 | E6 | 0 | 1001 | 1 |
| 1 | E5 | 0 | 1000 | 1 |
| 1 | E4 | 0 | 0111 | 1 |
| 1 | E3 | 0 | 0110 | 1 |
| 1 | E2 | 0 | 0101 | 1 |
| 1 | E1 | 0 | 0100 | 1 |
| 1 | E0 | 0 | 0011 | 1 |
| 1 | ninguna | 1 | 0000 | 0 |
| 0 | (cualquiera) | 0 | 0000 | 0 |
@end
@paso Ecuaciones
Cada bit de salida es un OR de las entradas cuyo código lo tiene a 1, todo AND con $EI$: $S_3=(E_9+E_8+E_7+E_6+E_5)\,EI$, $S_2=(E_9+E_4+E_3+E_2+E_1)\,EI$, $S_1=(E_8+E_7+E_4+E_3+E_0)\,EI$, $S_0=(E_8+E_6+E_4+E_2+E_0)\,EI$. Además $GS=(E_9+\dots+E_0)\,EI$ y $EO=\overline{E_9}\cdots\overline{E_0}\,EI$. El programa simula el bloque con las 11 combinaciones de una tecla (o ninguna) y con $EI=0$ y $EI=1$: las ecuaciones coinciden con la tabla.
@end
@paso Qué pasa con dos teclas a la vez
Como los ORs mezclan los códigos, pulsar $E_9$ y $E_0$ da $1100\,|\,0011=1111$, que no es ningún dígito válido. Para evitarlo hace falta un codificador **con** prioridad.
@end
@res
La tabla anterior y las seis ecuaciones describen el bloque. Todas se han verificado por simulación.
@end
@end

@ej lb5-2|Decodificador BCD a 7 segmentos con LT, RBI y RBO|Libro · Cap. 5 · P5.2|msi,7seg,bcd|lb5.p52
@enun
Completa la tabla de un decodificador BCD a 7 segmentos cuyas entradas y salidas son todas activas a nivel bajo. Tiene prueba de lámparas (LT), supresión de ceros a la izquierda (RBI) y una línea RBO/BI que es salida de supresión y a la vez entrada de borrado.
@end
@antes
**Pistas para leer la tabla.** «Activa a nivel bajo» significa que un 0 *activa*: una salida $\bar a=0$ **enciende** el segmento $a$, y una entrada $\bar E_3\ldots\bar E_0$ se lee invertida (el código $1100$ en las entradas es el dígito $0011=3$). La tabla se lee en dos direcciones: arriba, de entradas a salidas; abajo, al revés (dadas las salidas, ¿qué entradas las producen?).
@end
@paso Reglas del bloque
1) Si $BI=0$ entra por la línea RBO/BI, todo se apaga y $RBO=0$. 2) Si $\overline{LT}=0$, se encienden los siete segmentos (prueba de lámparas). 3) Si $\overline{RBI}=0$ y el dígito es $0$, se apaga y $RBO=0$: así un 0 a la izquierda no se escribe y avisa al siguiente dígito. 4) En cualquier otro caso se dibuja el dígito y $RBO=1$.
@end
@paso Parte superior (entradas → salidas)
| LT | RBI | E3 | E2 | E1 | E0 | RBO/BI | a | b | c | d | e | f | g | Qué se ve |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | todo encendido |
| 1 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 3 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | todo encendido |
| 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 7 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | apagado |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | todo encendido |
| 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 6 (sin trazo superior) |
| 1 | 1 | 0 | 0 | 1 | 1 | 1 | ¿ | ¿ | ¿ | ¿ | ¿ | ¿ | ¿ | código no BCD |
| 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

La fila del código $0011$ invertido (dígito 12) no es BCD: el programa confirma que el modelo no define ninguna salida y por eso se deja como «¿».
@end
@paso Parte inferior (salidas → entradas)
Se busca qué entradas dan la salida pedida. El programa recorre las 64 combinaciones de $LT,RBI,E_3..E_0$ y comprueba que cada fila del libro es cierta **para todas las combinaciones que cubren sus «X»**. Casos con dos respuestas posibles: (a) salida «todo encendido» con $RBO=1$: $LT=0$ y lo demás indiferente, **o** $LT=1$ con el dígito 8 (entradas $0111$); (b) «todo apagado» con $RBO=0$: $LT=1,RBI=0$ y dígito 0, **o** $BI=0$ forzado desde fuera (cualquier entrada). Las filas de los dígitos 6, 3, 1, 0, 5 y 7 salen de las entradas $1001$, $1100$, $1110$, $1111$, $1010$ y $1000$ respectivamente.
@end
@paso La fila «¿»
El patrón $a,d,g$ encendidos ($0110110$) no coincide con ningún dígito 0–9, ni siquiera con las variantes del 6 y del 9 con o sin trazo. Es el patrón que un fabricante da a un código **no BCD** (10–15); cuál es depende del integrado, así que el ejercicio solo pide reconocer que no hay dígito.
@end
@res
Las dos mitades de la tabla son coherentes con las cuatro reglas de arriba, salvo una excepción que anotamos.

@box ojo | Errata en el libro
El dígito 6 aparece de dos formas: en la mitad superior y en la primera fila de la inferior sale **sin** el trazo superior ($\bar a=1$, salidas $1100000$), pero en la penúltima fila del bloque inferior el mismo código $1001$ da **con** trazo superior ($0100000$). Un decodificador no puede dar dos salidas distintas para la misma entrada: una de las dos filas es una errata de copia. Aquí se ha tomado la versión sin trazo, que es la que aparece dos veces.
@end
@end
@end

@ej lb5-3|Qué hace una red de ANDs y sumadores completos|Libro · Cap. 5 · P5.3|msi,aritmetica|lb5.p53
@enun
Un circuito tiene nueve puertas AND y seis sumadores completos conectados en dos filas. Rellena una tabla de funcionamiento con cinco pares de entradas $A_{2\text{-}0}$, $B_{2\text{-}0}$ y averigua qué operación realiza.
@end
@antes
**Cómo se analiza:** se pone un valor en cada entrada y se propaga hacia la salida bloque a bloque. Cada AND forma un producto parcial $A_iB_j$; cada sumador completo (FA) suma tres bits y deja un bit de suma y un acarreo.
@end
@paso Producto parcial por filas
Las tres ANDs de cada fila multiplican **un bit de $A$** por los tres de $B$. La fila de $A_0$ está sin desplazar, la de $A_1$ desplazada una posición y la de $A_2$ dos. Las dos filas de sumadores van acumulando esas tres filas columna a columna, y el acarreo de cada FA pasa al siguiente.
@end
@paso Tabla
| $A_{2\text{-}0}$ | $B_{2\text{-}0}$ | $P_{5\text{-}0}$ | decimal |
|---|---|---|---|
| 010 (2) | 110 (6) | 001100 | 12 |
| 111 (7) | 111 (7) | 110001 | 49 |
| 000 (0) | 000 (0) | 000000 | 0 |
| 110 (6) | 110 (6) | 100100 | 36 |
| 001 (1) | 010 (2) | 000010 | 2 |

Ejemplo $010\times110$: $A_0=0$ da la fila $000$, $A_1=1$ da $110$ (desplazada), $A_2=0$ da $000$. Suma: $1100=12=2\times6$.
@end
@paso Qué operación es
Los resultados son $2\cdot6=12$, $7\cdot7=49$, $0$, $6\cdot6=36$ y $1\cdot2=2$: es un **multiplicador de $3\times3$ bits**. El programa modela las nueve ANDs y los seis FA y comprueba que da $A\times B$ en las 64 combinaciones de entrada.
@end
@res
El circuito es un multiplicador binario sin signo de $3\times3$ bits con salida de 6 bits. Verificado con las 64 combinaciones.
@end
@end

@ej lb5-4|Mostrar el mayor de dos números decimales|Libro · Cap. 5 · P5.4|msi,7seg,comparador|lb5.p54
@enun
Dos selectores giratorios dan los dígitos decimales $A$ y $B$. Un 7 segmentos debe mostrar solo el mayor; si son iguales no se ve nada. Diseña el circuito con bloques MSI.
@end
@antes
**Receta general:** *codificar → comparar → elegir → decodificar*. Cada selector entrega una línea de 10 (una por dígito), así que lo primero es pasarla a binario.
@end
@paso Codificar
Un codificador 10:4 por selector convierte «la línea $k$ activa» en el número $k$ en BCD (4 bits).
@end
@paso Comparar
Un comparador de 4 bits da $A>B$ y $A=B$.
@end
@paso Elegir
Un cuádruple multiplexor 2:1, mandado por $A>B$, deja pasar $A$ si $A>B=1$ y $B$ en caso contrario. Cuando son iguales da igual cuál pase, porque el display se borrará.
@end
@paso Mostrar
La salida del multiplexor va a un decodificador BCD‑7 segmentos. La señal $A=B$ se conecta a su entrada de borrado $BI$: si $A=B$, el display queda apagado.
@end
@paso Comprobación
El programa prueba los 100 pares $(A,B)$: muestra $\max(A,B)$ en todos los casos con $A\ne B$ y apagado en los 10 con $A=B$.
@end
@res
Coste: 2 codificadores 10:4, 1 comparador de 4 bits, 1 cuádruple mux 2:1 y 1 decodificador BCD‑7 segmentos con entrada de borrado. Verificado con los 100 pares.
@end
@end

@ej lb5-5|Restar dos dígitos y mostrar solo si es positivo|Libro · Cap. 5 · P5.5|msi,aritmetica,7seg|lb5.p55
@enun
Dos selectores dan los dígitos decimales $A$ y $B$. Un 7 segmentos debe mostrar $A-B$ solo si el resultado es positivo o cero; si es negativo, no debe mostrarse nada.
@end
@antes
**Restar en binario** es sumar el opuesto: $A-B=A+(-B)$, y en complemento a dos $-B=\overline{B}+1$. Con 4 bits se pueden representar los números $-8\ldots+7$.
@end
@paso Diseño del libro
1) Un sumador 4+4 calcula $-B=\overline{B}+1$ (cuatro inversores y la constante $0001$). 2) Otro sumador 4+4 hace $A+(-B)$ y da $R_3R_2R_1R_0$. 3) El resultado va al decodificador BCD‑7 segmentos, y el bit $R_3$ se lleva a su entrada de borrado: $R_3=1$ ⇒ «resta negativa» ⇒ display apagado. Hace falta un sumador 4+4 (no uno 1+1) porque el $+1$ puede generar acarreos entre bits.
@end
@paso Qué comprueba el programa
Se simulan los 100 pares $(A,B)$ de dígitos y se compara con el resultado esperado (mostrar $A-B$ si $A\ge B$, apagado si $A<B$). El diseño del libro acierta en 96 pares y **falla en cuatro**:
@end
@paso Los cuatro pares que fallan
| A | B | A−B | R3R2R1R0 | Debería mostrar | Muestra |
|---|---|---|---|---|---|
| 0 | 9 | -9 | 0111 | nada | 7 |
| 8 | 0 | 8 | 1000 | 8 | nada |
| 9 | 0 | 9 | 1001 | 9 | nada |
| 9 | 1 | 8 | 1000 | 8 | nada |

La resta de dos dígitos va de $-9$ a $+9$, pero con 4 bits en complemento a dos solo caben $-8\ldots+7$. Si la diferencia es **8 o 9** ($1000$ y $1001$, con $R_3=1$), el circuito la toma por negativa y **borra** un resultado que debía verse. Si la diferencia es $-9$ ($0-9$), el resultado se desborda a $+7$ ($0111$, $R_3=0$) y el circuito **muestra un 7** en lugar de apagarse.
@end
@paso Diseño corregido
Se usa **un solo sumador 4+4** con $A$, $\overline{B}$ y $C_{in}=1$. Su acarreo de salida $C_{out}$ vale 1 si y solo si $A\ge B$ (comprobado para los 256 pares de 4 bits). Se conecta $\overline{C_{out}}$ a $BI$. Las cuatro salidas $S_3S_2S_1S_0$ son directamente el resultado, hasta 9. El programa confirma que acierta en los 100 pares.
@end
@res
La estructura del libro sirve cuando $-8\le A-B\le7$, pero falla en $8-0$, $9-0$ y $9-1$ (borra) y en $0-9$ (muestra un 7).

@box ojo | Errata en el libro
Con $R_3$ como indicador de signo falla en cuatro pares de dígitos: con diferencia 8 o 9 (tres pares) borra un resultado válido, y con $0-9$ el desbordamiento da $+7$ y lo muestra. La solución más simple es usar el acarreo de salida de un único sumador $A+\overline{B}+1$ y negarlo hacia $BI$. El libro avisa de que no hay que comparar con $0000$ con un comparador, lo cual es cierto; pero tampoco basta con mirar el bit de signo.
@end
@end
@end

@ej lb5-6|Mostrar el mayor de tres números|Libro · Cap. 5 · P5.6|msi,7seg,comparador|lb5.p56
@enun
Tres selectores dan los dígitos decimales $A$, $B$ y $C$. Un 7 segmentos debe mostrar el mayor de los tres.
@end
@antes
**Torneo de eliminación:** el mayor de tres se obtiene en dos rondas, igual que en el problema de dos números.
@end
@paso Ronda 1
Un comparador $A>B$ gobierna un cuádruple mux 2:1 que da $R'$: si $A>B$, $R'=A$; si no, $R'=B$ (da igual cuál se tome cuando son iguales).
@end
@paso Ronda 2
Otro comparador compara $R'>C$ y manda otro cuádruple mux 2:1: si $R'>C$ el resultado es $R=R'$, si no, $R=C$.
@end
@paso Mostrar
$R$ entra en un decodificador BCD‑7 segmentos.
@end
@paso Comprobación
Se simulan las $16^3=4096$ ternas de números de 4 bits (incluidos los empates) y el resultado es siempre el máximo. En los empates da igual qué rama se escoja porque el valor es el mismo.
@end
@res
Dos comparadores de 4 bits, dos cuádruples multiplexores 2:1 y un decodificador. Verificado con las 4096 ternas.
@end
@end

@ej lb5-7|Mostrar los dos mayores de tres números|Libro · Cap. 5 · P5.7|msi,7seg,comparador|lb5.p57
@enun
Tres selectores dan los dígitos decimales $A$, $B$ y $C$. Dos 7 segmentos deben mostrar los dos mayores.
@end
@antes
**Idea:** tres comparaciones ($A>B$, $A>C$, $B>C$) determinan el orden completo de los tres números. Esas tres señales sirven de código de selección de dos multiplexores de 8 entradas.
@end
@paso Código de selección
Con $x=A>B$ (peso 4), $y=A>C$ (peso 2) y $z=B>C$ (peso 1) hay 8 combinaciones, pero **dos son imposibles**: $x=1,z=1,y=0$ ($A>B>C$ y $A\le C$) y $x=0,z=0,y=1$. Corresponden a los índices 5 y 2, y se dejan sin conectar (N.C.).
@end
@paso Entradas de los multiplexores
| x y z | Orden | M1 | M2 |
|---|---|---|---|
| 000 | $A\le B\le C$ | B | C |
| 001 | $A\le C<B$ | B | C |
| 011 | $C<A\le B$ | A | B |
| 100 | $B<A\le C$ | A | C |
| 110 | $A>C\ge B$ | A | C |
| 111 | $A>B>C$ | A | B |

En cada fila M1 y M2 son los **dos mayores**, sin garantizar quién es el primero: por ejemplo en $x\,y\,z=001$ el mayor es $B$ y el segundo $C$, y el libro los saca por M1 y M2 en ese orden, mientras que en $011$ el mayor es $B$ y sale por M2.
@end
@paso Comprobación
Con las $16^3=4096$ ternas el par $\{M_1,M_2\}$ coincide siempre con los dos mayores, **incluidos los empates**, y nunca se llega a los índices 2 y 5. El libro deja como ejercicio saber cuál es el mayor.
@end
@paso Variante: M1 el mayor y M2 el segundo
Basta con cambiar las entradas de los multiplexores: M1: $0\to C$, $1\to B$, $3\to B$, $4\to C$, $6\to A$, $7\to A$; M2: $0\to B$, $1\to C$, $3\to A$, $4\to A$, $6\to C$, $7\to B$. El programa comprueba que así M1 es siempre el mayor y M2 el segundo en las 4096 ternas.
@end
@res
Tres comparadores y dos multiplexores 4×8:1 (cuádruples) más dos decodificadores. Todo comprobado, incluidos los empates.
@end
@end

@ej lb5-8|Valor absoluto de un número en complemento a dos|Libro · Cap. 5 · P5.8|msi,aritmetica,c2|lb5.p58
@enun
Diseña un circuito que obtenga el valor absoluto de un número de cuatro bits en complemento a dos.
@end
@antes
**Idea:** el valor absoluto es $A$ si es positivo y $-A$ si es negativo. El signo está en el bit más significativo, $A_3$.
@end
@paso Calcular $-A$
Cuatro inversores y un sumador 4+4 con la constante $0001$ dan $\overline{A}+1$.
@end
@paso Elegir
Un cuádruple multiplexor 2:1, mandado por $A_3$, deja pasar $A$ si $A_3=0$ y $-A$ si $A_3=1$.
@end
@paso Tabla de comprobación
| A | valor | |A| calculado | valor |
|---|---|---|---|
| 0000 | 0 | 0000 | 0 |
| 0001 | 1 | 0001 | 1 |
| 0010 | 2 | 0010 | 2 |
| 0011 | 3 | 0011 | 3 |
| 0100 | 4 | 0100 | 4 |
| 0101 | 5 | 0101 | 5 |
| 0110 | 6 | 0110 | 6 |
| 0111 | 7 | 0111 | 7 |
| 1000 | -8 | 1000 | -8 |
| 1001 | -7 | 0111 | 7 |
| 1010 | -6 | 0110 | 6 |
| 1011 | -5 | 0101 | 5 |
| 1100 | -4 | 0100 | 4 |
| 1101 | -3 | 0011 | 3 |
| 1110 | -2 | 0010 | 2 |
| 1111 | -1 | 0001 | 1 |

El programa simula las 16 entradas: en 15 de ellas el resultado es correcto.
@end
@res
Un sumador 4+4, cuatro inversores y un cuádruple mux 2:1.

@box ojo | Errata en el libro
Con 4 bits el número $1000$ ($-8$) no tiene opuesto representable: el circuito devuelve $1000$, que sigue valiendo $-8$ y no $+8$. Es el único caso en el que el valor absoluto no es correcto. El libro no lo menciona; se ha detectado simulando las 16 entradas.
@end
@end
@end

@ej lb5-9|Nota final: media por defecto, por exceso, mínima o máxima|Libro · Cap. 5 · P5.9|msi,aritmetica,bcd,7seg|lb5.p59
@enun
Se tienen dos notas $N_1$ y $N_0$ (cada una un dígito BCD). Con dos líneas de control $C_1C_0$ se elige la nota final: $00$ media redondeada por defecto, $01$ nota mínima, $10$ nota máxima, $11$ media redondeada por exceso. Muéstrala en un 7 segmentos.
@end
@antes
**Dividir entre 2 en binario** es desplazar un bit a la derecha: el bit que se pierde es el resto. Si el resto es 1, redondear por exceso es sumar 1.
@end
@paso Media por defecto
Un sumador 4+4 da $A+B=C_{out}S_3S_2S_1S_0$ (5 bits). Se descarta $S_0$: queda $C_{out}S_3S_2S_1$, el cociente de dividir entre 2.
@end
@paso Media por exceso
Se suma $S_0$ al cociente anterior: con $S_0=0$ se suma 0 y con $S_0=1$ se suma 1. Así sale $\lceil (A+B)/2\rceil$. Un segundo sumador 4+4 hace esa suma.
@end
@paso Mínimo y máximo
Un comparador de 4 bits y dos cuádruples mux 2:1 eligen el menor y el mayor.
@end
@paso Elegir
Un cuádruple mux 4:1, mandado por $C_1C_0$, escoge entre las cuatro opciones (en el orden de la tabla del enunciado) y el decodificador BCD‑7 segmentos las muestra.
@end
@paso Ejemplos
| $N_1$ | $N_0$ | suma | por defecto | por exceso |
|---|---|---|---|---|
| 3 | 4 | 7 | 3 | 4 |
| 3 | 5 | 8 | 4 | 4 |
| 8 | 9 | 17 | 8 | 9 |

Se ha comprobado con las 100 parejas de dígitos que las cuatro opciones coinciden con $\lfloor(a+b)/2\rfloor$, $\min$, $\max$ y $\lceil(a+b)/2\rceil$.
@end
@res
Dos sumadores 4+4, un comparador de 4 bits, dos cuádruples mux 2:1 (mínimo y máximo) y un cuádruple mux 4:1. Verificado con las 100 parejas.
@end
@end

@ej lb5-10|Sensor de temperatura entre −5 °C y +4 °C|Libro · Cap. 5 · P5.10|msi,comparador,c2|lb5.p510
@enun
Un sensor entrega la temperatura en 4 bits, en complemento a dos. La salida debe activarse cuando la temperatura esté entre $-5$ °C y $+4$ °C, ambos incluidos.
@end
@antes
**Truco:** los comparadores MSI comparan en binario puro, no en complemento a dos. Así que conviene mirar el intervalo como números **sin signo**.
@end
@paso Cómo se ven los valores
En 4 bits: $0000\ldots0100$ son $0\ldots+4$ y $1011\ldots1111$ son $-5\ldots-1$. Sin signo, los primeros son $0\ldots4$ y los segundos $11\ldots15$: dos tramos separados.
@end
@paso Dos comparadores
Un comparador da $T<0101$ (menor que 5 ⇒ valores $0\ldots4$, o sea $0\ldots+4$ °C). Otro da $T>1010$ (mayor que 10 ⇒ $11\ldots15$, o sea $-5\ldots-1$ °C).
@end
@paso Salida
Una puerta OR une las dos salidas: $Salida=(T<5)+(T>10)$. Se prueban los 16 valores y la salida vale 1 exactamente cuando $-5\le T\le4$.
@end
@res
Dos comparadores de 4 bits con constantes $0101$ y $1010$, y una OR. Verificado con los 16 códigos.
@end
@end

@ej lb5-11|Expendedor de golosinas: dinero que falta o que sobra|Libro · Cap. 5 · P5.11|msi,aritmetica,7seg|lb5.p511
@enun
Un expendedor recibe el dinero introducido (4 bits, en céntimos de euro, binario puro) y el producto pedido mediante cuatro microinterruptores G, Ch, R y P (gominolas, chicle, regaliz y pipas), que cuestan 2, 3, 5 y 6 céntimos. Un 7 segmentos muestra cuánto dinero falta o sobra, y dos leds indican si debe entregarse el producto (LP) o si el usuario debe completar el dinero (LD).
@end
@antes
**Idea:** la resta *dinero − precio* da la información que se pide. Si es $\ge0$, el producto se entrega y la cifra es lo que sobra. Si es negativa, falta dinero y la cifra es su valor absoluto.
@end
@paso Elegir el precio
Un codificador 4:2 pasa la tecla pulsada a un código de 2 bits y un cuádruple multiplexor 4:1 saca **el precio ya negado** en complemento a dos: $-2=1110$, $-3=1101$, $-5=1011$, $-6=1010$.
@end
@paso Restar
Un sumador 4+4 hace $D+(-\text{precio})=R$.
@end
@paso Valor absoluto de $R$
Cuatro inversores y otro sumador 4+4 dan $-R=\overline{R}+1$. Un mux 2:1 gobernado por $R_3$ elige $R$ o $-R$.
@end
@paso Salidas
El 7 segmentos muestra $S$. $LP=\overline{R_3}$ (el producto sale si $R_3=0$) y $LD=R_3$ (el decodificador 1:2 de las dos señales es un simple inversor).
@end
@paso Qué ocurre si sobra mucho
Se han simulado los 16 importes con los cuatro productos. El diseño del libro acierta siempre que la diferencia $D-\text{precio}$ sea **como mucho 7**; falla cuando es 8 o más: 16 casos, p. ej. $D=15$ con gominolas ($15-2=13=1101$, que parece negativo porque $R_3=1$, y el circuito dice que falta dinero: $LD=1$ y muestra 3).
@end
@paso Diseño corregido
Se usa el **acarreo** del primer sumador: $C_{out}=1$ exactamente cuando $D\ge$ precio. Entonces $LP=C_{out}$, $LD=\overline{C_{out}}$ y el mux elige $R$ si $C_{out}=1$ y $-R$ si no. El programa lo comprueba con los 64 casos.
@end
@res
El diseño del libro es correcto para sobras de hasta 7 céntimos; con el acarreo como señal de «llega el dinero» lo es en todo el rango.

@box ojo | Errata en el libro
1) Con $R_3$ como indicador de signo falla cuando la diferencia es $\ge8$ (por ejemplo, 15 céntimos para unas gominolas de 2). 2) En el texto la lista de códigos del producto (gominolas $00$, chicle $01$, regaliz $10$, pipas $11$) está invertida respecto al esquema, donde G entra por la línea 3 del codificador 4:2 y selecciona el precio $-2$. El esquema es el coherente.
@end
@end
@end

@ej lb5-12|Votación en un consejo con voto de calidad, trampa y veto|Libro · Cap. 5 · P5.12|msi,7seg,comparador,aritmetica|lb5.p512
@enun
Cuatro países, A, B, C y D, votan en un consejo. Un 7 segmentos muestra el resultado de la votación. Si hay empate decide el voto de calidad de A. Además, el país anfitrión tiene un interruptor de trampa que da la vuelta al resultado. Después hay que rediseñar el circuito para seis países en los que los votos de A y B valen doble, y añadir el derecho de veto de un país.
@end
@antes
**Dos ideas:** (1) contar votos = **sumar bits**; (2) el resultado depende de si la suma es mayor, igual o menor que la mitad. Con cuatro votos, «mitad» es 2.
@end
@paso Primera solución: contar con sumadores y comparar
Dos sumadores 1+1 dan $S'=A+B$ y $S''=C+D$ (2 bits cada uno), y otro $S=S'+S''$ de 3 bits (0–4). Un comparador de 3 bits compara $S$ con $010$: $S>2$ ⇒ voto 1; $S=2$ ⇒ voto de $A$; $S<2$ ⇒ voto 0. Un multiplexor 4:1 gobernado por $(S>2,\;S=2)$ elige entre $0$, $A$ y $1$ (la combinación «mayor y a la vez igual» es imposible y queda sin conectar). Para la trampa un mux 2:1 elige entre $V$ y $\overline V$ según el interruptor. El resultado ($V_0$) y tres ceros forman el dígito BCD $000V_0$ que va al decodificador: muestra 0 o 1.
@end
@paso Segunda solución: fuerza bruta
Un solo multiplexor 16:1 con $A,B,C,D$ como selección y constantes en las entradas. Las 16 posiciones se rellenan a mano, porque se sabe qué vale el resultado en cada caso:

| A B C D | votos a favor | resultado (sin trampa) |
|---|---|---|
| 0000 | 0 | 0 |
| 0001 | 1 | 0 |
| 0010 | 1 | 0 |
| 0011 | 2 | 0 |
| 0100 | 1 | 0 |
| 0101 | 2 | 0 |
| 0110 | 2 | 0 |
| 0111 | 3 | 1 |
| 1000 | 1 | 0 |
| 1001 | 2 | 1 |
| 1010 | 2 | 1 |
| 1011 | 3 | 1 |
| 1100 | 2 | 1 |
| 1101 | 3 | 1 |
| 1110 | 3 | 1 |
| 1111 | 4 | 1 |

Con exactamente dos votos a favor, el resultado es el voto de $A$: es 1 en las posiciones 9, 10 y 12 ($A=1$) y 0 en la 3, 5 y 6. Las demás se rellenan por mayoría. Lo demás del circuito es igual (trampa y decodificador).
@end
@paso Tercera solución: seis países, A y B valen doble
Los votos pesan $2A+2B+C+D+E+F$, con total 8; la mayoría es $>4$ y el empate es $=4$. Un sumador 2+2 suma los números de dos bits $AC$ y $BD$ (donde $A$ y $B$ ocupan el bit de peso 2, así valen doble) y $E$ entra por su acarreo de entrada. Su resultado de 3 bits se suma con $000$ y con $F$ como acarreo de entrada en un sumador 3+3. Así los pesos no se mezclan; no valdría un sumador 2+2 *sin* agrupar, porque dos países valdrían doble por la posición equivocada. La salida de 4 bits se compara con $0100$. Un mux 4:1 elige $0$, $A$ o $1$ y otro 2:1 la trampa. La línea de **veto** va a la entrada de borrado del decodificador: si algún país veta, la pantalla se apaga.
@end
@paso Comprobación
Con las 16 combinaciones de 4 países y las dos posiciones de la trampa, las soluciones 1 y 2 dan lo mismo que una cuenta directa (empate para $A$). Con las 64 combinaciones de 6 países, las 2 de la trampa y las 2 del veto (256 casos) la solución de seis países coincide con $2A+2B+C+D+E+F$ comparado con 4.
@end
@res
Tres diseños verificados: dos sumadores 1+1 + sumador + comparador + mux (elegante), un mux 16:1 (fuerza bruta) y el rediseño de seis países con veto.
@end
@end

@ej lb5-13|Votación por bloques: cuatro países en A y tres en B|Libro · Cap. 5 · P5.13|msi,7seg,comparador,aritmetica|lb5.p513
@enun
En una votación los países se agrupan en dos bloques: cuatro en el bloque A y tres en el B. Un 7 segmentos muestra el resultado: si hay mayoría en A, ése es el resultado; si hay empate en A, decide el bloque B. Diseña el circuito.
@end
@antes
**Cómo se razona:** hay que saber **cuántos** votos a favor hay en A (0 a 4) y en B (0 a 3). La regla es: $a>2$ ⇒ 1; $a<2$ ⇒ 0; $a=2$ ⇒ el resultado lo da $B$, y gana el 1 si en $B$ hay al menos dos votos.
@end
@paso Primera solución
Cuatro sumadores 1+1 para el bloque A en dos capas (primero $A_3+A_2$ y $A_1+A_0$, luego se suman sus resultados de 2 bits columna a columna, $S_{A2..0}$) y un sumador 1+1 para B (suma 3 bits, uno por el acarreo de entrada, y da $S_{B1}S_{B0}$). Un comparador de 3 bits compara $S_A$ con $010$ ($A>2$ y $A=2$, la señal $C$). Un comparador de 2 bits compara $S_B$ con $01$ ($B>1$). Un mux 2:1 gobernado por $C$ elige entre $(A>2)$ si $C=0$ y $(B>1)$ si $C=1$. Se visualiza el resultado con $000V$ en el decodificador.
@end
@paso Segunda solución
Muy parecida, pero con sumadores 4+4 en lugar de 1+1: se rellenan con ceros las entradas libres. Funciona igual y no mezcla pesos porque la suma se hace en dos niveles.
@end
@paso Tercera solución: con puertas
Tres sumadores 1+1 para A (resultado $S_{A2}S_{A1}S_{A0}$) y uno para B ($S_{B1}S_{B0}$). El voto vale 1 si: $S_{A2}=1$ (cuatro votos), $S_{A1}S_{A0}=11$ (tres), o $S_{A1}S_{A0}=10$ (dos) y además $S_{B1}=1$. O sea $V=S_{A2}+S_{A1}S_{A0}+S_{A1}\overline{S_{A0}}S_{B1}$: una AND y una OR detectan «3 ó 4», otra AND resuelve el caso de 2 con $B$. Se sustituyen los comparadores y el multiplexor por tres puertas.
@end
@paso Comprobación
Las tres soluciones se han simulado con las $2^7=128$ combinaciones de votos y las tres coinciden con la regla $a>2$ ó $(a=2$ y $b\ge2)$.
@end
@res
Las tres soluciones son equivalentes. La tercera es la más barata; las dos primeras son más fáciles de ampliar si cambia el número de países.
@end
@end

@ej lb5-14|Reloj con alarma: cuatro displays y cuatro vistas|Libro · Cap. 5 · P5.14|msi,7seg,multiplexor|lb5.p514
@enun
Cuatro 7 segmentos deben mostrar, según dos señales de control $P_1$ y $P_2$, el mes, el día, la hora, los minutos, los segundos y las décimas de segundo del día en curso, y también la hora y los minutos de la alarma. Diseña el circuito.
@end
@antes
**Un multiplexor por display.** Cada display $SG_k$ necesita elegir su dígito entre cuatro fuentes, y la elección la hacen las mismas dos líneas $P_1P_2$ para los cuatro. Es el uso clásico de un **cuádruple multiplexor 4:1**: 4 bits de dato por entrada, 4 entradas.
@end
@paso Qué muestra cada combinación
| $P_1P_2$ | Se ve | $SG_3$ | $SG_2$ | $SG_1$ | $SG_0$ |
|---|---|---|---|---|---|
| 00 | HH MM | HD | HU | MD | MU |
| 01 | SS DD | SD | SU | DD | DU |
| 10 | HH MM de alarma | HAD | HAU | MAD | MAU |
| 11 | MM DD (mes y día) | MD | MU | DD | DU |

Siglas: HD/HU decenas/unidades de hora; MD/MU de minutos; SD/SU de segundos; HAD/HAU y MAD/MAU de hora y minutos de alarma; DD/DU de día.
@end
@paso Estructura
Cuatro multiplexores 4:1 de 4 bits (uno por display), con $P_1P_2$ como selección común; la salida de cada uno va a un decodificador BCD‑7 segmentos. Total: 4 cuádruples mux 4:1 y 4 decodificadores.
@end
@paso Comprobación
El programa recorre las cuatro combinaciones $P_1P_2$ y verifica que cada display recibe exactamente su fuente de la tabla.
@end
@res
Con esta estructura, para mostrar otra «vista» basta añadir una entrada a cada multiplexor.

@box ojo | Errata en el libro
En el esquema las entradas 1 de los displays $SG_1$ y $SG_0$ (vista «segundos y décimas») se llaman DD y DU, igual que las del día (entrada 3). Como las décimas de segundo no son el día del mes, deben ser señales distintas, por ejemplo $\text{dc}_D$ y $\text{dc}_U$.
@end
@end
@end

@ej lb5-15|Sumador/restador en C-1 o C-2|Libro · Cap. 5 · P5.15|msi,aritmetica,c2|lb5.p515
@enun
Diseña un sumador/restador en binario puro con signo en complemento a uno o a dos. Dos líneas de control: $COD=0$ elige C-1 y $COD=1$ elige C-2; $OP=0$ suma y $OP=1$ resta.
@end
@antes
**Recordatorio:** restar es sumar el opuesto. El opuesto en C-1 es invertir todos los bits ($\overline{B}$). En C-2 es invertir y sumar 1. La suma en C-1 necesita además el **acarreo circular**: el acarreo de salida se vuelve a sumar al bit menos significativo.
@end
@paso Negar $B$ si hay resta
Cuatro puertas XOR: $B'=B\oplus OP$. Si $OP=1$ invierten $B$; si $OP=0$ lo dejan igual.
@end
@paso Sumar
Un sumador 4+4 hace $A+B'+C_{in}$.
@end
@paso Elegir $C_{in}$
Un mux 4:1 gobernado por $OP\,COD$ da: $00$ (suma C-1) ⇒ $C_{in}=C_{out}$ (acarreo circular); $01$ (suma C-2) ⇒ $0$; $10$ (resta C-1) ⇒ $C_{out}$; $11$ (resta C-2) ⇒ $1$ (el $+1$ del complemento a dos).
@end
@paso Comprobación
Para los 256 pares de operandos y las dos operaciones, el programa calcula el resultado de cada modo y lo compara con el valor aritmético: en C-2 sale bien siempre que el resultado esté en $-8\ldots7$, y en C-1 siempre que esté en $-7\ldots7$ (fuera de esos rangos hay desbordamiento y el circuito no lo detecta).
@end
@res
El circuito funciona. Un único sumador 4+4 más 4 XOR y un mux 4:1.

@box ojo | Errata en el libro
En los modos C-1 el acarreo de salida alimenta la entrada de acarreo del mismo sumador, es decir, hay un **bucle combinacional**. Estable no siempre es único: cuando $A+B'=15$ ($1111$) hay dos soluciones consistentes ($1111$ con $C_{in}=0$ y $0000$ con $C_{in}=1$). Las dos son «cero» en C-1, así que el valor es correcto, pero el circuito físico puede quedarse en cualquiera. Un diseño sin bucle usa dos sumadores en cascada (el segundo suma el acarreo del primero).
@end
@end
@end

@ej lb5-16|Comparadores para C-1, C-2 y signo-magnitud con un comparador de 4 bits|Libro · Cap. 5 · P5.16|msi,comparador,c2|lb5.p516
@enun
A partir de un comparador de cuatro bits, diseña tres comparadores: uno para binario puro con complemento a 1, otro para binario puro con complemento a 2 y otro para binario con bit de signo.
@end
@antes
**El problema:** el comparador MSI trata sus 4 bits como un número **sin signo**. Si ambos operandos tienen el mismo signo, el orden es el mismo con o sin signo; si los signos difieren, el positivo siempre gana.
@end
@paso C-1 y C-2: el mismo circuito
Se usan $A_3$ y $B_3$ para gobernar dos multiplexores 4:1, uno para $A>B$ y otro para $A<B$: con $A_3B_3=00$ (ambos positivos) y $11$ (ambos negativos) se deja pasar la salida del comparador, porque en ambos casos el orden sin signo coincide con el orden con signo (p. ej. $1100$ vs $1001$: sin signo $12>9$, con signo $-4>-7$). Con $A_3B_3=01$ ($A$ positivo, $B$ negativo): $A>B=1$ y $A<B=0$. Con $10$: $A>B=0$ y $A<B=1$. La salida $A=B$ pasa directa.
@end
@paso Comparador con bit de signo
Antes del comparador se transcodifica cada operando a C-1 con cuatro XOR: si $A_3=1$ se invierte la magnitud $A_{2\text{-}0}$ ($A'=A_{2\text{-}0}\oplus A_3$) y si $A_3=0$ se deja igual. Después se usa el mismo circuito que antes. Ejemplo: $1100$ ($-4$ en signo y magnitud) y $1001$ ($-1$) se transcodifican a $1011$ y $1110$. Ambos son negativos, el comparador sin signo da $11<14$ y en efecto $-4<-1$.
@end
@paso Comprobación
Con los 256 pares de números en C-2, el circuito da exactamente la comparación aritmética. Con C-1 y con signo-magnitud, coincide en todos salvo en dos pares ordenados: el cero con cero negativo (en C-1: $0000$ y $1111$; con signo: $0000$ y $1000$), donde el circuito dice que el positivo es mayor en lugar de «iguales».
@end
@res
Un comparador de 4 bits y dos multiplexores 4:1 sirven para C-1 y C-2; para signo-magnitud se añaden dos cuartetos de XOR.

@box ojo | Errata en el libro
Con C-1 y con signo y magnitud hay **dos representaciones del cero** ($+0$ y $-0$). El circuito del libro las ordena ($+0>-0$) en vez de declararlas iguales; el libro no lo advierte. Si hace falta distinguirlo, hay que añadir una comprobación específica (por ejemplo, si los dos números son cero).
@end
@end
@end

@ej lb5-17|Sumador BCD exceso 3 con sumadores binarios|Libro · Cap. 5 · P5.17|msi,aritmetica,bcd|lb5.p517
@enun
Diseña un sumador de un dígito en BCD exceso 3 utilizando sumadores 4+4 en binario puro. Compruébalo con al menos tres ejemplos. ¿Es más sencillo un sumador BCD natural o uno en exceso 3? ¿Por qué?
@end
@antes
**Exceso 3:** el dígito $d$ se guarda como $d+3$. Al sumar dos dígitos se suman dos «+3», así que el resultado queda con un **exceso 6**. Hay que corregirlo para dejarlo con exceso 3 y, si la suma pasa de 9, pasar a la siguiente cifra.
@end
@paso Diseño
1) Un sumador 4+4 calcula $S'=A+B$. 2) Si $C'_{out}=0$ no hubo acarreo del dígito ($S'$ sigue en exceso 6 y la suma decimal es $\le9$): hay que restar 3, es decir, sumar $1101$. 3) Si $C'_{out}=1$ la suma decimal es $\ge10$, se genera acarreo y el resultado debe quedar en exceso 3: se suma $0011$. 4) La constante se obtiene con un inversor y un 1: $B_3=B_2=\overline{C'_{out}}$, $B_1=C'_{out}$, $B_0=1$. 5) Un segundo sumador 4+4 hace $S=S'+\text{constante}$. El acarreo de salida es $C'_{out}$.
@end
@paso Tres ejemplos
| $A$ | $B$ | $S'=A+B$ | $C'$ | se suma | $S$ | resultado |
|---|---|---|---|---|---|---|
| 0011 (0) | 0011 (0) | 0110 | 0 | 1101 | 0011 | 0, acarreo 0 |
| 0110 (3) | 1010 (7) | 0000 | 1 | 0011 | 0011 | 0, acarreo 1 (10) |
| 1100 (9) | 1100 (9) | 1000 | 1 | 0011 | 1011 | 8, acarreo 1 (18) |

El programa comprueba los 100 pares de dígitos.
@end
@paso ¿Cuál es más sencillo?
El de **exceso 3**: solo necesita un inversor para generar la constante. El BCD natural necesita detectar «suma $>9$ o acarreo» ($C'_{out}+S_3S_2+S_3S_1$, es decir, 2 AND y 1 OR de tres entradas) y además hacer la corrección $+0110$. La razón es que el exceso de 6 de la primera suma coincide con los 6 códigos que sobran en 4 bits: el acarreo binario es directamente el acarreo decimal y no hace falta detectar «>9». El programa simula ambos sumadores con los 100 pares.
@end
@res
Dos sumadores 4+4 y un inversor. El BCD natural cuesta además 2 AND y una OR de tres entradas.
@end
@end

@ej lb5-18|Binario de 5 bits a dos dígitos BCD|Libro · Cap. 5 · P5.18|msi,aritmetica,bcd|lb5.p518
@enun
Diseña un circuito que pase un número de cinco bits en binario puro a dos dígitos BCD.
@end
@antes
**Dividir entre 10:** un número entre 0 y 31 tiene como máximo 3 decenas. Cada vez que se pasa de 9 hay que «llevar» una decena, y como un dígito BCD usa 4 bits (16 combinaciones) para 10 valores, hay que sumar **6** para saltarse los códigos sobrantes.
@end
@paso Paso 1: los cuatro bits bajos
Se detecta si $A_{3\text{-}0}\ge10$ con $A_3A_2+A_3A_1$ (2 AND y una OR). Si es así se suma $0110$ con un sumador 4+4: $S'=A_{3\text{-}0}+(0\text{ ó }6)$; el acarreo $C_{out}S'$ vale 1 exactamente en ese caso (es la decena que hay que llevar).
@end
@paso Paso 2: el bit de peso 16
El bit $A_4$ vale 16, que es «1 decena y 6 unidades». Se le suma 6 al dígito de unidades: $RU=S'+(0\text{ ó }6)$ con $A_4$ como control. Esto debe hacerse con un **sumador BCD**, porque la suma puede pasar de 9 (por ejemplo $5+6=11$ ⇒ unidad 1 y acarreo 1).
@end
@paso Paso 3: decenas
$RD_{1\text{-}0}=A_4+C_{out}S'+C_{out}RU$ con un sumador 1+1 (valores 0 a 3).
@end
@paso Ejemplos
| $A_{4\text{-}0}$ | $S'$ | $RU$ | $RD$ |
|---|---|---|---|
| 00111 (7) | 0111 | 0111 (7) | 0 |
| 01100 (12) | 1100+0110 = 0010 | 0010 (2) | 0+1+0 = 1 |
| 11111 (31) | 1111+0110 = 0101 | 0101+0110 = 0001 (1) | 1+1+1 = 3 |

Se han simulado las 32 entradas y siempre sale el cociente y el resto de dividir entre 10.
@end
@res
Dos sumadores 4+4 (el segundo en BCD), un sumador 1+1 y una detección con 2 AND y 1 OR. Verificado con los 32 valores.

@box ojo | Errata en el libro
En el texto el criterio de corrección se enuncia como «$A_{3\text{-}0}$ mayor que 10», pero el circuito (que usa $A_3A_2+A_3A_1$) detecta $\ge10$, que es lo correcto: el valor 10 también necesita corrección.
@end
@end
@end

@ej lb5-19|Recinto con dos puertas y claves ligadas|Libro · Cap. 5 · P5.19|msi,comparador,aritmetica|lb5.p519
@enun
Para entrar en un recinto hay que pasar dos puertas, P1 y P2. En la P1 se introduce un dígito BCD mayor o igual que 6. En la P2, un número que esté a no más de tres unidades de la mitad del introducido en la P1 (si se introduce 8, hay que meter un número entre 1 —que es 4−3— y 7 —que es 4+3—). Diseña el circuito.
@end
@antes
**Dos condiciones independientes:** abrir P1 (un comparador) y abrir P2 (un intervalo, que son dos comparaciones). La puerta se abre si se cumplen las dos.
@end
@paso Puerta 1
Se necesita $P_1\ge6$, es decir, $P_1>5$: un comparador de 4 bits con la constante $0101$.
@end
@paso Puerta 2: dividir entre 2
Dividir entre 2 en binario puro es quitar el bit de menos peso: $P=P_{1\,3\text{-}1}$ (3 bits).
@end
@paso Puerta 2: los dos extremos
Un sumador 4+4 calcula $P+3$ ($P+0011$) y otro $P-3$, que se obtiene sumando $13$ ($1101$), porque $-3\equiv13 \pmod{16}$. Dos comparadores de 4 bits comparan $P_2$ con cada extremo: $P_2\le P+3$ (salidas «menor» o «igual») y $P_2\ge P-3$ (salidas «mayor» o «igual»). La puerta 2 se abre si se cumplen las dos: 2 OR y 1 AND.
@end
@paso Rango útil
Como $P_1\ge6$, $P$ vale 3 o 4, así que $P-3$ es 0 o 1 y nunca «da la vuelta» a números negativos. Por eso basta con comparar en binario puro.
@end
@paso Comprobación
El programa recorre $P_1\in0..9$ y $P_2\in0..15$ y confirma las dos condiciones.
@end
@res
Tres comparadores, dos sumadores 4+4, 3 puertas OR/AND. Con la corrección indicada abajo el circuito cumple el enunciado en todo el rango.

@box ojo | Errata en el libro
En el esquema el comparador de la puerta 1 tiene la constante $0101$ en la entrada $A$ y la clave $P_1$ en la $B$, y se toma la salida $A>B$. Eso da «$5>P_1$», o sea, abriría la puerta para $P_1<5$, justo al revés de lo que dice el enunciado ($P_1\ge6$). La solución es tomar la salida $A<B$ ($5<P_1$) o intercambiar las entradas. Comprobado por código.
@end
@end
@end

@ej lb5-20|Tres personas y cuatro leds según cuántos números coinciden|Libro · Cap. 5 · P5.20|msi,comparador|lb5.p520
@enun
Tres personas codifican con microinterruptores, cada una en dos bits, un número de 0 a 3. Diseña el circuito que active uno de los cuatro leds: L3 si los tres números son iguales, L2 si al menos dos son iguales, L2S si solo dos son iguales y L1 en el resto de casos.
@end
@antes
**Tres parejas posibles:** (A,B), (A,C) y (B,C). Si se comparan las tres parejas con comparadores de igualdad de 2 bits, cada led es una combinación sencilla de los tres resultados $e_{AB},e_{AC},e_{BC}$.
@end
@paso Comparar
Tres comparadores de 2 bits, usando solo la salida $A=B$.
@end
@paso L3 y L2
$L3=e_{AB}\,e_{BC}$ (si $A=B$ y $B=C$, los tres son iguales). $L2=e_{AB}+e_{AC}+e_{BC}$ (al menos una pareja coincide).
@end
@paso L2S
Solo una pareja coincide: $L2S=e_{AB}\overline{e_{AC}}+e_{AC}\overline{e_{BC}}+e_{BC}\overline{e_{AC}}$ (3 AND, un OR y 2 inversores). Es más fácil de leer como «hay exactamente una pareja que coincide».
@end
@paso L1
$L1=\overline{L3+L2+L2S}$, una NOR de tres entradas (o 3 inversores y 1 AND). Pero $L3$ y $L2S$ implican $L2$, así que $L1=\overline{L2}$ basta: **un solo inversor**.
@end
@paso Comprobación
Con las $4^3=64$ ternas, las cuatro salidas coinciden con la cuenta de cuántos valores distintos hay (1, 2 o 3).
@end
@res
Tres comparadores de 2 bits y unas pocas puertas. Verificado con las 64 ternas, y se ha comprobado que $L1=\overline{L2}$.
@end
@end

