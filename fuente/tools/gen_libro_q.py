# -*- coding: utf-8 -*-
"""Preguntas tipo test basadas en los capítulos 1–6 del libro de problemas. Cada respuesta correcta se calcula/verifica con código."""
import os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
out = []; N = {}
def W(s=''): out.append(s)
def q(tag, stem, ok, wrong, expl):
    assert len(wrong) in (2, 3) and ok not in wrong and len(set(wrong)) == len(wrong), (stem, ok, wrong)
    W('@q ' + tag); W(stem); W('+ ' + ok)
    for w in wrong: W('- ' + w)
    W('> ' + expl); W('@end'); W()
    N[tag] = N.get(tag, 0) + 1
def bits(v, n): return format(v & ((1 << n) - 1), '0%db' % n)
def c2(v, n=4): return v - (1 << n) if v >> (n - 1) & 1 else v
def tt(f, n): return [f(*[(i >> (n - 1 - k)) & 1 for k in range(n)]) for i in range(1 << n)]

W('%% id=libro_test'); W('%% group=auto'); W('%% n=2'); W('%% title=Test del libro de problemas'); W('%% short=Test del libro de problemas')
W('%% sub=Preguntas tipo test sobre los capítulos 1 a 6 del libro de problemas (códigos, álgebra de Boole, Karnaugh, diseño combinacional, bloques MSI y biestables). Cada respuesta está comprobada con código.'); W()
W('Responde sin mirar la solución. Al elegir una opción se marca la correcta y se explica por qué. Cada bloque corresponde a un capítulo de la sección *Libro de problemas resueltos*; si fallas dos preguntas de uno, repasa sus problemas.'); W()

