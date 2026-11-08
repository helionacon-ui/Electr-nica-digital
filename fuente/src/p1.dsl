%% id=p1
%% group=prac
%% n=1
%% title=Práctica 1 · Introducción al diseño con herramientas CAD/EDA
%% short=P1 · Entorno ISE y Basys
%% sub=Crear un proyecto en Xilinx ISE, describir un circuito y probarlo en la placa Basys.
%% kicker=Prácticas (20 % de la nota)

@box idea | Cómo se evalúa
Las prácticas pesan el **20 %**. Se evalúan con memorias e informes y, y, según se decida en el curso, con pruebas prácticas. Hay que **defender** el trabajo: explicar cómo funciona cada diseño y por qué tomaste cada decisión. Es obligatorio asistir (mínimo 80 %) y sacar **al menos un 4,0** en teoría y en prácticas para aprobar. Si usas IA para generar código (permitido en la Práctica 4), tienes que **entenderlo, revisarlo y justificarlo**.
@end

## Simulador de las prácticas

Elige una función, cambia los valores y mira el código VHDL equivalente, la salida tipo consola y el cronograma. Los botones «Abrir en el simulador» de cada práctica cargan aquí el ejemplo correspondiente.

@sim prac

## Objetivo

Aprender el flujo completo con una función trivial: describir, simular, sintetizar, asignar pines y programar la placa.

## Pasos

@ej p1-s1|Crear el proyecto y describir el circuito|Práctica 1|vhdl|
@enun
Crea un proyecto en Xilinx Foundation/ISE para la FPGA de la placa Basys y describe un circuito que enlace interruptores con LEDs.
@end
@antes
Herramientas: entorno ISE, captura de esquemáticos, diagramas de estados y VHDL (los tres modos de entrada de diseño). Ya conoces `entity`/`architecture` del [[t13|Tema 13]].
@end
@paso Nuevo proyecto
En ISE: *File → New Project*. Elige el nombre, la familia de la FPGA y el dispositivo que indica la placa Basys (consulta el manual de tu placa). Indica lenguaje **VHDL** y simulador **ISim**.
@end
@paso Nueva fuente
*Project → New Source → VHDL Module*. Pega el código de abajo (o dibuja el esquemático equivalente con puertas AND, OR, XOR).
@end
@paso Comprueba la sintaxis
Haz doble clic en *Check Syntax*. Debe terminar sin errores.
@end
@res
Un módulo `p1_leds` con 8 interruptores, 4 pulsadores y 8 LEDs, listo para simular.
@end
@end

@codefile vhdl|p1_leds.vhd|vhdl/p1_leds.vhd|leds

@ej p1-s2|Simular, asignar pines y programar|Práctica 1|vhdl|
@enun
Simula el módulo, asigna las señales a los pines de la placa y programa la FPGA.
@end
@antes
Flujo: simulación funcional → síntesis → implementación → asignación de pines (UCF) → fichero de configuración → programación.
@end
@paso Simulación
Crea un *test bench* o usa el simulador de ISE: pon `sw=00000011`. Espera `led=00110011` (AND=1, OR=1, XOR=0).
@end
@paso Asignación de pines
Crea un fichero de restricciones (UCF) que una cada señal con su pin físico. Ejemplo (**comprueba los pines con el manual de tu placa**):
@end
@paso Síntesis, implementación y bitstream
*Synthesize → Implement Design → Generate Programming File*. Si hay avisos de «latch» o de señales sin pin, léelos.
@end
@paso Programar
Con la placa conectada, ejecuta iMPACT y carga el fichero `.bit`. Mueve los interruptores y comprueba los LEDs.
@end
@res
Los LEDs siguen los interruptores. Si no se enciende ninguno, lo primero que hay que mirar es la asignación de pines y que el fichero se haya cargado.
@end
@end

@codefile text|p1_basys.ucf|vhdl/p1_basys.ucf

## Salida esperada

@codefile text|Resultado del modelo Python (salida esperada en la placa)|salidas/p1.txt

## Qué escribir en la memoria

- Un esquema del circuito y su tabla de verdad.
- Una captura de la simulación con $sw=00000011$ y la explicación del valor de cada LED.
- Una frase sobre qué hace cada paso del flujo (síntesis, implementación, programación).
- Cuál fue el error más típico que cometiste (por ejemplo, pines mal asignados) y cómo lo resolviste.
