%% id=x-dic
%% group=examdata
%% title=Diciembre (convocatoria sin año en el enunciado)
%% sub=4 problemas: recinto con comparadores, media de cuatro números BCD, contador JK+NAND y alarma de ventanas.
%% anio=Sin año
%% tipo=Parcial
%% orden=1000
%% featured=1

@ej xd-p1|P1 · Recinto con dos puertas (comparadores y sumadores)|Diciembre · P1|comb,msi,arit|recinto
@enun
Para entrar en un recinto hay que pasar por dos puertas, P1 y P2. Para entrar por P1 hay que introducir un dígito BCD mayor o igual a 6 y para pasar por la puerta P2 hay que introducir un número que esté tres unidades por arriba o por debajo de la mitad del número introducido en la puerta P1. Por ejemplo, si en la puerta P1 introducimos el 8, entramos por P1 y deberemos introducir en P2 un número entre el 1 $[(8/2)-3]$ y el 7 $[(8/2)+3]$. Diseñar el circuito lógico correspondiente.
@end
@antes
**Qué piden:** un circuito combinacional con dos entradas BCD ($P_1$, $P_2$) y dos salidas «abre P1» y «abre P2».
**Teoría:** comparadores y sumadores ([[t05|T5]]), dividir entre 2 como desplazamiento ([[t02|T2]]), C2 para el $-3$ ([[t02|T2]]).
@end
@paso Abrir P1
$P_1\ge6$ para $P_1\in\{0,\dots,9\}$ es $P_1>5$. Se usa un comparador de 4 bits con $B=0101$ y la salida $A>B$.
@end
@paso La mitad de $P_1$
Dividir entre 2 es **desplazar a la derecha**: se toman los bits $P_1(3{:}1)$ y se completan con un 0 en el MSB. El bit menos significativo se pierde (mitad entera): $9/2\to4$.
@end
@paso Los límites $h+3$ y $h-3$
Con $h=P_1/2$ (3 bits, ampliado a 4): un sumador de 4 bits con la constante $0011$ da $h+3$. Otro con la constante $1101$ (que es $-3$ en C2 de 4 bits) da $h-3$. Como $P_1\ge6$ implica $h\ge3$, el resultado $h-3$ nunca es negativo y se puede comparar **sin signo**. Se ha comprobado con las 40 combinaciones válidas de $(P_1,P_2)$.
@end
@paso Abrir P2
Dos comparadores de 4 bits: $P_2\le h+3$ (salidas $A<B$ o $A=B$ unidas con una OR) y $P_2\ge h-3$ ($A>B$ o $A=B$). «Abre P2» es la AND de ambos con «abre P1».
@end
@paso Tabla de valores permitidos
| $P_1$ | $h=P_1/2$ | $P_2$ permitido |
|---|---|---|
| 6 | 3 | 0 a 6 |
| 7 | 3 | 0 a 6 |
| 8 | 4 | 1 a 7 |
| 9 | 4 | 1 a 7 |
El caso $P_1=8$ coincide con el ejemplo del enunciado (1 a 7).
@end
@res
Abre P1 $=(P_1>0101)$; Abre P2 $=$ Abre P1 $\cdot(P_2\le h+3)\cdot(P_2\ge h-3)$ con $h=P_1(3{:}1)$. 2 comparadores de 4 bits para P2, 1 para P1 y 2 sumadores de 4 bits.
@end
@end