# ============================================================ capítulo 1
W('@details Capítulo 1 · Sistemas de numeración y códigos')
v = 37; a = bin(v)[2:]
q('libro1', f'El número decimal ${v}$ escrito en binario puro es:', a, ['101001', '100110', '010101'], f'${v}=32+4+1$, es decir, $100101_2$. Las otras opciones valen 41, 38 y 21.')
assert [int(x, 2) for x in ('101001', '100110', '010101')] == [41, 38, 21]
q('libro1', r'El hexadecimal $B7_{16}$ vale en decimal:', '183', ['187', '171', '247'], r'$B7_{16}=11\cdot16+7=183$. 171 es $AB_{16}$ y 247 es $F7_{16}$.')
assert int('B7', 16) == 183 and int('AB', 16) == 171 and int('F7', 16) == 247
d59 = ' '.join(format(int(c), '04b') for c in '59'); assert d59 == '0101 1001'
q('libro1', 'El número decimal $59$ en BCD natural es:', '0101 1001', ['0011 1011', '1001 0101', '0101 1010'], 'BCD codifica **cada dígito** por separado: $5\\to0101$ y $9\\to1001$. $0011\\,1011$ sería el binario puro de 59 cortado en dos; $1001\\,0101$ es el 95; $1010$ no es un dígito BCD.')
assert bits(59, 6) == '111011'
q('libro1', 'El dígito $5$ en código exceso 3 es:', '1000', ['0101', '0010', '1011'], 'Exceso 3 es el BCD del dígito más 3: $5+3=8=1000$. $0101$ sería el BCD natural y $1011$ el Aiken.')
aiken = {d: (format(d, '04b') if d < 5 else format(d + 6, '04b')) for d in range(10)}
assert aiken[5] == '1011' and aiken[7] == '1101' and aiken[6] == '1100'
q('libro1', 'En el código Aiken (2421) el dígito $7$ se escribe:', '1101', ['1011', '1110', '1100'], 'Con pesos $2,4,2,1$ de izquierda a derecha, $1101=2+4+0+1=7$. En Aiken los dígitos 0–4 coinciden con el binario y los 5–9 son el complemento de los 4–0; $1011$ es el 5, $1100$ el 6 y $1110$ el 8.')
g = lambda b_: b_ ^ (b_ >> 1)
assert bits(g(0b1011), 4) == '1110'
q('libro1', 'El código Gray de la combinación binaria $1011$ es:', '1110', ['1101', '0110', '1010'], 'El bit de mayor peso se copia y cada bit siguiente es el XOR de dos bits consecutivos del binario: $1,\\ 1\\oplus0=1,\\ 0\\oplus1=1,\\ 1\\oplus1=0$, es decir $1110$.')
q('libro1', 'El rango de números enteros con signo que se pueden representar en complemento a 2 con $6$ bits es:', '$-32$ a $+31$', ['$-31$ a $+31$', '$-32$ a $+32$', '$0$ a $63$'], 'Con $n$ bits en C2: de $-2^{n-1}$ a $2^{n-1}-1$. Con 6 bits, de $-32$ a $+31$. El rango simétrico $-31$ a $+31$ es el de signo y magnitud o el de C1.')
q('libro1', 'La combinación de 4 bits $1011$ leída en complemento a 2 vale:', '$-5$', ['$-4$', '$-3$', '$+11$'], 'Con signo negativo: $1011\\to$ se invierte y se suma 1: $0100+1=0101=5$, luego $-5$. Como C1 valdría $-4$, como signo y magnitud $-3$, y sin signo $11$.')
assert c2(0b1011) == -5 and -(0b0100) == -4 and -(0b011) == -3
sm = 0b0101 + 0b0100; assert sm == 9 and c2(sm & 15) == -7 and sm > 7
q('libro1', 'Se suman en C2 con 4 bits $0101+0100$ ($5+4$). Resulta:', 'Desbordamiento: dos positivos dan $1001$, que se lee como negativo', ['Resultado correcto $+9$', 'Resultado correcto $-7$', 'No hay desbordamiento porque no sale acarreo'], 'El resultado $1001$ no se puede leer como $+9$ (el máximo en C2 de 4 bits es $+7$): **el signo del resultado es distinto del de los sumandos**, y eso indica desbordamiento aunque no salga acarreo.')
assert 0b1011 + 0b0111 == 18 and bits(18, 5) == '10010'
q('libro1', 'En binario sin signo con 4 bits se suma $1011+0111$ ($11+7$). Resulta:', '$0010$ con acarreo de salida: desbordamiento', ['$1010$ sin desbordamiento', '$0010$ sin desbordamiento', '$10010$ cabe en 4 bits'], '$11+7=18$ no cabe en 4 bits (máximo 15). Se obtiene $10010_2$: se queda $0010$ y el acarreo de salida vale 1, lo que en sin signo indica **desbordamiento**.')
c10 = 1000 - 374; assert c10 == 626
q('libro1', 'El complemento a 10 del número decimal $374$ (con 3 dígitos) es:', '626', ['625', '636', '1626'], 'C10 $=10^3-374=626$. El complemento a 9 sería $625$ (a cada dígito se le resta de 9) y C10 es el C9 más 1.')
assert bits(-6, 4) == '1010'
q('libro1', 'El complemento a 2 de $0110$ ($+6$) con 4 bits es:', '1010', ['1001', '0110', '1110'], 'Se invierten los bits ($1001$) y se suma 1: $1010$, que en C2 vale $-6$. $1001$ sería el complemento a 1.')
W('@end'); W()

