%% id=x-feb25
%% group=examdata
%% title=Febrero 2025 (convocatoria del 23/01/2025)
%% sub=4 problemas: aritmética con display, decodificador, expendedora (Mealy) y noria (Moore).
%% anio=2024-25
%% tipo=Final
%% orden=2025
%% featured=1

@ej x25-p1|P1 · Función $(A\cdot B)+C$ con números de 3 bits en C2 y display|Feb 2025 · P1|arit,msi|feb25.p1
@enun
Realice el diseño de un circuito que realice la función $(A\cdot B)+C$, siendo $A$, $B$ y $C$ números de 2 bits de valor más 1 de signo, es decir, si el bit de signo es 1 el número es negativo y está representado en complemento a 2. El resultado deberá visualizarse en los displays de 7 segmentos que consideres necesarios.
@end
@antes
**Qué piden:** un circuito combinacional con entradas de 3 bits en C2 ($-4$ a $3$) que multiplique, sume y muestre el resultado con signo en decimal.
**Teoría que usas:** C2 y su rango ([[t02|T2]]), sumadores y multiplicadores ([[t05|T5]]), BCD y display de 7 segmentos ([[t05|T5]]). Idea clave: multiplicar **valores absolutos** (más fácil: sin signo) y corregir el signo al final.
@end
@paso Rango del resultado (decide cuántos bits y cuántos displays)
$A,B\in[-4,3]$, luego $A\cdot B\in[-12,16]$ y $A\cdot B+C\in[-16,19]$. El módulo llega a 19: **dos dígitos** (decenas 0 o 1, y unidades) más un indicador de signo. Cabe en 6 bits en C2 ($[-32,31]$). Rango comprobado por código.
@end
@paso Valor absoluto de $A$ y de $B$
Con $s$ el bit de signo: $|X|=X\oplus s$ (XOR de cada bit con $s$) **más** $s$ (acarreo de entrada de un sumador). Es el «invertir y sumar 1» del C2, que solo se aplica si es negativo. Resultado de 3 bits sin signo (el $-4=100$ da $|{-4}|=4=100$).
@end
@paso Producto sin signo
Un multiplicador $3\times3$ de AND y sumadores da $P=|A|\cdot|B|\le 4\cdot4=16$: **5 bits**.
@end
@paso Signo del producto y paso a C2
El producto es negativo si los signos son distintos: $s_P=s_A\oplus s_B$. Se amplía $P$ a 6 bits y se convierte a C2 con el mismo truco XOR + $s_P$ como acarreo.
@end
@paso Sumar $C$
Se extiende el signo de $C$ a 6 bits (se repite su MSB) y se suma con un sumador de 6 bits: $R=P_{C2}+C$.
@end
@paso Presentar con signo y en decimal
El signo de $R$ es su bit 5: va a un segmento «$-$» (o a un LED). El módulo $M=|R|$ se obtiene otra vez con XOR + $s_R$. Para pasar a BCD: **decenas** $=1$ si $M\ge10$ (comparador); **unidades** $=M-10$ si hay decenas, es decir $M+6$ quedándose con 4 bits. Dos decodificadores BCD a 7 segmentos ([[t05|T5]]).
@end
@paso Comprobación
El diseño se ha simulado con las $8^3=512$ combinaciones y siempre coincide con $A\cdot B+C$ en signo, decenas y unidades.
@end
@res
Valor absoluto (XOR + sumador) → multiplicador $3\times3$ → signo $s_A\oplus s_B$ y paso a C2 en 6 bits → suma de $C$ extendido → signo y módulo → BCD (decenas $=M\ge10$, unidades $=M+6$ módulo 16) → 2 displays y un segmento de signo. Rango $[-16,19]$.
@end
@end

