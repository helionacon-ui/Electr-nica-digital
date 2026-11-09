# -*- coding: utf-8 -*-
"""Biblioteca del capítulo 8 (autómatas finitos): máquinas definidas por reglas, tablas, ecuaciones J-K/D por
Quine-McCluskey, comprobación de ecuaciones impresas, minimización de estados y generación de diagramas."""
import itertools, math, random, re
from logic import minimize, _covers


def pat_match(pat, inp):
    return all(p == 'X' or int(p) == b for p, b in zip(pat, inp))


class FSM:
    """rules[estado] = lista de (patrón, siguiente[, salida]) con patrón de bits/X; gana la primera regla que encaja.
    Moore: outs[estado] = tupla de salida. Mealy: la salida va en la regla (tercer elemento)."""
    def __init__(s, ins, states, rules, outs=None, mealy=False, valid=None, start=None, outn=None):
        s.ins = ins; s.states = list(states); s.rules = rules; s.outs = outs; s.mealy = mealy
        s.valid = valid or (lambda i: True); s.start = start or s.states[0]
        s.outn = outn

    def inputs(s):
        return [i for i in itertools.product((0, 1), repeat=len(s.ins)) if s.valid(i)]

    def find(s, st, inp):
        for r in s.rules[st]:
            if pat_match(r[0], inp):
                return r
        return None

    def nxt(s, st, inp):
        r = s.find(st, inp)
        return None if r is None else r[1]

    def out(s, st, inp=None):
        if not s.mealy:
            return s.outs[st]
        r = s.find(st, inp)
        return None if r is None else r[2]

    def step(s, st, inp):
        return s.nxt(st, inp), s.out(st, inp)

    def run(s, seq, st=None):
        """Devuelve lista de (estado_antes, estado_despues, salida). Moore: salida del estado al que se llega."""
        st = s.start if st is None else st; res = []
        for i in seq:
            n = s.nxt(st, i)
            if n is None:
                raise ValueError('transición no definida %s %s' % (st, i))
            o = s.out(st, i) if s.mealy else s.outs[n]
            res.append((st, n, o)); st = n
        return res

    def complete(s):
        return all(s.nxt(st, i) is not None for st in s.states for i in s.inputs())

    def classes(s):
        """Particiones de estados equivalentes (sólo transiciones definidas)."""
        inps = s.inputs()
        if s.mealy:
            key = {st: tuple(s.out(st, i) for i in inps) for st in s.states}
        else:
            key = {st: s.outs[st] for st in s.states}
        part = {st: key[st] for st in s.states}
        while True:
            new = {st: (part[st], tuple(part.get(s.nxt(st, i)) for i in inps)) for st in s.states}
            ids = {}
            for st in s.states:
                ids.setdefault(new[st], len(ids))
            newp = {st: ids[new[st]] for st in s.states}
            if len(set(newp.values())) == len(set(part.values())):
                cl = {}
                for st in s.states:
                    cl.setdefault(newp[st], []).append(st)
                return list(cl.values())
            part = newp


def sbits(i):
    return ''.join(str(b) for b in i)


def toin(s, fill=0):
    return tuple(fill if c == 'X' else int(c) for c in s)


def parse(expr):
    """Expresión del libro: '/x' negación, '*' y, '+' o, '^' xor, '/(…)' negación de grupo, '1' y '0' constantes."""
    e = expr.replace('·', '*').replace('⊕', '^')
    e = re.sub(r'/\(', 'NOT(', e)
    e = re.sub(r'/(\w+)', r'NOT(\1)', e)
    e = e.replace('*', '&').replace('+', '|')
    code = compile(e, '<eq>', 'eval')
    return lambda v: int(eval(code, {'NOT': lambda x: 1 - x, '__builtins__': {}}, dict(v))) & 1


