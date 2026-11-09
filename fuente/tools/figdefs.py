"""Figuras con nombre propias de la guía (presets)."""
import figs, json

def f_bloques_comb_sec(cap=''):
    blocks = {'a': (10, 40, 120, 60, 'Lógica\ncombinacional'), 'b': (290, 40, 120, 60, 'Lógica\ncombinacional'), 'm': (440, 130, 100, 50, 'Memoria\n(biestables)')}
    body = figs.DEFS
    for bid, (x, y, w, h, t) in blocks.items():
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" class="s blk"/>'
        for i, ln in enumerate(t.split('\n')): body += figs.text(x + w / 2, y + h / 2 + 4 + (i - 0.5) * 15, ln, 't b' if i == 0 else 't m', 'middle', 12)
    body += figs.line(0, 70, 10, 70, 's', True) + figs.text(4, 58, 'entradas', 't tiny', 'start') + figs.line(130, 70, 168, 70, 's', True) + figs.text(168, 74, 'salidas', 't tiny', 'start')
    body += figs.text(70, 125, 'COMBINACIONAL', 't b', 'middle', 12) + figs.text(70, 141, 'salida = f(entradas)', 't m')
    body += figs.line(260, 70, 290, 70, 's', True) + figs.text(250, 58, 'entradas', 't tiny', 'end') + figs.line(410, 70, 470, 70, 's', True) + figs.text(474, 74, 'salidas', 't tiny', 'start')
    body += f'<path d="M440 155h-30v-85" class="s nf" marker-end="url(#arr)"/>' + f'<path d="M350 70v0" class="s"/>'
    body += f'<path d="M410 85h12v70h18" class="s nf"/>'
    body += figs.text(350, 140, 'SECUENCIAL', 't b', 'middle', 12) + figs.text(350, 156, 'salida = f(entradas, estado)', 't m')
    return figs.svg(560, 180, body, 'Combinacional frente a secuencial', 'fig blocks')

def f_mapa(cap=''):
    items = [('T1-T3', 'Sistemas, numeración\ny Boole', 0, 0), ('T4-T5', 'Familias lógicas\ny combinacional', 1, 0), ('T6-T9', 'Biestables, memorias,\ncontadores, registros', 2, 0),
             ('T10-T11', 'Autómatas síncronos\ny descripciones', 3, 0), ('T12-T13', 'FPGA y VHDL', 4, 0)]
    body = figs.DEFS; W = 600
    for i, (code, txt, k, _) in enumerate(items):
        x = 10 + i * 116
        body += f'<rect x="{x}" y="30" width="104" height="92" rx="9" class="s blk"/>'
        body += figs.text(x + 52, 52, code, 't b a', 'middle', 13)
        for j, ln in enumerate(txt.split('\n')): body += figs.text(x + 52, 78 + j * 16, ln, 't m', 'middle', 11)
        if i < 4: body += figs.line(x + 104, 76, x + 116, 76, 's', True)
    body += figs.text(300, 148, 'combinacional  →  secuencial  →  lógica programable', 't m')
    return figs.svg(W, 160, body, 'Mapa de la asignatura', 'fig blocks')

def f_noise(voh, vih, vil, vol, vcc, title='', cap=''):
    return figs.fig_noise(voh, vih, vil, vol, vcc, title)

def f_fsm(nodes, edges, W=560, H=300, title='', cap=''):
    return figs.fig_fsm({k: tuple(v) if len(v) == 3 else (v[0], v[1], '') for k, v in nodes.items()}, [tuple(e) if len(e) == 4 else tuple(e) + (0,) for e in edges], W, H, title)

def f_timing(signals, labels_top=None, title='', slots=None, cap=''):
    return figs.fig_timing([(n, v) for n, v in signals], slots, None, title, labels_top)

def f_ffsym(kind='JK', cap=''):
    return figs.fig_ff(kind)

def f_mm(kind='moore', cap=''):
    mealy = kind == 'mealy'
    bl = {'a': (120, 30, 120, 56, 'Lógica de\nsiguiente estado'), 'b': (290, 30, 100, 56, 'Biestables\n(estado Q)'), 'c': (440, 30, 110, 56, 'Lógica\nde salida')}
    ar = [(10, 58, 120, 58, 'X'), (240, 58, 290, 58, 'D / J,K'), (390, 58, 440, 58, 'Q'), (550, 58, 590, 58, 'Z')]
    body = figs.fig_blocks(bl, ar, 600, 150, '')
    body = body[:body.rfind('</svg>')]
    body += '<path d="M415 58V120H180V86" class="s nf" marker-end="url(#arr)"/>'
    body += figs.text(300, 136, 'realimentación del estado', 't tiny')
    body += '<text x="15" y="14" class="t tiny" text-anchor="start">%s</text>' % ('MEALY: la salida depende de Q y de X' if mealy else 'MOORE: la salida depende solo de Q')
    if mealy: body += '<path d="M70 58V10H495V30" class="s nf" marker-end="url(#arr)"/>'
    return body + '</svg>'