@ej x25-p2|P2 · Decodificador 4:16 con decodificadores 2:4|Feb 2025 · P2|msi,comb|feb25.p2
@enun
Realizar un decodificador de 4 entradas y 16 salidas a partir de decodificadores de 2 entradas y 4 salidas (con entrada de habilitación $E$ activa a 1; si $E=0$ todas las salidas valen 0).
@end
@antes
**Qué piden:** construir un 4:16 con piezas 2:4.
**Teoría:** cada salida de un decodificador es un minitérmino; la entrada $E$ permite **habilitar** un decodificador sin tocar los demás ([[t05|T5]]).
@end
@paso Cuántas piezas hacen falta
Son 16 salidas y cada 2:4 da 4: $16/4=4$ decodificadores para las salidas, más **1** para decidir cuál de ellos trabaja: 5 en total.
@end
@paso Reparto de entradas
Los bits altos $A_3A_2$ entran en el decodificador de arriba (con $E=1$ siempre). Sus cuatro salidas $S_0\dots S_3$ van a la entrada $E$ de cada uno de los cuatro decodificadores de abajo. Los bits bajos $A_1A_0$ entran en **los cuatro** a la vez.
@end
@paso Por qué funciona
Para $A=1011_2=11$: arriba $A_3A_2=10$ activa $S_2$, que habilita al tercer decodificador; este recibe $A_1A_0=11$ y activa su salida 3. La salida activa es $4\cdot2+3=11$ ✓.
@end
@fig dectree {"cap":"Esquema de la solución."}
@res
Cinco decodificadores 2:4. Salida $4k+j$ activa $\iff$ $A_3A_2=k$ y $A_1A_0=j$. Verificado para las 16 entradas.
@end
@end

