%% id=libro2
%% group=ejer
%% n=3.2
%% title=Libro de problemas · Capítulo 2 · Manipulación booleana
%% short=Libro · Cap. 2 Álgebra de Boole
%% sub=12 problemas resueltos: tablas de verdad, teoremas, minitérminos y maxitérminos, De Morgan, implementación con NAND y con NOR y análisis de circuitos.

@box idea | Cómo se usa esta sección
Son los problemas resueltos del capítulo 2 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. Cada igualdad y cada tabla se ha comprobado con un programa que recorre todas las combinaciones de entrada. Si el libro difiere, aparece una nota «Ojo». La teoría está en [[t03|el tema 3]].
@end

@ej lb2-1|Tablas de verdad de ocho funciones de tres variables|Libro · Cap. 2 · P2.1|comb|lb2.p21
@enun
Obtén la columna de salida de ocho funciones de $A,B,C$, desde el simple producto $ABC$ hasta expresiones con complementos anidados.
@end
@antes
**Método:** se sustituye cada combinación $ABC$ en la expresión y se opera de dentro hacia fuera. Recuerda que $0\cdot x=0$ y $1+x=1$: muchas filas salen a simple vista.
@end
@paso Las expresiones
- $f_1=ABC$
- $f_2=A+B+C$
- $f_3=A(B+\bar C)$
- $f_4=\overline{(A+B)(B+C)}$
- $f_5=\bar B\,(A+C\,\overline{(A+B)})$
- $f_6=\overline{(A+C)\cdot\overline{B(C+B)}}$
- $f_7=(A+B)(\bar A+\bar B)$
- $f_8=A+B\,(A+C\,B(A+B))$
@end
@paso Un ejemplo paso a paso: $f_6(001)$
Con $A=0,B=0,C=1$: $A+C=1$; $B(C+B)=0\cdot1=0$; su complemento es $1$; el producto es $1\cdot1=1$ y el complemento exterior da $0$. Así que $f_6(001)=0$.
@end
@paso Tabla de verdad
| ABC | f1 | f2 | f3 | f4 | f5 | f6 | f7 | f8 |
|---|---|---|---|---|---|---|---|---|
| 000 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 001 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| 010 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| 011 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| 100 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| 101 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| 110 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| 111 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
@end
@paso Formas más cortas
Mirando la tabla se reconocen formas simples. Todas se han comprobado por código:
- $f_3=A(B+\bar C)$ no se puede abreviar más.
- $f_4=\bar A\bar B+\bar B\bar C$
- $f_5=\bar B\,(A+C)$
- $f_6=B+\bar A\bar C$
- $f_7=A\oplus B$
- $f_8=A+BC$
@end
@res
Las ocho columnas coinciden con las del libro. Las expresiones largas ($f_5$, $f_6$, $f_8$) se reducen mucho: la absorción hace que partes enteras sobren.
@end
@end

