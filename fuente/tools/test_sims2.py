from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('file:///home/claude/guia/out/guia-electronica-digital.html');pg.wait_for_timeout(800)
    def sim(n): return pg.locator(f'.sim[data-sim="{n}"]').first
    def out(n): return sim(n).locator('.out').first.inner_text()
    # truth
    s=sim('truth');s.scroll_into_view_if_needed();print('TRUTH',out('truth')[:300].replace('\n',' | '))
    s.locator('#tx1').fill("A^B^C");print('XOR3',out('truth')[:200].replace('\n',' | '))
    s.locator('#tx1').fill("A+B*C");s.locator('#tx2').fill("(A+B)(A+C)");print('dist',out('truth')[-90:].replace('\n',' | '))
    s.locator('#tx2').fill("(A+B)C");print('noeq',out('truth')[-90:].replace('\n',' | '))
    s.locator('#tx1').fill("A+");print('err',out('truth'))
    # ovf
    s=sim('ovf');print('OVF',out('ovf').replace('\n',' | ')[-200:])
    s.locator('#ova').fill('-100');s.locator('#ovb').fill('-50');print('OVF2',out('ovf').replace('\n',' | ')[-160:])
    s.locator('#ova').fill('-20');s.locator('#ovb').fill('30');print('OVF3',out('ovf').replace('\n',' | ')[-120:])
    # msi
    s=sim('msi');print('MUX',out('msi').replace('\n',' | ')[:120])
    for v in ['dec','cmp','add']:
        s.locator('#msis').select_option(v);print(v.upper(),out('msi').replace('\n',' | ')[-230:])
    # shreg
    s=sim('shreg')
    for k in ['shift','anillo','johnson','lfsr']:
        s.locator('#srt').select_option(k)
        for i in range(16): s.get_by_text('Pulso de reloj').click()
        print(k,out('shreg').replace('\n',' | ')[-200:])
    # fsmdet
    s=sim('fsmdet')
    for x in '1011011': s.get_by_text('Enviar '+x).click()
    print('FSM',out('fsmdet').replace('\n',' | '))
    # compara con el algoritmo: solapamiento
    s.locator('#fdo').uncheck();s.locator('#fds').select_option('101')
    for x in '10101': s.get_by_text('Enviar '+x).click()
    print('FSM101 sin solap',out('fsmdet').replace('\n',' | '))
    s.locator('#fdo').check()
    for x in '10101': s.get_by_text('Enviar '+x).click()
    print('FSM101 solap',out('fsmdet').replace('\n',' | '))
    # mem
    s=sim('mem');s.get_by_text('Escribir').click();s.locator('#mea').fill('5');s.locator('#med').fill('9');s.get_by_text('Escribir').click();s.get_by_text('Leer').click();print('MEM',out('mem').split('\n')[0],'|',sim('mem').locator('.out').nth(1).inner_text().replace('\n',' | '))
    # divf
    s=sim('divf');print('DIVF',out('divf').replace('\n',' | '),'||',sim('divf').locator('.out').nth(1).inner_text().replace('\n',' | '))
    # lut
    s=sim('lut');print('LUT',out('lut').replace('\n',' | ')[:260])
    s.locator('#lup').select_option('maj');print('LUTmaj',out('lut').replace('\n',' | ')[:200])
    s.locator('#lup').select_option('bcd');print('LUTbcd',out('lut').replace('\n',' | ')[:200])
    ov=pg.evaluate('document.documentElement.scrollWidth')
    print('scrollW',ov,'errs',errs[:5])
    pg.screenshot(path='shots/sims2.png')
    b.close()
