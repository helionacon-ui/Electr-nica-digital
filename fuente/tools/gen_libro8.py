# -*- coding: utf-8 -*-
"""Capítulo 8 del libro de problemas (autómatas finitos): define cada máquina, la simula contra un modelo de referencia,
comprueba las ecuaciones J‑K/D impresas en el libro y genera src/libro8.dsl."""
import json, os, sys, random, itertools, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from l8_lib import *
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
def ojo(txt): return '\n\n@box ojo | Errata en el libro\n' + txt + '\n@end'
def cron(rows, title='', rh=34, w=8, grid=4):
    return '@fig cron ' + json.dumps({'signals': rows, 'title': title, 'rh': rh, 'w_slot': w, 'grid': grid}, ensure_ascii=False)
RNG = random.Random(8)
def mealy(ins, rules, start=None, valid=None): return FSM(ins, list(rules), rules, None, True, valid, start)
def moore(ins, rules, outs, start=None, valid=None): return FSM(ins, list(rules), rules, outs, False, valid, start)
def fsmfig(M, title, cap=''): return fsm_fig(M, title, cap)
def _plain(t):
    t = t.replace('$', '').replace('\\,', ' ').replace('\\overline', '').replace('\\', '')
    t = re.sub(r'_\{?(\w)\}?', r'\1', t)
    return t
def fsm_fig(M, title, cap=''):
    if len(M.states) > 9 or len(fsm_edges(M)) > 18 or len(M.ins) >= 3: return ''
    title = _plain(title); cap = _plain(cap)
    return fig_fsm_json(M, title=title, cap=cap) + '\n\n'
def tabs(M, enc=None):
    h, r = tabla_md(M, enc)
    return tab(h, r)
def encs(M, enc, nb):
    h, r = enc_md(M, enc, nb)
    if not M.mealy:
        h = h + ['Salida']; r = [x + [''.join(map(str, M.outs[x[0]]))] for x in r]
    return tab(h, r)
def stream(L, nb=1): return randseq(RNG, L, nb)
def coste(exprs):
    """Cuenta puertas de una lista de expresiones en suma de productos (sin XOR)."""
    ands = ors = 0; inv = set()
    for e in exprs:
        terms = [t.strip() for t in e.replace('·', '*').split('+')]
        if len(terms) > 1 and all(t not in ('0', '1') for t in terms): ors += 1
        for t in terms:
            lits = [l.strip() for l in t.split('*')]
            if len(lits) > 1: ands += 1
            for l in lits:
                if l.startswith('/') and '(' not in l: inv.add(l[1:])
    return ands, ors, len(inv)
def lab(k, no):
    if k[0] == 'S' and no == 1: return 'S'
    return '%s_{%s}' % (k[0], k[1:])
def diseno(id_, M, enc, nb, kind='JK', bk=None, bkS=None):
    """Deriva las ecuaciones mínimas, comprueba que reproducen la máquina y (si se da) que las del libro también lo hacen.
    Devuelve (res, filas_mías, filas_libro)."""
    res = derive(M, enc, nb, kind)
    keys = [c + str(b) for b in range(nb - 1, -1, -1) for c in (('J', 'K') if kind == 'JK' else ('D',))]
    no = len(res) - len(keys)
    skeys = ['S%d' % d for d in range(no - 1, -1, -1)]
    f = check_realization(M, enc, nb, {k: eq_plain(res, k) for k in keys}, kind, [eq_plain(res, k) for k in skeys])
    check(id_ + '.diseno_propio', not f, str(f[:3]))
    mine = [['$%s$' % lab(k, no), '$%s$' % eq_tex(res, k)] for k in keys + skeys]
    brow = None
    if bk is not None:
        fb = check_realization(M, enc, nb, bk, kind, bkS)
        check(id_ + '.ecuaciones_libro', not fb, str(fb[:3]))
        brow = [['$%s$' % lab(k, no), '$%s$' % tex(bk[k])] for k in keys] + [['$%s$' % lab(sk, no), '$%s$' % tex(e)] for sk, e in zip(skeys, bkS or [])]
    return res, mine, brow, keys, skeys, no
def eqs_of(res, keys, skeys):
    return {k: eq_plain(res, k) for k in keys}, [eq_plain(res, k) for k in skeys]
def pcount(exprs):
    a, o, i = coste(exprs)
    return 'Coste de la lógica combinacional: %d puertas AND, %d OR y %d inversores (sin contar los biestables).' % (a, o, i)
def ones(seq): return ''.join(str(s[0] if isinstance(s, tuple) else s) for s in seq)

W('%% id=libro8'); W('%% group=ejer'); W('%% n=3.8'); W('%% title=Libro de problemas · Capítulo 8 · Autómatas')
W('%% short=Libro · Cap. 8 Autómatas'); W('%% sub=Treinta y cinco problemas de diseño de autómatas de Moore y de Mealy: detectores de secuencias, aritmética serie, contadores, registros y automatismos industriales. Cada máquina se ha simulado contra un modelo de referencia y cada ecuación se ha comprobado.'); W()
W('@box idea | Cómo leer esta sección')
W('Son los problemas resueltos del capítulo 8 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Los diagramas del libro **no se copian**: cada autómata se da como tabla de transición y, cuando es pequeño, como diagrama dibujado aquí. Las ecuaciones J‑K y D que imprime el libro se comprueban **una a una** contra la tabla de estados, y las máquinas se simulan frente a un modelo de referencia con miles de entradas aleatorias. Si algo del libro no cuadra, se anota en un cuadro de *Errata*. La teoría está en [[t10|el tema 10]].')
W('')
W('Método común de todos los problemas (flujo de diseño):')
W('')
W('1. **Diagrama de transición de estados**: qué hay que recordar y cómo cambia con cada entrada (Mealy: salida en la transición; Moore: salida en el estado).')
W('2. **Tabla de transición** y reducción de estados (estados equivalentes se fusionan).')
W('3. **Codificación** de estados con $n$ biestables, $2^n\\ge$ número de estados; los códigos sobrantes y las entradas imposibles son **indiferentes** ($\\times$).')
W('4. **Tabla de excitación** del biestable elegido. Para el J‑K: $0\\to0$ pide $J=0,K=\\times$; $0\\to1$ pide $J=1,K=\\times$; $1\\to0$ pide $J=\\times,K=1$; $1\\to1$ pide $J=\\times,K=0$. Para el D: $D=Q^+$.')
W('5. **Minimización** (Karnaugh o Quine‑McCluskey) de $J$, $K$ (o $D$) y de la salida, y **circuito**.')
W('')
W('En este capítulo el orden de las variables es siempre *entradas primero, estado después* ($E\\,q_1q_0$), y el estado inicial lo fija el RESET asíncrono de los biestables.')
W('@end'); W()
exec(open(os.path.join(HERE, 'gen_libro8a.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'gen_libro8b.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'gen_libro8c.py'), encoding='utf-8').read())
def finish():
    open(os.path.join(ROOT, 'src', 'libro8.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [c for c in CHK if not c['ok']]
    json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results14.json'), 'w'), ensure_ascii=False)
    print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
    for d in DIFF: print('  -', d)
finish()
