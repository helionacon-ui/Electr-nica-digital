"""Mini-DSL de la guía -> árbol -> HTML. Formato de texto propio (ver README en src/)."""
import re, json, html, subprocess, os, hashlib, sys
sys.path.insert(0, os.path.dirname(__file__))

def esc(s): return html.escape(s, quote=False)

class Node:
    def __init__(self, kind, **kw): self.kind = kind; self.__dict__.update(kw)
    def __repr__(self): return f'<{self.kind} {getattr(self, "title", "")}>'

# ------------------------------------------------------------------ parser
BLOCK_OPEN = ('@box', '@ej', '@enun', '@antes', '@paso', '@res', '@code', '@details', '@q', '@enlace', '@nota', '@sol')
def parse(text, fname='?'):
    lines = text.split('\n')
    pos = [0]
    def parse_seq(stop_at_end):
        nodes = []; para = []
        def flush():
            nonlocal para
            if para: nodes.append(Node('para', text=' '.join(x.strip() for x in para))); para = []
        while pos[0] < len(lines):
            ln = lines[pos[0]]; s = ln.strip()
            if s.startswith('#') and not s.startswith('#!') and s.split(' ')[0] in ('#', '##', '###', '####') and not s.startswith('# #'):
                if s.startswith('# ') and ln.startswith('# ') and fname.endswith('.dsl') and False: pass
            if s.startswith('//'): pos[0] += 1; continue            # comentario
            if s == '@end':
                flush()
                if stop_at_end: pos[0] += 1; return nodes
                raise SyntaxError(f'{fname}:{pos[0]+1}: @end sin abrir')
            if s == '':
                flush(); pos[0] += 1; continue
            m = re.match(r'^(#{2,4}) (.*)$', s)
            if m: flush(); nodes.append(Node('h', level=len(m.group(1)), text=m.group(2))); pos[0] += 1; continue
            if s.startswith('$$'):
                flush(); buf = []
                first = s[2:]
                if first.endswith('$$') and len(first) > 2:
                    nodes.append(Node('dmath', text=first[:-2].strip())); pos[0] += 1; continue
                if first: buf.append(first)
                pos[0] += 1
                while pos[0] < len(lines) and not lines[pos[0]].strip().endswith('$$'):
                    buf.append(lines[pos[0]]); pos[0] += 1
                last = lines[pos[0]].strip()[:-2]
                if last: buf.append(last)
                pos[0] += 1
                nodes.append(Node('dmath', text='\n'.join(buf).strip())); continue
            if s.startswith('```'):
                flush(); lang = s[3:].strip(); buf = []; pos[0] += 1
                while not lines[pos[0]].strip().startswith('```'): buf.append(lines[pos[0]]); pos[0] += 1
                pos[0] += 1; nodes.append(Node('pre', lang=lang, text='\n'.join(buf))); continue
            if s.startswith('|'):
                flush(); rows = []
                while pos[0] < len(lines) and lines[pos[0]].strip().startswith('|'):
                    rows.append([c.strip() for c in lines[pos[0]].strip().strip('|').split('|')]); pos[0] += 1
                nodes.append(Node('table', rows=rows)); continue
            if re.match(r'^(- |\d+\. )', s) :
                flush(); items = []; ordered = bool(re.match(r'^\d+\. ', s))
                while pos[0] < len(lines) and re.match(r'^(- |\d+\. )', lines[pos[0]].strip()):
                    t = re.sub(r'^(- |\d+\. )', '', lines[pos[0]].strip()); pos[0] += 1
                    while pos[0] < len(lines) and lines[pos[0]].startswith('  ') and lines[pos[0]].strip() and not re.match(r'^(- |\d+\. )', lines[pos[0]].strip()):
                        t += ' ' + lines[pos[0]].strip(); pos[0] += 1
                    items.append(t)
                nodes.append(Node('list', items=items, ordered=ordered)); continue
            if s.startswith('@'):
                flush()
                m = re.match(r'^@(\w+)\s*(.*)$', s); d, arg = m.group(1), m.group(2)
                pos[0] += 1
                if '@' + d in BLOCK_OPEN or d in ('endej',):
                    if d == 'q':
                        buf = []
                        while lines[pos[0]].strip() != '@end': buf.append(lines[pos[0]]); pos[0] += 1
                        pos[0] += 1
                        nodes.append(Node('q', arg=arg, raw=buf)); continue
                    if d == 'code':
                        buf = []
                        while lines[pos[0]].strip() != '@end': buf.append(lines[pos[0]]); pos[0] += 1
                        pos[0] += 1
                        parts = [p.strip() for p in arg.split('|')]
                        nodes.append(Node('code', lang=parts[0], title=parts[1] if len(parts) > 1 else '', text='\n'.join(buf))); continue
                    children = parse_seq(True)
                    nodes.append(Node(d, arg=arg, children=children)); continue
                if d == 'codefile':
                    parts = [p.strip() for p in arg.split('|')]
                    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', parts[2])
                    nodes.append(Node('code', lang=parts[0], title=parts[1], text=open(path, encoding='utf-8').read().rstrip('\n'), sim=parts[3] if len(parts) > 3 else '')); continue
                if d == 'fig': nodes.append(Node('fig', arg=arg)); continue
                if d == 'sim': nodes.append(Node('sim', arg=arg)); continue
                if d == 'card': nodes.append(Node('card', arg=arg)); continue
                if d == 'gloss': nodes.append(Node('gloss', arg=arg)); continue
                if d == 'hr': nodes.append(Node('hr')); continue
                if d == 'auto': nodes.append(Node('auto', arg=arg)); continue
                raise SyntaxError(f'{fname}:{pos[0]}: directiva desconocida @{d}')
            para.append(ln); pos[0] += 1
        flush()
        if stop_at_end: raise SyntaxError(f'{fname}: falta @end')
        return nodes
    return parse_seq(False)

