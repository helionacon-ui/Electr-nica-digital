%% id=libro4
%% group=ejer
%% n=3.4
%% title=Libro de problemas · Capítulo 4 · Circuitos combinacionales con puertas
%% short=Libro · Cap. 4 Puertas lógicas
%% sub=Problemas resueltos de diseño combinacional: de la tabla de verdad al circuito de puertas, con Karnaugh, SOP y POS.

@box idea | Cómo se usa esta sección
Son los problemas resueltos del capítulo 4 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. El esquema del libro es siempre el mismo: **variables → tabla de verdad → simplificación → circuito**. Aquí cada tabla se genera por código, cada simplificación se calcula con un minimizador y se compara con la del libro (cubre los 1, no cubre ningún 0 y tiene el mismo coste), y cada circuito se describe por el número y el tipo de puertas, sin copiar el esquema. Los mapas de esta guía ponen las dos primeras variables en las filas y las otras dos en las columnas; el libro los dibuja con otros ejes, pero es el mismo mapa. Si el libro difiere, aparece una nota «Ojo». La teoría está en [[t03|el tema 3]] (Boole y Karnaugh) y [[t05|el tema 5]] (sumadores, comparadores, multiplexores).
@end

@ej lb4-1|Voto mayoritario de tres sensores|Libro · Cap. 4 · P4.1|comb,karnaugh|lb4.p41
@enun
Tres sensores binarios miden la misma señal. Diseña el circuito que dé a su salida el valor que tienen la mayoría de ellos.
@end
@antes
**Método de diseño combinacional:** (1) decide qué son entradas y qué salidas; (2) escribe la tabla de verdad; (3) pasa a suma de minitérminos; (4) simplifica con Karnaugh; (5) dibuja el circuito.
@end
@paso Entradas y salida
Entradas: $S_2,S_1,S_0$. Salida: $S$. Con tres sensores nunca hay empate, así que la mayoría siempre existe.
@end
@paso Tabla de verdad
| n | S2 | S1 | S0 | S |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 0 | 1 | 1 | 1 |
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 0 | 1 | 1 |
| 6 | 1 | 1 | 0 | 1 |
| 7 | 1 | 1 | 1 | 1 |

$S=1$ cuando hay **al menos dos** unos: filas 3, 5, 6 y 7. En la mitad de las filas gana el 0 y en la otra mitad el 1.
@end
@paso Simplificación
**$S=\Sigma(3, 5\text{-}7)$**. Simplificada: $S=S_{1}\,S_{0} + S_{2}\,S_{0} + S_{2}\,S_{1}$. Circuito de dos niveles: 3 AND de 2 entradas, 1 OR de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p41.S", "n": 3, "names": ["S2", "S1", "S0"], "title": "S", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Cada par de sensores que coinciden en 1 basta para activar la salida. Por eso hay tres términos: $S_1S_0$, $S_2S_1$ y $S_2S_0$.
@end
@paso Comprobación
El programa recorre las 8 combinaciones y comprueba que $S_1S_0+S_2S_1+S_2S_0$ vale 1 justo cuando hay dos o más unos.
@end
@res
$S=S_1S_0+S_2S_1+S_2S_0$: tres AND de dos entradas y una OR de tres, sin inversores.

@box ojo | Errata en el libro
En la fórmula final del libro el tercer término está escrito como $S_2S_1$, igual que el segundo. Debe ser $S_2S_0$: con la fórmula impresa, la combinación $S_2S_1S_0=101$ daría 0 en vez de 1. Se ha comprobado por código.
@end
@end
@end

@ej lb4-2|Divisor de dos números de 2 bits|Libro · Cap. 4 · P4.2|comb,karnaugh|lb4.p42
@enun
Diseña el circuito más pequeño que divida dos números naturales de dos bits, $A_1A_0$ entre $B_1B_0$, y dé el cociente $C_1C_0$ y el resto $R_1R_0$.
@end
@antes
**Idea:** con números tan pequeños, la «división» es repartir enteros. Hay 16 combinaciones de entrada y 4 salidas, así que son cuatro funciones de cuatro variables.
@end
@paso Entradas y salidas
Entradas: $A_1A_0$ (dividendo) y $B_1B_0$ (divisor). Salidas: cociente $C_1C_0$ y resto $R_1R_0$.
@end
@paso El caso del divisor cero
Dividir entre 0 no tiene resultado. Hay que **elegir** qué hacer. Aquí, igual que en el libro, se toma cociente y resto iguales al dividendo (filas 0, 4, 8 y 12). Es una decisión de diseño: otra opción serían indiferentes, que dan un circuito más pequeño.
@end
@paso Tabla de verdad
| A1 | A0 | B1 | B0 | C1 | C0 | R1 | R0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 |