@ej lb2-2|Demostrar los teoremas básicos por inducción perfecta|Libro · Cap. 2 · P2.2|comb|lb2.p22
@enun
Demuestra con tablas de verdad (inducción perfecta) los teoremas de una, dos y tres variables: neutros, complementos, idempotencia, elementos nulos, absorción, De Morgan y distributivas.
@end
@antes
**Inducción perfecta:** un teorema booleano es cierto si las dos columnas que se comparan son idénticas en **todas** las combinaciones de entrada. Con $n$ variables hay $2^n$ filas.
@end
@paso Resultado de cada comprobación
| Teorema | Un lado | El otro lado | Filas | Iguales |
|---|---|---|---|---|
| Elemento neutro de la suma | $0+X$ | $X$ | 2 | sí |
| Elemento neutro del producto | $1\cdot X$ | $X$ | 2 | sí |
| Complemento de la suma | $X+\bar X$ | $1$ | 2 | sí |
| Complemento del producto | $X\cdot\bar X$ | $0$ | 2 | sí |
| Idempotencia de la suma | $X+X$ | $X$ | 2 | sí |
| Idempotencia del producto | $X\cdot X$ | $X$ | 2 | sí |
| Elemento nulo de la suma | $X+1$ | $1$ | 2 | sí |
| Elemento nulo del producto | $X\cdot0$ | $0$ | 2 | sí |
| Absorción (1) | $X+XY$ | $X$ | 4 | sí |
| Absorción (2) | $X(X+Y)$ | $X$ | 4 | sí |
| De Morgan de la suma | $\overline{X+Y}$ | $\bar X\bar Y$ | 4 | sí |
| De Morgan del producto | $\overline{XY}$ | $\bar X+\bar Y$ | 4 | sí |
| Distributiva del producto | $X(Y+Z)$ | $XY+XZ$ | 8 | sí |
| Distributiva de la suma | $X+YZ$ | $(X+Y)(X+Z)$ | 8 | sí |
| De Morgan extendido (suma) | $\overline{X+Y+Z}$ | $\bar X\bar Y\bar Z$ | 8 | sí |
| De Morgan extendido (producto) | $\overline{XYZ}$ | $\bar X+\bar Y+\bar Z$ | 8 | sí |
@end
@paso Ejemplo: De Morgan con dos variables
| XY | $\overline{X+Y}$ | $\bar X\bar Y$ | $\overline{XY}$ | $\bar X+\bar Y$ |
|---|---|---|---|---|
| 00 | 1 | 1 | 1 | 1 |
| 01 | 0 | 0 | 1 | 1 |
| 10 | 0 | 0 | 1 | 1 |
| 11 | 0 | 0 | 0 | 0 |

Las columnas 2 y 3 coinciden, y las columnas 4 y 5 también.
@end
@paso Qué hacer con un teorema que no conoces
Haz su tabla de verdad. Si las dos columnas son iguales, es un teorema, aunque no sepas por qué. Si difieren en una sola fila, es falso.
@end
@res
Los 16 teoremas se cumplen en todas sus filas.

@box ojo | Errata del libro
En la tabla del elemento nulo, el libro imprime un $1$ en las dos filas de la columna del valor constante $0$ de $X\cdot0$. La columna del valor constante debe valer $0$, igual que el resultado de $X\cdot0$. Es un error de impresión: el teorema es correcto.
@end
@end
@end

