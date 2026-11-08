%% id=empieza
%% group=intro
%% n=0
%% title=Empieza aquí
%% short=Empieza aquí (desde cero)
%% sub=Qué es la asignatura, lo que necesitas saber antes de empezar y cómo usar esta guía.
%% kicker=Portada

## Qué vas a aprender

Electrónica Digital es una asignatura obligatoria de **3.º de Ingeniería Biomédica** (4,5 ECTS, primer cuatrimestre). Aprendes a **diseñar circuitos que trabajan con unos y ceros**: desde una puerta que decide si se abre un toldo hasta una máquina que reconoce la combinación de una caja fuerte.

Todo lo que se construye en electrónica digital se reduce a dos tipos de circuitos:

- **Combinacionales**: la salida depende *solo* de las entradas de ahora. No tienen memoria. Ejemplo: un sumador.
- **Secuenciales**: la salida depende de las entradas de ahora *y de lo que pasó antes*. Tienen memoria. Ejemplo: un contador.

@fig bloques_comb_sec {"cap":"Todo circuito digital es una de estas dos cosas, o una mezcla: lógica combinacional sola, o lógica combinacional más memoria (biestables) realimentada."}

El temario oficial se reparte en cuatro unidades:

| Unidad | Temas | Qué trabajas |
|---|---|---|
| UD1 · Introducción | 0 a 3 | Numeración, códigos, álgebra de Boole |
| UD2 · Combinacional | 4 y 5 | Familias lógicas, sumadores, multiplexores, decodificadores, comparadores |
| UD3 · Secuencial | 6 a 11 | Biestables, memorias, contadores, registros, autómatas |
| UD4 · Lógica programable | 12 y 13 | FPGA y lenguaje VHDL |

La evaluación se reparte en **80 % examen escrito** y **20 % prácticas**, y hay que sacar **al menos un 4,0 en cada parte** para aprobar. Todos los detalles están en [[examen|El examen y cómo estudiar]].

## Repaso desde cero

No hace falta saber electrónica. Hace falta tener claras cinco ideas.

### 1. Un bit es un interruptor

Un **bit** vale 0 o 1. En un circuito real, 0 y 1 son dos rangos de tensión (por ejemplo, cerca de 0 V y cerca de 5 V). Con $n$ bits puedes escribir $2^n$ combinaciones distintas.

$$N = 2^n \qquad\Longleftrightarrow\qquad n = \lceil \log_2 N \rceil$$

Con 3 bits hay 8 combinaciones; con 4 bits, 16. Si necesitas distinguir 10 cosas (los dígitos del 0 al 9), hacen falta 4 bits, porque con 3 solo llegas a 8.

### 2. Contar en binario es contar con dos dedos

En decimal cada posición vale 10 veces la anterior. En binario, 2 veces.

$$1011_2 = 1\cdot 2^3 + 0\cdot 2^2 + 1\cdot 2^1 + 1\cdot 2^0 = 8+0+2+1 = 11_{10}$$

### 3. Las tres puertas básicas

- **AND** ($A\cdot B$): vale 1 solo si *todas* las entradas valen 1.
- **OR** ($A+B$): vale 1 si *alguna* entrada vale 1.
- **NOT** ($\overline{A}$): invierte.

@fig gates {"cap":"Las siete puertas que vas a usar. El círculo pequeño a la salida significa «negado»."}

### 4. Tabla de verdad

Una tabla de verdad es la lista de **todas** las combinaciones de entradas con la salida que quieres para cada una. Es el punto de partida de casi cualquier diseño combinacional: si no sabes qué circuito hacer, escribe la tabla.

### 5. El reloj

En los circuitos secuenciales hay una señal de **reloj** que sube y baja siempre igual. Los biestables solo miran sus entradas en un instante: el **flanco** (el momento en que el reloj sube, o baja). Entre flancos, lo que pasa en las entradas no cambia la memoria.

## Cómo usar esta guía

1. **Empieza por la teoría de cada tema.** Está escrita con la intuición primero y las fórmulas después. Cada tema acaba con un recuadro de *Qué suele fallar* y otro de *Fórmulas clave*.
2. **Juega con los simuladores.** Si no entiendes algo, muévelo: cambia un bit, una secuencia, una tensión. Verás el resultado al momento.
3. **Haz los ejercicios sin mirar.** Cada ejercicio tiene el enunciado, un recuadro *Antes de empezar* y la resolución en pasos plegados. Abre un paso solo cuando estés atascado.
4. **Practica con exámenes reales.** En [[examenes|Exámenes resueltos]] tienes los que han salido, con búsqueda por tema.
5. **Cierra el círculo** con la [[autoeval|autoevaluación]], los [[simulacros|simulacros]] y el [[plan|plan de estudio]].

@box ojo | Cómo se ha comprobado todo
Cada resultado numérico, cada ecuación minimizada y cada secuencia de estados de esta guía se ha **comprobado con un programa** que simula el circuito entrada por entrada. Los ejercicios con la etiqueta «✔ verificado» pasan esa comprobación. Cuando una solución de referencia tenía un fallo, no se ha copiado: hay una nota **Ojo** que dice dónde está y por qué.
@end

@box def | Notación que usa la guía
- Decimales con coma en el texto ($0{,}5$) y con punto en el código (`0.5`).
- $\overline{A}$ es «A negada». $A\cdot B$ se escribe a veces $AB$. $\oplus$ es la XOR.
- $Q_n$ es el estado actual y $Q_{n+1}$ el estado siguiente.
- Los números en base 2 llevan subíndice ($1011_2$); sin subíndice, son decimales.
@end
