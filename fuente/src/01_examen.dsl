%% id=examen
%% group=intro
%% n=1
%% title=El examen y cómo estudiar
%% short=El examen y cómo estudiar
%% sub=Cómo se evalúa, qué cae más según los exámenes reales y una estrategia para sacar nota.

## Cómo se evalúa la asignatura

| Parte | Peso | Qué es |
|---|---|---|
| Exámenes escritos | **80 %** | Cuestiones conceptuales, análisis y síntesis de circuitos digitales, interpretación de diseños y resolución de casos prácticos. |
| Prácticas | **20 %** | Memorias e informes, y defensa del trabajo de laboratorio (individual o en grupo). |

Reglas que conviene tener presentes:

- Para aprobar hace falta **un 4,0 como mínimo tanto en la parte teórica como en la práctica**.
- La asistencia a las prácticas es obligatoria: hace falta al menos un **80 %** para que cuente como hecha.
- Si ya superaste una actividad en la evaluación continua y quieres presentarte a esa misma actividad en la evaluación final, **debes renunciar a la nota que tenías**.
- Las prácticas 4 a 7 permiten usar inteligencia artificial como ayuda, pero tienes que **entender, revisar y justificar** el código. En la defensa te preguntarán por él.
- También hay pruebas cortas en clase, individuales o por parejas (evaluación formativa).

@box ojo | Fechas y ponderaciones
Esta guía no inventa fechas ni notas. Mira en tu calendario académico cuándo es la convocatoria. Lo que sí sabes: el examen escrito vale el 80 % y debes sacar un 4,0 como mínimo.
@end

## Cómo son los exámenes de otros años

Los exámenes reales que han servido para preparar esta guía son de la **misma asignatura en la titulación de Ingeniería Electrónica Industrial y Automática** de la misma escuela. El contenido es esencialmente el mismo. La organización exacta del examen puede variar de un curso a otro, así que comprueba siempre la de tu convocatoria.

Lo que se repite en todos ellos:

| Dato | Lo que dicen los exámenes |
|---|---|
| Número de problemas | 4 |
| Valor de cada problema | 2,5 puntos (examen de febrero de 2023) |
| Tiempo | 2 horas (examen de diciembre de 2024) |
| Cómo se corrige | «Se tendrá en cuenta la simplicidad de la solución propuesta, así como la claridad de realización del mismo» (febrero de 2023 y febrero de 2025) |
| Cronogramas | «No se contabilizarán los ejercicios que sólo dibujen las formas de onda sin explicar nada» (diciembre de 2024) |
| Notas de aprobado (febrero de 2023) | Examen escrito ≥ 5 y prácticas ≥ 1 sobre 2; nota mínima de la asignatura 6 puntos. En tu titulación rige el 80 %/20 % de arriba. |

La última fila es una norma de *esa* convocatoria. Se incluye solo para que veas qué tipo de normas aparecen.

## Qué cae más

@auto stats

Mira la forma que tiene un examen típico. Casi siempre hay:

1. **Un problema de diseño combinacional con bloques estándar** (sumadores, comparadores, multiplexores, displays): «haz la media de…», «calcula $A\cdot B + C$ y muéstralo en displays», «un recinto con dos puertas».
2. **Un problema pequeño de lógica o de contadores**: simplificar una función con Karnaugh y pasarla a NAND, o analizar un circuito dado y dibujar su cronograma.
3. **Un problema de síntesis de un contador** con biestables JK y puertas, con una entrada de control (sube/baja).
4. **Un autómata**: la caja fuerte, la noria, la máquina expendedora… Diagrama de estados, tabla de transiciones, ecuaciones y circuito.

El problema 4 suele ser el más largo. Reserva tiempo.

## Estrategia para el examen

@box idea | Reparto de las 2 horas
- **5 min**: lee los cuatro enunciados completos y marca qué te sabes mejor.
- **25-30 min por problema**, empezando por el que tengas más claro.
- **10 min al final** para revisar: ¿cada problema tiene diagrama/tabla, ecuaciones y circuito?
Un problema empezado con buena idea y un esquema claro puntúa más que uno en blanco.
@end

Reglas prácticas que se repiten en las correcciones:

- **Escribe los pasos.** Un cronograma sin explicar cómo se obtuvo no puntúa. Una tabla de verdad sin la ecuación tampoco.
- **Define tus entradas, salidas y estados** antes de dibujar. Escribe qué significa cada estado con palabras.
- **Si el enunciado es ambiguo, di qué supones** y sigue. Es lo que se espera.
- **Simplifica**: la solución más sencilla puntúa mejor. Usa los indiferentes ($\times$) en Karnaugh.
- **Comprueba con un caso**: antes de entregar, mete una entrada concreta en tu circuito y mira que sale lo que debe.

## Tu seguimiento

Marca lo que vas haciendo. Se guarda en este navegador.

@auto checklist
