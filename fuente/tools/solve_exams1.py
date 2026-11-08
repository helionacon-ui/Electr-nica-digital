"""Resolución y verificación por código de los problemas de examen (bloque 1).
Todo lo que se publica en la guía (ecuaciones, tablas, secuencias) sale de aquí."""
import json, random
from logic import *

R = {}      # resultados publicables
CHK = []    # (id, ok, detalle)
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)

# ---------------------------------------------------------------- DIC-2024 P1: invernadero
# M = 1 si T o V o H (P no interviene)
tt = [(T, V, H, int(T or V or H)) for T in (0,1) for V in (0,1) for H in (0,1)]
on = [i for i,(T,V,H,M) in enumerate(tt) if M]
sop = minimize(3, on); R['inv.sop'] = sop_str(3, sop, 'TVH')
pos = pos_minimize(3, on); R['inv.pos'] = pos_str(3, pos, 'TVH')
check('inv.sop', sorted(R['inv.sop'].split(' + ')) == ['H','T','V'], R['inv.sop'])
R['inv.sop'] = 'T + V + H'
check('inv.pos', R['inv.pos'] == '(T + V + H)', R['inv.pos'])
# NAND: M = NAND(!T,!V,!H)
nand = lambda *x: 1 - int(all(x))
check('inv.nand', all(nand(1-T,1-V,1-H) == M for T,V,H,M in tt))
R['inv.minterms'] = on

# ---------------------------------------------------------------- Media de 4 números BCD de 2 cifras
def bcd2bin(d1, d0):
    # 10*d1 + d0 = 8*d1 + 2*d1 + d0 , con sumadores de 8 bits
    s = (d1 << 3) + (d1 << 1)
    assert s < 256
    return s + d0
ok = all(bcd2bin(a, b) == 10*a + b for a in range(10) for b in range(10))
check('media4.bcd2bin', ok)
# Arquitectura correcta: S = A+B+C+D (9 bits), resultado = S>>2 (7 bits)
def media_ok(A, B, C, D): return (A + B + C + D) >> 2
# Arquitectura en cascada de la solución de referencia: ((A+B)>>1 + (C+D)>>1)>>1
def media_cascada(A, B, C, D): return (((A + B) >> 1) + ((C + D) >> 1)) >> 1
bad = 0; tot = 0; maxerr = 0
for s1 in range(199):
    for s2 in range(199):
        tot += 1
        v1 = ((s1 >> 1) + (s2 >> 1)) >> 1
        v2 = (s1 + s2) >> 2
        if v1 != v2: bad += 1; maxerr = max(maxerr, v2 - v1)
R['media4.cascada_malas'] = bad; R['media4.cascada_total'] = tot
R['media4.cascada_pct'] = round(100.0 * bad / tot, 1)
R['media4.maxerr'] = maxerr
ex = None
for s1 in range(199):
    for s2 in range(199):
        if (((s1>>1)+(s2>>1))>>1) != ((s1+s2)>>2): ex = (s1, s2); break
    if ex: break
R['media4.ejemplo'] = ex
check('media4.cascada_difiere', bad > 0 and maxerr == 1, f'{bad}/{tot}')
# rango del resultado: 7 bits
check('media4.rango', max(media_ok(99,99,99,99), 0) == 99 and 99 < 128)
# bits necesarios: A+B+C+D <= 396 < 512 -> 9 bits
check('media4.bits', 4*99 < 2**9 and 4*99 > 2**8)

# ---------------------------------------------------------------- Biestables T + XOR (cronograma)
def tstep(q2, q1, q0):
    t2 = q1 ^ q0; t1 = q0; t0 = 1 - q2
    return (q2 ^ t2, q1 ^ t1, q0 ^ t0), (t2, t1, t0)
s = (0, 0, 0); seq = [s]; rows = []
for _ in range(10):
    n, t = tstep(*s); rows.append((s, t, n)); s = n
    if s == (0, 0, 0): break
    seq.append(s)
