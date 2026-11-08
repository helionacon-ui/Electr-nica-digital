"""Hojas de problemas: Karnaugh/combinacional y autómatas. Todo verificado."""
import json, itertools, re
from logic import *
from fsm import FSM
R = {}; CHK = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)

def comb(id_, n, names, fun, outs, dc=lambda *x: False, latex=True):
    """fun(*bits)-> tupla de salidas (o None si dc). Devuelve sop por salida, comprueba exhaustivo."""
    res = {}
    for k, oname in enumerate(outs):
        on = []; dcs = []
        for i in range(2 ** n):
            b = bits(i, n)
            if dc(*b): dcs.append(i); continue
            v = fun(*b)
            if v is None: dcs.append(i); continue
            if v[k]: on.append(i)
        imps = minimize(n, on, dcs)
        ok = all(eval_sop(imps, i) == (1 if i in on else 0) for i in range(2 ** n) if i not in dcs)
        check(f'{id_}.{oname}', ok)
        res[oname] = {'sop': sop_str(n, imps, names), 'on': on, 'dc': dcs, 'imps': imps, 'n': n}
        R[f'{id_}.{oname}'] = res[oname]['sop']
        R[f'{id_}.{oname}.on'] = on; R[f'{id_}.{oname}.dc'] = dcs
    return res

# ---- K1 mayoria de 3
comb('k1', 3, ['S_2','S_1','S_0'], lambda a,b,c: (int(a+b+c >= 2),), ['S'])
# ---- K2 divisor 2 bits
def div2(a1,a0,b1,b0):
    A = a1*2+a0; B = b1*2+b0
    if B == 0: return None
    q, r = divmod(A, B); return (q>>1&1, q&1, r>>1&1, r&1)
comb('k2', 4, ['A_1','A_0','B_1','B_0'], div2, ['C1','C0','R1','R0'])
# ---- K4 multiplicador 2x2
comb('k4', 4, ['A_1','A_0','B_1','B_0'], lambda a1,a0,b1,b0: tuple(((a1*2+a0)*(b1*2+b0)) >> k & 1 for k in (3,2,1,0)), ['S3','S2','S1','S0'])
# ---- K5 produccion en serie (4 unidades)
def prod(s3,s2,s1,s0):
    n = s3+s2+s1+s0
    return (int(n==4), int(n>=3), int(n==2), int(n<=1))
comb('k5', 4, ['S_3','S_2','S_1','S_0'], prod, ['TA','MA','I','MR'])
# ---- K6 barco: N S E O -> a..g
SEG = 'abcdefg'
def barco(N,S,E,O):
    if (N and S) or (E and O): return None
    act = set()
    if N and not (E or O): act |= {'a'}
    if S and not (E or O): act |= {'d'}
    if E and not (N or S): act |= {'b','c'}
    if O and not (N or S): act |= {'e','f'}
    if N and E: act |= {'a','b'}
    if N and O: act |= {'a','f'}
    if S and E: act |= {'c','d'}
    if S and O: act |= {'d','e'}
    if not (N or S or E or O): return None
    return tuple(int(c in act) for c in SEG)
comb('k6', 4, ['N','S','E','O'], barco, list(SEG))
# ---- K7 decodificador BCD -> 7seg (activos a 1)
def dec7(a,b,c,d):
    v = a*8+b*4+c*2+d
    if v > 9: return None
    return tuple(int(x) for x in bcd7seg(v))
comb('k7', 4, ['A','B','C','D'], dec7, list(SEG))
# ---- K8 comparador 2 bits
comb('k8', 4, ['A_1','A_0','B_1','B_0'], lambda a1,a0,b1,b0: (int(a1*2+a0 > b1*2+b0), int(a1*2+a0 == b1*2+b0), int(a1*2+a0 < b1*2+b0)), ['GT','EQ','LT'])
# ---- K9 maquina registradora: monedas 25,25,10,5 ; precio 40
def maq(e25a,e25b,e10,e5):
    s = 25*e25a + 25*e25b + 10*e10 + 5*e5
    p = int(s >= 40); ch = s - 40 if p else 0
    return (p, int(ch >= 20), int(ch >= 10 and ch != 20 and ch != 25 or ch in (20,25) and True), int(ch % 10 == 5))
def maq2(e25a,e25b,e10,e5):
    s = 25*e25a + 25*e25b + 10*e10 + 5*e5
    p = int(s >= 40); ch = s - 40 if p else 0
    # dispensadores: dos de 10 y uno de 5 -> ch = 10*n10 + 5*n5
    n10 = ch // 10; n5 = (ch % 10) // 5
    return (p, int(n10 >= 1), int(n10 >= 2), n5)