@ej x25-p3|P3 · Expendedora de tabaco (Mealy, biestables T y JK)|Feb 2025 · P3|sec|feb25.p3
@enun
Una máquina expendedora de tabaco está controlada por un circuito secuencial. Recibe como entradas el código de dos bits de las monedas que se introducen ($M_1M_0$: $00$ no hay moneda, $01$ moneda de 50 cts, $10$ moneda de 1 €, $11$ error) y activa dos señales: si se debe entregar el tabaco ($T$) y la cantidad de cambio a reintegrar ($C_0$: $00$ no cambio y no tabaco; $01$ no cambio y da tabaco; $10$ no procede; $11$ da cambio y da tabaco). El usuario introduce monedas hasta alcanzar 2 €, que es el precio. Al alcanzar o superar el importe, la máquina sirve el tabaco y devuelve el cambio. Diseña el circuito (Mealy o Moore) indicando: número y codificación de estados, diagrama de estados, tabla de transiciones y salidas con un biestable T para el bit más significativo del estado y JK para el resto, e implementación con mapas de Karnaugh.
@end
@antes
**Qué piden:** un autómata que acumule dinero y dispare $T$ (y $C_0$) al llegar a 2 €.
**Teoría:** método de diseño de autómatas ([[t10|T10]]): estados → diagrama → tabla → tabla de excitación de T y JK ([[t06|T6]]) → Karnaugh ([[t03|T3]]).
@end
@box ojo | Ojo con el enunciado
El ejemplo del enunciado habla de «monedas de 25», pero la Tabla 1 solo tiene monedas de **50 cts y 1 €**. Aquí se resuelve con esas dos monedas: el cambio posible es siempre una moneda de 50 cts (si el total llega a 2,5 €). El código $11$ de entrada (error) se trata como «sin moneda».
@end
@paso Estados
Lo único que hay que recordar es **cuánto dinero hay**: 0 €, 0,5 €, 1 € o 1,5 € (al llegar a 2 € se sirve y se vuelve a 0). **4 estados**, 2 biestables: $S_0=00$, $S_1=01$, $S_2=10$, $S_3=11$ (el código es el dinero en medios euros). Es Mealy: la salida $T,C_0$ depende del estado **y de la moneda** que cae.
@end
@fig fsm {"nodes":{"S0":[60,110,"0 €"],"S1":[220,110,"0,5 €"],"S2":[380,110,"1 €"],"S3":[540,110,"1,5 €"]},"edges":[["S0","S0","00/00",0],["S0","S1","01/00",0],["S0","S2","10/00",-70],["S1","S1","00/00",0],["S1","S2","01/00",0],["S1","S3","10/00",-70],["S2","S2","00/00",0],["S2","S3","01/00",0],["S2","S0","10/10",90],["S3","S3","00/00",0],["S3","S0","01/10, 10/11",110]],"W":620,"H":260,"title":"Etiquetas: M1M0 / T C0","cap":"Al llegar a 2 € (T=1) se vuelve a S0. Con 1,5 € y moneda de 1 € se pasa a 2,5 € y se devuelve 50 cts (C0=1)."}
@paso Tabla de transiciones
| $Q_1Q_0$ | $M_1M_0$ | $Q_1^+Q_0^+$ | $T$ | $C_0$ |
|---|---|---|---|---|
| 00 | 00/11 | 00 | 0 | 0 |
| 00 | 01 | 01 | 0 | 0 |
| 00 | 10 | 10 | 0 | 0 |
| 01 | 00/11 | 01 | 0 | 0 |
| 01 | 01 | 10 | 0 | 0 |
| 01 | 10 | 11 | 0 | 0 |
| 10 | 00/11 | 10 | 0 | 0 |
| 10 | 01 | 11 | 0 | 0 |
| 10 | 10 | 00 | 1 | 0 |
| 11 | 00/11 | 11 | 0 | 0 |
| 11 | 01 | 00 | 1 | 0 |
| 11 | 10 | 00 | 1 | 1 |
@end
@paso Tabla de excitación
Para el biestable T del bit alto: $T_1=Q_1\oplus Q_1^+$ (1 si cambia). Para el JK del bit bajo se usa la tabla de excitación de [[t06|T6]]: $0\to0$: $J=0,K=X$; $0\to1$: $J=1,K=X$; $1\to0$: $J=X,K=1$; $1\to1$: $J=X,K=0$.
@end
@paso Ecuaciones (Karnaugh de 4 variables $Q_1,Q_0,M_1,M_0$)
$$T_1={{tab.T1}}$$
$$J_0={{tab.J0}}\qquad K_0={{tab.K0}}$$
$$T={{tab.T}}\qquad C_0={{tab.C0}}$$
Se simplifica cada una con un mapa de Karnaugh de 4 variables, con las filas $M_1M_0=11$ tratadas como moneda inexistente.
@end
@paso Comprobación con el ejemplo
**Tres monedas: 50 cts, 50 cts, 1 €.** Estados: $S_1\to S_2\to S_0$; en la última, $T=1$, $C_0=0$ (2 € justos, sin cambio).
**Cuatro monedas: 50, 50, 50, 1 €.** $S_1\to S_2\to S_3\to S_0$ y en la última, $T=1$ y $C_0=1$ (2,5 € ⇒ 50 cts de cambio).
@end
@res
4 estados (dinero acumulado), 2 biestables. $T_1={{tab.T1}}$; $J_0={{tab.J0}}$, $K_0={{tab.K0}}$; $T={{tab.T}}$; $C_0={{tab.C0}}$. Verificado con todas las secuencias de hasta 7 monedas contra una especificación aritmética independiente.
@end
@end

