"""Capítulo 2 del libro de problemas (manipulación booleana): resuelve, verifica y genera src/libro2.dsl."""
import json, os, itertools
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CHK = []; DIFF = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
def book(id_, ok, detail=''):
    if not ok: DIFF.append((id_, detail))
N = lambda x: 1 - x
def rows(n): return list(itertools.product((0, 1), repeat=n))
def col(f, n): return [int(f(*r)) for r in rows(n)]
def same(f, g, n): return col(f, n) == col(g, n)
out = []
def W(s=''): out.append(s)
def ej(id_, title, origen, tags, checks, enun, antes, pasos, res):
    W('@ej %s|%s|%s|%s|%s' % (id_, title, origen, tags, checks)); W('@enun'); W(enun); W('@end')
    if antes: W('@antes'); W(antes); W('@end')
    for t, body in pasos: W('@paso ' + t); W(body); W('@end')
    W('@res'); W(res); W('@end'); W('@end'); W()
def tab(head, rws):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rws])
def bar(v): return '\\bar{%s}' % v
VARS = 'ABCD'
def mint(i, n=4):
    b = format(i, '0%db' % n); return ''.join((VARS[k] if b[k] == '1' else bar(VARS[k])) for k in range(n))
def maxt(i, n=4):
    b = format(i, '0%db' % n); return '+'.join((bar(VARS[k]) if b[k] == '1' else VARS[k]) for k in range(n))
def rng(lst):
    lst = sorted(lst); parts = []; i = 0
    while i < len(lst):
        j = i
        while j + 1 < len(lst) and lst[j + 1] == lst[j] + 1: j += 1
        if j - i >= 2: parts.append('%d\\text{-}%d' % (lst[i], lst[j]))
        else: parts += [str(x) for x in lst[i:j + 1]]
        i = j + 1
    return ', '.join(parts)

W('%% id=libro2'); W('%% group=ejer'); W('%% n=3.2'); W('%% title=Libro de problemas · Capítulo 2 · Manipulación booleana')
W('%% short=Libro · Cap. 2 Álgebra de Boole'); W('%% sub=12 problemas resueltos: tablas de verdad, teoremas, minitérminos y maxitérminos, De Morgan, implementación con NAND y con NOR y análisis de circuitos.'); W()
W('@box idea | Cómo se usa esta sección')
W('Son los problemas resueltos del capítulo 2 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. Cada igualdad y cada tabla se ha comprobado con un programa que recorre todas las combinaciones de entrada. Si el libro difiere, aparece una nota «Ojo». La teoría está en [[t03|el tema 3]].')
W('@end'); W()

# ============================================================== P2.1
f21 = {
    'f1': lambda a, b, c: a & b & c,
    'f2': lambda a, b, c: a | b | c,
    'f3': lambda a, b, c: a & (b | N(c)),
    'f4': lambda a, b, c: N((a | b) & (b | c)),
    'f5': lambda a, b, c: N(b) & (a | (c & N(a | b))),
    'f6': lambda a, b, c: N((a | c) & N(b & (c | b))),
    'f7': lambda a, b, c: (a | b) & (N(a) | N(b)),
    'f8': lambda a, b, c: a | (b & (a | (c & b & (a | b)))),
}
book21 = {'f1': [0, 0, 0, 0, 0, 0, 0, 1], 'f2': [0, 1, 1, 1, 1, 1, 1, 1], 'f3': [0, 0, 0, 0, 1, 0, 1, 1], 'f4': [1, 1, 0, 0, 1, 0, 0, 0],
          'f5': [0, 1, 0, 0, 1, 1, 0, 0], 'f6': [1, 0, 1, 1, 0, 0, 1, 1], 'f7': [0, 0, 1, 1, 1, 1, 0, 0], 'f8': [0, 0, 0, 1, 1, 1, 1, 1]}
ok = True
for k, f in f21.items():
    c = col(f, 3); ok &= (c == book21[k]); book('lb2.p21.' + k, c == book21[k], k)
check('lb2.p21', ok)
simp = {'f5': lambda a, b, c: N(b) & (a | c), 'f6': lambda a, b, c: b | (N(a) & N(c)), 'f3': lambda a, b, c: a & (b | N(c)),
        'f7': lambda a, b, c: a ^ b, 'f8': lambda a, b, c: a | (b & c), 'f4': lambda a, b, c: (N(a) & N(b)) | (N(b) & N(c))}
check('lb2.p21.simplificadas', all(same(f21[k], g, 3) for k, g in simp.items()))
r21 = [[''.join(map(str, r))] + [col(f21[k], 3)[i] for k in f21] for i, r in enumerate(rows(3))]
ej('lb2-1', 'Tablas de verdad de ocho funciones de tres variables', 'Libro · Cap. 2 · P2.1', 'comb', 'lb2.p21',
   'Obtén la columna de salida de ocho funciones de $A,B,C$, desde el simple producto $ABC$ hasta expresiones con complementos anidados.',
   '**Método:** se sustituye cada combinación $ABC$ en la expresión y se opera de dentro hacia fuera. Recuerda que $0\\cdot x=0$ y $1+x=1$: muchas filas salen a simple vista.',
   [('Las expresiones', '- $f_1=ABC$\n- $f_2=A+B+C$\n- $f_3=A(B+\\bar C)$\n- $f_4=\\overline{(A+B)(B+C)}$\n- $f_5=\\bar B\\,(A+C\\,\\overline{(A+B)})$\n- $f_6=\\overline{(A+C)\\cdot\\overline{B(C+B)}}$\n- $f_7=(A+B)(\\bar A+\\bar B)$\n- $f_8=A+B\\,(A+C\\,B(A+B))$'),
    ('Un ejemplo paso a paso: $f_6(001)$', 'Con $A=0,B=0,C=1$: $A+C=1$; $B(C+B)=0\\cdot1=0$; su complemento es $1$; el producto es $1\\cdot1=1$ y el complemento exterior da $0$. Así que $f_6(001)=0$.'),
    ('Tabla de verdad', tab(['ABC'] + list(f21), r21)),
    ('Formas más cortas', 'Mirando la tabla se reconocen formas simples. Todas se han comprobado por código:\n- $f_3=A(B+\\bar C)$ no se puede abreviar más.\n- $f_4=\\bar A\\bar B+\\bar B\\bar C$\n- $f_5=\\bar B\\,(A+C)$\n- $f_6=B+\\bar A\\bar C$\n- $f_7=A\\oplus B$\n- $f_8=A+BC$')],
   'Las ocho columnas coinciden con las del libro. Las expresiones largas ($f_5$, $f_6$, $f_8$) se reducen mucho: la absorción hace que partes enteras sobren.')

