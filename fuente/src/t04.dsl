%% id=t04
%% group=tema
%% n=4
%% title=Tema 4 · Familias lógicas
%% short=T4 · Familias lógicas
%% sub=Qué hay dentro de una puerta real: niveles de tensión, márgenes de ruido, fan-out, consumo y retardo.

@box idea | Desde cero
Hasta ahora una puerta era un símbolo perfecto. En la realidad es un circuito con transistores, con **tensiones** que no son exactamente 0 y 5 V, que **consume** energía y que **tarda** un poco en responder. Una **familia lógica** es un conjunto de puertas fabricadas con la misma tecnología (TTL, CMOS…) y diseñadas para conectarse entre sí. Este tema responde: ¿se pueden conectar estas dos puertas? ¿Cuántas? ¿Qué velocidad y consumo tendrá el conjunto?
@end

## Niveles lógicos y margen de ruido

Un 0 o un 1 es un **rango** de tensión. Cada familia da cuatro números (valores típicos de un 74LS de TTL y de un 74HC de CMOS a 5 V):

| Parámetro | Significa | TTL (74LS) | CMOS (74HC) |
|---|---|---|---|
| $V_{OH}$ | salida mínima en nivel alto | 2,7 V | 4,4 V |
| $V_{OL}$ | salida máxima en nivel bajo | 0,5 V | 0,33 V |
| $V_{IH}$ | entrada mínima que se reconoce como alta | 2,0 V | 3,5 V |
| $V_{IL}$ | entrada máxima que se reconoce como baja | 0,8 V | 1,5 V |

La salida de una puerta alimenta la entrada de la siguiente. Para que funcione, lo que **garantiza** la salida debe cumplir lo que **exige** la entrada. La diferencia es el **margen de ruido**: cuánto ruido puede sumarse al cable sin que se estropee el dato.

$$NM_H = V_{OH}-V_{IH}\qquad NM_L = V_{IL}-V_{OL}$$

@fig noise {"voh":4.4,"vih":3.5,"vil":1.5,"vol":0.33,"vcc":5,"title":"74HC a 5 V","cap":"Márgenes de ruido de CMOS: 0,9 V en alto y 1,17 V en bajo."}

@ej t4-e1|Márgenes de ruido de TTL y CMOS|Ejemplo T4|fam|t4.nm
@enun
Calcula los márgenes de ruido de la familia TTL (74LS) y de la CMOS (74HC) de la tabla anterior. ¿Cuál tolera más ruido?
@end
@antes
Teoría: $NM_H=V_{OH}-V_{IH}$ y $NM_L=V_{IL}-V_{OL}$. El margen **efectivo** de una conexión es el menor de los dos.
@end
@paso TTL
$NM_H=2{,}7-2{,}0=0{,}7$ V y $NM_L=0{,}8-0{,}5=0{,}3$ V.
@end
@paso CMOS
$NM_H=4{,}4-3{,}5=0{,}9$ V y $NM_L=1{,}5-0{,}33=1{,}17$ V.
@end
@paso Compara
El peor caso de TTL es $0{,}3$ V; el de CMOS, $0{,}9$ V. CMOS aguanta el triple de ruido en el peor caso.
@end
@res
TTL: $0{,}7$ V y $0{,}3$ V. CMOS: $0{,}9$ V y $1{,}17$ V. Gana CMOS.
@end
@end

@sim familias

## Fan-out: cuántas puertas puede mover una salida

Cada entrada **absorbe** o **suministra** algo de corriente. Una salida solo puede dar una corriente máxima. El **fan-out** es el número de entradas que una salida puede alimentar sin salirse de los niveles garantizados. Se calcula para cada nivel y vale el **menor**:

$$\text{fan-out}=\min\left(\frac{I_{OL}}{I_{IL}},\;\frac{I_{OH}}{I_{IH}}\right)$$

Para un 74LS: $I_{OL}=8$ mA e $I_{IL}=0{,}4$ mA dan 20; $I_{OH}=0{,}4$ mA e $I_{IH}=20\ \mu$A dan 20. El fan-out es **20**. En CMOS las entradas casi no toman corriente, así que el límite real lo pone la capacidad (retardo), no la corriente.

## Retardo y potencia

- **Retardo de propagación** $t_{pd}$: lo que tarda la salida en reaccionar cuando cambia la entrada. En una cadena de puertas, **los retardos se suman**: 5 puertas de 10 ns dan 50 ns.
- **Potencia en CMOS:** casi no consume en reposo, pero **cada conmutación** carga y descarga una capacidad:

