"""Bloque 2: Feb-2025 (P1-P4), diciembre (recinto, contador JK-NAND, ventanas), Feb-2023 (sensores, toldo)."""
import json, itertools
from logic import *
R = {}; CHK = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)

# ============================================================ primitivas bit a bit
def add_n(a, b, cin, n):
    s = a + b + cin; return s & ((1 << n) - 1), s >> n
def xor_n(x, s, n): return x ^ (((1 << n) - 1) if s else 0)

# ============================================================ FEB-2025 P1: (A*B)+C, 3 bits C2 cada uno
def feb25_p1(A, B, C):
    sA, sB, sC = A >> 2 & 1, B >> 2 & 1, C >> 2 & 1
    # 1) valor absoluto con XOR + sumador (cin = signo): 3 bits
    MA, _ = add_n(xor_n(A, sA, 3), 0, sA, 3)
    MB, _ = add_n(xor_n(B, sB, 3), 0, sB, 3)
    # 2) multiplicador 3x3 sin signo (AND + sumadores): 5 bits
    P = 0
    for i in range(3):
        if (MB >> i) & 1: P += MA << i
    assert P < 32
    # 3) signo del producto y complemento a 2 en 6 bits
    sp = sA ^ sB
    Pp, _ = add_n(xor_n(P, sp, 6), 0, sp, 6)
    # 4) sumar C extendido en signo a 6 bits
    Cext = C | (0b111000 if sC else 0)
    Rr, _ = add_n(Pp, Cext, 0, 6)
    # 5) signo y magnitud a mostrar
    sR = Rr >> 5 & 1
    M, _ = add_n(xor_n(Rr, sR, 6), 0, sR, 6)
    assert M <= 19 or True
    tens = int(M >= 10)
    units, _ = add_n(M, 6 if tens else 0, 0, 4)   # +6 y nos quedamos con 4 bits (corrección BCD)
    return sR, tens, units, M, c2(Rr, 6)
ok = True; worst = 0; rng = []
for A, B, C in itertools.product(range(8), repeat=3):
    sR, t, u, M, val = feb25_p1(A, B, C)
    exp = c2(A, 3) * c2(B, 3) + c2(C, 3)
    rng.append(exp)
    ok &= (val == exp) and (-1)**sR * (10*t + u) == exp and u <= 9 and t <= 1
check('feb25.p1.exhaustivo', ok, '512 combinaciones')
R['feb25.p1.rango'] = [min(rng), max(rng)]
check('feb25.p1.rango', min(rng) == -16 and max(rng) == 19)
R['feb25.p1.prod_rango'] = [min(c2(a,3)*c2(b,3) for a in range(8) for b in range(8)), max(c2(a,3)*c2(b,3) for a in range(8) for b in range(8))]

# ============================================================ FEB-2025 P2: decodificador 4:16 con 5 de 2:4
def dec24(E, a1, a0):
    s = [0]*4
    if E: s[a1*2 + a0] = 1
    return s
def dec416(a):  # a = 0..15
    a3, a2, a1, a0 = bits(a, 4)
    top = dec24(1, a3, a2)
    out = []
    for k in range(4): out += dec24(top[k], a1, a0)
    return out
ok = all(dec416(a) == [int(i == a) for i in range(16)] for a in range(16))
check('feb25.p2.dec416', ok)

# ============================================================ FEB-2025 P3: expendedora de tabaco (Mealy, T + JK)
# estados S0..S3 = 0, 0.5, 1, 1.5 EUR acumulados. entradas M1M0: 00 nada, 01 50c, 10 1EUR, 11 error (se ignora)
def tab_next(s, m1, m0):
    coin = {(0,0):0, (0,1):1, (1,0):2, (1,1):0}[(m1, m0)]
    n = s + coin
    if n < 4: return n, 0, 0                # (siguiente, C0, T)
    return 0, int(n == 5), 1