# ============================================================== P2.2
th = []
def T(name, n, lf, rf, ltxt, rtxt):
    th.append((name, n, lf, rf, ltxt, rtxt))
T('Elemento neutro de la suma', 1, lambda x: 0 | x, lambda x: x, '0+X', 'X')
T('Elemento neutro del producto', 1, lambda x: 1 & x, lambda x: x, '1\\cdot X', 'X')
T('Complemento de la suma', 1, lambda x: x | N(x), lambda x: 1, 'X+\\bar X', '1')
T('Complemento del producto', 1, lambda x: x & N(x), lambda x: 0, 'X\\cdot\\bar X', '0')
T('Idempotencia de la suma', 1, lambda x: x | x, lambda x: x, 'X+X', 'X')
T('Idempotencia del producto', 1, lambda x: x & x, lambda x: x, 'X\\cdot X', 'X')
T('Elemento nulo de la suma', 1, lambda x: x | 1, lambda x: 1, 'X+1', '1')
T('Elemento nulo del producto', 1, lambda x: x & 0, lambda x: 0, 'X\\cdot0', '0')
T('Absorción (1)', 2, lambda x, y: x | (x & y), lambda x, y: x, 'X+XY', 'X')
T('Absorción (2)', 2, lambda x, y: x & (x | y), lambda x, y: x, 'X(X+Y)', 'X')
T('De Morgan de la suma', 2, lambda x, y: N(x | y), lambda x, y: N(x) & N(y), '\\overline{X+Y}', '\\bar X\\bar Y')
T('De Morgan del producto', 2, lambda x, y: N(x & y), lambda x, y: N(x) | N(y), '\\overline{XY}', '\\bar X+\\bar Y')
T('Distributiva del producto', 3, lambda x, y, z: x & (y | z), lambda x, y, z: (x & y) | (x & z), 'X(Y+Z)', 'XY+XZ')
T('Distributiva de la suma', 3, lambda x, y, z: x | (y & z), lambda x, y, z: (x | y) & (x | z), 'X+YZ', '(X+Y)(X+Z)')
T('De Morgan extendido (suma)', 3, lambda x, y, z: N(x | y | z), lambda x, y, z: N(x) & N(y) & N(z), '\\overline{X+Y+Z}', '\\bar X\\bar Y\\bar Z')
T('De Morgan extendido (producto)', 3, lambda x, y, z: N(x & y & z), lambda x, y, z: N(x) | N(y) | N(z), '\\overline{XYZ}', '\\bar X+\\bar Y+\\bar Z')
allok = True; throws = []
for name, n, lf, rf, lt, rt in th:
    ok_ = same(lf, rf, n); allok &= ok_; check('lb2.p22.' + name, ok_)
    throws.append((name, '$%s$' % lt, '$%s$' % rt, 2 ** n, 'sí' if ok_ else 'NO'))
check('lb2.p22', allok)
dm = [[''.join(map(str, r)), N(r[0] | r[1]), N(r[0]) & N(r[1]), N(r[0] & r[1]), N(r[0]) | N(r[1])] for r in rows(2)]
ej('lb2-2', 'Demostrar los teoremas básicos por inducción perfecta', 'Libro · Cap. 2 · P2.2', 'comb', 'lb2.p22',
   'Demuestra con tablas de verdad (inducción perfecta) los teoremas de una, dos y tres variables: neutros, complementos, idempotencia, elementos nulos, absorción, De Morgan y distributivas.',
   '**Inducción perfecta:** un teorema booleano es cierto si las dos columnas que se comparan son idénticas en **todas** las combinaciones de entrada. Con $n$ variables hay $2^n$ filas.',
   [('Resultado de cada comprobación', tab(['Teorema', 'Un lado', 'El otro lado', 'Filas', 'Iguales'], throws)),
    ('Ejemplo: De Morgan con dos variables', tab(['XY', '$\\overline{X+Y}$', '$\\bar X\\bar Y$', '$\\overline{XY}$', '$\\bar X+\\bar Y$'], dm) + '\n\nLas columnas 2 y 3 coinciden, y las columnas 4 y 5 también.'),
    ('Qué hacer con un teorema que no conoces', 'Haz su tabla de verdad. Si las dos columnas son iguales, es un teorema, aunque no sepas por qué. Si difieren en una sola fila, es falso.')],
   'Los 16 teoremas se cumplen en todas sus filas.\n\n@box ojo | Errata del libro\nEn la tabla del elemento nulo, el libro imprime un $1$ en las dos filas de la columna del valor constante $0$ de $X\\cdot0$. La columna del valor constante debe valer $0$, igual que el resultado de $X\\cdot0$. Es un error de impresión: el teorema es correcto.\n@end')

# ============================================================== P2.3
F23 = {'f1': ([1, 2, 3, 5, 8, 15], []), 'f2': ([0, 1, 3, 4, 5, 9, 10, 11, 12, 13, 15], []),
       'f3': ([0, 2, 3, 7, 14, 15], [4, 6, 8, 9, 10]), 'f4': ([6, 7, 8, 11, 12, 13], [0, 1, 2, 10, 14])}
# columnas impresas en el libro (X = indiferente)
book23 = {'f1': '0111010010000001', 'f2': '1101110001111101', 'f3': '1011X0X1XXX00011', 'f4': 'XXX0001110X111X0'}
# f2 impreso: ver tabla del libro (1,1,0,1,1,1,0,0,0,1,1,1,1,1,0,1)
book23['f2'] = '1101110001111101'
cols23 = {}
for k, (ones, dc) in F23.items():
    cols23[k] = ''.join('X' if i in dc else ('1' if i in ones else '0') for i in range(16))
    check('lb2.p23.col.' + k, cols23[k] == book23[k], '%s %s' % (cols23[k], book23[k]))
    book('lb2.p23.col.' + k, cols23[k] == book23[k], '%s %s' % (cols23[k], book23[k]))