vals = [from_bits(x) for x in seq]
R['t.secuencia'] = vals + [0]
R['t.tabla'] = [{'q': ''.join(map(str, r[0])), 't': ''.join(map(str, r[1])), 'n': ''.join(map(str, r[2]))} for r in rows]
check('t.secuencia', vals == [0, 1, 6, 2, 7, 5, 3], str(vals))
check('t.periodo', len(rows) == 7)

# ---------------------------------------------------------------- Caja fuerte A A B A (Mealy, 8 estados, JK)
# entradas (a,b): 00 nada, 10 tecla A, 01 tecla B, 11 imposible (don't care)
NAMES = ['S0','S1','S2','S3','S4','S5','S6','S7']
def caja_next(s, a, b):
    """Devuelve (s', z) -- modelo del diagrama de estados."""
    x = (a, b)
    if x == (1, 1): return None   # don't care
    A, B, N = x == (1, 0), x == (0, 1), x == (0, 0)
    if s == 0: return (1, 0) if A else (0, 0)
    if s == 1: return (1, 0) if A else ((2, 0) if N else (0, 0))
    if s == 2: return (2, 0) if N else ((3, 0) if A else (0, 0))
    if s == 3: return (3, 0) if A else ((4, 0) if N else (0, 0))
    if s == 4: return (4, 0) if N else ((5, 0) if B else (0, 0))
    if s == 5: return (5, 0) if B else ((6, 0) if N else (0, 0))
    if s == 6: return (6, 0) if N else ((7, 1) if A else (0, 0))
    if s == 7: return (7, 0) if A else (0, 0)
R['caja.estados'] = {
 'S0':'Reposo, esperando la primera A', 'S1':'A nº1 pulsada (se mantiene)', 'S2':'A nº1 soltada, espera A nº2',
 'S3':'A nº2 pulsada (se mantiene)', 'S4':'A nº2 soltada, espera B', 'S5':'B pulsada (se mantiene)',
 'S6':'B soltada, espera A nº3', 'S7':'A final pulsada (caja abierta, espera soltar)'}
# tabla de transiciones: variables Q2 Q1 Q0 a b  (5 variables)
vars_ = ['Q_2','Q_1','Q_0','a','b']
fn = {k: {'on': [], 'dc': []} for k in ['J2','K2','J1','K1','J0','K0','Z']}
for s_ in range(8):
    for a in (0,1):
        for b in (0,1):
            idx = (s_ << 2) | (a << 1) | b
            r = caja_next(s_, a, b)
            if r is None:
                for k in fn: fn[k]['dc'].append(idx)
                continue
            ns, z = r
            if z: fn['Z']['on'].append(idx)
            for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
                q = (s_ >> bit) & 1; qn = (ns >> bit) & 1
                j, k = jk_excitation(q, qn)
                if j == 1: fn[J]['on'].append(idx)
                elif j is None: fn[J]['dc'].append(idx)
                if k == 1: fn[K]['on'].append(idx)
                elif k is None: fn[K]['dc'].append(idx)
imps = {}
for k, d in fn.items():
    imps[k] = minimize(5, d['on'], d['dc'])
    R['caja.' + k] = sop_str(5, imps[k], vars_)
# Comprobación a nivel de puerta: simular el circuito JK con las ecuaciones minimizadas
def caja_gate(s, a, b):
    idx = (s << 2) | (a << 1) | b
    ns = 0
    for bit, (J, K) in zip((2,1,0), (('J2','K2'),('J1','K1'),('J0','K0'))):
        j = eval_sop(imps[J], idx); k = eval_sop(imps[K], idx)
        q = (s >> bit) & 1
        ns |= ff_next('JK', q, j, k) << bit
    return ns, eval_sop(imps['Z'], idx)
ok = True
for s_ in range(8):
    for a, b in ((0,0),(1,0),(0,1)):
        ok &= caja_gate(s_, a, b) == caja_next(s_, a, b)
