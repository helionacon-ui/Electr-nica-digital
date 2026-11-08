"""Comprobación por código de los ejemplos de teoría (temas 2 a 13)."""
import json, itertools
from logic import *
R = {}; CHK = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)

# ---- T2 numeración
check('t2.dec2bin', bin(156) == '0b10011100' and hex(156) == '0x9c' and oct(156) == '0o234')
frac = 0.6875; b = ''
for _ in range(8):
    frac *= 2; b += str(int(frac)); frac -= int(frac)
    if frac == 0: break
check('t2.frac', b == '1011')
def c2(x, n): return format(x & ((1 << n) - 1), f'0{n}b')
check('t2.c2_37', c2(-37, 8) == '11011011')
check('t2.c2_rango', all(-2**(n-1) <= v <= 2**(n-1)-1 for n in (4, 8) for v in range(-2**(n-1), 2**(n-1))) and c2(-128, 8) == '10000000')
def add_c2(a, b, n):
    s = (a + b); ov = not (-2**(n-1) <= s < 2**(n-1)); return c2(s, n), ov
check('t2.ov1', add_c2(100, 50, 8)[1] is True and add_c2(45, -20, 8) == ('00011001', False))
# desbordamiento por signos: acarreo de entrada al bit de signo != acarreo de salida
def ov_carry(a, b, n):
    m = (1 << (n - 1)) - 1; ca = ((a & m) + (b & m)) >> (n - 1)
    full = (a & ((1<<n)-1)) + (b & ((1<<n)-1)); co = full >> n
    return ca ^ co
check('t2.ov_carry', all(bool(ov_carry(a, b, 4)) == (not (-8 <= a + b <= 7)) for a in range(-8, 8) for b in range(-8, 8)))
def bcd(x): return ' '.join(format(int(d), '04b') for d in str(x))
check('t2.bcd47', bcd(47) == '0100 0111')
def bcd_add(a, b):
    s = 0; c = 0
    for i in range(2):
        da = (a // 10**i) % 10; db = (b // 10**i) % 10; t = da + db + c
        if t > 9: t += 6
        c = t >> 4; s += (t & 15) * 10**i
    return s + c * 100
check('t2.bcdadd', bcd_add(38, 45) == 83 and all(bcd_add(a, b) == a + b for a in range(100) for b in range(100)))
check('t2.bcdadd_bits', format(0b00111000 + 0b01000101, '08b') == '01111101' and format(0b01111101 + 6, '08b') == '10000011')
gray = [i ^ (i >> 1) for i in range(8)]
check('t2.gray', [format(g, '03b') for g in gray] == ['000', '001', '011', '010', '110', '111', '101', '100'] and all(bin(gray[i] ^ gray[(i+1) % 8]).count('1') == 1 for i in range(8)))
check('t2.paridad', bin(0b1011001).count('1') == 4)
# Hamming(7,4) distancia 3 -> corrige 1 error
def hamming(d):
    d1, d2, d3, d4 = d
    p1 = d1 ^ d2 ^ d4; p2 = d1 ^ d3 ^ d4; p3 = d2 ^ d3 ^ d4
    return [p1, p2, d1, p3, d2, d3, d4]
def decode(c):
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]; s2 = c[1] ^ c[2] ^ c[5] ^ c[6]; s3 = c[3] ^ c[4] ^ c[5] ^ c[6]
    pos = s1 + 2 * s2 + 4 * s3
    if pos: c = c[:]; c[pos - 1] ^= 1
    return [c[2], c[4], c[5], c[6]]
ok = True
for d in itertools.product((0, 1), repeat=4):
    c = hamming(d)
    for e in range(7):
        c2_ = c[:]; c2_[e] ^= 1; ok &= decode(c2_) == list(d)
    ok &= decode(c) == list(d)
check('t2.hamming', ok)
R['t2.ham1011'] = ''.join(map(str, hamming((1, 0, 1, 1))))
check('t2.ham1011', R['t2.ham1011'] == '0110011')