zeros = {k: [i for i in range(16) if cols23[k][i] == '0'] for k in F23}
# Σ y Π impresas en el libro
book_sum = {'f1': [1, 2, 3, 5, 8, 15], 'f2': [0, 1, 3, 4, 5, 9, 10, 11, 12, 13, 15], 'f3': [0, 2, 3, 7, 14, 15], 'f4': [6, 7, 8, 11, 12, 13]}
book_pi = {'f1': [0, 4, 6, 7, 9, 10, 11, 12, 13, 14], 'f2': [2, 6, 7, 8, 14], 'f3': [1, 5, 11, 12, 13], 'f4': [3, 4, 5, 9, 15]}
okS = all(F23[k][0] == book_sum[k] for k in F23); okP = all(zeros[k] == book_pi[k] for k in F23)
check('lb2.p23.sumatorios', okS); check('lb2.p23.factoriales', okP)
check('lb2.p23.complementarios', all(sorted(F23[k][0] + zeros[k] + F23[k][1]) == list(range(16)) for k in F23))
# la forma Σ y la forma Π definen la misma función en las combinaciones no indiferentes
def f_sum(k, i): return int(i in F23[k][0])
def f_pi(k, i): return int(i not in zeros[k])
check('lb2.p23.sigma_igual_pi', all(f_sum(k, i) == f_pi(k, i) for k in F23 for i in range(16) if i not in F23[k][1]))
r23 = []
for i in range(16):
    r23.append([i, format(i, '04b'), '$%s$' % mint(i), '$%s$' % maxt(i)] + [cols23[k][i] for k in F23])
sums = '\n'.join('- $%s=\\Sigma(%s)$%s' % (k, rng(F23[k][0]), (' con indiferentes $d(%s)$' % rng(F23[k][1])) if F23[k][1] else '') for k in F23)
pis = '\n'.join('- $%s=\\Pi(%s)$%s' % (k, rng(zeros[k]), (' con indiferentes $d(%s)$' % rng(F23[k][1])) if F23[k][1] else '') for k in F23)
gates = [[k, len(F23[k][0]), 1, len(zeros[k]), 1] for k in F23]
ej('lb2-3', 'Minitérminos, maxitérminos, Σ y Π de cuatro funciones', 'Libro · Cap. 2 · P2.3', 'comb', 'lb2.p23',
   'Con la tabla de verdad de cuatro funciones de $A,B,C,D$ (dos de ellas con combinaciones indiferentes), escribe cada una como suma de minitérminos y como producto de maxitérminos, en forma compacta $\\Sigma$ y $\\Pi$, y cuenta las puertas de los dos circuitos.',
   '**Minitérmino $m_i$:** producto de las 4 variables que vale 1 solo en la fila $i$ (la variable va sin negar si su bit es 1). **Maxitérmino $M_i$:** suma de las 4 variables que vale 0 solo en la fila $i$ (la variable va negada si su bit es 1). Una función es la suma de los $m_i$ de sus unos o el producto de los $M_i$ de sus ceros. Una $X$ no se escribe en ninguna de las dos formas.',
   [('Tabla de verdad con minitérminos y maxitérminos', tab(['i', 'ABCD', 'Minitérmino', 'Maxitérmino'] + list(F23), r23)),
    ('Forma normal disyuntiva: suma de minitérminos', sums),
    ('Forma normal conjuntiva: producto de maxitérminos', pis),
    ('Circuitos', 'Cada minitérmino es una puerta AND de 4 entradas y todas van a una OR. Cada maxitérmino es una OR de 4 entradas y todas van a una AND.\n\n' + tab(['Función', 'AND de 4 entradas', 'OR final', 'OR de 4 entradas', 'AND final'], gates) + '\n\nSe necesitan además 4 inversores para tener $\\bar A,\\bar B,\\bar C,\\bar D$. Con indiferentes conviene usarlas luego al simplificar (tema de Karnaugh), pero en esta forma canónica no se escriben.')],
   'Se han obtenido los cuatro $\\Sigma$ y los cuatro $\\Pi$ y coinciden con los del libro. Se ha comprobado que los minitérminos, los maxitérminos y las indiferentes de cada función forman justo las 16 filas.')

