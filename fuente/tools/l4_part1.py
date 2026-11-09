# -*- coding: utf-8 -*-
# Problemas 4.6 - 4.17 del capítulo 4 (se ejecuta dentro de gen_libro4.py)

def table_x(innames, outnames, cols, dc_rows):
    n = len(innames); dcs = set(dc_rows)
    return tab(innames + outnames, [list(bits(i, n)) + [('×' if i in dcs else c[i]) for c in cols] for i in range(2 ** n)])
def all_rows_check(key, names, outcol, terms, dc=()):
    n = len(names)
    return all(eval_terms(terms, names, bits(i, n)) == outcol[i] for i in range(2 ** n) if i not in dc)
SEG = 'abcdefg'
def seg_cols(patterns):                      # patterns: dict fila -> cadena 'abcdefg' de 0/1
    return {s: {i: int(p[k]) for i, p in patterns.items()} for k, s in enumerate(SEG)}

# ============================================================== 4.6  complemento a 9 de un dígito BCD
n46 = ['B3', 'B2', 'B1', 'B0']; dc46 = list(range(10, 16))
c9 = [(9 - i) if i < 10 else 0 for i in range(16)]
cols46 = {'C93': [(v >> 3) & 1 for v in c9], 'C92': [(v >> 2) & 1 for v in c9], 'C91': [(v >> 1) & 1 for v in c9], 'C90': [v & 1 for v in c9]}
bk46 = {'C93': [0, 1], 'C92': [2, 3, 4, 5], 'C91': [2, 3, 6, 7], 'C90': [0, 2, 4, 6, 8]}
for k, v in bk46.items():
    on_ = [i for i in minterms_of(cols46[k]) if i < 10]
    check('lb4.p46.sigma.' + k, on_ == v); book('lb4.p46.sigma.' + k, on_ == v)
bt46 = {'C93': ['!B3 !B2 !B1'], 'C92': ['B2 !B1', '!B2 B1'], 'C91': ['B1'], 'C90': ['!B0']}
rep46 = {}; ok46 = True
for k in ['C93', 'C92', 'C91', 'C90']:
    t, m, okb, same = sop_report('lb4.p46.' + k, n46, k, cols46[k], bt46[k], dc_idx=dc46); rep46[k] = t; ok46 &= bool(okb and same)
check('lb4.p46', ok46)
err46 = [i for i in range(16) if i >= 10]
check('lb4.p46.error', all(eval_terms(['B3 B2', 'B3 B1'], n46, bits(i, 4)) == (1 if i >= 10 else 0) for i in range(16)))
ej('lb4-6', 'Complemento a 9 de un dígito BCD', 'Libro · Cap. 4 · P4.6', 'comb,karnaugh,bcd', 'lb4.p46',
   'Diseña el circuito más pequeño que obtenga el complemento a 9 de un dígito BCD $B_3B_2B_1B_0$, con salida $C_{93}C_{92}C_{91}C_{90}$.',
   '**Complemento a 9:** para un dígito $B$ es $9-B$. Se usa para restar en decimal. Las combinaciones $1010\\ldots1111$ no son dígitos BCD: ¿qué hacer con ellas?',
   [('Qué hacer con las seis combinaciones prohibidas', 'Hay tres opciones: (1) declarar la salida **indiferente** ($\\times$), (2) forzar un valor, por ejemplo $0000$, o (3) añadir una salida de **error** que valga 1. El libro elige la primera, porque da circuitos más pequeños. Si se quisiera la salida de error, sería $B_3B_2+B_3B_1$ (comprobado por código).'),
    ('Tabla de verdad', table_x(n46, ['C93', 'C92', 'C91', 'C90'], [cols46[k] for k in ['C93', 'C92', 'C91', 'C90']], dc46) + '\n\nEjemplos: $0\\to 9=1001$; $6\\to 3=0011$; $9\\to 0=0000$.'),
    ('Salida $C_{93}$', rep46['C93']), ('Salida $C_{92}$', rep46['C92']), ('Salida $C_{91}$', rep46['C91'] + '\n\nFíjate: $C_{91}=B_1$ es un cable, no hace falta ninguna puerta.'), ('Salida $C_{90}$', rep46['C90'] + '\n\nEs un solo inversor.')],
   'Con las indiferentes, las cuatro funciones son muy sencillas: un AND de tres entradas, dos AND y una OR, un cable y un inversor. Las cuatro soluciones del libro son correctas y mínimas.')

# ============================================================== 4.7  control de calidad de 4 piezas
n47 = ['M1', 'M2', 'M3', 'M4']
sums47 = [sum(bits(i, 4)) for i in range(16)]
cols47 = {'TA': [1 if s == 4 else 0 for s in sums47], 'MA': [1 if s == 3 else 0 for s in sums47], 'I': [1 if s == 2 else 0 for s in sums47], 'MR': [1 if s <= 1 else 0 for s in sums47]}
check('lb4.p47.exclusivas', all(sum(cols47[k][i] for k in cols47) == 1 for i in range(16)))
bk47 = {'TA': [15], 'MA': [7, 11, 13, 14], 'I': [3, 5, 6, 9, 10, 12], 'MR': [0, 1, 2, 4, 8]}
for k, v in bk47.items():
    check('lb4.p47.sigma.' + k, minterms_of(cols47[k]) == v); book('lb4.p47.sigma.' + k, minterms_of(cols47[k]) == v)
bt47 = {'TA': ['M1 M2 M3 M4'],
        'MA': ['M1 M2 M3 !M4', 'M1 M2 !M3 M4', 'M1 !M2 M3 M4', '!M1 M2 M3 M4'],
        'I': ['M1 M2 !M3 !M4', 'M1 !M2 M3 !M4', 'M1 !M2 !M3 M4', '!M1 M2 !M3 M4', '!M1 M2 M3 !M4', '!M1 !M2 M3 M4'],
        'MR': ['!M2 !M3 !M4', '!M1 !M3 !M4', '!M1 !M2 !M4', '!M1 !M2 !M3']}