def tex(expr):
    """Convierte una expresión del libro a LaTeX (sin signos $)."""
    e = expr.replace('·', '*').replace('⊕', '^')
    def neg_group(m):
        return m.group(0)
    # negación de grupo
    while '/(' in e:
        k = e.index('/('); depth = 0
        for j in range(k + 1, len(e)):
            if e[j] == '(': depth += 1
            elif e[j] == ')':
                depth -= 1
                if depth == 0: break
        inner = e[k + 2:j]
        e = e[:k] + '\\overline{' + inner + '}' + e[j + 1:]
    e = re.sub(r'/(\w+)', lambda m: '\\overline{' + m.group(1) + '}', e)
    e = re.sub(r'(?<![\\{A-Za-z])([A-Za-z])(\d)', r'\1_{\2}', e)
    e = re.sub(r'\\overline\{([A-Za-z])(\d)\}', r'\\overline{\1_{\2}}', e)
    e = e.replace('*', '\\cdot ').replace('^', '\\oplus ').replace('+', ' + ')
    return e


def name_tex(n):
    m = re.fullmatch(r'([A-Za-z]+)(\d+)', n)
    if m and len(m.group(1)) == 1: return '%s_{%s}' % (m.group(1), m.group(2))
    if len(n) > 1 and not m: return '\\mathrm{%s}' % n
    return n


def imps_tex(n, imps, names):
    if not imps: return '0'
    terms = []
    for v, mask in imps:
        lits = []
        for i in range(n):
            bit = n - 1 - i
            if mask >> bit & 1: continue
            nm = name_tex(names[i])
            lits.append(nm if (v >> bit) & 1 else '\\overline{%s}' % nm)
        terms.append('\\cdot '.join(lits) if lits else '1')
    return ' + '.join(terms)


def imps_plain(n, imps, names):
    if not imps: return '0'
    terms = []
    for v, mask in imps:
        lits = []
        for i in range(n):
            bit = n - 1 - i
            if mask >> bit & 1: continue
            lits.append(names[i] if (v >> bit) & 1 else '/' + names[i])
        terms.append('*'.join(lits) if lits else '1')
    return ' + '.join(terms)


def qnames(nb):
    return ['q%d' % k for k in range(nb - 1, -1, -1)]


JKREQ = {(0, 0): (0, None), (0, 1): (1, None), (1, 0): (None, 1), (1, 1): (None, 0)}


def derive(M, enc, nb, kind='JK', moore_out_on_q=True):
    """Ecuaciones mínimas. Variables: entradas (en el orden de M.ins) y luego q(nb-1)..q0. Devuelve dict
    nombre -> (imps, nvars, names). Combinaciones sin uso (códigos libres, entradas imposibles, transiciones
    sin definir) son indiferentes."""
    names = list(M.ins) + qnames(nb); n = len(names); ni = len(M.ins)
    used = {}
    for st in M.states:
        for i in M.inputs():
            nx = M.nxt(st, i)
            if nx is None: continue
            m = 0
            for b in i: m = (m << 1) | b
            m = (m << nb) | enc[st]
            used[m] = (st, i, nx)
    res = {}
    for b in range(nb):
        if kind == 'JK':
            onJ, dcJ, onK, dcK = [], [], [], []
            for m in range(1 << n):
                if m not in used:
                    dcJ.append(m); dcK.append(m); continue
                st, i, nx = used[m]
                j, k = JKREQ[((enc[st] >> b) & 1, (enc[nx] >> b) & 1)]
                if j is None: dcJ.append(m)
                elif j: onJ.append(m)
                if k is None: dcK.append(m)
                elif k: onK.append(m)
            res['J%d' % b] = (minimize(n, onJ, dcJ), n, names)
            res['K%d' % b] = (minimize(n, onK, dcK), n, names)
        else:
            on, dc = [], []
            for m in range(1 << n):
                if m not in used: dc.append(m); continue
                st, i, nx = used[m]
                if (enc[nx] >> b) & 1: on.append(m)
            res['D%d' % b] = (minimize(n, on, dc), n, names)
    # salidas
    no = M.outn or (len(M.rules[M.states[0]][0][2]) if M.mealy else len(next(iter(M.outs.values()))))
    for o in range(no):
        if M.mealy:
            on, dc = [], []
            for m in range(1 << n):
                if m not in used: dc.append(m); continue
                st, i, nx = used[m]
                if M.out(st, i)[o]: on.append(m)
            res['S%d' % (no - 1 - o)] = (minimize(n, on, dc), n, names)
        else:
            qn = qnames(nb)
            on, dc = [], []
            codes = {enc[s] for s in M.states}
            for c in range(1 << nb):
                if c not in codes: dc.append(c); continue
                st = [s for s in M.states if enc[s] == c][0]
                if M.outs[st][o]: on.append(c)
            res['S%d' % (no - 1 - o)] = (minimize(nb, on, dc), nb, qn)
    return res