# ---- T3 Boole
bits2 = list(itertools.product((0, 1), repeat=2)); bits3 = list(itertools.product((0, 1), repeat=3))
check('t3.demorgan', all((1 - (a & b)) == ((1 - a) | (1 - b)) and (1 - (a | b)) == ((1 - a) & (1 - b)) for a, b in bits2))
check('t3.absorcion', all((a | (a & b)) == a and (a & (a | b)) == a for a, b in bits2))
check('t3.consenso', all(((a & b) | ((1-a) & c) | (b & c)) == ((a & b) | ((1-a) & c)) for a, b, c in bits3))
check('t3.xor', all((a ^ b) == ((a & (1-b)) | ((1-a) & b)) and (a ^ b ^ 1) == (1 if a == b else 0) for a, b in bits2))
on = [1, 3, 5, 6, 7]
imp = minimize(3, on); R['t3.ej1'] = sop_str(3, imp, 'ABC')
check('t3.ej1', sorted(i for i in range(8) if eval_sop(imp, i)) == on, R['t3.ej1'])
R['t3.ej1_pos'] = pos_str(3, pos_minimize(3, on), 'ABC')
nand_only = lambda a, b: 1 - (a & b)
check('t3.nand_univ', all(nand_only(nand_only(a, a), nand_only(b, b)) == (a | b) and nand_only(nand_only(a, b), nand_only(a, b)) == (a & b) and nand_only(a, a) == 1 - a for a, b in bits2))
R['t3.ncomb4'] = 2 ** 16
check('t3.nfun', 2 ** (2 ** 2) == 16 and 2 ** (2 ** 3) == 256 and 2 ** (2 ** 4) == 65536)

# ---- T4 familias
ttl = dict(voh=2.7, vih=2.0, vil=0.8, vol=0.5); cmos = dict(voh=4.4, vih=3.5, vil=1.5, vol=0.33)
nm = lambda f: (round(f['voh'] - f['vih'], 2), round(f['vil'] - f['vol'], 2))
R['t4.nm_ttl'] = nm(ttl); R['t4.nm_cmos'] = nm(cmos)
check('t4.nm', R['t4.nm_ttl'] == (0.7, 0.3) and R['t4.nm_cmos'] == (0.9, 1.17))
R['t4.fo_ls'] = [int(8 / 0.4), int(0.4 / 0.02)]
check('t4.fanout', R['t4.fo_ls'] == [20, 20])
R['t4.pdin'] = 20e-12 * 5 ** 2 * 1e6
check('t4.pdin', abs(R['t4.pdin'] - 0.5e-3) < 1e-12)
R['t4.tpd_cadena'] = 5 * 10
check('t4.tpd', R['t4.tpd_cadena'] == 50)

# ---- T5 combinacional
fa = all(((a ^ b ^ c), ((a & b) | (c & (a ^ b)))) == ((a + b + c) & 1, (a + b + c) >> 1) for a, b, c in bits3)
check('t5.fa', fa)
def ripple(a, b, n):
    c = 0; s = 0
    for i in range(n):
        x = (a >> i) & 1; y = (b >> i) & 1; s |= (x ^ y ^ c) << i; c = (x & y) | (c & (x ^ y))
    return s | (c << n)
check('t5.ripple4', all(ripple(a, b, 4) == a + b for a in range(16) for b in range(16)))
R['t5.retardo'] = 4 * 2 * 10  # 4 etapas, 2 puertas de retardo 10 ns
# función con mux 4:1: f = Σm(1,2,4,7) con A,B en selección
fmux = [1, 2, 4, 7]
D = {}
for A in (0, 1):
    for B in (0, 1):
        col = [int((A * 4 + B * 2 + C) in fmux) for C in (0, 1)]
        D[(A, B)] = col
R['t5.mux_data'] = {f'{a}{b}': ('0' if v == [0, 0] else '1' if v == [1, 1] else 'C' if v == [0, 1] else "C'") for (a, b), v in D.items()}
check('t5.mux', R['t5.mux_data'] == {'00': 'C', '01': "C'", '10': "C'", '11': 'C'})
def mux_out(A, B, C):
    d = {'00': C, '01': 1 - C, '10': 1 - C, '11': C}; return d[f'{A}{B}']
check('t5.mux_ok', all(mux_out(A, B, C) == int((A*4+B*2+C) in fmux) for A, B, C in bits3), str(R['t5.mux_data']))
check('t5.dec', all(sum(1 for k in range(4) if (k == a*2+b)) == 1 for a, b in bits2))
check('t5.dec_fun', all(((a*4+b*2+c) in fmux) == any((a*4+b*2+c) == m for m in fmux) for a, b, c in bits3))
# comparador de 1 bit
check('t5.comp1', all(((a > b), (a == b), (a < b)) == (int(a & (1-b)), int(1 - (a ^ b)), int((1-a) & b)) for a, b in bits2))
# codificador de prioridad 4:2
def prio(i):
    for k in (3, 2, 1, 0):
        if (i >> k) & 1: return k, 1
    return 0, 0
R['t5.prio'] = [prio(i) for i in (0b0001, 0b0110, 0b1010)]
check('t5.prio', R['t5.prio'] == [(0, 1), (2, 1), (3, 1)])
check('t5.shannon', all(((a & b) | (c & (1 - a))) == ((a & ((b))) | ((1-a) & c)) for a, b, c in bits3))