comb('k9', 4, ['E_{25A}','E_{25B}','E_{10}','E_5'], maq2, ['P','C10A','C10B','C5'])
R['k9.max'] = max(25*a+25*b+10*c+5*d for a,b,c,d in itertools.product((0,1),repeat=4))
# ---- K10 nota 0..10 -> 7seg
def nota(a,b,c,d):
    v = a*8+b*4+c*2+d
    if v > 10: return None
    act = set()
    if v <= 4: act = {'g'}
    elif v == 5: act = {'a'}
    elif v == 6: act = {'a','b'}
    elif v in (7,8): act = {'a','b','c'}
    elif v == 9: act = {'a','b','c','d'}
    else: act = set('abcdef')
    return tuple(int(c in act) for c in SEG)
comb('k10', 4, ['N_3','N_2','N_1','N_0'], nota, list(SEG))
# ---- K17 binario (4 bits) -> 2 digitos BCD
def b2bcd(e3,e2,e1,e0):
    v = e3*8+e2*4+e1*2+e0
    t, u = divmod(v, 10)
    return (t, u>>3&1, u>>2&1, u>>1&1, u&1)
comb('k17', 4, ['E_3','E_2','E_1','E_0'], b2bcd, ['D','U3','U2','U1','U0'])

# =================================================================== AUTOMATAS
def detector(seq, overlap=True, mealy=True):
    """Detector de secuencia 'seq' (str de 0/1) con solapamiento. Estados = longitud del prefijo mas largo."""
    n = len(seq)
    def nxt(k, x):
        s = seq[:k] + str(x)
        for l in range(min(len(s), n), -1, -1):
            if s.endswith(seq[:l]) and (overlap or l == len(s) or l == 0): return l
        return 0
    return n, nxt

def spec_detect(seq, stream, overlap=True):
    out = []; buf = ''
    for x in stream:
        buf += str(x)
        hit = buf.endswith(seq)
        out.append(int(hit))
        if hit and not overlap: buf = ''
    return out

def build_detector(id_, seq, overlap=True):
    n, nxt = detector(seq, overlap)
    # estados 0..n-1 (al llegar a n se emite 1 y se pasa al estado de solapamiento)
    def step(s, x):
        k = int(s[1:])
        j = nxt(k, x)
        if j == n: return 'S%d' % nxt_after(n), 1
        return 'S%d' % j, 0
    def nxt_after(k):  # estado tras completar: mayor prefijo propio que es sufijo
        for l in range(n - 1, -1, -1):
            if seq.endswith(seq[:l]): return l
        return 0
    states = ['S%d' % i for i in range(n)]
    f = FSM(states, 1, step, nout=1, moore=False, ff='JK')
    check(f'{id_}.puertas', f.verify_table())
    ok = True
    for L in range(1, 13):
        for st in itertools.product((0, 1), repeat=L):
            if f.run(list(st)) != spec_detect(seq, st, overlap): ok = False; break
        if not ok: break
    check(f'{id_}.exhaustivo', ok, 'secuencias hasta longitud 12')
    for k, v in f.eq.items(): R[f'{id_}.{k}'] = v
    R[f'{id_}.nestados'] = len(states); R[f'{id_}.nq'] = f.nq
    R[f'{id_}.trans'] = [(s, x, ns, o) for (s, x, ns, o) in f.rows]
    return f

# A1: 3 o mas unos consecutivos (la salida vale 1 desde el tercer uno, y sigue mientras haya unos)
def step_a1(s, x):
    k = int(s[1:])
    if x == 0: return 'S0', 0
    if k == 0: return 'S1', 0
    if k == 1: return 'S2', 0
    return 'S2', 1
f = FSM(['S0','S1','S2'], 1, step_a1, nout=1, ff='JK'); check('a1.puertas', f.verify_table())
def spec_ge3(stream, bit):
    out = []; run = 0
    for x in stream:
        run = run + 1 if x == bit else 0
        out.append(int(run >= 3))
    return out
ok = all(f.run(list(st)) == spec_ge3(st, 1) for L in range(1, 13) for st in itertools.product((0,1), repeat=L))
check('a1.exhaustivo', ok)
for k, v in f.eq.items(): R['a1.' + k] = v
# A2: 3 o mas ceros consecutivos
def step_a2(s, x):
    k = int(s[1:])
    if x == 1: return 'S0', 0
    if k == 0: return 'S1', 0
    if k == 1: return 'S2', 0
    return 'S2', 1
