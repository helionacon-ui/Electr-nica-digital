%% id=libro3
%% group=ejer
%% n=3.3
%% title=Libro de problemas · Capítulo 3 · Mapas de Karnaugh
%% short=Libro · Cap. 3 Karnaugh
%% sub=Dos problemas, con 28 mapas para dibujar y 58 funciones para simplificar: con unos, con indiferentes y como producto de sumas.

@box idea | Cómo se usa esta sección
Son los problemas resueltos del capítulo 3 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Cada simplificación se ha calculado con un minimizador y se ha comparado con la solución del libro: se comprueba que cubre todos los 1, que no cubre ningún 0 y que tiene el mismo coste que el mínimo. Los mapas de esta guía ponen $AB$ en las filas y $CD$ en las columnas. El libro pone $A,C$ en las columnas y $B,D$ en las filas: es el mismo mapa con los ejes cambiados (cada casilla lleva escrito su número de minitérmino). La teoría está en [[t04|el tema 4]].
@end

@ej lb3-1|Dibujar 28 mapas de Karnaugh a partir de formas normales|Libro · Cap. 3 · P3.1|comb,karnaugh|lb3.p31
@enun
Dibuja el mapa de Karnaugh de 28 funciones de cuatro variables, dadas como suma de minitérminos $\Sigma$ o como producto de maxitérminos $\Pi$, algunas con combinaciones indiferentes.
@end
@antes
**Cómo se coloca cada minitérmino:** el número $m=8A+4B+2C+D$. Las filas y las columnas del mapa siguen el orden de Gray ($00,01,11,10$), de modo que dos casillas vecinas se diferencian en una sola variable. En un $\Sigma$ se escribe 1 en las casillas de la lista; en un $\Pi$ la lista son los **ceros** y el resto son unos; las $X$ de $d(\ldots)$ van aparte.
@end
@paso Funciones 1 a 10 (sumatorios sin indiferentes)
$f_{1}=\Sigma(0, 2, 4, 6, 8, 10)$
@fig kmap {"key": "lb3.p31.f1", "n": 4, "names": ["A", "B", "C", "D"], "title": "f1", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{2}=\Sigma(4, 8\text{-}12, 15)$
@fig kmap {"key": "lb3.p31.f2", "n": 4, "names": ["A", "B", "C", "D"], "title": "f2", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{3}=\Sigma(1, 4, 8, 9)$
@fig kmap {"key": "lb3.p31.f3", "n": 4, "names": ["A", "B", "C", "D"], "title": "f3", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{4}=\Sigma(2, 3, 7, 8, 10)$
@fig kmap {"key": "lb3.p31.f4", "n": 4, "names": ["A", "B", "C", "D"], "title": "f4", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{5}=\Sigma(1, 5, 9, 13)$
@fig kmap {"key": "lb3.p31.f5", "n": 4, "names": ["A", "B", "C", "D"], "title": "f5", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{6}=\Sigma(8, 10, 12, 14)$
@fig kmap {"key": "lb3.p31.f6", "n": 4, "names": ["A", "B", "C", "D"], "title": "f6", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{7}=\Sigma(1, 13\text{-}15)$
@fig kmap {"key": "lb3.p31.f7", "n": 4, "names": ["A", "B", "C", "D"], "title": "f7", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{8}=\Sigma(1\text{-}9, 12, 15)$
@fig kmap {"key": "lb3.p31.f8", "n": 4, "names": ["A", "B", "C", "D"], "title": "f8", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{9}=\Sigma(1, 3, 5, 7, 9, 11, 13, 15)$
@fig kmap {"key": "lb3.p31.f9", "n": 4, "names": ["A", "B", "C", "D"], "title": "f9", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
$f_{10}=\Sigma(0, 2, 4, 6, 8, 10, 12, 14)$
@fig kmap {"key": "lb3.p31.f10", "n": 4, "names": ["A", "B", "C", "D"], "title": "f10", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$."}
@end
@paso Funciones 11 a 14 (sumatorios con indiferentes)
$f_{11}=\Sigma(1, 8, 10, 15)$ con indiferentes $d(0, 2, 6, 7)$
@fig kmap {"key": "lb3.p31.f11", "n": 4, "names": ["A", "B", "C", "D"], "title": "f11", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$; × indiferente."}
$f_{12}=\Sigma(3, 4, 13, 14)$ con indiferentes $d(7\text{-}12)$
@fig kmap {"key": "lb3.p31.f12", "n": 4, "names": ["A", "B", "C", "D"], "title": "f12", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$; × indiferente."}
$f_{13}=\Sigma(1, 2, 5, 12)$ con indiferentes $d(0, 4)$
@fig kmap {"key": "lb3.p31.f13", "n": 4, "names": ["A", "B", "C", "D"], "title": "f13", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$; × indiferente."}
$f_{14}=\Sigma(0\text{-}4, 8\text{-}12)$ con indiferentes $d(5\text{-}7)$
@fig kmap {"key": "lb3.p31.f14", "n": 4, "names": ["A", "B", "C", "D"], "title": "f14", "groups": false, "cap": "Los 1 son las casillas de $\\Sigma$; × indiferente."}
@end
@paso Funciones 15 a 24 (productos de maxitérminos)
$f_{15}=\Pi(0, 4, 6, 10)$
@fig kmap {"key": "lb3.p31.f15", "n": 4, "names": ["A", "B", "C", "D"], "title": "f15", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{16}=\Pi(0, 2, 4, 5, 7, 11)$
@fig kmap {"key": "lb3.p31.f16", "n": 4, "names": ["A", "B", "C", "D"], "title": "f16", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{17}=\Pi(13\text{-}15)$
@fig kmap {"key": "lb3.p31.f17", "n": 4, "names": ["A", "B", "C", "D"], "title": "f17", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{18}=\Pi(1, 4, 8, 9, 14, 15)$
@fig kmap {"key": "lb3.p31.f18", "n": 4, "names": ["A", "B", "C", "D"], "title": "f18", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{19}=\Pi(0, 2, 4, 10\text{-}15)$
@fig kmap {"key": "lb3.p31.f19", "n": 4, "names": ["A", "B", "C", "D"], "title": "f19", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{20}=\Pi(2, 3, 6, 7, 10, 11, 14, 15)$
@fig kmap {"key": "lb3.p31.f20", "n": 4, "names": ["A", "B", "C", "D"], "title": "f20", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{21}=\Pi(2, 6, 7, 11, 15)$
@fig kmap {"key": "lb3.p31.f21", "n": 4, "names": ["A", "B", "C", "D"], "title": "f21", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{22}=\Pi(0\text{-}7)$
@fig kmap {"key": "lb3.p31.f22", "n": 4, "names": ["A", "B", "C", "D"], "title": "f22", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{23}=\Pi(0\text{-}3, 8\text{-}11)$
@fig kmap {"key": "lb3.p31.f23", "n": 4, "names": ["A", "B", "C", "D"], "title": "f23", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
$f_{24}=\Pi(0, 1, 4, 5, 8, 9, 12, 13)$
@fig kmap {"key": "lb3.p31.f24", "n": 4, "names": ["A", "B", "C", "D"], "title": "f24", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea."}
@end
@paso Funciones 25 a 28 (productos con indiferentes)
$f_{25}=\Pi(3, 4, 9, 10)$ con indiferentes $d(7, 8, 13, 14)$
@fig kmap {"key": "lb3.p31.f25", "n": 4, "names": ["A", "B", "C", "D"], "title": "f25", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea; × indiferente."}
$f_{26}=\Pi(4\text{-}9, 13\text{-}15)$ con indiferentes $d(0\text{-}2)$
@fig kmap {"key": "lb3.p31.f26", "n": 4, "names": ["A", "B", "C", "D"], "title": "f26", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea; × indiferente."}
$f_{27}=\Pi(4, 5, 14, 15)$ con indiferentes $d(0\text{-}3, 7\text{-}9)$
@fig kmap {"key": "lb3.p31.f27", "n": 4, "names": ["A", "B", "C", "D"], "title": "f27", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea; × indiferente."}
$f_{28}=\Pi(1, 3, 5, 13)$ con indiferentes $d(7\text{-}12)$
@fig kmap {"key": "lb3.p31.f28", "n": 4, "names": ["A", "B", "C", "D"], "title": "f28", "groups": false, "cap": "Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea; × indiferente."}
@end
@res
Los 28 mapas se han generado de la lista, y se ha comprobado que los unos, los ceros y las indiferentes de cada función suman las 16 casillas. Los mapas impresos en el libro que se han contrastado coinciden.
@end
@end

@ej lb3-2|Simplificar 22 mapas de Karnaugh con unos|Libro · Cap. 3 · P3.2 (f1–f22)|comb,karnaugh|lb3.p32a
@enun
Simplifica 22 funciones de cuatro variables dadas por su mapa de Karnaugh (sin indiferentes) y escribe la suma de productos mínima.
@end
@antes
**Método:** rodea todos los 1 con el menor número de lazos y del mayor tamaño posible (de 1, 2, 4, 8 o 16 casillas). Los lazos pueden solaparse y pueden dar la vuelta al mapa. Cada lazo da un producto con las variables que **no cambian** dentro de él.
@end
@paso Funciones 1 a 6
**$f_{1}$**: $f_{1}=\overline{A}\overline{B} + \overline{A}D + C + A\overline{D}$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f1", "n": 4, "names": ["A", "B", "C", "D"], "title": "f1", "cap": "Se rodean los 1."}

**$f_{2}$**: $f_{2}=\overline{A}B + B\overline{C} + A\overline{B}$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f2", "n": 4, "names": ["A", "B", "C", "D"], "title": "f2", "cap": "Se rodean los 1."}

**$f_{3}$**: $f_{3}=\overline{A}\overline{B}\overline{C} + \overline{A}CD + AB$
@fig kmap {"key": "lb3.p32.f3", "n": 4, "names": ["A", "B", "C", "D"], "title": "f3", "cap": "Se rodean los 1."}

**$f_{4}$**: $f_{4}=\overline{A}\overline{B} + B\overline{C}D$
@fig kmap {"key": "lb3.p32.f4", "n": 4, "names": ["A", "B", "C", "D"], "title": "f4", "cap": "Se rodean los 1."}

**$f_{5}$**: $f_{5}=\overline{A}B + A\overline{B}$
@fig kmap {"key": "lb3.p32.f5", "n": 4, "names": ["A", "B", "C", "D"], "title": "f5", "cap": "Se rodean los 1."}

**$f_{6}$**: $f_{6}=\overline{A}\overline{B}C + C\overline{D} + B\overline{C} + A\overline{D}$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f6", "n": 4, "names": ["A", "B", "C", "D"], "title": "f6", "cap": "Se rodean los 1."}
@end
@paso Funciones 7 a 12
**$f_{7}$**: $f_{7}=\overline{A}BC + A\overline{C} + A\overline{D}$
@fig kmap {"key": "lb3.p32.f7", "n": 4, "names": ["A", "B", "C", "D"], "title": "f7", "cap": "Se rodean los 1."}

**$f_{8}$**: $f_{8}=\overline{A}\overline{B}\overline{C} + \overline{A}\overline{B}D + \overline{A}BC + A\overline{D}$ Hay 4 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f8", "n": 4, "names": ["A", "B", "C", "D"], "title": "f8", "cap": "Se rodean los 1."}

**$f_{9}$**: $f_{9}=\overline{C}D + \overline{A}BD + BC\overline{D} + A\overline{B}\overline{D}$ Hay 4 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f9", "n": 4, "names": ["A", "B", "C", "D"], "title": "f9", "cap": "Se rodean los 1."}

**$f_{10}$**: $f_{10}=\overline{A}\overline{C}\overline{D} + B\overline{C}D + A\overline{B}\overline{D} + ABC$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f10", "n": 4, "names": ["A", "B", "C", "D"], "title": "f10", "cap": "Se rodean los 1."}

**$f_{11}$**: $f_{11}=\overline{A}\overline{B}\overline{D} + \overline{B}CD + B\overline{C}\overline{D} + ABC$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f11", "n": 4, "names": ["A", "B", "C", "D"], "title": "f11", "cap": "Se rodean los 1."}

**$f_{12}$**: $f_{12}=B\overline{C}D + BC\overline{D} + A\overline{C}\overline{D} + ACD$
@fig kmap {"key": "lb3.p32.f12", "n": 4, "names": ["A", "B", "C", "D"], "title": "f12", "cap": "Se rodean los 1."}
@end
@paso Funciones 13 a 18
**$f_{13}$**: $f_{13}=\overline{A}\overline{C}D + B\overline{D} + A\overline{B}D$
@fig kmap {"key": "lb3.p32.f13", "n": 4, "names": ["A", "B", "C", "D"], "title": "f13", "cap": "Se rodean los 1."}

**$f_{14}$**: $f_{14}=\overline{A}CD + \overline{A}BD + \overline{A}BC + AC\overline{D} + AB\overline{C}$ Hay 6 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f14", "n": 4, "names": ["A", "B", "C", "D"], "title": "f14", "cap": "Se rodean los 1."}

**$f_{15}$**: $f_{15}=B\overline{C}D + \overline{A}BC\overline{D} + A\overline{B}\overline{C} + ABD$
@fig kmap {"key": "lb3.p32.f15", "n": 4, "names": ["A", "B", "C", "D"], "title": "f15", "cap": "Se rodean los 1."}

**$f_{16}$**: $f_{16}=\overline{A}\overline{B}\overline{D} + CD + B\overline{C} + A\overline{C} + AB$ El libro da $\bar C\bar D+B\bar C+AB+AD+CD+\bar A\bar BC$: es correcta, pero tiene 6 términos y 13 literales. La mínima tiene 5 términos y 11 literales (se ha comprobado que cubre exactamente los mismos 1).
@fig kmap {"key": "lb3.p32.f16", "n": 4, "names": ["A", "B", "C", "D"], "title": "f16", "cap": "Se rodean los 1."}

**$f_{17}$**: $f_{17}=B\overline{C}D + \overline{A}BC\overline{D} + A\overline{B}\overline{C} + ABD$
@fig kmap {"key": "lb3.p32.f17", "n": 4, "names": ["A", "B", "C", "D"], "title": "f17", "cap": "Se rodean los 1."}

**$f_{18}$**: $f_{18}=D + C + B + A$
@fig kmap {"key": "lb3.p32.f18", "n": 4, "names": ["A", "B", "C", "D"], "title": "f18", "cap": "Se rodean los 1."}
@end
@paso Funciones 19 a 22
**$f_{19}$**: $f_{19}=\overline{A}\overline{B} + \overline{C}\overline{D} + BD + AC$ Hay 6 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f19", "n": 4, "names": ["A", "B", "C", "D"], "title": "f19", "cap": "Se rodean los 1."}

**$f_{20}$**: $f_{20}=\overline{A}\overline{B} + \overline{C}D + BC + A\overline{D}$ Hay 6 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f20", "n": 4, "names": ["A", "B", "C", "D"], "title": "f20", "cap": "Se rodean los 1."}

**$f_{21}$**: $f_{21}=1$
@fig kmap {"key": "lb3.p32.f21", "n": 4, "names": ["A", "B", "C", "D"], "title": "f21", "cap": "Se rodean los 1."}

**$f_{22}$**: $f_{22}=\overline{A}\overline{D} + B\overline{D} + AD$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f22", "n": 4, "names": ["A", "B", "C", "D"], "title": "f22", "cap": "Se rodean los 1."}
@end
@res
Las 22 soluciones del libro cubren exactamente los 1 y tienen el coste mínimo. Las funciones $f_{19}$ y $f_{20}$ tienen varias soluciones equivalentes (se han contado por código). $f_{21}$ vale 1 siempre y $f_{18}=A+B+C+D$ vale 1 salvo en $ABCD=0000$.

@box ojo | Nota sobre $f_{16}$
La solución del libro para $f_{16}$ es correcta pero **no es mínima**: usa 6 términos y existe una de 5 (ver más arriba).
@end
@end
@end

@ej lb3-3|Simplificar 16 mapas con combinaciones indiferentes|Libro · Cap. 3 · P3.2 (f23–f38)|comb,karnaugh|lb3.p32b
@enun
Simplifica 16 funciones de cuatro variables con casillas indiferentes (×) y escribe la suma de productos mínima.
@end
@antes
**Las indiferentes:** una × puede valer 0 o 1 según convenga. Se usa para hacer lazos más grandes o menos lazos, pero **nunca se forma un lazo solo con ×** (no haría falta).
@end
@paso Funciones 23 a 28
**$f_{23}$**: $f_{23}=\overline{B}\overline{C}\overline{D} + AB\overline{C}$
@fig kmap {"key": "lb3.p32.f23", "n": 4, "names": ["A", "B", "C", "D"], "title": "f23", "cap": "Se rodean los 1 usando las ×."}

**$f_{24}$**: $f_{24}=C\overline{D} + AB\overline{C}$
@fig kmap {"key": "lb3.p32.f24", "n": 4, "names": ["A", "B", "C", "D"], "title": "f24", "cap": "Se rodean los 1 usando las ×."}

**$f_{25}$**: $f_{25}=AC$
@fig kmap {"key": "lb3.p32.f25", "n": 4, "names": ["A", "B", "C", "D"], "title": "f25", "cap": "Se rodean los 1 usando las ×."}

**$f_{26}$**: $f_{26}=\overline{D} + B + A$
@fig kmap {"key": "lb3.p32.f26", "n": 4, "names": ["A", "B", "C", "D"], "title": "f26", "cap": "Se rodean los 1 usando las ×."}

**$f_{27}$**: $f_{27}=B\overline{C} + A\overline{C} + A\overline{D} + AB$
@fig kmap {"key": "lb3.p32.f27", "n": 4, "names": ["A", "B", "C", "D"], "title": "f27", "cap": "Se rodean los 1 usando las ×."}

**$f_{28}$**: $f_{28}=\overline{A}C + \overline{B}C + A\overline{C}$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f28", "n": 4, "names": ["A", "B", "C", "D"], "title": "f28", "cap": "Se rodean los 1 usando las ×."}
@end
@paso Funciones 29 a 34
**$f_{29}$**: $f_{29}=C + B$
@fig kmap {"key": "lb3.p32.f29", "n": 4, "names": ["A", "B", "C", "D"], "title": "f29", "cap": "Se rodean los 1 usando las ×."}

**$f_{30}$**: $f_{30}=\overline{A}\overline{C}D + ACD + AB\overline{D}$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f30", "n": 4, "names": ["A", "B", "C", "D"], "title": "f30", "cap": "Se rodean los 1 usando las ×."}

**$f_{31}$**: $f_{31}=\overline{D} + B + AC$
@fig kmap {"key": "lb3.p32.f31", "n": 4, "names": ["A", "B", "C", "D"], "title": "f31", "cap": "Se rodean los 1 usando las ×."}

**$f_{32}$**: $f_{32}=B\overline{C}\overline{D} + BCD + A\overline{D} + AB$
@fig kmap {"key": "lb3.p32.f32", "n": 4, "names": ["A", "B", "C", "D"], "title": "f32", "cap": "Se rodean los 1 usando las ×."}

**$f_{33}$**: $f_{33}=A\overline{B}\overline{D} + ABC$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f33", "n": 4, "names": ["A", "B", "C", "D"], "title": "f33", "cap": "Se rodean los 1 usando las ×."}

**$f_{34}$**: $f_{34}=1$
@fig kmap {"key": "lb3.p32.f34", "n": 4, "names": ["A", "B", "C", "D"], "title": "f34", "cap": "Se rodean los 1 usando las ×."}
@end
@paso Funciones 35 a 38
**$f_{35}$**: $f_{35}=\overline{B}CD + B\overline{C} + AC$
@fig kmap {"key": "lb3.p32.f35", "n": 4, "names": ["A", "B", "C", "D"], "title": "f35", "cap": "Se rodean los 1 usando las ×."}

**$f_{36}$**: $f_{36}=1$
@fig kmap {"key": "lb3.p32.f36", "n": 4, "names": ["A", "B", "C", "D"], "title": "f36", "cap": "Se rodean los 1 usando las ×."}

**$f_{37}$**: $f_{37}=1$
@fig kmap {"key": "lb3.p32.f37", "n": 4, "names": ["A", "B", "C", "D"], "title": "f37", "cap": "Se rodean los 1 usando las ×."}

**$f_{38}$**: $f_{38}=D$
@fig kmap {"key": "lb3.p32.f38", "n": 4, "names": ["A", "B", "C", "D"], "title": "f38", "cap": "Se rodean los 1 usando las ×."}
@end
@res
Las 16 soluciones del libro son válidas y mínimas. Casos curiosos: $f_{34}$ y $f_{37}$ valen 1 (todas las × y unos forman un único lazo de 16); $f_{36}$ solo tiene indiferentes y vale cualquier cosa (0, 1 o $AB+C$); $f_{38}=D$ usa las × de las filas con $D=1$.
@end
@end

@ej lb3-4|Simplificar 20 mapas como producto de sumas|Libro · Cap. 3 · P3.2 (f39–f58)|comb,karnaugh|lb3.p32c
@enun
Simplifica 20 funciones de cuatro variables, representadas por los **ceros** de su mapa, y escribe el producto de sumas mínimo.
@end
@antes
**Producto de sumas (POS):** rodea los 0 como si fueran unos, lee cada lazo como un producto y niega el resultado con De Morgan. Cada lazo se convierte en una **suma** en la que cada variable aparece **negada si vale 1** en el lazo y sin negar si vale 0.
@end
@paso Funciones 39 a 44
**$f_{39}$**: $f_{39}=(A + B + \overline{C} + \overline{D})(\overline{B} + C + \overline{D})(\overline{A} + B + D)(\overline{A} + C + D)$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f39", "n": 4, "names": ["A", "B", "C", "D"], "title": "f39", "cap": "Mapa de $\\overline{f_{39}}$: los 1 son los ceros de $f_{39}$. Se rodean para leer el producto de sumas."}

**$f_{40}$**: $f_{40}=0$
@fig kmap {"key": "lb3.p32.f40", "n": 4, "names": ["A", "B", "C", "D"], "title": "f40", "cap": "Mapa de $\\overline{f_{40}}$: los 1 son los ceros de $f_{40}$. Se rodean para leer el producto de sumas."}

**$f_{41}$**: $f_{41}=(A + B + D)(A + \overline{C} + \overline{D})(\overline{B} + C + D)(\overline{A} + \overline{B} + \overline{D})$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f41", "n": 4, "names": ["A", "B", "C", "D"], "title": "f41", "cap": "Mapa de $\\overline{f_{41}}$: los 1 son los ceros de $f_{41}$. Se rodean para leer el producto de sumas."}

**$f_{42}$**: $f_{42}=(A + B + C)(A + B + \overline{D})(A + \overline{B} + \overline{C} + D)(\overline{A} + B + D)(\overline{A} + \overline{C} + \overline{D})(\overline{A} + \overline{B} + C)$ En el mapa del libro hay un 0 aislado en la casilla $ABCD=0110$ que no tiene lazo ni factor en la solución impresa: $(\bar A+B+D)(\bar A+\bar B+C)(\bar A+\bar B+\bar D)(B+\bar C+\bar D)(A+B+C)$. Si ese 0 es real, la solución del libro **no** lo cumple (valdría 1 en esa casilla). Si es una errata del mapa, la solución del libro es correcta. Aquí se resuelve el mapa tal como se ve.
@fig kmap {"key": "lb3.p32.f42", "n": 4, "names": ["A", "B", "C", "D"], "title": "f42", "cap": "Mapa de $\\overline{f_{42}}$: los 1 son los ceros de $f_{42}$. Se rodean para leer el producto de sumas."}

**$f_{43}$**: $f_{43}=(A + \overline{B})(\overline{B} + C)(\overline{A} + B + D)(\overline{A} + \overline{C} + \overline{D})$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f43", "n": 4, "names": ["A", "B", "C", "D"], "title": "f43", "cap": "Mapa de $\\overline{f_{43}}$: los 1 son los ceros de $f_{43}$. Se rodean para leer el producto de sumas."}

**$f_{44}$**: $f_{44}=(A + D)(\overline{C} + D)(\overline{B} + \overline{D})(\overline{A} + B)$ Hay 6 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f44", "n": 4, "names": ["A", "B", "C", "D"], "title": "f44", "cap": "Mapa de $\\overline{f_{44}}$: los 1 son los ceros de $f_{44}$. Se rodean para leer el producto de sumas."}
@end
@paso Funciones 45 a 50
**$f_{45}$**: $f_{45}=(A + B + C)(A + \overline{B} + \overline{C} + D)(\overline{A} + B + \overline{C})(\overline{A} + \overline{B} + C + D)$
@fig kmap {"key": "lb3.p32.f45", "n": 4, "names": ["A", "B", "C", "D"], "title": "f45", "cap": "Mapa de $\\overline{f_{45}}$: los 1 son los ceros de $f_{45}$. Se rodean para leer el producto de sumas."}

**$f_{46}$**: $f_{46}=(A + B + C)(A + \overline{C} + D)(\overline{A} + B + \overline{D})(\overline{A} + \overline{B} + \overline{C})$ Hay 2 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f46", "n": 4, "names": ["A", "B", "C", "D"], "title": "f46", "cap": "Mapa de $\\overline{f_{46}}$: los 1 son los ceros de $f_{46}$. Se rodean para leer el producto de sumas."}

**$f_{47}$**: $f_{47}=(A + B)(A + D)(B + \overline{C})(\overline{C} + \overline{D})(\overline{A} + \overline{B} + C)$ El libro da $(A+\bar C)(A+B)(B+\bar C)(\bar B+C+D)(\bar A+\bar B+\bar D)$: es correcta, con 5 factores y 12 literales. La mínima tiene también 5 factores y un literal menos.
@fig kmap {"key": "lb3.p32.f47", "n": 4, "names": ["A", "B", "C", "D"], "title": "f47", "cap": "Mapa de $\\overline{f_{47}}$: los 1 son los ceros de $f_{47}$. Se rodean para leer el producto de sumas."}

**$f_{48}$**: $f_{48}=(A)(B)(C)(D)$
@fig kmap {"key": "lb3.p32.f48", "n": 4, "names": ["A", "B", "C", "D"], "title": "f48", "cap": "Mapa de $\\overline{f_{48}}$: los 1 son los ceros de $f_{48}$. Se rodean para leer el producto de sumas."}

**$f_{49}$**: $f_{49}=(A + \overline{B} + C)$
@fig kmap {"key": "lb3.p32.f49", "n": 4, "names": ["A", "B", "C", "D"], "title": "f49", "cap": "Mapa de $\\overline{f_{49}}$: los 1 son los ceros de $f_{49}$. Se rodean para leer el producto de sumas."}

**$f_{50}$**: $f_{50}=(D)(\overline{B})(\overline{A} + C)$
@fig kmap {"key": "lb3.p32.f50", "n": 4, "names": ["A", "B", "C", "D"], "title": "f50", "cap": "Mapa de $\\overline{f_{50}}$: los 1 son los ceros de $f_{50}$. Se rodean para leer el producto de sumas."}
@end
@paso Funciones 51 a 56
**$f_{51}$**: $f_{51}=(A + C + D)(A + B + \overline{C})$
@fig kmap {"key": "lb3.p32.f51", "n": 4, "names": ["A", "B", "C", "D"], "title": "f51", "cap": "Mapa de $\\overline{f_{51}}$: los 1 son los ceros de $f_{51}$. Se rodean para leer el producto de sumas."}

**$f_{52}$**: $f_{52}=0$
@fig kmap {"key": "lb3.p32.f52", "n": 4, "names": ["A", "B", "C", "D"], "title": "f52", "cap": "Mapa de $\\overline{f_{52}}$: los 1 son los ceros de $f_{52}$. Se rodean para leer el producto de sumas."}

**$f_{53}$**: $f_{53}=(\overline{C} + D)(\overline{B} + C)$
@fig kmap {"key": "lb3.p32.f53", "n": 4, "names": ["A", "B", "C", "D"], "title": "f53", "cap": "Mapa de $\\overline{f_{53}}$: los 1 son los ceros de $f_{53}$. Se rodean para leer el producto de sumas."}

**$f_{54}$**: $f_{54}=(B + C + D)(A + \overline{C} + D)(\overline{A} + \overline{B} + C)$
@fig kmap {"key": "lb3.p32.f54", "n": 4, "names": ["A", "B", "C", "D"], "title": "f54", "cap": "Mapa de $\\overline{f_{54}}$: los 1 son los ceros de $f_{54}$. Se rodean para leer el producto de sumas."}

**$f_{55}$**: $f_{55}=(\overline{B} + \overline{C} + D)(\overline{A})$
@fig kmap {"key": "lb3.p32.f55", "n": 4, "names": ["A", "B", "C", "D"], "title": "f55", "cap": "Mapa de $\\overline{f_{55}}$: los 1 son los ceros de $f_{55}$. Se rodean para leer el producto de sumas."}

**$f_{56}$**: $f_{56}=(B + D)(\overline{C} + \overline{D})(\overline{B} + C)$ Hay 3 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f56", "n": 4, "names": ["A", "B", "C", "D"], "title": "f56", "cap": "Mapa de $\\overline{f_{56}}$: los 1 son los ceros de $f_{56}$. Se rodean para leer el producto de sumas."}
@end
@paso Funciones 57 a 58
**$f_{57}$**: $f_{57}=(B + \overline{D})(C + \overline{D})(\overline{A} + D)$ Hay 3 soluciones mínimas equivalentes.
@fig kmap {"key": "lb3.p32.f57", "n": 4, "names": ["A", "B", "C", "D"], "title": "f57", "cap": "Mapa de $\\overline{f_{57}}$: los 1 son los ceros de $f_{57}$. Se rodean para leer el producto de sumas."}

**$f_{58}$**: $f_{58}=(\overline{B} + D)(\overline{A} + \overline{B})$
@fig kmap {"key": "lb3.p32.f58", "n": 4, "names": ["A", "B", "C", "D"], "title": "f58", "cap": "Mapa de $\\overline{f_{58}}$: los 1 son los ceros de $f_{58}$. Se rodean para leer el producto de sumas."}
@end
@res
Las 20 soluciones del libro valen 0 en los 0 y 1 en los 1 del mapa. Funciones especiales: $f_{40}=0$ y $f_{52}=0$ (el mapa entero son ceros e indiferentes), $f_{48}=ABCD$ (un solo 1), $f_{49}=A+\bar B+C$.

@box ojo | Notas sobre $f_{42}$ y $f_{47}$
En $f_{42}$ el mapa tiene un 0 en $ABCD=0110$ que la solución impresa no cubre: o sobra ese 0 en el mapa o falta un factor. En $f_{47}$ la solución impresa es correcta pero tiene un literal de más.
@end
@end
@end