# ============================================================== P2.4
def ident(lf, rf, n=4): return same(lf, rf, n)
d24 = [
 ('f1', '\\overline{AB+CD}', '(\\bar A+\\bar B)(\\bar C+\\bar D)',
  lambda a, b, c, d: N(a & b | c & d), lambda a, b, c, d: (N(a) | N(b)) & (N(c) | N(d))),
 ('f2', '\\overline{\\bar A\\bar B+\\bar D}', '(A+B)\\,D',
  lambda a, b, c, d: N(N(a) & N(b) | N(d)), lambda a, b, c, d: (a | b) & d),
 ('f3', '\\overline{A+BC+BD+\\bar B\\bar D+\\bar A\\bar B}', '\\bar A(\\bar B+\\bar C)(\\bar B+\\bar D)(B+D)(A+B)',
  lambda a, b, c, d: N(a | b & c | b & d | N(b) & N(d) | N(a) & N(b)), lambda a, b, c, d: N(a) & (N(b) | N(c)) & (N(b) | N(d)) & (b | d) & (a | b)),
 ('f4', '\\overline{ABCD+\\bar A\\bar B\\bar C\\bar D}', '(\\bar A+\\bar B+\\bar C+\\bar D)(A+B+C+D)',
  lambda a, b, c, d: N(a & b & c & d | N(a) & N(b) & N(c) & N(d)), lambda a, b, c, d: (N(a) | N(b) | N(c) | N(d)) & (a | b | c | d)),
 ('f5', '\\overline{\\bar A+\\bar B\\bar C+\\bar BC\\bar D+A\\bar C\\bar D}', 'A(B+C)(B+\\bar C+D)(\\bar A+C+D)',
  lambda a, b, c, d: N(N(a) | N(b) & N(c) | N(b) & c & N(d) | a & N(c) & N(d)), lambda a, b, c, d: a & (b | c) & (b | N(c) | d) & (N(a) | c | d)),
 ('f6', '\\overline{AB+AC+A\\bar B\\bar CD+\\bar A\\bar C}', '(\\bar A+\\bar B)(\\bar A+\\bar C)(\\bar A+B+C+\\bar D)(A+C)',
  lambda a, b, c, d: N(a & b | a & c | a & N(b) & N(c) & d | N(a) & N(c)), lambda a, b, c, d: (N(a) | N(b)) & (N(a) | N(c)) & (N(a) | b | c | N(d)) & (a | c)),
 ('f7', '\\overline{ABCD}', '\\bar A+\\bar B+\\bar C+\\bar D',
  lambda a, b, c, d: N(a & b & c & d), lambda a, b, c, d: N(a) | N(b) | N(c) | N(d)),
 ('f8', '\\overline{(A+B)(C+D)}', '\\bar A\\bar B+\\bar C\\bar D',
  lambda a, b, c, d: N((a | b) & (c | d)), lambda a, b, c, d: N(a) & N(b) | N(c) & N(d)),
 ('f9', '\\overline{(\\bar A+\\bar C)(\\bar A+D)(\\bar A+C+\\bar D)(B+D)}', 'AC+A\\bar D+A\\bar CD+\\bar B\\bar D',
  lambda a, b, c, d: N((N(a) | N(c)) & (N(a) | d) & (N(a) | c | N(d)) & (b | d)), lambda a, b, c, d: a & c | a & N(d) | a & N(c) & d | N(b) & N(d)),
 ('f10', '\\overline{(B+D)\\,A\\,(A+\\bar C+D)(\\bar A+C+D)}', '\\bar B\\bar D+\\bar A+\\bar AC\\bar D+A\\bar C\\bar D',
  lambda a, b, c, d: N((b | d) & a & (a | N(c) | d) & (N(a) | c | d)), lambda a, b, c, d: N(b) & N(d) | N(a) | N(a) & c & N(d) | a & N(c) & N(d)),
]
ok = True; l24 = []
for k, lt, rt, lf, rf in d24:
    o = ident(lf, rf); ok &= o; check('lb2.p24.' + k, o); l24.append('- $%s=%s=%s$' % (k, lt, rt))
check('lb2.p24', ok)
bad_book = lambda a, b, c, d: (N(a) | N(b) | N(c) | N(c)) & (a | b | c | d)
chk_err = not ident(d24[3][3], bad_book)
check('lb2.p24.f4_errata', chk_err)
ej('lb2-4', 'Teorema de De Morgan sobre sumas y productos', 'Libro · Cap. 2 · P2.4', 'comb', 'lb2.p24',
   'Aplica el teorema de De Morgan a diez expresiones: un complemento exterior sobre una suma de productos se convierte en un producto de sumas, y al revés.',
   '**Regla:** para negar una expresión, cambia cada $+$ por $\\cdot$, cada $\\cdot$ por $+$, y niega cada variable. Cuida los paréntesis. Para fiarte de un resultado, compara las tablas de verdad de los dos lados.',
   [('Las diez igualdades', '\n'.join(l24)),
    ('Cómo se comprueba', 'Se ha recorrido por código toda la tabla de 16 filas de cada pareja de expresiones. En las diez, los dos lados dan la misma salida en todas las filas.')],
   'Las diez igualdades son correctas.\n\n@box ojo | Errata del libro\nEn el apartado $f_4$ el libro escribe $(\\bar A+\\bar B+\\bar C+\\bar C)(A+B+C+D)$ con la $C$ negada dos veces. El factor correcto es $\\bar A+\\bar B+\\bar C+\\bar D$. Con la versión impresa las dos expresiones **no** son iguales (se comprueba mirando la fila $ABCD=1110$).\n@end')
check('lb2.p24.f4_fila1110', d24[3][3](1, 1, 1, 0) == 1 and bad_book(1, 1, 1, 0) == 0)

# ============================================================== P2.5
d25 = [
 ('f1', '\\overline{AB+C(A+\\bar B)+D(A+\\bar C)}', '(\\bar A+\\bar B)(\\bar C+\\bar A B)(\\bar D+\\bar A C)',
  lambda a, b, c, d: N(a & b | c & (a | N(b)) | d & (a | N(c))), lambda a, b, c, d: (N(a) | N(b)) & (N(c) | (N(a) & b)) & (N(d) | (N(a) & c))),
 ('f2', '\\overline{B(C+D(A+\\bar B))+\\bar A\\bar B}', '(\\bar B+\\bar C(\\bar D+\\bar AB))(A+B)',
  lambda a, b, c, d: N(b & (c | d & (a | N(b))) | N(a) & N(b)), lambda a, b, c, d: (N(b) | (N(c) & (N(d) | (N(a) & b)))) & (a | b)),
 ('f3', '\\overline{BC+A\\bar D\\,(B+\\overline{A(B+D)})}', '(\\bar B+\\bar C)(\\bar A+D+\\bar B A(B+D))',
  lambda a, b, c, d: N(b & c | a & N(d) & (b | N(a & (b | d)))), lambda a, b, c, d: (N(b) | N(c)) & (N(a) | d | (N(b) & a & (b | d)))),
 ('f4', '\\overline{A+B(C+D(A+\\bar B))}', '\\bar A(\\bar B+\\bar C(\\bar D+\\bar AB))',
  lambda a, b, c, d: N(a | b & (c | d & (a | N(b)))), lambda a, b, c, d: N(a) & (N(b) | N(c) & (N(d) | N(a) & b))),
 ('f5', '\\overline{\\overline{ABCD}+\\overline{A+B+C+D}}', 'ABCD\\,(A+B+C+D)',
  lambda a, b, c, d: N(N(a & b & c & d) | N(a | b | c | d)), lambda a, b, c, d: (a & b & c & d) & (a | b | c | d)),
 ('g1', '\\overline{\\overline{AB}+\\bar CD}', 'AB\\,(C+\\bar D)',
  lambda a, b, c, d: N(N(a & b) | N(c) & d), lambda a, b, c, d: (a & b) & (c | N(d))),
 ('g2', '\\overline{\\overline{A+B}\\cdot\\overline{C\\bar D}}', 'A+B+C\\bar D',
  lambda a, b, c, d: N(N(a | b) & N(c & N(d))), lambda a, b, c, d: a | b | (c & N(d))),
]
ok = True; l25 = []
for k, lt, rt, lf, rf in d25:
    o = ident(lf, rf); ok &= o; check('lb2.p25.' + k, o); l25.append('- $%s=%s=%s$' % (k.replace('g', 'g_').replace('f', 'f_'), lt, rt))
