%% id=t01
%% group=tema
%% n=1
%% title=Tema 1 · Introducción a los sistemas digitales
%% short=T1 · Sistemas digitales
%% sub=Qué significa «digital», por qué se usa y cómo se representan 0 y 1.

## Analógico frente a digital

Una señal **analógica** puede tomar cualquier valor entre dos extremos (la tensión de un micrófono). Una señal **digital** solo toma un conjunto finito de valores, casi siempre dos: 0 y 1.

¿Por qué se prefiere lo digital?

- **Aguanta el ruido.** Si un 1 es «unos 5 V» y le llegan 4,6 V, sigue siendo un 1. El circuito siguiente lo limpia.
- **Se puede copiar sin pérdida.** Un fichero se duplica bit a bit.
- **Es programable.** El mismo hardware hace cosas distintas según el código.

El precio: hay que convertir lo real (temperatura, presión, señal ECG) en números. Eso lo hacen los convertidores A/D.

## Representar 0 y 1 con tensiones

Un 1 y un 0 son **rangos** de tensión, no valores exactos. Entre ellos hay una zona prohibida. Lo verás en detalle en el [[t04|Tema 4]].

@fig noise {"voh":4.4,"vih":3.5,"vil":1.5,"vol":0.33,"vcc":5,"title":"Niveles lógicos de una familia CMOS de 5 V","cap":"A la salida, un 1 es cualquier tensión por encima de 4,4 V. A la entrada, el circuito acepta como 1 todo lo que supere 3,5 V. La diferencia (0,9 V) es el margen de ruido."}

## Lógica positiva y negativa

En **lógica positiva** el nivel alto significa 1. En **lógica negativa**, el nivel alto significa 0. Casi todo lo que verás es lógica positiva. Pero en las placas Basys los segmentos de los displays y algunos pulsadores son *activos a nivel bajo*: se encienden con un 0.

@box def | Señal activa a nivel alto o bajo
Una señal está **activa a nivel alto** si hace su trabajo cuando vale 1, y **activa a nivel bajo** si lo hace cuando vale 0. En los esquemas, la activa a nivel bajo lleva un círculo en su pin o una barra encima ($\overline{CLR}$, $\overline{LD}$).
@end

## Tipos de sistemas digitales

@fig bloques_comb_sec {}

Un **sistema combinacional** no recuerda nada. Un **sistema secuencial** tiene memoria y un reloj. Esta división organiza todo el temario:

| | Combinacional | Secuencial |
|---|---|---|
| Salida depende de | Entradas actuales | Entradas actuales y pasado |
| Elemento básico | Puerta lógica | Biestable |
| Se describe con | Tabla de verdad, ecuación | Diagrama de estados, tabla de transiciones |
| Ejemplos | Sumador, multiplexor, decodificador | Contador, registro, autómata |

@box falla | Qué suele fallar
- Pensar que una puerta «recuerda». No: una puerta solo calcula.
- Olvidar que un 0 o un 1 reales son *rangos*. Dos circuitos solo se pueden conectar directamente si sus rangos encajan (Tema 4).
@end
