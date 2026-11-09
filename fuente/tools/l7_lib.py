# -*- coding: utf-8 -*-
"""Modelos para el capítulo 7 (registros y contadores): contador síncrono tipo 74160/74163,
cadena de biestables asíncronos con flancos, y utilidades para dibujar cronogramas por ranuras."""

class Cnt:
    """74160 (mod 10, BCD) o 74163 (mod 16, binario). Borrado asíncrono, carga síncrona, ENP·ENT habilitan."""
    def __init__(s, mod=10, q=0):
        s.mod = mod; s.q = q
    def rco(s, ent=1):
        return int(bool(ent) and s.q == s.mod - 1)
    def clk(s, clear=1, load=1, en=1, d=0):
        """Un flanco de subida con las entradas dadas (se toman antes del flanco)."""
        if not clear: s.q = 0
        elif not load: s.q = d
        elif en: s.q = (s.q + 1) % s.mod

def edge_slots(ck, e):
    return [k for k in range(1, len(ck)) if (e == 'r' and ck[k-1] == '0' and ck[k] == '1') or (e == 'f' and ck[k-1] == '1' and ck[k] == '0')]

def ckstr(n, lead=4, half=4):
    """Reloj con 'lead' ranuras iniciales a 0 y luego n pulsos de 2*half ranuras (subida al principio)."""
    return '0' * lead + ('1' * half + '0' * half) * n

def ripple(ffs, ck, init, force=None):
    """Cadena de biestables con relojes propios. ffs: lista de (clk, d).
    clk = ('ck','r'|'f')  -> flanco del reloj externo;  clk = ('q', i, 'r'|'f') -> flanco de la salida del biestable i.
    d(q) -> nuevo valor del biestable cuando llega su flanco (q: lista de valores actuales).
    force(q) -> None, o el estado al que se obliga (puesta a 0 / a 1 asíncrona) en cuanto se cumple la condición.
    Devuelve (lista de estados por ranura, lista de estados transitorios 'glitch')."""
    q = list(init); seq = []; glitches = []
    for k in range(len(ck)):
        if k > 0:
            e = 'r' if (ck[k-1] == '0' and ck[k] == '1') else ('f' if (ck[k-1] == '1' and ck[k] == '0') else None)
            if e:
                ev = [('ck', e)]
                while ev:
                    sig = ev.pop(0)
                    for i, (clk, d) in enumerate(ffs):
                        hit = (clk[0] == 'ck' and sig[0] == 'ck' and clk[1] == sig[1]) or \
                              (clk[0] == 'q' and sig[0] == 'q' and clk[1] == sig[1] and clk[2] == sig[2])
                        if not hit: continue
                        nv = d(q)
                        if nv != q[i]:
                            q[i] = nv; ev.append(('q', i, 'r' if nv else 'f'))
                            if force:
                                f = force(q)
                                if f is not None:
                                    glitches.append(tuple(q)); q[:] = f; ev = []; break
        seq.append(tuple(q))
    return seq, glitches

def bits(seq, i):
    return ''.join(str(s[i]) for s in seq)

def val(s, w=None):
    """Valor entero de una tupla (q0, q1, ...) con q0 = bit de menor peso."""
    return sum(b << i for i, b in enumerate(s))
