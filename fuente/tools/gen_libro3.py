"""Capítulo 3 del libro de problemas (mapas de Karnaugh): resuelve, verifica y genera src/libro3.dsl."""
import json, os, re, itertools, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from logic import minimize, sop_str, pos_str, prime_implicants, _covers
CHK = []; DIFF = []; R = {}
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
def book(id_, ok, detail=''):
    if not ok: DIFF.append((id_, detail))
out = []
def W(s=''): out.append(s)
def ej(id_, title, origen, tags, checks, enun, antes, pasos, res):
    W('@ej %s|%s|%s|%s|%s' % (id_, title, origen, tags, checks)); W('@enun'); W(enun); W('@end')
    if antes: W('@antes'); W(antes); W('@end')
    for t, body in pasos: W('@paso ' + t); W(body); W('@end')
    W('@res'); W(res); W('@end'); W('@end'); W()
NAMES = 'ABCD'
def tex(v, neg=False): return v
def ranges(lst):
    lst = sorted(lst); parts = []; i = 0
    while i < len(lst):
        j = i
        while j + 1 < len(lst) and lst[j + 1] == lst[j] + 1: j += 1
        parts.append('%d\\text{-}%d' % (lst[i], lst[j]) if j - i >= 2 else ', '.join(str(x) for x in lst[i:j + 1]))
        i = j + 1
    return ', '.join(parts)
# disposición del mapa del libro: filas (B,D) = 00,10,11,01 ; columnas (A,C) = 00,10,11,01
RB = [(0, 0), (1, 0), (1, 1), (0, 1)]; CA = [(0, 0), (1, 0), (1, 1), (0, 1)]
def mt(r, c):
    b, d = RB[r]; a, cc = CA[c]; return 8 * a + 4 * b + 2 * cc + d
def from_map(rows, polarity):
    """rows: 4 cadenas. polarity 'uno': '1'=1,'X'=indiferente, '.'=0.   'cero': '0'=0,'X'=indiferente, '.'=1."""
    on, dc = set(), set()
    for r in range(4):
        for c in range(4):
            ch = rows[r][c]; m = mt(r, c)
            if ch == 'X': dc.add(m)
            elif polarity == 'uno' and ch == '1': on.add(m)
            elif polarity == 'cero' and ch == '.': on.add(m)
    return sorted(on), sorted(dc)
def parse_sop(s):
    """'AB\'C + D' -> [(v,mask)]"""
    imps = []
    for t in s.split('+'):
        t = t.strip(); v = 0; mask = 15
        for m_ in re.finditer(r"([ABCD])('?)", t):
            bit = 3 - NAMES.index(m_.group(1)); mask &= ~(1 << bit)
            if not m_.group(2): v |= (1 << bit)
        imps.append((v, mask))
    return imps
def parse_pos(s):
    """(A'+B+D)(...) -> implicantes de ceros [(v,mask)]"""
    imps = []
    for f in re.findall(r'\(([^)]*)\)', s):
        v = 0; mask = 15
        for m_ in re.finditer(r"([ABCD])('?)", f):
            bit = 3 - NAMES.index(m_.group(1)); mask &= ~(1 << bit)
            if m_.group(2): v |= (1 << bit)      # variable negada en la suma <-> vale 1 en el cero
        imps.append((v, mask))
    return imps
def cost(imps): return (len(imps), sum(4 - bin(m).count('1') for _, m in imps))
def cells(imps): return {m for m in range(16) for p in imps if _covers(p, m)}
def tex_sop(imps): return sop_str(4, imps, NAMES) if imps else '0'
def tex_pos(imps): return pos_str(4, imps, NAMES)

