%% id=t03
%% group=tema
%% n=3
%% title=Tema 3 · Álgebra de Boole y funciones lógicas
%% short=T3 · Álgebra de Boole
%% sub=Puertas, tablas de verdad, formas canónicas y simplificación con mapas de Karnaugh.

@box idea | Desde cero
Una **función lógica** es una regla que dice, para cada combinación de entradas (0/1), si la salida es 0 o 1. Se puede escribir de tres formas equivalentes: **tabla de verdad**, **ecuación** y **circuito de puertas**. El álgebra de Boole es el conjunto de reglas para pasar de una a otra y, sobre todo, para **simplificar**: menos puertas es menos coste, menos consumo y menos retardo.
@end

## Las operaciones básicas

| Operación | Símbolo | Se lee | Vale 1 cuando |
|---|---|---|---|
| NOT | $\overline{A}$ | no A | $A=0$ |
| AND | $A\cdot B$ | A y B | las dos entradas valen 1 |
| OR | $A+B$ | A o B | al menos una vale 1 |
| XOR | $A\oplus B$ | A o exclusivo B | las entradas **son distintas** |
| NAND | $\overline{A\cdot B}$ | | no las dos a 1 |
| NOR | $\overline{A+B}$ | | las dos a 0 |

@fig gates {"cap":"Símbolos de las puertas básicas. El círculo a la salida significa «negado»."}

**Las puertas NAND y NOR son universales:** con solo una de ellas puedes construir cualquier circuito. Se ha comprobado por código que con NAND se obtienen NOT, AND y OR.

## Reglas que debes saber de memoria

| Regla | Forma 1 | Forma 2 |
|---|---|---|
| Identidad | $A+0=A$ | $A\cdot1=A$ |
| Nulo | $A+1=1$ | $A\cdot0=0$ |
| Idempotencia | $A+A=A$ | $A\cdot A=A$ |
| Complemento | $A+\overline{A}=1$ | $A\cdot\overline{A}=0$ |
| Absorción | $A+AB=A$ | $A(A+B)=A$ |
| Adyacencia | $AB+A\overline{B}=A$ | $(A+B)(A+\overline{B})=A$ |
| Consenso | $AB+\overline{A}C+BC=AB+\overline{A}C$ | |
| **De Morgan** | $\overline{A+B}=\overline{A}\cdot\overline{B}$ | $\overline{A\cdot B}=\overline{A}+\overline{B}$ |

Todas estas identidades se han comprobado por código con las tablas de verdad completas.

@box idea | De Morgan en una frase
Para negar una expresión: **cambia cada AND por OR (y al revés) y niega cada variable**. Por eso una puerta NAND es lo mismo que una OR con las entradas negadas.
@end

## Formas canónicas

Un **minitérmino** es un AND que contiene todas las variables (cada una negada o no) y vale 1 en **una sola** fila de la tabla. Un **maxitérmino** es un OR con todas las variables que vale 0 en una sola fila.

- **Suma de minitérminos** ($\Sigma m$): suma (OR) de los minitérminos de las filas donde $f=1$.
- **Producto de maxitérminos** ($\Pi M$): producto (AND) de los maxitérminos de las filas donde $f=0$.

Ejemplo: $f(A,B,C)=\Sigma m(1,3,5,6,7)$ significa que $f=1$ en las filas $001,011,101,110,111$.

## Simplificar con mapas de Karnaugh

Un **mapa de Karnaugh** es la tabla de verdad colocada en una rejilla donde las casillas vecinas difieren en **un solo bit** (por eso las columnas van en orden Gray: 00, 01, 11, 10). Dos casillas vecinas con un 1 se pueden juntar y desaparece la variable que cambia.

**Reglas para agrupar:**

