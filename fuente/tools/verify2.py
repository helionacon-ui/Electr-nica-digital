import asyncio, glob, os
from playwright.async_api import async_playwright
SITE='/home/claude/guia/site'; SH='/home/claude/guia/shots'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':1280,'height':900}); 
        for pg in sorted(os.path.basename(f) for f in glob.glob(SITE+'/*.html')):
            page = await ctx.new_page(); errs=[]
            page.on('pageerror', lambda e: errs.append(str(e))); page.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
            await page.goto('file://'+SITE+'/'+pg); await page.wait_for_timeout(300)
            n = await page.evaluate('''()=>{let c=0;document.querySelectorAll('[class*=sim] button, [class*=sim] input, [class*=sim] select').forEach(e=>{try{ if(e.tagName==='BUTTON')e.click(); else if(e.type==='checkbox'||e.type==='radio')e.click(); else if(e.tagName==='SELECT'){e.selectedIndex=(e.selectedIndex+1)%e.options.length;e.dispatchEvent(new Event('change',{bubbles:true}))} else {e.dispatchEvent(new Event('input',{bubbles:true}))}; c++}catch(x){throw x}});return c}''')
            await page.wait_for_timeout(200)
            print(pg, 'controles sim pulsados:', n, 'errores:', errs[:3])
            await page.close()
        # quiz + tarjetas en autoevaluacion
        page = await ctx.new_page(); await page.goto('file://'+SITE+'/autoevaluacion.html')
        await page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        await page.click('.quiz .opt >> nth=0'); print('score:', await page.inner_text('#score'))
        await page.click('.card >> nth=0'); print('flip', await page.evaluate("document.querySelector('.card').classList.contains('flip')"))
        # busqueda global
        page2 = await ctx.new_page(); await page2.goto('file://'+SITE+'/index.html')
        await page2.fill('input[type=search]', 'caja fuerte'); await page2.wait_for_timeout(600)
        print('busqueda:', (await page2.evaluate("document.body.innerText"))[:0], await page2.evaluate("[...document.querySelectorAll('[class*=result] a, .sres a, #sr a')].length"))
        await page2.screenshot(path=SH+'/d-busqueda.png')
        await b.close()
asyncio.run(main())