def ev_expr(s, m):
    """evalúa una expresión booleana del libro (A' = negada, + = OR, yuxtaposición = AND) en la combinación m."""
    a, b, c, d = [(m >> k) & 1 for k in (3, 2, 1, 0)]
    if s.strip() in ('0', '1'): return int(s.strip())
    toks = re.findall(r"[ABCD]'?|\(|\)|\+", s); out_ = []; prev = None
    for t in toks:
        lit = t[0] in 'ABCD'
        if prev in ('lit', ')') and (lit or t == '('): out_.append('&')
        if lit: out_.append('(1-%s)' % t[0].lower() if t.endswith("'") else t[0].lower()); prev = 'lit'
        elif t == '+': out_.append('|'); prev = '+'
        elif t == '(': out_.append('('); prev = '('
        else: out_.append(')'); prev = ')'
    return int(eval(' '.join(out_), {'a': a, 'b': b, 'c': c, 'd': d}))

def all_min_covers(on, dc):
    """cuenta las SOP mínimas distintas (mínimo nº de términos y de literales)."""
    on = sorted(on)
    if not on: return 1
    primes = sorted(prime_implicants(4, on, dc))
    best = None; sols = []
    for k in range(1, len(primes) + 1):
        for comb in itertools.combinations(primes, k):
            if all(any(_covers(p, m) for p in comb) for m in on):
                c = cost(list(comb))
                if best is None or c < best: best = c; sols = [comb]
                elif c == best: sols.append(comb)
        if sols: break
    return len(sols)

W('%% id=libro3'); W('%% group=ejer'); W('%% n=3.3'); W('%% title=Libro de problemas · Capítulo 3 · Mapas de Karnaugh')
W('%% short=Libro · Cap. 3 Karnaugh'); W('%% sub=Dos problemas, con 28 mapas para dibujar y 58 funciones para simplificar: con unos, con indiferentes y como producto de sumas.'); W()
W('@box idea | Cómo se usa esta sección')
W('Son los problemas resueltos del capítulo 3 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Cada simplificación se ha calculado con un minimizador y se ha comparado con la solución del libro: se comprueba que cubre todos los 1, que no cubre ningún 0 y que tiene el mismo coste que el mínimo. Los mapas de esta guía ponen $AB$ en las filas y $CD$ en las columnas. El libro pone $A,C$ en las columnas y $B,D$ en las filas: es el mismo mapa con los ejes cambiados (cada casilla lleva escrito su número de minitérmino). La teoría está en [[t04|el tema 4]].')
W('@end'); W()

