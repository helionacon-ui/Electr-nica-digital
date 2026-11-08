%% id=t11
%% group=tema
%% n=11
%% title=Tema 11 · Descripciones funcionales y estructurales
%% short=T11 · Descripciones
%% sub=Distintas formas de describir un mismo circuito: ecuaciones, tablas, diagramas, bloques y código.

@box idea | Desde cero
Un mismo circuito se puede **describir** de muchas formas. Una **descripción estructural** dice **de qué piezas** está hecho y cómo se conectan (un esquemático). Una **descripción funcional** dice **qué hace** sin decir cómo (una tabla, unas ecuaciones, un diagrama de estados, un programa). Saber pasar de una a otra es lo que permite usar herramientas de diseño: tú describes el comportamiento y la herramienta fabrica la estructura.
@end

## Las formas de describir

| Descripción | Tipo | Cuándo usarla |
|---|---|---|
| Tabla de verdad | Funcional | Pocas entradas |
| Ecuaciones booleanas | Funcional | Lógica combinacional pequeña |
| Diagrama de estados / tabla de transiciones | Funcional | Autómatas |
| Esquemático de puertas | Estructural | Ver el circuito, depurar |
| Diagrama de bloques | Estructural (alto nivel) | Sistemas grandes |
| Lenguaje HDL (VHDL) | Ambas | Todo; es lo que usa el laboratorio |

## Niveles de abstracción

De más bajo a más alto: **transistor → puerta → bloque MSI (sumador, contador…) → sistema**. El diseño **jerárquico** usa piezas ya hechas y probadas. Primero se diseña y simula cada bloque; luego se unen. Es la forma de abordar el proyecto integrador.

@fig flujo {"cap":"Flujo de diseño. Si falla un paso, se vuelve a la descripción."}

## Del comportamiento a la estructura

El flujo de diseño con herramientas EDA:

1. **Descripción** (esquemático, diagrama de estados o VHDL).
2. **Simulación funcional:** comprueba que *hace lo que debe*, sin retardos.
3. **Síntesis:** la herramienta convierte la descripción en puertas y biestables.
4. **Implementación:** coloca y conecta los recursos de la FPGA.
5. **Simulación temporal y prueba en placa.**

@box falla | Qué suele fallar
- Confundir «estructural» con «funcional»: estructural = piezas y cables; funcional = comportamiento.
- Saltarse la simulación funcional y depurar directamente en la placa.
- Describir en un bloque todo el sistema en lugar de diseñar por partes.
@end

@card ¿Qué es una descripción estructural? || Dice de qué componentes consta el circuito y cómo se conectan.
@card ¿Qué es una descripción funcional? || Dice qué hace el circuito sin indicar su estructura interna.
@card ¿Qué hace la síntesis? || Convierte la descripción en puertas y biestables.
@gloss EDA | Herramientas de diseño electrónico asistido por ordenador.
@gloss Síntesis | Transformación de una descripción de alto nivel en una red de puertas y biestables.
@gloss Descripción estructural | Descripción por componentes e interconexiones.
@gloss Descripción funcional | Descripción por comportamiento.

@q t11
Un archivo VHDL que describe un sumador con la expresión `s <= a + b;` es una descripción:
+ Funcional (de comportamiento)
- Estructural
- De transistores
- Física
> Dice qué calcula, no con qué puertas.
@end
@q t11
¿Qué paso del flujo de diseño comprueba que el circuito hace lo que debe, sin tener en cuenta los retardos?
+ La simulación funcional
- La síntesis
- La implementación
- La programación de la placa
> La simulación funcional ignora los retardos reales; la temporal los incluye.
@end