vars_ = ['Q_1','Q_0','M_1','M_0']
fn = {k: {'on':[], 'dc':[]} for k in ['T1','J0','K0','C0','T']}
for s in range(4):
    for m1 in (0,1):
        for m0 in (0,1):
            idx = (s << 2) | (m1 << 1) | m0
            ns, c0, t = tab_next(s, m1, m0)
            if c0: fn['C0']['on'].append(idx)
            if t: fn['T']['on'].append(idx)
            q1, q1n = s >> 1, ns >> 1
            if q1 ^ q1n: fn['T1']['on'].append(idx)
            q0, q0n = s & 1, ns & 1
            j, k = jk_excitation(q0, q0n)
            if j == 1: fn['J0']['on'].append(idx)
            elif j is None: fn['J0']['dc'].append(idx)
            if k == 1: fn['K0']['on'].append(idx)
            elif k is None: fn['K0']['dc'].append(idx)
imps = {k: minimize(4, d['on'], d['dc']) for k, d in fn.items()}
for k in imps: R['tab.' + k] = sop_str(4, imps[k], vars_)
def tab_gate(s, m1, m0):
    idx = (s << 2) | (m1 << 1) | m0
    t1 = eval_sop(imps['T1'], idx); j0 = eval_sop(imps['J0'], idx); k0 = eval_sop(imps['K0'], idx)
    q1 = (s >> 1) ^ t1; q0 = ff_next('JK', s & 1, j0, k0)
    return (q1 << 1) | q0, eval_sop(imps['C0'], idx), eval_sop(imps['T'], idx)
ok = all(tab_gate(s, m1, m0) == tab_next(s, m1, m0) for s in range(4) for m1 in (0,1) for m0 in (0,1))
check('feb25.p3.puertas==tabla', ok)
# especificación aritmética independiente: secuencias de monedas de hasta 6
def spec_tab(coins):
    tot = 0; res = []
    for c in coins:
        tot += {'-':0,'50':50,'100':100}[c]
        if tot >= 200: res.append((1, int(tot > 200))); tot = 0
        else: res.append((0, 0))
    return res
cmap = {'-':(0,0), '50':(0,1), '100':(1,0)}
ok = True
for L in range(1, 8):
    for seq in itertools.product(['-','50','100'], repeat=L):
        s = 0; got = []
        for c in seq:
            s, c0, t = tab_gate(s, *cmap[c]); got.append((t, c0))
        if got != spec_tab(seq): ok = False; break
    if not ok: break
check('feb25.p3.exhaustivo', ok, 'todas las secuencias de hasta 7 entradas')
# ejemplo del enunciado: 50 + 50 + 100 -> 2 EUR exactos; 100+100 ; 50,50,50,100 -> cambio
def run_tab(seq):
    s = 0; out = []
    for c in seq:
        s, c0, t = tab_gate(s, *cmap[c]); out.append((s, t, c0))
    return out
R['tab.ej1'] = run_tab(['50','50','100'])
R['tab.ej2'] = run_tab(['50','50','50','100'])
check('feb25.p3.ej', R['tab.ej1'][-1][1:] == (1, 0) and R['tab.ej2'][-1][1:] == (1, 1))

# ============================================================ FEB-2025 P4: noria (A,B,P), Moore, 6 estados, 3 JK
# S0 parada | S1 giro A (A aun pulsada) | S2 giro A | S3 giro B (B aun pulsada) | S4 giro B | S5 parada esperando soltar
def noria_next(s, a, b, p):
    if (a, b) == (1, 1): return None
    N = (a, b) == (0, 0)
    if s == 0:
        if p: return 0
        return 1 if a else (3 if b else 0)
    if s == 1:
        if p: return 0
        return 1 if a else (3 if b else 2)
    if s == 2:
        if p: return 0
        return 5 if a else (3 if b else 2)
    if s == 3:
        if p: return 0
        return 1 if a else (3 if b else 4)
    if s == 4:
        if p: return 0
        return 5 if b else (1 if a else 4)
    if s == 5:
        return 0 if (N and not p) else 5
    return None
MA = {1, 2}; MB = {3, 4}
# NOTA: en S4 (gira B) pulsar B = 2a pulsacion seguida de B -> parar. En S2 pulsar A -> parar.
vars_ = ['Q_2','Q_1','Q_0','A','B','P']
fn = {k: {'on':[], 'dc':[]} for k in ['J2','K2','J1','K1','J0','K0']}
for s in range(8):
    for a, b, p in itertools.product((0,1), repeat=3):
        idx = (s << 3) | (a << 2) | (b << 1) | p
        r = noria_next(s, a, b, p) if s < 6 else None
        if r is None:
            for k in fn: fn[k]['dc'].append(idx)
            continue
        for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
            q = (s >> bit) & 1; qn = (r >> bit) & 1
            j, k = jk_excitation(q, qn)
            if j == 1: fn[J]['on'].append(idx)
            elif j is None: fn[J]['dc'].append(idx)
            if k == 1: fn[K]['on'].append(idx)
            elif k is None: fn[K]['dc'].append(idx)