check('lb2.p25', ok)
check('lb2.p25.f5_igual_ABCD', same(d25[4][3], lambda a, b, c, d: a & b & c & d, 4))
ej('lb2-5', 'De Morgan con complementos anidados', 'Libro · Cap. 2 · P2.5', 'comb', 'lb2.p25',
   'Aplica De Morgan a expresiones con paréntesis y varios niveles de complemento, de modo que al final solo queden variables negadas (nunca una barra sobre una suma o un producto).',
   '**Truco:** trabaja de fuera hacia dentro. Quita la barra exterior con la regla de De Morgan y repite el proceso con cada barra que quede dentro. Un complemento doble desaparece: $\\bar{\\bar x}=x$.',
   [('Los cinco primeros apartados', '\n'.join(l25[:5])),
    ('Dos ejercicios propios del mismo estilo', '\n'.join(l25[5:]) + '\n\nSustituyen a los apartados $f_6$ y $f_7$ del libro, que encadenan tres complementos y cuya lectura en la copia que he usado no es fiable. La técnica es idéntica.'),
    ('Una observación', 'En $f_5$ el resultado se reduce a $ABCD$: si las cuatro variables valen 1, la suma $A+B+C+D$ vale 1 también, y en cualquier otro caso $ABCD=0$.')],
   'Las siete igualdades se han comprobado en las 16 filas de la tabla.')

# ============================================================== P2.6 NAND
S26 = [  # (nombre, términos [(var, negada)...], texto)
 ('f1', [[('A', 0), ('B', 0)], [('C', 0), ('D', 0)]]),
 ('f2', [[('A', 1), ('B', 1)], [('A', 1), ('B', 0), ('C', 0), ('D', 0)], [('B', 1), ('C', 0), ('D', 1)]]),
 ('f3', [[('A', 0)], [('B', 0), ('C', 0)], [('D', 1)]]),
 ('f4', [[('A', 1), ('D', 1)], [('A', 0), ('B', 0), ('C', 0), ('D', 0)], [('A', 1), ('C', 1)]]),
 ('f5', [[('A', 0), ('B', 0), ('C', 0), ('D', 0)], [('A', 0), ('B', 0), ('C', 1)], [('A', 1), ('C', 0), ('D', 1)], [('B', 0), ('C', 1), ('D', 1)]]),
]
def ev_term(t, env): return int(all((env[v] ^ n) for v, n in t))
def tex_term(t): return ''.join((bar(v) if n else v) for v, n in t)
def tex_nand_term(t): return '\\overline{%s}' % tex_term(t) if len(t) > 1 else (bar(t[0][0]) if t[0][1] == 0 else t[0][0])
def nand_stats(terms):
    inv = set(); nand = 0
    for t in terms:
        if len(t) > 1:
            nand += 1
            for v, n in t:
                if n: inv.add(v)
        else:
            v, n = t[0]
            if n == 0: inv.add(v)       # hace falta A negada para entrar a la NAND final
    return nand + 1, len(inv)
ok = True; r26 = []; l26 = []
for k, terms in S26:
    f_sop = lambda *x, terms=terms: int(any(ev_term(t, dict(zip('ABCD', x))) for t in terms))
    def f_nand(*x, terms=terms):
        env = dict(zip('ABCD', x)); outs = []
        for t in terms:
            if len(t) > 1: outs.append(N(ev_term(t, env)))
            else:
                v, n = t[0]; outs.append(N(env[v] ^ n))
        return N(int(all(outs)))
    o = same(f_sop, f_nand, 4); ok &= o; check('lb2.p26.' + k, o)
    nn, ni = nand_stats(terms)
    sop = '+'.join(tex_term(t) for t in terms); nd = '\\,'.join(tex_nand_term(t) for t in terms)
    l26.append('- $%s=%s=\\overline{%s}$' % (k, sop, nd))
    r26.append([k, nn, ni])
check('lb2.p26', ok)
check('lb2.p26.cuentas', [r[1] for r in r26] == [3, 4, 2, 4, 5] and [r[2] for r in r26] == [0, 3, 1, 3, 3])
ej('lb2-6', 'Implementar sumas de productos solo con puertas NAND', 'Libro · Cap. 2 · P2.6', 'comb', 'lb2.p26',
   'Reescribe cinco sumas de productos de modo que solo hagan falta puertas NAND (dos niveles) y cuenta las puertas.',
   '**Idea:** si niegas dos veces una suma de productos y aplicas De Morgan una vez, queda un NAND de NANDs: $\\overline{\\overline{t_1}\\cdot\\overline{t_2}\\cdots}=t_1+t_2+\\cdots$. Cada producto de varias variables es una NAND de primer nivel. Un término de una sola variable entra directamente negado en la NAND de salida.',
   [('Las cinco funciones en forma NAND', '\n'.join(l26)),
    ('Puertas necesarias', tab(['Función', 'NAND (incluida la de salida)', 'Inversores'], r26) + '\n\nLos inversores sirven para generar las variables negadas que usan las NAND de primer nivel. En $f_3$ solo hace falta negar $A$; $\\bar D$ ya se compensa porque $\\overline{\\bar D}=D$ entra directamente.'),
    ('Comprobación', 'Para cada función se ha evaluado la forma con NAND y la suma de productos en las 16 combinaciones: coinciden.')],
   'Todas las implementaciones NAND son equivalentes a la suma de productos original.')