@ej xd-p2|P2 · Media de cuatro números de dos cifras en BCD|Diciembre · P2|arit,msi|media4
@enun
Realice el diseño de un circuito que haga la media de cuatro números de dos cifras dado en BCD.
@end
@antes
**Qué piden:** pasar los cuatro números de BCD a binario, sumarlos, dividir entre 4 y presentar el resultado.
**Teoría:** BCD ↔ binario ([[t02|T2]]), sumadores en cascada ([[t05|T5]]), dividir entre $2^k$ como desplazamiento.
@end
@paso De BCD a binario
Un número de dos cifras $d_1d_0$ vale $10d_1+d_0=8d_1+2d_1+d_0$. Multiplicar por 8 y por 2 son **desplazamientos** (cableado), así que basta un sumador: $(d_1\ll3)+(d_1\ll1)+d_0$. Cada número sale en binario de 7 bits (máximo $99<128$).
@end
@paso Sumar los cuatro
La suma máxima es $4\cdot99=396$. Como $2^8=256<396<512=2^9$, hacen falta **9 bits**. Se suman con tres sumadores (o dos niveles: $A+B$, $C+D$, y la suma de ambos).
@end
@paso Dividir entre 4
Dividir entre 4 es **descartar los dos bits menos significativos** de la suma de 9 bits. El resultado tiene 7 bits ($396/4=99$). Es la mitad entera de la mitad entera, calculada **una sola vez**: $\lfloor(A+B+C+D)/4\rfloor$.
@end
@paso Presentar en BCD
Para mostrar la media en dos displays hay que volver de binario a BCD (decenas y unidades). Se hace con comparadores y restas de 10, o con una ROM de 128 posiciones (ver [[t07|T7]]).
@end
@box erra | Ojo: la cascada de medias pierde precisión
Una solución típica hace $((A+B)/2+(C+D)/2)/2$ con dos desplazamientos. **No es equivalente**: cada desplazamiento descarta un bit que el siguiente necesitaba. Con $A=0,B=1,C=1,D=2$ la media entera correcta es $\lfloor4/4\rfloor=1$, pero la cascada da $(0+1)\gg1=0$. Sobre las $199\times199=39\,601$ combinaciones de $(A+B,\,C+D)$, la cascada falla en $4\,900$ (un {{media4.cascada_pct}} %), con error máximo de 1 unidad. Para una media exacta: suma primero **todo** y desplaza **una vez**.
@end
@res
BCD→binario con $8d_1+2d_1+d_0$; suma de los cuatro en 9 bits; media $=$ suma$(8{:}2)$ (7 bits). La versión en cascada de desplazamientos es incorrecta en {{media4.cascada_pct}} % de los casos.
@end
@end

@ej xd-p3|P3 · Contador síncrono reversible con JK y NAND|Diciembre · P3|cont,sec|cnt
@enun
Utilizando biestables J-K y puertas NAND, diseñar un contador síncrono que posea una entrada de control $X$ y que cumpla: (a) si $X=0$, el contador funciona en modo ascendente con la secuencia $0\to2\to4\to6\to1\to3\to5\to7\ [\to0\dots]$; (b) si $X=1$, funciona en modo descendente, siendo la secuencia de conteo $0\to7\to5\to3\to1\to6\to4\to2\ [\to0\dots]$.
@end
@antes
**Qué piden:** un contador de 3 bits con una secuencia no binaria y dos sentidos, con JK y solo NAND.
**Teoría:** diseño de contadores como autómata ([[t08|T8]], [[t10|T10]]); tabla de excitación del JK ([[t06|T6]]); NAND universal ([[t03|T3]]).
@end
@paso Estados y entradas
8 estados ($000$ a $111$), 3 biestables, una entrada $X$. Cada estado tiene dos sucesores: el siguiente en la lista (si $X=0$) o el anterior (si $X=1$). Es la misma secuencia recorrida en uno u otro sentido. La descendente enunciada es justo la ascendente al revés: $0,7,5,3,1,6,4,2$ ✓.
@end
@paso Tabla de transiciones
| $Q_2Q_1Q_0$ | $X=0$ | $X=1$ |
|---|---|---|
| 000 | 010 | 111 |
| 001 | 011 | 110 |
| 010 | 100 | 000 |
| 011 | 101 | 001 |
| 100 | 110 | 010 |
| 101 | 111 | 011 |
| 110 | 001 | 100 |
| 111 | 000 | 101 |
@end
@paso Ecuaciones con la tabla de excitación del JK
Se rellena $J$ y $K$ de cada biestable según $Q\to Q^+$ y se simplifica con Karnaugh de 4 variables $(Q_2,Q_1,Q_0,X)$:
$$J_2=K_2={{cnt.J2}}\qquad J_1=K_1={{cnt.J1}}$$
$$J_0=K_0={{cnt.J0}}$$
**Intuición:** $Q_1$ conmuta en cada ciclo (en ambas secuencias alterna 0,1,0,1…), por eso $J_1=K_1=1$. $Q_2$ conmuta cuando $Q_1\ne X$.
@end
@paso Pasarlo a NAND
Cada suma de productos se implementa en **dos niveles de NAND** (NAND-NAND). Para $J_2=K_2=\overline{Q_1}X+Q_1\overline{X}$: $J_2=\text{NAND}\big(\text{NAND}(\overline{Q_1},X),\ \text{NAND}(Q_1,\overline{X})\big)$. Las variables negadas salen de la salida $\overline{Q}$ de los biestables y de una NAND con las dos entradas unidas para $\overline{X}$. $J_1=K_1$ se conectan a nivel alto.
@end
@paso Comprobación
Las ecuaciones minimizadas, simuladas a nivel de puerta, reproducen la tabla en los 16 casos $(Q,X)$ y generan las secuencias ascendente {{cnt.up}} y descendente {{cnt.down}}.
@end
@res
$J_2=K_2={{cnt.J2}}$; $J_1=K_1=1$; $J_0=K_0={{cnt.J0}}$. Todo con NAND en dos niveles.
@end
@end