# ------------------------------------------------------------------ matemáticas (KaTeX en build)
MATH = {}   # latex -> (display: bool)
def collect_math(s):
    out = []
    def rep(m):
        MATH.setdefault((m.group(1), False), None); out.append(m.group(1)); return '\x00M' + str(len(out) - 1) + '\x00'
    return re.sub(r'(?<!\\)\$((?:[^$\\]|\\.)+?)\$', rep, s), out

def render_math_all(katex_dir='/opt/npm-tools/node_modules/katex'):
    keys = [k for k, v in MATH.items() if v is None]
    if not keys: return
    cache_f = os.path.join(os.path.dirname(__file__), '..', 'out', 'math_cache.json')
    cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    todo = [k for k in keys if f'{int(k[1])}:{k[0]}' not in cache]
    if todo:
        job = [{'t': k[0], 'd': k[1]} for k in todo]
        p = subprocess.run(['node', '-e', f'''
const katex=require("{katex_dir}");
const job=JSON.parse(require("fs").readFileSync(0,"utf8"));
const out=job.map(j=>{{try{{return katex.renderToString(j.t,{{displayMode:j.d,throwOnError:true,strict:"ignore",trust:false,output:"html"}})}}catch(e){{return "ERR:"+e.message}}}});
process.stdout.write(JSON.stringify(out));'''], input=json.dumps(job), capture_output=True, text=True)
        if p.returncode: raise RuntimeError(p.stderr)
        res = json.loads(p.stdout)
        for k, r in zip(todo, res):
            if r.startswith('ERR:'): raise ValueError(f'KaTeX falló en «{k[0]}»: {r}')
            cache[f'{int(k[1])}:{k[0]}'] = r
        json.dump(cache, open(cache_f, 'w'))
    for k in keys: MATH[k] = cache[f'{int(k[1])}:{k[0]}']

class Ctx:
    R = {}          # resultados {clave: valor}
    refs = {}       # id -> (page, titulo)
    figs = None     # callable(name, args)->svg
    auto = None     # callable(name)->html

def subst(s):
    def rep(m):
        k = m.group(1).strip()
        if k not in Ctx.R: raise KeyError(f'clave desconocida {{{{{k}}}}}')
        v = Ctx.R[k]
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return re.sub(r'\{\{([^}]+)\}\}', rep, s)

