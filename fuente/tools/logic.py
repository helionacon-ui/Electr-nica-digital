"""Utilidades de lógica digital para verificar TODO resultado de la guía.
Sin dependencias externas (no hay sympy): Quine-McCluskey propio."""
from itertools import product, combinations

# ---------- Quine-McCluskey ----------
def _combine(a, b):
    (va, ma), (vb, mb) = a, b
    if ma != mb: return None
    d = va ^ vb
    if d and d & (d - 1) == 0:
        return (va & ~d, ma | d)
    return None

def prime_implicants(n, on, dc=()):
    terms = {(m, 0) for m in set(on) | set(dc)}
    primes = set()
    while terms:
        nxt, used = set(), set()
        tl = sorted(terms)
        for i in range(len(tl)):
            for j in range(i + 1, len(tl)):
                c = _combine(tl[i], tl[j])
                if c: nxt.add(c); used.add(tl[i]); used.add(tl[j])
        primes |= terms - used
        terms = nxt
    return primes

def _covers(imp, m):
    v, mask = imp
    return (m & ~mask) == (v & ~mask)

def minimize(n, on, dc=()):
    """Devuelve lista de implicantes (value, mask) de una SOP mínima (min nº de términos, luego de literales)."""
    on = sorted(set(on))
    if not on: return []
    primes = sorted(prime_implicants(n, on, dc))
    # esenciales
    chosen, left = set(), set(on)
    for m in on:
        cov = [p for p in primes if _covers(p, m)]
        if len(cov) == 1: chosen.add(cov[0])
    for p in chosen: left -= {m for m in on if _covers(p, m)}
    rest = [p for p in primes if p not in chosen]
    def lits(p): return n - bin(p[1]).count('1')
    best = None
    if left:
        for k in range(1, len(rest) + 1):
            sols = []
            for comb in combinations(rest, k):
                if all(any(_covers(p, m) for p in comb) for m in left):
                    sols.append(comb)
            if sols:
                best = min(sols, key=lambda c: sum(lits(p) for p in c)); break
    res = list(chosen) + (list(best) if best else [])
    return sorted(res)

def sop_str(n, imps, names, latex=True):
    if not imps: return '0'
    terms = []
    for v, mask in imps:
        lits = []
        for i in range(n):
            bit = n - 1 - i
            if mask >> bit & 1: continue
            name = names[i]
            if (v >> bit) & 1: lits.append(name)
            else: lits.append(('\\overline{%s}' % name) if latex else name + "'")
        terms.append(''.join(lits) if lits else '1')
    return ' + '.join(terms)

def pos_minimize(n, on, dc=()):
    """Producto de sumas mínimo: minimiza los ceros y complementa."""
    off = [m for m in range(2 ** n) if m not in set(on) and m not in set(dc)]
    return minimize(n, off, dc)

def pos_str(n, imps, names, latex=True):
    if not imps: return '1'
    out = []
    for v, mask in imps:
        lits = []
        for i in range(n):
            bit = n - 1 - i
            if mask >> bit & 1: continue
            name = names[i]
            # suma: variable aparece negada si en el implicante de ceros vale 1
            if (v >> bit) & 1: lits.append(('\\overline{%s}' % name) if latex else name + "'")
            else: lits.append(name)
        out.append('(' + ' + '.join(lits) + ')')
    return ''.join(out)

def eval_sop(imps, m):
    return int(any(_covers(p, m) for p in imps))

def bits(x, n):  # MSB primero
    return [(x >> (n - 1 - i)) & 1 for i in range(n)]

def from_bits(b):
    r = 0
    for x in b: r = (r << 1) | x
    return r

def c2(x, n):
    """valor con signo de x (n bits)."""
    return x - (1 << n) if x >> (n - 1) & 1 else x

def to_c2(v, n):
    return v & ((1 << n) - 1)

# ---------- flip-flops ----------
def ff_next(kind, q, a, b=None):
    if kind == 'T':  return q ^ a
    if kind == 'D':  return a
    if kind == 'JK':
        j, k = a, b
        return (j & (1 - q)) | ((1 - k) & q)
    raise ValueError(kind)

JK_EXC = {(0,0):(0,'x'), (0,1):(1,'x'), (1,0):('x',1), (1,1):('x',0)}  # (q,q+) -> (J,K)

def jk_excitation(q, qn):
    return {(0,0):(0,None),(0,1):(1,None),(1,0):(None,1),(1,1):(None,0)}[(q, qn)]

def bcd7seg(d):
    """segmentos a..g activos a 1 para dígito 0-9 (ánodo/cátodo común aparte)."""
    t = {0:'1111110',1:'0110000',2:'1101101',3:'1111001',4:'0110011',5:'1011011',
         6:'1011111',7:'1110000',8:'1111111',9:'1111011'}
    return t[d]
