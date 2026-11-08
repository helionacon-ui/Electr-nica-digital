%% id=plan
%% group=ref
%% n=3
%% title=Plan de estudio
%% short=Plan de estudio
%% sub=Un plan de 4 semanas y uno de 7 días, con qué hacer cada sesión y cómo saber si vas bien.

Ningún plan sustituye a hacer problemas con lápiz. La regla de oro: **cada hora de teoría va seguida de media hora de ejercicios** de ese tema.

@box idea | Antes de empezar
No hay fechas aquí a propósito: usa la de tu convocatoria. Cuenta hacia atrás desde ella y reparte las semanas. Marca lo hecho en la lista de progreso de [[examen|El examen y cómo estudiar]].
@end

## Plan de 4 semanas (1–2 horas al día)

| Semana | Temas y bloques | Qué haces | Cómo sabes que vas bien |
|---|---|---|---|
| **1 · Base** | [[t02|T2]] numeración y [[t03|T3]] Boole y Karnaugh | Teoría + tests de [[autoeval]] + hoja de Karnaugh K1–K5 | Haces un mapa de 4 variables con indiferentes sin dudar |
| **2 · Combinacional** | [[t04|T4]] familias y [[t05|T5]] bloques | Sumador, comparador, MUX y displays; hoja K6–K17; primer examen resuelto ([[examenes]]) | Diseñas el recinto o la media de cuatro números sin mirar |
| **3 · Secuencial** | [[t06|T6]]–[[t09|T9]] biestables, memorias, contadores y registros | Tablas de excitación; contadores con JK; simulacro 1 | Tienes la tabla de excitación del JK de memoria |
| **4 · Autómatas y VHDL** | [[t10|T10]], [[t11|T11]], [[t12|T12]], [[t13|T13]] y las prácticas | Hoja de autómatas; detectores con solapamiento; revisar VHDL; simulacro 2 | Un detector de secuencia te sale en 15 minutos |

## Plan exprés de 7 días

| Día | Qué haces |
|---|---|
| 1 | [[t02|T2]] y [[t03|T3]]: numeración, C2, BCD, Boole y Karnaugh. 10 mapas. |
| 2 | [[t05|T5]]: sumador, comparador, MUX, decodificador y display. Examen de diciembre completo ([[examenes]]). |
| 3 | [[t06|T6]] y [[t08|T8]]: biestables y contadores; tabla de excitación JK. Hoja de autómatas A1, A2. |
| 4 | [[t10|T10]]: autómatas. Detectores A3, A5 y A7; sumador serie A9. |
| 5 | [[t07|T7]], [[t09|T9]], [[t12|T12]] y [[t13|T13]]: memorias, registros, FPGA y VHDL. Repasa las prácticas ([[p1|Práctica 1]] a [[p567|Prácticas 5–7]]). |
| 6 | **Simulacro 1** en 2 horas ([[simulacros]]) y corrección. Repite los fallos. |
| 7 | **Simulacro 2**, formulario de una página y glosario. Descansa pronto. |

## Cómo repartir el tiempo según los exámenes

El recuento de problemas por tipo está en [[examen|El examen y cómo estudiar]]. Con solo tres exámenes no es una regla, pero orienta: **bloques MSI**, **aritmética y códigos** y **autómatas** aparecen en los tres; los contadores con biestables, en uno. Dedica la mitad del tiempo a esos tres grupos.

## El día del examen

- Lee **todos** los enunciados y empieza por el que más seguro estés.
- En cada problema, **dibuja lo que te piden** (esquema, diagrama de estados, tabla) y explica en una frase por qué.
- Un cronograma sin explicación no cuenta: escribe qué ocurre en cada flanco.
- Guarda **10 minutos** para revisar: ¿cabe el resultado en los bits que has elegido? ¿Has cubierto el solapamiento? ¿Has puesto reset?