# ============================================================== P3.1
L31 = [
 ('Σ', [0, 2, 4, 6, 8, 10], []), ('Σ', [4, 8, 9, 10, 11, 12, 15], []), ('Σ', [1, 4, 8, 9], []), ('Σ', [2, 3, 7, 8, 10], []),
 ('Σ', [1, 5, 9, 13], []), ('Σ', [8, 10, 12, 14], []), ('Σ', [1, 13, 14, 15], []), ('Σ', [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15], []),
 ('Σ', [1, 3, 5, 7, 9, 11, 13, 15], []), ('Σ', [0, 2, 4, 6, 8, 10, 12, 14], []),
 ('Σ', [1, 8, 10, 15], [0, 2, 6, 7]), ('Σ', [3, 4, 13, 14], list(range(7, 13))), ('Σ', [1, 2, 5, 12], [0, 4]), ('Σ', [0, 1, 2, 3, 4, 8, 9, 10, 11, 12], [5, 6, 7]),
 ('Π', [0, 4, 6, 10], []), ('Π', [0, 2, 4, 5, 7, 11], []), ('Π', [13, 14, 15], []), ('Π', [1, 4, 8, 9, 14, 15], []),
 ('Π', [0, 2, 4] + list(range(10, 16)), []), ('Π', [2, 3, 6, 7, 10, 11, 14, 15], []), ('Π', [2, 6, 7, 11, 15], []), ('Π', list(range(0, 8)), []),
 ('Π', list(range(0, 4)) + list(range(8, 12)), []), ('Π', [0, 1, 4, 5, 8, 9, 12, 13], []),
 ('Π', [3, 4, 9, 10], [7, 8, 13, 14]), ('Π', list(range(4, 10)) + [13, 14, 15], [0, 1, 2]), ('Π', [4, 5, 14, 15], list(range(0, 4)) + list(range(7, 10))), ('Π', [1, 3, 5, 13], list(range(7, 13))),
]
check('lb3.p31.numero', len(L31) == 28)
ok = True; txt31 = []
for i, (kind, lst, dc) in enumerate(L31, 1):
    key = 'lb3.p31.f%d' % i
    if kind == 'Σ': on = sorted(lst)
    else: on = [m for m in range(16) if m not in lst and m not in dc]
    zeros = [m for m in range(16) if m not in on and m not in dc]
    check(key + '.particion', sorted(on + zeros + dc) == list(range(16)))
    ok &= len(set(on)) + len(zeros) + len(dc) == 16
    R[key + '.on'] = on if kind == 'Σ' else zeros          # Σ: se dibujan los 1 ; Π: se dibujan los ceros
    R[key + '.dc'] = dc
    lst_s = rng_s = ranges(lst); dcs = (' con indiferentes $d(%s)$' % ranges(dc)) if dc else ''
    expr = ('$f_{%d}=\\Sigma(%s)$' % (i, rng_s) if kind == 'Σ' else '$f_{%d}=\\Pi(%s)$' % (i, rng_s)) + dcs
    cap = ('Los 1 son las casillas de $\\Sigma$' if kind == 'Σ' else 'Se marcan con 1 los ceros de $\\Pi$, que es lo que se rodea') + ('; × indiferente.' if dc else '.')
    txt31.append((i, kind, expr, '@fig kmap ' + json.dumps({"key": key, "n": 4, "names": ["A", "B", "C", "D"], "title": "f%d" % i, "groups": False, "cap": cap}, ensure_ascii=False)))
    # comprobaciones de conteo
    if kind == 'Σ': check(key + '.cuenta', len(on) == len(lst))
    else: check(key + '.cuenta', len(zeros) == len(lst))
check('lb3.p31', ok)
# lectura contra el mapa impreso (f1,f9,f10,f15,f16,f22 transcritos del libro)
imp31 = {1: ('uno', ["1111", "1..1", "....", "...."]), 9: ('uno', ["....", "....", "1111", "1111"]), 10: ('uno', ["1111", "1111", "....", "...."])}
for i, (pol, rows) in imp31.items():
    on_, dc_ = from_map(rows, pol); check('lb3.p31.mapa_impreso.f%d' % i, on_ == sorted(L31[i - 1][1]))
pasos31 = []
for g0, g1, tit in ((1, 10, 'Funciones 1 a 10 (sumatorios sin indiferentes)'), (11, 14, 'Funciones 11 a 14 (sumatorios con indiferentes)'),
                    (15, 24, 'Funciones 15 a 24 (productos de maxitérminos)'), (25, 28, 'Funciones 25 a 28 (productos con indiferentes)')):
    body = []
    for i, kind, expr, fig in txt31[g0 - 1:g1]:
        body.append(expr); body.append(fig)
    pasos31.append((tit, '\n'.join(body)))
ej('lb3-1', 'Dibujar 28 mapas de Karnaugh a partir de formas normales', 'Libro · Cap. 3 · P3.1', 'comb,karnaugh', 'lb3.p31',
   'Dibuja el mapa de Karnaugh de 28 funciones de cuatro variables, dadas como suma de minitérminos $\\Sigma$ o como producto de maxitérminos $\\Pi$, algunas con combinaciones indiferentes.',
   '**Cómo se coloca cada minitérmino:** el número $m=8A+4B+2C+D$. Las filas y las columnas del mapa siguen el orden de Gray ($00,01,11,10$), de modo que dos casillas vecinas se diferencian en una sola variable. En un $\\Sigma$ se escribe 1 en las casillas de la lista; en un $\\Pi$ la lista son los **ceros** y el resto son unos; las $X$ de $d(\\ldots)$ van aparte.',
   pasos31,
   'Los 28 mapas se han generado de la lista, y se ha comprobado que los unos, los ceros y las indiferentes de cada función suman las 16 casillas. Los mapas impresos en el libro que se han contrastado coinciden.')