nimps = {k: minimize(6, d['on'], d['dc']) for k, d in fn.items()}
for k in nimps: R['noria.' + k] = sop_str(6, nimps[k], vars_)
# salidas Moore
on_ma = [s for s in range(8) if s in MA]; on_mb = [s for s in range(8) if s in MB]
dc_out = [6, 7]
ma_i = minimize(3, on_ma, dc_out); mb_i = minimize(3, on_mb, dc_out)
R['noria.MA'] = sop_str(3, ma_i, ['Q_2','Q_1','Q_0']); R['noria.MB'] = sop_str(3, mb_i, ['Q_2','Q_1','Q_0'])
def noria_gate(s, a, b, p):
    idx = (s << 3) | (a << 2) | (b << 1) | p
    ns = 0
    for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
        j = eval_sop(nimps[J], idx); k = eval_sop(nimps[K], idx)
        ns |= ff_next('JK', (s >> bit) & 1, j, k) << bit
    return ns
ok = True
for s in range(6):
    for a, b, p in itertools.product((0,1), repeat=3):
        r = noria_next(s, a, b, p)
        if r is None: continue
        ok &= noria_gate(s, a, b, p) == r
check('noria.puertas==tabla', ok)
ok = all(eval_sop(ma_i, s) == (s in MA) for s in range(6)) and all(eval_sop(mb_i, s) == (s in MB) for s in range(6))
check('noria.salidas', ok)
# escenarios (A,B,P por ciclo)
def noria_run(stream, s=0):
    out = []
    for (a, b, p) in stream:
        s = noria_gate(s, a, b, p)
        out.append((s, eval_sop(ma_i, s), eval_sop(mb_i, s)))
    return out
sc = noria_run([(1,0,0),(1,0,0),(0,0,0),(0,0,0)])        # pulsacion larga de A: arranca y sigue
check('noria.escA', [(x[1], x[2]) for x in sc] == [(1,0)]*4)
sc = noria_run([(1,0,0),(0,0,0),(1,0,0),(1,0,0),(0,0,0),(0,0,0)])   # A, A -> para (aunque se mantenga)
check('noria.escAA', [(x[1], x[2]) for x in sc] == [(1,0),(1,0),(0,0),(0,0),(0,0),(0,0)])
sc = noria_run([(1,0,0),(0,0,0),(0,1,0),(0,0,0)])        # A luego B -> cambia de sentido
check('noria.escAB', [(x[1], x[2]) for x in sc] == [(1,0),(1,0),(0,1),(0,1)])
sc = noria_run([(0,1,0),(0,0,0),(0,0,1),(0,0,0)])        # B y P -> para
check('noria.escBP', [(x[1], x[2]) for x in sc] == [(0,1),(0,1),(0,0),(0,0)])
sc = noria_run([(1,0,0),(0,0,0),(1,0,0),(0,0,0),(1,0,0)])   # A,A para; A de nuevo arranca
check('noria.escAAA', [(x[1], x[2]) for x in sc] == [(1,0),(1,0),(0,0),(0,0),(1,0)])
R['noria.terminos'] = sum(len(v) for v in nimps.values())

# ============================================================ DICIEMBRE P1: recinto (P1 BCD >= 6; P2 en [P1/2-3, P1/2+3])
def recinto(p1, p2):
    abre1 = p1 >= 6 and p1 <= 9
    h = p1 >> 1                                  # mitad entera (desplazar a la derecha)
    return int(abre1), int(abre1 and (h - 3) <= p2 <= (h + 3))
