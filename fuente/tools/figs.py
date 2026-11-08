"""Figuras SVG propias (sin librerías). Usan clases CSS para tema claro/oscuro."""
import math, html
from logic import minimize, sop_str, bits, eval_sop

def esc(s): return html.escape(str(s), quote=False)

def svg(w, h, body, label='', cls='fig'):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')

DEFS = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')

def text(x, y, s, cls='t', anchor='middle', size=None):
    st = f' font-size="{size}"' if size else ''
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{st}>{esc(s)}</text>'

def line(x1, y1, x2, y2, cls='s', arrow=False):
    m = ' marker-end="url(#arr)"' if arrow else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{m}/>'

# --------------------------------------------------------------------- puertas
def gate_shape(kind, x, y, w=60, h=40):
    k = kind.upper(); b = ''
    inv = k in ('NAND', 'NOR', 'XNOR', 'NOT')
    if k in ('AND', 'NAND'):
        b = f'<path d="M{x} {y}h{w*0.5}a{h/2} {h/2} 0 0 1 0 {h}h-{w*0.5}z" class="s f"/>'
        ox = x + w * 0.5 + h / 2
    elif k in ('OR', 'NOR', 'XOR', 'XNOR'):
        b = (f'<path d="M{x} {y}Q{x+w*0.55} {y} {x+w} {y+h/2}Q{x+w*0.55} {y+h} {x} {y+h}Q{x+w*0.25} {y+h/2} {x} {y}z" class="s f"/>')
        if k in ('XOR', 'XNOR'):
            b += f'<path d="M{x-7} {y}Q{x+w*0.25-7} {y+h/2} {x-7} {y+h}" class="s"/>'
        ox = x + w
    elif k in ('NOT', 'BUF'):
        b = f'<path d="M{x} {y}L{x+w*0.65} {y+h/2}L{x} {y+h}z" class="s f"/>'
        ox = x + w * 0.65
    else: raise ValueError(kind)
    if inv:
        b += f'<circle cx="{ox+4}" cy="{y+h/2}" r="4" class="s f"/>'; ox += 8
    return b, ox