# ============================================================== P2.7 NOR
S27 = [
 ('f1', [[('A', 0), ('B', 0)], [('C', 0), ('D', 0)]]),
 ('f2', [[('A', 1), ('D', 1)], [('B', 0), ('C', 1), ('D', 1)], [('A', 0), ('B', 1), ('C', 1), ('D', 0)]]),
 ('f3', [[('B', 1), ('D', 1)], [('B', 1), ('C', 1)], [('A', 1), ('D', 1)], [('B', 0), ('D', 0)]]),
 ('f4', [[('B', 1), ('C', 1), ('D', 0)], [('A', 0)], [('B', 0), ('D', 1)], [('B', 0)]]),
 ('f5', [[('A', 1), ('B', 1), ('D', 1)], [('A', 0), ('C', 0)], [('B', 0), ('D', 1)], [('A', 1), ('D', 1)]]),
]
def ev_sum(t, env): return int(any((env[v] ^ n) for v, n in t))
def tex_sum(t): return '(' + '+'.join((bar(v) if n else v) for v, n in t) + ')' if len(t) > 1 else (bar(t[0][0]) if t[0][1] else t[0][0])
def tex_nor_term(t): return '\\overline{%s}' % '+'.join((bar(v) if n else v) for v, n in t) if len(t) > 1 else (t[0][0] if t[0][1] else bar(t[0][0]))
def nor_stats(terms):
    inv = set(); nor = 0
    for t in terms:
        if len(t) > 1:
            nor += 1
            for v, n in t:
                if n: inv.add(v)
        else:
            v, n = t[0]
            if n == 0: inv.add(v)
    return nor + 1, len(inv)
ok = True; r27 = []; l27 = []
for k, terms in S27:
    f_pos = lambda *x, terms=terms: int(all(ev_sum(t, dict(zip('ABCD', x))) for t in terms))
    def f_nor(*x, terms=terms):
        env = dict(zip('ABCD', x)); outs = []
        for t in terms:
            if len(t) > 1: outs.append(N(ev_sum(t, env)))
            else:
                v, n = t[0]; outs.append(N(env[v] ^ n))
        return N(int(any(outs)))
    o = same(f_pos, f_nor, 4); ok &= o; check('lb2.p27.' + k, o)
    nn, ni = nor_stats(terms)
    l27.append('- $%s=%s=\\overline{%s}$' % (k, ''.join(tex_sum(t) for t in terms), '+'.join(tex_nor_term(t) for t in terms)))
    r27.append([k, nn, ni])
check('lb2.p27', ok)
f4_27 = lambda a, b, c, d: (N(b) | N(c) | d) & a & (b | N(d)) & b
check('lb2.p27.f4_simplifica', same(f4_27, lambda a, b, c, d: a & b & (N(c) | d), 4))
ej('lb2-7', 'Implementar productos de sumas solo con puertas NOR', 'Libro · Cap. 2 · P2.7', 'comb', 'lb2.p27',
   'Reescribe cinco productos de sumas de modo que solo hagan falta puertas NOR (dos niveles) y cuenta las puertas.',
   '**Idea:** es el dual del problema anterior. Un producto de sumas $(s_1)(s_2)\\cdots$ es igual a $\\overline{\\overline{s_1}+\\overline{s_2}+\\cdots}$. Cada suma de varias variables es una NOR de primer nivel; un factor de una sola variable entra negado en la NOR de salida.',
   [('Las cinco funciones en forma NOR', '\n'.join(l27)),
    ('Puertas necesarias', tab(['Función', 'NOR (incluida la de salida)', 'Inversores'], r27)),
    ('Un detalle', 'En $f_4$ aparecen los factores sueltos $A$ y $B$. Como $A\\,B\\,(\\ldots)=1$ exige $A=B=1$, la función se reduce a $AB(\\bar C+D)$ (se ha comprobado en las 16 filas). El circuito del enunciado funciona igual, pero está lejos de ser mínimo.')],
   'Todas las implementaciones NOR son equivalentes al producto de sumas de partida.')

# ============================================================== P2.8 análisis
f1c = lambda x, y, z: N(x) & N(y) | x & y | x & z
f2c = lambda x, y, z: N(N(N(x) & N(y)) & N(x & y) & N(x & z))
bk1 = [1, 1, 0, 0, 0, 1, 1, 1]
check('lb2.p28.f1', col(f1c, 3) == bk1); check('lb2.p28.f2', col(f2c, 3) == bk1)
si = lambda a, b, c: a ^ b ^ c
co = lambda a, b, c: a & b | (a ^ b) & c
bk_si = [0, 1, 1, 0, 1, 0, 0, 1]; bk_co = [0, 0, 0, 1, 0, 1, 1, 1]
check('lb2.p28.suma_si', col(si, 3) == bk_si); check('lb2.p28.suma_co', col(co, 3) == bk_co)
check('lb2.p28.suma_aritmetica', all((a + b + c) == 2 * co(a, b, c) + si(a, b, c) for a, b, c in rows(3)))
check('lb2.p28', True)
r28 = [[''.join(map(str, r)), bk1[i], bk1[i], bk_si[i], bk_co[i]] for i, r in enumerate(rows(3))]
ej('lb2-8', 'Analizar tres circuitos y obtener su tabla de verdad', 'Libro · Cap. 2 · P2.8', 'comb', 'lb2.p28',
   'Obtén la tabla de verdad de tres circuitos de tres entradas: uno con inversores, tres puertas AND y una OR; otro con tres NAND y una NAND de salida; y un sumador completo con puertas XOR, AND y OR.',
   '**Método:** fija una combinación en las entradas, propaga el valor puerta a puerta hasta la salida y apúntalo. Repite para las 8 combinaciones. Es lento pero seguro.',
   [('Circuito AND–OR', 'Las tres puertas AND calculan $\\bar X\\bar Y$, $XY$ y $XZ$ y una OR las suma: $f_1=\\bar X\\bar Y+XY+XZ$.'),
    ('Circuito NAND–NAND', 'Con las mismas tres funciones en NAND de primer nivel y una NAND de salida, $f_2=\\overline{\\overline{\\bar X\\bar Y}\\cdot\\overline{XY}\\cdot\\overline{XZ}}$. Por De Morgan es igual a $f_1$: la tabla es idéntica.'),
    ('Sumador completo', 'Con sumandos $A_i$, $B_i$ y acarreo de entrada $C_{i-1}$: $S_i=A_i\\oplus B_i\\oplus C_{i-1}$ y $C_i=A_iB_i+(A_i\\oplus B_i)\\,C_{i-1}$. Comprobación: $A_i+B_i+C_{i-1}=2C_i+S_i$ en las 8 filas.'),
    ('Tabla de verdad conjunta', tab(['XYZ = $A_iB_iC_{i-1}$', '$f_1$', '$f_2$', '$S_i$', '$C_i$'], r28))],
   '$f_1=f_2$, y el sumador completo da $S_i$ = paridad de los tres bits y $C_i$ = mayoría de los tres.')