@ej lb2-3|Minitérminos, maxitérminos, Σ y Π de cuatro funciones|Libro · Cap. 2 · P2.3|comb|lb2.p23
@enun
Con la tabla de verdad de cuatro funciones de $A,B,C,D$ (dos de ellas con combinaciones indiferentes), escribe cada una como suma de minitérminos y como producto de maxitérminos, en forma compacta $\Sigma$ y $\Pi$, y cuenta las puertas de los dos circuitos.
@end
@antes
**Minitérmino $m_i$:** producto de las 4 variables que vale 1 solo en la fila $i$ (la variable va sin negar si su bit es 1). **Maxitérmino $M_i$:** suma de las 4 variables que vale 0 solo en la fila $i$ (la variable va negada si su bit es 1). Una función es la suma de los $m_i$ de sus unos o el producto de los $M_i$ de sus ceros. Una $X$ no se escribe en ninguna de las dos formas.
@end
@paso Tabla de verdad con minitérminos y maxitérminos
| i | ABCD | Minitérmino | Maxitérmino | f1 | f2 | f3 | f4 |
|---|---|---|---|---|---|---|---|
| 0 | 0000 | $\bar{A}\bar{B}\bar{C}\bar{D}$ | $A+B+C+D$ | 0 | 1 | 1 | X |
| 1 | 0001 | $\bar{A}\bar{B}\bar{C}D$ | $A+B+C+\bar{D}$ | 1 | 1 | 0 | X |
| 2 | 0010 | $\bar{A}\bar{B}C\bar{D}$ | $A+B+\bar{C}+D$ | 1 | 0 | 1 | X |
| 3 | 0011 | $\bar{A}\bar{B}CD$ | $A+B+\bar{C}+\bar{D}$ | 1 | 1 | 1 | 0 |
| 4 | 0100 | $\bar{A}B\bar{C}\bar{D}$ | $A+\bar{B}+C+D$ | 0 | 1 | X | 0 |
| 5 | 0101 | $\bar{A}B\bar{C}D$ | $A+\bar{B}+C+\bar{D}$ | 1 | 1 | 0 | 0 |
| 6 | 0110 | $\bar{A}BC\bar{D}$ | $A+\bar{B}+\bar{C}+D$ | 0 | 0 | X | 1 |
| 7 | 0111 | $\bar{A}BCD$ | $A+\bar{B}+\bar{C}+\bar{D}$ | 0 | 0 | 1 | 1 |
| 8 | 1000 | $A\bar{B}\bar{C}\bar{D}$ | $\bar{A}+B+C+D$ | 1 | 0 | X | 1 |
| 9 | 1001 | $A\bar{B}\bar{C}D$ | $\bar{A}+B+C+\bar{D}$ | 0 | 1 | X | 0 |
| 10 | 1010 | $A\bar{B}C\bar{D}$ | $\bar{A}+B+\bar{C}+D$ | 0 | 1 | X | X |
| 11 | 1011 | $A\bar{B}CD$ | $\bar{A}+B+\bar{C}+\bar{D}$ | 0 | 1 | 0 | 1 |
| 12 | 1100 | $AB\bar{C}\bar{D}$ | $\bar{A}+\bar{B}+C+D$ | 0 | 1 | 0 | 1 |
| 13 | 1101 | $AB\bar{C}D$ | $\bar{A}+\bar{B}+C+\bar{D}$ | 0 | 1 | 0 | 1 |
| 14 | 1110 | $ABC\bar{D}$ | $\bar{A}+\bar{B}+\bar{C}+D$ | 0 | 0 | 1 | X |
| 15 | 1111 | $ABCD$ | $\bar{A}+\bar{B}+\bar{C}+\bar{D}$ | 1 | 1 | 1 | 0 |
@end
@paso Forma normal disyuntiva: suma de minitérminos
- $f1=\Sigma(1\text{-}3, 5, 8, 15)$
- $f2=\Sigma(0, 1, 3\text{-}5, 9\text{-}13, 15)$
- $f3=\Sigma(0, 2, 3, 7, 14, 15)$ con indiferentes $d(4, 6, 8\text{-}10)$
- $f4=\Sigma(6\text{-}8, 11\text{-}13)$ con indiferentes $d(0\text{-}2, 10, 14)$
@end
@paso Forma normal conjuntiva: producto de maxitérminos
- $f1=\Pi(0, 4, 6, 7, 9\text{-}14)$
- $f2=\Pi(2, 6\text{-}8, 14)$
- $f3=\Pi(1, 5, 11\text{-}13)$ con indiferentes $d(4, 6, 8\text{-}10)$
- $f4=\Pi(3\text{-}5, 9, 15)$ con indiferentes $d(0\text{-}2, 10, 14)$
@end
@paso Circuitos
Cada minitérmino es una puerta AND de 4 entradas y todas van a una OR. Cada maxitérmino es una OR de 4 entradas y todas van a una AND.

| Función | AND de 4 entradas | OR final | OR de 4 entradas | AND final |
|---|---|---|---|---|
| f1 | 6 | 1 | 10 | 1 |
| f2 | 11 | 1 | 5 | 1 |
| f3 | 6 | 1 | 5 | 1 |
| f4 | 6 | 1 | 5 | 1 |

Se necesitan además 4 inversores para tener $\bar A,\bar B,\bar C,\bar D$. Con indiferentes conviene usarlas luego al simplificar (tema de Karnaugh), pero en esta forma canónica no se escriben.
@end
@res
Se han obtenido los cuatro $\Sigma$ y los cuatro $\Pi$ y coinciden con los del libro. Se ha comprobado que los minitérminos, los maxitérminos y las indiferentes de cada función forman justo las 16 filas.
@end
@end