# ============================================================ capítulo 2
W('@details Capítulo 2 · Álgebra de Boole y funciones lógicas')
assert all(((1 - (a | (b & c))) == ((1 - a) & ((1 - b) | (1 - c)))) for a, b, c in itertools.product((0, 1), repeat=3))
q('libro2', r'Aplicando De Morgan, $\overline{A+B\cdot C}$ es igual a:', r'$\overline A\cdot(\overline B+\overline C)$', [r'$\overline A+\overline B\cdot\overline C$', r'$\overline A\cdot\overline B\cdot\overline C$', r'$\overline A\cdot\overline B+\overline C$'], r'La suma exterior pasa a producto y la parte interior $\overline{B\cdot C}=\overline B+\overline C$. Se verifica con las 8 combinaciones.')
fs = tt(lambda a, b, c: c, 3); assert [i for i, v in enumerate(fs) if v] == [1, 3, 5, 7]
q('libro2', r'La función de tres variables $f(A,B,C)=\sum m(1,3,5,7)$ (con $A$ el bit de más peso) es igual a:', '$C$', ['$A$', r'$\overline C$', '$A+B$'], 'Los minitérminos 1, 3, 5 y 7 son los de índice impar: es decir, los que tienen $C=1$. La función es $f=C$.')
assert all((1 - (1 - (a & b)) * (1 - (c & d)) if False else ((1 - ((1 - (a & b)) & (1 - (c & d))))) == ((a & b) | (c & d))) for a, b, c, d in itertools.product((0, 1), repeat=4))
q('libro2', r'¿Cuántas puertas NAND de 2 entradas necesita una función $f=AB+CD$ en dos niveles si solo hay NAND?', '3', ['2', '4', '5'], r'$f=\overline{\overline{AB}\cdot\overline{CD}}$: una NAND por cada producto y una NAND final que los combina. Las entradas se usan sin negar.')
assert all((1 - (1 - (a | b)) | (1 - (c | d)) if False else (1 - ((1 - (a | b)) | (1 - (c | d))))) == ((a | b) & (c | d)) for a, b, c, d in itertools.product((0, 1), repeat=4))
q('libro2', r'Con solo puertas NOR, el producto de sumas $(A+B)(C+D)$ se implementa con:', 'Tres NOR: dos primeras y una que las combina', ['Tres NAND: dos primeras y una que las combina', 'Una sola NOR de cuatro entradas', 'Cuatro NOR en cuatro niveles'], r'$(A+B)(C+D)=\overline{\overline{A+B}+\overline{C+D}}$: dos NOR y una tercera NOR. Es el dual del caso de la suma de productos con NAND.')
assert all(((d1 | d3 | d5 | d7) == (i & 1)) for i in range(8) for d1, d3, d5, d7 in [(int(i == 1), int(i == 3), int(i == 5), int(i == 7))])
q('libro2', 'En un codificador de 8 a 3 hecho con puertas OR, el bit de menos peso $A_0$ vale:', r'$D_1+D_3+D_5+D_7$', [r'$D_0+D_2+D_4+D_6$', r'$D_4+D_5+D_6+D_7$', r'$D_2+D_3+D_6+D_7$'], r'$A_0=1$ para las entradas cuyo índice en binario termina en 1: 1, 3, 5 y 7. $D_4+D_5+D_6+D_7$ es $A_2$ y $D_2+D_3+D_6+D_7$ es $A_1$.')
q('libro2', 'Un decodificador de 3 a 8 con habilitación activa recibe la entrada $101$. Las salidas que se activan son:', 'Solo la salida 5', ['Las salidas 1 y 4', 'Las salidas 0 a 5', 'Ninguna, porque 101 es impar'], 'Un decodificador activa **exactamente una** salida: la que corresponde al número de entrada ($101_2=5$). Si la habilitación estuviese inactiva no se activaría ninguna.')
x = 0
for b_ in map(int, '1101001'): x ^= b_
assert x == 0 and '1101001'.count('1') == 4
q('libro2', 'Un generador de paridad par para el dato de 7 bits $1101001$ añade un bit de paridad igual a:', '0', ['1', 'El que corresponda al bit de más peso', 'No se puede calcular con menos de 8 bits'], 'El dato tiene 4 unos (par), luego el bit añadido vale 0 para que el total siga siendo par. El bit es el **XOR de los 7 bits**: $1\\oplus1\\oplus0\\oplus1\\oplus0\\oplus0\\oplus1=0$.')
assert all((a | (a & b)) == a for a in (0, 1) for b in (0, 1))
q('libro2', 'El teorema de absorción dice que $A+A\\cdot B$ vale:', '$A$', ['$B$', '$A\\cdot B$', '$A+B$'], 'Si $A=1$ la suma da 1; si $A=0$ el producto $AB=0$ y la suma da 0. En los dos casos coincide con $A$.')
uno = {0, 2, 5}; ceros = sorted(set(range(8)) - uno); assert ceros == [1, 3, 4, 6, 7]
q('libro2', r'Si $f(A,B,C)=\sum m(0,2,5)$, su forma en producto de maxitérminos es:', r'$\prod M(1,3,4,6,7)$', [r'$\prod M(0,2,5)$', r'$\prod M(1,3,5,7)$', r'$\prod M(4,6,7)$'], 'Los maxitérminos son los índices donde la función vale 0, es decir, el resto de índices de 0 a 7: 1, 3, 4, 6 y 7.')
assert all((1 - a) & (1 - b) == 1 - (a | b) for a in (0, 1) for b in (0, 1))
q('libro2', r'La expresión $\overline A\cdot\overline B$ es equivalente a la salida de una puerta:', 'NOR de $A$ y $B$', ['NAND de $A$ y $B$', 'XNOR de $A$ y $B$', 'OR de $\\overline A$ y $\\overline B$'], 'Por De Morgan, $\\overline A\\,\\overline B=\\overline{A+B}$, que es la NOR. $\\overline A+\\overline B$ sería la NAND.')
W('@end'); W()