check('caja.puertas==diagrama', ok)
# Especificación independiente: gestos A,A,B,A separados por reposo; cualquier error reinicia
def spec_caja(stream):
    """stream: lista de (a,b). Devuelve lista Z. Especificación a nivel de gestos."""
    gest = []          # gestos completados desde el último reinicio
    cur = None         # tecla en curso ('A'/'B'/None)
    out = []
    target = ['A','A','B','A']
    for (a, b) in stream:
        key = 'A' if (a, b) == (1,0) else ('B' if (a, b) == (0,1) else None)
        z = 0
        if key is None:                    # soltar
            if cur is not None: gest.append(cur); cur = None
        else:
            if cur is None:                # pulsación nueva
                exp = target[len(gest)] if len(gest) < 4 else None
                if exp == key:
                    cur = key
                    if len(gest) == 3: z = 1       # cuarta tecla correcta
                else:
                    gest = []; cur = None
            elif cur != key:               # cambia de tecla sin soltar
                gest = []; cur = None
        out.append(z)
        # tras abrir, se queda 'sujetando' A; al soltar vuelve a empezar
        if len(gest) == 3 and cur == 'A' and z: pass
    return out
# El modelo de gestos no resetea tras la cuarta; lo ajustamos: tras Z=1 y soltar -> reinicio
def spec_caja2(stream):
    out = []; gest = []; cur = None; opened_hold = False
    target = ['A','A','B','A']
    for (a, b) in stream:
        key = 'A' if (a, b) == (1,0) else ('B' if (a, b) == (0,1) else None)
        z = 0
        if opened_hold:
            if key != 'A': opened_hold = False; gest = []; cur = None
        elif key is None:
            if cur is not None: gest.append(cur); cur = None
        else:
            if cur is None:
                if len(gest) < 4 and target[len(gest)] == key:
                    if len(gest) == 3: z = 1; opened_hold = True
                    else: cur = key
                else: gest = []; cur = None
            elif cur != key: gest = []; cur = None
        out.append(z)
    return out
random.seed(7)
ok = True; n_tests = 0
syms = [(0,0),(1,0),(0,1)]
import itertools
for L in range(1, 9):
    for st in itertools.product(syms, repeat=L):
        s_ = 0; zs = []
        for (a, b) in st:
            s_, z = caja_gate(s_, a, b); zs.append(z)
        n_tests += 1
        if zs != spec_caja2(list(st)): ok = False; bad_st = st; break
    if not ok: break
check('caja.exhaustivo', ok, f'{n_tests} secuencias de longitud<=8' if ok else str(bad_st))
R['caja.n_tests'] = n_tests
# secuencia correcta abre; variantes no
good = [(1,0),(0,0),(1,0),(0,0),(0,1),(0,0),(1,0)]
s_ = 0; z_last = 0
for (a,b) in good: s_, z_last = caja_gate(s_, a, b)
check('caja.abre', z_last == 1)
bad_ = [(1,0),(0,0),(0,1),(0,0),(0,1),(0,0),(1,0)]
s_ = 0; zz = []
for (a,b) in bad_: s_, z = caja_gate(s_, a, b); zz.append(z)
check('caja.no_abre_error', sum(zz) == 0)
# sin soltar: A,A seguidas sin reposo NO cuenta como dos pulsaciones
s_ = 0; zz=[]
for (a,b) in [(1,0),(1,0),(0,1),(0,0),(1,0)]: s_, z = caja_gate(s_, a, b); zz.append(z)
check('caja.sin_soltar', sum(zz) == 0)
R['caja.literales'] = sum(len(p) and (5 - bin(p[1]).count('1')) for k in imps for p in imps[k])
R['caja.terminos'] = sum(len(imps[k]) for k in imps)

json.dump({'R': R, 'CHK': CHK}, open('../out/results1.json', 'w'), indent=1, default=str, ensure_ascii=False)
print(len(CHK), 'checks;', sum(not c['ok'] for c in CHK), 'fallos')
for k in ['inv.sop','inv.pos','media4.cascada_pct','media4.ejemplo','t.secuencia']+['caja.'+x for x in ['J2','K2','J1','K1','J0','K0','Z']]:
    print(k, '=', R[k])
print('terminos', R['caja.terminos'], 'literales', R['caja.literales'])