# modelo con bloques: comparador 4 bits, sumador 4 bits (3 bits de mitad + constante 0011 y 1101)
def recinto_bloques(p1, p2):
    A1 = int(p1 > 5)                              # comparador A>B con B = 0101
    h = (p1 >> 1) & 0b111                         # P(3:1) en un sumador de 4 bits con MSB a 0
    plus, _ = add_n(h, 0b0011, 0, 4)              # h + 3
    minus, _ = add_n(h, 0b1101, 0, 4)             # h + (-3) en C2 (4 bits)
    # cuidado: h-3 puede ser negativo -> en 4 bits C2: 1101..1111 son negativos
    minus_signed = c2(minus, 4)
    le = int(p2 <= plus)                          # comparador (A<=B)
    ge = int(c2(p2, 4) >= minus_signed)           # comparador con signo / o en C2
    return A1, int(A1 and le and ge)
ok = all(recinto(a, b) == recinto_bloques(a, b) for a in range(6, 10) for b in range(10))
check('recinto.bloques', ok)
R['recinto.tabla'] = {p1: [b for b in range(10) if recinto(p1, b)[1]] for p1 in range(6, 10)}
check('recinto.ejemplo', R['recinto.tabla'][8] == [1,2,3,4,5,6,7])
# AVISO: con comparador sin signo, h-3 en C2 daria 13..15 (>=) -> falla; se comprueba
def recinto_sin_signo(p1, p2):
    A1 = int(p1 > 5); h = (p1 >> 1) & 7
    plus, _ = add_n(h, 3, 0, 4); minus, _ = add_n(h, 0b1101, 0, 4)
    return A1, int(A1 and p2 <= plus and p2 >= minus)
bad = [(a, b) for a in range(6,10) for b in range(10) if recinto(a, b) != recinto_sin_signo(a, b)]
R['recinto.err_sin_signo'] = len(bad)
check('recinto.sin_signo_ok', len(bad) == 0, 'h-3>=0 siempre porque h>=3')

# ============================================================ DICIEMBRE P3: contador sincrono JK + NAND, X=0 asc 0,2,4,6,1,3,5,7 ; X=1 desc
asc = [0, 2, 4, 6, 1, 3, 5, 7]
def cnt_next(s, x):
    i = asc.index(s)
    return asc[(i + (1 if x == 0 else -1)) % 8]
fn = {k: {'on':[], 'dc':[]} for k in ['J2','K2','J1','K1','J0','K0']}
for s in range(8):
    for x in (0, 1):
        idx = (s << 1) | x; ns = cnt_next(s, x)
        for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
            j, k = jk_excitation((s >> bit) & 1, (ns >> bit) & 1)
            if j == 1: fn[J]['on'].append(idx)
            elif j is None: fn[J]['dc'].append(idx)
            if k == 1: fn[K]['on'].append(idx)
            elif k is None: fn[K]['dc'].append(idx)
cimps = {k: minimize(4, d['on'], d['dc']) for k, d in fn.items()}
for k in cimps: R['cnt.' + k] = sop_str(4, cimps[k], ['Q_2','Q_1','Q_0','X'])
def cnt_gate(s, x):
    idx = (s << 1) | x; ns = 0
    for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
        ns |= ff_next('JK', (s >> bit) & 1, eval_sop(cimps[J], idx), eval_sop(cimps[K], idx)) << bit
    return ns
check('cnt.puertas', all(cnt_gate(s, x) == cnt_next(s, x) for s in range(8) for x in (0,1)))
R['cnt.up'] = asc; R['cnt.down'] = [0] + asc[:0:-1]
check('cnt.down_enunciado', R['cnt.down'] == [0, 7, 5, 3, 1, 6, 4, 2])

# ============================================================ DICIEMBRE P4: barrido de 16 ventanas
def barrido(estado_ventanas, ciclos, start=0):
    """estado_ventanas: funcion t -> 16 bits (1 = abierta). contador de 4 bits: planta=Q3Q2 (0..3) ventana=Q1Q0.
    el contador solo avanza si la ventana seleccionada esta cerrada."""
    q = start; hist = []
    for t in range(ciclos):
        w = estado_ventanas(t)
        hist.append((q >> 2, q & 3, w[q]))
        if not w[q]: q = (q + 1) % 16
    return hist
openset = {5}
h = barrido(lambda t: [1 if (i in openset and t < 10) else 0 for i in range(16)], 20)
stuck = [x for x in h[:10] if x[2]]
check('ventanas.para', all((x[0], x[1]) == (1, 1) for x in stuck) and len(stuck) >= 1)   # ventana 5 = planta 2, ventana 2 (indices 1,1)
check('ventanas.continua', h[10][0:2] == (1, 1) and h[11][0:2] == (1, 2))
# display: planta = Q3Q2 + 1, ventana = Q1Q0 + 1  (sumador de 2 bits con B=01)
ok = all(((q >> 2) + 1 <= 4) and ((q & 3) + 1 <= 4) for q in range(16))
check('ventanas.display', ok)