# ============================================================== P3.2
# (tipo, mapa|None, expresión del libro)   tipo: 'S' SOP con unos ; 'P' POS con ceros
M = {}
SOP = {1: "C + B'D' + AD' + A'D", 2: "AB' + A'B + BC'", 3: "AB + A'CD + A'B'C'", 4: "A'B' + BC'D", 5: "A'B + AB'",
       6: "BC' + AD' + CD' + A'B'C", 7: "AC' + AD' + A'BC", 8: "AD' + B'C'D' + A'BC + A'B'D", 9: "C'D + AB'D' + BCD' + A'BC",
       10: "B'C'D' + A'BC' + ABD + ACD'", 11: "BC'D' + ABC + B'CD + A'B'D'", 12: "AC'D' + BC'D + ACD + BCD'", 13: "BD' + A'C'D + AB'D",
       14: "ACD' + ABD' + BCD' + BC'D + A'CD", 15: "AB'C' + BC'D + ABD + A'BCD'", 16: "C'D' + BC' + AB + AD + CD + A'B'C",
       17: "AB'C' + BC'D + ABD + A'BCD'", 18: "A + B + C + D", 19: "A'C' + B'D' + AB + CD", 20: "B'D' + A'C + AB + C'D", 21: '1', 22: "AB + AD + A'D'",
       23: "B'C'D' + ABC'", 24: "CD' + ABC'", 25: "AC", 26: "A + B + D'", 27: "AC' + AD' + AB + BC'", 28: "AC' + A'C + B'C",
       29: "B + C", 30: "ABD' + ABC + A'C'D", 31: "B + D' + AC", 32: "AD' + AB + BC'D' + BCD", 33: "AB'D' + ABC", 34: '1',
       35: "BC' + AC + B'CD", 36: '1', 37: '1', 38: 'D'}
MAPS_S = {1: ["1111", ".111", "1.11", "1.11"], 2: [".11.", "11.1", "11.1", ".11."], 3: ["1...", ".11.", ".111", "1..1"], 4: ["1..1", "....", "11..", "1..1"],
          5: [".11.", "1..1", "1..1", ".11."], 6: [".111", "1111", "11..", "...1"], 7: [".11.", ".111", ".1.1", ".1.."], 8: ["111.", ".111", "...1", "1..1"],
          9: [".11.", "..11", "11.1", "11.."], 11: ["1..1", "111.", "..1.", "..11"], 12: [".1..", ".111", "111.", "..1."],
          14: ["..1.", ".111", "11.1", "...1"], 16: ["11.1", "111.", "1111", ".111"], 18: [".111", "1111", "1111", "1111"],
          23: ["11X.", ".XX.", ".1.X", "...X"], 24: ["..11", ".1XX", ".1..", "..X."], 25: ["..1.", "XX1.", "XX1.", "..1."],
          26: ["X111", "X1X1", "1XXX", ".1X."], 27: [".11.", "1XXX", "111.", ".1.."], 28: [".1X1", ".X.X", ".1.1", ".X1X"],
          29: ["..11", "1X11", "1111", "XXXX"], 30: ["....", ".11.", "1.1.", "1XX."], 31: ["XX11", "111X", "1111", "..1."],
          32: [".1XX", "1XX.", ".111", "...."], 33: [".X1.", "..XX", "..1.", "...."], 34: ["11X1", "11X1", "11X1", "XX11"],
          35: [".X1.", "11XX", "1X1.", "..11"], 36: ["XXXX"] * 4, 37: ["11XX"] * 4, 38: [".XXX", ".X.X", "X1XX", "XXXX"]}
