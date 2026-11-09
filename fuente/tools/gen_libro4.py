"""Capítulo 4 del libro de problemas (circuitos combinacionales con puertas): resuelve, verifica y genera src/libro4.dsl."""
import json, os, itertools, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from logic import minimize, sop_str, pos_str, pos_minimize, prime_implicants, _covers
CHK = []; DIFF = []; R = {}
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
def book(id_, ok, detail=''):
    if not ok: DIFF.append((id_, detail)); print('DIF', id_, detail)
out = []
def W(s=''): out.append(s)
def ej(id_, title, origen, tags, checks, enun, antes, pasos, res):
    W('@ej %s|%s|%s|%s|%s' % (id_, title, origen, tags, checks)); W('@enun'); W(enun); W('@end')
    if antes: W('@antes'); W(antes); W('@end')
    for t, body in pasos: W('@paso ' + t); W(body); W('@end')
    W('@res'); W(res); W('@end'); W('@end'); W()
def tab(head, rws):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rws])
def ranges(lst):
    lst = sorted(lst); parts = []; i = 0
    while i < len(lst):
        j = i
        while j + 1 < len(lst) and lst[j + 1] == lst[j] + 1: j += 1
        parts.append('%d\\text{-}%d' % (lst[i], lst[j]) if j - i >= 2 else ', '.join(str(x) for x in lst[i:j + 1]))
        i = j + 1
    return ', '.join(parts)
def lst_s(l): return ', '.join(str(x) for x in l)
def bits(i, n): return tuple(int(c) for c in format(i, '0%db' % n))
import re
def tx(name):                      # 'A1' -> A_{1} ; 'PR' -> \\mathrm{PR}
    if len(name) == 1: return name
    if re.match(r'^[A-Za-z]\d+$', name): return name[0] + '_{' + name[1:] + '}'
    return '\\mathrm{%s}' % name
def lit_tex(l):
    neg = l.startswith('!'); v = tx(l.lstrip('!'))
    return '\\overline{%s}' % v if neg else v
def terms_tex(terms, join=' + '):
    return join.join('\\,'.join(lit_tex(l) for l in t.split()) or '1' for t in terms) if terms else '0'
def sums_tex(factors):
    return ''.join('(' + ' + '.join(lit_tex(l) for l in f.split()) + ')' for f in factors)
def eval_terms(terms, names, row):
    v = dict(zip(names, row)); res = 0
    for t in terms:
        p = 1
        for l in t.split():
            p &= (1 - v[l[1:]]) if l.startswith('!') else v[l]
        res |= p
    return res
def eval_sums(factors, names, row):
    v = dict(zip(names, row)); res = 1
    for f in factors:
        s = 0
        for l in f.split():
            s |= (1 - v[l[1:]]) if l.startswith('!') else v[l]
        res &= s
    return res
def imps_terms(imps, names):
    n = len(names); ts = []
    for v, m in imps:
        ls = []
        for i in range(n):
            b = n - 1 - i
            if m >> b & 1: continue
            ls.append(names[i] if (v >> b) & 1 else '!' + names[i])
        ts.append(' '.join(ls))
    return ts
def imps_sums(imps, names):        # POS: minimizando los ceros; cada implicante -> suma con literales invertidos
    n = len(names); fs = []
    for v, m in imps:
        ls = []
        for i in range(n):
            b = n - 1 - i
            if m >> b & 1: continue
            ls.append('!' + names[i] if (v >> b) & 1 else names[i])
        fs.append(' '.join(ls))
    return fs
def cost_terms(ts):
    return (len(ts), sum(len(t.split()) for t in ts))
def gates(ts):
    """puertas de la realización a dos niveles: AND de k entradas, OR, inversores."""
    ands = [len(t.split()) for t in ts if len(t.split()) >= 2]
    singles = [t for t in ts if len(t.split()) == 1]
    invs = sorted({l[1:] for t in ts for l in t.split() if l.startswith('!')})
    return ands, len(ts), invs