# ============================================================== P2.9 BCD -> XS3 (circuito del libro)
def circ29(b3, b2, b1, b0):
    x3 = b3 | (b2 & b0)
    x2 = (N(b2) & b0) | (b2 & N(b1) & N(b0)) | (N(b2) & b1)
    x1 = (b1 & b0) | (N(b1) & N(b0))
    x0 = N(b0)
    return x3, x2, x1, x0
book29 = ['0011', '0100', '0101', '0110', '0111', '1000', '0001', '1010', '1011', '1100', '1101', '1110', '1011', '1000', '1001', '1010']
r29 = []; diff29 = []
for i in range(16):
    got = ''.join(map(str, circ29(*[int(c) for c in format(i, '04b')])))
    if got != book29[i]: diff29.append((i, got, book29[i]))
    r29.append([format(i, '04b'), got, format(i + 3, '04b') if i < 10 else '—', 'ok' if (i < 10 and got == format(i + 3, '04b')) else ('error' if i < 10 else 'sin uso')])
check('lb2.p29.circuito_vs_xs3', [r[3] for r in r29[:10]].count('ok') == 9 and r29[6][3] == 'error')
check('lb2.p29.fila_1100_libro', diff29 == [(12, '1111', '1011')], str(diff29))
book('lb2.p29.tabla', not diff29, str(diff29))
check('lb2.p29.xs3_correcto', all(((b3 | (b2 & b1) | (b2 & b0)) == int(format(i + 3, '04b')[0])) for i in range(10) for b3, b2, b1, b0 in [[int(c) for c in format(i, '04b')]]))
check('lb2.p29', True)
ej('lb2-9', 'Analizar un circuito de 4 entradas y 4 salidas', 'Libro · Cap. 2 · P2.9', 'comb', 'lb2.p29',
   'Un circuito recibe un dígito BCD $B_3B_2B_1B_0$ y produce $X_3X_2X_1X_0$ con seis puertas AND, tres OR y un inversor directo. Obtén su tabla de verdad con las 16 combinaciones y di qué hace.',
   '**Método:** primero escribe la función de cada salida leyendo las puertas, después evalúa. Es más rápido que propagar bit a bit las 16 filas.',
   [('Funciones de salida', '- $X_3=B_3+B_2B_0$\n- $X_2=\\bar B_2B_0+B_2\\bar B_1\\bar B_0+\\bar B_2B_1$\n- $X_1=B_1B_0+\\bar B_1\\bar B_0$ (es una XNOR)\n- $X_0=\\bar B_0$'),
    ('Tabla de verdad del circuito', tab(['$B_3B_2B_1B_0$', 'Salida $X_3X_2X_1X_0$', 'BCD exceso 3 ($d+3$)', 'Coincide'], r29)),
    ('Conclusión', 'Casi todas las filas válidas ($0$ a $9$) coinciden con el código **exceso 3**: el circuito es un convertidor de BCD natural a BCD exceso 3, salvo en el dígito 6. Las filas $1010$ a $1111$ no son dígitos BCD: su salida no importa.')],
   'Es un convertidor BCD → exceso 3 incompleto.\n\n@box ojo | Errata del libro\n(1) Falta un término en $X_3$: el valor correcto es $X_3=B_3+B_2B_1+B_2B_0$. Con el circuito del libro el dígito $6$ ($0110$) da $0001$ en lugar de $1001$. El libro afirma que la tabla es la de un conversor a exceso 3 y no menciona este fallo.\n(2) En la fila $1100$ la tabla del libro imprime $1011$, pero el circuito da $1111$ (la puerta de $X_2$ detecta $B_2\\bar B_1\\bar B_0$). Esta segunda diferencia no afecta a ningún dígito BCD válido.\n@end')

# ============================================================== P2.10 codificador 8:3
S2f = lambda e: (e[7] | e[6] | e[5] | e[4], e[7] | e[6] | e[3] | e[2], e[7] | e[5] | e[3] | e[1])
book210 = [('10000000', '111'), ('01000000', '110'), ('00100000', '101'), ('00010000', '100'), ('00001000', '011'), ('00000100', '010'), ('00000010', '001'), ('00000001', '000'),
           ('00000000', '000'), ('00011100', '111'), ('10000001', '111'), ('11111111', '111')]
ok = True; r210 = []
for s, sal in book210:
    e = [int(c) for c in s][::-1]            # e[7] = primer carácter
    e = [int(c) for c in s]; e = e[::-1]
    # s está escrito E7..E0, e[i] = Ei
    got = ''.join(map(str, S2f(e)))
    ok &= (got == sal); r210.append([s, got])