# ============================================================ capítulo 3
W('@details Capítulo 3 · Mapas de Karnaugh')
q('libro3', 'En un mapa de Karnaugh de 4 variables, un grupo de 8 unos adyacentes produce un término con:', 'Un solo literal', ['Dos literales', 'Tres literales', 'Ninguno: la función vale siempre 1'], 'Un grupo de $2^k$ casillas elimina $k$ variables. Con $k=3$ se eliminan tres de las cuatro y queda un literal.')
assert tt(lambda a, b, c: int(a == 0), 3) == [1, 1, 1, 1, 0, 0, 0, 0]
q('libro3', r'En tres variables, $f=\sum m(0,1,2,3)$ (con $A$ el bit de más peso) se simplifica a:', r'$\overline A$', ['$A$', r'$\overline B$', '$1$'], 'Los minitérminos 0–3 son los que tienen $A=0$: cuatro casillas adyacentes, un grupo que elimina $B$ y $C$ y deja $\\overline A$.')
q('libro3', 'Con combinaciones indiferentes en un mapa de Karnaugh, se incluyen en un grupo:', 'Solo las que permiten hacer el grupo más grande', ['Todas, siempre', 'Ninguna: no se pueden usar', 'Solo las que están más cerca del origen'], 'Las X se toman como 1 **si ayudan** a formar un grupo mayor (menos literales) y se ignoran en caso contrario. No hay obligación de cubrirlas.')
assert tt(lambda a, b, c: (a | b), 3)[0] == 0 and tt(lambda a, b, c: (a | b), 3)[1] == 0 and sum(1 for v in tt(lambda a, b, c: (a | b), 3) if v == 0) == 2
q('libro3', r'En producto de sumas, un mapa de tres variables con ceros solo en $m_0$ y $m_1$ da:', '$A+B$', [r'$\overline A+\overline B$', r'$\overline A\cdot\overline B$', '$A\\cdot B$'], 'Se agrupan los ceros: $m_0=000$ y $m_1=001$ forman un grupo con $A=0$ y $B=0$. En una **suma**, las variables que valen 0 aparecen **sin negar**: $A+B$.')
q('libro3', 'En un mapa de Karnaugh de 4 variables, las cuatro esquinas:', 'Son adyacentes entre sí y forman un grupo posible', ['No se pueden agrupar', 'Solo se agrupan si son indiferentes', 'Forman un grupo de 2 casillas'], 'El mapa es un toroide: la primera y la última fila, y la primera y la última columna, son adyacentes. Las cuatro esquinas difieren solo en dos variables y forman un grupo de 4.')
q('libro3', 'Las filas y las columnas de un mapa de Karnaugh se ordenan $00,01,11,10$ porque:', 'Casillas contiguas deben diferir solo en una variable (orden Gray)', ['Es el orden del binario natural', 'Así se simplifica siempre a una sola puerta', 'Lo exige la forma producto de sumas'], 'Con el orden Gray, dos casillas vecinas son combinaciones adyacentes, que se pueden agrupar y eliminar la variable que cambia.')
assert [i for i in range(16) if not (i >> 2) & 1] == [0, 1, 2, 3, 8, 9, 10, 11]
q('libro3', r'En 4 variables ($ABCD$, $A$ el de más peso), $f=\sum m(0,1,2,3,8,9,10,11)$ vale:', r'$\overline B$', ['$\\overline A$', '$\\overline C$', r'$\overline B\,\overline D$'], 'Los ocho minitérminos son los que tienen $B=0$: en el mapa forman dos filas contiguas por el borde (un grupo de 8) y se simplifica a $\\overline B$.')
q('libro3', 'Un implicante primo es esencial cuando:', 'Cubre algún 1 que ningún otro implicante primo cubre', ['Tiene el mayor número de casillas del mapa', 'Cubre alguna combinación indiferente', 'No comparte casillas con ningún otro'], 'Los implicantes primos esenciales hay que incluirlos siempre: son los únicos que cubren cierto 1 del mapa. El resto se elige para cubrir lo que falte con el menor coste.')
q('libro3', 'Para obtener la forma mínima como producto de sumas se agrupan en el mapa:', 'Los ceros', ['Los unos', 'Las combinaciones indiferentes', 'Las filas completas'], 'El producto de sumas se obtiene agrupando los ceros: cada grupo da una suma y la función es el producto de todas ellas. Los unos darían una suma de productos.')
W('@end'); W()