def f_flujo(cap=''):
    names = ['Descripción\n(esquema, estados,\nVHDL)', 'Simulación\nfuncional', 'Síntesis', 'Implementación\n(colocar y\nconectar)', 'Prueba en\nla placa']
    bl = {}; ar = []
    for i, t in enumerate(names):
        x = 8 + i * 112
        bl[f'b{i}'] = (x, 30, 96, 70, t)
        if i < 4: ar.append((x + 96, 65, x + 112, 65, ''))
    return figs.fig_blocks(bl, ar, 570, 120, 'Flujo de diseño con herramientas EDA')


# ====================================================================== figuras añadidas (2ª tanda)
import math as _m
T = figs.text; L = figs.line; D = figs.DEFS

def _box(x, y, w, h, lines, cls='blk', big=12):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" class="s {cls}"/>'
    lines = lines if isinstance(lines, list) else str(lines).split('\n')
    for i, ln in enumerate(lines):
        s += T(x + w / 2, y + h / 2 + 4 + (i - (len(lines) - 1) / 2) * 15, ln, 't b' if i == 0 else 't m', 'middle', big)
    return s

def _clk(x, y):
    return f'<path d="M{x} {y-6}l9 6l-9 6" class="s nf"/>'

def f_blocks(blocks, arrows, W=560, H=240, title='', cap=''):
    """Diagrama de bloques genérico. blocks: {id: [x,y,w,h,'texto\\nsegunda línea']}; arrows: [[x1,y1,x2,y2,'etiqueta']]"""
    return figs.fig_blocks({k: tuple(v) for k, v in blocks.items()}, [tuple(a) for a in arrows], W, H, title)

def f_rueda_c2(n=4, cap=''):
    N = 2 ** n; cx, cy, R = 200, 190, 135; body = D + f'<circle cx="{cx}" cy="{cy}" r="{R}" class="s nf"/>'
    for v in range(N):
        a = -_m.pi / 2 + 2 * _m.pi * v / N; sv = v if v < N // 2 else v - N
        x, y = cx + R * _m.cos(a), cy + R * _m.sin(a)
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="s f"/>'
        xi, yi = cx + (R - 30) * _m.cos(a), cy + (R - 30) * _m.sin(a)
        body += T(f'{xi:.1f}', f'{yi + 4:.1f}', format(v, f'0{n}b'), 't tiny', 'middle')
        xo, yo = cx + (R + 24) * _m.cos(a), cy + (R + 24) * _m.sin(a)
        body += T(f'{xo:.1f}', f'{yo + 4:.1f}', str(sv), 't b a' if sv < 0 else 't b', 'middle', 12)
    body += T(cx, cy - 6, f'{n} bits', 't b', 'middle', 14) + T(cx, cy + 12, 'fuera: valor en C2', 't m') + T(cx, cy + 28, 'dentro: código binario', 't m')
    return figs.svg(400, 380, body, f'Rueda de complemento a 2 de {n} bits', 'fig blocks')

def f_gray(n=3, cap=''):
    N = 2 ** n; cx, cy, R = 150, 150, 100; body = D + f'<circle cx="{cx}" cy="{cy}" r="{R}" class="s nf"/>'
    for v in range(N):
        a = -_m.pi / 2 + 2 * _m.pi * v / N; g = v ^ (v >> 1)
        x, y = cx + R * _m.cos(a), cy + R * _m.sin(a)
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="s f"/>'
        xo, yo = cx + (R + 28) * _m.cos(a), cy + (R + 28) * _m.sin(a)
        body += T(f'{xo:.1f}', f'{yo + 4:.1f}', format(g, f'0{n}b'), 't b', 'middle', 12)
        xi, yi = cx + (R - 22) * _m.cos(a), cy + (R - 22) * _m.sin(a)
        body += T(f'{xi:.1f}', f'{yi + 4:.1f}', str(v), 't tiny', 'middle')
    body += T(cx, cy + 4, 'Gray', 't b', 'middle', 14)
    return figs.svg(300, 300, body, f'Código Gray de {n} bits en anillo', 'fig blocks')