def inline(s):
    s = subst(s)
    s, maths = collect_math(s)
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    def ref(m):
        rid, txt = m.group(1), m.group(2)
        return f'<a class="xref" data-ref="{rid}" href="#{rid}">{txt or rid}</a>'
    s = re.sub(r'\[\[([\w.\-]+)(?:\|([^\]]+))?\]\]', ref, s)
    s = re.sub(r'\x00M(\d+)\x00', lambda m: '\x01' + json.dumps([maths[int(m.group(1))], False]) + '\x02', s)
    return s

def finalize_math(s):
    def rep(m):
        t, d = json.loads(m.group(1)); return MATH[(t, d)]
    return re.sub(r'\x01(.*?)\x02', rep, s)

def dmath(t):
    MATH.setdefault((subst(t), True), None)
    return '\x01' + json.dumps([subst(t), True]) + '\x02'

# ------------------------------------------------------------------ render
BOXES = {'idea': ('💡', 'La idea'), 'ojo': ('⚠️', 'Ojo'), 'falla': ('🚧', 'Qué suele fallar'), 'mas': ('🔭', 'Más a fondo'),
         'formula': ('∑', 'Fórmulas clave'), 'def': ('📘', 'Definición'), 'ej': ('✏️', 'Ejemplo'), 'erra': ('🛠️', 'Errata')}

class Counter:
    n = 0
def uid(p='x'): Counter.n += 1; return f'{p}{Counter.n}'

def render(nodes, ctx_ej=None):
    out = []
    for n in nodes:
        k = n.kind
        if k == 'para': out.append(f'<p>{inline(n.text)}</p>')
        elif k == 'h':
            lvl = n.level; hid = uid('h'); out.append(f'<h{lvl} id="{hid}">{inline(n.text)}</h{lvl}>')
        elif k == 'dmath':
            parts = [x.strip() for x in re.split(r'\\qquad', n.text) if x.strip()]
            if len(parts) > 1: out.append('<div class="dmrow">' + ''.join(f'<div class="dmath">{dmath(x)}</div>' for x in parts) + '</div>')
            else: out.append(f'<div class="dmath">{dmath(n.text)}</div>')
        elif k == 'pre': out.append(f'<pre class="code"><code>{esc(n.text)}</code></pre>')
        elif k == 'code':
            fn = n.title; head = f'<div class="codehead"><span>{esc(n.lang)}{" · " + esc(fn) if fn else ""}</span></div>' if (n.lang or fn) else ''
            sm = getattr(n, 'sim', '')
            btn = f'<a class="btn simgo" href="#sim-prac" data-simsel="{esc(sm)}">Abrir en el simulador</a>' if sm else ''
            out.append(f'<div class="codeblock">{head}<pre class="code"><code>{esc(n.text)}</code></pre>{btn}</div>')
        elif k == 'list':
            tag = 'ol' if n.ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(i)}</li>' for i in n.items) + f'</{tag}>')
        elif k == 'table':
            rows = n.rows; h = rows[0]
            t = '<div class="tw"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in h) + '</tr></thead><tbody>'
            for r in rows[1:]:
                if all(re.match(r'^:?-+:?$', c) for c in r): continue
                t += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
            out.append(t + '</tbody></table></div>')
        elif k == 'box':
            parts = [p.strip() for p in n.arg.split('|')]; typ = parts[0]; ttl = parts[1] if len(parts) > 1 else BOXES[typ][1]
            out.append(f'<aside class="box {typ}"><div class="boxh"><span class="ic">{BOXES[typ][0]}</span> {inline(ttl)}</div>{render(n.children)}</aside>')
        elif k == 'details':
            out.append(f'<details class="det"><summary>{inline(n.arg)}</summary>{render(n.children)}</details>')
        elif k == 'fig':
            name, _, js = n.arg.partition(' ')
            args = json.loads(js) if js.strip() else {}
            cap = args.pop('cap', '')
            svg = Ctx.figs(name, args)
            out.append(f'<figure class="figure">{svg}' + (f'<figcaption>{inline(cap)}</figcaption>' if cap else '') + '</figure>')
        elif k == 'sim': out.append(f'<div class="sim" data-sim="{esc(n.arg.strip())}"><noscript>Este simulador necesita JavaScript.</noscript></div>')
        elif k == 'hr': out.append('<hr>')
        elif k == 'auto': out.append(Ctx.auto(n.arg.strip()))
        elif k == 'ej': out.append(render_ej(n))
        elif k == 'card':
            f, _, b = n.arg.partition('||')
            out.append(f'<div class="card" tabindex="0"><div class="cf">{inline(f.strip())}</div><div class="cb">{inline(b.strip())}</div></div>')
        elif k == 'q': out.append(render_q(n))
        elif k == 'gloss':
            t, _, d = n.arg.partition('|'); out.append(f'<dl class="gl"><dt>{inline(t.strip())}</dt><dd>{inline(d.strip())}</dd></dl>')
        else: raise ValueError('nodo no renderizable ' + k)
    return '\n'.join(out)