@ej lb2-4|Teorema de De Morgan sobre sumas y productos|Libro · Cap. 2 · P2.4|comb|lb2.p24
@enun
Aplica el teorema de De Morgan a diez expresiones: un complemento exterior sobre una suma de productos se convierte en un producto de sumas, y al revés.
@end
@antes
**Regla:** para negar una expresión, cambia cada $+$ por $\cdot$, cada $\cdot$ por $+$, y niega cada variable. Cuida los paréntesis. Para fiarte de un resultado, compara las tablas de verdad de los dos lados.
@end
@paso Las diez igualdades
- $f1=\overline{AB+CD}=(\bar A+\bar B)(\bar C+\bar D)$
- $f2=\overline{\bar A\bar B+\bar D}=(A+B)\,D$
- $f3=\overline{A+BC+BD+\bar B\bar D+\bar A\bar B}=\bar A(\bar B+\bar C)(\bar B+\bar D)(B+D)(A+B)$
- $f4=\overline{ABCD+\bar A\bar B\bar C\bar D}=(\bar A+\bar B+\bar C+\bar D)(A+B+C+D)$
- $f5=\overline{\bar A+\bar B\bar C+\bar BC\bar D+A\bar C\bar D}=A(B+C)(B+\bar C+D)(\bar A+C+D)$
- $f6=\overline{AB+AC+A\bar B\bar CD+\bar A\bar C}=(\bar A+\bar B)(\bar A+\bar C)(\bar A+B+C+\bar D)(A+C)$
- $f7=\overline{ABCD}=\bar A+\bar B+\bar C+\bar D$
- $f8=\overline{(A+B)(C+D)}=\bar A\bar B+\bar C\bar D$
- $f9=\overline{(\bar A+\bar C)(\bar A+D)(\bar A+C+\bar D)(B+D)}=AC+A\bar D+A\bar CD+\bar B\bar D$
- $f10=\overline{(B+D)\,A\,(A+\bar C+D)(\bar A+C+D)}=\bar B\bar D+\bar A+\bar AC\bar D+A\bar C\bar D$
@end
@paso Cómo se comprueba
Se ha recorrido por código toda la tabla de 16 filas de cada pareja de expresiones. En las diez, los dos lados dan la misma salida en todas las filas.
@end
@res
Las diez igualdades son correctas.

@box ojo | Errata del libro
En el apartado $f_4$ el libro escribe $(\bar A+\bar B+\bar C+\bar C)(A+B+C+D)$ con la $C$ negada dos veces. El factor correcto es $\bar A+\bar B+\bar C+\bar D$. Con la versión impresa las dos expresiones **no** son iguales (se comprueba mirando la fila $ABCD=1110$).
@end
@end
@end

@ej lb2-5|De Morgan con complementos anidados|Libro · Cap. 2 · P2.5|comb|lb2.p25
@enun
Aplica De Morgan a expresiones con paréntesis y varios niveles de complemento, de modo que al final solo queden variables negadas (nunca una barra sobre una suma o un producto).
@end
@antes
**Truco:** trabaja de fuera hacia dentro. Quita la barra exterior con la regla de De Morgan y repite el proceso con cada barra que quede dentro. Un complemento doble desaparece: $\bar{\bar x}=x$.
@end
@paso Los cinco primeros apartados
- $f_1=\overline{AB+C(A+\bar B)+D(A+\bar C)}=(\bar A+\bar B)(\bar C+\bar A B)(\bar D+\bar A C)$
- $f_2=\overline{B(C+D(A+\bar B))+\bar A\bar B}=(\bar B+\bar C(\bar D+\bar AB))(A+B)$
- $f_3=\overline{BC+A\bar D\,(B+\overline{A(B+D)})}=(\bar B+\bar C)(\bar A+D+\bar B A(B+D))$
- $f_4=\overline{A+B(C+D(A+\bar B))}=\bar A(\bar B+\bar C(\bar D+\bar AB))$
- $f_5=\overline{\overline{ABCD}+\overline{A+B+C+D}}=ABCD\,(A+B+C+D)$
@end
@paso Dos ejercicios propios del mismo estilo
- $g_1=\overline{\overline{AB}+\bar CD}=AB\,(C+\bar D)$
- $g_2=\overline{\overline{A+B}\cdot\overline{C\bar D}}=A+B+C\bar D$