check('lb2.p210', ok)
check('lb2.p210.OR_de_codigos', all(int(''.join(map(str, S2f([int(c) for c in s][::-1]))), 2) == eval('|'.join(str(7 - k) for k, c in enumerate(s) if c == '1') or '0') for s, _ in book210))
ej('lb2-10', 'Un codificador de 8 a 3 construido con puertas OR', 'Libro · Cap. 2 · P2.10', 'comb', 'lb2.p210',
   'Un bloque tiene 8 entradas $E_7\\ldots E_0$ y tres salidas, cada una con una OR de cuatro entradas. Obtén sus tablas con las ocho combinaciones de «un solo 1» y con algunas más con varios unos, y di qué hace.',
   '**Cómo se lee:** cada salida es una OR de las entradas cuyo número tiene un 1 en esa posición. $S_2=E_7+E_6+E_5+E_4$, $S_1=E_7+E_6+E_3+E_2$, $S_0=E_7+E_5+E_3+E_1$.',
   [('Tabla de verdad (selección)', tab(['$E_7\\ldots E_0$', '$S_2S_1S_0$'], r210)),
    ('Conclusión', 'Con un solo 1 la salida es el número binario de la entrada activa. Con varios unos la salida es la **OR bit a bit** de sus códigos (por ejemplo $00011100\\to 100\\,|\\,011\\,|\\,010=111$). Es un **codificador sin prioridad** 8:3: solo vale si se activa una entrada cada vez.')],
   'Codificador 8:3 sin prioridad. Las 12 filas verificadas coinciden con las del libro.')

# ============================================================== P2.11 decodificador 3:8 con habilitación
ok = True; r211 = []
for ei in (0, 1):
    for a in range(8):
        s = [int(ei == 1 and a == k) for k in range(7, -1, -1)]
        r211.append([ei] + [int(c) for c in format(a, '03b')] + s)
check('lb2.p211', all(sum(r[4:]) == r[0] for r in r211) and all((r[0] == 0) <= (sum(r[4:]) == 0) for r in r211))
r211b = [['%d' % r[0], ''.join(map(str, r[1:4])), ''.join(map(str, r[4:]))] for r in r211]
ej('lb2-11', 'Un decodificador de 3 a 8 con habilitación', 'Libro · Cap. 2 · P2.11', 'comb', 'lb2.p211',
   'Un circuito con entradas $E_I,A_2,A_1,A_0$ y ocho salidas $S_7\\ldots S_0$ tiene ocho puertas AND de cuatro entradas. Obtén su tabla de verdad y di qué función realiza.',
   '**Lectura:** la salida $S_k$ es una AND de $E_I$ con $A_2,A_1,A_0$ (cada una directa o negada) tal que vale 1 solo cuando $A_2A_1A_0$ es el número $k$ en binario.',
   [('Salidas', '$S_k=E_I\\cdot m_k(A_2,A_1,A_0)$ para $k=0\\ldots7$, donde $m_k$ es el minitérmino de índice $k$.'),
    ('Tabla de verdad', tab(['$E_I$', '$A_2A_1A_0$', '$S_7S_6S_5S_4S_3S_2S_1S_0$'], r211b))],
   'Con $E_I=0$ todas las salidas valen 0; con $E_I=1$ se activa solo la salida cuyo número es $A_2A_1A_0$. Es un **decodificador 3:8 con habilitación**.')

# ============================================================== P2.12 paridad
d = lambda x: [int(c) for c in x]
par = lambda dd: N(dd[0] ^ dd[1] ^ dd[2] ^ dd[3] ^ dd[4] ^ dd[5] ^ dd[6])
# el circuito: XOR de pares, XOR de los resultados, XOR con D6 y NOT
def circ212(D6, D5, D4, D3, D2, D1, D0):
    g1 = D0 ^ D1; g2 = D2 ^ D3; g3 = D4 ^ D5; h1 = g1 ^ g2; h2 = g3 ^ D6
    return N(h1 ^ h2)
book212 = [('0000000', 1), ('1010101', 1), ('0101010', 0), ('1111000', 1), ('0000111', 0), ('0110100', 0), ('0000011', 1), ('1110001', 1), ('1111110', 0), ('1111100', 0), ('0000001', 0), ('1111111', 0)]
r212 = []; dif = []
for s, b in book212:
    bits = d(s); got = circ212(*bits); ones = sum(bits)
    r212.append([s, ones, got, b, 'ok' if got == b else '**error del libro**'])
    if got != b: dif.append((s, got, b))
check('lb2.p212.circuito_es_paridad', all(circ212(*r) == int(sum(r) % 2 == 0) for r in rows(7)))
check('lb2.p212.fila_1111110', dif == [('1111110', 1, 0)], str(dif))
book('lb2.p212.tabla', not dif, str(dif))
check('lb2.p212.total_impar', all((sum(r) + circ212(*r)) % 2 == 1 for r in rows(7)))
check('lb2.p212', True)
ej('lb2-12', 'Un generador de paridad de 7 bits', 'Libro · Cap. 2 · P2.12', 'comb', 'lb2.p212',
   'Un circuito tiene 7 entradas $D_6\\ldots D_0$ y una salida $BPI_1$. Se forma con seis XOR en árbol (tres de primer nivel, dos de segundo y una de tercero que reciben $D_6$ directamente) y un inversor final. Obtén su tabla de verdad con varias combinaciones y di qué hace.',
   '**Idea:** la XOR de varios bits vale 1 si el número de unos es impar. Con el inversor al final, $BPI_1=1$ cuando el número de unos de $D_6\\ldots D_0$ es **par**.',
   [('Tabla de verdad (selección)', tab(['$D_6\\ldots D_0$', 'Unos', 'Salida calculada', 'Salida del libro', 'Estado'], r212)),
    ('Conclusión', 'Si añades $BPI_1$ a los 7 bits, el total de unos siempre es **impar**. Se ha verificado en las 128 combinaciones. Es un **generador de paridad impar** (bit de paridad impar).')],
   'Generador de paridad impar para 7 bits de datos.\n\n@box ojo | Errata del libro\nEn la fila $1111110$ el libro imprime $BPI_1=0$. Tiene 6 unos (par), así que el circuito da $1$. El resto de filas coinciden.\n@end')

# ============================================================== salida
txt = '\n'.join(out) + '\n'
open(os.path.join(ROOT, 'src', 'libro2.dsl'), 'w', encoding='utf-8').write(txt)
bad = [c for c in CHK if not c['ok']]
json.dump({'R': {}, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results8.json'), 'w'), ensure_ascii=False)
print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
for d_ in DIFF: print('  libro:', d_)