def f_sumador(n=4, cap=''):
    """El bit 0 va a la derecha; el acarreo viaja hacia la izquierda."""
    body = D; W = 70 + n * 110
    for k in range(n):
        i = n - 1 - k; x = 40 + k * 110
        body += _box(x, 60, 80, 70, ['Sumador', f'completo {i}'])
        body += L(x + 25, 20, x + 25, 60, 's', True) + T(x + 25, 14, f'A{i}', 't', 'middle', 12)
        body += L(x + 55, 20, x + 55, 60, 's', True) + T(x + 55, 14, f'B{i}', 't', 'middle', 12)
        body += L(x + 40, 130, x + 40, 168, 's', True) + T(x + 40, 184, f'S{i}', 't b', 'middle', 12)
        if k < n - 1: body += L(x + 110, 95, x + 80, 95, 's', True) + T(x + 95, 87, f'C{i}', 't tiny halo', 'middle')
    body += L(40, 95, 4, 95, 's', True) + T(4, 84, f'C{n}', 't tiny', 'start') + T(4, 112, '(C_out)', 't tiny', 'start')
    xr = 40 + (n - 1) * 110 + 80
    body += L(xr + 34, 95, xr, 95, 's', True) + T(xr + 38, 99, 'C_in', 't', 'start', 12)
    return figs.svg(W + 30, 195, body, f'Sumador de {n} bits con acarreo en cascada', 'fig blocks')

def f_mux(k=2, cap=''):
    n = 2 ** k; H = 30 + 26 * n; body = D
    body += f'<path d="M110 10 L190 {10+(H-20)*0.18:.0f} L190 {H-10-(H-20)*0.18:.0f} L110 {H-10} Z" class="s blk"/>'
    for i in range(n):
        y = 30 + 26 * i - 6
        body += L(60, y + 5, 110, y + 5, 's', True) + T(54, y + 9, f'I{i}', 't', 'end', 12)
    body += L(190, H / 2, 240, H / 2, 's', True) + T(246, H / 2 + 4, 'Y', 't b', 'start', 13)
    for j in range(k):
        x = 135 + j * 22
        body += L(x, H + 22, x, H - 12, 's', True) + T(x, H + 36, f'S{k-1-j}', 't', 'middle', 12)
    body += T(150, H / 2 + 4, f'MUX {n}:1', 't b', 'middle', 12)
    return figs.svg(280, H + 46, body, f'Multiplexor {n}:1', 'fig blocks')

def f_dec(k=2, cap=''):
    n = 2 ** k; H = 30 + 26 * n; body = D + f'<rect x="90" y="10" width="90" height="{H-10}" rx="7" class="s blk"/>'
    for j in range(k):
        y = 30 + j * 26 + (H - 10 - 26 * k) / 2
        body += L(40, y, 90, y, 's', True) + T(34, y + 4, f'A{k-1-j}', 't', 'end', 12)
    for i in range(n):
        y = 28 + 26 * i
        body += L(180, y, 230, y, 's', True) + T(238, y + 4, f'Y{i}', 't', 'start', 12)
    body += L(135, H + 14, 135, H, 's', True) + T(135, H + 28, 'EN', 't tiny', 'middle')
    body += T(135, H / 2 + 6, f'{k}→{n}', 't b', 'middle', 13)
    return figs.svg(290, H + 36, body, f'Decodificador {k} a {n}', 'fig blocks')

def f_memoria(n=3, m=4, cap=''):
    rows = 2 ** n; ch = 24; body = D; top = 30; hh = rows * ch
    body += f'<rect x="40" y="{top}" width="96" height="{hh}" rx="7" class="s blk"/>' + T(88, top + hh / 2 - 2, 'Decodificador', 't b', 'middle', 11) + T(88, top + hh / 2 + 14, f'{n} → {rows}', 't m', 'middle')
    for j in range(n):
        y = top + hh / 2 - 18 + j * 18 - (n - 3) * 9
        body += L(8, y, 40, y, 's', True)
    body += T(6, top - 8, f'dirección ({n} bits)', 't tiny', 'start')
    xa = 210; wa = m * 34 + 10
    body += f'<rect x="{xa}" y="{top}" width="{wa}" height="{hh}" rx="6" class="s f"/>'
    for r in range(rows):
        y = top + r * ch + ch / 2
        body += L(136, y, xa, y, 's') + T(xa - 8, y - 3, f'palabra {r}', 't tiny', 'end') if False else L(136, y, xa, y, 's')
        if r: body += f'<line x1="{xa}" y1="{top+r*ch}" x2="{xa+wa}" y2="{top+r*ch}" class="grid"/>'
        body += T(172, y - 3, f'{r}', 't tiny', 'middle')
        for c in range(m): body += T(xa + 22 + c * 34, y + 4, '·', 't m', 'middle')
    xr = xa + wa
    body += L(xr, top + hh / 2, xr + 54, top + hh / 2, 's', True) + T(xr + 58, top + hh / 2 + 4, f'datos ({m} bits)', 't tiny', 'start')
    body += T(xa + wa / 2, top - 8, 'matriz de celdas', 't m', 'middle')
    return figs.svg(xr + 150, top + hh + 14, body, f'Memoria de {rows} palabras de {m} bits', 'fig blocks')

