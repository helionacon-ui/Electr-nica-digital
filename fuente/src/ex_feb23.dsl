%% id=x-feb23
%% group=examdata
%% title=Febrero 2023 (convocatoria del 22/01/2023)
%% sub=Problemas 1, 2 y 4: sensores con signo, toldo y caja fuerte. El problema 3 (contador de la figura) no se resuelve aquí.
%% anio=2022-23
%% tipo=Final
%% orden=2023
%% featured=1

@ej x23-p1|P1 · Dos sensores en C2: diferencia y media|Feb 2023 · P1|arit,msi|feb23.p1
@enun
Un dispositivo industrial utiliza dos sensores para la medida. Estos sensores son idénticos y están midiendo la misma variable, aunque su medida puede diferir. Las dos medidas se entregan a un sistema digital codificadas cada una con 4 bits en complemento a 2 ($A_3A_0$ para el sensor 1 y $B_3B_0$ para el sensor 2; $A_3$ y $B_3$ son los bits de signo). Para visualizar la medida se dispone de dos displays de 7 segmentos. En uno de ellos se visualizará la diferencia de valores y en el otro la media de las dos medidas. El signo se representará mediante un led. Diseñar mediante bloques combinacionales estándares (multiplexores, decodificadores, sumadores, comparadores...) el esquema del circuito combinacional.
@end
@antes
**Qué piden:** restar y promediar dos números en C2, mostrar el módulo en un display y el signo en un LED.
**Teoría:** C2, extensión de signo y desbordamiento ([[t02|T2]]); sumador/restador y valor absoluto ([[t05|T5]]).
@end
@paso Rango de la diferencia
Cada medida va de $-8$ a $7$. La diferencia $A-B$ va de $-15$ a $15$: **5 bits** en C2. Para no desbordar, primero se **extiende el signo** de $A$ y $B$ a 5 bits (se repite el MSB).
@end
@paso Restar con un sumador
$A-B=A+\overline{B}+1$: un sumador de 5 bits, con $B$ negada y $C_{in}=1$. El bit 4 del resultado es el **signo**: va al LED.
@end
@paso Módulo de la diferencia
$|D|=D\oplus s$ más $s$ como $C_{in}$ de un segundo sumador. El módulo va de 0 a 15 (4 bits).
@end
@paso Media
Se suman $A+B$ en 5 bits (rango $-16$ a $14$) y se divide entre 2 con un **desplazamiento aritmético** (se descarta el LSB y se repite el signo). La media va de $-8$ a $7$. El signo (otro LED o el mismo) es el MSB del desplazado.
@end
@paso Display
Un módulo de 0 a 15 en un solo display solo se puede mostrar en **hexadecimal** (0–F). Si se quiere decimal hace falta un segundo dígito. Para cada uno: decodificador a 7 segmentos.
@end
@box ojo | Redondeo de la media
El desplazamiento aritmético da $\lfloor(A+B)/2\rfloor$ (redondea hacia $-\infty$: $-1/2\to-1$). Truncar hacia cero daría $0$. Ambas son válidas, pero **hay que decir cuál** se usa. Coinciden salvo en 72 de las 256 combinaciones (suma impar y negativa).
@end
@res
Diferencia: sumador de 5 bits con $B$ invertida y $C_{in}=1$; signo = bit 4; módulo = XOR + sumador. Media: $A+B$ en 5 bits desplazado 1 a la derecha. Verificado con las 256 combinaciones.
@end
@end