rep47 = {}; ok47 = True
for k in ['TA', 'MA', 'I', 'MR']:
    t, m, okb, same = sop_report('lb4.p47.' + k, n47, k, cols47[k], bt47[k]); rep47[k] = t; ok47 &= bool(okb and same)
check('lb4.p47', ok47)
ej('lb4-7', 'Control de calidad: cuatro piezas por lote', 'Libro · Cap. 4 · P4.7', 'comb,karnaugh', 'lb4.p47',
   'De cada lote se extraen 4 piezas y un sensor da 1 si la pieza es aprobada y 0 si no. Diseña el circuito que indique: todas aprobadas ($TA$), mayoría aprobada ($MA$), igual número de aprobadas y rechazadas ($I$) y mayoría de rechazadas ($MR$).',
   '**Truco:** el número de unos de la entrada decide la salida. Cuatro unos: TA. Tres: MA. Dos: I. Cero o uno: MR. Siempre se activa **una y solo una** de las cuatro salidas.',
   [('Tabla de verdad', table_all(n47, ['TA', 'MA', 'I', 'MR'], [cols47[k] for k in ['TA', 'MA', 'I', 'MR']]) + '\n\nFila 0: todas rechazadas, $MR=1$. Fila 6 ($0110$): dos aprobadas, $I=1$. Fila 11 ($1011$): tres aprobadas, $MA=1$. Fila 15: $TA=1$ (y $MA$ no se activa, aunque la mayoría también sea de aprobadas).'),
    ('Salida $TA$', rep47['TA']), ('Salida $MA$', rep47['MA'] + '\n\nLos cuatro 1 del mapa están aislados (no son vecinos): no hay nada que agrupar y la suma de minitérminos ya es la mínima.'),
    ('Salida $I$', rep47['I'] + '\n\nSeis minitérminos aislados: es el patrón de «tablero de ajedrez» de los mapas, que no se simplifica. Son las combinaciones con exactamente dos unos.'),
    ('Salida $MR$', rep47['MR'])],
   'Los cuatro resultados coinciden con los del libro y son mínimos. Observa el coste: $MA$ e $I$ necesitan 4 y 6 AND de 4 entradas. Es el precio de detectar «exactamente $k$ unos».')

# ============================================================== 4.8 / 4.9  rumbo de un barco en un 7 segmentos
n48 = ['N', 'S', 'E', 'O']
DIR = {8: 'a', 4: 'd', 2: 'bc', 1: 'ef', 10: 'ab', 9: 'af', 6: 'cd', 5: 'de'}   # N, S, E, O, NE, NO, SE, SO
dc48 = [i for i in range(16) if i not in DIR]
cols48 = {s: [1 if (i in DIR and s in DIR[i]) else 0 for i in range(16)] for s in SEG}
bk48 = {'a': [8, 9, 10], 'b': [2, 10], 'c': [2, 6], 'd': [4, 5, 6], 'e': [1, 5], 'f': [1, 9], 'g': []}
for k, v in bk48.items():
    check('lb4.p48.sigma.' + k, minterms_of(cols48[k]) == v); book('lb4.p48.sigma.' + k, minterms_of(cols48[k]) == v)
check('lb4.p48.dc', dc48 == [0, 3, 7, 11, 12, 13, 14, 15])
bt48 = {'a': ['N'], 'b': ['!S E'], 'c': ['!N E'], 'd': ['S'], 'e': ['!N O'], 'f': ['!S O'], 'g': []}
rep48 = {}; ok48 = True
for k in SEG:
    t, m, okb, same = sop_report('lb4.p48.' + k, n48, k, cols48[k], bt48[k], dc_idx=dc48); rep48[k] = t; ok48 &= bool(okb and same)
check('lb4.p48', ok48)
ej('lb4-8', 'Rumbo de un barco en un display de 7 segmentos', 'Libro · Cap. 4 · P4.8', 'comb,karnaugh,7seg', 'lb4.p48',
   'El piloto automático indica el rumbo con cuatro señales $N,S,E,O$. Diseña el circuito más pequeño que lo dibuje en un 7 segmentos: norte activa $a$; sur, $d$; este, $b,c$; oeste, $e,f$; noreste, $a,b$; noroeste, $a,f$; sureste, $c,d$; suroeste, $d,e$.',
   '**Dibujar con segmentos.** Cada fila de la tabla es un rumbo y solo hay que «pintarlo». Un rumbo válido tiene una señal activa, o dos que sean vecinas (N+E, N+O, S+E, S+O). Norte con sur, o este con oeste, son imposibles.',
   [('Qué filas son válidas', 'Válidas (8): $N$=8, $S$=4, $E$=2, $O$=1, $NE$=10, $NO$=9, $SE$=6, $SO$=5. Imposibles (8): 0, 3, 7, 11, 12, 13, 14 y 15. El libro las deja como indiferentes, incluida la fila 0 (sin rumbo): un barco siempre lleva alguno.'),
    ('Tabla de verdad', table_x(n48, list(SEG), [cols48[k] for k in SEG], dc48) + '\n\nEjemplos: fila 1 (oeste): se encienden $e,f$ (el lado izquierdo). Fila 9 (noroeste): $a,f$. Fila 8 (norte): solo $a$.')] +
   [('Segmento $%s$' % k, rep48[k]) for k in SEG],
   'Con tantas indiferentes, casi todo se reduce a una o dos variables: $a=N$, $d=S$, $b=\\bar S E$, $c=\\bar N E$, $e=\\bar N O$, $f=\\bar S O$ y $g=0$ (el segmento central nunca se enciende). Todas coinciden con el libro.')