def f_shreg(kind='shift', n=4, cap=''):
    ox, oy = 64, 54 if kind == 'lfsr' else 34; body = D; W = ox + n * 90 + 90
    xs = [ox + i * 90 for i in range(n)]
    for i, x in enumerate(xs):
        body += _box(x, oy + 20, 56, 50, [f'FF{i}', 'D'], 'blk', 12)
        if i: body += L(xs[i - 1] + 56, oy + 45, x, oy + 45, 's', True)
        body += _clk(x, oy + 58) if False else ''
        body += L(x + 28, oy + 98, x + 28, oy + 70, 's', True) + f'<path d="M{x+21} {oy+70}l7 -8l7 8" class="s nf"/>'
    body += L(ox - 40, oy + 45, ox, oy + 45, 's', True) + T(ox - 42, oy + 36, 'entrada', 't tiny', 'start')
    xe = xs[-1] + 56
    body += L(xe, oy + 45, xe + 44, oy + 45, 's', True) + T(xe + 48, oy + 49, 'salida', 't tiny', 'start')
    body += L(xs[0] + 28, oy + 98, xs[-1] + 28, oy + 98, 's') + T(ox - 30, oy + 102, 'CLK', 't', 'start', 12)
    top = oy - 6
    if kind in ('anillo', 'johnson'):
        mx = (xe + 22 + ox - 22) / 2
        body += f'<path d="M{xe+22} {oy+45} V{top} H{ox-22} V{oy+45} H{ox}" class="s nf" marker-end="url(#arr)"/>'
        if kind == 'johnson': body += f'<circle cx="{mx:.0f}" cy="{top}" r="5" class="s f"/>' + T(mx, top - 9, 'NOT', 't tiny', 'middle')
        else: body += T(mx, top - 8, 'realimentación directa', 't tiny', 'middle')
    elif kind == 'lfsr':
        xa, xb = xs[-1] + 28, xs[-2] + 28; mx = (xa + xb) / 2
        body += f'<circle cx="{mx:.0f}" cy="{top}" r="11" class="s f"/>' + T(mx, top + 5, '⊕', 't b', 'middle', 15)
        body += f'<path d="M{xa} {oy+45} V{top} H{mx+11:.0f}" class="s nf"/>' + f'<path d="M{xb} {oy+45} V{top} H{mx-11:.0f}" class="s nf"/>'
        body += f'<path d="M{mx:.0f} {top-11} V{top-22} H{ox-22} V{oy+45} H{ox}" class="s nf" marker-end="url(#arr)"/>'
        body += T(mx, top - 28, 'XOR de las dos últimas salidas', 't tiny', 'middle')
    return figs.svg(W, oy + 118, body, {'shift': 'Registro de desplazamiento', 'anillo': 'Contador en anillo', 'johnson': 'Contador Johnson', 'lfsr': 'LFSR'}[kind], 'fig blocks')