def fig_gates():
    kinds = ['NOT', 'AND', 'NAND', 'OR', 'NOR', 'XOR', 'XNOR']
    tts = {'NOT': ['A', 'Y', '01', '10'], 'AND': 'A·B', 'NAND': 'A·B', 'OR': 'A+B', 'NOR': 'A+B', 'XOR': 'A⊕B', 'XNOR': 'A⊕B'}
    body = DEFS; W = 170; H = 110
    for i, k in enumerate(kinds):
        cx = (i % 4) * W + 12; cy = (i // 4) * H + 14
        shp, ox = gate_shape(k, cx + 20, cy + 10, 50, 36)
        body += shp
        ins = [(cx + 20, cy + 10 + 12), (cx + 20, cy + 10 + 24)] if k != 'NOT' else [(cx + 20, cy + 28)]
        for (ax, ay) in ins: body += line(cx + 4, ay, ax, ay)
        body += line(ox, cy + 28, ox + 14, cy + 28)
        body += text(cx + 20 + 25, cy + 68, k, 't b')
        lab = {'NOT': 'Ā', 'AND': 'A·B', 'NAND': 'A·B̄'.replace('B̄', 'B') , 'OR': 'A+B', 'NOR': 'A+B', 'XOR': 'A⊕B', 'XNOR': 'A⊕B'}[k]
        if k in ('NAND', 'NOR', 'XNOR'): lab = '¬(' + lab + ')'
        if k == 'NOT': lab = '¬A'
        body += text(cx + 20 + 25, cy + 86, lab, 't m')
    return svg(4 * W, 2 * H, body, 'Símbolos de puertas lógicas')

# --------------------------------------------------------------------- Karnaugh
GRAY2 = [0, 1]; GRAY4 = [0, 1, 3, 2]
def fig_kmap(n, on, dc, names, imps=None, title=''):
    """Mapa de Karnaugh para 2, 3 o 4 variables. names = lista de nombres de variable (texto plano)."""
    if n == 2: rv, cv = 1, 1; rg, cg = GRAY2, GRAY2
    elif n == 3: rv, cv = 1, 2; rg, cg = GRAY2, GRAY4
    elif n == 4: rv, cv = 2, 2; rg, cg = GRAY4, GRAY4
    else: raise ValueError('solo 2..4 variables')
    nr, nc = len(rg), len(cg)
    cs = 44; ox, oy = 78, 46
    W = ox + nc * cs + 20; H = oy + nr * cs + 24
    body = ''
    # variables de fila (primeras rv) y de columna (resto)
    rn = names[:rv]; cn = names[rv:]
    body += text(ox - 38, oy - 28, ''.join(rn) + '\\' + ''.join(cn), 't m', 'middle', 11)
    for c, g in enumerate(cg):
        body += text(ox + c * cs + cs / 2, oy - 8, format(g, '0%db' % cv), 't m')
    for r, g in enumerate(rg):
        body += text(ox - 8, oy + r * cs + cs / 2 + 4, format(g, '0%db' % rv), 't m', 'end')
    colors = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8']
    # grupos
    if imps:
        for gi, (v, mask) in enumerate(imps):
            cells = [(r, c) for r in range(nr) for c in range(nc)
                     if ((v & ~mask) == (((rg[r] << cv) | cg[c]) & ~mask))]
            rows = sorted({r for r, _ in cells}); cols = sorted({c for _, c in cells})
            def runs(idx, size):
                if len(idx) == size: return [(0, size - 1)]
                out = []; start = prev = idx[0]
                for i in idx[1:]:
                    if i == prev + 1: prev = i
                    else: out.append((start, prev)); start = prev = i
                out.append((start, prev))
                if len(out) == 2 and out[0][0] == 0 and out[1][1] == size - 1:  # envuelve
                    return [(out[1][0], size - 1), (0, out[0][1])]
                return out
            for (r0, r1) in runs(rows, nr):
                for (c0, c1) in runs(cols, nc):
                    pad = 3 + (gi % 3) * 2
                    x = ox + c0 * cs + pad; y = oy + r0 * cs + pad
                    w = (c1 - c0 + 1) * cs - 2 * pad; h = (r1 - r0 + 1) * cs - 2 * pad
                    body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" class="grp {colors[gi % 8]}"/>'
    for r in range(nr):
        for c in range(nc):
            m = (rg[r] << cv) | cg[c]
            body += f'<rect x="{ox + c * cs}" y="{oy + r * cs}" width="{cs}" height="{cs}" class="cell"/>'
            if m in on: body += text(ox + c * cs + cs / 2, oy + r * cs + cs / 2 + 6, '1', 't b', 'middle', 17)
            elif m in dc: body += text(ox + c * cs + cs / 2, oy + r * cs + cs / 2 + 6, '×', 't d', 'middle', 17)
            body += text(ox + c * cs + 4, oy + r * cs + 11, str(m), 't tiny', 'start')
    if title: body += text(W / 2, H - 4, title, 't m')
    return svg(W, H, body, 'Mapa de Karnaugh ' + title, 'fig kmap')

# --------------------------------------------------------------------- cronograma
def fig_timing(signals, slots=None, labels=None, title='', labels_top=None, w_slot=44):
    """signals: lista de (nombre, [0/1,...]) ; 'CLK' se dibuja como reloj si valores = None."""
    n = slots or max(len(v) for _, v in signals if v)
    ox, oy, rh = 70, 30, 46
    W = ox + n * w_slot + 14; H = oy + len(signals) * rh + 22
    body = ''
    for i in range(n + 1):
        body += line(ox + i * w_slot, oy - 6, ox + i * w_slot, H - 14, 'grid')
    if labels_top:
        for i, s in enumerate(labels_top): body += text(ox + i * w_slot + w_slot / 2, oy - 12, s, 't tiny')
    for k, (name, vals) in enumerate(signals):
        y0 = oy + k * rh + rh - 12; y1 = oy + k * rh + 10
        body += text(ox - 8, (y0 + y1) / 2 + 4, name, 't m', 'end')
        if vals is None:   # reloj
            d = ''
            for i in range(n):
                x = ox + i * w_slot
                d += f'M{x} {y0}V{y1}H{x + w_slot/2}V{y0}H{x + w_slot}'
            body += f'<path d="{d}" class="wave"/>'
            continue
        d = ''; prev = None
        for i, v in enumerate(vals):
            x = ox + i * w_slot; y = y1 if v else y0
            if prev is None: d += f'M{x} {y}'
            elif prev != v: d += f'V{y}'
            d += f'H{x + w_slot}'
            prev = v
        body += f'<path d="{d}" class="wave a"/>'
    if title: body += text(W / 2, H - 4, title, 't m')
    return svg(W, H, body, 'Cronograma ' + title, 'fig timing')

# --------------------------------------------------------------------- diagrama de estados
def fig_fsm(nodes, edges, W=560, H=300, title='', r=24):
    """nodes: {nombre: (x, y, subtitulo)} ; edges: lista de (a, b, etiqueta, curvatura)"""
    body = DEFS
    for a, b, lab, cur in edges:
        xa, ya = nodes[a][:2]; xb, yb = nodes[b][:2]
        if a == b:
            dx = cur if isinstance(cur, (int, float)) and cur else -1
            body += (f'<path d="M{xa-10} {ya-r+3}C{xa-34} {ya-r-40} {xa+34} {ya-r-40} {xa+10} {ya-r+3}" class="s nf" marker-end="url(#arr)"/>')
            body += text(xa, ya - r - 30, lab, 't tiny')
            continue
        dx, dy = xb - xa, yb - ya; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        sx, sy = xa + ux * r, ya + uy * r; ex, ey = xb - ux * (r + 5), yb - uy * (r + 5)
        cx, cy = (xa + xb) / 2 + nx * cur, (ya + yb) / 2 + ny * cur
        if cur:
            sx, sy = xa + (cx - xa) / math.hypot(cx - xa, cy - ya) * r, ya + (cy - ya) / math.hypot(cx - xa, cy - ya) * r
            ex, ey = xb + (cx - xb) / math.hypot(cx - xb, cy - yb) * (r + 5), yb + (cy - yb) / math.hypot(cx - xb, cy - yb) * (r + 5)
        body += f'<path d="M{sx:.1f} {sy:.1f}Q{cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f}" class="s nf" marker-end="url(#arr)"/>'
        lx, ly = (sx + 2 * cx + ex) / 4, (sy + 2 * cy + ey) / 4
        body += f'<text x="{lx:.1f}" y="{ly - 4:.1f}" class="t tiny halo" text-anchor="middle">{esc(lab)}</text>'
    for name, (x, y, sub) in nodes.items():
        body += f'<circle cx="{x}" cy="{y}" r="{r}" class="s node"/>'
        body += text(x, y + (1 if sub else 5), name, 't b', 'middle', 13)
        if sub: body += text(x, y + 14, sub, 't tiny')
    if title: body += text(W / 2, H - 6, title, 't m')
    return svg(W, H, body, 'Diagrama de estados ' + title, 'fig fsm')

# --------------------------------------------------------------------- diagrama de bloques
def fig_blocks(blocks, arrows, W=560, H=240, title=''):
    """blocks: {id: (x, y, w, h, texto)} ; arrows: [(x1,y1,x2,y2,etiqueta)]"""
    body = DEFS
    for bid, (x, y, w, h, t) in blocks.items():
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" class="s blk"/>'
        lines = t.split('\n')
        for i, ln in enumerate(lines):
            body += text(x + w / 2, y + h / 2 + 4 + (i - (len(lines) - 1) / 2) * 15, ln, 't b' if i == 0 else 't m', 'middle', 12)
    for (x1, y1, x2, y2, lab) in arrows:
        body += line(x1, y1, x2, y2, 's', True)
        if lab: body += text((x1 + x2) / 2, (y1 + y2) / 2 - 5, lab, 't tiny halo')
    if title: body += text(W / 2, H - 6, title, 't m')
    return svg(W, H, body, 'Diagrama de bloques ' + title, 'fig blocks')

# --------------------------------------------------------------------- familias lógicas: márgenes de ruido
def fig_noise(voh, vih, vil, vol, vcc, title='', cmos=False):
    W, H = 420, 270; ox = 60; sc = 190 / vcc
    def Y(v): return 20 + (vcc - v) * sc
    body = DEFS
    body += text(ox + 70, 14, 'Salida', 't b'); body += text(ox + 260, 14, 'Entrada', 't b')
    for xo, hi, lo, name in ((ox, voh, vol, 'out'), (ox + 190, vih, vil, 'in')):
        body += f'<rect x="{xo}" y="{Y(vcc)}" width="90" height="{Y(hi)-Y(vcc) if False else Y(hi)-Y(vcc)}" class="zone1"/>'
        body += f'<rect x="{xo}" y="{Y(hi)}" width="90" height="{Y(lo)-Y(hi)}" class="zoneX"/>'
        body += f'<rect x="{xo}" y="{Y(lo)}" width="90" height="{Y(0)-Y(lo)}" class="zone0"/>'
        body += text(xo + 45, (Y(vcc) + Y(hi)) / 2 + 4, "'1'", 't b'); body += text(xo + 45, (Y(lo) + Y(0)) / 2 + 4, "'0'", 't b')
        body += text(xo + 45, (Y(hi) + Y(lo)) / 2 + 4, 'no permitido', 't tiny')
    for v, lab, xo in ((voh, 'V_OH min', ox), (vol, 'V_OL max', ox), (vih, 'V_IH min', ox + 190), (vil, 'V_IL max', ox + 190)):
        body += line(xo - (4 if xo == ox else 0), Y(v), xo + 90, Y(v), 'dash')
        body += text(xo - 6 if xo == ox else xo + 96, Y(v) + 4, f'{v:g} V', 't tiny', 'end' if xo == ox else 'start')
    # márgenes
    body += line(ox + 140, Y(voh), ox + 140, Y(vih), 'a', True); body += text(ox + 150, (Y(voh) + Y(vih)) / 2 + 4, f'NMH={voh-vih:.2f} V', 't tiny a', 'start')
    body += line(ox + 140, Y(vil), ox + 140, Y(vol), 'a', True); body += text(ox + 150, (Y(vil) + Y(vol)) / 2 + 4, f'NML={vil-vol:.2f} V', 't tiny a', 'start')
    if title: body += text(W / 2, H - 4, title, 't m')
    return svg(W, H, body, 'Márgenes de ruido ' + title, 'fig noise')

# --------------------------------------------------------------------- inversor CMOS
def fig_cmos():
    W, H = 300, 250; body = DEFS
    body += line(150, 20, 150, 40) + text(172, 24, 'VDD', 't m', 'start')
    body += f'<circle cx="150" cy="95" r="26" class="s f"/>' + text(150, 99, 'PMOS', 't b', 'middle', 11)
    body += f'<circle cx="150" cy="170" r="26" class="s f"/>' + text(150, 174, 'NMOS', 't b', 'middle', 11)
    body += line(150, 40, 150, 69) + line(150, 121, 150, 144) + line(150, 196, 150, 215)
    body += line(150, 133, 220, 133) + text(226, 137, 'Vout', 't b', 'start')
    body += line(40, 133, 100, 133) + text(30, 137, 'Vin', 't b', 'end')
    body += line(100, 95, 100, 170) + line(100, 95, 124, 95) + line(100, 170, 124, 170)
    body += text(150, 232, 'GND', 't m')
    body += text(256, 90, 'Vin=0: PMOS ON', 't tiny', 'end') + text(290, 195, 'Vin=1: NMOS ON', 't tiny', 'end')
    return svg(W, H, body, 'Inversor CMOS', 'fig cmos')

# --------------------------------------------------------------------- árbol de decodificadores
def fig_dec_tree():
    W, H = 560, 250; body = DEFS
    body += f'<rect x="20" y="95" width="90" height="60" rx="7" class="s blk"/>' + text(65, 122, 'DEC 2:4', 't b') + text(65, 140, 'E=1', 't tiny')
    body += text(8, 112, 'A3', 't m', 'end') + text(8, 138, 'A2', 't m', 'end')
    body += line(10, 110, 20, 110) + line(10, 136, 20, 136)
    for k in range(4):
        y = 10 + k * 58
        body += f'<rect x="250" y="{y}" width="100" height="48" rx="7" class="s blk"/>' + text(300, y + 22, f'DEC 2:4 #{k}', 't b') + text(300, y + 38, f'E=S{k}', 't tiny')
        body += line(110, 105 + k * 12 - 6, 250, y + 24, 's', True)
        body += line(350, y + 24, 430, y + 24, 's', True) + text(436, y + 28, f'S{4*k}…S{4*k+3}', 't m', 'start')
    body += text(200, 235, 'A1,A0 llegan a los cuatro decodificadores de la derecha', 't tiny', 'middle')
    return svg(W, H, body, 'Decodificador 4:16 con cinco 2:4', 'fig dectree')

# --------------------------------------------------------------------- biestable JK/T/D (tabla + símbolo)
def fig_ff(kind='JK'):
    W, H = 220, 150; body = DEFS
    body += f'<rect x="70" y="20" width="80" height="110" rx="4" class="s blk"/>'
    ins = {'JK': ['J', 'K'], 'T': ['T'], 'D': ['D']}[kind]
    for i, nme in enumerate(ins):
        y = 45 + i * 40 if kind == 'JK' else 55
        body += line(40, y, 70, y) + text(78, y + 4, nme, 't b', 'start')
    body += f'<path d="M70 98l12 8l-12 8" class="s"/>' + line(40, 106, 70, 106) + text(32, 110, 'CLK', 't m', 'end')
    body += line(150, 45, 185, 45) + text(142, 49, 'Q', 't b', 'end') + line(150, 105, 185, 105) + text(142, 109, 'Q̄', 't b', 'end')
    return svg(W, H, body, f'Biestable {kind}', 'fig ff')

def fig_mealy_moore():
    W, H = 600, 200; body = DEFS
    for dx, name, sub in ((0, 'Moore', 'salida = f(estado)'), (300, 'Mealy', 'salida = f(estado, entrada)')):
        body += f'<rect x="{dx+90}" y="60" width="80" height="50" rx="6" class="s blk"/>' + text(dx + 130, 82, 'Lógica', 't b') + text(dx + 130, 98, 'siguiente', 't m')
        body += f'<rect x="{dx+200}" y="60" width="60" height="50" rx="6" class="s blk"/>' + text(dx + 230, 90, 'Reg. Q', 't b')
        body += line(dx + 10, 85, dx + 90, 85, 's', True) + text(dx + 10, 78, 'X', 't b', 'start')
        body += line(dx + 170, 85, dx + 200, 85, 's', True)
        body += f'<path d="M{dx+260} 85h14v50h-230v-35h46" class="s nf" marker-end="url(#arr)"/>'
        body += f'<rect x="{dx+200}" y="140" width="0" height="0"/>'
        if name == 'Moore':
            body += line(dx + 274, 85, dx + 296 - 6, 85, 's', False)
            body += line(dx + 274, 85, dx + 280, 40, 's', False)
        body += text(dx + 150, 22, name, 't b', 'middle', 15) + text(dx + 150, 40, sub, 't m')
    return svg(W, H, body, 'Máquinas de Moore y de Mealy', 'fig mm')

REG = {'gates': fig_gates, 'cmos': fig_cmos, 'dectree': fig_dec_tree}