# ---- 4.9: mismas señales pero las combinaciones imposibles encienden todo
cols49 = {s: [1 if (i in dc48 or cols48[s][i]) else 0 for i in range(16)] for s in SEG}
bk49 = {'a': [0, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'b': [0, 2, 3, 7, 10, 11, 12, 13, 14, 15], 'c': [0, 2, 3, 6, 7, 11, 12, 13, 14, 15],
        'd': [0, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15], 'e': [0, 1, 3, 5, 7, 11, 12, 13, 14, 15], 'f': [0, 1, 3, 7, 9, 11, 12, 13, 14, 15], 'g': [0, 3, 7, 11, 12, 13, 14, 15]}
for k, v in bk49.items():
    check('lb4.p49.sigma.' + k, minterms_of(cols49[k]) == v); book('lb4.p49.sigma.' + k, minterms_of(cols49[k]) == v)
print_b49 = ['!N !S !E', 'E O', 'N S', '!S E']          # tal como está impreso (término 1 con Ē)
fix_b49 = ['!N !S !O', 'E O', 'N S', '!S E']
check('lb4.p49.b_impresa_falla', not all_rows_check('b', n48, cols49['b'], print_b49))
bt49 = {'a': ['!S !E !O', 'E O', 'N'], 'b': fix_b49, 'c': ['!N !S !O', 'E O', 'N S', '!N E'], 'd': ['!N !E !O', 'E O', 'S'],
        'e': ['!N !S !E', 'E O', 'N S', '!N O'], 'f': ['!N !S !E', 'E O', 'N S', '!S O'], 'g': ['!N !S !E !O', 'E O', 'N S']}
rep49 = {}; ok49 = True
for k in SEG:
    t, m, okb, same = sop_report('lb4.p49.' + k, n48, k, cols49[k], bt49[k]); rep49[k] = t; ok49 &= bool(okb and same)
check('lb4.p49', ok49)
ej('lb4-9', 'Rumbo del barco con alarma de datos erróneos', 'Libro · Cap. 4 · P4.9', 'comb,karnaugh,7seg', 'lb4.p49',
   'Repite el ejercicio anterior, pero si las señales dan información imposible se debe encender **todo** el 7 segmentos.',
   '**Cambio respecto al 4.8:** las ocho combinaciones imposibles dejan de ser indiferentes y valen 1 en las siete salidas. Un display totalmente encendido avisa al piloto de que algo falla. A cambio, el circuito crece: perdemos las simplificaciones que daban las $\\times$.',
   [('Tabla de verdad', tab(n48 + list(SEG), [list(bits(i, 4)) + [cols49[k][i] for k in SEG] for i in range(16)]) + '\n\nEs la tabla del 4.8 con las $\\times$ convertidas en 1.')] +
   [('Segmento $%s$' % k, rep49[k]) for k in SEG],
   'Las siete funciones del libro son mínimas, salvo una errata en $b$ (ver nota). Comparado con el 4.8, el circuito pasa de unos pocos cables a 3–4 productos por salida: **saber qué pasa con lo imposible cambia mucho el coste**. El término $EO$ (la combinación imposible «este y oeste») aparece en las siete salidas, y $NS$ («norte y sur») en cinco.\n\n@box ojo | Errata en el libro (función $b$)\nEn la fórmula del libro para $b$, el primer término está escrito con $\\bar E$ ($\\bar N\\bar S\\bar E$). Ese término valdría 1 en la fila 1 ($0001$, oeste), pero $b=0$ en esa fila. El término correcto es $\\bar N\\bar S\\bar O$ (cubre las filas 0 y 2). Se ha comprobado por código.\n@end')

# ============================================================== 4.10  decodificador BCD a 7 segmentos
n410 = ['B3', 'B2', 'B1', 'B0']; dc410 = list(range(10, 16))
PAT = {0: '1111110', 1: '0110000', 2: '1101101', 3: '1111001', 4: '0110011', 5: '1011011', 6: '0011111', 7: '1110000', 8: '1111111', 9: '1110011'}
cols410 = {s: [int(PAT[i][k]) if i < 10 else 0 for i in range(16)] for k, s in enumerate(SEG)}
bk410 = {'a': [0, 2, 3, 5, 7, 8, 9], 'b': [0, 1, 2, 3, 4, 7, 8, 9], 'c': [0, 1, 3, 4, 5, 6, 7, 8, 9], 'd': [0, 2, 3, 5, 6, 8], 'e': [0, 2, 6, 8], 'f': [0, 4, 5, 6, 8, 9], 'g': [2, 3, 4, 5, 6, 8, 9]}
for k, v in bk410.items():
    check('lb4.p410.sigma.' + k, minterms_of(cols410[k]) == v); book('lb4.p410.sigma.' + k, minterms_of(cols410[k]) == v)
printed9 = '1111001'      # fila 9 tal como está impresa en la tabla del libro (d=1, f=0)
check('lb4.p410.fila9_impresa_distinta', printed9 != PAT[9])
bt410 = {'a': ['!B2 !B0', 'B2 B0', 'B3', '!B2 B1'], 'b': ['!B1 !B0', '!B2', 'B1 B0'], 'c': ['!B1', 'B0', 'B2'],
         'd': ['!B2 !B0', 'B1 !B0', 'B2 !B1 B0', '!B2 B1'], 'e': ['!B2 !B0', 'B1 !B0'], 'f': ['!B1 !B0', 'B2 !B0', 'B2 !B1', 'B3'], 'g': ['B2 !B1', '!B2 B1', 'B3', 'B2 !B0']}
rep410 = {}; ok410 = True
for k in SEG:
    t, m, okb, same = sop_report('lb4.p410.' + k, n410, k, cols410[k], bt410[k], dc_idx=dc410); rep410[k] = t; ok410 &= bool(okb and same)
check('lb4.p410', ok410)
# variante: el 9 con segmento inferior (d=1, f=1, e=0) -> d cambia
col_d9 = list(cols410['d']); col_d9[9] = 1
mine_d9, _, _, _ = solve_sop('lb4.p410.d9', n410, [i for i in minterms_of(col_d9) if i < 10], dc410, None, 'd', kmap=False)
ej('lb4-10', 'Decodificador de BCD a 7 segmentos', 'Libro · Cap. 4 · P4.10', 'comb,karnaugh,7seg,bcd', 'lb4.p410',
   'Implementa el circuito más pequeño que convierta un dígito BCD $B_3B_2B_1B_0$ en las siete señales $a,b,c,d,e,f,g$ de un display de 7 segmentos.',
   '**Cómo se rellena la tabla:** ten delante un 7 segmentos dibujado y apunta qué segmentos forman cada cifra. Las filas 10 a 15 no son BCD y se dejan como indiferentes. El 6 se dibuja sin el segmento superior ($a=0$) y el 9 sin el inferior ($d=0$); son formas de escribirlos, no la única posible.',
   [('Tabla de verdad', table_x(n410, list(SEG), [cols410[k] for k in SEG], dc410) + '\n\nEjemplos: el 0 enciende todo menos $g$ ($1111110$); el 1, $b$ y $c$ ($0110000$); el 2, $a,b,d,e,g$ ($1101101$).')] +
   [('Segmento $%s$' % k, rep410[k]) for k in SEG] +
   [('Variante: el 9 con segmento inferior', 'Si se prefiere el 9 con el segmento $d$ encendido, solo cambia $d$, que pasa a valer 1 también en la fila 9: $d=%s$ (%d términos, frente a 4).' % (terms_tex(mine_d9), len(mine_d9)))],
   'Las siete simplificaciones del libro son correctas y de coste mínimo. Cada segmento necesita entre 1 y 4 productos. $c=\\bar B_1+B_0+B_2$ es el más sencillo (solo es 0 en los números 2).\n\n@box ojo | Errata en el libro (tabla)\nEn la tabla del libro, la fila del 9 aparece con $d=1$ y $f=0$ ($1111001$), que es justo lo contrario de lo que dicen sus propios sumatorios ($d=\\Sigma(0,2,3,5,6,8)$ no incluye el 9 y $f=\\Sigma(0,4,5,6,8,9)$ sí). Aquí se sigue la versión de los sumatorios y de las expresiones finales ($1110011$).\n@end')

# ============================================================== 4.11  comparador de dos números de 2 bits
n411 = ['A1', 'A0', 'B1', 'B0']
G411 = [1 if (i >> 2) > (i & 3) else 0 for i in range(16)]
E411 = [1 if (i >> 2) == (i & 3) else 0 for i in range(16)]
L411 = [1 if (i >> 2) < (i & 3) else 0 for i in range(16)]
bk411 = {'G': [4, 8, 9, 12, 13, 14], 'E': [0, 5, 10, 15], 'L': [1, 2, 3, 6, 7, 11]}
for k, c in (('G', G411), ('E', E411), ('L', L411)):
    check('lb4.p411.sigma.' + k, minterms_of(c) == bk411[k]); book('lb4.p411.sigma.' + k, minterms_of(c) == bk411[k])
check('lb4.p411.E_xnor', all(E411[i] == ((1 - ((bits(i, 4)[0]) ^ (bits(i, 4)[2]))) & (1 - ((bits(i, 4)[1]) ^ (bits(i, 4)[3])))) for i in range(16)))
bt411 = {'G': ['A0 !B1 !B0', 'A1 A0 !B0', 'A1 !B1'], 'E': ['!A1 !A0 !B1 !B0', 'A1 !A0 B1 !B0', '!A1 A0 !B1 B0', 'A1 A0 B1 B0'], 'L': ['!A1 !A0 B0', '!A0 B1 B0', '!A1 B1']}
rep411 = {}; ok411 = True
for k, nm in (('G', 'A>B'), ('E', 'A=B'), ('L', 'A<B')):
    c = {'G': G411, 'E': E411, 'L': L411}[k]
    t, m, okb, same = sop_report('lb4.p411.' + k, n411, k, c, bt411[k]); rep411[k] = t.replace('$%s=' % k, '$(%s)=' % nm, 1).replace('**$%s=' % k, '**$(%s)=' % nm); ok411 &= bool(okb and same)
check('lb4.p411', ok411)
ej('lb4-11', 'Comparador de dos números de 2 bits', 'Libro · Cap. 4 · P4.11', 'comb,karnaugh,comparador', 'lb4.p411',
   'Diseña un comparador de dos números $A=A_1A_0$ y $B=B_1B_0$ con tres salidas: $A>B$, $A=B$ y $A<B$.',
   '**Idea:** se comparan las dos cifras y se activa **una sola** de las tres salidas. Es un ejercicio muy sistemático: la tabla se escribe leyendo $A$ y $B$ como números de 0 a 3.',
   [('Tabla de verdad', tab(n411 + ['A>B', 'A=B', 'A<B'], [list(bits(i, 4)) + [G411[i], E411[i], L411[i]] for i in range(16)]) + '\n\nFila 0: $0=0$. Fila 3: $0<3$. Fila 8: $2>0$.'),
    ('Salida $A>B$', rep411['G']), ('Salida $A=B$', rep411['E'] + '\n\nLa igualdad es la diagonal del mapa y no se simplifica: cuatro minitérminos. Pero hay un truco: $A=B$ equivale a que **cada pareja de bits** coincida, es decir, $(A_1\\odot B_1)\\cdot(A_0\\odot B_0)$ con dos puertas XNOR y un AND. Es la forma habitual de hacerlo (verificada por código).'),
    ('Salida $A<B$', rep411['L'])],
   'Las tres funciones del libro son correctas y mínimas como suma de productos. La salida «$A=B$» es mucho más barata con XNOR que con cuatro AND de cuatro entradas.')

# ============================================================== 4.12  máquina registradora con vueltas
n412 = ['M25A', 'M25B', 'M10', 'M5']
val412 = [25 * a + 25 * b + 10 * c + 5 * d for a, b, c, d in (bits(i, 4) for i in range(16))]
chg = [max(v - 40, 0) for v in val412]
cols412 = {'PR': [1 if v >= 40 else 0 for v in val412], 'D5': [1 if (v >= 40 and chg[i] % 10 == 5) else 0 for i, v in enumerate(val412)],
           'D10A': [1 if c >= 10 else 0 for c in chg], 'D10B': [1 if c >= 20 else 0 for c in chg]}
check('lb4.p412.vueltas_correctas', all(chg[i] == 5 * cols412['D5'][i] + 10 * cols412['D10A'][i] + 10 * cols412['D10B'][i] for i in range(16) if cols412['PR'][i]))
bk412 = {'PR': [7, 11, 12, 13, 14, 15], 'D5': [13, 15], 'D10A': [12, 13, 14, 15], 'D10B': [14, 15]}
for k, v in bk412.items():
    check('lb4.p412.sigma.' + k, minterms_of(cols412[k]) == v); book('lb4.p412.sigma.' + k, minterms_of(cols412[k]) == v)
bt412 = {'PR': ['M25B M10 M5', 'M25A M10 M5', 'M25A M25B'], 'D5': ['M25A M25B M5'], 'D10A': ['M25A M25B'], 'D10B': ['M25A M25B M10']}
rep412 = {}; ok412 = True
for k in ['PR', 'D5', 'D10A', 'D10B']:
    t, m, okb, same = sop_report('lb4.p412.' + k, n412, k, cols412[k], bt412[k]); rep412[k] = t; ok412 &= bool(okb and same)
check('lb4.p412', ok412)
ej('lb4-12', 'Máquina registradora con cambio', 'Libro · Cap. 4 · P4.12', 'comb,karnaugh', 'lb4.p412',
   'Una máquina tiene cuatro ranuras, de 25, 25, 10 y 5 ptas (en cada una cabe una moneda). Entrega el producto cuando lo introducido llega a 40 ptas o más y devuelve el cambio con monedas de 5 y de 10. Salidas: producto $PR$, vuelta de 5 ($D_5$) y dos vueltas de 10 ($D_{10A}$, $D_{10B}$).',
   '**Sumar el dinero de cada fila:** $25A+25B+10+5$. Si llega a 40, se da producto y el cambio es lo que sobra, repartido con monedas de 10 primero y de 5 si queda una.',
   [('Tabla de verdad', tab(n412 + ['PR', 'D5', 'D10A', 'D10B'], [list(bits(i, 4)) + [cols412[k][i] for k in ['PR', 'D5', 'D10A', 'D10B']] for i in range(16)]) + '\n\nEjemplos: fila 7 ($25+10+5=40$): solo $PR$. Fila 12 ($25+25=50$): producto y 10 de vuelta ($D_{10A}$). Fila 13 ($55$): producto y 15 de vuelta ($D_{10A}$ y $D_5$). Fila 15 ($65$): producto y 25 de vuelta ($D_{10A},D_{10B},D_5$).'),
    ('Una decisión de diseño', 'Las filas intermedias (por ejemplo 10 ptas) no dan nada: la máquina está esperando más monedas. Además la fila 15 «no debería ocurrir», porque el producto ya habría salido antes. Aun así **no se dejan indiferentes**: un valor libre en la salida podría soltar monedas por error. Pon un valor seguro cuando un error cueste dinero.'),
    ('Producto $PR$', rep412['PR']), ('Vuelta de 5 ($D_5$)', rep412['D5']), ('Vuelta de 10 ($D_{10A}$)', rep412['D10A']), ('Vuelta de 10 ($D_{10B}$)', rep412['D10B'])],
   'Las cuatro funciones del libro son correctas y mínimas. $D_{10A}$ y $D_{10B}$ son simples ANDs: el cambio solo existe cuando se han metido las dos monedas de 25.')

# ============================================================== 4.13  nota en 7 segmentos con puertas NAND
n413 = ['N3', 'N2', 'N1', 'N0']; dc413 = list(range(11, 16))
SEG413 = {}
for i in range(11):
    SEG413[i] = 'g' if i <= 4 else 'a' if i == 5 else 'ab' if i == 6 else 'abc' if i in (7, 8) else 'abcd' if i == 9 else 'abcdef'
cols413 = {s: [1 if (i <= 10 and s in SEG413[i]) else 0 for i in range(16)] for s in SEG}
bk413 = {'a': list(range(5, 11)), 'b': list(range(6, 11)), 'c': list(range(7, 11)), 'd': [9, 10], 'e': [10], 'f': [10], 'g': list(range(0, 5))}
for k, v in bk413.items():
    check('lb4.p413.sigma.' + k, minterms_of(cols413[k]) == v); book('lb4.p413.sigma.' + k, minterms_of(cols413[k]) == v)
bt413 = {'a': ['N2 N0', 'N2 N1', 'N3'], 'b': ['N2 N1', 'N3'], 'c': ['N2 N1 N0', 'N3'], 'd': ['N3 N0', 'N3 N1'], 'e': ['N3 N1'], 'f': ['N3 N1'], 'g': ['!N3 !N2', '!N3 !N1 !N0']}
rep413 = {}; ok413 = True; mine413 = {}
for k in SEG:
    t, m, okb, same = sop_report('lb4.p413.' + k, n413, k, cols413[k], bt413[k], dc_idx=dc413); rep413[k] = t; ok413 &= bool(okb and same); mine413[k] = m
check('lb4.p413', ok413)
def nand_nand(ts, names, row):
    v = dict(zip(names, row)); lvl = []
    for t in ts:
        lits = [(1 - v[l[1:]]) if l.startswith('!') else v[l] for l in t.split()]
        lvl.append(1 - min(lits))                        # NAND
    return 1 - min(lvl) if lvl else 0                    # NAND de los productos negados
check('lb4.p413.nand_nand', all(nand_nand(bt413[k], n413, bits(i, 4)) == cols413[k][i] for k in SEG for i in range(11)))
# recuento de puertas NAND compartiendo términos idénticos y complementos
terms_all = []
for k in SEG:
    for t in bt413[k]:
        if t not in terms_all: terms_all.append(t)
l1 = [t for t in terms_all if len(t.split()) >= 2]
invs_in = sorted({l[1:] for t in l1 for l in t.split() if l.startswith('!')})
single_pos = sorted({t for t in terms_all if len(t.split()) == 1 and not t.startswith('!')})
single_neg = sorted({t for t in terms_all if len(t.split()) == 1 and t.startswith('!')})
outs_distinct = []
for k in SEG:
    if bt413[k] and tuple(sorted(bt413[k])) not in outs_distinct: outs_distinct.append(tuple(sorted(bt413[k])))
n_nand_l1 = len(l1); n_inv = len(invs_in); n_single = len(single_pos); n_out = len(outs_distinct)
check('lb4.p413.recuento', n_nand_l1 + n_inv + n_single + n_out > 0)
ej('lb4-13', 'Nota de un alumno en un 7 segmentos (solo NAND)', 'Libro · Cap. 4 · P4.13', 'comb,karnaugh,nand,7seg', 'lb4.p413',
   'La nota (0 a 10) llega en binario puro $N_3N_2N_1N_0$. Diseña con puertas NAND el circuito que la muestre en un 7 segmentos de cátodo común: suspenso (0–4) enciende $g$; aprobado (5), $a$; bien (6), $a,b$; notable (7–8), $a,b,c$; sobresaliente (9), $a,b,c,d$; matrícula (10), todos menos $g$.',
   '**Dos pasos:** (1) simplificar como suma de productos; (2) pasar a **NAND–NAND**: cada AND se sustituye por un NAND y la OR final por otro NAND. Por De Morgan el resultado no cambia, y una familia lógica solo necesita un tipo de puerta. Las filas 11 a 15 (notas imposibles) son indiferentes. Atención: aquí 10 es una nota válida (no confundir con BCD).',
   [('Tabla de verdad', table_x(n413, list(SEG), [cols413[k] for k in SEG], dc413)),
    ('Simplificación de las siete salidas', '\n\n'.join('**%s.** %s' % (k, rep413[k].split('. ', 1)[1] if False else rep413[k]) for k in SEG)),
    ('Paso a NAND–NAND', 'Regla: $S=T_1+T_2+\\dots=\\overline{\\overline{T_1}\\cdot\\overline{T_2}\\cdots}$. Cada producto $T_i$ de dos o más literales sale de una NAND; la salida es una NAND de todas ellas. Un literal solo, como $N_3$, entra a la NAND de salida a través de un inversor (una NAND con las entradas unidas). Aquí, compartiendo términos que se repiten ($N_2N_1$, $N_3N_1$) y con $e=f$ iguales:\n- %d NAND de dos o tres entradas para los productos,\n- %d NAND de salida distintas (las salidas $e$ y $f$ son la misma señal),\n- %d inversores para los complementos de entrada ($%s$) y %d para el literal suelto $N_3$.\nSe ha simulado por código el circuito NAND–NAND completo y da exactamente la tabla de verdad para las 11 notas válidas.' % (n_nand_l1, n_out, n_inv, ', '.join('\\overline{%s}' % tx(x) for x in invs_in), n_single))],
   'Las siete funciones del libro son correctas y mínimas. Se ve la lógica de las notas: $e$ y $f$ solo valen 1 en la matrícula ($N_3N_1$), $d$ en 9 y 10, y $g$ en el suspenso (0 a 4). Fíjate en que $N_3$ solo vale 1 a partir de 8, y las indiferentes de 11 a 15 permiten escribir «$N_3$» en vez de un producto largo.')

# ============================================================== 4.14  termómetro de dos leds
n414 = ['T3', 'T2', 'T1', 'T0']
sv = [i if i < 8 else i - 16 for i in range(16)]
LV = [1 if -3 <= v <= 4 else 0 for v in sv]; LR = [1 - x for x in LV]
check('lb4.p414.sigma', minterms_of(LV) == [0, 1, 2, 3, 4, 13, 14, 15] and minterms_of(LR) == list(range(5, 13)))
book('lb4.p414.sigma', minterms_of(LV) == [0, 1, 2, 3, 4, 13, 14, 15] and minterms_of(LR) == list(range(5, 13)))
bt414 = {'LV': ['!T3 !T1 !T0', 'T3 T2 T0', 'T3 T2 T1', '!T3 !T2'], 'LR': ['T3 !T1 !T0', '!T3 T2 T0', '!T3 T2 T1', 'T3 !T2']}
rep414 = {}; ok414 = True
for k, c in (('LV', LV), ('LR', LR)):
    t, m, okb, same = sop_report('lb4.p414.' + k, n414, k, c, bt414[k]); rep414[k] = t; ok414 &= bool(okb and same)
check('lb4.p414', ok414)
check('lb4.p414.LR_es_not_LV', all(LR[i] == 1 - LV[i] for i in range(16)))
ej('lb4-14', 'Termómetro con dos leds (verde/rojo)', 'Libro · Cap. 4 · P4.14', 'comb,karnaugh,c2', 'lb4.p414',
   'Activa el led verde $LV$ si la temperatura está entre $-3$ y $+4\\,^\\circ$C (ambas incluidas) y el rojo $LR$ en el resto. La temperatura llega en complemento a 2 con 4 bits $T_3T_2T_1T_0$.',
   '**Lectura en C2:** con 4 bits se representan los valores de $-8$ a $+7$. Las filas $0\\ldots7$ son $0\\ldots7$ y las filas $8\\ldots15$ son $-8\\ldots-1$.',
   [('Tabla de verdad', tab(n414 + ['grados', 'LV', 'LR'], [list(bits(i, 4)) + [('%+d' % sv[i]) if sv[i] else '0', LV[i], LR[i]] for i in range(16)]) + '\n\nEl rango verde es $0,1,2,3,4$ (filas 0–4) y $-3,-2,-1$ (filas 13–15): en total 8 de las 16 combinaciones.'),
    ('Led verde $LV$', rep414['LV']), ('Led rojo $LR$', rep414['LR'])],
   'Las dos funciones del libro son correctas y mínimas. Pero hay un atajo: $LR=\\overline{LV}$ (comprobado por código), así que basta **un inversor** detrás de $LV$ en vez de otros 4 AND y una OR.')

# ============================================================== 4.15  cambio de pesetas a euros
n415 = ['P5', 'P10', 'P25', 'P50']
CT = {8: 3, 4: 6, 2: 15, 1: 30}     # céntimos: 5, 10, 25 y 50 ptas
check('lb4.p415.conversion', all(round(p / 1.66386) == c for p, c in ((5, 3), (10, 6), (25, 15), (50, 30))))
COIN = [1, 2, 5, 10, 20]
def coins(c):
    out = []
    for v in (20, 10, 5, 2, 1):
        k = c // v; c -= k * v; out.append(k)
    return out[::-1]          # [E1,E2,E5,E10,E20]
cols415 = {}; dc415 = [i for i in range(16) if i not in (0, 1, 2, 4, 8)]
for j, nm in enumerate(['E1', 'E2', 'E5', 'E10', 'E20']):
    cols415[nm] = [coins(CT.get(i, 0))[j] if i in (0, 1, 2, 4, 8) else 0 for i in range(16)]
check('lb4.p415.monedas_suman', all(sum(c * v for c, v in zip([cols415[n][i] for n in ['E1', 'E2', 'E5', 'E10', 'E20']], COIN)) == CT.get(i, 0) for i in (0, 1, 2, 4, 8)))
bk415 = {'E1': [4, 8], 'E2': [8], 'E5': [2, 4], 'E10': [1, 2], 'E20': [1]}
for k, v in bk415.items():
    check('lb4.p415.sigma.' + k, minterms_of(cols415[k]) == v); book('lb4.p415.sigma.' + k, minterms_of(cols415[k]) == v)
bt415 = {'E1': ['P5', 'P10'], 'E2': ['P5'], 'E5': ['P25', 'P10'], 'E10': ['P50', 'P25'], 'E20': ['P50']}
rep415 = {}; ok415 = True
for k in ['E1', 'E2', 'E5', 'E10', 'E20']:
    t, m, okb, same = sop_report('lb4.p415.' + k, n415, k, cols415[k], bt415[k], dc_idx=dc415); rep415[k] = t; ok415 &= bool(okb and same)
check('lb4.p415', ok415)
ej('lb4-15', 'Cambio de pesetas a euros', 'Libro · Cap. 4 · P4.15', 'comb,karnaugh', 'lb4.p415',
   'Una máquina acepta por una única ranura monedas de 5, 10, 25 y 50 ptas y devuelve su valor en euros con monedas de 1, 2, 5, 10 y 20 céntimos (con redondeo). Cuatro señales $P_5,P_{10},P_{25},P_{50}$ indican qué moneda se ha introducido.',
   '**Conversión:** al cambio oficial de $166{,}386$ ptas por euro, 5 ptas son $3{,}005$ cént. (3), 10 ptas son 6, 25 ptas son 15 y 50 ptas son 30 (comprobado por código). Cada importe se reparte con las monedas disponibles: $3=2+1$, $6=5+1$, $15=10+5$, $30=20+10$.',
   [('Qué filas son válidas', 'Como la ranura es única, solo puede haber **una** moneda a la vez: son válidas la fila 0 (ninguna) y las filas con un único 1 (1, 2, 4 y 8). Las otras 11 filas son indiferentes.'),
    ('Tabla de verdad', table_x(n415, ['E1', 'E2', 'E5', 'E10', 'E20'], [cols415[k] for k in ['E1', 'E2', 'E5', 'E10', 'E20']], dc415) + '\n\nEjemplos: fila 2 (25 ptas): 15 cént. $=10+5$, salidas $00110$. Fila 8 (5 ptas): 3 cént. $=2+1$, salidas $11000$.')] +
   [('Salida $%s$' % k, rep415[k]) for k in ['E1', 'E2', 'E5', 'E10', 'E20']],
   'Con tantas indiferentes todo se reduce a cables y OR de dos entradas: $E_1=P_5+P_{10}$, $E_2=P_5$, $E_5=P_{25}+P_{10}$, $E_{10}=P_{50}+P_{25}$, $E_{20}=P_{50}$. Coinciden con el libro y son mínimas. Si se quisiera permitir varias monedas a la vez, habría que rehacer la tabla (el propio libro lo deja como ejercicio).')

# ============================================================== 4.16  semáforos de una rotonda
n416 = ['A', 'B', 'C', 'D']
FL = [5, 15, 25, 30]
flow = [sum(f for f, b in zip(FL, bits(i, 4)) if b) for i in range(16)]
dc416 = [i for i in range(16) if sum(bits(i, 4)) > 2]
check('lb4.p416.dc', dc416 == [7, 11, 13, 14, 15])
unit = [f // 5 for f in flow]
cols416 = {'SA': [(u >> 0) & 1 for u in unit], 'SB': [(u >> 1) & 1 for u in unit], 'SC': [(u >> 2) & 1 for u in unit], 'SD': [(u >> 3) & 1 for u in unit]}
check('lb4.p416.capacidades', all(5 * cols416['SA'][i] + 10 * cols416['SB'][i] + 20 * cols416['SC'][i] + 40 * cols416['SD'][i] == flow[i] for i in range(16)))
bk416 = {'SA': [2, 3, 4, 5, 8, 9], 'SB': [1, 3, 4, 9, 10], 'SC': [1, 2, 9, 10, 12], 'SD': [3, 5, 6]}
for k, v in bk416.items():
    on_ = [i for i in minterms_of(cols416[k]) if i not in dc416]
    check('lb4.p416.sigma.' + k, on_ == v); book('lb4.p416.sigma.' + k, on_ == v)
bt416 = {'SA': ['A !B !C', '!A B !C', '!A !B C'], 'SB': ['!B D', '!A B !C !D', 'A C'], 'SC': ['!B C !D', '!B !C D', 'A B'], 'SD': ['C D', 'B D', 'B C']}
rep416 = {}; ok416 = True
for k in ['SA', 'SB', 'SC', 'SD']:
    t, m, okb, same = sop_report('lb4.p416.' + k, n416, k, cols416[k], bt416[k], dc_idx=dc416); rep416[k] = t; ok416 &= bool(okb and same)
check('lb4.p416', ok416)
ej('lb4-16', 'Semáforos de una rotonda', 'Libro · Cap. 4 · P4.16', 'comb,karnaugh', 'lb4.p416',
   'Una rotonda tiene cuatro calles de entrada y cuatro de salida. Por la entrada $A$ llegan 5 coches/min, por $B$ 15, por $C$ 25 y por $D$ 30. Cuatro sensores indican por qué calles circulan coches. Las salidas $S_A,S_B,S_C,S_D$ pueden recoger 5, 10, 20 y 40 coches/min. Como mucho hay coches en dos calles de entrada a la vez. Activa los semáforos de salida para que salgan tantos coches como entran.',
   '**Es un convertidor de código:** divide el flujo total entre 5 y escríbelo en binario con pesos $1,2,4,8$ (que corresponden a 5, 10, 20 y 40). Por ejemplo, $35=7\\cdot5$, y $7=0111$: se abren las salidas de 5, 10 y 20.',
   [('Qué filas son válidas', 'Como mucho dos calles activas: son indiferentes las filas con tres o cuatro unos: 7, 11, 13, 14 y 15. El libro avisa de que poner $\\times$ aquí es algo arriesgado y que también se podrían fijar a 0 o a 1.'),
    ('Tabla de verdad', table_x(n416, ['SA', 'SB', 'SC', 'SD'], [cols416[k] for k in ['SA', 'SB', 'SC', 'SD']], dc416) + '\n\nEjemplos: fila 2 (entran 25): se abren $S_A$ y $S_C$ ($5+20$). Fila 6 (entran 40): solo $S_D$. Fila 9 (35): $S_A,S_B,S_C$. Fila 3 (55): $S_A,S_B,S_D$ ($5+10+40$).')] +
   [('Salida $%s$' % k, rep416[k]) for k in ['SA', 'SB', 'SC', 'SD']],
   'Las cuatro funciones del libro son correctas y mínimas. Se comprueba por código que los semáforos abiertos suman exactamente el flujo de entrada en las 11 filas válidas. $S_D=CD+BD+BC$ es una función **mayoría** de tres variables.')

# ============================================================== 4.17  transcodificador binario a dos dígitos BCD
n417 = ['E3', 'E2', 'E1', 'E0']
tens = [i // 10 for i in range(16)]; units = [i % 10 for i in range(16)]
cols417 = {'A3': [(t >> 3) & 1 for t in tens], 'A2': [(t >> 2) & 1 for t in tens], 'A1': [(t >> 1) & 1 for t in tens], 'A0': [t & 1 for t in tens],
           'B3': [(u >> 3) & 1 for u in units], 'B2': [(u >> 2) & 1 for u in units], 'B1': [(u >> 1) & 1 for u in units], 'B0': [u & 1 for u in units]}
bk417 = {'A3': [], 'A2': [], 'A1': [], 'A0': list(range(10, 16)), 'B3': [8, 9], 'B2': [4, 5, 6, 7, 14, 15], 'B1': [2, 3, 6, 7, 12, 13], 'B0': [1, 3, 5, 7, 9, 11, 13, 15]}
for k, v in bk417.items():
    check('lb4.p417.sigma.' + k, minterms_of(cols417[k]) == v); book('lb4.p417.sigma.' + k, minterms_of(cols417[k]) == v)
print_b2 = ['!E3 E2', 'E2 E0']; fix_b2 = ['!E3 E2', 'E2 E1']
check('lb4.p417.B2_impresa_falla', not all_rows_check('B2', n417, cols417['B2'], print_b2))
bt417 = {'A3': [], 'A2': [], 'A1': [], 'A0': ['E3 E1', 'E3 E2'], 'B3': ['E3 !E2 !E1'], 'B2': fix_b2, 'B1': ['E3 E2 !E1', '!E3 E1'], 'B0': ['E0']}
rep417 = {}; ok417 = True
for k in ['A0', 'B3', 'B2', 'B1', 'B0']:
    t, m, okb, same = sop_report('lb4.p417.' + k, n417, k, cols417[k], bt417[k]); rep417[k] = t; ok417 &= bool(okb and same)
check('lb4.p417', ok417)
check('lb4.p417.valor', all(10 * (8 * cols417['A3'][i] + 4 * cols417['A2'][i] + 2 * cols417['A1'][i] + cols417['A0'][i]) + 8 * cols417['B3'][i] + 4 * cols417['B2'][i] + 2 * cols417['B1'][i] + cols417['B0'][i] == i for i in range(16)))
ej('lb4-17', 'Transcodificador de binario a dos dígitos BCD', 'Libro · Cap. 4 · P4.17', 'comb,karnaugh,bcd', 'lb4.p417',
   'Implementa un transcodificador que pase un número en binario puro $E_3E_2E_1E_0$ (0 a 15) a dos dígitos BCD: decenas $A_3A_2A_1A_0$ y unidades $B_3B_2B_1B_0$.',
   '**Basta pasar a decimal y escribir en BCD.** Hasta 9 solo hay unidades. De 10 a 15 hay una decena (1) y las unidades son el número menos 10. Las tres cifras más significativas de las decenas valen siempre 0.',
   [('Tabla de verdad', tab(n417 + ['A3', 'A2', 'A1', 'A0', 'B3', 'B2', 'B1', 'B0'], [list(bits(i, 4)) + [cols417[k][i] for k in ['A3', 'A2', 'A1', 'A0', 'B3', 'B2', 'B1', 'B0']] for i in range(16)]) + '\n\nEjemplos: $9\\to0000\\,1001$; $10\\to0001\\,0000$; $15\\to0001\\,0101$.'),
    ('Decenas: $A_3=A_2=A_1=0$', 'Para 4 bits de entrada la decena solo puede ser 0 o 1, así que esas tres salidas son **la constante 0** (se pueden conectar a masa; el libro las deja por coherencia con el BCD).'),
    ('Decenas: $A_0$', rep417['A0']), ('Unidades: $B_3$', rep417['B3']), ('Unidades: $B_2$', rep417['B2']),
    ('Unidades: $B_1$', rep417['B1']), ('Unidades: $B_0$', rep417['B0'] + '\n\nEl bit menos significativo no cambia: $B_0=E_0$, un cable.')],
   'Se comprueba que $10\\cdot(\\text{decenas})+\\text{unidades}$ vale la entrada en las 16 filas. Las soluciones del libro son correctas y mínimas salvo una errata en $B_2$.\n\n@box ojo | Errata en el libro ($B_2$)\nEn la fórmula del libro $B_2=\\bar E_3E_2+E_2E_0$. El segundo término debe ser $E_2E_1$: con $E_2E_0$ la fila 13 ($1101$) daría $B_2=1$ (el 13 es $0001\\,0011$, y $B_2=0$) y la fila 14 ($1110$, que es $0001\\,0100$) daría 0 en vez de 1. Se ha comprobado por código.\n@end')