def circ_text(ts, out_name):
    if not ts: return 'La salida $%s$ es constante.' % out_name
    ands, nor, invs = gates(ts)
    parts = []
    if ands:
        from collections import Counter
        c = Counter(ands); parts.append(' y '.join('%d AND de %d entradas' % (v, k) for k, v in sorted(c.items())))
    if nor >= 2: parts.append('1 OR de %d entradas' % nor)
    if invs: parts.append('%d inversor%s (%s)' % (len(invs), '' if len(invs) == 1 else 'es', ', '.join('$%s$' % tx(x) for x in invs)))
    if not parts: return '$%s$ es un simple cable (o una sola variable).' % out_name
    return 'Circuito de dos niveles: ' + ', '.join(parts) + '.'

def solve_sop(key, names, on, dc, book_terms, out_name, kmap=True, title=None):
    """minimiza SOP, verifica la solución del libro (cubre los 1, ningún 0) y compara coste. Devuelve (mine_terms, ok_book, same_cost, texto)"""
    n = len(names); on = sorted(on); dc = sorted(dc)
    imps = minimize(n, on, dc); mine = imps_terms(imps, names)
    offs = [m for m in range(2 ** n) if m not in on and m not in dc]
    okm = all(any(_covers(p, m) for p in imps) for m in on) and not any(any(_covers(p, m) for p in imps) for m in offs)
    check(key + '.minimo_valido', okm)
    ok_b = None; same = None
    if book_terms is not None:
        vals = [eval_terms(book_terms, names, bits(m, n)) for m in range(2 ** n)]
        ok_b = all(vals[m] == 1 for m in on) and all(vals[m] == 0 for m in offs)
        same = cost_terms(book_terms) == cost_terms(mine)
        check(key + '.libro_valido', ok_b); book(key + '.libro_coste', same, '%s vs %s' % (book_terms, mine))
    if kmap and n <= 4:
        R[key + '.on'] = on; R[key + '.dc'] = dc
    return mine, ok_b, same, imps

def kfig(key, names, title, cap, groups=True):
    d = {"key": key, "n": len(names), "names": names, "title": title, "cap": cap}
    if not groups: d["groups"] = False
    return '@fig kmap ' + json.dumps(d, ensure_ascii=False)

W('%% id=libro4'); W('%% group=ejer'); W('%% n=3.4'); W('%% title=Libro de problemas · Capítulo 4 · Circuitos combinacionales con puertas')
W('%% short=Libro · Cap. 4 Puertas lógicas'); W('%% sub=Problemas resueltos de diseño combinacional: de la tabla de verdad al circuito de puertas, con Karnaugh, SOP y POS.'); W()
W('@box idea | Cómo se usa esta sección')
W('Son los problemas resueltos del capítulo 4 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. El esquema del libro es siempre el mismo: **variables → tabla de verdad → simplificación → circuito**. Aquí cada tabla se genera por código, cada simplificación se calcula con un minimizador y se compara con la del libro (cubre los 1, no cubre ningún 0 y tiene el mismo coste), y cada circuito se describe por el número y el tipo de puertas, sin copiar el esquema. Los mapas de esta guía ponen las dos primeras variables en las filas y las otras dos en las columnas; el libro los dibuja con otros ejes, pero es el mismo mapa. Si el libro difiere, aparece una nota «Ojo». La teoría está en [[t03|el tema 3]] (Boole y Karnaugh) y [[t05|el tema 5]] (sumadores, comparadores, multiplexores).')
W('@end'); W()

PROBS = []   # (id, titulo, origen, checks) para el resumen final

def table_all(innames, outnames, outcols):
    n = len(innames)
    return tab(innames + outnames, [list(bits(i, n)) + [c[i] for c in outcols] for i in range(2 ** n)])
