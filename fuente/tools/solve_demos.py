"""Comprobación exhaustiva de los enunciados que se demuestran en la guía."""
import json, itertools
from logic import *
R = {}; CHK = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
B = (0, 1)
check('d.demorgan', all((1 - (a | b)) == ((1 - a) & (1 - b)) and (1 - (a & b)) == ((1 - a) | (1 - b)) for a in B for b in B))
check('d.demorgan3', all((1 - (a | b | c)) == ((1 - a) & (1 - b) & (1 - c)) for a in B for b in B for c in B))
check('d.absorcion', all((a | (a & b)) == a and (a & (a | b)) == a for a in B for b in B))
check('d.adyacencia', all(((a & b) | (a & (1 - b))) == a for a in B for b in B))
check('d.consenso', all(((a & b) | ((1 - a) & c) | (b & c)) == ((a & b) | ((1 - a) & c)) for a in B for b in B for c in B))
check('d.xor', all((a ^ b) == ((a & (1 - b)) | ((1 - a) & b)) for a in B for b in B))
check('d.a_mas_nb', all(((a & b) | (a & (1 - b)) | ((1 - a) & b)) == (a | b) for a in B for b in B))
nand = lambda a, b: 1 - (a & b)
check('d.nand_not', all(nand(a, a) == 1 - a for a in B))
check('d.nand_and', all(nand(nand(a, b), nand(a, b)) == (a & b) for a in B for b in B))
check('d.nand_or', all(nand(nand(a, a), nand(b, b)) == (a | b) for a in B for b in B))
nor = lambda a, b: 1 - (a | b)
check('d.nor_universal', all(nor(a, a) == 1 - a and nor(nor(a, b), nor(a, b)) == (a | b) and nor(nor(a, a), nor(b, b)) == (a & b) for a in B for b in B))
# complemento a 2
for n in (3, 4, 5, 8):
    check(f'd.c2.{n}', all(((~x & (2 ** n - 1)) + 1) % 2 ** n == (-x) % 2 ** n for x in range(2 ** n)))
# sumador completo
check('d.fa', all(((a ^ b ^ c) == (a + b + c) % 2) and (((a & b) | (c & (a ^ b))) == (a + b + c) // 2) for a in B for b in B for c in B))
check('d.fa2', all(((a & b) | (c & (a | b))) == (a + b + c) // 2 for a in B for b in B for c in B))
# resta
for n in (4, 8): check(f'd.resta.{n}', all((a + ((~b) & (2 ** n - 1)) + 1) % 2 ** n == (a - b) % 2 ** n for a in range(2 ** n) for b in range(2 ** n)))
# JK
check('d.jk', all(ff_next('JK', q, j, k) == ((j & (1 - q)) | ((1 - k) & q)) for q in B for j in B for k in B))
check('d.t', all(ff_next('T', q, t) == (t ^ q) for q in B for t in B))
# excitacion JK
exc = {(0, 0): (0, None), (0, 1): (1, None), (1, 0): (None, 1), (1, 1): (None, 0)}
okk = True
for (q, qn), (j, k) in exc.items():
    for jj in B:
        for kk in B:
            if (j is None or jj == j) and (k is None or kk == k):
                okk &= ff_next('JK', q, jj, kk) == qn
check('d.excitacion_jk', okk)
check('d.excitacion_fn', all(jk_excitation(q, qn) == exc[(q, qn)] for q in B for qn in B))
# numero de funciones
for n in (1, 2, 3):
    fs = set(itertools.product(B, repeat=2 ** n)); check(f'd.nfun.{n}', len(fs) == 2 ** (2 ** n))
R['d.nfun4'] = 2 ** 16
# bits
check('d.bits', all((N - 1).bit_length() == __import__('math').ceil(__import__('math').log2(N)) for N in range(2, 1025)))
# Johnson y anillo
def johnson(n):
    s = (0,) * n; seen = []
    while s not in seen: seen.append(s); s = (1 - s[-1],) + s[:-1]
    return len(seen)
check('d.johnson', all(johnson(n) == 2 * n for n in range(1, 9)))
def ring(n):
    s = (1,) + (0,) * (n - 1); seen = []
    while s not in seen: seen.append(s); s = (s[-1],) + s[:-1]
    return len(seen)
check('d.anillo', all(ring(n) == n for n in range(1, 9)))
# LFSR maximo (polinomios primitivos x^n + x^(n-1) + 1 no siempre; usamos taps conocidos)
TAPS = {3: (3, 2), 4: (4, 3), 5: (5, 3), 6: (6, 5), 7: (7, 6)}
def lfsr(n, taps):
    s = 1; seen = set()
    while s not in seen:
        seen.add(s); fb = 0
        for t in taps: fb ^= (s >> (t - 1)) & 1
        s = ((s << 1) | fb) & (2 ** n - 1)
    return len(seen)
res = {n: lfsr(n, t) for n, t in TAPS.items()}
check('d.lfsr', all(res[n] == 2 ** n - 1 for n in res), str(res))
R['d.lfsr_ciclos'] = res
# divisor de frecuencia: contador modulo N tiene salida con periodo N
for N in (3, 5, 6, 10):
    q = 0; msb = []
    for t in range(4 * N): msb.append(int(q == N - 1)); q = (q + 1) % N
    per = [i for i in range(N, 2 * N) if msb[i] == 1][0] - [i for i in range(N) if msb[i] == 1][0]
    check(f'd.divN.{N}', per == N)
# binario sincrono T_i
def sync_inc(q, n):
    t = [int(all(((q >> j) & 1) for j in range(i))) for i in range(n)]
    return sum((((q >> i) & 1) ^ t[i]) << i for i in range(n))
check('d.contsync', all(sync_inc(q, 4) == (q + 1) % 16 for q in range(16)))
# memoria: chips
check('d.chips', (2 ** 14 // 2 ** 12) * (16 // 8) == 8 and 2 ** 14 * 16 // (2 ** 12 * 8) == 8)
# mux 2^k:1 implementa k+1 variables: f(A,B,C) con mux 4:1 (selecciones A,B) y datos {0,1,C,C'}
ok = True
for f in itertools.product(B, repeat=8):
    # para cada (a,b) el par (f(a,b,0), f(a,b,1)) es una de 4 funciones de C
    for a in B:
        for b in B:
            i = a * 2 + b; pair = (f[i * 2], f[i * 2 + 1])
            ok &= pair in {(0, 0), (1, 1), (0, 1), (1, 0)}
check('d.mux', ok)
json.dump({'R': R, 'CHK': CHK}, open('../out/results6.json', 'w'), indent=1, default=str, ensure_ascii=False)
print(len(CHK), 'checks;', sum(not c['ok'] for c in CHK), 'fallos')
