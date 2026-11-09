#!/usr/bin/env python3
"""Genera la guía: HTML maestro (un solo archivo) + web multipágina + PWA a partir de src/*.dsl.
Uso:  python3 build.py [--site]   """
import os, re, sys, json, glob, base64, datetime, html, shutil, zoneinfo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import dsl, figs, figdefs
from dsl import Ctx, esc, inline, render, finalize_math, render_math_all, MATH
from logic import minimize

OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Madrid'))
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
FECHA = f'{NOW.day} de {MESES[NOW.month-1]} de {NOW.year}'
TITLE = 'Electrónica Digital · Guía de estudio'

# ------------------------------------------------------------ resultados verificados
R = {}; CHK = {}
for f in sorted(glob.glob(os.path.join(OUT, 'results*.json'))):
    d = json.load(open(f)); R.update(d['R'])
    for c in d['CHK']: CHK[c['id']] = c['ok']
Ctx.R = R
bad = [k for k, v in CHK.items() if not v]
if bad: sys.exit('Hay comprobaciones fallidas: ' + ', '.join(bad))

# ------------------------------------------------------------ lectura de fuentes
BLOCKS = []; EXAMS = []; HOJAS = []
def read_src():
    for f in sorted(glob.glob(os.path.join(ROOT, 'src', '*.dsl'))):
        txt = open(f, encoding='utf-8').read()
        meta = {}; body = []
        for ln in txt.split('\n'):
            if ln.startswith('%%'):
                k, _, v = ln[2:].strip().partition('='); meta[k.strip()] = v.strip()
            else: body.append(ln)
        nodes = dsl.parse('\n'.join(body), os.path.basename(f))
        meta['file'] = os.path.basename(f); meta['nodes'] = nodes
        g = meta.get('group', 'tema')
        (EXAMS if g == 'examdata' else HOJAS if g == 'hojadata' else BLOCKS).append(meta)
read_src()
GROUP_ORDER = ['intro', 'tema', 'prac', 'ejer', 'demo', 'auto', 'ref']
GROUP_NAME = {'intro': 'Empieza aquí', 'tema': 'Teoría por temas', 'prac': 'Prácticas', 'ejer': 'Ejercicios resueltos', 'demo': 'Demostraciones', 'auto': 'Repaso', 'ref': 'Consulta'}
BLOCKS.sort(key=lambda m: (GROUP_ORDER.index(m.get('group', 'tema')), float(m.get('n', 0))))
for i, b in enumerate(BLOCKS):
    b['idx'] = i
    b['color'] = f"c{(int(b.get('color', 0)) or (int(float(b.get('n', i))) % 8) + 1)}"

# ------------------------------------------------------------ comprobaciones declaradas en los ejercicios
def check_ejs(nodes):
    for n in nodes:
        if n.kind == 'ej':
            m = dsl.meta_ej(n)
            for c in m['checks']:
                hit = [k for k in CHK if k == c or k.startswith(c.rstrip('*') if c.endswith('*') else c + '.')]
                if not hit: sys.exit(f'Ejercicio {m["id"]}: comprobación inexistente «{c}»')
        if hasattr(n, 'children'): check_ejs(n.children)
for m in BLOCKS + EXAMS + HOJAS: check_ejs(m['nodes'])

# ------------------------------------------------------------ figuras
def fig_dispatch(name, args):
    if name == 'kmap':
        key = args.get('key'); n = args['n']
        on = args.get('on') or R[key + '.on']; dc = args.get('dc') if 'dc' in args else R.get(key + '.dc', [])
        imps = minimize(n, on, dc) if args.get('groups', True) else None
        return figs.fig_kmap(n, set(on), set(dc), args['names'], imps, args.get('title', ''))
    if hasattr(figdefs, 'f_' + name): return getattr(figdefs, 'f_' + name)(**args)
    if name in figs.REG: return figs.REG[name](**args)
    raise KeyError('figura desconocida ' + name)
Ctx.figs = fig_dispatch

# ------------------------------------------------------------ auto-contenido
TAGNAME = {'comb': 'Combinacional (puertas, Karnaugh)', 'msi': 'Bloques MSI y displays', 'arit': 'Aritmética y códigos (BCD, C2)',
           'sec': 'Autómatas / síntesis secuencial', 'cont': 'Contadores y biestables', 'fam': 'Familias lógicas', 'vhdl': 'VHDL / lógica programable'}
