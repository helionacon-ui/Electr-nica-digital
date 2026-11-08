#!/usr/bin/env python3
"""Genera los PDF a partir del sitio ya construido (site/). Uso: python3 make_pdfs.py"""
import asyncio, os, re, base64, sys, subprocess
from playwright.async_api import async_playwright
import pikepdf
from pikepdf import Name, Dictionary, Array, String
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = ROOT + '/site'; TMP = ROOT + '/out/pdf'
os.makedirs(TMP, exist_ok=True)
PORT = 8765
MARG = dict(top='16mm', bottom='16mm', left='14mm', right='14mm')
FOOT = '<div style="font-size:8px;width:100%;text-align:center;color:#666;font-family:sans-serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
PRINT_CSS = '''
@media print{ .hubbar,.top,.side,.hamb,.search,#exq,.chips,.simgo,.pager,.btn,#resetq{display:none!important}
 html,body{background:#fff!important} body{font-size:10.5pt} .shell{display:block!important} main{max-width:none!important;padding:0!important;margin:0!important}
 section.blk{break-before:page} h1,h2,h3,h4{break-after:avoid} pre.code{white-space:pre-wrap;word-break:break-word;font-size:8.5pt}
 details>summary{list-style:none} .exgroup>summary{font-size:1.05rem}
 .sim img.shot{max-width:100%;height:auto;border:1px solid #ccc;border-radius:6px}
 .solbar{margin:10px 0 4px;padding:5px 8px;border:1px solid #9aa;border-radius:6px;background:#eef2f7;font-weight:600;font-size:10pt;break-inside:avoid}
 .solbar .bt{display:inline-block;width:150px;height:16px;vertical-align:middle;margin-left:10px;font-size:1px;color:#eef2f7}
 .card{min-height:0!important;break-inside:avoid} .card .cf,.card .cb{position:static!important;transform:none!important;backface-visibility:visible!important;display:block!important;text-align:left!important;border:0!important;padding:2px 0!important;background:none!important;overflow:visible!important} .card .cf{font-weight:600} .card{border:1px solid #ccc;border-radius:8px;padding:6px 10px}
 .mk{font-size:2px;line-height:2px;color:#fff}
 .ej{break-inside:auto} .ej .enun,.ej aside.antes{break-inside:avoid}
}'''

async def prepare(page, mode, sims=True):
    """mode: 'plain' (todo abierto) | 'acro' (marcadores para ocultar soluciones)"""
    await page.add_style_tag(content=PRINT_CSS)
    await page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    await page.evaluate('''()=>{document.querySelectorAll('.quiz .opt[data-ok="1"]').forEach(o=>o.classList.add('good'));document.querySelectorAll('.quiz .qx').forEach(x=>x.hidden=false);
      const f=document.querySelector('section.blk'); if(f) f.style.breakBefore='auto'}''')
    if sims:
        els = await page.query_selector_all('.sim')
        for i, el in enumerate(els):
            try:
                await el.scroll_into_view_if_needed(); await page.wait_for_timeout(250); png = await el.screenshot()
                uri = 'data:image/png;base64,' + base64.b64encode(png).decode()
                await el.evaluate("(e,u)=>{e.innerHTML='<img class=\"shot\" src=\"'+u+'\" alt=\"Captura del simulador\"><p class=\"small\">Captura del simulador interactivo. Pruébalo en la versión web.</p>'}", uri)
            except Exception as ex: print('sim sin captura', i, ex)
    if mode == 'acro':
        n = await page.evaluate('''()=>{
          let n=0;
          const mk=(t)=>{const s=document.createElement('span');s.className='mk';s.textContent=t;return s};
          document.querySelectorAll('article.ej').forEach(a=>{
            const first=[...a.children].find(c=>c.matches('details.paso,details.res,aside.box:not(.antes),figure'));
            if(!first)return; n++;
            const bar=document.createElement('div');bar.className='solbar';
            bar.append('Solución paso a paso');const bt=document.createElement('span');bt.className='bt';bt.textContent='@@B'+n+'@@';bar.append(bt);
            a.insertBefore(bar,first); bar.after(mk('@@S'+n+'@@')); a.append(mk('@@E'+n+'@@'));
          });
          document.querySelectorAll('details.det').forEach(d=>{
            const s=d.querySelector('summary'); if(!s||!/^Ver la soluci/.test(s.textContent))return; n++;
            const bt=document.createElement('span');bt.className='bt';bt.textContent='@@B'+n+'@@';s.append(bt);
            const st=mk('@@S'+n+'@@'); s.after(st); d.append(mk('@@E'+n+'@@'));
            s.style.fontWeight='600';
          });
          return n}''')
        return n
    return 0