f2 = FSM(['S0','S1','S2'], 1, step_a2, nout=1, ff='JK'); check('a2.puertas', f2.verify_table())
ok = all(f2.run(list(st)) == spec_ge3(st, 0) for L in range(1, 13) for st in itertools.product((0,1), repeat=L))
check('a2.exhaustivo', ok)
for k, v in f2.eq.items(): R['a2.' + k] = v
# A3: secuencia 1011 con solapamiento
build_detector('a3', '1011')
# A5: 1111 y 11011 (Mealy)... se hacen por separado
build_detector('a5a', '1111')
build_detector('a5b', '11011')
# A7: 1010 o 110 con solapamiento -> autómata para union de secuencias
def a7_step(s, x):
    # estado = sufijo mas largo que es prefijo de 1010 o de 110 (conjunto de prefijos)
    pre = {''}
    for w in ('1010', '110'):
        for l in range(1, len(w) + 1): pre.add(w[:l])
    cur = s.replace('S_', '')
    t = cur + str(x)
    hit = t.endswith('1010') or t.endswith('110')
    best = ''
    for l in range(len(t), -1, -1):
        if t[-l:] in pre and t[-l:] not in ('1010', '110') if l else True:
            best = t[-l:] if l else ''; break
    if hit:
        # tras un acierto: seguimos con el mayor sufijo propio que sea prefijo
        best = ''
        for l in range(len(t) - 1, 0, -1):
            if t[-l:] in pre and t[-l:] not in ('1010', '110'): best = t[-l:]; break
    return 'S_' + best, int(hit)
# construir conjunto alcanzable
seen = ['S_']; todo = ['S_']
while todo:
    c = todo.pop()
    for x in (0, 1):
        n, _ = a7_step(c, x)
        if n not in seen: seen.append(n); todo.append(n)
f7 = FSM(seen, 1, a7_step, nout=1, ff='JK'); check('a7.puertas', f7.verify_table())
def spec_a7(stream):
    out = []; buf = ''
    for x in stream:
        buf += str(x); out.append(int(buf.endswith('1010') or buf.endswith('110')))
    return out
ok = all(f7.run(list(st)) == spec_a7(st) for L in range(1, 13) for st in itertools.product((0,1), repeat=L))
check('a7.exhaustivo', ok, f'{len(seen)} estados')
R['a7.nestados'] = len(seen); R['a7.estados'] = seen
for k, v in f7.eq.items(): R['a7.' + k] = v
# A9: sumador serie Mealy (entradas E1 E0, estado = acarreo)
def sum_step(s, x):
    e1, e0 = x >> 1 & 1, x & 1
    c = int(s == 'B')
    t = e1 + e0 + c
    return ('B' if t >= 2 else 'A'), t & 1
fs = FSM(['A','B'], 2, sum_step, nout=1, ff='JK', in_names=['E_1','E_0']); check('a9.puertas', fs.verify_table())
import random
random.seed(3); ok = True
for _ in range(400):
    n = random.randint(1, 10); a = random.randrange(2**n); b = random.randrange(2**n)
    stream = [((a >> i & 1) << 1) | (b >> i & 1) for i in range(n)]
    outs = fs.run(stream)
    got = sum(o << i for i, o in enumerate(outs))
    ok &= got == (a + b) & ((1 << n) - 1)
check('a9.suma', ok)
for k, v in fs.eq.items(): R['a9.' + k] = v
# A11: contador reversible modulo 4 con Moore y salida de 2 bits (E0=1 asc / 0 desc)
def rev_step(s, x):
    k = int(s[1:]); return 'S%d' % ((k + (1 if x else -1)) % 4), 0
frv = FSM(['S0','S1','S2','S3'], 1, rev_step, nout=2, moore=True, out_moore=lambda s: int(s[1:]), ff='JK', in_names=['E']);
check('a11.puertas', frv.verify_table())
for k, v in frv.eq.items(): R['a11.' + k] = v
outs = frv.run([1,1,1,1,1,0,0,0,0]); R['a11.traza'] = outs
check('a11.traza', outs == [1,2,3,0,1,0,3,2,1])

json.dump({'R': R, 'CHK': CHK}, open('../out/results3.json', 'w'), indent=1, default=str, ensure_ascii=False)
print(len(CHK), 'checks;', sum(not c['ok'] for c in CHK), 'fallos')
for k in ['k1.S','k2.C1','k2.R0','k5.TA','k5.MA','k5.I','k5.MR','k9.P','k9.C10A','k9.C10B','k9.C5','k9.max','k17.D','a1.J1','a1.K1','a1.S0','a3.J1','a3.nq','a7.nestados','a9.J0','a9.K0','a9.S0','a11.J1','a11.K1','a11.J0','a11.K0','a11.S1','a11.S0']:
    print(k, '=', R.get(k))
