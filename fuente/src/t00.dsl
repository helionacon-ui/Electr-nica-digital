%% id=t00
%% group=tema
%% n=0
%% title=Tema 0 · Introducción a la asignatura
%% short=T0 · Introducción
%% sub=Qué se pide, con qué herramientas y cómo encaja cada tema.

## El mapa en una página

La asignatura recorre este camino. Cada paso usa lo del anterior.

@fig mapa {"cap":"De los números al diseño con FPGA. Los temas de la izquierda son la base; los de la derecha son lo que se ve en el laboratorio."}

Cuatro resultados de aprendizaje te dicen qué se espera de ti:

- **Explicar** cómo funcionan los sistemas digitales.
- **Analizar y sintetizar** circuitos digitales. *Analizar* es entender uno que ya existe. *Sintetizar* es diseñar uno a partir de una descripción.
- **Usar** instrumentación básica y software de simulación.
- **Programar** una FPGA con esquemáticos y con VHDL.

## Dos verbos que lo resumen todo

@box idea | Analizar frente a sintetizar
- **Analizar**: te dan el circuito y te piden la función, la tabla o el cronograma. Camino: circuito $\rightarrow$ ecuaciones $\rightarrow$ tabla $\rightarrow$ comportamiento.
- **Sintetizar**: te dan una descripción en palabras y te piden el circuito. Camino: palabras $\rightarrow$ tabla o diagrama de estados $\rightarrow$ ecuaciones $\rightarrow$ circuito.
Son el mismo camino recorrido en sentidos opuestos. Si dominas uno, el otro es el mismo mapa al revés.
@end

## Herramientas del laboratorio

Se trabaja con placas de desarrollo **Basys** con una **FPGA de Xilinx** y el entorno **Xilinx ISE**. Una FPGA es un chip que puedes «reconfigurar» para que se comporte como el circuito digital que has diseñado. Se describe el circuito de tres maneras equivalentes:

1. **Esquemático**: dibujas las puertas y los bloques.
2. **Diagrama de estados**: dibujas los estados y las transiciones.
3. **VHDL**: lo escribes como texto.

El proyecto final es un sistema de monitorización de una **incubadora neonatal** usada como entorno de simulación. Lo verás en [[prac|Prácticas]].

@box falla | Qué suele fallar
- Empezar a dibujar circuitos antes de escribir la **tabla de verdad o el diagrama de estados**. Todo diseño bueno empieza ahí.
- Confundir *analizar* con *sintetizar* y calcular al revés.
- No decir las suposiciones cuando el enunciado es ambiguo.
@end