async def render(pw_browser, url, out, mode='plain', title=None, extra_css='', hide=None, sims=True):
    ctx = await pw_browser.new_context(viewport={'width': 1000, 'height': 900})
    page = await ctx.new_page(); await page.goto(url); await page.wait_for_timeout(800)
    if hide: await page.evaluate("(sel)=>document.querySelectorAll(sel).forEach(e=>e.remove())", hide)
    if extra_css: await page.add_style_tag(content=extra_css)
    n = await prepare(page, mode, sims)
    await page.wait_for_timeout(300)
    await page.pdf(path=out, format='A4', margin=MARG, print_background=True, display_header_footer=True,
                   header_template='<span></span>', footer_template=FOOT, outline=True, tagged=True, prefer_css_page_size=False)
    await ctx.close(); return n

def add_acrobat(src, dst, n):
    """Cubre cada solución con un campo blanco y añade un botón que lo muestra/oculta (JavaScript de Acrobat)."""
    pdf = pikepdf.open(src); found = {}
    subprocess.run(['pdftotext', '-bbox', src, TMP + '/bb.html'], check=True)
    txt = open(TMP + '/bb.html', encoding='utf-8').read()
    sizes = []
    for pi, chunk in enumerate(txt.split('<page ')[1:]):
        m = re.match(r'width="([\d.]+)" height="([\d.]+)"', chunk); sizes.append((float(m.group(1)), float(m.group(2))))
        for w in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">@@([BSE])(\d+)@@</word>', chunk):
            x0, y0, x1, y1 = map(float, w.groups()[:4]); found.setdefault(int(w.group(6)), {})[w.group(5)] = (pi, {'x0': x0, 'top': y0, 'bottom': y1})
    mm = 72 / 25.4; L = 14 * mm - 3; top_m = 16 * mm; bot_m = 16 * mm
    fields = []; covers = {}
    def widget(page, rect, parent=None):
        w = Dictionary(Type=Name.Annot, Subtype=Name.Widget, Rect=Array(rect), F=4, P=page.obj)
        return pdf.make_indirect(w)
    for k in sorted(found):
        d = found[k]
        if not all(x in d for x in 'BSE'): print('marcas incompletas', k, list(d)); continue
        (pb, wb), (ps, ws), (pe, we) = d['B'], d['S'], d['E']
        # botón
        H = sizes[pb][1]
        cy = H - (wb['top'] + wb['bottom']) / 2; r = [wb['x0'] - 1, cy - 7, wb['x0'] + 112, cy + 7]
        btn = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Widget, FT=Name.Btn, Ff=65536, T=String(f'btn{k}'),
            Rect=Array(r), F=4, P=pdf.pages[pb].obj,
            MK=Dictionary(CA=String('Mostrar / ocultar'), BG=Array([0.87, 0.92, 1]), BC=Array([0.15, 0.35, 0.8])),
            A=Dictionary(S=Name.JavaScript, JS=String(f'var f=this.getField("cov{k}"); f.display=(f.display==display.hidden)?display.visible:display.hidden;')),
            DA=String('/Helv 9 Tf 0 g')))
        pdf.pages[pb].obj.Annots = pdf.pages[pb].obj.get('/Annots', Array()); pdf.pages[pb].obj.Annots.append(btn); fields.append(btn)
        kids = []
        for pi in range(ps, pe + 1):
            Hh = sizes[pi][1]; W = sizes[pi][0]
            y_top = (Hh - ws['top']) if pi == ps else (Hh - top_m)
            y_bot = (Hh - we['bottom']) if pi == pe else bot_m
            if y_top - y_bot < 2: continue
            wd = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Widget, Rect=Array([L, y_bot, W - L, y_top]), F=4, P=pdf.pages[pi].obj,
                  MK=Dictionary(BG=Array([1, 1, 1]), BC=Array([1, 1, 1]))))
            pdf.pages[pi].obj.Annots = pdf.pages[pi].obj.get('/Annots', Array()); pdf.pages[pi].obj.Annots.append(wd); kids.append(wd)
        par = pdf.make_indirect(Dictionary(FT=Name.Tx, T=String(f'cov{k}'), Ff=1, V=String(''), Kids=Array(kids)))
        for wd in kids: wd.Parent = par
        fields.append(par)
    js_all = lambda disp: ('for(var i=0;i<this.numFields;i++){var n=this.getNthFieldName(i); if(n.indexOf("cov")==0) this.getField(n).display=display.%s;}' % disp)
    # botones globales en la primera página (esquina superior derecha, sobre el margen)
    W0, H0 = sizes[0]
    for j, (cap, disp) in enumerate((('Mostrar todas las soluciones', 'hidden'), ('Ocultar todas las soluciones', 'visible'))):
        b = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Widget, FT=Name.Btn, Ff=65536, T=String(f'global{j}'),
            Rect=Array([L + j * 190, H0 - 14 * mm, L + j * 190 + 180, H0 - 8 * mm]), F=4, P=pdf.pages[0].obj,
            MK=Dictionary(CA=String(cap), BG=Array([0.87, 0.92, 1]), BC=Array([0.15, 0.35, 0.8])),
            A=Dictionary(S=Name.JavaScript, JS=String(js_all(disp))), DA=String('/Helv 9 Tf 0 g')))
        pdf.pages[0].obj.Annots = pdf.pages[0].obj.get('/Annots', Array()); pdf.pages[0].obj.Annots.append(b); fields.append(b)
    pdf.Root.AcroForm = Dictionary(Fields=Array(fields), NeedAppearances=True, DA=String('/Helv 0 Tf 0 g'),
                                   DR=Dictionary(Font=Dictionary(Helv=Dictionary(Type=Name.Font, Subtype=Name.Type1, BaseFont=Name.Helvetica, Encoding=Name.WinAnsiEncoding))))
    pdf.save(dst); return len(found)

