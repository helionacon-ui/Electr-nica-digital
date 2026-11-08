%% id=p3
%% group=prac
%% n=3
%% title=Práctica 3 · Diseño de sistemas secuenciales
%% short=P3 · Secuenciales
%% sub=Contadores, divisor de frecuencia, antirrebote y máquinas de estados con reloj.
%% kicker=Prácticas (20 % de la nota)

## Objetivo

Diseñar sistemas sincronizados con reloj: contadores, registros y divisores de frecuencia, máquinas de estados y tratamiento del rebote de los pulsadores ([[t08|T8]], [[t09|T9]], [[t10|T10]]).

@ej p3-s1|Contador módulo N|Práctica 3|vhdl,cont|t8.mod10,t8.mod12
@enun
Diseña un contador síncrono de módulo $N$ configurable, con reset asíncrono, habilitación y una salida de fin de cuenta.
@end
@antes
Teoría: contador de módulo $N$, biestables $\lceil\log_2N\rceil$ ([[t08|T8]]); proceso síncrono con reset asíncrono ([[t13|T13]]).
@end
@paso Estructura
Un único proceso con `clk` y `rst` en la lista de sensibilidad. El reset va **antes** que el flanco.
@end
@paso Módulo N
Si `cnt = N-1` vuelve a 0; si no, incrementa. El `generic N` hace el diseño reutilizable.
@end
@paso Fin de cuenta
`fin` vale 1 cuando `cnt = N-1`: sirve para encadenar contadores.
@end
@res
Secuencia $0,1,\dots,N-1,0,\dots$. Para $N=10$: 4 biestables.
@end
@end

@codefile vhdl|p3_contador.vhd|vhdl/p3_contador.vhd|cnt

@ej p3-s2|Divisor de frecuencia|Práctica 3|vhdl,cont|t12.div
@enun
Genera una señal de 1 Hz a partir del reloj de 50 MHz de la placa y úsala para hacer parpadear un LED.
@end
@antes
Teoría: contador como divisor ([[t08|T8]]); $DIV=f_{in}/f_{out}$.
@end
@paso Cálculo
$DIV=50\,000\,000$. La salida conmuta cada $DIV/2=25\,000\,000$ ciclos: se cuenta de $0$ a $24\,999\,999$ (25 bits).
@end
@paso Código
Contador con comparación y una señal `s` que se invierte al llegar al final.
@end
@paso Prueba
En simulación no esperes 25 millones de ciclos: baja `DIV` (por ejemplo, a 10) en el *test bench* y comprueba la forma de onda.
@end
@res
LED parpadeando a 1 Hz (medio segundo encendido y medio apagado).
@end
@end

@codefile vhdl|p3_divisor.vhd|vhdl/p3_divisor.vhd|div

@ej p3-s3|Antirrebote de un pulsador|Práctica 3|vhdl,sec|t10.deb
@enun
Un pulsador mecánico rebota unos milisegundos. Diseña un circuito que entregue un nivel limpio.
@end
@antes
Teoría: sincronizar la entrada con 2 biestables para evitar la metaestabilidad ([[t06|T6]]) y aceptarla solo si permanece estable un tiempo ([[t10|T10]]).
@end
@paso Sincroniza
`s1` y `s2` son dos biestables D en serie: la entrada asíncrona se alinea con el reloj.
@end
@paso Cuenta de estabilidad
Si la entrada cambia, reinicia el contador. Si llega a `LIM` sin cambiar, acepta el valor.
@end
@paso Calcula LIM
20 ms a 50 MHz son $10^6$ ciclos: contador de 20 bits.
@end
@res
Un solo pulso limpio por pulsación, aunque la señal original rebote.
@end
@end

@codefile vhdl|p3_antirrebote.vhd|vhdl/p3_antirrebote.vhd|deb

@ej p3-s4|Máquina de estados: detector de secuencia|Práctica 3|vhdl,sec|t10.det101,t10.det_gates
@enun
Implementa en VHDL el detector Mealy de la secuencia 101 del [[t10|Tema 10]].
@end
@antes
Teoría: diagrama de estados de Mealy y su traducción a dos procesos.
@end
@paso Tipo enumerado
`type estado_t is (S0, S1, S2);` deja que la herramienta elija la codificación.
@end
@paso Dos procesos
El primero guarda el estado en el flanco. El segundo, combinacional, calcula `sig` y `z` con un `case`.
@end
@paso Evita latches
Asigna `z <= '0'` al principio del proceso combinacional: así `z` se asigna en **todos** los casos.
@end
@res
Para $x=1,0,1,0,1,1,0,1$ da $z=0,0,1,0,1,0,0,1$.
@end
@end

@codefile vhdl|p3_detector101.vhd|vhdl/p3_detector101.vhd|det

## Salida esperada

@codefile text|Resultado del modelo Python|salidas/p3.txt

## Qué escribir en la memoria

- El diagrama de estados del detector y la tabla de transiciones.
- El cálculo de $DIV$ y del número de bits del contador del divisor.
- Una captura de la señal del pulsador **con rebotes** y la salida del filtro.
- Una discusión de por qué el reset asíncrono puede dar problemas y cuándo conviene el síncrono.
