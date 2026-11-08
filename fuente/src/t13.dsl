%% id=t13
%% group=tema
%% n=13
%% title=Tema 13 · Introducción al diseño digital con VHDL
%% short=T13 · VHDL
%% sub=Entidad y arquitectura, descripciones de flujo, de comportamiento y estructurales, procesos y máquinas de estados.

@box idea | Desde cero
**VHDL** es un lenguaje para **describir hardware**, no para programar un procesador. Cuando escribes `y <= a and b;` no le dices «calcula» a un ordenador: describes que **existe una puerta AND** entre `a`, `b` e `y`. Dos líneas de VHDL a la vez son dos circuitos funcionando a la vez. Esta idea es la que más cuesta y la que más acaba cayendo en examen.
@end

## Las dos piezas de todo diseño

- **`entity`** (entidad): la **caja negra**. Dice el nombre y los puertos (entradas y salidas).
- **`architecture`** (arquitectura): lo que hay **dentro** de la caja.

@code vhdl|Plantilla mínima
library ieee;
use ieee.std_logic_1164.all;

entity puerta_and is
  port ( a, b : in  std_logic;
         y    : out std_logic );
end puerta_and;

architecture flujo of puerta_and is
begin
  y <= a and b;
end flujo;
@end

**Tipos que vas a usar:** `std_logic` (un bit, con valores `'0'`, `'1'`, `'Z'`, `'X'`…), `std_logic_vector(3 downto 0)` (un bus de 4 bits), `unsigned`/`signed` (para aritmética, en `ieee.numeric_std`) e `integer`.

## Tres estilos de descripción

1. **Flujo de datos:** ecuaciones con asignaciones concurrentes (`<=`). Incluye `when ... else` y `with ... select`.
2. **Comportamiento:** dentro de un `process` con `if`, `case`… Se ejecuta en secuencia **en la simulación**, pero describe hardware.
3. **Estructural:** instancias de otros componentes conectadas con `port map`. Es el equivalente a un esquemático.

@codefile vhdl|Flujo de datos: multiplexor (p2_mux4.vhd)|vhdl/p2_mux4.vhd|mux4

## Combinacional y secuencial en VHDL

- **Combinacional:** proceso con **todas** las entradas en la lista de sensibilidad (o asignaciones concurrentes). Si olvidas asignar una salida en alguna rama del `if`, la herramienta infiere un **latch** (memoria no deseada). Regla de oro: **toda salida se asigna en todos los casos**.
- **Secuencial (síncrono):** proceso sensible al reloj con `rising_edge(clk)`. Lo que se asigna ahí se convierte en **biestables**.

@codefile vhdl|Secuencial: contador con reset y habilitación (p3_contador.vhd)|vhdl/p3_contador.vhd|cnt

### Señales y variables

- Una **señal** (`signal`) es un cable (o un biestable): la asignación `<=` toma efecto **al terminar el proceso**.
- Una **variable** (`variable`) solo existe dentro de un proceso y se asigna al instante con `:=`.

Si lees una señal que acabas de asignar en el mismo proceso, ves el **valor antiguo**. Es una de las trampas más típicas.

## Máquinas de estados en VHDL

La forma recomendada son **dos procesos**: uno secuencial que guarda el estado, otro combinacional con el `case` que calcula el siguiente estado y la salida. Es la traducción directa del diagrama de estados de [[t10|Tema 10]].

@codefile vhdl|Máquina de estados: detector 101 (p3_detector101.vhd)|vhdl/p3_detector101.vhd|det

@ej t13-e1|Leer código VHDL: ¿qué circuito es?|Ejemplo T13|vhdl|t13.cnt,t10.det101
@enun
Dado el contador `p3_contador` con $N=10$, ¿qué secuencia genera `q` si `rst` se activa en el sexto ciclo? ¿Cuántos biestables se sintetizan y qué hace `fin`?
@end
@antes
Teoría: proceso síncrono, reset asíncrono, módulo $N$, número de bits $=\lceil\log_2N\rceil$.
@end
@paso Cuenta normal
Con `en='1'` incrementa en cada flanco: $0,1,2,\dots,9$ y al llegar a $N-1=9$ vuelve a $0$.
@end
@paso Efecto del reset
`rst='1'` pone `cnt` a 0 **al instante** (es asíncrono), sin esperar al flanco. En el ejemplo la cuenta reinicia: $\dots,4,5,0,1,2\dots$
@end
@paso Recursos
`cnt` tiene 4 bits ($2^3<10\le2^4$): **4 biestables**, más la lógica de comparación con 9 y de incremento.
@end
@paso La salida `fin`
Es combinacional: `fin='1'` cuando `cnt=9`. Sirve para encadenar otro contador.
@end
@res
Secuencia $0,1,\dots,9,0,\dots$; 4 biestables; `fin` vale 1 solo en el estado 9.
@end
@end

@box mas | Más a fondo: genéricos y jerarquía
Un `generic` es un parámetro de la entidad (`N`, `DIV`…) que se fija al instanciar el componente. Permite reutilizar el mismo código para un contador de módulo 10 o 60. El **diseño jerárquico** crea módulos pequeños y probados (contador, divisor, display) y los une en un módulo superior con `port map`.
@end

@box falla | Qué suele fallar
- Pensar que el código se ejecuta «línea a línea» como en C: las asignaciones concurrentes funcionan **a la vez**.
- No asignar una salida en alguna rama: aparece un **latch** inesperado.
- Mezclar `std_logic_vector` con aritmética sin convertir a `unsigned`.
- Olvidar `rising_edge(clk)` y escribir procesos sensibles a todo.
- Leer una señal justo después de asignarla y esperar el valor nuevo.
- Usar un reloj generado por un divisor como si fuera reloj de la FPGA.
@end

@box formula | Fórmulas clave
- Divisor: $DIV=f_{in}/f_{out}$; conmuta cada $DIV/2$ ciclos.
- Bits de un contador: $\lceil\log_2N\rceil$.
- Una `case` completa en un proceso combinatorio: añade siempre `when others`.
@end

@card ¿Qué es una entity? || La interfaz del módulo: nombre y puertos.
@card ¿Qué es una architecture? || La descripción de lo que hay dentro del módulo.
@card ¿Qué infiere VHDL si no asignas una salida en todas las ramas? || Un latch.
@card ¿Cuándo toma efecto una asignación a una signal? || Al terminar el proceso (no al instante).
@card ¿Qué sentencia detecta un flanco de subida? || `rising_edge(clk)`.
@gloss VHDL | Lenguaje de descripción de hardware.
@gloss Entity | Parte del código VHDL que define las entradas y salidas de un módulo.
@gloss Architecture | Parte del código VHDL que define el funcionamiento interno.
@gloss Proceso | Bloque `process` de VHDL que describe comportamiento.
@gloss Latch inferido | Memoria no deseada que aparece cuando una señal no se asigna en todos los casos.

@q t13
En VHDL, `y <= a and b;` describe:
+ Una puerta AND siempre presente
- Una instrucción que se ejecuta una sola vez
- Una variable temporal
- Un proceso secuencial
> Es una asignación concurrente: hardware que existe de forma permanente.
@end
@q t13
¿Qué provoca un `if` sin `else` dentro de un proceso combinacional?
+ Un latch inferido
- Un contador
- Un error de sintaxis siempre
- Una puerta NOT
> La salida mantiene su valor en la rama no cubierta, y eso es memoria.
@end
@q t13
Un contador módulo 10 en VHDL necesita como mínimo una señal de:
+ 4 bits
- 3 bits
- 10 bits
- 5 bits
> $\lceil\log_2 10\rceil=4$.
@end