@ej x23-p2|P2 · Circuito de control de un toldo|Feb 2023 · P2|comb|toldo
@enun
Se desea realizar un circuito de control para el toldo de una terraza. El toldo tiene la función tanto de dar sombra como de proteger del viento y de la lluvia. Entradas: $S$ (hay sol), $L$ (llueve), $V$ (hay mucho viento), $F$ (hace frío en el interior de la casa). Salida $BT$: si $BT=1$ el toldo debe estar extendido (bajado), si $BT=0$ recogido. Características: (1) siempre que llueva se extiende el toldo para evitar que moje la terraza (no se considera posible que simultáneamente llueva y haga sol); (2) si hace viento se debe extender el toldo, salvo si el día está soleado y hace frío en la casa: entonces se recoge para que el sol caliente la casa; (3) si no hace viento ni llueve, solo se baja el toldo en los días de sol y cuando haga calor en el interior.
Se pide: 1. Tabla de verdad de $BT(S,L,V,F)$. 2. Expresión reducida en suma de productos y en producto de sumas. 3. Esquema en puertas. 4. Variante con un interruptor manual/automático: en automático funciona como se ha descrito; en manual, un pulsador da la orden de recoger y otro de bajar, y el circuito debe mantener la orden tras soltarlos; si se pulsan ambos a la vez, el comportamiento debe ser predecible.
@end
@antes
**Qué piden:** pasar un texto a tabla de verdad, simplificar (SOP y POS) y añadir memoria en el modo manual.
**Teoría:** tabla de verdad y Karnaugh con indiferentes ([[t03|T3]]); biestables ([[t06|T6]]).
@end
@paso Traducir el texto a reglas
- Llueve ($L=1$) $\Rightarrow BT=1$.
- Viento ($V=1$) $\Rightarrow BT=1$, **salvo** $S=1$ y $F=1$ ($BT=0$).
- Sin lluvia ni viento: $BT=1$ solo si $S=1$ y $F=0$.
- $S=L=1$ **no ocurre**: son 4 combinaciones indiferentes.
@end
@paso Tabla de verdad (orden $S,L,V,F$)
$BT=1$ en las filas $2,3,4,5,6,7,8,10$ (con $S=L=1$, filas $12$ a $15$, indiferentes). En el resto, $BT=0$.
@end
@fig kmap {"key":"toldo","n":4,"names":["S","L","V","F"],"title":"BT con indiferentes","cap":"Mapa de Karnaugh con las filas $S=L=1$ como indiferentes."}
@paso Suma de productos
Tres grupos: $L$ (cuatro casillas con indiferentes), $\overline{S}V$ y $S\overline{F}$:
$$BT={{toldo.sop}}$$
@end
@paso Producto de sumas
Se agrupan los ceros y se niega: $BT={{toldo.pos}}$. Comprobación: ambas coinciden en las 12 filas posibles.
@end
@paso Modo manual con memoria
En manual hay que **recordar** la orden tras soltar los pulsadores: un biestable $Q$. Sea $U$ «recoger» y $D$ «bajar». $Q^+=\overline{U}\,(D+Q)$: $U$ tiene prioridad (si se pulsan ambos, se recoge: comportamiento predecible y **seguro**), $D$ pone $Q=1$ y se mantiene hasta que se pulse $U$. La salida es $BT=M\cdot Q+\overline{M}\cdot BT_{auto}$ (un multiplexor 2:1 controlado por $M$).
@end
@res
$BT={{toldo.sop}}={{toldo.pos}}$. Manual: biestable con $Q^+=\overline{U}(D+Q)$ y un MUX para elegir manual o automático. Verificado con las 12 combinaciones posibles.
@end
@end