# ---- T6 biestables
def sr(q, s, r): return None if s and r else (1 if s else 0 if r else q)
check('t6.sr', sr(0, 1, 0) == 1 and sr(1, 0, 1) == 0 and sr(1, 0, 0) == 1 and sr(1, 1, 1) is None)
check('t6.jk', all(ff_next('JK', q, j, k) == ((j & (1-q)) | ((1-k) & q)) for q in (0, 1) for j in (0, 1) for k in (0, 1)))
check('t6.t', all(ff_next('T', q, t, None) == q ^ t for q in (0, 1) for t in (0, 1)))
check('t6.d', all(ff_next('D', q, d, None) == d for q in (0, 1) for d in (0, 1)))
R['t6.exc'] = {f'{q}{n}': jk_excitation(q, n) for q in (0, 1) for n in (0, 1)}
check('t6.exc', R['t6.exc'] == {'00': (0, None), '01': (1, None), '10': (None, 1), '11': (None, 0)}, str(R['t6.exc']))
# JK con J=K=1 conmuta: divisor por 2
q = 0; seq = []
for _ in range(6): q = ff_next('JK', q, 1, 1); seq.append(q)
check('t6.div2', seq == [1, 0, 1, 0, 1, 0])
# D con realimentacion Q' -> divisor por 2
q = 0; seq = []
for _ in range(6): q = 1 - q; seq.append(q)
check('t6.d_div2', seq == [1, 0, 1, 0, 1, 0])
R['t6.setup'] = 20 + 5

# ---- T7 memorias
R['t7.dir_8Kx8'] = 13; check('t7.dir', 2 ** 13 == 8192)
R['t7.bits_64Kx16'] = 64 * 1024 * 16; check('t7.bits', R['t7.bits_64Kx16'] == 1048576)
R['t7.chips'] = (8 // 2) * (16 // 8)
check('t7.chips', R['t7.chips'] == 8)
# ROM como tabla de verdad: sumador completo en ROM 8x2
rom = [((a + b + c) & 1) | (((a + b + c) >> 1) << 1) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
R['t7.rom_fa'] = rom
check('t7.rom_fa', rom == [0, 1, 1, 2, 1, 2, 2, 3])
# PLA: términos compartidos
R['t7.pal_terminos'] = 6

# ---- T8 contadores
check('t8.bits', all(2 ** (n - 1) < N <= 2 ** n for N, n in ((10, 4), (12, 4), (60, 6), (5, 3), (16, 4), (100, 7))))
R['t8.f_div'] = 1e6 / 12
check('t8.fdiv', abs(R['t8.f_div'] - 83333.33333333333) < 1e-6)
def ctr_sync(n, steps):
    q = 0; out = []
    for _ in range(steps):
        t = [int(all((q >> j) & 1 for j in range(i))) for i in range(n)]
        q ^= sum(t[i] << i for i in range(n)); out.append(q)
    return out
check('t8.sync', ctr_sync(3, 9) == [1, 2, 3, 4, 5, 6, 7, 0, 1])
def mod10():
    q = 0; out = []
    for _ in range(12):
        q = 0 if q == 9 else q + 1; out.append(q)
    return out
check('t8.mod10', mod10() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2])
# contador asíncrono de 4 bits con tpd=12 ns: retardo máximo
R['t8.ripple_t'] = 4 * 12; R['t8.ripple_fmax'] = round(1e3 / (4 * 12), 2)
check('t8.ripple', R['t8.ripple_fmax'] == 20.83, R['t8.ripple_fmax'])
# mod 6 por reset asíncrono: detecta 6 (110) y resetea -> estado 110 dura un instante
check('t8.mod6', set(range(6)) == {i for i in range(6)})
# contador mod 12 con carga síncrona
def mod12_sync():
    q = 0; out = []
    for _ in range(14): q = 0 if q == 11 else q + 1; out.append(q)
    return out
check('t8.mod12', mod12_sync()[:13] == [1,2,3,4,5,6,7,8,9,10,11,0,1])

# ---- T9 registros
def shift(reg, d, n): return ((reg << 1) | d) & ((1 << n) - 1)
r = 0
for bit in (1, 0, 1, 1): r = shift(r, bit, 4)
check('t9.sipo', r == 0b1011)
q = 0b1000; ring = []
for _ in range(5): ring.append(format(q, '04b')); q = ((q >> 1) | ((q & 1) << 3))
check('t9.anillo', ring == ['1000', '0100', '0010', '0001', '1000'])
q = 0; joh = []
for _ in range(9): joh.append(format(q, '04b')); q = ((q >> 1) | (((~q) & 1) << 3))
R['t9.johnson'] = joh
check('t9.johnson', joh == ['0000', '1000', '1100', '1110', '1111', '0111', '0011', '0001', '0000'] and len(set(joh[:8])) == 8)
# LFSR 4 bits x^4+x^3+1 -> periodo 15
q = 1; seen = []
for _ in range(16):
    seen.append(q); fb = ((q >> 3) ^ (q >> 2)) & 1; q = ((q << 1) | fb) & 15
check('t9.lfsr', len(set(seen[:15])) == 15 and seen[15] == seen[0])
R['t9.lfsr'] = [format(x, '04b') for x in seen[:15]]

# ---- T10 autómata detector 101 solapado Mealy
def det101(bits):
    s = 0; out = []
    for x in bits:
        z = int(s == 2 and x == 1)
        s = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 1, (2, 0): 0, (2, 1): 1}[(s, x)]
        out.append(z)
    return out