def minterms_of(col): return [i for i, v in enumerate(col) if v == 1]
def sop_report(key, innames, outname, col, book_terms, dc_idx=(), cap_prefix=''):
    """bloque de texto para una salida: Σ, mapa, SOP mínima, comparación con libro, circuito."""
    on = [i for i in minterms_of(col) if i not in dc_idx]
    mine, okb, same, imps = solve_sop(key, innames, on, list(dc_idx), book_terms, outname)
    t = '**$%s=\\Sigma(%s)$**' % (tx(outname), ranges(on) if on else '')
    if dc_idx: t += ' con indiferentes $d(%s)$' % lst_s(dc_idx)
    t += '. Simplificada: $%s=%s$. %s' % (tx(outname), terms_tex(mine), circ_text(mine, tx(outname)))
    if book_terms is not None:
        if okb and same: t += ' Coincide en coste con la solución del libro (%s).' % ('misma expresión' if sorted(book_terms) == sorted(mine) else 'otra forma equivalente, también mínima')
        elif okb: t += ' La solución del libro es correcta, pero no es mínima: $%s$.' % terms_tex(book_terms)
    if len(innames) <= 4 and on:
        t += '\n' + kfig(key, innames, outname, 'Casillas con el número de minitérmino; cada lazo da un producto.')
    return t, mine, okb, same

# ============================================================== 4.1  mayoría de tres sensores
n41 = ['S2', 'S1', 'S0']
col41 = [1 if sum(bits(i, 3)) >= 2 else 0 for i in range(8)]
book41 = [0, 0, 0, 1, 0, 1, 1, 1]
check('lb4.p41.tabla', col41 == book41); book('lb4.p41.tabla', col41 == book41)
printed41 = ['S1 S0', 'S2 S1', 'S2 S1']; right41 = ['S1 S0', 'S2 S1', 'S2 S0']
printed_ok = all(eval_terms(printed41, n41, bits(i, 3)) == col41[i] for i in range(8))
check('lb4.p41.erratas_impresa_falla', not printed_ok)
t41, mine41, ok41, same41 = sop_report('lb4.p41.S', n41, 'S', col41, right41)
check('lb4.p41', ok41 and same41 and sorted(mine41) == sorted(right41))
# alternativa con 3 NAND y una NAND de 3 entradas
ej('lb4-1', 'Voto mayoritario de tres sensores', 'Libro · Cap. 4 · P4.1', 'comb,karnaugh', 'lb4.p41',
   'Tres sensores binarios miden la misma señal. Diseña el circuito que dé a su salida el valor que tienen la mayoría de ellos.',
   '**Método de diseño combinacional:** (1) decide qué son entradas y qué salidas; (2) escribe la tabla de verdad; (3) pasa a suma de minitérminos; (4) simplifica con Karnaugh; (5) dibuja el circuito.',
   [('Entradas y salida', 'Entradas: $S_2,S_1,S_0$. Salida: $S$. Con tres sensores nunca hay empate, así que la mayoría siempre existe.'),
    ('Tabla de verdad', tab(['n', 'S2', 'S1', 'S0', 'S'], [[i] + list(bits(i, 3)) + [col41[i]] for i in range(8)]) + '\n\n$S=1$ cuando hay **al menos dos** unos: filas 3, 5, 6 y 7. En la mitad de las filas gana el 0 y en la otra mitad el 1.'),
    ('Simplificación', t41 + '\n\nCada par de sensores que coinciden en 1 basta para activar la salida. Por eso hay tres términos: $S_1S_0$, $S_2S_1$ y $S_2S_0$.'),
    ('Comprobación', 'El programa recorre las 8 combinaciones y comprueba que $S_1S_0+S_2S_1+S_2S_0$ vale 1 justo cuando hay dos o más unos.')],
   '$S=S_1S_0+S_2S_1+S_2S_0$: tres AND de dos entradas y una OR de tres, sin inversores.\n\n@box ojo | Errata en el libro\nEn la fórmula final del libro el tercer término está escrito como $S_2S_1$, igual que el segundo. Debe ser $S_2S_0$: con la fórmula impresa, la combinación $S_2S_1S_0=101$ daría 0 en vez de 1. Se ha comprobado por código.\n@end')