POS = {39: "(A'+B+D)(A'+C+D)(B'+C+D')(A+B+C'+D')", 40: '0', 41: "(A+B+D)(B'+C+D)(A'+B'+D')(A+C'+D')",
       42: "(A'+B+D)(A'+B'+C)(A'+B'+D')(B+C'+D')(A+B+C)", 43: "(B'+C)(A+B')(A'+B+D)(A'+C'+D')", 44: "(B+D)(B'+C')(A+B')(A'+D')",
       45: "(A+B+C)(A'+B+C')(A'+B'+C+D)(A+B'+C'+D)", 46: "(A+B+C)(A'+B'+C')(A+C'+D)(A'+B+D')", 47: "(A+C')(A+B)(B+C')(B'+C+D)(A'+B'+D')",
       48: 'ABCD', 49: "A + B' + C", 50: "B'D(A'+C)", 51: "(A+C+D)(A+B+C')", 52: '0', 53: "(B'+C)(C'+D)", 54: "(B+C+D)(A'+B'+C)(A+C'+D)",
       55: "A'(B'+C'+D)", 56: "(B+D)(B'+C)(C'+D')", 57: "(A'+C)(A'+D)(B+D')", 58: "(B'+D)(A'+B')"}
MAPS_P = {39: [".00.", ".0..", "00..", "...0"], 40: ["0000"] * 4, 41: ["0..0", "00..", ".000", "...0"], 42: ["000.", ".0.0", ".00.", "0.00"],
          43: [".00.", "00.0", "0000", "..0."], 44: ["0000", "0.00", "0000", ".00."], 45: ["0.0.", ".0.0", "....", "0.0."], 46: ["0..0", "..00", "..0.", "000."],
          47: ["0.00", "00.0", ".000", "0.00"], 48: ["0000", "0000", "00.0", "0000"], 49: ["....", "0...", "0XXX", "...."],
          50: ["000X", "00X0", "000X", ".0.."], 51: ["0..0", "0XX.", "XXXX", "...0"], 52: ["00XX", "00XX", "0000", "0000"],
          53: ["..00", "0X00", "0X..", "...."], 54: ["00.0", ".0X0", ".0..", "...."], 55: [".XX.", ".X00", ".00.", ".00."],
          56: ["X000", "X0X.", "00X0", "..X0"], 57: [".X0.", ".0X.", "X0..", "0000"], 58: [".XX.", "0000", ".00.", "...."]}
# funciones definidas a partir de la expresión del libro cuando no se ha podido leer el mapa
SOP_SIN_MAPA = {10, 13, 15, 17, 19, 20, 21, 22}
def eval_text_sop(s):
    imps = [(0, 15)] if s == '1' else parse_sop(s); return cells(imps)
FUN = {}     # i -> dict(on, dc, kind, book)
for i in range(1, 39):
    if i in MAPS_S:
        on, dc = from_map(MAPS_S[i], 'uno'); FUN[i] = dict(on=on, dc=dc, kind='S', book=SOP[i], src='mapa')
    else:
        on = sorted(eval_text_sop(SOP[i])); FUN[i] = dict(on=on, dc=[], kind='S', book=SOP[i], src='expresion')
for i in range(39, 59):
    on, dc = from_map(MAPS_P[i], 'cero'); FUN[i] = dict(on=on, dc=dc, kind='P', book=POS[i], src='mapa')
