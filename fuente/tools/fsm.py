"""Diseñador genérico de autómatas síncronos con JK / T / D + verificación a nivel de puerta."""
import itertools
from logic import *

class FSM:
    """states: lista de nombres. nin: nº de bits de entrada. step(state_name, x:int)->(next_name, out:int)
    Si moore=True, out(state) viene de out_moore(state)."""
    def __init__(self, states, nin, step, nout=1, moore=False, out_moore=None, enc=None, ff='JK',
                 in_names=None, dc_inputs=()):
        self.states = states; self.nin = nin; self.step = step; self.nout = nout
        self.moore = moore; self.out_moore = out_moore; self.ff = ff
        self.nq = max(1, (len(states) - 1).bit_length())
        self.enc = enc or {s: i for i, s in enumerate(states)}
        self.nq = max(self.nq, max(self.enc.values()).bit_length())
        self.in_names = in_names or (['E'] if nin == 1 else ['E%d' % i for i in range(nin - 1, -1, -1)])
        self.dc_inputs = set(dc_inputs)
        self.q_names = ['Q_%d' % i for i in range(self.nq - 1, -1, -1)]
        self.var_names = self.q_names + self.in_names
        self.nv = self.nq + nin
        self.solve()

    def idx(self, code, x): return (code << self.nin) | x

    def solve(self):
        nq, nin = self.nq, self.nin
        used = set(self.enc.values())
        self.tables = {}
        keys = []
        for b in range(nq - 1, -1, -1):
            if self.ff == 'JK': keys += ['J%d' % b, 'K%d' % b]
            elif self.ff == 'T': keys += ['T%d' % b]
            else: keys += ['D%d' % b]
        outk = ['S%d' % i for i in range(self.nout)] if not self.moore else []
        fn = {k: {'on': [], 'dc': []} for k in keys + outk}
        rows = []
        inv = {v: k for k, v in self.enc.items()}
        for code in range(2 ** nq):
            for x in range(2 ** nin):
                i = self.idx(code, x)
                if code not in used or x in self.dc_inputs:
                    for k in fn: fn[k]['dc'].append(i)
                    continue
                ns, out = self.step(inv[code], x)
                ncode = self.enc[ns]
                rows.append((inv[code], x, ns, out))
                for b in range(nq):
                    q = code >> b & 1; qn = ncode >> b & 1
                    if self.ff == 'JK':
                        j, k = jk_excitation(q, qn)
                        for name, v in (('J%d' % b, j), ('K%d' % b, k)):
                            if v == 1: fn[name]['on'].append(i)
                            elif v is None: fn[name]['dc'].append(i)
                    elif self.ff == 'T':
                        if q ^ qn: fn['T%d' % b]['on'].append(i)
                    else:
                        if qn: fn['D%d' % b]['on'].append(i)
                if not self.moore:
                    for o in range(self.nout):
                        if out >> o & 1: fn['S%d' % o]['on'].append(i)
        self.rows = rows
        self.imps = {k: minimize(self.nv, d['on'], d['dc']) for k, d in fn.items()}
        self.eq = {k: sop_str(self.nv, v, self.var_names) for k, v in self.imps.items()}
        if self.moore:
            self.omoore = {}
            for o in range(self.nout):
                on = [self.enc[s] for s in self.states if self.out_moore(s) >> o & 1]
                dc = [c for c in range(2 ** nq) if c not in used]
                imp = minimize(nq, on, dc)
                self.omoore['S%d' % o] = imp
                self.eq['S%d' % o] = sop_str(nq, imp, self.q_names)

    # --- simulación a nivel de puerta
    def gate_step(self, code, x):
        i = self.idx(code, x); nc = 0
        for b in range(self.nq):
            q = code >> b & 1
            if self.ff == 'JK': n = ff_next('JK', q, eval_sop(self.imps['J%d' % b], i), eval_sop(self.imps['K%d' % b], i))
            elif self.ff == 'T': n = q ^ eval_sop(self.imps['T%d' % b], i)
            else: n = eval_sop(self.imps['D%d' % b], i)
            nc |= n << b
        if self.moore:
            out = 0
            for o in range(self.nout): out |= eval_sop(self.omoore['S%d' % o], code) << o
        else:
            out = 0
            for o in range(self.nout): out |= eval_sop(self.imps['S%d' % o], i) << o
        return nc, out

    def verify_table(self):
        inv = {v: k for k, v in self.enc.items()}
        for (s, x, ns, out) in self.rows:
            nc, o = self.gate_step(self.enc[s], x)
            exp_o = self.out_moore(s) if self.moore else out
            if nc != self.enc[ns] or o != exp_o: return False
        return True

    def moore_out(self, code):
        o = 0
        for k in range(self.nout): o |= eval_sop(self.omoore['S%d' % k], code) << k
        return o

    def run(self, inputs, start=None):
        """Mealy: salida durante cada transición. Moore: salida del estado alcanzado tras el flanco."""
        code = self.enc[start or self.states[0]]; outs = []
        for x in inputs:
            nc, o = self.gate_step(code, x)
            outs.append(self.moore_out(nc) if self.moore else o)
            code = nc
        return outs