def eq_tex(res, key):
    imps, n, names = res[key]
    return imps_tex(n, imps, names)


def eq_plain(res, key):
    imps, n, names = res[key]
    return imps_plain(n, imps, names)


def check_realization(M, enc, nb, eqs, kind='JK', souts=None):
    """eqs: dict 'J0'/'K0'/… -> expresión del libro; souts: lista (S_{no-1}..S_0) de expresiones. Comprueba que el
    circuito formado por esos flip-flops reproduce M en TODAS las transiciones definidas. Devuelve lista de fallos."""
    fails = []
    fs = {k: parse(v) for k, v in eqs.items()}
    so = [parse(x) for x in souts] if souts else None
    for st in M.states:
        for i in M.inputs():
            nx = M.nxt(st, i)
            if nx is None: continue
            v = {nm: b for nm, b in zip(M.ins, i)}
            for b in range(nb): v['q%d' % b] = (enc[st] >> b) & 1
            code = 0
            for b in range(nb):
                q = (enc[st] >> b) & 1
                if kind == 'JK':
                    j = fs['J%d' % b](v); k = fs['K%d' % b](v)
                    qn = (j & (1 - q)) | ((1 - k) & q)
                else:
                    qn = fs['D%d' % b](v)
                code |= qn << b
            if code != enc[nx]:
                fails.append(('next', st, sbits(i), code, enc[nx]))
            if so is not None:
                o = M.out(st, i) if M.mealy else M.outs[st]
                got = tuple(f(v) for f in so)
                if got != tuple(o):
                    fails.append(('out', st, sbits(i), got, tuple(o)))
    return fails


def tabla_md(M, enc=None, cols=None, show_out=True):
    """Tabla de transición (Moore: columna de salida; Mealy: 'sig/sal' en cada celda). Devuelve (head, rows)."""
    combos = list(itertools.product((0, 1), repeat=len(M.ins)))
    head = ['Estado'] + [sbits(i) for i in combos] + (['Salida'] if (not M.mealy and show_out) else [])
    rows = []
    for st in M.states:
        r = [st + (' (%s)' % format(enc[st], '0%db' % max(1, (max(enc.values())).bit_length())) if False else '')]
        for i in combos:
            if not M.valid(i): r.append('×'); continue
            n = M.nxt(st, i)
            if n is None: r.append('—'); continue
            if M.mealy: r.append('%s/%s' % (n, ''.join(map(str, M.out(st, i)))))
            else: r.append(n)
        if not M.mealy and show_out: r.append(''.join(map(str, M.outs[st])))
        rows.append(r)
    return head, rows


def enc_md(M, enc, nb):
    head = ['Estado', 'Código $' + ''.join('q_%d' % k for k in range(nb - 1, -1, -1)) + '$']
    rows = [[st, format(enc[st], '0%db' % nb)] for st in M.states]
    return head, rows


def fsm_edges(M, short=True):
    """Aristas agrupadas (a,b) -> etiquetas para el diagrama."""
    g = {}
    for st in M.states:
        for r in M.rules[st]:
            lab = r[0] + ('/' + ''.join(map(str, r[2])) if M.mealy else '')
            g.setdefault((st, r[1]), []).append(lab)
    return g