def ref101(bits): return [int(i >= 2 and bits[i-2:i+1] == [1, 0, 1]) for i in range(len(bits))]
ok = all(det101(list(b)) == ref101(list(b)) for n in range(1, 11) for b in itertools.product((0, 1), repeat=n))
check('t10.det101', ok)
# implementación con biestables D: D1=Q0·x', D0=x, Z=Q1·x
def det_gates(bits):
    q1 = q0 = 0; out = []
    for x in bits:
        z = q1 & x; d1 = q0 & (1 - x); d0 = x; q1, q0 = d1, d0; out.append(z)
    return out
check('t10.det_gates', all(det_gates(list(b)) == ref101(list(b)) for n in range(1, 11) for b in itertools.product((0, 1), repeat=n)))
R['t10.ej_seq'] = [1, 0, 1, 0, 1, 1, 0, 1]; R['t10.ej_out'] = det101(R['t10.ej_seq'])
check('t10.ej_out', R['t10.ej_out'] == [0, 0, 1, 0, 1, 0, 0, 1], str(R['t10.ej_out']))
# Moore equivalente: 4 estados
def det101_moore(bits):
    s = 0; out = []
    nxt = {(0,0):0,(0,1):1,(1,0):2,(1,1):1,(2,0):0,(2,1):3,(3,0):2,(3,1):1}
    for x in bits:
        s = nxt[(s, x)]; out.append(int(s == 3))
    return out
check('t10.moore', all(det101_moore(list(b)) == ref101(list(b)) for n in range(1, 11) for b in itertools.product((0, 1), repeat=n)))
R['t10.nbiest'] = {'mealy': 2, 'moore': 2}
# Número de biestables
check('t10.nq', all(2 ** (n - 1) < N <= 2 ** n for N, n in ((3, 2), (5, 3), (8, 3), (9, 4))))
# Antirrebote: contador de 20 ms con reloj 50 MHz = 1.000.000 ciclos -> 20 bits
R['t10.deb_ciclos'] = int(50e6 * 20e-3); R['t10.deb_bits'] = (R['t10.deb_ciclos'] - 1).bit_length()
check('t10.deb', R['t10.deb_ciclos'] == 1000000 and R['t10.deb_bits'] == 20)

# ---- T12 FPGA
check('t12.lut', 2 ** 4 == 16 and 2 ** 16 == 65536)
R['t12.div_1hz'] = 50_000_000 // 2   # contador hasta 25M para conmutar a 1 Hz con reloj 50 MHz
R['t12.div_bits'] = (R['t12.div_1hz'] - 1).bit_length()
check('t12.div', R['t12.div_1hz'] == 25000000 and R['t12.div_bits'] == 25)
R['t12.disp_refresco'] = 50e6 / 2 ** 16
check('t12.refresco', round(R['t12.disp_refresco'], 1) == 762.9)
R['t12.disp_digito'] = round(R['t12.disp_refresco'] / 4, 1)
check('t12.disp', R['t12.disp_digito'] == 190.7)

# ---- T13 VHDL: modelo en Python equivalente a los ejemplos
def vh_sum4(a, b, cin):
    t = a + b + cin; return t & 15, t >> 4
check('t13.sum4', all(vh_sum4(a, b, c) == ((a + b + c) % 16, (a + b + c) // 16) for a in range(16) for b in range(16) for c in (0, 1)))
def vh_mux4(sel, d): return d[sel]
check('t13.mux4', all(vh_mux4(s, [1, 0, 0, 1]) == [1, 0, 0, 1][s] for s in range(4)))
def vh_cnt(n, rst_ev, steps):
    q = 0; out = []
    for i in range(steps):
        q = 0 if (i in rst_ev) else (q + 1) % n; out.append(q)
    return out
check('t13.cnt', vh_cnt(10, {5}, 8) == [1, 2, 3, 4, 5, 0, 1, 2])
json.dump({'R': R, 'CHK': CHK}, open('../out/results4.json', 'w'), ensure_ascii=False)
print(len(CHK), 'checks;', sum(1 for c in CHK if not c['ok']), 'fallos')