Ejemplos: $2\div1=2$ resto 0 (fila 9); $3\div2=1$ resto 1 (fila 14); $1\div3=0$ resto 1 (fila 7).
@end
@paso Cociente $C_1$
**$C_{1}=\Sigma(8, 9, 12, 13)$**. Simplificada: $C_{1}=A_{1}\,\overline{B_{1}}$. Circuito de dos niveles: 1 AND de 2 entradas, 1 inversor ($B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p42.C1", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "C1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Cociente $C_0$
**$C_{0}=\Sigma(4, 5, 10, 12\text{-}15)$**. Simplificada: $C_{0}=A_{0}\,\overline{B_{1}} + A_{1}\,B_{1}\,\overline{B_{0}} + A_{1}\,A_{0}$. Circuito de dos niveles: 2 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 3 entradas, 2 inversores ($B_{0}$, $B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p42.C0", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "C0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Resto $R_1$
**$R_{1}=\Sigma(8, 11, 12)$**. Simplificada: $R_{1}=A_{1}\,\overline{B_{1}}\,\overline{B_{0}} + A_{1}\,\overline{A_{0}}\,B_{1}\,B_{0}$. Circuito de dos niveles: 1 AND de 3 entradas y 1 AND de 4 entradas, 1 OR de 2 entradas, 3 inversores ($A_{0}$, $B_{0}$, $B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p42.R1", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "R1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Resto $R_0$
**$R_{0}=\Sigma(4, 6, 7, 12, 14)$**. Simplificada: $R_{0}=A_{0}\,\overline{B_{0}} + \overline{A_{1}}\,A_{0}\,B_{1}$. Circuito de dos niveles: 1 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 2 entradas, 2 inversores ($A_{1}$, $B_{0}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p42.R0", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "R0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las cuatro funciones del libro son correctas y mínimas. Coste total: $C_1$ (1 término), $C_0$ (3), $R_1$ (2), $R_0$ (2).
@end
@end

@ej lb4-3|Sumador/restador de 1 bit con acarreo previo|Libro · Cap. 4 · P4.3|comb,karnaugh,aritmetica|lb4.p43
@enun
Diseña un circuito con entradas $M,A_0,B_0,C_i$ y salida $S_2S_1S_0$ en complemento a dos: si $M=0$ calcula $A_0+B_0+C_i$; si $M=1$ calcula $A_0-(B_0+C_i)$.
@end
@antes
**Ejercicio para practicar el complemento a dos.** El resultado necesita 3 bits porque el rango va de $-2$ a $+3$ ($A_0-(B_0+C_i)$ llega a $-2$; $A_0+B_0+C_i$ llega a $+3$).
@end
@paso Entradas y salidas
Cuatro entradas ($M$ elige la operación) y tres salidas $S_2S_1S_0$ en C2 de 3 bits, donde el rango es $-4\ldots+3$.
@end
@paso Tabla de verdad
| M | A0 | B0 | Ci | S2 | S1 | S0 |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 | 1 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Ejemplos: fila 3: $0+1+1=+2=010$. Fila 7: $1+1+1=+3=011$. Fila 10: $0-(1+0)=-1=111$. Fila 14: $1-(1+0)=0=000$.
@end
@paso Salida $S_2$ (signo)
**$S_{2}=\Sigma(9\text{-}11, 15)$**. Simplificada: $S_{2}=M\,\overline{A_{0}}\,\mathrm{Ci} + M\,\overline{A_{0}}\,B_{0} + M\,B_{0}\,\mathrm{Ci}$. Circuito de dos niveles: 3 AND de 3 entradas, 1 OR de 3 entradas, 1 inversor ($A_{0}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p43.S2", "n": 4, "names": ["M", "A0", "B0", "Ci"], "title": "S2", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $S_1$
**$S_{1}=\Sigma(3, 5\text{-}7, 9\text{-}11, 15)$**. Simplificada: $S_{1}=B_{0}\,\mathrm{Ci} + \overline{M}\,A_{0}\,\mathrm{Ci} + \overline{M}\,A_{0}\,B_{0} + M\,\overline{A_{0}}\,\mathrm{Ci} + M\,\overline{A_{0}}\,B_{0}$. Circuito de dos niveles: 1 AND de 2 entradas y 4 AND de 3 entradas, 1 OR de 5 entradas, 2 inversores ($A_{0}$, $M$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p43.S1", "n": 4, "names": ["M", "A0", "B0", "Ci"], "title": "S1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $S_0$
**$S_{0}=\Sigma(1, 2, 4, 7, 9, 10, 12, 15)$**. Simplificada: $S_{0}=\overline{A_{0}}\,\overline{B_{0}}\,\mathrm{Ci} + \overline{A_{0}}\,B_{0}\,\overline{\mathrm{Ci}} + A_{0}\,\overline{B_{0}}\,\overline{\mathrm{Ci}} + A_{0}\,B_{0}\,\mathrm{Ci}$. Circuito de dos niveles: 4 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($A_{0}$, $B_{0}$, $\mathrm{Ci}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p43.S0", "n": 4, "names": ["M", "A0", "B0", "Ci"], "title": "S0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Observa que $S_0=A_0\oplus B_0\oplus C_i$: el bit menos significativo no depende de $M$ (sumar o restar cambia la paridad igual).
@end
@res
Las tres funciones del libro son correctas y mínimas como suma de productos. $S_0$ es un XOR de tres entradas: con puertas XOR cuesta menos que sus cuatro términos de tres literales.
@end
@end

@ej lb4-4|Multiplicador de dos números de 2 bits|Libro · Cap. 4 · P4.4|comb,karnaugh,pos|lb4.p44
@enun
Implementa el circuito más pequeño capaz de multiplicar dos números en binario puro de dos bits, $A_1A_0$ y $B_1B_0$.
@end
@antes
**Por qué 4 bits de salida:** el producto más grande es $3\times3=9=1001_2$, que necesita 4 bits. Aquí hay muchos ceros en las salidas, así que conviene trabajar con **productos de sumas** (maxitérminos).
@end
@paso Tabla de verdad
| A1 | A0 | B1 | B0 | S3 | S2 | S1 | S0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |

Ejemplos: fila 6: $01\times10=1\times2=0010$. Fila 12: $11\times00=0$. Fila 15: $11\times11=3\times3=9=1001$.
@end
@paso Salida $S_3$
**$S3=\Pi(0\text{-}14)$**. Producto de sumas mínimo: $S3=(A_{1})(A_{0})(B_{1})(B_{0})$. En suma de productos sería $A_{1}\,A_{0}\,B_{1}\,B_{0}$ (1 términos). Coincide en coste con el libro.
@fig kmap {"key": "lb4.p44.S3", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "S3 (se marcan los ceros)", "cap": "Se rodean los ceros: cada lazo da una suma."}
@end
@paso Salida $S_2$
**$S2=\Pi(0\text{-}9, 12, 13, 15)$**. Producto de sumas mínimo: $S2=(A_{1})(B_{1})(\overline{A_{0}} + \overline{B_{0}})$. En suma de productos sería $A_{1}\,\overline{A_{0}}\,B_{1} + A_{1}\,B_{1}\,\overline{B_{0}}$ (2 términos). Coincide en coste con el libro.
@fig kmap {"key": "lb4.p44.S2", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "S2 (se marcan los ceros)", "cap": "Se rodean los ceros: cada lazo da una suma."}
@end
@paso Salida $S_1$
**$S1=\Pi(0\text{-}5, 8, 10, 12, 15)$**. Producto de sumas mínimo: $S1=(A_{1} + A_{0})(A_{1} + B_{1})(A_{0} + B_{0})(B_{1} + B_{0})(\overline{A_{1}} + \overline{A_{0}} + \overline{B_{1}} + \overline{B_{0}})$. En suma de productos sería $\overline{A_{1}}\,A_{0}\,B_{1} + A_{0}\,B_{1}\,\overline{B_{0}} + A_{1}\,\overline{A_{0}}\,B_{0} + A_{1}\,\overline{B_{1}}\,B_{0}$ (4 términos). Coincide en coste con el libro.
@fig kmap {"key": "lb4.p44.S1", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "S1 (se marcan los ceros)", "cap": "Se rodean los ceros: cada lazo da una suma."}
@end
@paso Salida $S_0$
**$S0=\Pi(0\text{-}4, 6, 8\text{-}12, 14)$**. Producto de sumas mínimo: $S0=(A_{0})(B_{0})$. En suma de productos sería $A_{0}\,B_{0}$ (1 términos). Coincide en coste con el libro.
@fig kmap {"key": "lb4.p44.S0", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "S0 (se marcan los ceros)", "cap": "Se rodean los ceros: cada lazo da una suma."}

Es el AND de los dos bits menos significativos: $A_0B_0$.
@end
@res
Se comprueba que las cuatro salidas forman el producto correcto para las 16 combinaciones. $S_3=A_1A_0B_1B_0$ y $S_0=A_0B_0$ son simples ANDs; $S_2$ y $S_1$ son las que requieren simplificar.
@end
@end

@ej lb4-5|Complemento a dos de un número de 4 bits|Libro · Cap. 4 · P4.5|comb,karnaugh,aritmetica|lb4.p45
@enun
Diseña el circuito más pequeño que calcule el complemento a dos de un número de cuatro bits $E_3E_2E_1E_0$, con salida $C_3C_2C_1C_0$.
@end
@antes
**Regla:** C2 $=$ invertir todos los bits $+1$. Hay una forma más rápida de leerlo: de derecha a izquierda se copian los bits hasta el primer 1 (incluido) y el resto se invierte.
@end
@paso Tabla de verdad
| E3 | E2 | E1 | E0 | C3 | C2 | C1 | C0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 |
| 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

Ejemplos: $0010\to1101+1=1110$. $1000\to0111+1=1000$ (el $-8$ es su propio opuesto). $0000\to1111+1=0000$.
@end
@paso Salida $C_3$
**$C_{3}=\Sigma(1\text{-}8)$**. Simplificada: $C_{3}=\overline{E_{3}}\,E_{0} + \overline{E_{3}}\,E_{1} + \overline{E_{3}}\,E_{2} + E_{3}\,\overline{E_{2}}\,\overline{E_{1}}\,\overline{E_{0}}$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 4 entradas, 1 OR de 4 entradas, 4 inversores ($E_{0}$, $E_{1}$, $E_{2}$, $E_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p45.C3", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "C3", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $C_2$
**$C_{2}=\Sigma(1\text{-}4, 9\text{-}12)$**. Simplificada: $C_{2}=\overline{E_{2}}\,E_{0} + \overline{E_{2}}\,E_{1} + E_{2}\,\overline{E_{1}}\,\overline{E_{0}}$. Circuito de dos niveles: 2 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 3 entradas, 3 inversores ($E_{0}$, $E_{1}$, $E_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p45.C2", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "C2", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $C_1$
**$C_{1}=\Sigma(1, 2, 5, 6, 9, 10, 13, 14)$**. Simplificada: $C_{1}=\overline{E_{1}}\,E_{0} + E_{1}\,\overline{E_{0}}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas, 2 inversores ($E_{0}$, $E_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p45.C1", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "C1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Es el XOR $E_1\oplus E_0$.
@end
@paso Salida $C_0$
**$C_{0}=\Sigma(1, 3, 5, 7, 9, 11, 13, 15)$**. Simplificada: $C_{0}=E_{0}$. $C_{0}$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p45.C0", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "C0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

El bit menos significativo no cambia: $C_0=E_0$, un cable.
@end
@res
Las cuatro funciones del libro son correctas y mínimas. Nota: el $-8$ ($1000$) no tiene opuesto en 4 bits y el circuito lo devuelve igual: es el desbordamiento típico del C2.
@end
@end

@ej lb4-6|Complemento a 9 de un dígito BCD|Libro · Cap. 4 · P4.6|comb,karnaugh,bcd|lb4.p46
@enun
Diseña el circuito más pequeño que obtenga el complemento a 9 de un dígito BCD $B_3B_2B_1B_0$, con salida $C_{93}C_{92}C_{91}C_{90}$.
@end
@antes
**Complemento a 9:** para un dígito $B$ es $9-B$. Se usa para restar en decimal. Las combinaciones $1010\ldots1111$ no son dígitos BCD: ¿qué hacer con ellas?
@end
@paso Qué hacer con las seis combinaciones prohibidas
Hay tres opciones: (1) declarar la salida **indiferente** ($\times$), (2) forzar un valor, por ejemplo $0000$, o (3) añadir una salida de **error** que valga 1. El libro elige la primera, porque da circuitos más pequeños. Si se quisiera la salida de error, sería $B_3B_2+B_3B_1$ (comprobado por código).
@end
@paso Tabla de verdad
| B3 | B2 | B1 | B0 | C93 | C92 | C91 | C90 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 |
| 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | × | × | × | × |
| 1 | 0 | 1 | 1 | × | × | × | × |
| 1 | 1 | 0 | 0 | × | × | × | × |
| 1 | 1 | 0 | 1 | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × |

Ejemplos: $0\to 9=1001$; $6\to 3=0011$; $9\to 0=0000$.
@end
@paso Salida $C_{93}$
**$C_{93}=\Sigma(0, 1)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $C_{93}=\overline{B_{3}}\,\overline{B_{2}}\,\overline{B_{1}}$. Circuito de dos niveles: 1 AND de 3 entradas, 3 inversores ($B_{1}$, $B_{2}$, $B_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p46.C93", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "C93", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $C_{92}$
**$C_{92}=\Sigma(2\text{-}5)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $C_{92}=\overline{B_{2}}\,B_{1} + B_{2}\,\overline{B_{1}}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas, 2 inversores ($B_{1}$, $B_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p46.C92", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "C92", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $C_{91}$
**$C_{91}=\Sigma(2, 3, 6, 7)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $C_{91}=B_{1}$. $C_{91}$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p46.C91", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "C91", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Fíjate: $C_{91}=B_1$ es un cable, no hace falta ninguna puerta.
@end
@paso Salida $C_{90}$
**$C_{90}=\Sigma(0, 2, 4, 6, 8)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $C_{90}=\overline{B_{0}}$. Circuito de dos niveles: 1 inversor ($B_{0}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p46.C90", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "C90", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Es un solo inversor.
@end
@res
Con las indiferentes, las cuatro funciones son muy sencillas: un AND de tres entradas, dos AND y una OR, un cable y un inversor. Las cuatro soluciones del libro son correctas y mínimas.
@end
@end

@ej lb4-7|Control de calidad: cuatro piezas por lote|Libro · Cap. 4 · P4.7|comb,karnaugh|lb4.p47
@enun
De cada lote se extraen 4 piezas y un sensor da 1 si la pieza es aprobada y 0 si no. Diseña el circuito que indique: todas aprobadas ($TA$), mayoría aprobada ($MA$), igual número de aprobadas y rechazadas ($I$) y mayoría de rechazadas ($MR$).
@end
@antes
**Truco:** el número de unos de la entrada decide la salida. Cuatro unos: TA. Tres: MA. Dos: I. Cero o uno: MR. Siempre se activa **una y solo una** de las cuatro salidas.
@end
@paso Tabla de verdad
| M1 | M2 | M3 | M4 | TA | MA | I | MR |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

Fila 0: todas rechazadas, $MR=1$. Fila 6 ($0110$): dos aprobadas, $I=1$. Fila 11 ($1011$): tres aprobadas, $MA=1$. Fila 15: $TA=1$ (y $MA$ no se activa, aunque la mayoría también sea de aprobadas).
@end
@paso Salida $TA$
**$\mathrm{TA}=\Sigma(15)$**. Simplificada: $\mathrm{TA}=M_{1}\,M_{2}\,M_{3}\,M_{4}$. Circuito de dos niveles: 1 AND de 4 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p47.TA", "n": 4, "names": ["M1", "M2", "M3", "M4"], "title": "TA", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $MA$
**$\mathrm{MA}=\Sigma(7, 11, 13, 14)$**. Simplificada: $\mathrm{MA}=\overline{M_{1}}\,M_{2}\,M_{3}\,M_{4} + M_{1}\,\overline{M_{2}}\,M_{3}\,M_{4} + M_{1}\,M_{2}\,\overline{M_{3}}\,M_{4} + M_{1}\,M_{2}\,M_{3}\,\overline{M_{4}}$. Circuito de dos niveles: 4 AND de 4 entradas, 1 OR de 4 entradas, 4 inversores ($M_{1}$, $M_{2}$, $M_{3}$, $M_{4}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p47.MA", "n": 4, "names": ["M1", "M2", "M3", "M4"], "title": "MA", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Los cuatro 1 del mapa están aislados (no son vecinos): no hay nada que agrupar y la suma de minitérminos ya es la mínima.
@end
@paso Salida $I$
**$I=\Sigma(3, 5, 6, 9, 10, 12)$**. Simplificada: $I=\overline{M_{1}}\,\overline{M_{2}}\,M_{3}\,M_{4} + \overline{M_{1}}\,M_{2}\,\overline{M_{3}}\,M_{4} + \overline{M_{1}}\,M_{2}\,M_{3}\,\overline{M_{4}} + M_{1}\,\overline{M_{2}}\,\overline{M_{3}}\,M_{4} + M_{1}\,\overline{M_{2}}\,M_{3}\,\overline{M_{4}} + M_{1}\,M_{2}\,\overline{M_{3}}\,\overline{M_{4}}$. Circuito de dos niveles: 6 AND de 4 entradas, 1 OR de 6 entradas, 4 inversores ($M_{1}$, $M_{2}$, $M_{3}$, $M_{4}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p47.I", "n": 4, "names": ["M1", "M2", "M3", "M4"], "title": "I", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

Seis minitérminos aislados: es el patrón de «tablero de ajedrez» de los mapas, que no se simplifica. Son las combinaciones con exactamente dos unos.
@end
@paso Salida $MR$
**$\mathrm{MR}=\Sigma(0\text{-}2, 4, 8)$**. Simplificada: $\mathrm{MR}=\overline{M_{1}}\,\overline{M_{2}}\,\overline{M_{3}} + \overline{M_{1}}\,\overline{M_{2}}\,\overline{M_{4}} + \overline{M_{1}}\,\overline{M_{3}}\,\overline{M_{4}} + \overline{M_{2}}\,\overline{M_{3}}\,\overline{M_{4}}$. Circuito de dos niveles: 4 AND de 3 entradas, 1 OR de 4 entradas, 4 inversores ($M_{1}$, $M_{2}$, $M_{3}$, $M_{4}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p47.MR", "n": 4, "names": ["M1", "M2", "M3", "M4"], "title": "MR", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Los cuatro resultados coinciden con los del libro y son mínimos. Observa el coste: $MA$ e $I$ necesitan 4 y 6 AND de 4 entradas. Es el precio de detectar «exactamente $k$ unos».
@end
@end

@ej lb4-8|Rumbo de un barco en un display de 7 segmentos|Libro · Cap. 4 · P4.8|comb,karnaugh,7seg|lb4.p48
@enun
El piloto automático indica el rumbo con cuatro señales $N,S,E,O$. Diseña el circuito más pequeño que lo dibuje en un 7 segmentos: norte activa $a$; sur, $d$; este, $b,c$; oeste, $e,f$; noreste, $a,b$; noroeste, $a,f$; sureste, $c,d$; suroeste, $d,e$.
@end
@antes
**Dibujar con segmentos.** Cada fila de la tabla es un rumbo y solo hay que «pintarlo». Un rumbo válido tiene una señal activa, o dos que sean vecinas (N+E, N+O, S+E, S+O). Norte con sur, o este con oeste, son imposibles.
@end
@paso Qué filas son válidas
Válidas (8): $N$=8, $S$=4, $E$=2, $O$=1, $NE$=10, $NO$=9, $SE$=6, $SO$=5. Imposibles (8): 0, 3, 7, 11, 12, 13, 14 y 15. El libro las deja como indiferentes, incluida la fila 0 (sin rumbo): un barco siempre lleva alguno.
@end
@paso Tabla de verdad
| N | S | E | O | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | × | × | × | × | × | × | × |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | × | × | × | × | × | × | × |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | × | × | × | × | × | × | × |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × | × | × | × |

Ejemplos: fila 1 (oeste): se encienden $e,f$ (el lado izquierdo). Fila 9 (noroeste): $a,f$. Fila 8 (norte): solo $a$.
@end
@paso Segmento $a$
**$a=\Sigma(8\text{-}10)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $a=N$. $a$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.a", "n": 4, "names": ["N", "S", "E", "O"], "title": "a", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $b$
**$b=\Sigma(2, 10)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $b=\overline{S}\,E$. Circuito de dos niveles: 1 AND de 2 entradas, 1 inversor ($S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.b", "n": 4, "names": ["N", "S", "E", "O"], "title": "b", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $c$
**$c=\Sigma(2, 6)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $c=\overline{N}\,E$. Circuito de dos niveles: 1 AND de 2 entradas, 1 inversor ($N$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.c", "n": 4, "names": ["N", "S", "E", "O"], "title": "c", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $d$
**$d=\Sigma(4\text{-}6)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $d=S$. $d$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.d", "n": 4, "names": ["N", "S", "E", "O"], "title": "d", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $e$
**$e=\Sigma(1, 5)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $e=\overline{N}\,O$. Circuito de dos niveles: 1 AND de 2 entradas, 1 inversor ($N$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.e", "n": 4, "names": ["N", "S", "E", "O"], "title": "e", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $f$
**$f=\Sigma(1, 9)$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $f=\overline{S}\,O$. Circuito de dos niveles: 1 AND de 2 entradas, 1 inversor ($S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p48.f", "n": 4, "names": ["N", "S", "E", "O"], "title": "f", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $g$
**$g=\Sigma()$** con indiferentes $d(0, 3, 7, 11, 12, 13, 14, 15)$. Simplificada: $g=0$. La salida $g$ es constante. Coincide en coste con la solución del libro (misma expresión).
@end
@res
Con tantas indiferentes, casi todo se reduce a una o dos variables: $a=N$, $d=S$, $b=\bar S E$, $c=\bar N E$, $e=\bar N O$, $f=\bar S O$ y $g=0$ (el segmento central nunca se enciende). Todas coinciden con el libro.
@end
@end

@ej lb4-9|Rumbo del barco con alarma de datos erróneos|Libro · Cap. 4 · P4.9|comb,karnaugh,7seg|lb4.p49
@enun
Repite el ejercicio anterior, pero si las señales dan información imposible se debe encender **todo** el 7 segmentos.
@end
@antes
**Cambio respecto al 4.8:** las ocho combinaciones imposibles dejan de ser indiferentes y valen 1 en las siete salidas. Un display totalmente encendido avisa al piloto de que algo falla. A cambio, el circuito crece: perdemos las simplificaciones que daban las $\times$.
@end
@paso Tabla de verdad
| N | S | E | O | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Es la tabla del 4.8 con las $\times$ convertidas en 1.
@end
@paso Segmento $a$
**$a=\Sigma(0, 3, 7\text{-}15)$**. Simplificada: $a=\overline{S}\,\overline{E}\,\overline{O} + E\,O + N$. Circuito de dos niveles: 1 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 3 entradas, 3 inversores ($E$, $O$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.a", "n": 4, "names": ["N", "S", "E", "O"], "title": "a", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $b$
**$b=\Sigma(0, 2, 3, 7, 10\text{-}15)$**. Simplificada: $b=\overline{N}\,\overline{S}\,\overline{O} + \overline{S}\,E + E\,O + N\,S$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($N$, $O$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.b", "n": 4, "names": ["N", "S", "E", "O"], "title": "b", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $c$
**$c=\Sigma(0, 2, 3, 6, 7, 11\text{-}15)$**. Simplificada: $c=\overline{N}\,\overline{S}\,\overline{O} + \overline{N}\,E + E\,O + N\,S$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($N$, $O$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.c", "n": 4, "names": ["N", "S", "E", "O"], "title": "c", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $d$
**$d=\Sigma(0, 3\text{-}7, 11\text{-}15)$**. Simplificada: $d=\overline{N}\,\overline{E}\,\overline{O} + E\,O + S$. Circuito de dos niveles: 1 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 3 entradas, 3 inversores ($E$, $N$, $O$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.d", "n": 4, "names": ["N", "S", "E", "O"], "title": "d", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $e$
**$e=\Sigma(0, 1, 3, 5, 7, 11\text{-}15)$**. Simplificada: $e=\overline{N}\,\overline{S}\,\overline{E} + \overline{N}\,O + E\,O + N\,S$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($E$, $N$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.e", "n": 4, "names": ["N", "S", "E", "O"], "title": "e", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $f$
**$f=\Sigma(0, 1, 3, 7, 9, 11\text{-}15)$**. Simplificada: $f=\overline{N}\,\overline{S}\,\overline{E} + \overline{S}\,O + E\,O + N\,S$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($E$, $N$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.f", "n": 4, "names": ["N", "S", "E", "O"], "title": "f", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $g$
**$g=\Sigma(0, 3, 7, 11\text{-}15)$**. Simplificada: $g=\overline{N}\,\overline{S}\,\overline{E}\,\overline{O} + E\,O + N\,S$. Circuito de dos niveles: 2 AND de 2 entradas y 1 AND de 4 entradas, 1 OR de 3 entradas, 4 inversores ($E$, $N$, $O$, $S$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p49.g", "n": 4, "names": ["N", "S", "E", "O"], "title": "g", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las siete funciones del libro son mínimas, salvo una errata en $b$ (ver nota). Comparado con el 4.8, el circuito pasa de unos pocos cables a 3–4 productos por salida: **saber qué pasa con lo imposible cambia mucho el coste**. El término $EO$ (la combinación imposible «este y oeste») aparece en las siete salidas, y $NS$ («norte y sur») en cinco.

@box ojo | Errata en el libro (función $b$)
En la fórmula del libro para $b$, el primer término está escrito con $\bar E$ ($\bar N\bar S\bar E$). Ese término valdría 1 en la fila 1 ($0001$, oeste), pero $b=0$ en esa fila. El término correcto es $\bar N\bar S\bar O$ (cubre las filas 0 y 2). Se ha comprobado por código.
@end
@end
@end

@ej lb4-10|Decodificador de BCD a 7 segmentos|Libro · Cap. 4 · P4.10|comb,karnaugh,7seg,bcd|lb4.p410
@enun
Implementa el circuito más pequeño que convierta un dígito BCD $B_3B_2B_1B_0$ en las siete señales $a,b,c,d,e,f,g$ de un display de 7 segmentos.
@end
@antes
**Cómo se rellena la tabla:** ten delante un 7 segmentos dibujado y apunta qué segmentos forman cada cifra. Las filas 10 a 15 no son BCD y se dejan como indiferentes. El 6 se dibuja sin el segmento superior ($a=0$) y el 9 sin el inferior ($d=0$); son formas de escribirlos, no la única posible.
@end
@paso Tabla de verdad
| B3 | B2 | B1 | B0 | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | × | × | × | × | × | × | × |
| 1 | 0 | 1 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × | × | × | × |

Ejemplos: el 0 enciende todo menos $g$ ($1111110$); el 1, $b$ y $c$ ($0110000$); el 2, $a,b,d,e,g$ ($1101101$).
@end
@paso Segmento $a$
**$a=\Sigma(0, 2, 3, 5, 7\text{-}9)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $a=\overline{B_{2}}\,\overline{B_{0}} + \overline{B_{2}}\,B_{1} + B_{2}\,B_{0} + B_{3}$. Circuito de dos niveles: 3 AND de 2 entradas, 1 OR de 4 entradas, 2 inversores ($B_{0}$, $B_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.a", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "a", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $b$
**$b=\Sigma(0\text{-}4, 7\text{-}9)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $b=\overline{B_{2}} + \overline{B_{1}}\,\overline{B_{0}} + B_{1}\,B_{0}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 3 entradas, 3 inversores ($B_{0}$, $B_{1}$, $B_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.b", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "b", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $c$
**$c=\Sigma(0, 1, 3\text{-}9)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $c=\overline{B_{1}} + B_{0} + B_{2}$. Circuito de dos niveles: 1 OR de 3 entradas, 1 inversor ($B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.c", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "c", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $d$
**$d=\Sigma(0, 2, 3, 5, 6, 8)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $d=\overline{B_{2}}\,\overline{B_{0}} + \overline{B_{2}}\,B_{1} + B_{1}\,\overline{B_{0}} + B_{2}\,\overline{B_{1}}\,B_{0}$. Circuito de dos niveles: 3 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 4 entradas, 3 inversores ($B_{0}$, $B_{1}$, $B_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.d", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "d", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $e$
**$e=\Sigma(0, 2, 6, 8)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $e=\overline{B_{2}}\,\overline{B_{0}} + B_{1}\,\overline{B_{0}}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas, 2 inversores ($B_{0}$, $B_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.e", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "e", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $f$
**$f=\Sigma(0, 4\text{-}6, 8, 9)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $f=\overline{B_{1}}\,\overline{B_{0}} + B_{2}\,\overline{B_{1}} + B_{2}\,\overline{B_{0}} + B_{3}$. Circuito de dos niveles: 3 AND de 2 entradas, 1 OR de 4 entradas, 2 inversores ($B_{0}$, $B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p410.f", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "f", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Segmento $g$
**$g=\Sigma(2\text{-}6, 8, 9)$** con indiferentes $d(10, 11, 12, 13, 14, 15)$. Simplificada: $g=\overline{B_{2}}\,B_{1} + B_{1}\,\overline{B_{0}} + B_{2}\,\overline{B_{1}} + B_{3}$. Circuito de dos niveles: 3 AND de 2 entradas, 1 OR de 4 entradas, 3 inversores ($B_{0}$, $B_{1}$, $B_{2}$). Coincide en coste con la solución del libro (otra forma equivalente, también mínima).
@fig kmap {"key": "lb4.p410.g", "n": 4, "names": ["B3", "B2", "B1", "B0"], "title": "g", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Variante: el 9 con segmento inferior
Si se prefiere el 9 con el segmento $d$ encendido, solo cambia $d$, que pasa a valer 1 también en la fila 9: $d=\overline{B_{2}}\,\overline{B_{0}} + \overline{B_{2}}\,B_{1} + B_{1}\,\overline{B_{0}} + B_{2}\,\overline{B_{1}}\,B_{0} + B_{3}$ (5 términos, frente a 4).
@end
@res
Las siete simplificaciones del libro son correctas y de coste mínimo. Cada segmento necesita entre 1 y 4 productos. $c=\bar B_1+B_0+B_2$ es el más sencillo (solo es 0 en los números 2).

@box ojo | Errata en el libro (tabla)
En la tabla del libro, la fila del 9 aparece con $d=1$ y $f=0$ ($1111001$), que es justo lo contrario de lo que dicen sus propios sumatorios ($d=\Sigma(0,2,3,5,6,8)$ no incluye el 9 y $f=\Sigma(0,4,5,6,8,9)$ sí). Aquí se sigue la versión de los sumatorios y de las expresiones finales ($1110011$).
@end
@end
@end

@ej lb4-11|Comparador de dos números de 2 bits|Libro · Cap. 4 · P4.11|comb,karnaugh,comparador|lb4.p411
@enun
Diseña un comparador de dos números $A=A_1A_0$ y $B=B_1B_0$ con tres salidas: $A>B$, $A=B$ y $A<B$.
@end
@antes
**Idea:** se comparan las dos cifras y se activa **una sola** de las tres salidas. Es un ejercicio muy sistemático: la tabla se escribe leyendo $A$ y $B$ como números de 0 a 3.
@end
@paso Tabla de verdad
| A1 | A0 | B1 | B0 | A>B | A=B | A<B |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 1 | 0 |

Fila 0: $0=0$. Fila 3: $0<3$. Fila 8: $2>0$.
@end
@paso Salida $A>B$
**$(A>B)=\Sigma(4, 8, 9, 12\text{-}14)$**. Simplificada: $G=A_{0}\,\overline{B_{1}}\,\overline{B_{0}} + A_{1}\,\overline{B_{1}} + A_{1}\,A_{0}\,\overline{B_{0}}$. Circuito de dos niveles: 1 AND de 2 entradas y 2 AND de 3 entradas, 1 OR de 3 entradas, 2 inversores ($B_{0}$, $B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p411.G", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "G", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $A=B$
**$(A=B)=\Sigma(0, 5, 10, 15)$**. Simplificada: $E=\overline{A_{1}}\,\overline{A_{0}}\,\overline{B_{1}}\,\overline{B_{0}} + \overline{A_{1}}\,A_{0}\,\overline{B_{1}}\,B_{0} + A_{1}\,\overline{A_{0}}\,B_{1}\,\overline{B_{0}} + A_{1}\,A_{0}\,B_{1}\,B_{0}$. Circuito de dos niveles: 4 AND de 4 entradas, 1 OR de 4 entradas, 4 inversores ($A_{0}$, $A_{1}$, $B_{0}$, $B_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p411.E", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "E", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

La igualdad es la diagonal del mapa y no se simplifica: cuatro minitérminos. Pero hay un truco: $A=B$ equivale a que **cada pareja de bits** coincida, es decir, $(A_1\odot B_1)\cdot(A_0\odot B_0)$ con dos puertas XNOR y un AND. Es la forma habitual de hacerlo (verificada por código).
@end
@paso Salida $A<B$
**$(A<B)=\Sigma(1\text{-}3, 6, 7, 11)$**. Simplificada: $L=\overline{A_{1}}\,\overline{A_{0}}\,B_{0} + \overline{A_{1}}\,B_{1} + \overline{A_{0}}\,B_{1}\,B_{0}$. Circuito de dos niveles: 1 AND de 2 entradas y 2 AND de 3 entradas, 1 OR de 3 entradas, 2 inversores ($A_{0}$, $A_{1}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p411.L", "n": 4, "names": ["A1", "A0", "B1", "B0"], "title": "L", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las tres funciones del libro son correctas y mínimas como suma de productos. La salida «$A=B$» es mucho más barata con XNOR que con cuatro AND de cuatro entradas.
@end
@end

@ej lb4-12|Máquina registradora con cambio|Libro · Cap. 4 · P4.12|comb,karnaugh|lb4.p412
@enun
Una máquina tiene cuatro ranuras, de 25, 25, 10 y 5 ptas (en cada una cabe una moneda). Entrega el producto cuando lo introducido llega a 40 ptas o más y devuelve el cambio con monedas de 5 y de 10. Salidas: producto $PR$, vuelta de 5 ($D_5$) y dos vueltas de 10 ($D_{10A}$, $D_{10B}$).
@end
@antes
**Sumar el dinero de cada fila:** $25A+25B+10+5$. Si llega a 40, se da producto y el cambio es lo que sobra, repartido con monedas de 10 primero y de 5 si queda una.
@end
@paso Tabla de verdad
| M25A | M25B | M10 | M5 | PR | D5 | D10A | D10B |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Ejemplos: fila 7 ($25+10+5=40$): solo $PR$. Fila 12 ($25+25=50$): producto y 10 de vuelta ($D_{10A}$). Fila 13 ($55$): producto y 15 de vuelta ($D_{10A}$ y $D_5$). Fila 15 ($65$): producto y 25 de vuelta ($D_{10A},D_{10B},D_5$).
@end
@paso Una decisión de diseño
Las filas intermedias (por ejemplo 10 ptas) no dan nada: la máquina está esperando más monedas. Además la fila 15 «no debería ocurrir», porque el producto ya habría salido antes. Aun así **no se dejan indiferentes**: un valor libre en la salida podría soltar monedas por error. Pon un valor seguro cuando un error cueste dinero.
@end
@paso Producto $PR$
**$\mathrm{PR}=\Sigma(7, 11\text{-}15)$**. Simplificada: $\mathrm{PR}=\mathrm{M25B}\,M_{10}\,M_{5} + \mathrm{M25A}\,M_{10}\,M_{5} + \mathrm{M25A}\,\mathrm{M25B}$. Circuito de dos niveles: 1 AND de 2 entradas y 2 AND de 3 entradas, 1 OR de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p412.PR", "n": 4, "names": ["M25A", "M25B", "M10", "M5"], "title": "PR", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Vuelta de 5 ($D_5$)
**$D_{5}=\Sigma(13, 15)$**. Simplificada: $D_{5}=\mathrm{M25A}\,\mathrm{M25B}\,M_{5}$. Circuito de dos niveles: 1 AND de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p412.D5", "n": 4, "names": ["M25A", "M25B", "M10", "M5"], "title": "D5", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Vuelta de 10 ($D_{10A}$)
**$\mathrm{D10A}=\Sigma(12\text{-}15)$**. Simplificada: $\mathrm{D10A}=\mathrm{M25A}\,\mathrm{M25B}$. Circuito de dos niveles: 1 AND de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p412.D10A", "n": 4, "names": ["M25A", "M25B", "M10", "M5"], "title": "D10A", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Vuelta de 10 ($D_{10B}$)
**$\mathrm{D10B}=\Sigma(14, 15)$**. Simplificada: $\mathrm{D10B}=\mathrm{M25A}\,\mathrm{M25B}\,M_{10}$. Circuito de dos niveles: 1 AND de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p412.D10B", "n": 4, "names": ["M25A", "M25B", "M10", "M5"], "title": "D10B", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las cuatro funciones del libro son correctas y mínimas. $D_{10A}$ y $D_{10B}$ son simples ANDs: el cambio solo existe cuando se han metido las dos monedas de 25.
@end
@end

@ej lb4-13|Nota de un alumno en un 7 segmentos (solo NAND)|Libro · Cap. 4 · P4.13|comb,karnaugh,nand,7seg|lb4.p413
@enun
La nota (0 a 10) llega en binario puro $N_3N_2N_1N_0$. Diseña con puertas NAND el circuito que la muestre en un 7 segmentos de cátodo común: suspenso (0–4) enciende $g$; aprobado (5), $a$; bien (6), $a,b$; notable (7–8), $a,b,c$; sobresaliente (9), $a,b,c,d$; matrícula (10), todos menos $g$.
@end
@antes
**Dos pasos:** (1) simplificar como suma de productos; (2) pasar a **NAND–NAND**: cada AND se sustituye por un NAND y la OR final por otro NAND. Por De Morgan el resultado no cambia, y una familia lógica solo necesita un tipo de puerta. Las filas 11 a 15 (notas imposibles) son indiferentes. Atención: aquí 10 es una nota válida (no confundir con BCD).
@end
@paso Tabla de verdad
| N3 | N2 | N1 | N0 | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 0 | 1 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × | × | × | × |
@end
@paso Simplificación de las siete salidas
**a.** **$a=\Sigma(5\text{-}10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $a=N_{2}\,N_{0} + N_{2}\,N_{1} + N_{3}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.a", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "a", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**b.** **$b=\Sigma(6\text{-}10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $b=N_{2}\,N_{1} + N_{3}$. Circuito de dos niveles: 1 AND de 2 entradas, 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.b", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "b", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**c.** **$c=\Sigma(7\text{-}10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $c=N_{2}\,N_{1}\,N_{0} + N_{3}$. Circuito de dos niveles: 1 AND de 3 entradas, 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.c", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "c", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**d.** **$d=\Sigma(9, 10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $d=N_{3}\,N_{0} + N_{3}\,N_{1}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.d", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "d", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**e.** **$e=\Sigma(10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $e=N_{3}\,N_{1}$. Circuito de dos niveles: 1 AND de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.e", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "e", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**f.** **$f=\Sigma(10)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $f=N_{3}\,N_{1}$. Circuito de dos niveles: 1 AND de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.f", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "f", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

**g.** **$g=\Sigma(0\text{-}4)$** con indiferentes $d(11, 12, 13, 14, 15)$. Simplificada: $g=\overline{N_{3}}\,\overline{N_{2}} + \overline{N_{3}}\,\overline{N_{1}}\,\overline{N_{0}}$. Circuito de dos niveles: 1 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 2 entradas, 4 inversores ($N_{0}$, $N_{1}$, $N_{2}$, $N_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p413.g", "n": 4, "names": ["N3", "N2", "N1", "N0"], "title": "g", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Paso a NAND–NAND
Regla: $S=T_1+T_2+\dots=\overline{\overline{T_1}\cdot\overline{T_2}\cdots}$. Cada producto $T_i$ de dos o más literales sale de una NAND; la salida es una NAND de todas ellas. Un literal solo, como $N_3$, entra a la NAND de salida a través de un inversor (una NAND con las entradas unidas). Aquí, compartiendo términos que se repiten ($N_2N_1$, $N_3N_1$) y con $e=f$ iguales:
- 7 NAND de dos o tres entradas para los productos,
- 6 NAND de salida distintas (las salidas $e$ y $f$ son la misma señal),
- 4 inversores para los complementos de entrada ($\overline{N_{0}}, \overline{N_{1}}, \overline{N_{2}}, \overline{N_{3}}$) y 1 para el literal suelto $N_3$.
Se ha simulado por código el circuito NAND–NAND completo y da exactamente la tabla de verdad para las 11 notas válidas.
@end
@res
Las siete funciones del libro son correctas y mínimas. Se ve la lógica de las notas: $e$ y $f$ solo valen 1 en la matrícula ($N_3N_1$), $d$ en 9 y 10, y $g$ en el suspenso (0 a 4). Fíjate en que $N_3$ solo vale 1 a partir de 8, y las indiferentes de 11 a 15 permiten escribir «$N_3$» en vez de un producto largo.
@end
@end

@ej lb4-14|Termómetro con dos leds (verde/rojo)|Libro · Cap. 4 · P4.14|comb,karnaugh,c2|lb4.p414
@enun
Activa el led verde $LV$ si la temperatura está entre $-3$ y $+4\,^\circ$C (ambas incluidas) y el rojo $LR$ en el resto. La temperatura llega en complemento a 2 con 4 bits $T_3T_2T_1T_0$.
@end
@antes
**Lectura en C2:** con 4 bits se representan los valores de $-8$ a $+7$. Las filas $0\ldots7$ son $0\ldots7$ y las filas $8\ldots15$ son $-8\ldots-1$.
@end
@paso Tabla de verdad
| T3 | T2 | T1 | T0 | grados | LV | LR |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 1 | +1 | 1 | 0 |
| 0 | 0 | 1 | 0 | +2 | 1 | 0 |
| 0 | 0 | 1 | 1 | +3 | 1 | 0 |
| 0 | 1 | 0 | 0 | +4 | 1 | 0 |
| 0 | 1 | 0 | 1 | +5 | 0 | 1 |
| 0 | 1 | 1 | 0 | +6 | 0 | 1 |
| 0 | 1 | 1 | 1 | +7 | 0 | 1 |
| 1 | 0 | 0 | 0 | -8 | 0 | 1 |
| 1 | 0 | 0 | 1 | -7 | 0 | 1 |
| 1 | 0 | 1 | 0 | -6 | 0 | 1 |
| 1 | 0 | 1 | 1 | -5 | 0 | 1 |
| 1 | 1 | 0 | 0 | -4 | 0 | 1 |
| 1 | 1 | 0 | 1 | -3 | 1 | 0 |
| 1 | 1 | 1 | 0 | -2 | 1 | 0 |
| 1 | 1 | 1 | 1 | -1 | 1 | 0 |

El rango verde es $0,1,2,3,4$ (filas 0–4) y $-3,-2,-1$ (filas 13–15): en total 8 de las 16 combinaciones.
@end
@paso Led verde $LV$
**$\mathrm{LV}=\Sigma(0\text{-}4, 13\text{-}15)$**. Simplificada: $\mathrm{LV}=\overline{T_{3}}\,\overline{T_{2}} + \overline{T_{3}}\,\overline{T_{1}}\,\overline{T_{0}} + T_{3}\,T_{2}\,T_{0} + T_{3}\,T_{2}\,T_{1}$. Circuito de dos niveles: 1 AND de 2 entradas y 3 AND de 3 entradas, 1 OR de 4 entradas, 4 inversores ($T_{0}$, $T_{1}$, $T_{2}$, $T_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p414.LV", "n": 4, "names": ["T3", "T2", "T1", "T0"], "title": "LV", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Led rojo $LR$
**$\mathrm{LR}=\Sigma(5\text{-}12)$**. Simplificada: $\mathrm{LR}=\overline{T_{3}}\,T_{2}\,T_{0} + \overline{T_{3}}\,T_{2}\,T_{1} + T_{3}\,\overline{T_{2}} + T_{3}\,\overline{T_{1}}\,\overline{T_{0}}$. Circuito de dos niveles: 1 AND de 2 entradas y 3 AND de 3 entradas, 1 OR de 4 entradas, 4 inversores ($T_{0}$, $T_{1}$, $T_{2}$, $T_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p414.LR", "n": 4, "names": ["T3", "T2", "T1", "T0"], "title": "LR", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las dos funciones del libro son correctas y mínimas. Pero hay un atajo: $LR=\overline{LV}$ (comprobado por código), así que basta **un inversor** detrás de $LV$ en vez de otros 4 AND y una OR.
@end
@end

@ej lb4-15|Cambio de pesetas a euros|Libro · Cap. 4 · P4.15|comb,karnaugh|lb4.p415
@enun
Una máquina acepta por una única ranura monedas de 5, 10, 25 y 50 ptas y devuelve su valor en euros con monedas de 1, 2, 5, 10 y 20 céntimos (con redondeo). Cuatro señales $P_5,P_{10},P_{25},P_{50}$ indican qué moneda se ha introducido.
@end
@antes
**Conversión:** al cambio oficial de $166{,}386$ ptas por euro, 5 ptas son $3{,}005$ cént. (3), 10 ptas son 6, 25 ptas son 15 y 50 ptas son 30 (comprobado por código). Cada importe se reparte con las monedas disponibles: $3=2+1$, $6=5+1$, $15=10+5$, $30=20+10$.
@end
@paso Qué filas son válidas
Como la ranura es única, solo puede haber **una** moneda a la vez: son válidas la fila 0 (ninguna) y las filas con un único 1 (1, 2, 4 y 8). Las otras 11 filas son indiferentes.
@end
@paso Tabla de verdad
| P5 | P10 | P25 | P50 | E1 | E2 | E5 | E10 | E20 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 0 | 1 | 1 | × | × | × | × | × |
| 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | × | × | × | × | × |
| 0 | 1 | 1 | 0 | × | × | × | × | × |
| 0 | 1 | 1 | 1 | × | × | × | × | × |
| 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | × | × | × | × | × |
| 1 | 0 | 1 | 0 | × | × | × | × | × |
| 1 | 0 | 1 | 1 | × | × | × | × | × |
| 1 | 1 | 0 | 0 | × | × | × | × | × |
| 1 | 1 | 0 | 1 | × | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × | × |

Ejemplos: fila 2 (25 ptas): 15 cént. $=10+5$, salidas $00110$. Fila 8 (5 ptas): 3 cént. $=2+1$, salidas $11000$.
@end
@paso Salida $E1$
**$E_{1}=\Sigma(4, 8)$** con indiferentes $d(3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)$. Simplificada: $E_{1}=P_{10} + P_{5}$. Circuito de dos niveles: 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p415.E1", "n": 4, "names": ["P5", "P10", "P25", "P50"], "title": "E1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $E2$
**$E_{2}=\Sigma(8)$** con indiferentes $d(3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)$. Simplificada: $E_{2}=P_{5}$. $E_{2}$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p415.E2", "n": 4, "names": ["P5", "P10", "P25", "P50"], "title": "E2", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $E5$
**$E_{5}=\Sigma(2, 4)$** con indiferentes $d(3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)$. Simplificada: $E_{5}=P_{25} + P_{10}$. Circuito de dos niveles: 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p415.E5", "n": 4, "names": ["P5", "P10", "P25", "P50"], "title": "E5", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $E10$
**$E_{10}=\Sigma(1, 2)$** con indiferentes $d(3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)$. Simplificada: $E_{10}=P_{50} + P_{25}$. Circuito de dos niveles: 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p415.E10", "n": 4, "names": ["P5", "P10", "P25", "P50"], "title": "E10", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $E20$
**$E_{20}=\Sigma(1)$** con indiferentes $d(3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)$. Simplificada: $E_{20}=P_{50}$. $E_{20}$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p415.E20", "n": 4, "names": ["P5", "P10", "P25", "P50"], "title": "E20", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Con tantas indiferentes todo se reduce a cables y OR de dos entradas: $E_1=P_5+P_{10}$, $E_2=P_5$, $E_5=P_{25}+P_{10}$, $E_{10}=P_{50}+P_{25}$, $E_{20}=P_{50}$. Coinciden con el libro y son mínimas. Si se quisiera permitir varias monedas a la vez, habría que rehacer la tabla (el propio libro lo deja como ejercicio).
@end
@end

@ej lb4-16|Semáforos de una rotonda|Libro · Cap. 4 · P4.16|comb,karnaugh|lb4.p416
@enun
Una rotonda tiene cuatro calles de entrada y cuatro de salida. Por la entrada $A$ llegan 5 coches/min, por $B$ 15, por $C$ 25 y por $D$ 30. Cuatro sensores indican por qué calles circulan coches. Las salidas $S_A,S_B,S_C,S_D$ pueden recoger 5, 10, 20 y 40 coches/min. Como mucho hay coches en dos calles de entrada a la vez. Activa los semáforos de salida para que salgan tantos coches como entran.
@end
@antes
**Es un convertidor de código:** divide el flujo total entre 5 y escríbelo en binario con pesos $1,2,4,8$ (que corresponden a 5, 10, 20 y 40). Por ejemplo, $35=7\cdot5$, y $7=0111$: se abren las salidas de 5, 10 y 20.
@end
@paso Qué filas son válidas
Como mucho dos calles activas: son indiferentes las filas con tres o cuatro unos: 7, 11, 13, 14 y 15. El libro avisa de que poner $\times$ aquí es algo arriesgado y que también se podrían fijar a 0 o a 1.
@end
@paso Tabla de verdad
| A | B | C | D | SA | SB | SC | SD |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 |
| 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | × | × | × | × |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | × | × | × | × |
| 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | × | × | × | × |
| 1 | 1 | 1 | 0 | × | × | × | × |
| 1 | 1 | 1 | 1 | × | × | × | × |

Ejemplos: fila 2 (entran 25): se abren $S_A$ y $S_C$ ($5+20$). Fila 6 (entran 40): solo $S_D$. Fila 9 (35): $S_A,S_B,S_C$. Fila 3 (55): $S_A,S_B,S_D$ ($5+10+40$).
@end
@paso Salida $SA$
**$\mathrm{SA}=\Sigma(2\text{-}5, 8, 9)$** con indiferentes $d(7, 11, 13, 14, 15)$. Simplificada: $\mathrm{SA}=\overline{A}\,\overline{B}\,C + \overline{A}\,B\,\overline{C} + A\,\overline{B}\,\overline{C}$. Circuito de dos niveles: 3 AND de 3 entradas, 1 OR de 3 entradas, 3 inversores ($A$, $B$, $C$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p416.SA", "n": 4, "names": ["A", "B", "C", "D"], "title": "SA", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $SB$
**$\mathrm{SB}=\Sigma(1, 3, 4, 9, 10)$** con indiferentes $d(7, 11, 13, 14, 15)$. Simplificada: $\mathrm{SB}=\overline{B}\,D + \overline{A}\,B\,\overline{C}\,\overline{D} + A\,C$. Circuito de dos niveles: 2 AND de 2 entradas y 1 AND de 4 entradas, 1 OR de 3 entradas, 4 inversores ($A$, $B$, $C$, $D$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p416.SB", "n": 4, "names": ["A", "B", "C", "D"], "title": "SB", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $SC$
**$\mathrm{SC}=\Sigma(1, 2, 9, 10, 12)$** con indiferentes $d(7, 11, 13, 14, 15)$. Simplificada: $\mathrm{SC}=\overline{B}\,\overline{C}\,D + \overline{B}\,C\,\overline{D} + A\,B$. Circuito de dos niveles: 1 AND de 2 entradas y 2 AND de 3 entradas, 1 OR de 3 entradas, 3 inversores ($B$, $C$, $D$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p416.SC", "n": 4, "names": ["A", "B", "C", "D"], "title": "SC", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Salida $SD$
**$\mathrm{SD}=\Sigma(3, 5, 6)$** con indiferentes $d(7, 11, 13, 14, 15)$. Simplificada: $\mathrm{SD}=C\,D + B\,D + B\,C$. Circuito de dos niveles: 3 AND de 2 entradas, 1 OR de 3 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p416.SD", "n": 4, "names": ["A", "B", "C", "D"], "title": "SD", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@res
Las cuatro funciones del libro son correctas y mínimas. Se comprueba por código que los semáforos abiertos suman exactamente el flujo de entrada en las 11 filas válidas. $S_D=CD+BD+BC$ es una función **mayoría** de tres variables.
@end
@end

@ej lb4-17|Transcodificador de binario a dos dígitos BCD|Libro · Cap. 4 · P4.17|comb,karnaugh,bcd|lb4.p417
@enun
Implementa un transcodificador que pase un número en binario puro $E_3E_2E_1E_0$ (0 a 15) a dos dígitos BCD: decenas $A_3A_2A_1A_0$ y unidades $B_3B_2B_1B_0$.
@end
@antes
**Basta pasar a decimal y escribir en BCD.** Hasta 9 solo hay unidades. De 10 a 15 hay una decena (1) y las unidades son el número menos 10. Las tres cifras más significativas de las decenas valen siempre 0.
@end
@paso Tabla de verdad
| E3 | E2 | E1 | E0 | A3 | A2 | A1 | A0 | B3 | B2 | B1 | B0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 |

Ejemplos: $9\to0000\,1001$; $10\to0001\,0000$; $15\to0001\,0101$.
@end
@paso Decenas: $A_3=A_2=A_1=0$
Para 4 bits de entrada la decena solo puede ser 0 o 1, así que esas tres salidas son **la constante 0** (se pueden conectar a masa; el libro las deja por coherencia con el BCD).
@end
@paso Decenas: $A_0$
**$A_{0}=\Sigma(10\text{-}15)$**. Simplificada: $A_{0}=E_{3}\,E_{1} + E_{3}\,E_{2}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas. Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p417.A0", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "A0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Unidades: $B_3$
**$B_{3}=\Sigma(8, 9)$**. Simplificada: $B_{3}=E_{3}\,\overline{E_{2}}\,\overline{E_{1}}$. Circuito de dos niveles: 1 AND de 3 entradas, 2 inversores ($E_{1}$, $E_{2}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p417.B3", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "B3", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Unidades: $B_2$
**$B_{2}=\Sigma(4\text{-}7, 14, 15)$**. Simplificada: $B_{2}=\overline{E_{3}}\,E_{2} + E_{2}\,E_{1}$. Circuito de dos niveles: 2 AND de 2 entradas, 1 OR de 2 entradas, 1 inversor ($E_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p417.B2", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "B2", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Unidades: $B_1$
**$B_{1}=\Sigma(2, 3, 6, 7, 12, 13)$**. Simplificada: $B_{1}=\overline{E_{3}}\,E_{1} + E_{3}\,E_{2}\,\overline{E_{1}}$. Circuito de dos niveles: 1 AND de 2 entradas y 1 AND de 3 entradas, 1 OR de 2 entradas, 2 inversores ($E_{1}$, $E_{3}$). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p417.B1", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "B1", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}
@end
@paso Unidades: $B_0$
**$B_{0}=\Sigma(1, 3, 5, 7, 9, 11, 13, 15)$**. Simplificada: $B_{0}=E_{0}$. $B_{0}$ es un simple cable (o una sola variable). Coincide en coste con la solución del libro (misma expresión).
@fig kmap {"key": "lb4.p417.B0", "n": 4, "names": ["E3", "E2", "E1", "E0"], "title": "B0", "cap": "Casillas con el número de minitérmino; cada lazo da un producto."}

El bit menos significativo no cambia: $B_0=E_0$, un cable.
@end
@res
Se comprueba que $10\cdot(\text{decenas})+\text{unidades}$ vale la entrada en las 16 filas. Las soluciones del libro son correctas y mínimas salvo una errata en $B_2$.

@box ojo | Errata en el libro ($B_2$)
En la fórmula del libro $B_2=\bar E_3E_2+E_2E_0$. El segundo término debe ser $E_2E_1$: con $E_2E_0$ la fila 13 ($1101$) daría $B_2=1$ (el 13 es $0001\,0011$, y $B_2=0$) y la fila 14 ($1110$, que es $0001\,0100$) daría 0 en vez de 1. Se ha comprobado por código.
@end
@end
@end