Sustituyen a los apartados $f_6$ y $f_7$ del libro, que encadenan tres complementos y cuya lectura en la copia que he usado no es fiable. La técnica es idéntica.
@end
@paso Una observación
En $f_5$ el resultado se reduce a $ABCD$: si las cuatro variables valen 1, la suma $A+B+C+D$ vale 1 también, y en cualquier otro caso $ABCD=0$.
@end
@res
Las siete igualdades se han comprobado en las 16 filas de la tabla.
@end
@end

@ej lb2-6|Implementar sumas de productos solo con puertas NAND|Libro · Cap. 2 · P2.6|comb|lb2.p26
@enun
Reescribe cinco sumas de productos de modo que solo hagan falta puertas NAND (dos niveles) y cuenta las puertas.
@end
@antes
**Idea:** si niegas dos veces una suma de productos y aplicas De Morgan una vez, queda un NAND de NANDs: $\overline{\overline{t_1}\cdot\overline{t_2}\cdots}=t_1+t_2+\cdots$. Cada producto de varias variables es una NAND de primer nivel. Un término de una sola variable entra directamente negado en la NAND de salida.
@end
@paso Las cinco funciones en forma NAND
- $f1=AB+CD=\overline{\overline{AB}\,\overline{CD}}$
- $f2=\bar{A}\bar{B}+\bar{A}BCD+\bar{B}C\bar{D}=\overline{\overline{\bar{A}\bar{B}}\,\overline{\bar{A}BCD}\,\overline{\bar{B}C\bar{D}}}$
- $f3=A+BC+\bar{D}=\overline{\bar{A}\,\overline{BC}\,D}$
- $f4=\bar{A}\bar{D}+ABCD+\bar{A}\bar{C}=\overline{\overline{\bar{A}\bar{D}}\,\overline{ABCD}\,\overline{\bar{A}\bar{C}}}$
- $f5=ABCD+AB\bar{C}+\bar{A}C\bar{D}+B\bar{C}\bar{D}=\overline{\overline{ABCD}\,\overline{AB\bar{C}}\,\overline{\bar{A}C\bar{D}}\,\overline{B\bar{C}\bar{D}}}$
@end
@paso Puertas necesarias
| Función | NAND (incluida la de salida) | Inversores |
|---|---|---|
| f1 | 3 | 0 |
| f2 | 4 | 3 |
| f3 | 2 | 1 |
| f4 | 4 | 3 |
| f5 | 5 | 3 |

Los inversores sirven para generar las variables negadas que usan las NAND de primer nivel. En $f_3$ solo hace falta negar $A$; $\bar D$ ya se compensa porque $\overline{\bar D}=D$ entra directamente.
@end
@paso Comprobación
Para cada función se ha evaluado la forma con NAND y la suma de productos en las 16 combinaciones: coinciden.
@end
@res
Todas las implementaciones NAND son equivalentes a la suma de productos original.
@end
@end