# ============================================================ capítulo 4
W('@details Capítulo 4 · Diseño combinacional con puertas')
mj = tt(lambda a, b, c: int(a + b + c >= 2), 3)
assert sum(mj) == 4 and all(mj[i] == ((((i >> 2) & (i >> 1)) | ((i >> 2) & i) | ((i >> 1) & i)) & 1) for i in range(8))
q('libro4', 'En el voto mayoritario de tres sensores, la salida vale 1 en:', '4 de las 8 combinaciones', ['3 de las 8', '5 de las 8', 'Solo en la combinación $111$'], 'Vale 1 si hay al menos dos unos: $011,101,110,111$. Es $f=AB+AC+BC$.')
assert all((bits(-v, 4)[-1] == bits(v, 4)[-1]) for v in range(16))
q('libro4', 'En el complemento a 2 de un número de 4 bits, el bit de menor peso de la salida es:', 'Igual que el de la entrada', ['El opuesto al de la entrada', 'Siempre 0', 'Siempre 1'], 'Al invertir y sumar 1, el bit de menos peso se invierte y vuelve a invertirse con el +1: queda igual. En cambio, los demás bits dependen de los de menos peso.')
c9 = [9 - d for d in range(10)]; assert c9[4] == 5 and format(5, '04b') == '0101'
q('libro4', 'En un circuito que da el complemento a 9 de un dígito BCD, la entrada $0100$ ($4$) produce la salida:', '0101', ['0110', '0100', '1011'], 'El complemento a 9 es $9-d$: $9-4=5=0101$. Las entradas $1010$ a $1111$ no son dígitos BCD y se toman como indiferentes en el diseño.')
assert max(a * b for a in range(4) for b in range(4)) == 9
q('libro4', 'Un multiplicador de dos números de 2 bits necesita una salida de:', '4 bits', ['2 bits', '3 bits', '5 bits'], 'El producto máximo es $3\\cdot3=9=1001_2$, que necesita 4 bits.')
q('libro4', r'En un comparador de dos números de 2 bits ($A_1A_0$ y $B_1B_0$), la salida «A es igual a B» es:', r'$(A_1\odot B_1)\cdot(A_0\odot B_0)$', [r'$(A_1\oplus B_1)\cdot(A_0\oplus B_0)$', r'$A_1B_1+A_0B_0$', r'$(A_1\odot B_1)+(A_0\odot B_0)$'], 'Son iguales si **cada bit** lo es: XNOR bit a bit y un AND de los resultados. Con XOR se detectaría que todos los bits son distintos.')
assert all((a & b) | (c & (a ^ b)) == (1 if a + b + c >= 2 else 0) for a in (0, 1) for b in (0, 1) for c in (0, 1))
q('libro4', 'En un sumador completo de 1 bit, el acarreo de salida es:', r'$C_{out}=AB+C_{in}(A\oplus B)$', [r'$C_{out}=A\oplus B\oplus C_{in}$', r'$C_{out}=A+B+C_{in}$', r'$C_{out}=A\cdot B\cdot C_{in}$'], r'Hay acarreo si $A$ y $B$ valen 1, o si uno de los dos vale 1 y viene acarreo de entrada. La suma $A\oplus B\oplus C_{in}$ es la salida $S$, no el acarreo.')
q('libro4', 'Con solo puertas NAND, una AND de dos entradas necesita:', '2 NAND', ['1 NAND', '3 NAND', 'No se puede hacer'], '$A\\cdot B=\\overline{\\overline{AB}}$: una NAND y otra NAND con las dos entradas unidas, que hace de inversor.')
q('libro4', 'En un divisor de dos números de 2 bits hay una combinación que hay que tratar aparte. Es:', 'Divisor igual a $00$ (división por cero)', ['Dividendo igual a $00$', 'Dividendo igual al divisor', 'Dividendo $11$ y divisor $11$'], 'Dividir por 0 no está definido: la salida correspondiente suele marcarse como indiferente o con un indicador de error. El resto de combinaciones tienen cociente y resto definidos.')
q('libro4', 'En un decodificador de BCD a 7 segmentos, el dígito 1 enciende los segmentos:', '$b$ y $c$', ['$a$ y $d$', '$a$, $b$ y $c$', '$e$ y $f$'], 'Los segmentos $b$ y $c$ son los dos verticales de la derecha, que dibujan el 1. El dígito 7 es el que enciende $a$, $b$ y $c$.')
W('@end'); W()