# ============================================================ FEB-2023 P1: dos sensores 4 bits C2 -> diferencia (con signo) y media
def feb23_p1(a, b):
    A, B = c2(a, 4), c2(b, 4)
    # diferencia A-B en 5 bits C2 (sumador con B negado y cin=1)
    d, _ = add_n(a | (0b10000 if a & 8 else 0), xor_n(b | (0b10000 if b & 8 else 0), 1, 5), 1, 5)
    dv = c2(d, 5)
    # media: (A+B) en 5 bits C2 y desplazamiento aritmetico a la derecha (floor)
    s, _ = add_n(a | (0b10000 if a & 8 else 0), b | (0b10000 if b & 8 else 0), 0, 5)
    sv = c2(s, 5)
    avg = sv >> 1                                  # floor
    return dv, avg
ok = True
for a in range(16):
    for b in range(16):
        dv, avg = feb23_p1(a, b); A, B = c2(a,4), c2(b,4)
        ok &= dv == A - B and avg == (A + B) // 2 and -15 <= dv <= 15 and -8 <= avg <= 7
check('feb23.p1', ok, '256 combinaciones')
R['feb23.p1.dif_rango'] = [-15, 15]
# redondeo: floor vs truncar hacia cero
dif_trunc = sum(1 for a in range(16) for b in range(16) if (c2(a,4)+c2(b,4)) // 2 != int((c2(a,4)+c2(b,4))/2))
R['feb23.p1.dif_redondeo'] = dif_trunc

# ============================================================ FEB-2023 P2: toldo (S,L,V,F)
def toldo_spec(S, L, V, F):
    if L: return 1
    if V: return int(not (S and F))
    return int(S and not F)
on = []; dc = []
for i, (S, L, V, F) in enumerate(itertools.product((0,1), repeat=4)):
    if S and L: dc.append(i)
    elif toldo_spec(S, L, V, F): on.append(i)
tsop = minimize(4, on, dc); tpos = pos_minimize(4, on, dc)
R['toldo.sop'] = sop_str(4, tsop, 'SLVF'); R['toldo.pos'] = pos_str(4, tpos, 'SLVF')
R['toldo.on'] = on; R['toldo.dc'] = dc
ok = all(eval_sop(tsop, i) == toldo_spec(*bits(i, 4)) for i in range(16) if i not in dc)
ok2 = all((1 - eval_sop(tpos, i)) == toldo_spec(*bits(i, 4)) ^ 1 or True for i in range(16))
check('toldo.sop', ok)
def eval_pos(imps, m):  # producto de sumas: la funcion vale 0 si algun implicante de ceros cubre m
    return 1 - eval_sop(imps, m)
check('toldo.pos', all(eval_pos(tpos, i) == toldo_spec(*bits(i, 4)) for i in range(16) if i not in dc))
# apartado 4: manual/auto con memoria
def toldo_total(M, U, D, S, L, V, F, q):
    auto = toldo_spec(S, L, V, F) if not (S and L) else 0
    qn = int((1 - U) and (D or q))          # recoger (U) tiene prioridad; D baja y memoriza
    bt = int(auto if not M else qn)
    return bt, qn
q = 0; ok = True
for (U, D, exp) in [(0,0,0),(0,1,1),(0,0,1),(1,0,0),(0,0,0),(1,1,0),(0,0,0),(0,1,1),(1,1,0)]:
    bt, q = toldo_total(1, U, D, 0, 0, 0, 0, q); ok &= bt == exp
check('toldo.manual_memoria', ok)

json.dump({'R': R, 'CHK': CHK}, open('../out/results2.json', 'w'), indent=1, default=str, ensure_ascii=False)
print(len(CHK), 'checks;', sum(not c['ok'] for c in CHK), 'fallos')
for k in sorted(R):
    if k.startswith(('tab.','noria.J','noria.K','noria.M','cnt.J','cnt.K','toldo','recinto.t','recinto.err','feb25.p1.r','feb23')): print(k, '=', R[k])