def meta_ej(n):
    p = [x.strip() for x in n.arg.split('|')]
    d = {'id': p[0], 'title': p[1], 'origen': p[2] if len(p) > 2 else '', 'tags': [t.strip() for t in p[3].split(',')] if len(p) > 3 else [],
         'checks': [t.strip() for t in p[4].split(',')] if len(p) > 4 and p[4] else []}
    return d

def render_ej(n):
    m = meta_ej(n); enun = antes = res = None; pasos = []
    for c in n.children:
        if c.kind == 'enun': enun = c
        elif c.kind == 'antes': antes = c
        elif c.kind == 'res': res = c
        else: pasos.append(c)
    assert enun and res, f'ej {m["id"]} incompleto'
    tags = ' '.join(m['tags'])
    h = f'<article class="ej" id="{m["id"]}" data-tags="{esc(tags)}" data-origen="{esc(m["origen"])}">'
    h += f'<header class="ejh"><span class="ejid">{esc(m["origen"])}</span><h4>{inline(m["title"])}</h4>'
    if m['checks']: h += '<span class="badge ok" title="Resultados comprobados con código">✔ verificado</span>'
    h += '</header>'
    h += f'<div class="enun">{render(enun.children)}</div>'
    if antes: h += f'<aside class="box antes"><div class="boxh"><span class="ic">🧭</span> Antes de empezar: qué piden y qué teoría usas</div>{render(antes.children)}</aside>'
    i = 0
    for p in pasos:
        if p.kind != 'paso': h += render([p]); continue
        i += 1
        h += f'<details class="paso"><summary><span class="pn">{i}</span> {inline(p.arg)}</summary><div class="pbody">{render(p.children)}</div></details>'
    h += f'<details class="res"><summary>✅ Resultado final</summary><div class="pbody">{render(res.children)}</div></details>'
    return h + '</article>'

import random
def render_q(n):
    stem = []; opts = []; expl = []
    for ln in n.raw:
        t = ln.strip()
        if not t: continue
        if t.startswith('+ '): opts.append((True, t[2:]))
        elif t.startswith('- '): opts.append((False, t[2:]))
        elif t.startswith('> '): expl.append(t[2:])
        else: stem.append(t)
    rnd = random.Random(hashlib.md5(' '.join(stem).encode()).hexdigest()); rnd.shuffle(opts)
    tag = n.arg.strip()
    h = f'<div class="quiz" data-tag="{esc(tag)}"><div class="qs">{inline(" ".join(stem))}</div><div class="qo">'
    for i, (ok, t) in enumerate(opts):
        h += f'<button type="button" class="opt" data-ok="{int(ok)}"><span class="ol">{"ABCDEFG"[i]}</span><span>{inline(t)}</span></button>'
    h += f'</div><div class="qx" hidden>{inline(" ".join(expl))}</div></div>'
    return h

def collect_ejs(nodes, acc):
    for n in nodes:
        if n.kind == 'ej': acc.append(meta_ej(n))
        if hasattr(n, 'children'): collect_ejs(n.children, acc)
    return acc
