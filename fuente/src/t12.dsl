%% id=t12
%% group=tema
%% n=12
%% title=Tema 12 · Introducción a los dispositivos lógicos programables
%% short=T12 · Lógica programable (FPGA)
%% sub=Qué es una FPGA, cómo está hecha por dentro (LUT, biestables, interconexión) y cómo se programa.

@box idea | Desde cero
Un circuito digital normal tiene su función **fija** al fabricarlo. Un **dispositivo lógico programable** se fabrica «en blanco» y tú decides **después** qué circuito es, cargándole un fichero de configuración. Una **FPGA** (*field-programmable gate array*) es el más flexible: contiene miles de bloques lógicos pequeños y una red de cables que se puede reconectar. Es como una caja de piezas de electrónica digital que se recoloca con un fichero.
@end

## Qué hay dentro de una FPGA

- **CLB / slice** (bloque lógico configurable): la unidad básica. Contiene **tablas de consulta** (LUT) y **biestables**.
- **LUT de 4 entradas:** una memoria de $2^4=16$ bits. Almacena la tabla de verdad de **cualquier** función de 4 variables ($2^{16}=65\,536$ funciones posibles).
- **Interconexión programable:** cables y conmutadores que unen los bloques.
- **Bloques de E/S:** adaptan los pines a distintos niveles de tensión.
- **Bloques extra:** RAM en bloque, multiplicadores, gestores de reloj.

@fig fpga {"cap": "Estructura de una FPGA: una malla de bloques lógicos unida por conexiones programables."}

@fig lut {"cap": "Un bloque lógico: una LUT de 4 entradas seguida, opcionalmente, de un biestable."}

@sim lut

Una función de **más de 4 variables** se reparte entre varias LUT conectadas.

## ¿Por qué FPGA y no un microcontrolador?

| | Microcontrolador | FPGA |
|---|---|---|
| Ejecuta | Instrucciones, una tras otra | Hardware real, **todo en paralelo** |
| Velocidad por tarea | Limitada por el programa | Muy alta (cada módulo es un circuito) |
| Cambiar la función | Cambiar el programa | Reconfigurar el hardware |
| Facilidad | Alta | Más trabajo de diseño |

## Flujo de trabajo en el laboratorio

1. Describes el diseño (esquemático, diagrama de estados o VHDL).
2. **Simulas** para comprobar la función.
3. **Sintetizas** y **implementas** (colocar y conectar).
4. Asignas **pines** (fichero de restricciones) a interruptores, LEDs, displays y reloj.
5. Generas el fichero de configuración y **programas la placa**.

La placa **Basys** tiene una FPGA de Xilinx, interruptores, pulsadores, LEDs, displays de 7 segmentos y un reloj de **50 MHz**.

@ej t12-e1|Un reloj lento a partir de los 50 MHz de la placa|Ejemplo T12|cont|t12.div,t12.refresco,t12.disp
@enun
La placa da un reloj de 50 MHz. (a) ¿Hasta cuánto debe contar un divisor para generar 1 Hz y cuántos bits necesita? (b) Para refrescar un display de 4 dígitos con un contador de 18 bits cuyos 2 bits altos eligen el dígito, ¿a qué frecuencia cambia el dígito y a qué frecuencia se refresca cada uno?
@end
@antes
Teoría: divisor de frecuencia $f_{out}=f_{in}/DIV$; la salida conmuta cada $DIV/2$ ciclos; bits $=\lceil\log_2(\text{cuenta})\rceil$.
@end
@paso (a) Divisor a 1 Hz
$DIV=50\cdot10^6/1=50\,000\,000$. La salida debe conmutar cada medio periodo: $DIV/2=25\,000\,000$ ciclos. El contador cuenta de $0$ a $24\,999\,999$. Como $2^{24}=16{,}8\cdot10^6<25\cdot10^6\le2^{25}$, hacen falta **25 bits**.
@end
@paso (b) Cambio de dígito
Los dos bits altos de un contador de 18 bits cambian cada $2^{16}$ ciclos: $50\cdot10^6/2^{16}=762{,}9$ Hz.
@end
@paso (b) Refresco de cada dígito
Hay 4 dígitos por barrido: $762{,}9/4=190{,}7$ Hz por dígito. Por encima de unos 60 Hz el ojo no ve parpadeo.
@end
@res
(a) Cuenta hasta $24\,999\,999$ con 25 bits. (b) Cambio de dígito a $762{,}9$ Hz; refresco de cada dígito a $190{,}7$ Hz.
@end
@end

@box mas | Más a fondo: CPLD frente a FPGA y memoria de configuración
Las **CPLD** guardan su configuración en memoria no volátil (el circuito está listo al encender) y tienen retardos predecibles. Las **FPGA** de Xilinx usan **SRAM**: pierden la configuración al apagar y la cargan de una memoria externa (o del PC) al encender. Por eso al reiniciar la placa hay que volver a programarla si no usas memoria flash.
@end

@box falla | Qué suele fallar
- Olvidar asignar los **pines**: el diseño compila pero no hace nada en la placa.
- Suponer que la placa tiene los displays «activos a 1»: en la Basys se encienden con 0.
- Usar un reloj dividido como si fuera un reloj de la FPGA: es mejor usar **un solo reloj** y una señal de habilitación.
- Pensar que una FPGA «ejecuta» el código VHDL. El código **describe hardware** que existe a la vez.
@end

@card ¿Qué almacena una LUT de 4 entradas? || 16 bits: la tabla de verdad de una función de 4 variables.
@card ¿Qué ventaja tiene la FPGA sobre un microcontrolador? || Paralelismo real: cada bloque es hardware que funciona a la vez.
@card ¿Qué reloj trae la placa Basys? || 50 MHz.
@card ¿Qué pasa con una FPGA SRAM al apagarse? || Pierde la configuración y hay que volver a cargarla.
@gloss FPGA | Dispositivo lógico reprogramable formado por bloques lógicos y una red de interconexión.
@gloss LUT | Tabla de consulta: memoria que almacena la tabla de verdad de una función de pocas variables.
@gloss CLB | Bloque lógico configurable de una FPGA (LUT y biestables).
@gloss Restricciones (UCF) | Fichero que asocia las señales del diseño con los pines físicos de la FPGA.
@gloss Síntesis | Conversión de la descripción en puertas y biestables.

@q t12
Una LUT de 5 entradas almacena:
+ 32 bits
- 5 bits
- 16 bits
- 25 bits
> $2^5=32$ posiciones de un bit.
@end
@q t12
¿Qué hace falta para que un diseño aparezca en los LEDs de la placa?
+ Asignar las señales a los pines de la FPGA
- Solo simularlo
- Cambiar el reloj de la placa
- Nada más que sintetizarlo
> Sin las restricciones de pines, la herramienta coloca las señales donde quiere.
@end