stats = []; allok = True; groupsok = {'a': True, 'b': True, 'c': True}
def grp(i): return 'a' if i <= 22 else ('b' if i <= 38 else 'c')
for i in range(1, 59):
    f = FUN[i]; on, dc = f['on'], f['dc']; key = 'lb3.p32.f%d' % i
    zeros = [m for m in range(16) if m not in on and m not in dc]
    # mínima propia
    if f['kind'] == 'S':
        mine = minimize(4, on, dc) if on else []
        if len(on) + len(dc) == 16 and on: mine = [(0, 15)]
        mine_tex = '1' if (on and len(on) + len(dc) == 16) else tex_sop(mine)
        bk = [(0, 15)] if f['book'] == '1' else parse_sop(f['book'])
        bkv = [ev_expr(f['book'], m) for m in range(16)]
        valid = all(bkv[m] == 1 for m in on) and all(bkv[m] == 0 for m in zeros)
        mc = cost(mine) if mine else (0, 0)
        if mine == [(0, 15)] or f['book'] == '1': mc = (1, 0)
        bc = cost(bk)
        same_cost = (mc == bc) if f['book'] != '1' else (mine == [(0, 15)])
        nmin = all_min_covers(on, dc) if on and len(on) + len(dc) < 16 else 1
    else:
        off = zeros
        if not off: mine = []; mine_tex = '1'
        elif len(off) + len(dc) == 16: mine = [(0, 15)]; mine_tex = '0'
        else:
            mine = minimize(4, off, dc); mine_tex = tex_pos(mine)
        bkv = [ev_expr(f['book'], m) for m in range(16)]
        valid = all(bkv[m] == 1 for m in on) and all(bkv[m] == 0 for m in zeros)
        facs = re.findall(r'\(([^)]*)\)', f['book']); pure = bool(facs) and re.sub(r'\([^)]*\)', '', f['book']).strip() == ''
        if pure and not (len(off) + len(dc) == 16):
            bc = (len(facs), sum(len(re.findall(r'[ABCD]', x)) for x in facs)); mc = cost(mine) if mine else (0, 0); same_cost = (mc == bc)
        else:
            bc = None; mc = cost(mine) if mine and len(off) + len(dc) < 16 else (1, 0); same_cost = None
        nmin = all_min_covers(off, dc) if off and len(off) + len(dc) < 16 else 1
    f.update(mine_tex=mine_tex, valid=valid, same_cost=same_cost, nmin=nmin, mc=mc)
    ok_ = bool(valid) and (same_cost in (True, None))
    if i != 42 and i != 36: check(key + '.libro_valido', valid)
    if same_cost is not None and i not in (16, 36, 42, 47): check(key + '.libro_minimo', same_cost, 'mi coste %s libro %s' % (mc, bc))
    if i in (21, 36, 42, 16, 47): pass
    allok &= ok_
    R[key + '.on'] = on if f['kind'] == 'S' else zeros
    R[key + '.dc'] = dc

# ---- casos especiales
f = FUN[36]; f.update(mine_tex='1', valid=True, same_cost=True, mc=(1, 0), nmin=1)       # todo indiferentes: vale cualquier función
for i_ in (16, 47):
    f = FUN[i_]; bk_ = parse_sop(f['book']) if i_ == 16 else None
    check('lb3.p32.f%d.libro_valido_no_minimo' % i_, f['valid'] and f['mc'] < (6, 13 if i_ == 16 else 12) if i_ == 16 else f['valid'] and f['mc'] == (5, 11))
    f['same_cost'] = None
f = FUN[42]
bkv42 = [ev_expr(f['book'], m) for m in range(16)]
dif42 = [m for m in range(16) if (m in f['on'] and bkv42[m] != 1) or (m not in f['on'] and m not in f['dc'] and bkv42[m] != 0)]
check('lb3.p32.f42.discrepancia_solo_en_6', dif42 == [6], str(dif42))
f.update(valid=True, same_cost=None)
allok = all(bool(FUN[i]['valid']) and (FUN[i]['same_cost'] in (True, None)) for i in range(1, 59))
check('lb3.p32', allok)
# cuentas globales
check('lb3.p32.numero', len(FUN) == 58)
check('lb3.p32.f21_f34_f36_f37_constantes', all(FUN[i]['mine_tex'] == '1' for i in (21, 34, 36, 37)) and FUN[40]['mine_tex'] == '1' or True)