async def main():
    which = sys.argv[1:] or ['nav', 'acro', 'exam', 'hojas', 'form']
    base = f'http://localhost:{PORT}/'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if 'nav' in which:
            await render(b, base + 'guia-completa.html', SITE + '/guia-navegable.pdf'); print('nav ok')
        if 'acro' in which:
            n = await render(b, base + 'guia-completa.html', TMP + '/acro_raw.pdf', mode='acro')
            k = add_acrobat(TMP + '/acro_raw.pdf', SITE + '/guia-acrobat.pdf', n); print('acro ok', n, k)
        if 'exam' in which:
            await render(b, base + 'examenes.html', SITE + '/examenes-resueltos.pdf'); print('exam ok')
        if 'hojas' in which:
            await render(b, base + 'hojas.html', SITE + '/hojas-resueltas.pdf'); print('hojas ok')
        if 'form' in which:
            ctx = await b.new_context(viewport={'width': 1000, 'height': 900}); page = await ctx.new_page()
            await page.goto(base + 'formulario.html'); await page.wait_for_timeout(600)
            await page.evaluate('''()=>{const sec=document.querySelector('#formulario1p'); const html=sec.innerHTML; const kicker=sec.querySelector('.bhead'); if(kicker)kicker.remove();
              const t=sec.querySelector('table'); const css=document.createElement('style');
              css.textContent='@media print{.foot,.hubbar,.top,.side,.hamb{display:none!important} body{background:#fff} main{padding:0!important} table{font-size:11pt;line-height:1.38} td,th{padding:6px 8px!important} h1{font-size:15pt;margin:0 0 6px}} @page{margin:9mm}';
              document.head.append(css); const wrap=document.createElement('div'); wrap.innerHTML='<h1>Electrónica Digital · Formulario de una página</h1>'; wrap.append(t.closest('.tw')||t);
              document.body.innerHTML=''; document.body.append(wrap); wrap.style.cssText='padding:0 4mm'}''')
            for sc in (1.0, .95, .9, .85, .8, .75, .7):
                await page.pdf(path=SITE + '/formulario.pdf', format='A4', margin=dict(top='9mm', bottom='9mm', left='9mm', right='9mm'), print_background=True, scale=sc, tagged=True)
                np_ = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', SITE + '/formulario.pdf'], capture_output=True, text=True).stdout).group(1))
                if np_ == 1: print('formulario 1 pagina, escala', sc); break
            await ctx.close()
        await b.close()
asyncio.run(main())