# ============================================================== 4.2  divisor de dos números de 2 bits
n42 = ['A1', 'A0', 'B1', 'B0']
def div(i):
    a = i >> 2; b = i & 3
    return (a, a) if b == 0 else (a // b, a % b)       # B=0: cociente = resto = A (convenio elegido en el libro)
Q = [div(i) for i in range(16)]
cols42 = {'C1': [(q >> 1) & 1 for q, r in Q], 'C0': [q & 1 for q, r in Q], 'R1': [(r >> 1) & 1 for q, r in Q], 'R0': [r & 1 for q, r in Q]}
bk42 = {'C1': [8, 9, 12, 13], 'C0': [4, 5, 10, 12, 13, 14, 15], 'R1': [8, 11, 12], 'R0': [4, 6, 7, 12, 14]}
for k, v in bk42.items():
    check('lb4.p42.sigma.' + k, minterms_of(cols42[k]) == v); book('lb4.p42.sigma.' + k, minterms_of(cols42[k]) == v)
bt42 = {'C1': ['A1 !B1'], 'C0': ['A1 B1 !B0', 'A0 !B1', 'A1 A0'], 'R1': ['A1 !B1 !B0', 'A1 !A0 B1 B0'], 'R0': ['A0 !B0', '!A1 A0 B1']}
rep42 = {}; ok42 = True
for k in ['C1', 'C0', 'R1', 'R0']:
    t, m, okb, same = sop_report('lb4.p42.' + k, n42, k, cols42[k], bt42[k]); rep42[k] = t; ok42 &= bool(okb and same)
check('lb4.p42', ok42)
ej('lb4-2', 'Divisor de dos números de 2 bits', 'Libro · Cap. 4 · P4.2', 'comb,karnaugh', 'lb4.p42',
   'Diseña el circuito más pequeño que divida dos números naturales de dos bits, $A_1A_0$ entre $B_1B_0$, y dé el cociente $C_1C_0$ y el resto $R_1R_0$.',
   '**Idea:** con números tan pequeños, la «división» es repartir enteros. Hay 16 combinaciones de entrada y 4 salidas, así que son cuatro funciones de cuatro variables.',
   [('Entradas y salidas', 'Entradas: $A_1A_0$ (dividendo) y $B_1B_0$ (divisor). Salidas: cociente $C_1C_0$ y resto $R_1R_0$.'),
    ('El caso del divisor cero', 'Dividir entre 0 no tiene resultado. Hay que **elegir** qué hacer. Aquí, igual que en el libro, se toma cociente y resto iguales al dividendo (filas 0, 4, 8 y 12). Es una decisión de diseño: otra opción serían indiferentes, que dan un circuito más pequeño.'),
    ('Tabla de verdad', table_all(n42, ['C1', 'C0', 'R1', 'R0'], [cols42[k] for k in ['C1', 'C0', 'R1', 'R0']]) + '\n\nEjemplos: $2\\div1=2$ resto 0 (fila 9); $3\\div2=1$ resto 1 (fila 14); $1\\div3=0$ resto 1 (fila 7).'),
    ('Cociente $C_1$', rep42['C1']), ('Cociente $C_0$', rep42['C0']), ('Resto $R_1$', rep42['R1']), ('Resto $R_0$', rep42['R0'])],
   'Las cuatro funciones del libro son correctas y mínimas. Coste total: $C_1$ (1 término), $C_0$ (3), $R_1$ (2), $R_0$ (2).')

# ============================================================== 4.3  sumador / restador de 1 bit
n43 = ['M', 'A0', 'B0', 'Ci']
def sr(i):
    m, a, b, c = bits(i, 4); v = a - (b + c) if m else a + b + c
    return v & 7
S43 = [sr(i) for i in range(16)]
cols43 = {'S2': [(v >> 2) & 1 for v in S43], 'S1': [(v >> 1) & 1 for v in S43], 'S0': [v & 1 for v in S43]}
bk43 = {'S2': [9, 10, 11, 15], 'S1': [3, 5, 6, 7, 9, 10, 11, 15], 'S0': [1, 2, 4, 7, 9, 10, 12, 15]}
for k, v in bk43.items():
    check('lb4.p43.sigma.' + k, minterms_of(cols43[k]) == v); book('lb4.p43.sigma.' + k, minterms_of(cols43[k]) == v)
bt43 = {'S2': ['M !A0 Ci', 'M !A0 B0', 'M B0 Ci'],
        'S1': ['B0 Ci', 'M !A0 Ci', 'M !A0 B0', '!M A0 Ci', '!M A0 B0'],
        'S0': ['A0 !B0 !Ci', '!A0 B0 !Ci', '!A0 !B0 Ci', 'A0 B0 Ci']}
rep43 = {}; ok43 = True
for k in ['S2', 'S1', 'S0']:
    t, m, okb, same = sop_report('lb4.p43.' + k, n43, k, cols43[k], bt43[k]); rep43[k] = t; ok43 &= bool(okb and same)
check('lb4.p43', ok43)
check('lb4.p43.S0_xor', all(cols43['S0'][i] == (bits(i, 4)[1] ^ bits(i, 4)[2] ^ bits(i, 4)[3]) for i in range(16)))
ej('lb4-3', 'Sumador/restador de 1 bit con acarreo previo', 'Libro · Cap. 4 · P4.3', 'comb,karnaugh,aritmetica', 'lb4.p43',
   'Diseña un circuito con entradas $M,A_0,B_0,C_i$ y salida $S_2S_1S_0$ en complemento a dos: si $M=0$ calcula $A_0+B_0+C_i$; si $M=1$ calcula $A_0-(B_0+C_i)$.',
   '**Ejercicio para practicar el complemento a dos.** El resultado necesita 3 bits porque el rango va de $-2$ a $+3$ ($A_0-(B_0+C_i)$ llega a $-2$; $A_0+B_0+C_i$ llega a $+3$).',
   [('Entradas y salidas', 'Cuatro entradas ($M$ elige la operación) y tres salidas $S_2S_1S_0$ en C2 de 3 bits, donde el rango es $-4\\ldots+3$.'),
    ('Tabla de verdad', table_all(n43, ['S2', 'S1', 'S0'], [cols43[k] for k in ['S2', 'S1', 'S0']]) + '\n\nEjemplos: fila 3: $0+1+1=+2=010$. Fila 7: $1+1+1=+3=011$. Fila 10: $0-(1+0)=-1=111$. Fila 14: $1-(1+0)=0=000$.'),
    ('Salida $S_2$ (signo)', rep43['S2']), ('Salida $S_1$', rep43['S1']), ('Salida $S_0$', rep43['S0'] + '\n\nObserva que $S_0=A_0\\oplus B_0\\oplus C_i$: el bit menos significativo no depende de $M$ (sumar o restar cambia la paridad igual).')],
   'Las tres funciones del libro son correctas y mínimas como suma de productos. $S_0$ es un XOR de tres entradas: con puertas XOR cuesta menos que sus cuatro términos de tres literales.')

# ============================================================== 4.4  multiplicador de 2x2 bits
n44 = ['A1', 'A0', 'B1', 'B0']
P44 = [(i >> 2) * (i & 3) for i in range(16)]
cols44 = {'S3': [(p >> 3) & 1 for p in P44], 'S2': [(p >> 2) & 1 for p in P44], 'S1': [(p >> 1) & 1 for p in P44], 'S0': [p & 1 for p in P44]}
bz44 = {'S3': list(range(15)), 'S2': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 15], 'S1': [0, 1, 2, 3, 4, 5, 8, 10, 12, 15], 'S0': [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 14]}
for k, v in bz44.items():
    z = [i for i, x in enumerate(cols44[k]) if x == 0]
    check('lb4.p44.pi.' + k, z == v); book('lb4.p44.pi.' + k, z == v)