@ej x25-p4|P4 · Noria con dos motores (Moore, biestables JK)|Feb 2025 · P4|sec|noria
@enun
El mecanismo de una noria de un parque de atracciones dispone de dos motores que permiten que la noria gire en un sentido o en el inverso. Estos dos motores se gobiernan por medio de dos señales ($M_A$ y $M_B$) de tal manera que cuando una de ellas se pone a «1» se pone en funcionamiento el motor correspondiente. El empleado de controlar la atracción dispone de dos pulsadores ($A$ y $B$), de manera que al pulsar uno de ellos se acciona el motor correspondiente. Si se acciona dos veces seguidas el mismo pulsador, la noria se detiene. Además, en el puesto de control central se dispone de otro pulsador ($P$) que en caso de ser accionado detiene la noria. (Los pulsadores están normalmente a nivel bajo, pasando a nivel alto cuando se accionan.) Diseña el autómata.
@end
@antes
**Qué piden:** un autómata que recuerde qué motor está en marcha y si el último pulsador fue el mismo.
**Teoría:** Moore (salida solo del estado) y diseño con JK ([[t10|T10]], [[t06|T6]]). Hay que distinguir «sigo con el dedo en el botón» de «he vuelto a pulsar».
@end
@box ojo | Suposiciones que hay que declarar
- $A$ y $B$ no se pulsan a la vez ($AB=11$ no ocurre: indiferente).
- $P$ tiene prioridad sobre todo: si $P=1$ se va a parada.
- «Dos veces seguidas el mismo pulsador» = soltar y volver a pulsar el mismo. Mantener pulsado **no** cuenta como dos pulsaciones.
- Pulsar el **otro** botón cambia el sentido sin pararse.
@end
@paso Estados (6) y codificación
| Estado | Código $Q_2Q_1Q_0$ | Significado | $M_A$ | $M_B$ |
|---|---|---|---|---|
| $S_0$ | 000 | Parada | 0 | 0 |
| $S_1$ | 001 | Gira A, botón A aún pulsado | 1 | 0 |
| $S_2$ | 010 | Gira A, botón soltado (otra pulsación de A parará) | 1 | 0 |
| $S_3$ | 011 | Gira B, botón B aún pulsado | 0 | 1 |
| $S_4$ | 100 | Gira B, botón soltado | 0 | 1 |
| $S_5$ | 101 | Parada, esperando a soltar el botón | 0 | 0 |
Los códigos $110$ y $111$ no se usan (indiferentes). Necesitas 3 biestables: $2^2<6\le2^3$.
@end
@paso Transiciones (entradas $A,B,P$)
- $S_0$: $P\to S_0$; $A\to S_1$; $B\to S_3$; nada $\to S_0$.
- $S_1$: $P\to S_0$; $A\to S_1$ (sigue pulsado); $B\to S_3$; nada $\to S_2$.
- $S_2$: $P\to S_0$; $A\to S_5$ (segunda pulsación de A: para); $B\to S_3$; nada $\to S_2$.
- $S_3$: $P\to S_0$; $B\to S_3$; $A\to S_1$; nada $\to S_4$.
- $S_4$: $P\to S_0$; $B\to S_5$ (para); $A\to S_1$; nada $\to S_4$.
- $S_5$: si nada y $P=0$ $\to S_0$; si no, se queda en $S_5$ (evita que mantener el botón rearranque).
@end
@paso Ecuaciones de entrada de los JK (Karnaugh de 6 variables)
$$J_2={{noria.J2}}\qquad K_2={{noria.K2}}$$
$$J_1={{noria.J1}}\qquad K_1={{noria.K1}}$$
$$J_0={{noria.J0}}\qquad K_0={{noria.K0}}$$
Cada una sale de aplicar la tabla de excitación del JK a las 6 variables $Q_2,Q_1,Q_0,A,B,P$ con indiferentes en los estados 6 y 7 y en $AB=11$.
@end
@paso Salidas (Moore)
$$M_A={{noria.MA}}\qquad M_B={{noria.MB}}$$
Dependen solo de $Q$: $M_A=1$ en $S_1,S_2$ y $M_B=1$ en $S_3,S_4$.
@end
@paso Comprobación con escenarios
Pulsación larga de $A$: gira A y sigue. $A$, soltar, $A$: para. $A$, soltar, $B$: cambia a giro B. $B$ y luego $P$: para. $A,A$ (para), $A$ de nuevo: arranca otra vez. Todos coinciden con el circuito de puertas.
@end
@res
6 estados, 3 JK, Moore. $M_A={{noria.MA}}$, $M_B={{noria.MB}}$. Ecuaciones de entrada: ver pasos. Comprobado con las ecuaciones minimizadas simuladas a nivel de puerta frente a la tabla.
@end
@end
