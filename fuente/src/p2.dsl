%% id=p2
%% group=prac
%% n=2
%% title=Práctica 2 · Diseño e implementación de sistemas combinacionales
%% short=P2 · Combinacional
%% sub=Sumador, comparador, multiplexor y display de 7 segmentos, mostrados en LEDs y displays.
%% kicker=Prácticas (20 % de la nota)

## Objetivo

Diseñar con esquemático y con VHDL los bloques combinacionales del [[t05|Tema 5]] y verlos funcionar en LEDs y displays.

@ej p2-s1|Sumador de 4 bits|Práctica 2|vhdl,arit|t5.ripple4
@enun
Describe un sumador de 4 bits con acarreo de entrada y salida. Muestra la suma en 4 LEDs y el acarreo en un quinto.
@end
@antes
Teoría: sumador completo y en cascada ([[t05|T5]]); aritmética con `unsigned` ([[t13|T13]]).
@end
@paso Qué se pide
Entradas `a`, `b` (4 bits) y `cin`; salidas `s` (4 bits) y `cout`.
@end
@paso Idea
Para no perder el acarreo, se hace la suma en **5 bits**: se amplían `a` y `b` con un `'0'` por la izquierda. El bit más significativo es `cout`.
@end
@paso Código
Ver abajo.
@end
@res
$s=(a+b+cin)\bmod16$ y $cout=\lfloor(a+b+cin)/16\rfloor$. Comprobado con las 512 combinaciones del modelo.
@end
@end

@codefile vhdl|p2_sum4.vhd|vhdl/p2_sum4.vhd|sum4

@ej p2-s2|Comparador y multiplexor|Práctica 2|vhdl,comb|t5.comp1,t5.mux_ok
@enun
Diseña un comparador de 4 bits con salidas $A>B$, $A=B$, $A<B$ y un multiplexor 4:1.
@end
@antes
Teoría: comparador y multiplexor ([[t05|T5]]); `when ... else` y `with ... select` ([[t13|T13]]).
@end
@paso Comparador
Con `unsigned` el comparador es una línea por salida. **Exactamente una** de las tres salidas vale 1: es una buena comprobación.
@end
@paso Multiplexor
Un `with sel select` enumera las cuatro posibilidades de `sel`; la última usa `others` para cubrir los valores no binarios de `std_logic`.
@end
@res
Comparador: una y solo una salida a 1. Mux: $y=d_{sel}$.
@end
@end

@codefile vhdl|p2_cmp4.vhd|vhdl/p2_cmp4.vhd|cmp4
@codefile vhdl|p2_mux4.vhd|vhdl/p2_mux4.vhd|mux4

@ej p2-s3|Display de 7 segmentos|Práctica 2|vhdl,msi|
@enun
Muestra en un display de 7 segmentos de la Basys una cifra BCD recibida por los interruptores.
@end
@antes
Teoría: decodificador BCD a 7 segmentos con indiferentes en $1010$–$1111$ ([[t05|T5]]); en la Basys los segmentos son **activos a nivel bajo**.
@end
@paso Tabla
Para cada cifra, qué segmentos (a a g) deben encenderse. En lógica positiva el 8 enciende los siete; en la Basys hay que **invertir**.
@end
@paso Código
Un `with d select` con las 10 cifras, y `"1111111"` (apagado) para el resto.
@end
@paso Activa un dígito
La Basys tiene 4 dígitos con ánodo común: para ver una cifra hay que **activar el ánodo** de ese dígito (a nivel bajo).
@end
@res
Con `d=0111` el display muestra un 7: segmentos a, b, c a 0 (encendidos), el resto a 1.
@end
@end

@codefile vhdl|p2_seg7.vhd|vhdl/p2_seg7.vhd|seg7

## Salida esperada

@codefile text|Resultado del modelo Python|salidas/p2.txt

## Qué escribir en la memoria

- La tabla de verdad del decodificador y las ecuaciones simplificadas (con indiferentes).
- Una comparación del esquemático y del VHDL: cuántos recursos usa cada uno.
- Capturas de la simulación del sumador con un caso con acarreo ($15+1$).
- Por qué en el display se usa lógica negativa.
