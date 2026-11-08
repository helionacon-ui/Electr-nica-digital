"""Simulacros: todos los resultados que se publican salen de aquí y se verifican."""
import json, itertools, math
from logic import *
from fsm import FSM
R = {}; CHK = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)

# ============================================================ SIMULACRO 1
# P1 Gray -> binario de 3 bits
def gray(b): return b ^ (b >> 1)
names = ['G_2', 'G_1', 'G_0']
for k in (2, 1, 0):
    on = [g for g in range(8) if (next(b for b in range(8) if gray(b) == g) >> k) & 1]
    imps = minimize(3, on)
    R[f's1p1.B{k}'] = sop_str(3, imps, names)
    R[f's1p1.B{k}.on'] = on
    check(f's1p1.B{k}', all(eval_sop(imps, g) == ((next(b for b in range(8) if gray(b) == g) >> k) & 1) for g in range(8)))
def g2b(g2, g1, g0): return (g2, g2 ^ g1, g2 ^ g1 ^ g0)
check('s1p1.xor', all(g2b(*bits(gray(b), 3)) == tuple(bits(b, 3)) for b in range(8)))
R['s1p1.seq'] = [gray(b) for b in range(8)]
R['s1p1.seqbin'] = [format(gray(b), '03b') for b in range(8)]
# P2 sumador BCD de un digito
ok = True; corr = {}
for a in range(10):
    for b in range(10):
        for c in (0, 1):
            s = a + b + c; k = s >> 4; s4 = s & 15
            adj = int(k or (s4 >> 3 & 1 and (s4 >> 2 & 1 or s4 >> 1 & 1)))
            bcd = s4 + (6 if adj else 0)
            res = (adj, bcd & 15)
            ok &= (res[0] * 10 + res[1]) == a + b + c
            ok &= (adj == int(s > 9))
check('s1p2.bcd', ok)
R['s1p2.max'] = 9 + 9 + 1
ex = [(7, 8, 0), (9, 9, 1), (4, 3, 0)]
R['s1p2.ejemplos'] = []
for a, b, c in ex:
    s = a + b + c; s4 = s & 15; adj = int(s > 9)
    R['s1p2.ejemplos'].append({'a': a, 'b': b, 'c': c, 'bin': format(s, '05b'), 'sum': s, 'adj': adj,
                               'fin': format(((s4 + 6) if adj else s4), '05b')})
# P3 contador JK 0,2,5,7
seq = ['A', 'B', 'C', 'D']; enc = {'A': 0, 'B': 2, 'C': 5, 'D': 7}
def cstep(s, x): return seq[(seq.index(s) + 1) % 4], 0
f = FSM(seq, 0, cstep, nout=1, moore=True, out_moore=lambda s: int(s == 'D'), enc=enc, ff='JK')
check('s1p3.puertas', f.verify_table())
st = 'A'; trace = []
code = enc['A']; trace = [code]
for _ in range(8):
    code, _o = f.gate_step(code, 0); trace.append(code)
check('s1p3.secuencia', trace == [0, 2, 5, 7, 0, 2, 5, 7, 0], str(trace))
for k, v in f.eq.items(): R['s1p3.' + k] = v
# autoarranque: estados no usados 1,3,4,6 -> a donde van
nxt_unused = {}
for c in (1, 3, 4, 6):
    nxt_unused[c] = f.gate_step(c, 0)[0]
R['s1p3.sin_uso'] = nxt_unused
# alcanzan la secuencia?
def reach(c):
    seen = []
    while c not in (0, 2, 5, 7) and c not in seen: seen.append(c); c = f.gate_step(c, 0)[0]
    return c in (0, 2, 5, 7)
check('s1p3.lazo', not any(reach(c) for c in (1, 3, 4, 6)) and sorted(nxt_unused.values()) == [1, 3, 4, 6], str(nxt_unused))
R['s1p3.autoarranque'] = all(reach(c) for c in (1, 3, 4, 6))
# P4 detector 0110
def spec_detect(seq_, stream):
    out = []; buf = ''
    for x in stream:
        buf += str(x); out.append(int(buf.endswith(seq_)))
    return out
