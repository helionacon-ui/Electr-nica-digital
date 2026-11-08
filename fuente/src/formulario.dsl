%% id=formulario
%% group=ref
%% n=1
%% title=Formulario por temas
%% short=Formulario
%% sub=Las fórmulas y reglas que hay que saber de memoria, tema a tema. Al final, la versión de una página para imprimir.

Esto es lo que debes **saber sin mirar**. Si una fórmula te suena a chino, vuelve a la teoría del tema: aprender una fórmula sin saber de dónde sale falla en el examen.

@auto formulas

### T5 · Bloques combinacionales (tabla de decisión)

| Quiero… | Uso… |
|---|---|
| Sumar dos números de $n$ bits | $n$ sumadores completos en cascada (acarreo de uno al siguiente) |
| Restar $A-B$ | Sumador con $B$ invertida y $C_{in}=1$ |
| Comparar | Comparador: salidas $A>B$, $A=B$, $A<B$ |
| Elegir una entre $2^k$ | Multiplexor con $k$ bits de selección |
| Activar una salida según un código | Decodificador $n$ a $2^n$ |
| Mostrar un dígito | Decodificador BCD a 7 segmentos |
| Dividir/multiplicar por $2^k$ | Desplazar $k$ posiciones (sin puertas) |

### T11 y T12 · Descripciones y lógica programable

- Un mismo circuito se describe con **ecuaciones**, **tabla de verdad**, **diagrama de estados**, **bloques** o **código** (VHDL). Los distintos niveles de abstracción son comportamiento, flujo de datos y estructura.
- LUT de $k$ entradas: memoria de $2^k$ bits; implementa cualquier función de $k$ variables.
- Una función de más de $k$ variables se reparte entre varias LUT.

La versión de **una sola página**, para imprimir, está justo debajo y en el PDF `formulario.pdf`. Comprueba en las normas de tu convocatoria si puedes llevar un formulario al examen.
