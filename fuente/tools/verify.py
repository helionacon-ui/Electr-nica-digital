import asyncio, glob, os, json, sys
from playwright.async_api import async_playwright
SITE = '/home/claude/guia/site'; SH = '/home/claude/guia/shots'
async def main():
    pages = sorted(os.path.basename(f) for f in glob.glob(SITE + '/*.html'))
    errs = {}; overflow = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp, scale in (('d', {'width': 1280, 'height': 900}, 1), ('m', {'width': 390, 'height': 844}, 2)):
            ctx = await b.new_context(viewport=vp, device_scale_factor=scale)
            for pg in pages:
                page = await ctx.new_page(); msgs = []
                page.on('console', lambda m, msgs=msgs: msgs.append(m.text) if m.type == 'error' else None)
                page.on('pageerror', lambda e, msgs=msgs: msgs.append(str(e)))
                await page.goto('file://' + SITE + '/' + pg); await page.wait_for_timeout(500)
                w = await page.evaluate('[document.documentElement.scrollWidth, document.documentElement.clientWidth]')
                if w[0] > w[1] + 1: overflow[f'{name}:{pg}'] = w
                if pg in ('index.html', 'examenes.html', 'laboratorio.html', 'autoevaluacion.html', 'tema-4-5.html', 'formulario.html'):
                    await page.screenshot(path=f'{SH}/{name}-{pg[:-5]}.png', full_page=False)
                if msgs: errs[f'{name}:{pg}'] = msgs[:5]
                await page.close()
            await ctx.close()
        await b.close()
    print('erroresconsola', json.dumps(errs, ensure_ascii=False)[:1500]); print('desbordes', overflow)
asyncio.run(main())
