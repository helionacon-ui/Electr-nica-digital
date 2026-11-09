# -*- coding: utf-8 -*-
"""Simulación de biestables para el capítulo 6.
Latches y maestro/esclavo: red de puertas NAND con retardo unitario (todas las puertas se actualizan a la vez).
Si el estado oscila mientras las entradas no cambian -> carrera ('r'). Si el estado final depende de la fase de la
oscilación (o de qué puerta gana una competición simétrica) -> valor desconocido ('x').
Flip-flops por flanco: modelo por flanco con valor desconocido 'x'."""

def nand(*v): return 0 if all(v) else 1

def runs(spec):
    return ''.join(str(v) * n for v, n in spec)

def successors(step, st, inp):
    nw = step(st, inp)
    return [st[:i] + (nw[i],) + st[i+1:] for i in range(len(st)) if nw[i] != st[i]]

def closure(step, starts, inp):
    """Estados alcanzables si las puertas se disparan una a una en cualquier orden (retardos desconocidos)."""
    seen = set(starts); todo = list(starts)
    while todo:
        s = todo.pop()
        for t in successors(step, s, inp):
            if t not in seen: seen.add(t); todo.append(t)
    return seen

def stables(step, states, inp):
    return {s for s in states if step(s, inp) == s}

def classify(states, idx):
    vals = {f[idx] for f in states}
    return 'x' if len(vals) > 1 else str(next(iter(vals)))

def simulate(step, init, slots, outs, race=lambda inp: False):
    """slots: lista de entradas por ranura. Devuelve una cadena por cada índice de salida de 'outs'.
    Una ranura con race(inp) verdadero se marca 'r' (la salida bascula sin parar); de ahí se sale con todos los estados posibles."""
    starts = {init}; res = [''] * len(outs)
    for inp in slots:
        cl = closure(step, starts, inp)
        if race(inp):
            for k in range(len(outs)): res[k] += 'r'
            starts = cl
            continue
        st = stables(step, cl, inp)
        if not st: raise RuntimeError('sin estado estable %r' % (inp,))
        for k, i in enumerate(outs): res[k] += classify(st, i)
        starts = st
    return res

# ---------------------------------------------------------------- latch con puertas NAND (estado: a,b,Q,Qb)
def latch_step(kind):
    def step(st, inp):
        a, b, Q, Qb = st
        X, Y, g = inp
        if kind == 'rs':
            na, nb = nand(X, g), nand(Y, g)
        else:
            na, nb = nand(X, g, Qb), nand(Y, g, Q)
        return (na, nb, nand(a, Qb), nand(b, Q))
    return step
LATCH_INIT = (1, 1, 0, 1)           # Q=0, Qb=1, puertas de entrada inactivas
def jk_race(inp): return bool(inp[0] and inp[1] and inp[2])

# ---------------------------------------------------------------- latch RS asincrono NAND (estado: Q,Qb); entradas Sb,Rb
def rsn_step(st, inp):
    Q, Qb = st; Sb, Rb = inp
    return (nand(Sb, Qb), nand(Rb, Q))

# ---------------------------------------------------------------- maestro/esclavo: dos latches RS en serie, uno activo cada vez
def ms_sim(kind, mode, X, Y, ck):
    """mode 'A': maestro activo con Ck=1 y esclavo con Ck=0; 'B': al revés. Devuelve (QM, QS) como cadenas."""
    step = latch_step('rs')
    mst = {LATCH_INIT}; sst = {LATCH_INIT}; QM = QS = ''
    for x, y, c in zip(X, Y, ck):
        c = int(c); gM = c if mode == 'A' else 1 - c; gS = 1 - gM
        qm = classify(mst, 2); qs = classify(sst, 2)
        assert qm in '01' and qs in '01', 'valor desconocido en M/S'
        if gM:
            qsb = 1 - int(qs)
            SM, RM = (int(x) & qsb, int(y) & int(qs)) if kind == 'jk' else (int(x), int(y))
            mst = stables(step, closure(step, mst, (SM, RM, 1)), (SM, RM, 1))
        else:
            qmb = 1 - int(qm)
            sst = stables(step, closure(step, sst, (int(qm), qmb, 1)), (int(qm), qmb, 1))
        QM += classify(mst, 2); QS += classify(sst, 2)
        assert QM[-1] in '01' and QS[-1] in '01'
    return QM, QS

# ---------------------------------------------------------------- flip-flops por flanco (valores '0','1','x')
def edge_ff(kind, ck, X, Y, edge):
    """ck, X, Y: cadenas por ranura. El flanco en la ranura k (ck[k-1]!=ck[k]) muestrea X[k-1], Y[k-1].
    kind: 'rs','jk','d','t'. Devuelve la cadena de Q."""
    q = '0'; out = ''
    for k in range(len(ck)):
        if k > 0 and ((edge == 'r' and ck[k-1] == '0' and ck[k] == '1') or (edge == 'f' and ck[k-1] == '1' and ck[k] == '0')):
            x, y = X[k-1], (Y[k-1] if Y else '0')
            if kind == 'd': q = x
            elif kind == 't': q = q if x == '0' else tog(q)
            elif kind == 'rs':
                if x == '1' and y == '1': q = 'x'
                elif x == '1': q = '1'
                elif y == '1': q = '0'
            elif kind == 'jk':
                if x == '1' and y == '1': q = tog(q)
                elif x == '1': q = '1'
                elif y == '1': q = '0'
        out += q
    return out
def tog(q): return 'x' if q == 'x' else ('1' if q == '0' else '0')
def inv(s): return ''.join({'0': '1', '1': '0'}.get(c, c) for c in s)