def fig_fsm_json(M, title='', cap='', W=None, H=None, pos=None, sub=None, r=None):
    """Diagrama de estados automático. pos: dict opcional estado->(x,y); si no, rejilla en una o dos filas."""
    import json
    n = len(M.states)
    if pos is None:
        if n <= 4: rows_ = [M.states]
        elif n <= 8:
            h = (n + 1) // 2; rows_ = [M.states[:h], M.states[h:]]
        else:
            h = (n + 2) // 3; rows_ = [M.states[:h], M.states[h:2 * h], M.states[2 * h:]]
        wcol = 130; hrow = 120
        W = W or max(len(x) for x in rows_) * wcol + 40
        H = H or len(rows_) * hrow + 60
        pos = {}
        for ri, row in enumerate(rows_):
            for ci, st in enumerate(row):
                off = (max(len(x) for x in rows_) - len(row)) * wcol / 2
                pos[st] = (int(20 + wcol / 2 + off + ci * wcol), int(70 + ri * hrow))
    nodes = {}
    for st in M.states:
        s_ = ''
        if sub is not None: s_ = sub(st)
        elif not M.mealy and M.outs: s_ = ''.join(map(str, M.outs[st]))
        nodes[st] = [pos[st][0], pos[st][1], s_]
    edges = []
    g = fsm_edges(M)
    for (a, b), labs in g.items():
        lab = ', '.join(labs)
        if len(lab) > 26: lab = ', '.join(labs[:3]) + '…' if len(labs) > 3 else lab
        if a == b: cur = 0
        else:
            xa, ya = pos[a]; xb, yb = pos[b]
            cur = 0
            if (b, a) in g: cur = 38
            elif ya == yb and abs(xa - xb) > 140: cur = -70 if ya < 100 else 70
        edges.append([a, b, lab, cur])
    d = {'nodes': nodes, 'edges': edges, 'W': W, 'H': H, 'title': title}
    if cap: d['cap'] = cap
    if r: d['r'] = r
    return '@fig fsm ' + json.dumps(d, ensure_ascii=False)


def quotient(M):
    """Autómata mínimo (clases de equivalencia). Mantiene el orden original y el nombre del primer representante."""
    cl = M.classes()
    cl = sorted(cl, key=lambda c: min(M.states.index(s) for s in c))
    rep = {}
    for c in cl:
        c2 = sorted(c, key=M.states.index)
        for s in c2: rep[s] = c2[0]
    states = [rep[c[0]] for c in cl]
    rules = {}
    for r0 in states:
        rr = []
        for r in M.rules[r0]:
            rr.append((r[0], rep[r[1]]) + tuple(r[2:]))
        rules[r0] = rr
    outs = {r0: M.outs[r0] for r0 in states} if not M.mealy else None
    return FSM(M.ins, states, rules, outs, M.mealy, M.valid, rep[M.start], M.outn)


def moore_of_mealy(M, prefix='Q'):
    """Moore equivalente a un Mealy de salida de 1 bit: el estado recuerda si la transición de llegada daba 1."""
    start = (M.start, 0); todo = [start]; seen = {start}; order = [start]; trans = {}
    while todo:
        st = todo.pop(0); s, o = st; r = []
        for i in M.inputs():
            n, oo = M.find(s, i)[1:3]
            ns = (n, oo[0]); r.append((sbits(i), ns))
            if ns not in seen: seen.add(ns); todo.append(ns); order.append(ns)
        trans[st] = r
    nm = {st: '%s%d' % (prefix, k) for k, st in enumerate(order)}
    rules = {nm[st]: [(p, nm[n]) for p, n in trans[st]] for st in order}
    outs = {nm[st]: (st[1],) for st in order}
    return FSM(M.ins, [nm[st] for st in order], rules, outs, False, M.valid, nm[start]), nm


def randseq(rng, L, nb=1, weights=None):
    return [tuple(rng.randint(0, 1) for _ in range(nb)) for _ in range(L)]


def same_funcs(res, bk, M, nb, extra_names=()):
    """¿Las ecuaciones mínimas calculadas (res) y las del libro (bk: dict nombre->expresión) son idénticas
    como funciones en las 2^n combinaciones (incluyendo las indiferentes)?"""
    names = list(M.ins) + qnames(nb)
    n = len(names)
    for k, e in bk.items():
        if k not in res: continue
        f = parse(e)
        imps, nn, nms = res[k]
        for m in range(1 << n):
            v = {nm: (m >> (n - 1 - i)) & 1 for i, nm in enumerate(names)}
            mine = int(any(((m & ~mask) == (val & ~mask)) for val, mask in imps)) if nn == n else None
            if mine is None: return None
            if mine != f(v): return False
    return True