1. Grupos de 1, 2, 4, 8… casillas (potencias de 2), rectangulares.
2. Cuanto **más grandes**, mejor: eliminan más variables.
3. El mapa es **cíclico**: el borde izquierdo es vecino del derecho, y el de arriba del de abajo.
4. Cubre todos los 1 con el mínimo número de grupos. Un 1 puede estar en varios grupos.
5. Las casillas **indiferentes** (X, *don't care*) se usan solo si ayudan a hacer el grupo mayor.

@fig kmap {"n":3,"on":[1,3,5,6,7],"dc":[],"names":["A","B","C"],"title":"f = Σm(1,3,5,6,7)","cap":"Dos grupos de cuatro y de dos casillas cubren los cinco unos."}

@ej t3-e1|Simplificar $f=\Sigma m(1,3,5,6,7)$|Ejemplo T3|comb|t3.ej1
@enun
Simplifica $f(A,B,C)=\Sigma m(1,3,5,6,7)$ como suma de productos y como producto de sumas.
@end
@antes
Teoría: mapa de Karnaugh de 3 variables, agrupación en potencias de 2, y la dualidad: para el producto de sumas se agrupan los **ceros** y se niega el resultado.
@end
@paso Rellena el mapa
Pon un 1 en las casillas $1,3,5,6,7$. Los ceros están en $0,2,4$.
@end
@paso Agrupa los unos
Grupo de 4: $m_1,m_3,m_5,m_7$ (la columna $C=1$): queda solo $C$. El 1 que falta, $m_6=110$, se agrupa con $m_7$: queda $AB$.
@end
@paso Escribe la suma de productos
$f=C+AB$.
@end
@paso Producto de sumas
Ahora agrupa los **ceros** ($m_0,m_2,m_4$). $m_0$ y $m_2$ (la fila $A=0$, $C=0$) dan $\overline{A}\,\overline{C}$. $m_0$ y $m_4$ ($B=0$, $C=0$) dan $\overline{B}\,\overline{C}$. Así $\overline{f}=\overline{A}\,\overline{C}+\overline{B}\,\overline{C}$.
@end
@paso Niega con De Morgan
$f=\overline{\overline{A}\,\overline{C}+\overline{B}\,\overline{C}}=(A+C)(B+C)$. Es la misma función: $(A+C)(B+C)=AB+C$.
@end
@res
$f=C+AB=(A+C)(B+C)$.
@end
@end

@sim kmap

@box mas | Más a fondo: método de Quine–McCluskey
Cuando hay más de 4 variables el mapa se vuelve incómodo. El algoritmo de **Quine–McCluskey** hace lo mismo con tablas: (1) agrupa minitérminos que difieren en un bit para obtener los **implicantes primos**; (2) elige un conjunto mínimo que cubra todos los minitérminos, empezando por los **implicantes primos esenciales** (los únicos que cubren algún minitérmino). Todas las simplificaciones de esta guía se han obtenido con una implementación propia de este método y se han comprobado contra la tabla de verdad.
@end

@box falla | Qué suele fallar
- Hacer grupos de 3, 5 o 6 casillas. Solo valen 1, 2, 4, 8, 16.
- Olvidar que el mapa es cíclico y no ver el grupo de las esquinas.
- Usar una casilla X como si fuera un 1 obligatorio: las X solo ayudan, nunca hay que cubrirlas.
- Dejar un grupo redundante (todos sus unos ya están cubiertos por otros).
- Negar mal con De Morgan: hay que cambiar la operación **y** negar las variables.
@end

@box formula | Fórmulas clave
- $\overline{A+B}=\overline{A}\,\overline{B}$ y $\overline{AB}=\overline{A}+\overline{B}$.
- $A+AB=A$; $AB+A\overline{B}=A$; $AB+\overline{A}C+BC=AB+\overline{A}C$.
- $A\oplus B=A\overline{B}+\overline{A}B$.
- $n$ variables: $2^n$ filas y $2^{2^n}$ funciones distintas (con 4 variables, 65536).
@end

@card ¿Enuncia De Morgan? || $\overline{A+B}=\overline{A}\,\overline{B}$ y $\overline{AB}=\overline{A}+\overline{B}$.
@card ¿Cuántas funciones lógicas distintas hay de $n$ variables? || $2^{2^n}$.
@card ¿Qué son puertas universales? || NAND y NOR: con una sola se construye cualquier función.
@card ¿Por qué las columnas de Karnaugh van en orden 00,01,11,10? || Para que las casillas vecinas difieran en un solo bit (código Gray).
@card ¿Cómo se usan las casillas indiferentes? || Solo si permiten hacer un grupo mayor; no hay que cubrirlas.
@gloss Minitérmino | AND con todas las variables que vale 1 en una sola fila de la tabla.
@gloss Maxitérmino | OR con todas las variables que vale 0 en una sola fila de la tabla.
@gloss Implicante primo | Grupo de unos que no se puede ampliar más en el mapa de Karnaugh.
@gloss Indiferente (X) | Combinación de entradas que no ocurre o cuya salida da igual.
@gloss Puerta universal | Puerta con la que se puede construir cualquier función lógica (NAND o NOR).

@q t3
Según De Morgan, $\overline{A\cdot B+C}$ es igual a:
+ $(\overline{A}+\overline{B})\,\overline{C}$
- $\overline{A}\,\overline{B}+\overline{C}$
- $(\overline{A}+\overline{B})+\overline{C}$
- $\overline{A}+\overline{B}+C$
> Se cambia + por · y se niega cada término: $\overline{AB}\cdot\overline{C}=(\overline{A}+\overline{B})\overline{C}$.
@end
@q t3
En un mapa de Karnaugh, ¿cuántas casillas puede tener un grupo válido?
+ 1, 2, 4, 8…
- Cualquier número
- Solo números pares
- Hasta un máximo de 4
> Los grupos son potencias de 2.
@end
@q t3
¿Cuál es la forma simplificada de $AB+A\overline{B}+\overline{A}B$?
+ $A+B$
- $AB$
- $A\oplus B$
- $\overline{A}+\overline{B}$
> $AB+A\overline{B}=A$, y queda $A+\overline{A}B=A+B$.
@end