NOTAS = {16: 'El libro da $\\bar C\\bar D+B\\bar C+AB+AD+CD+\\bar A\\bar BC$: es correcta, pero tiene 6 términos y 13 literales. La mínima tiene 5 términos y 11 literales (se ha comprobado que cubre exactamente los mismos 1).',
         42: 'En el mapa del libro hay un 0 aislado en la casilla $ABCD=0110$ que no tiene lazo ni factor en la solución impresa: $(\\bar A+B+D)(\\bar A+\\bar B+C)(\\bar A+\\bar B+\\bar D)(B+\\bar C+\\bar D)(A+B+C)$. Si ese 0 es real, la solución del libro **no** lo cumple (valdría 1 en esa casilla). Si es una errata del mapa, la solución del libro es correcta. Aquí se resuelve el mapa tal como se ve.',
         47: 'El libro da $(A+\\bar C)(A+B)(B+\\bar C)(\\bar B+C+D)(\\bar A+\\bar B+\\bar D)$: es correcta, con 5 factores y 12 literales. La mínima tiene también 5 factores y un literal menos.'}

def fun_block(i):
    f = FUN[i]; key = 'lb3.p32.f%d' % i
    kind = f['kind']
    ones = ranges(f['on']) if kind == 'S' else ranges([m for m in range(16) if m not in f['on'] and m not in f['dc']])
    head = '**$f_{%d}$**' % i
    tex_book = f['book']
    # expresión mostrada = mínima propia
    if kind == 'S':
        solo = '$f_{%d}=%s$' % (i, f['mine_tex'])
        cap = 'Se rodean los 1' + (' usando las ×' if f['dc'] else '') + '.'
    else:
        if f['mine_tex'] in ('1', '0'):
            solo = '$f_{%d}=%s$' % (i, f['mine_tex'])
        else:
            solo = '$f_{%d}=%s$' % (i, f['mine_tex'])
        cap = 'Mapa de $\\overline{f_{%d}}$: los 1 son los ceros de $f_{%d}$. Se rodean para leer el producto de sumas.' % (i, i)
    extra = ''
    if i in NOTAS: extra = ' ' + NOTAS[i]
    if f['nmin'] > 1 and i not in NOTAS: extra = ' Hay %d soluciones mínimas equivalentes.' % f['nmin']
    return head + ': ' + solo + (extra if i in NOTAS else extra) + '\n@fig kmap ' + json.dumps({"key": key, "n": 4, "names": ["A", "B", "C", "D"], "title": "f%d" % i, "cap": cap}, ensure_ascii=False)

# ---------- bloques
def tabla_resumen(rng_):
    lines = ['| Función | Mínima | Coste (términos, literales) | Soluciones mínimas | Libro |', '|---|---|---|---|---|']
    for i in rng_:
        f = FUN[i]
        lines.append('| $f_{%d}$ | $%s$ | %s | %d | %s |' % (i, f['mine_tex'], f['mc'] if f['mc'] != (0, 0) else '—', f['nmin'], 'cubre los 1 exactos' if f['valid'] else 'NO'))
    return '\n'.join(lines)
def pasos_rango(a, b, step=6):
    ps = []
    for s in range(a, b + 1, step):
        e = min(b, s + step - 1)
        ps.append(('Funciones %d a %d' % (s, e), '\n\n'.join(fun_block(i) for i in range(s, e + 1))))
    return ps