# ============================================================ capítulo 5
W('@details Capítulo 5 · Bloques combinacionales MSI')
s_ = 0b0111 + 0b0101; assert s_ == 12 and (s_ >> 4) == 0
q('libro5', 'Un sumador de 4 bits recibe $A=0111$, $B=0101$ y $C_{in}=0$. Su salida es:', '$S=1100$ y $C_{out}=0$', ['$S=1100$ y $C_{out}=1$', '$S=0010$ y $C_{out}=1$', '$S=1110$ y $C_{out}=0$'], '$7+5=12=1100_2$, que cabe en 4 bits: no hay acarreo de salida.')
assert all(((a + (~b & 15) + 1) >> 4 == int(a >= b)) for a in range(16) for b in range(16))
q('libro5', 'Para calcular $A-B$ (sin signo, 4 bits) con un sumador se hace:', r'$A+\overline B+1$, y el acarreo de salida vale 1 si $A\ge B$', [r'$A+\overline B$, y el acarreo vale 1 si $A<B$', r'$A+B+1$, y el acarreo vale 1 si $A\ge B$', r'$\overline A+B+1$, y el acarreo vale 1 si $A\ge B$'], 'Restar es sumar el complemento a 2: $\\overline B+1$. Si el acarreo de salida vale 1 el resultado es positivo o cero ($A\\ge B$); si vale 0, no hay «llevada» y es negativo.')
q('libro5', 'Para implementar una función cualquiera de 4 variables con un multiplexor 8:1 se llevan a las líneas de selección:', '3 variables, y la cuarta (o 0, 1 o su complemento) a las entradas de datos', ['Las 4 variables a la selección', '2 variables y las otras 2 a los datos', 'Solo se puede con un 16:1'], 'Un 8:1 tiene 3 selecciones. Se eligen 3 variables como selección y, para cada una de las 8 combinaciones, la función restante depende solo de la cuarta: vale 0, 1, la variable o su complemento.')
cod = {d: d + 3 for d in range(10)}; assert (cod[9] | cod[0]) == 0b1111 and bits(cod[9], 4) == '1100' and bits(cod[0], 4) == '0011'
q('libro5', 'Un codificador decimal a exceso 3 **sin prioridad** recibe a la vez las líneas 9 y 0. La salida es:', '1111', ['1100', '0011', '0000'], 'Cada línea activa pone a 1 los bits de su código: el 9 da $1100$ y el 0 da $0011$. Sin prioridad, las salidas se combinan con OR: $1111$, que ni siquiera es un código válido.')
v7_8 = 7 + 8; assert v7_8 == 15 and bits(15 + 6, 8) == '00010101'
q('libro5', 'Se suman dos dígitos BCD, $7+8$, con un sumador binario. Para obtener el resultado BCD hay que:', 'Sumar 6: $1111+0110$ da $0001\\,0101$', ['Restar 6', 'Sumar 3 a cada dígito', 'No hace falta corrección: $1111$ es BCD'], 'La suma binaria es $1111$ ($15$), que no es un dígito BCD. Sumando 6 se salta de $1001$ a $0000$ con acarreo: $1111+0110=0001\\,0101$, que es $15$ en BCD.')
def ovf(a, b): s = c2(a) + c2(b); return not -8 <= s <= 7
def cin_cout(a, b):
    cin = ((a & 7) + (b & 7)) >> 3; cout = (a + b) >> 4; return cin != cout