$$P_{din}=C\,V_{DD}^2\,f$$

Con $C=20$ pF, $V_{DD}=5$ V y $f=1$ MHz: $P=20\cdot10^{-12}\cdot25\cdot10^{6}=0{,}5$ mW. Doblar la frecuencia dobla la potencia; doblar la tensión la multiplica por cuatro.

@fig cmos {"cap":"Inversor CMOS: con la entrada a 0 conduce el PMOS y la salida va a VDD; con la entrada a 1 conduce el NMOS y va a tierra. Nunca conducen los dos a la vez, por eso casi no consume en reposo."}

## Salidas especiales

- **Colector abierto / drenador abierto:** la salida solo sabe llevar a 0; para el 1 hace falta una resistencia externa (*pull-up*). Permite conectar varias salidas al mismo cable (AND cableada).
- **Tres estados (*tri-state*):** la salida puede estar en 0, 1 o **alta impedancia** (Z, «desconectada»). Permite que muchos dispositivos compartan un bus: solo uno habilita su salida a la vez.
- **Entradas sin conectar:** en CMOS una entrada al aire **flota** y puede oscilar y consumir. Conéctala siempre a 0 o a 1.

@box falla | Qué suele fallar
- Comparar $V_{OH}$ con $V_{OL}$ en vez de $V_{OH}$ con $V_{IH}$ para el margen.
- Dar como fan-out el cociente de un solo nivel en lugar del **mínimo** de los dos.
- Sumar retardos en paralelo: solo se suman los de la **ruta más larga**.
- Creer que CMOS no consume: no consume en reposo, pero sí al conmutar, y crece con la frecuencia.
- Conectar dos salidas totem-pole directamente: si una da 1 y otra 0, hay cortocircuito. Para eso existen colector abierto y tres estados.
@end

@box formula | Fórmulas clave
- $NM_H=V_{OH}-V_{IH}$, $NM_L=V_{IL}-V_{OL}$.
- fan-out $=\min(I_{OL}/I_{IL},\,I_{OH}/I_{IH})$.
- $P_{din}=C\,V_{DD}^2\,f$.
- Retardo de una ruta: suma de los $t_{pd}$ de sus puertas.
@end

@card ¿Margen de ruido en nivel alto? || $NM_H=V_{OH}-V_{IH}$.
@card ¿Cómo se calcula el fan-out? || El menor de $I_{OL}/I_{IL}$ y $I_{OH}/I_{IH}$.
@card ¿Para qué sirve el colector abierto? || Permite unir varias salidas en un cable (AND cableada) usando una resistencia pull-up.
@card ¿Qué es el estado Z? || Alta impedancia: la salida queda desconectada. Permite compartir un bus.
@card ¿De qué depende la potencia dinámica de CMOS? || De la capacidad, de la tensión al cuadrado y de la frecuencia.
@gloss Margen de ruido | Cuánto ruido tolera una conexión sin que se interprete mal el nivel lógico.
@gloss Fan-out | Número máximo de entradas que una salida puede alimentar.
@gloss Retardo de propagación | Tiempo que tarda la salida en reaccionar a un cambio de la entrada.
@gloss Colector abierto | Salida que solo fuerza el 0; el 1 lo pone una resistencia externa.
@gloss Alta impedancia (Z) | Estado de una salida tri-state en el que está eléctricamente desconectada.

@q t4
Una puerta tiene $V_{OH}=2{,}7$ V y la siguiente exige $V_{IH}=2{,}0$ V. El margen de ruido en alto es:
+ 0,7 V
- 4,7 V
- 2,0 V
- 0,3 V
> $NM_H=V_{OH}-V_{IH}=0{,}7$ V.
@end
@q t4
Una salida da $I_{OL}=16$ mA y $I_{OH}=0{,}8$ mA; cada entrada pide $I_{IL}=0{,}8$ mA e $I_{IH}=40\ \mu$A. El fan-out es:
+ 20
- 40
- 16
- 1
> $16/0{,}8=20$ y $0{,}8\text{ mA}/40\ \mu\text{A}=20$. El mínimo es 20.
@end
@q t4
Una puerta CMOS conmuta a 2 MHz con $C=10$ pF y $V_{DD}=3$ V. Su potencia dinámica es:
+ 0,18 mW
- 0,06 mW
- 0,9 mW
- 1,8 mW
> $P=10\cdot10^{-12}\cdot 9\cdot 2\cdot10^{6}=1{,}8\cdot10^{-4}$ W $=0{,}18$ mW.
@end