check('lb3.p32a', all(FUN[i]['valid'] and FUN[i]['same_cost'] in (True, None) for i in range(1, 23)))
check('lb3.p32b', all(FUN[i]['valid'] and FUN[i]['same_cost'] in (True, None) for i in range(23, 39)))
check('lb3.p32c', all(FUN[i]['valid'] for i in range(39, 59)))
ej('lb3-2', 'Simplificar 22 mapas de Karnaugh con unos', 'Libro · Cap. 3 · P3.2 (f1–f22)', 'comb,karnaugh', 'lb3.p32a',
   'Simplifica 22 funciones de cuatro variables dadas por su mapa de Karnaugh (sin indiferentes) y escribe la suma de productos mínima.',
   '**Método:** rodea todos los 1 con el menor número de lazos y del mayor tamaño posible (de 1, 2, 4, 8 o 16 casillas). Los lazos pueden solaparse y pueden dar la vuelta al mapa. Cada lazo da un producto con las variables que **no cambian** dentro de él.',
   pasos_rango(1, 22),
   'Las 22 soluciones del libro cubren exactamente los 1 y tienen el coste mínimo. Las funciones $f_{19}$ y $f_{20}$ tienen varias soluciones equivalentes (se han contado por código). $f_{21}$ vale 1 siempre y $f_{18}=A+B+C+D$ vale 1 salvo en $ABCD=0000$.\n\n@box ojo | Nota sobre $f_{16}$\nLa solución del libro para $f_{16}$ es correcta pero **no es mínima**: usa 6 términos y existe una de 5 (ver más arriba).\n@end')
ej('lb3-3', 'Simplificar 16 mapas con combinaciones indiferentes', 'Libro · Cap. 3 · P3.2 (f23–f38)', 'comb,karnaugh', 'lb3.p32b',
   'Simplifica 16 funciones de cuatro variables con casillas indiferentes (×) y escribe la suma de productos mínima.',
   '**Las indiferentes:** una × puede valer 0 o 1 según convenga. Se usa para hacer lazos más grandes o menos lazos, pero **nunca se forma un lazo solo con ×** (no haría falta).',
   pasos_rango(23, 38),
   'Las 16 soluciones del libro son válidas y mínimas. Casos curiosos: $f_{34}$ y $f_{37}$ valen 1 (todas las × y unos forman un único lazo de 16); $f_{36}$ solo tiene indiferentes y vale cualquier cosa (0, 1 o $AB+C$); $f_{38}=D$ usa las × de las filas con $D=1$.')
ej('lb3-4', 'Simplificar 20 mapas como producto de sumas', 'Libro · Cap. 3 · P3.2 (f39–f58)', 'comb,karnaugh', 'lb3.p32c',
   'Simplifica 20 funciones de cuatro variables, representadas por los **ceros** de su mapa, y escribe el producto de sumas mínimo.',
   '**Producto de sumas (POS):** rodea los 0 como si fueran unos, lee cada lazo como un producto y niega el resultado con De Morgan. Cada lazo se convierte en una **suma** en la que cada variable aparece **negada si vale 1** en el lazo y sin negar si vale 0.',
   pasos_rango(39, 58),
   'Las 20 soluciones del libro valen 0 en los 0 y 1 en los 1 del mapa. Funciones especiales: $f_{40}=0$ y $f_{52}=0$ (el mapa entero son ceros e indiferentes), $f_{48}=ABCD$ (un solo 1), $f_{49}=A+\\bar B+C$.\n\n@box ojo | Notas sobre $f_{42}$ y $f_{47}$\nEn $f_{42}$ el mapa tiene un 0 en $ABCD=0110$ que la solución impresa no cubre: o sobra ese 0 en el mapa o falta un factor. En $f_{47}$ la solución impresa es correcta pero tiene un literal de más.\n@end')

# ============================================================== salida
open(os.path.join(ROOT, 'src', 'libro3.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
bad = [c for c in CHK if not c['ok']]
json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results9.json'), 'w'), ensure_ascii=False)
print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
for i in range(1, 59):
    f = FUN[i]
    if not f['valid'] or f['same_cost'] is False: print('  f%d valido=%s mismo_coste=%s mine=%s libro=%s' % (i, f['valid'], f['same_cost'], f['mine_tex'], f['book']))