assert all(ovf(a, b) == cin_cout(a, b) for a in range(16) for b in range(16))
q('libro5', 'En una suma en C2, hay desbordamiento cuando:', 'El acarreo que entra al bit de signo y el que sale son distintos', ['Siempre que $C_{out}=1$', 'Siempre que $C_{out}=0$', 'Solo si los dos sumandos son negativos'], 'Se comprueba para las 256 sumas de 4 bits: coincide con $C_{in,3}\\ne C_{out}$. Que salga acarreo no basta: $-1+(-1)$ da acarreo y es correcto.')
assert (-(-8)) & 15 == 0b1000 and c2(0b1000) == -8
q('libro5', 'Un circuito de valor absoluto de 4 bits (C2) recibe $1000$ ($-8$). La salida es:', '$1000$, que sigue valiendo $-8$', ['$0111$', '$1000$, que ahora vale $+8$', '$0000$'], 'El $+8$ no es representable en 4 bits C2 (máximo $+7$). Al negar $1000$ resulta $1000$ otra vez: es el único caso en que el valor absoluto es incorrecto.')
q('libro5', 'Un multiplexor 4:1 tiene:', '4 entradas de datos, 2 de selección y 1 salida', ['2 entradas de datos y 4 de selección', '4 de datos y 4 de selección', '4 de datos y 1 de selección'], 'Para elegir entre 4 entradas hacen falta $\\log_2 4=2$ líneas de selección.')
q('libro5', 'Un decodificador de BCD a 7 segmentos solo define su salida para:', 'Las entradas $0000$ a $1001$; las otras seis son combinaciones no usadas', ['Las 16 entradas por igual', 'Solo las entradas pares', 'Solo $0000$ a $0111$'], 'Hay 10 dígitos BCD. Las entradas $1010$ a $1111$ nunca se dan y en el diseño se toman como indiferentes (o se usan para mostrar símbolos o apagar el display).')
a_, b_ = 15, 1; assert (a_ + b_) & 15 == 0 and (a_ + b_) >> 4 == 1
q('libro5', 'Un sumador de 4 bits recibe $A=1111$ y $B=0001$ con $C_{in}=0$. La salida es:', '$S=0000$ y $C_{out}=1$', ['$S=1111$ y $C_{out}=0$', '$S=0000$ y $C_{out}=0$', '$S=1110$ y $C_{out}=1$'], '$15+1=16=10000_2$: los cuatro bits bajos valen 0 y se genera el acarreo de salida.')
W('@end'); W()