def f_contador(kind='sync', n=3, cap=''):
    body = D; W = 100 + n * 130
    xs = [80 + i * 130 for i in range(n)]
    for i, x in enumerate(xs):
        body += _box(x, 60, 70, 56, [f'T{i}' if kind == 'sync' else 'T = 1', f'Q{i}'], 'blk', 12)
        body += _clk(x, 100)
        body += L(x + 70, 78, x + 100, 78, 's', True) if (kind == 'sync' or i == n - 1) else ''
        body += T(x + 84, 70, f'Q{i}', 't tiny', 'middle') if (kind == 'sync' or i == n - 1) else ''
        if kind == 'sync':
            lab = ['T0 = 1', 'T1 = Q0', 'T2 = Q1·Q0', 'T3 = Q2·Q1·Q0'][i]
            body += L(x + 35, 28, x + 35, 60, 's', True) + T(x + 35, 20, lab, 't tiny', 'middle')
            body += L(x - 18 if False else x - 12, 100, x, 100, 's')
        elif i < n - 1:
            body += f'<path d="M{x+70} 78 H{x+95} V100 H{x+130-12}" class="s nf"/>' + L(xs[i + 1] - 12, 100, xs[i + 1], 100, 's', True)
            body += T(x + 84, 70, f'Q{i}', 't tiny', 'middle')
    if kind == 'sync':
        body += f'<path d="M{xs[0]-12} 100 V150 H{xs[-1]-12} V100" class="s nf"/>'
        for x in xs[1:-1]: body += L(x - 12, 150, x - 12, 100, 's')
        body += T(xs[0] - 14, 168, 'CLK (el mismo para todos)', 't tiny', 'start')
        body += T(W / 2, 12, 'Cada biestable recibe su T calculada con puertas AND', 't m', 'middle') if False else ''
    else:
        body += L(xs[0] - 44, 100, xs[0] - 12, 100, 's') + L(xs[0] - 12, 100, xs[0], 100, 's', True) + T(xs[0] - 46, 94, 'CLK', 't', 'end', 12)
        body += T(W / 2, 40, 'El reloj de cada biestable es la salida del anterior', 't m', 'middle')
    return figs.svg(W, 180, body, 'Contador ' + ('síncrono' if kind == 'sync' else 'asíncrono'), 'fig blocks')

def f_lut(cap=''):
    body = D + _box(50, 30, 120, 100, ['LUT de 4', '16 bits'], 'blk', 13)
    for i, nm in enumerate('ABCD'): body += L(20, 52 + i * 20, 50, 52 + i * 20, 's', True) + T(14, 56 + i * 20, nm, 't tiny', 'end')
    body += L(170, 80, 215, 80, 's') + _box(215, 55, 80, 50, ['Biestable', 'D'], 'blk', 12) + _clk(215, 92)
    body += f'<path d="M190 80 V135 H330 V80" class="s nf" stroke-dasharray="5 3"/>'
    body += L(295, 80, 380, 80, 's', True) + T(300, 72, 'a la salida', 't tiny', 'start') + T(190, 150, 'camino sin biestable (lógica combinacional)', 't tiny', 'start')
    return figs.svg(430, 160, body, 'Bloque lógico: LUT más biestable', 'fig blocks')

def f_fpga(cap=''):
    body = D; g = 84
    for r in range(3):
        for c in range(4):
            x, y = 60 + c * g, 46 + r * 64
            body += f'<rect x="{x}" y="{y}" width="46" height="38" rx="5" class="s blk"/>' + T(x + 23, y + 24, 'CLB', 't b', 'middle', 11)
            if c < 3: body += L(x + 46, y + 19, x + g, y + 19, 's')
            if r < 2: body += L(x + 23, y + 38, x + 23, y + 64, 's')
    for c in range(4):
        x = 60 + c * g + 23
        body += f'<rect x="{x-14}" y="2" width="28" height="18" rx="3" class="s f"/>' + T(x, 15, 'E/S', 't tiny', 'middle') + L(x, 20, x, 46, 's')
        body += f'<rect x="{x-14}" y="{46+3*64-6}" width="28" height="18" rx="3" class="s f"/>' + T(x, 46 + 3 * 64 + 7, 'E/S', 't tiny', 'middle') + L(x, 46 + 2 * 64 + 38, x, 46 + 3 * 64 - 6, 's')
    return figs.svg(440, 46 + 3 * 64 + 40, body + T(220, 46 + 3 * 64 + 34, 'CLB = bloque lógico · E/S = pines · líneas = conexiones programables', 't m', 'middle'), 'Esquema de una FPGA', 'fig blocks')

def f_entidad(name='sum4', entradas=('a[3:0]', 'b[3:0]', 'cin'), salidas=('s[3:0]', 'cout'), cap=''):
    h = 30 + 24 * max(len(entradas), len(salidas)); body = D + _box(130, 10, 150, h, [name, 'entity / architecture'], 'blk', 13)
    for lst, x0, x1, anc, xt in ((entradas, 70, 130, 'end', 64), (salidas, 280, 340, 'start', 346)):
        for i, e in enumerate(lst):
            y = 10 + h / 2 + (i - (len(lst) - 1) / 2) * 24
            body += L(x0, y, x1, y, 's', True) + T(xt, y + 4, e, 't', anc, 12)
    return figs.svg(440, h + 20, body, 'Entidad VHDL ' + name, 'fig blocks')