def all_ej(items):
    out = []
    def walk(ns, meta):
        for n in ns:
            if n.kind == 'ej': out.append((meta, n))
            if hasattr(n, 'children'): walk(n.children, meta)
    for m in items: walk(m['nodes'], m)
    return out
EJ_EX = all_ej(EXAMS); EJ_HO = all_ej(HOJAS)

def auto_stats():
    cnt = {}; tot = len(EJ_EX)
    per = {}
    for m, n in EJ_EX:
        e = dsl.meta_ej(n)
        for t in e['tags']:
            if t in TAGNAME: cnt[t] = cnt.get(t, 0) + 1; per.setdefault(t, set()).add(m['id'])
    rows = ''
    nex = len(EXAMS)
    for t, c in sorted(cnt.items(), key=lambda x: -x[1]):
        rows += (f'<tr><td>{esc(TAGNAME[t])}</td><td>{c} de {tot}</td><td style="min-width:120px"><div class="bar"><i style="width:{100*c/tot:.0f}%"></i></div></td>'
                 f'<td>{len(per[t])} de {nex} exámenes</td></tr>')
    return ('<div class="tw"><table><thead><tr><th>Tipo de problema</th><th>Problemas</th><th>Peso</th><th>Aparece en</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            f'<p class="small">Recuento propio sobre los {tot} problemas de los {nex} exámenes resueltos aquí (un problema puede tener varias etiquetas). Son pocos exámenes: úsalo como orientación, no como regla.</p>')

def auto_exam_start():
    out = '<div class="cardgrid">'
    for m in sorted([e for e in EXAMS if e.get('featured') == '1'], key=lambda e: -int(e.get('orden', 0))):
        ids = [dsl.meta_ej(n)['id'] for mm, n in EJ_EX if mm is m]
        out += (f'<a class="tile" href="#{m["id"]}"><b>{esc(m["title"])}</b><span>{esc(m.get("sub", ""))}<br>{len(ids)} problemas</span></a>')
    return out + '</div>'

def auto_exam_topic():
    by = {}
    for m, n in EJ_EX + EJ_HO:
        e = dsl.meta_ej(n)
        for t in e['tags']:
            if t in TAGNAME: by.setdefault(t, []).append((e, m))
    out = ''
    for t in TAGNAME:
        if t not in by: continue
        out += f'<details class="det"><summary>{esc(TAGNAME[t])} <span class="small">({len(by[t])})</span></summary><ul>'
        for e, m in by[t]: out += f'<li><a class="xref" href="#{e["id"]}">{inline(e["title"])}</a> <span class="small">· {esc(e["origen"])}</span></li>'
        out += '</ul></details>'
    return out

def auto_exam_search():
    chips = ''.join(f'<button class="chip" data-f="{t}" type="button">{esc(TAGNAME[t].split(" (")[0])}</button>' for t in TAGNAME if any(t in dsl.meta_ej(n)['tags'] for _, n in EJ_EX))
    chips += ''.join(f'<button class="chip" data-f="{k.lower()}" type="button">{k}</button>' for k in sorted({e.get('tipo', '') for e in EXAMS if e.get('tipo')}))
    out = f'<div class="chips">{chips}</div><input id="exq" type="search" placeholder="Buscar en los exámenes (p. ej. caja fuerte, BCD, contador)…" style="width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:9px;background:var(--paper);color:var(--ink);font:inherit">'
    years = sorted({e.get('anio', '') for e in EXAMS}, reverse=True)
    for y in years:
        out += f'<h3>{esc(y)}</h3>'
        for m in sorted([e for e in EXAMS if e.get('anio', '') == y], key=lambda e: -int(e.get('orden', 0))):
            out += (f'<details class="exgroup" id="{m["id"]}"><summary><b>{esc(m["title"])}</b> <span class="small">{esc(m.get("sub", ""))}</span></summary><div class="inner">'
                    + render(m['nodes']) + '</div></details>')
    return out

def auto_hojas():
    out = ''
    for m in sorted(HOJAS, key=lambda e: float(e.get('n', 0))):
        out += (f'<details class="exgroup" id="{m["id"]}"><summary><b>{esc(m["title"])}</b> <span class="small">{esc(m.get("sub", ""))}</span></summary><div class="inner">'
                + render(m['nodes']) + '</div></details>')
    return out

def auto_checklist():
    out = '<div class="box idea"><div class="boxh"><span class="ic">📈</span> Tu progreso <span class="small">(se guarda en este navegador)</span></div><div class="bar"><i id="gprog" style="width:0"></i></div><p class="small" id="gprogt"></p></div>'
    for b in BLOCKS:
        if b.get('group') != 'tema': continue
        gid = b['id']
        out += f'<div class="box" style="--bx:var(--{b["color"]})"><div class="boxh">{esc(b["title"])}</div>'
        for k, lab in (('t', 'Leer la teoría y entender las figuras'), ('e', 'Hacer los ejemplos sin mirar la solución'), ('q', 'Test de autoevaluación del tema')):
            out += f'<label class="check"><input type="checkbox" data-chk="{gid}-{k}" data-grp="{gid}"><span>{lab}</span></label>'
        out += '</div>'
    out += '<div class="box"><div class="boxh">Bloques de examen</div>'
    for k, lab in (('ex1', 'Resolver 2 exámenes completos en 2 horas (sin mirar la teoría)'), ('ex2', 'Rehacer los problemas que fallaste'), ('ho', 'Hojas de problemas: combinacional'), ('ho2', 'Hojas de problemas: autómatas'), ('pr', 'Repasar las prácticas y el código VHDL')):
        out += f'<label class="check"><input type="checkbox" data-chk="gen-{k}" data-grp="gen"><span>{lab}</span></label>'
    return out + '</div>'

def auto_gloss():
    items = []
    def walk(ns):
        for n in ns:
            if n.kind == 'gloss': items.append(n.arg)
            if hasattr(n, 'children'): walk(n.children)
    for b in BLOCKS + EXAMS + HOJAS: walk(b['nodes'])
    items.sort(key=lambda a: a.split('|')[0].strip().lower())
    return ''.join(render([dsl.Node('gloss', arg=a)]) for a in items)

def auto_cards():
    cs = []
    for b in BLOCKS:
        def walk(ns):
            for n in ns:
                if n.kind == 'card': cs.append(n)
                if hasattr(n, 'children'): walk(n.children)
        walk(b['nodes'])
    return '<div class="cards">' + render(cs) + '</div>'

def auto_quizzes():
    out = ''
    for b in BLOCKS:
        if b.get('group') != 'tema': continue
        qs = []
        def walk(ns):
            for n in ns:
                if n.kind == 'q': qs.append(n)
                if hasattr(n, 'children'): walk(n.children)
        walk(b['nodes'])
        if not qs: continue
        out += (f'<details class="det" id="q-{b["id"]}"><summary>{esc(b["title"])} <span class="small">({len(qs)} preguntas)</span></summary>'
                + render(qs) + '</details>')
    return out
def auto_formulas():
    out = ''
    for b in BLOCKS:
        if b.get('group') != 'tema': continue
        bx = [n for n in b['nodes'] if n.kind == 'box' and n.arg.split('|')[0].strip() == 'formula' and 'Fórmulas clave' in n.arg]
        if not bx: continue
        out += f'<h3>{esc(b["title"])}</h3>' + ''.join(render(n.children) for n in bx)
    return out

def auto_onepage():
    b = [x for x in BLOCKS if x['id'] == 'formulario1p']
    return render(b[0]['nodes']) if b else ''

def auto_score():
    return '<div class="box idea"><div class="boxh"><span class="ic">🎯</span> Tu puntuación</div><p id="score" class="small">0 correctas de 0 respondidas</p><button class="btn" id="resetq" type="button">Reiniciar el test</button></div>'
AUTO = {'onepage': auto_onepage, 'formulas': auto_formulas, 'score': auto_score, 'stats': auto_stats, 'exam-start': auto_exam_start, 'exam-topic': auto_exam_topic, 'exam-search': auto_exam_search,
        'hojas': auto_hojas, 'quizzes': auto_quizzes, 'checklist': auto_checklist, 'gloss': auto_gloss, 'cards': auto_cards}
Ctx.auto = lambda name: AUTO[name]()

# ------------------------------------------------------------ plantilla
def katex_css():
    css = open('/opt/npm-tools/node_modules/katex/dist/katex.min.css', encoding='utf-8').read()
    fd = '/opt/npm-tools/node_modules/katex/dist/fonts/'
    def rep(m):
        name = m.group(1)
        b = base64.b64encode(open(fd + name + '.woff2', 'rb').read()).decode()
        return f'src:url(data:font/woff2;base64,{b}) format("woff2")'
    css = re.sub(r'src:url\(fonts/([\w\-]+)\.woff2\) format\("woff2"\),url\(fonts/[\w\-]+\.woff\) format\("woff"\),url\(fonts/[\w\-]+\.ttf\) format\("truetype"\)', rep, css)
    return css


HUB = 'https://helionacon-ui.github.io/GIEIA-UPCT/'
# páginas del sitio multipágina: (archivo, título, grupo de navegación, bloques, color)
PAGES = [
 ('index', 'Portada', 'Empezar', ['empieza'], 'c1'),
 ('empezar', 'El examen y cómo estudiar', 'Empezar', ['examen'], 'c1'),
 ('tema-0-3', 'T0–T3 · Fundamentos y álgebra de Boole', 'Unidad 1 · Introducción', ['t00', 't01', 't02', 't03'], 'c1'),
 ('tema-4-5', 'T4–T5 · Familias lógicas y combinacional', 'Unidad 2 · Combinacional', ['t04', 't05'], 'c3'),
 ('tema-6-9', 'T6–T9 · Biestables, memorias, contadores y registros', 'Unidad 3 · Secuencial', ['t06', 't07', 't08', 't09'], 'c4'),
 ('tema-10-11', 'T10–T11 · Autómatas síncronos y descripciones', 'Unidad 3 · Secuencial', ['t10', 't11'], 'c5'),
 ('tema-12-13', 'T12–T13 · Lógica programable y VHDL', 'Unidad 4 · Programable', ['t12', 't13'], 'c6'),
 ('laboratorio', 'Prácticas y simulador', 'Prácticas', ['p1', 'p2', 'p3', 'p4', 'p567'], 'c7'),
 ('examenes', 'Exámenes resueltos paso a paso', 'Practicar', ['examenes'], 'c8'),
 ('hojas', 'Hojas de problemas resueltas', 'Practicar', ['hojas'], 'c8'),
 ('libro', 'Libro de problemas resueltos', 'Practicar', ['libro1', 'libro2', 'libro3', 'libro4'], 'c2'),
 ('demostraciones', 'Demostraciones', 'Practicar', ['demos'], 'c8'),
 ('autoevaluacion', 'Autoevaluación', 'Practicar', ['autoeval'], 'c8'),
 ('simulacros', 'Simulacros con soluciones', 'Practicar', ['simulacros'], 'c8'),
 ('formulario', 'Formulario por tema', 'Repasar', ['formulario', 'formulario1p'], 'c1'),
 ('glosario', 'Glosario', 'Repasar', ['glosario'], 'c1'),
 ('plan', 'Plan de estudio', 'Repasar', ['plan'], 'c1'),
]
BID = {b['id']: b for b in BLOCKS}
for p in PAGES:
    for bid in p[3]:
        if bid not in BID: print('AVISO: bloque sin escribir:', bid)
PAGES = [(f, t, g, [x for x in ids if x in BID], c) for f, t, g, ids, c in PAGES]
PAGES = [p for p in PAGES if p[3]]
B2P = {bid: p[0] for p in PAGES for bid in p[3]}
MISSING = [b['id'] for b in BLOCKS if b['id'] not in B2P]
if MISSING: sys.exit('Bloques sin página: %s' % MISSING)

def side_html(cur=None, multipage=False):
    s = ('<div class="search"><input id="q" type="search" placeholder="Buscar en toda la guía…" aria-label="Buscar"></div><div id="hits"></div>')
    last = None
    if multipage:
        for f, t, g, ids, c in PAGES:
            if g != last: s += f'<h5>{esc(g)}</h5>'; last = g
            on = ' class="on"' if cur == f else ''
            s += f'<a href="{f}.html" data-pg="{f}"{on} style="--tc:var(--{c})"><i class="dot"></i><span>{esc(t)}</span></a>'
            if cur == f and len(ids) > 1:
                for bid in ids: s += f'<a class="sub" href="#{bid}" style="--tc:var(--{c})"><span>{esc(BID[bid].get("short", BID[bid]["title"]))}</span></a>'
        s += '<h5>Todo junto</h5><a href="guia-completa.html" style="--tc:var(--c7)"><i class="dot"></i><span>Guía completa en una página</span></a>'
        s += '<a href="pdf.html" style="--tc:var(--c7)"><i class="dot"></i><span>Descargas en PDF</span></a>'
        return s
    for p in PAGES:
        f, t, g, ids, c = p
        if g != last: s += f'<h5>{esc(g)}</h5>'; last = g
        for bid in ids:
            b = BID[bid]; on = ' class="on"' if cur == bid else ''
            pct = f'<span class="pct" data-grp="{bid}"></span>' if b.get('group') == 'tema' else ''
            s += f'<a href="#{bid}" data-blk="{bid}"{on} style="--tc:var(--{c})"><i class="dot"></i><span>{esc(b.get("short", b["title"]))}</span>{pct}</a>'
    return s

def block_html(b):
    body = render(b['nodes'])
    kick = b.get('kicker', GROUP_NAME[b.get('group', 'tema')])
    sub = f'<p>{inline(b["sub"])}</p>' if b.get('sub') else ''
    return (f'<section class="blk" id="{b["id"]}" style="--tc:var(--{b["color"]})"><div class="bhead"><div class="kick">{esc(kick)}</div>'
            f'<h1>{inline(b["title"])}</h1>{sub}</div>{body}</section>')

def hero(stats):
    st = ''.join(f'<div><b>{n}</b><span>{esc(l)}</span></div>' for n, l in stats)
    return (f'<header class="hero"><div class="eyebrow">UPCT · Grado en Ingeniería Biomédica · 3.º curso</div>'
            f'<p class="fecha">Última actualización: <time datetime="{NOW.date().isoformat()}">{FECHA}</time></p>'
            f'<h1>Electrónica <span>Digital</span></h1><p class="sub">Guía para aprobar</p><div class="stats">{st}</div>'
            '<div class="cta"><a class="btn pri" href="#empieza">Empieza desde cero</a><a class="btn" href="empezar.html">El examen</a><a class="btn" href="examenes.html">Exámenes resueltos</a>'
            '<a class="btn" href="laboratorio.html">Prácticas</a><a class="btn" href="autoevaluacion.html">Autoevaluación</a><a class="btn" href="formulario.html">Formulario</a></div></header>')

def pages_grid():
    out = '<section class="blk" id="paginas" style="--tc:var(--c1)"><div class="bhead"><div class="kick">Contenido</div><h1>Páginas de la guía</h1></div><div class="cardgrid">'
    for f, t, g, ids, c in PAGES:
        if f == 'index': continue
        out += f'<a class="tile" href="{f}.html" style="border-left:5px solid var(--{c})"><span>{esc(g)}</span><b>{esc(t)}</b></a>'
    for href, lab, tp in (('guia-completa.html', 'Guía completa en una sola página', 'Todo junto'), ('pdf.html', 'Descargas en PDF', 'PDF')):
        out += f'<a class="tile" href="{href}" style="border-left:5px solid var(--c7)"><span>{tp}</span><b>{lab}</b></a>'
    return out + '</div></section>'

def stats_list():
    nex = len(EXAMS); nej = len(EJ_EX); nho = len(EJ_HO)
    return [('14', 'temas (T0–T13)'), (str(nej), 'problemas de examen resueltos'), (str(nho), 'problemas de hojas resueltos'), (str(len(CHK)), 'comprobaciones por código')]

def page(title, side, main, assets_inline=None, multipage=False, extra_head='', cur=None, pre=''):
    if assets_inline:
        css = assets_inline['css']; jsa = f'<script>{assets_inline["sims"]}</script><script>{assets_inline["app"]}</script>'; head = f'<style>{css}</style>'
    else:
        head = '<link rel="stylesheet" href="assets/app.css">'; jsa = '<script src="assets/sims.js"></script><script src="assets/app.js"></script>'
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="Guía de estudio completa de Electrónica Digital (3.º Ingeniería Biomédica, UPCT): teoría, exámenes resueltos, prácticas con VHDL, simuladores y autoevaluación.">
<meta name="theme-color" content="#2457d6">{extra_head}{head}</head>
<body>
<div class="hubbar"><a href="{HUB}">← Todas las guías GIEyA</a></div>
<header class="top"><button class="btn hamb" id="hamb" aria-label="Menú">☰</button>
<div class="brand">Electrónica Digital <small>Actualizada el {FECHA}</small></div>
<button class="btn" id="expand" type="button">Desplegar todo</button><button class="btn" id="theme" type="button" aria-label="Cambiar tema">◐</button></header>
<div class="shell"><nav class="side" aria-label="Índice">{side}</nav><main><div class="page">{pre}{main}
<div class="foot">Guía no oficial de Electrónica Digital (UPCT) · Última actualización: {FECHA}. Los resultados numéricos y las ecuaciones se han comprobado con código.</div></div></main></div>
{jsa}</body></html>"""

def xref_fix(h, page_file, idmap):
    def rep(m):
        t = m.group(1)
        tgt = idmap.get(t)
        if tgt and tgt != page_file: return f'href="{tgt}.html#{t}"'
        return m.group(0)
    return re.sub(r'href="#([^"]+)"', rep, h)

def build():
    htmls = {}
    for b in BLOCKS: htmls[b['id']] = block_html(b)
    render_math_all()
    for k in htmls: htmls[k] = finalize_math(htmls[k])
    css = open(os.path.join(ROOT, 'web', 'style.css')).read() + '\n' + katex_css()
    app = open(os.path.join(ROOT, 'web', 'app.js')).read(); sims = open(os.path.join(ROOT, 'web', 'sims.js')).read() + '\n' + open(os.path.join(ROOT, 'web', 'sims2.js')).read()
    inl = {'css': css, 'app': app, 'sims': sims}
    main = hero(stats_list()) + ''.join(htmls[b['id']] for b in BLOCKS)
    master = page(TITLE, side_html(), main, inl)
    p = os.path.join(OUT, 'guia-electronica-digital.html'); open(p, 'w', encoding='utf-8').write(master)
    print('maestro', round(len(master) / 1024), 'KB')
    if '--site' in sys.argv:
        site = os.path.join(ROOT, 'site'); shutil.rmtree(site, ignore_errors=True); os.makedirs(site + '/assets')
        open(site + '/assets/app.css', 'w').write(css); open(site + '/assets/app.js', 'w').write(app); open(site + '/assets/sims.js', 'w').write(sims)
        idmap = {}
        for bid, h in htmls.items():
            for m in re.finditer(r'\sid="([^"]+)"', h): idmap.setdefault(m.group(1), B2P[bid])
        idx = []
        extra = ('<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="assets/icon-192.png"><link rel="apple-touch-icon" href="assets/icon-192.png">'
                 '<script>window.SEARCH_URL="search.json";window.SW_URL="sw.js";</script>')
        for k, (f, t, g, ids, c) in enumerate(PAGES):
            main1 = ''.join(htmls[x] for x in ids)
            pre = hero(stats_list()) if f == 'index' else ''
            if f == 'index': main1 = pages_grid() + main1
            prev = PAGES[k - 1] if k else None; nxt = PAGES[k + 1] if k + 1 < len(PAGES) else None
            nav = '<nav class="pager cardgrid">' + (f'<a class="tile" href="{prev[0]}.html"><span>← Anterior</span><b>{esc(prev[1])}</b></a>' if prev else '') + (f'<a class="tile" href="{nxt[0]}.html"><span>Siguiente →</span><b>{esc(nxt[1])}</b></a>' if nxt else '') + '</nav>'
            full = xref_fix(main1 + nav, f, idmap)
            open(f'{site}/{f}.html', 'w', encoding='utf-8').write(page(f'{t} · Electrónica Digital', side_html(f, True), full, None, True, extra, f, pre))
            for x in ids:
                txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', htmls[x], flags=re.S)); txt = re.sub(r'\s+', ' ', html.unescape(txt))
                idx.append({'p': f + '.html', 'id': x, 't': BID[x]['title'], 'x': txt})
                for m in re.finditer(r'<article class="ej" id="([^"]+)".*?<h4>(.*?)</h4>(.*?)</article>', htmls[x], flags=re.S):
                    t2 = re.sub(r'<[^>]+>', '', m.group(2)); x2 = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(3))))
                    idx.append({'p': f + '.html', 'id': m.group(1), 't': html.unescape(t2), 'b': BID[x]['title'], 'x': x2})
        # guía completa (una sola página) y página de PDF
        open(site + '/guia-completa.html', 'w', encoding='utf-8').write(master.replace('<div class="hubbar">', '<div class="hubbar">'))
        pdfs = [('guia-navegable.pdf', 'Guía completa (PDF navegable, cualquier visor)'), ('guia-acrobat.pdf', 'Guía completa con botones de mostrar/ocultar solución (Adobe Acrobat)'),
                ('examenes-resueltos.pdf', 'Exámenes resueltos paso a paso'), ('hojas-resueltas.pdf', 'Hojas de problemas resueltas'), ('formulario.pdf', 'Formulario en una página')]
        lst = ''.join(f'<a class="tile" href="{a}"><span>PDF</span><b>{b}</b></a>' for a, b in pdfs)
        pdfhtml = f'<section class="blk" id="pdf" style="--tc:var(--c7)"><div class="bhead"><div class="kick">Descargas</div><h1>Descargas en PDF</h1></div><div class="cardgrid">{lst}</div></section>'
        open(site + '/pdf.html', 'w', encoding='utf-8').write(page('Descargas en PDF · Electrónica Digital', side_html('pdf', True), pdfhtml, None, True, extra, 'pdf'))
        open(site + '/README.md', 'w', encoding='utf-8').write(f'# Electrónica Digital · Guía para aprobar\n\nGuía de estudio interactiva de Electrónica Digital (UPCT, Grado en Ingeniería Biomédica, 3.º).\n\nÚltima actualización: {FECHA}.\n\nÁbrela en: https://helionacon-ui.github.io/Electr-nica-digital/\n\nEstá dividida en páginas: portada, el examen y cómo estudiar, una página por bloque de temas, prácticas con simulador, exámenes resueltos paso a paso, hojas de problemas, demostraciones, autoevaluación, simulacros, formulario, glosario y plan de estudio. `guia-completa.html` es la misma guía en una sola página. Se puede instalar como aplicación y funciona sin conexión después de abrirla una vez.\n\n## Descargas en PDF\n\n' + '\n'.join(f'- [{b}]({a})' for a, b in pdfs) + '\n\n## Código\n\n- `scripts/vhdl/`: código VHDL de las prácticas.\n- `scripts/python/`: modelos en Python que reproducen cada práctica y sus salidas (`scripts/salidas/`).\n- `fuente/`: fuentes de la guía y herramientas para reconstruirla (`python3 fuente/tools/build.py --site`).\n')
        open(site + '/.nojekyll', 'w').write('')
        json.dump(idx, open(site + '/search.json', 'w', encoding='utf-8'), ensure_ascii=False)
        manifest = {'name': 'Electrónica Digital · Guía para aprobar', 'short_name': 'Electrónica Digital', 'description': 'Guía de estudio de Electrónica Digital (UPCT): teoría, simuladores, exámenes y prácticas resueltas.',
                    'start_url': './index.html', 'scope': './', 'display': 'standalone', 'background_color': '#12151c', 'theme_color': '#2457d6', 'lang': 'es',
                    'icons': [{'src': 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}]}
        json.dump(manifest, open(site + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)
        files = ['./', 'search.json', 'manifest.webmanifest', 'assets/app.css', 'assets/app.js', 'assets/sims.js', 'assets/icon-192.png', 'pdf.html', 'guia-completa.html'] + [p[0] + '.html' for p in PAGES]
        sw = f"""const V="ed-{NOW.strftime('%Y%m%d%H%M')}";const F={json.dumps(files)};
self.addEventListener("install",e=>{{e.waitUntil(caches.open(V).then(c=>Promise.all(F.map(u=>c.add(u).catch(()=>{{}})))).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{if(e.request.method!=="GET")return;e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}}).catch(()=>caches.match(e.request,{{ignoreSearch:true}})))}});"""
        open(site + '/sw.js', 'w').write(sw)
        from PIL import Image, ImageDraw, ImageFont
        for s in (192, 512):
            im = Image.new('RGB', (s, s), '#2457d6'); d = ImageDraw.Draw(im)
            try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(s * 0.36))
            except Exception: f = ImageFont.load_default()
            d.rounded_rectangle([s*0.12, s*0.12, s*0.88, s*0.88], radius=int(s*0.16), outline='white', width=max(3, s//40))
            w = d.textlength('ED', font=f); d.text(((s - w) / 2, s * 0.3), 'ED', fill='white', font=f)
            im.save(f'{site}/assets/icon-{s}.png')
        print('web multipágina:', len(PAGES) + 2, 'páginas en', site)
    json.dump({'blocks': [b['id'] for b in BLOCKS], 'math': len(MATH)}, open(os.path.join(OUT, 'build_info.json'), 'w'))

if __name__ == '__main__': build()