@ej x23-p4|P4 · Caja fuerte: secuencia A, A, B, A (Mealy con JK)|Feb 2023 · P4|sec|caja
@enun
El sistema de apertura de una caja fuerte está compuesto por dos teclas A y B, un circuito secuencial a diseñar y un temporizador que mantiene la caja fuerte abierta durante 5 minutos cuando recibe un nivel lógico 1 desde el circuito secuencial. Este temporizador vuelve a cerrar la caja fuerte pasado dicho tiempo. Mientras no se pulse ninguna tecla no se genera ningún nivel lógico de entrada al circuito secuencial. Para abrir la caja fuerte, la combinación secreta es: pulsar dos veces seguidas la tecla A, a continuación pulsar una vez la tecla B, y finalmente pulsar una vez la tecla A. Si se hace de esta manera, el circuito secuencial dará una salida a nivel lógico 1 que actuará sobre el temporizador. Si en cualquier momento se introdujera un error al pulsar la secuencia secreta, en el siguiente ciclo de reloj todos los biestables se pondrán a cero (el sistema pasará al estado inicial) y la secuencia debe volver a introducirse desde el principio. 1. Dibujar el diagrama de estados, explicando claramente en qué consiste cada estado. 2. Implementar el circuito secuencial usando biestables JK y las puertas necesarias.
@end
@antes
**Qué piden:** un detector de la secuencia A-A-B-A, con las pulsaciones separadas, que reinicia ante cualquier error.
**Teoría:** diseño de autómatas ([[t10|T10]]), tabla de excitación del JK ([[t06|T6]]), Karnaugh de 5 variables.
@end
@box ojo | Suposiciones que hay que declarar
El enunciado no fija cómo llegan las teclas. Se supone **dos líneas**: $a=1$ si se pulsa A y $b=1$ si se pulsa B ($ab=00$: ninguna tecla; $ab=11$ no ocurre: indiferente). «Pulsar dos veces seguidas A» = pulsar, soltar y pulsar de nuevo A (dos pulsaciones). Mantener la tecla varios ciclos cuenta como **una** pulsación. Después de abrir se espera a soltar A antes de volver a empezar.
@end
@paso Estados (8)
| Estado | Significado |
|---|---|
| $S_0$ | Reposo, esperando la primera A |
| $S_1$ | A nº1 pulsada (se mantiene) |
| $S_2$ | A nº1 soltada, espera A nº2 |
| $S_3$ | A nº2 pulsada (se mantiene) |
| $S_4$ | A nº2 soltada, espera B |
| $S_5$ | B pulsada (se mantiene) |
| $S_6$ | B soltada, espera A nº3 |
| $S_7$ | A final pulsada: caja abierta, espera soltar |
Son 8 estados: **3 biestables**, código $Q_2Q_1Q_0$ igual al número del estado.
@end
@paso Transiciones
- «Esperando una tecla» ($S_2,S_4,S_6$): sin tecla se queda; con la tecla correcta avanza; con la incorrecta, vuelve a $S_0$.
- «Tecla pulsada» ($S_1,S_3,S_5$): si se mantiene, se queda; si se suelta, avanza; si se pulsa otra, error y vuelve a $S_0$.
- $S_0$: con A va a $S_1$; con B va a $S_0$ (error).
- $S_6$ con A: pasa a $S_7$ y **$Z=1$**.
- $S_7$: mientras A siga pulsada se queda; si no, vuelve a $S_0$.
@end
@paso Ecuaciones (Karnaugh de 5 variables $Q_2,Q_1,Q_0,a,b$ con $ab=11$ indiferente)
$$J_2={{caja.J2}}\qquad K_2={{caja.K2}}$$
$$J_1={{caja.J1}}\qquad K_1={{caja.K1}}$$
$$J_0={{caja.J0}}\qquad K_0={{caja.K0}}$$
$$Z={{caja.Z}}$$
@end
@paso Comprobación
Las ecuaciones, simuladas a nivel de puerta, reproducen el diagrama en todas las transiciones y generan $Z=1$ solo con la secuencia correcta. Se han comparado con una especificación independiente en las {{caja.n_tests}} secuencias de entrada de hasta 8 ciclos: sin discrepancias. Si en la secuencia hay un error, no se abre; si A se mantiene dos ciclos, cuenta como una sola pulsación.
@end
@res
8 estados, 3 JK. $Z={{caja.Z}}$. $J_2={{caja.J2}}$, $K_2={{caja.K2}}$, $J_1={{caja.J1}}$, $K_1={{caja.K1}}$, $J_0={{caja.J0}}$, $K_0={{caja.K0}}$ (en total {{caja.terminos}} términos y {{caja.literales}} literales).
@end
@end