@ej lb2-7|Implementar productos de sumas solo con puertas NOR|Libro · Cap. 2 · P2.7|comb|lb2.p27
@enun
Reescribe cinco productos de sumas de modo que solo hagan falta puertas NOR (dos niveles) y cuenta las puertas.
@end
@antes
**Idea:** es el dual del problema anterior. Un producto de sumas $(s_1)(s_2)\cdots$ es igual a $\overline{\overline{s_1}+\overline{s_2}+\cdots}$. Cada suma de varias variables es una NOR de primer nivel; un factor de una sola variable entra negado en la NOR de salida.
@end
@paso Las cinco funciones en forma NOR
- $f1=(A+B)(C+D)=\overline{\overline{A+B}+\overline{C+D}}$
- $f2=(\bar{A}+\bar{D})(B+\bar{C}+\bar{D})(A+\bar{B}+\bar{C}+D)=\overline{\overline{\bar{A}+\bar{D}}+\overline{B+\bar{C}+\bar{D}}+\overline{A+\bar{B}+\bar{C}+D}}$
- $f3=(\bar{B}+\bar{D})(\bar{B}+\bar{C})(\bar{A}+\bar{D})(B+D)=\overline{\overline{\bar{B}+\bar{D}}+\overline{\bar{B}+\bar{C}}+\overline{\bar{A}+\bar{D}}+\overline{B+D}}$
- $f4=(\bar{B}+\bar{C}+D)A(B+\bar{D})B=\overline{\overline{\bar{B}+\bar{C}+D}+\bar{A}+\overline{B+\bar{D}}+\bar{B}}$
- $f5=(\bar{A}+\bar{B}+\bar{D})(A+C)(B+\bar{D})(\bar{A}+\bar{D})=\overline{\overline{\bar{A}+\bar{B}+\bar{D}}+\overline{A+C}+\overline{B+\bar{D}}+\overline{\bar{A}+\bar{D}}}$
@end
@paso Puertas necesarias
| Función | NOR (incluida la de salida) | Inversores |
|---|---|---|
| f1 | 3 | 0 |
| f2 | 4 | 4 |
| f3 | 5 | 4 |
| f4 | 3 | 4 |
| f5 | 5 | 3 |
@end
@paso Un detalle
En $f_4$ aparecen los factores sueltos $A$ y $B$. Como $A\,B\,(\ldots)=1$ exige $A=B=1$, la función se reduce a $AB(\bar C+D)$ (se ha comprobado en las 16 filas). El circuito del enunciado funciona igual, pero está lejos de ser mínimo.
@end
@res
Todas las implementaciones NOR son equivalentes al producto de sumas de partida.
@end
@end

@ej lb2-8|Analizar tres circuitos y obtener su tabla de verdad|Libro · Cap. 2 · P2.8|comb|lb2.p28
@enun
Obtén la tabla de verdad de tres circuitos de tres entradas: uno con inversores, tres puertas AND y una OR; otro con tres NAND y una NAND de salida; y un sumador completo con puertas XOR, AND y OR.
@end
@antes
**Método:** fija una combinación en las entradas, propaga el valor puerta a puerta hasta la salida y apúntalo. Repite para las 8 combinaciones. Es lento pero seguro.
@end
@paso Circuito AND–OR
Las tres puertas AND calculan $\bar X\bar Y$, $XY$ y $XZ$ y una OR las suma: $f_1=\bar X\bar Y+XY+XZ$.
@end
@paso Circuito NAND–NAND
Con las mismas tres funciones en NAND de primer nivel y una NAND de salida, $f_2=\overline{\overline{\bar X\bar Y}\cdot\overline{XY}\cdot\overline{XZ}}$. Por De Morgan es igual a $f_1$: la tabla es idéntica.
@end
@paso Sumador completo
Con sumandos $A_i$, $B_i$ y acarreo de entrada $C_{i-1}$: $S_i=A_i\oplus B_i\oplus C_{i-1}$ y $C_i=A_iB_i+(A_i\oplus B_i)\,C_{i-1}$. Comprobación: $A_i+B_i+C_{i-1}=2C_i+S_i$ en las 8 filas.
@end
@paso Tabla de verdad conjunta
| XYZ = $A_iB_iC_{i-1}$ | $f_1$ | $f_2$ | $S_i$ | $C_i$ |
|---|---|---|---|---|
| 000 | 1 | 1 | 0 | 0 |
| 001 | 1 | 1 | 1 | 0 |
| 010 | 0 | 0 | 1 | 0 |
| 011 | 0 | 0 | 0 | 1 |
| 100 | 0 | 0 | 1 | 0 |
| 101 | 1 | 1 | 0 | 1 |
| 110 | 1 | 1 | 0 | 1 |
| 111 | 1 | 1 | 1 | 1 |
@end
@res
$f_1=f_2$, y el sumador completo da $S_i$ = paridad de los tres bits y $C_i$ = mayoría de los tres.
@end
@end

