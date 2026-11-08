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