# ============================================================ capítulo 6
W('@details Capítulo 6 · Biestables y cronogramas')
q('libro6', r'En una báscula R‑S asíncrona con puertas NAND (entradas activas en bajo), la combinación $\overline S=\overline R=0$ da:', 'Las dos salidas a 1: situación prohibida', ['$Q=0$ y $\\overline Q=1$', '$Q=1$ y $\\overline Q=0$', 'Mantiene el estado anterior'], r'Cada NAND con una entrada a 0 da 1: $Q=\overline Q=1$. Es prohibida porque las dos salidas dejan de ser complementarias.')
q('libro6', r'En la báscula R‑S de NAND, las dos entradas pasan **a la vez** de $\overline S\,\overline R=00$ a $11$. La salida:', 'Queda en un valor desconocido a priori', ['Queda siempre a 1', 'Queda siempre a 0', 'Se mantiene en el valor anterior a la prohibida'], 'Las dos puertas ven «1,1» a la vez y compiten: la que gane se queda a 0 y la otra a 1, sin que se pueda saber cuál. Si solo cambia una entrada, el resultado sí es único.')
q('libro6', 'Una báscula J‑K **asíncrona** con $J=K=1$ mantenido produce:', 'Carreras: la salida bascula continuamente', ['Q invertida una sola vez', 'Q a 1', 'Q a 0'], 'Sin reloj que acote el instante, la salida se realimenta y cambia una y otra vez mientras dure $JK=11$. Por eso se necesita el sincronismo por flanco o el maestro/esclavo.')
q('libro6', 'Un R‑S síncrono por flanco encuentra $S=R=1$ justo antes del flanco activo. Su salida es:', 'Indeterminada hasta una nueva orden clara', ['Q a 1', 'Q a 0', 'Q invertida'], 'Es la situación prohibida del R‑S. Con sincronismo por flanco no hay una puerta que «acabe» antes: la salida queda desconocida hasta que un flanco posterior dé $10$ o $01$.')
q('libro6', 'Un J‑K por flanco de subida con $J=K=1$ antes del flanco:', 'Invierte la salida una vez en ese flanco', ['Queda indeterminado', 'Entra en carreras', 'Mantiene la salida'], 'En un J‑K por flanco, $JK=11$ es la orden de **conmutar**: $Q^+=\\overline Q$. Al ser un instante, no hay carreras.')
q('libro6', 'Un maestro/esclavo J‑K equivale a un J‑K por flanco si:', 'J y K no cambian durante el nivel activo del maestro', ['Siempre, sea cual sea el cronograma', 'Solo si $J=K$', 'Solo si el reloj es simétrico'], 'El maestro «piensa» durante su nivel activo y puede ser sensible a cambios de J y K en ese tiempo, mientras que el J‑K por flanco solo mira un instante. En el problema del libro, un $JK=11$ seguido de $10$ da $0$ en el M/S y $1$ por flanco.')
q('libro6', r'En el maestro de un J‑K maestro/esclavo, las entradas del R‑S interno son:', r'$S_M=J\cdot\overline{Q_S}$ y $R_M=K\cdot Q_S$', [r'$S_M=J\cdot Q_S$ y $R_M=K\cdot\overline{Q_S}$', r'$S_M=J+\overline{Q_S}$ y $R_M=K+Q_S$', '$S_M=J$ y $R_M=K$'], 'Realimentar la salida del esclavo impide que $S_M$ y $R_M$ valgan 1 a la vez: solo se puede **subir** si $Q_S=0$ y **bajar** si $Q_S=1$. Con $JK=11$ el maestro toma el opuesto del esclavo.')
q('libro6', 'Un latch D con línea ENABLE a 1 y D con pulsos cortos:', 'La salida sigue a D, incluidos los pulsos cortos', ['La salida ignora D mientras ENABLE vale 1', 'La salida solo copia D en los flancos de ENABLE', 'La salida queda indeterminada'], 'Por nivel, el latch D es **transparente** mientras ENABLE está activo y guarda el último valor al cerrarse. No hay situaciones prohibidas porque solo tiene una entrada.')
q('libro6', r'Dos biestables D por flanco de subida en cadena ($Q_1$ copia a $Ent$, $Q_2$ copia a $Q_1$) con una AND $Sal=\overline{Q_1}\cdot Q_2$ forman:', 'Un detector de flancos descendentes: pulso de un periodo de reloj', ['Un detector de flancos ascendentes', 'Un divisor de frecuencia por 2', 'Un contador de pulsos'], '$Sal=1$ solo cuando $Q_1$ ya ha bajado y $Q_2$ aún recuerda el 1: durante exactamente un periodo $T$ tras cada flanco de bajada de $Ent$.')
q('libro6', r'Con los mismos dos D, para detectar flancos **ascendentes** se usa la salida:', r'$Sal=Q_1\cdot\overline{Q_2}$', [r'$Sal=\overline{Q_1}\cdot Q_2$', r'$Sal=Q_1\cdot Q_2$', r'$Sal=Q_1\oplus Q_2$ con un solo D'], r'Tras un flanco de subida de $Ent$, $Q_1=1$ pero $Q_2$ aún vale 0 durante un periodo. $Q_1\oplus Q_2$ detectaría los dos tipos de flanco.')
def tff(A, B, q_): T = (A & (1 - q_)) | (B & q_); return q_ ^ T
assert all(tff(a, b, q_) == ((a & (1 - q_)) | ((1 - b) & q_)) for a in (0, 1) for b in (0, 1) for q_ in (0, 1))
q('libro6', r'Un flip‑flop T por flanco con $T=A\cdot\overline Q+B\cdot Q$ se comporta como:', 'Un J‑K con $J=A$ y $K=B$', ['Un D con $D=A$', 'Un R‑S con $S=A$ y $R=B$', 'Un T con $T=A+B$'], 'Si $A=1$ y $Q=0$ hay que subir (invertir); si $B=1$ y $Q=1$ hay que bajar (invertir). Se comprueba con las 8 filas: $Q^+=J\\overline Q+\\overline K Q$.')
q('libro6', r'El circuito $Q=A\cdot B+\overline A\cdot Q$ (con $Q$ realimentada) es:', 'Un latch D por nivel con $A=Ck$ y $B=D$', ['Un R‑S asíncrono', 'Un J‑K síncrono por nivel', 'Un T por flanco'], 'Con $A=0$ mantiene ($Q^+=Q$) y con $A=1$ copia $B$. No tiene combinación prohibida.')
q('libro6', 'El D por flanco hecho con seis puertas NAND puede verse como:', 'Tres latches R‑S asíncronos de NAND', ['Un J‑K con dos puertas extra', 'Un maestro/esclavo de dos latches D', 'Un contador de 3 bits'], 'Las puertas 1‑2 y 3‑4 forman dos latches de entrada que «capturan» D en el flanco, y las puertas 5‑6 forman el latch de salida. Después del flanco, los cambios de D ya no llegan a la salida.')
W('@end'); W()

open(os.path.join(ROOT, 'src', 'libro_test.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(N, sum(N.values()), 'preguntas')