bf44 = {'S3': ['B0', 'B1', 'A0', 'A1'], 'S2': ['!A0 !B0', 'B1', 'A1'],
        'S1': ['!A1 !A0 !B1 !B0', 'B1 B0', 'A0 B0', 'A1 B1', 'A1 A0'], 'S0': ['B0', 'A0']}
rep44 = {}; ok44 = True
for k in ['S3', 'S2', 'S1', 'S0']:
    z = [i for i, x in enumerate(cols44[k]) if x == 0]
    ones = minterms_of(cols44[k])
    pimps = pos_minimize(4, ones, []); pmine = imps_sums(pimps, n44)
    vals_b = [eval_sums(bf44[k], n44, bits(i, 4)) for i in range(16)]
    okb = vals_b == cols44[k]; same = cost_terms(bf44[k]) == cost_terms(pmine)
    check('lb4.p44.libro_valido.' + k, okb); book('lb4.p44.libro_coste.' + k, same, '%s vs %s' % (bf44[k], pmine))
    check('lb4.p44.mi_pos_valido.' + k, all(eval_sums(pmine, n44, bits(i, 4)) == cols44[k][i] for i in range(16)))
    R['lb4.p44.' + k + '.on'] = z; R['lb4.p44.' + k + '.dc'] = []      # ceros (se rodean los ceros)
    smine, _, _, _ = solve_sop('lb4.p44s.' + k, n44, ones, [], None, k, kmap=False)
    t = '**$%s=\\Pi(%s)$**. Producto de sumas mínimo: $%s=%s$.' % (k, ranges(z), k, sums_tex(pmine))
    t += ' En suma de productos sería $%s$ (%d términos).' % (terms_tex(smine), len(smine))
    t += ' ' + ('Coincide en coste con el libro.' if okb and same else ('La solución del libro es correcta pero no es mínima.' if okb else 'DIFERENTE'))
    t += '\n' + '@fig kmap ' + json.dumps({"key": 'lb4.p44.' + k, "n": 4, "names": n44, "title": k + ' (se marcan los ceros)', "cap": 'Se rodean los ceros: cada lazo da una suma.'}, ensure_ascii=False)
    rep44[k] = t; ok44 &= bool(okb)