@ej lb2-9|Analizar un circuito de 4 entradas y 4 salidas|Libro · Cap. 2 · P2.9|comb|lb2.p29
@enun
Un circuito recibe un dígito BCD $B_3B_2B_1B_0$ y produce $X_3X_2X_1X_0$ con seis puertas AND, tres OR y un inversor directo. Obtén su tabla de verdad con las 16 combinaciones y di qué hace.
@end
@antes
**Método:** primero escribe la función de cada salida leyendo las puertas, después evalúa. Es más rápido que propagar bit a bit las 16 filas.
@end
@paso Funciones de salida
- $X_3=B_3+B_2B_0$
- $X_2=\bar B_2B_0+B_2\bar B_1\bar B_0+\bar B_2B_1$
- $X_1=B_1B_0+\bar B_1\bar B_0$ (es una XNOR)
- $X_0=\bar B_0$
@end
@paso Tabla de verdad del circuito
| $B_3B_2B_1B_0$ | Salida $X_3X_2X_1X_0$ | BCD exceso 3 ($d+3$) | Coincide |
|---|---|---|---|
| 0000 | 0011 | 0011 | ok |
| 0001 | 0100 | 0100 | ok |
| 0010 | 0101 | 0101 | ok |
| 0011 | 0110 | 0110 | ok |
| 0100 | 0111 | 0111 | ok |
| 0101 | 1000 | 1000 | ok |
| 0110 | 0001 | 1001 | error |
| 0111 | 1010 | 1010 | ok |
| 1000 | 1011 | 1011 | ok |
| 1001 | 1100 | 1100 | ok |
| 1010 | 1101 | — | sin uso |
| 1011 | 1110 | — | sin uso |
| 1100 | 1111 | — | sin uso |
| 1101 | 1000 | — | sin uso |
| 1110 | 1001 | — | sin uso |
| 1111 | 1010 | — | sin uso |
@end
@paso Conclusión
Casi todas las filas válidas ($0$ a $9$) coinciden con el código **exceso 3**: el circuito es un convertidor de BCD natural a BCD exceso 3, salvo en el dígito 6. Las filas $1010$ a $1111$ no son dígitos BCD: su salida no importa.
@end
@res
Es un convertidor BCD → exceso 3 incompleto.

@box ojo | Errata del libro
(1) Falta un término en $X_3$: el valor correcto es $X_3=B_3+B_2B_1+B_2B_0$. Con el circuito del libro el dígito $6$ ($0110$) da $0001$ en lugar de $1001$. El libro afirma que la tabla es la de un conversor a exceso 3 y no menciona este fallo.
(2) En la fila $1100$ la tabla del libro imprime $1011$, pero el circuito da $1111$ (la puerta de $X_2$ detecta $B_2\bar B_1\bar B_0$). Esta segunda diferencia no afecta a ningún dígito BCD válido.
@end
@end
@end

@ej lb2-10|Un codificador de 8 a 3 construido con puertas OR|Libro · Cap. 2 · P2.10|comb|lb2.p210
@enun
Un bloque tiene 8 entradas $E_7\ldots E_0$ y tres salidas, cada una con una OR de cuatro entradas. Obtén sus tablas con las ocho combinaciones de «un solo 1» y con algunas más con varios unos, y di qué hace.
@end
@antes
**Cómo se lee:** cada salida es una OR de las entradas cuyo número tiene un 1 en esa posición. $S_2=E_7+E_6+E_5+E_4$, $S_1=E_7+E_6+E_3+E_2$, $S_0=E_7+E_5+E_3+E_1$.
@end
@paso Tabla de verdad (selección)
| $E_7\ldots E_0$ | $S_2S_1S_0$ |
|---|---|
| 10000000 | 111 |
| 01000000 | 110 |
| 00100000 | 101 |
| 00010000 | 100 |
| 00001000 | 011 |
| 00000100 | 010 |
| 00000010 | 001 |
| 00000001 | 000 |
| 00000000 | 000 |
| 00011100 | 111 |
| 10000001 | 111 |
| 11111111 | 111 |
@end
@paso Conclusión
Con un solo 1 la salida es el número binario de la entrada activa. Con varios unos la salida es la **OR bit a bit** de sus códigos (por ejemplo $00011100\to 100\,|\,011\,|\,010=111$). Es un **codificador sin prioridad** 8:3: solo vale si se activa una entrada cada vez.
@end
@res
Codificador 8:3 sin prioridad. Las 12 filas verificadas coinciden con las del libro.
@end
@end