@ej xd-p4|P4 · Alarma de ventanas con barrido secuencial|Diciembre · P4|sec,msi,cont|ventanas
@enun
Un edificio de cuatro plantas tiene cuatro ventanas por planta. En cada ventana se coloca un sensor que detecta la apertura de la misma (0 cerrada, 1 abierta). Realice el diseño de un sistema de alarma que funcione así: dos displays (planta y número de ventana vigilada); un LED junto a los displays que se enciende si la ventana indicada está abierta; barrido secuencial cíclico, desde planta 1-ventana 1 hasta planta 4-ventana 4, de frecuencia 1 o 2 segundos seleccionable con un interruptor; en el momento en que se encuentre una ventana abierta el sistema se detendrá hasta que la ventana en cuestión se cierre.
@end
@antes
**Qué piden:** un contador que recorra las 16 ventanas, un selector que mire el sensor de la ventana actual y que **congele** el contador si está abierta.
**Teoría:** contador binario ([[t08|T8]]), multiplexor 16:1 ([[t05|T5]]), sumador para mostrar «1 a 4» en lugar de «0 a 3», decodificador BCD a 7 segmentos ([[t05|T5]]).
@end
@paso Contador de ventanas
Un contador binario de 4 bits $Q_3Q_2Q_1Q_0$. Los dos bits altos $Q_3Q_2$ son la **planta** (0 a 3) y los dos bajos $Q_1Q_0$ la **ventana** (0 a 3). Cuenta 16 estados y vuelve a 0: barrido cíclico.
@end
@paso Mirar el sensor de la ventana actual
Un multiplexor 16:1 con los 16 sensores en las entradas de datos y $Q_3Q_2Q_1Q_0$ en la selección da la señal $ABIERTA$ del sensor vigilado. Esa misma señal enciende el LED.
@end
@paso Detener el barrido
El contador **solo avanza si $ABIERTA=0$**: se usa $ABIERTA$ negada como habilitación del contador (o se hace AND de la señal de reloj con $\overline{ABIERTA}$). Mientras la ventana siga abierta, la selección no cambia y el LED sigue encendido. En cuanto se cierra, el barrido continúa. Mejor usar una **habilitación** que cortar el reloj: así no se generan pulsos cortos.
@end
@paso Frecuencia seleccionable
Se parte de un reloj de 1 Hz (periodo 1 s). Un biestable T con $T=1$ lo divide por 2 (periodo 2 s). Un multiplexor 2:1 controlado por el interruptor elige uno de los dos relojes.
@end
@paso Displays
Planta $=Q_3Q_2+1$ y ventana $=Q_1Q_0+1$ (valores de 1 a 4): un sumador de 2 bits con la constante $01$ para cada uno, y un decodificador BCD a 7 segmentos para cada display.
@end
@paso Comprobación
Con la ventana 5 (planta 2, ventana 2) abierta durante 10 ciclos, el contador se queda en ella los 10 ciclos y luego pasa a la siguiente. Los valores mostrados están siempre entre 1 y 4.
@end
@res
Contador de 4 bits (planta $Q_3Q_2$, ventana $Q_1Q_0$) + MUX 16:1 + habilitación $\overline{ABIERTA}$ + selector de reloj (1 Hz o 0,5 Hz) + dos sumadores «+1» y dos decodificadores 7 segmentos.
@end
@end