check('lb4.p44', ok44)
check('lb4.p44.producto', all((cols44['S3'][i] * 8 + cols44['S2'][i] * 4 + cols44['S1'][i] * 2 + cols44['S0'][i]) == (i >> 2) * (i & 3) for i in range(16)))
ej('lb4-4', 'Multiplicador de dos números de 2 bits', 'Libro · Cap. 4 · P4.4', 'comb,karnaugh,pos', 'lb4.p44',
   'Implementa el circuito más pequeño capaz de multiplicar dos números en binario puro de dos bits, $A_1A_0$ y $B_1B_0$.',
   '**Por qué 4 bits de salida:** el producto más grande es $3\\times3=9=1001_2$, que necesita 4 bits. Aquí hay muchos ceros en las salidas, así que conviene trabajar con **productos de sumas** (maxitérminos).',
   [('Tabla de verdad', table_all(n44, ['S3', 'S2', 'S1', 'S0'], [cols44[k] for k in ['S3', 'S2', 'S1', 'S0']]) + '\n\nEjemplos: fila 6: $01\\times10=1\\times2=0010$. Fila 12: $11\\times00=0$. Fila 15: $11\\times11=3\\times3=9=1001$.'),
    ('Salida $S_3$', rep44['S3']), ('Salida $S_2$', rep44['S2']), ('Salida $S_1$', rep44['S1']), ('Salida $S_0$', rep44['S0'] + '\n\nEs el AND de los dos bits menos significativos: $A_0B_0$.')],
   'Se comprueba que las cuatro salidas forman el producto correcto para las 16 combinaciones. $S_3=A_1A_0B_1B_0$ y $S_0=A_0B_0$ son simples ANDs; $S_2$ y $S_1$ son las que requieren simplificar.')