@ej lb2-11|Un decodificador de 3 a 8 con habilitación|Libro · Cap. 2 · P2.11|comb|lb2.p211
@enun
Un circuito con entradas $E_I,A_2,A_1,A_0$ y ocho salidas $S_7\ldots S_0$ tiene ocho puertas AND de cuatro entradas. Obtén su tabla de verdad y di qué función realiza.
@end
@antes
**Lectura:** la salida $S_k$ es una AND de $E_I$ con $A_2,A_1,A_0$ (cada una directa o negada) tal que vale 1 solo cuando $A_2A_1A_0$ es el número $k$ en binario.
@end
@paso Salidas
$S_k=E_I\cdot m_k(A_2,A_1,A_0)$ para $k=0\ldots7$, donde $m_k$ es el minitérmino de índice $k$.
@end
@paso Tabla de verdad
| $E_I$ | $A_2A_1A_0$ | $S_7S_6S_5S_4S_3S_2S_1S_0$ |
|---|---|---|
| 0 | 000 | 00000000 |
| 0 | 001 | 00000000 |
| 0 | 010 | 00000000 |
| 0 | 011 | 00000000 |
| 0 | 100 | 00000000 |
| 0 | 101 | 00000000 |
| 0 | 110 | 00000000 |
| 0 | 111 | 00000000 |
| 1 | 000 | 00000001 |
| 1 | 001 | 00000010 |
| 1 | 010 | 00000100 |
| 1 | 011 | 00001000 |
| 1 | 100 | 00010000 |
| 1 | 101 | 00100000 |
| 1 | 110 | 01000000 |
| 1 | 111 | 10000000 |
@end
@res
Con $E_I=0$ todas las salidas valen 0; con $E_I=1$ se activa solo la salida cuyo número es $A_2A_1A_0$. Es un **decodificador 3:8 con habilitación**.
@end
@end

@ej lb2-12|Un generador de paridad de 7 bits|Libro · Cap. 2 · P2.12|comb|lb2.p212
@enun
Un circuito tiene 7 entradas $D_6\ldots D_0$ y una salida $BPI_1$. Se forma con seis XOR en árbol (tres de primer nivel, dos de segundo y una de tercero que reciben $D_6$ directamente) y un inversor final. Obtén su tabla de verdad con varias combinaciones y di qué hace.
@end
@antes
**Idea:** la XOR de varios bits vale 1 si el número de unos es impar. Con el inversor al final, $BPI_1=1$ cuando el número de unos de $D_6\ldots D_0$ es **par**.
@end
@paso Tabla de verdad (selección)
| $D_6\ldots D_0$ | Unos | Salida calculada | Salida del libro | Estado |
|---|---|---|---|---|
| 0000000 | 0 | 1 | 1 | ok |
| 1010101 | 4 | 1 | 1 | ok |
| 0101010 | 3 | 0 | 0 | ok |
| 1111000 | 4 | 1 | 1 | ok |
| 0000111 | 3 | 0 | 0 | ok |
| 0110100 | 3 | 0 | 0 | ok |
| 0000011 | 2 | 1 | 1 | ok |
| 1110001 | 4 | 1 | 1 | ok |
| 1111110 | 6 | 1 | 0 | **error del libro** |
| 1111100 | 5 | 0 | 0 | ok |
| 0000001 | 1 | 0 | 0 | ok |
| 1111111 | 7 | 0 | 0 | ok |
@end
@paso Conclusión
Si añades $BPI_1$ a los 7 bits, el total de unos siempre es **impar**. Se ha verificado en las 128 combinaciones. Es un **generador de paridad impar** (bit de paridad impar).
@end
@res
Generador de paridad impar para 7 bits de datos.

@box ojo | Errata del libro
En la fila $1111110$ el libro imprime $BPI_1=0$. Tiene 6 unos (par), así que el circuito da $1$. El resto de filas coinciden.
@end
@end
@end