def det_step(s, x):
    k = int(s[1:]); t = ('0110'[:k] + str(x))
    hit = t == '0110'
    for l in range(min(len(t), 3 if hit else 4), -1, -1):
        if l == 0 or t.endswith('0110'[:l]) : nk = l; break
    return 'S%d' % nk, int(hit)
fd = FSM(['S0', 'S1', 'S2', 'S3'], 1, det_step, nout=1, ff='JK')
check('s1p4.puertas', fd.verify_table())
ok = all(fd.run(list(s)) == spec_detect('0110', s) for L in range(1, 13) for s in itertools.product((0, 1), repeat=L))
check('s1p4.exhaustivo', ok)
for k, v in fd.eq.items(): R['s1p4.' + k] = v
R['s1p4.trans'] = [(s, x, ns, o) for (s, x, ns, o) in fd.rows]

# ============================================================ SIMULACRO 2
# P1 codificador de prioridad 4:2 con validez
def penc(i3, i2, i1, i0):
    if i3: return (1, 1, 1)
    if i2: return (1, 1, 0)
    if i1: return (1, 0, 1)
    if i0: return (1, 0, 0)
    return (0, 0, 0)
nm = ['I_3', 'I_2', 'I_1', 'I_0']
for k, nmo in enumerate(['V', 'A1', 'A0']):
    on = [i for i in range(16) if penc(*bits(i, 4))[k]]
    imps = minimize(4, on)
    R[f's2p1.{nmo}'] = sop_str(4, imps, nm)
    R[f's2p1.{nmo}.on'] = on
    check(f's2p1.{nmo}', all(eval_sop(imps, i) == penc(*bits(i, 4))[k] for i in range(16)))
# P2 multiplicar por 5
check('s2p2.x5', all(((x << 2) + x) == 5 * x and 5 * x < 128 for x in range(16)))
R['s2p2.max'] = 5 * 15; R['s2p2.bits'] = (5 * 15).bit_length()
# P3 temporización con 50 MHz
f0 = 50_000_000
R['s2p3.bits1hz'] = math.ceil(math.log2(f0 // 2))      # cuenta hasta 25e6 para conmutar cada medio segundo
check('s2p3.bits', 2 ** 24 < 25_000_000 <= 2 ** 25 and R['s2p3.bits1hz'] == 25)
R['s2p3.cuenta'] = 25_000_000 - 1
bd = 19
check('s2p3.antirrebote', 2 ** 18 < 500_000 <= 2 ** 19)
R['s2p3.fbarrido'] = round(f0 / 2 ** 17, 1)
R['s2p3.fdigito'] = round(f0 / 2 ** 17 / 4, 1)
check('s2p3.refresco', 95 < f0 / 2 ** 17 / 4 < 96 and f0 / 2 ** 17 / 4 > 60)
# P4 maquina de 30 cts con monedas de 10 y 20 -> Z (producto) y C (cambio de 10)
def vstep(s, x):
    k = int(s[1:]); v = 10 * k + (10 if x == 1 else 20 if x == 2 else 0)
    if v >= 30: return 'S0', (1 | (2 if v == 40 else 0))
    return 'S%d' % (v // 10), 0
fv = FSM(['S0', 'S1', 'S2'], 2, vstep, nout=2, ff='JK', in_names=['M_{20}', 'M_{10}'], dc_inputs=(3,))
check('s2p4.puertas', fv.verify_table())
def spec_v(stream):
    tot = 0; out = []
    for x in stream:
        tot += 10 if x == 1 else 20 if x == 2 else 0
        if tot >= 30: out.append(1 | (2 if tot == 40 else 0)); tot = 0
        else: out.append(0)
    return out
ok = all(fv.run(list(s)) == spec_v(s) for L in range(1, 9) for s in itertools.product((0, 1, 2), repeat=L))
check('s2p4.exhaustivo', ok)
for k, v in fv.eq.items(): R['s2p4.' + k] = v
R['s2p4.trans'] = [(s, x, ns, o) for (s, x, ns, o) in fv.rows]

json.dump({'R': R, 'CHK': CHK}, open('../out/results5.json', 'w'), indent=1, default=str, ensure_ascii=False)
print(len(CHK), 'checks;', sum(not c['ok'] for c in CHK), 'fallos')
for k, v in R.items():
    if not k.endswith('.on'): print(k, '=', str(v)[:120])