# ============================================================== 4.5  complemento a dos de 4 bits
n45 = ['E3', 'E2', 'E1', 'E0']
C45 = [(-i) & 15 for i in range(16)]
cols45 = {'C3': [(v >> 3) & 1 for v in C45], 'C2': [(v >> 2) & 1 for v in C45], 'C1': [(v >> 1) & 1 for v in C45], 'C0': [v & 1 for v in C45]}
bk45 = {'C3': [1, 2, 3, 4, 5, 6, 7, 8], 'C2': [1, 2, 3, 4, 9, 10, 11, 12], 'C1': [1, 2, 5, 6, 9, 10, 13, 14], 'C0': [1, 3, 5, 7, 9, 11, 13, 15]}
for k, v in bk45.items():
    check('lb4.p45.sigma.' + k, minterms_of(cols45[k]) == v); book('lb4.p45.sigma.' + k, minterms_of(cols45[k]) == v)
bt45 = {'C3': ['E3 !E2 !E1 !E0', '!E3 E0', '!E3 E1', '!E3 E2'], 'C2': ['E2 !E1 !E0', '!E2 E0', '!E2 E1'], 'C1': ['E1 !E0', '!E1 E0'], 'C0': ['E0']}
rep45 = {}; ok45 = True
for k in ['C3', 'C2', 'C1', 'C0']:
    t, m, okb, same = sop_report('lb4.p45.' + k, n45, k, cols45[k], bt45[k]); rep45[k] = t; ok45 &= bool(okb and same)
check('lb4.p45', ok45)
ej('lb4-5', 'Complemento a dos de un número de 4 bits', 'Libro · Cap. 4 · P4.5', 'comb,karnaugh,aritmetica', 'lb4.p45',
   'Diseña el circuito más pequeño que calcule el complemento a dos de un número de cuatro bits $E_3E_2E_1E_0$, con salida $C_3C_2C_1C_0$.',
   '**Regla:** C2 $=$ invertir todos los bits $+1$. Hay una forma más rápida de leerlo: de derecha a izquierda se copian los bits hasta el primer 1 (incluido) y el resto se invierte.',
   [('Tabla de verdad', table_all(n45, ['C3', 'C2', 'C1', 'C0'], [cols45[k] for k in ['C3', 'C2', 'C1', 'C0']]) + '\n\nEjemplos: $0010\\to1101+1=1110$. $1000\\to0111+1=1000$ (el $-8$ es su propio opuesto). $0000\\to1111+1=0000$.'),
    ('Salida $C_3$', rep45['C3']), ('Salida $C_2$', rep45['C2']), ('Salida $C_1$', rep45['C1'] + '\n\nEs el XOR $E_1\\oplus E_0$.'), ('Salida $C_0$', rep45['C0'] + '\n\nEl bit menos significativo no cambia: $C_0=E_0$, un cable.')],
   'Las cuatro funciones del libro son correctas y mínimas. Nota: el $-8$ ($1000$) no tiene opuesto en 4 bits y el circuito lo devuelve igual: es el desbordamiento típico del C2.')

# ============================================================== SALIDA (se amplía con los siguientes problemas)
def finish():
    open(os.path.join(ROOT, 'src', 'libro4.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [c for c in CHK if not c['ok']]
    json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results10.json'), 'w'), ensure_ascii=False)
    print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
import glob
for _f in sorted(glob.glob(os.path.join(HERE, 'l4_part*.py'))):
    exec(compile(open(_f, encoding='utf-8').read(), _f, 'exec'))
finish()
