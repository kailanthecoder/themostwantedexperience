#!/usr/bin/env python3
"""Fah Mai v26 QA: one-row fixed nav, arrow hover contrast, and pricing split."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

URI=(Path(__file__).parent / "index.html").resolve().as_uri()
SIZES=[(320,568),(360,740),(390,844),(430,932),(540,700),(768,1024),(820,720),(1024,768),(1280,900),(1440,900)]

async def check(browser,w,h):
    page=await browser.new_page(viewport={"width":w,"height":h})
    errors=[]
    page.on("pageerror",lambda exc: errors.append(str(exc)))
    await page.goto(URI+"#budget",wait_until="domcontentloaded")
    await page.wait_for_timeout(420)
    state=await page.evaluate("""() => {
      const rect=e=>{const r=e.getBoundingClientRect();return {l:r.left,r:r.right,t:r.top,b:r.bottom,w:r.width,h:r.height}};
      const toolbar=document.querySelector('.toolbar');
      const switcher=document.querySelector('.view-switcher');
      const nav=document.querySelector('nav.proposal-sections');
      const pdf=document.querySelector('.pdf-btn');
      const left=document.querySelector('#budget .budgetv8-rate-tables table[data-cost-type="one-time"]');
      const right=document.querySelector('#budget .budgetv8-rate-tables table[data-cost-type="monthly"]');
      return {
        viewport:innerWidth, toolbar:rect(toolbar),switcher:rect(switcher),nav:rect(nav),pdf:rect(pdf),
        navScrollWidth:nav.scrollWidth,navClientWidth:nav.clientWidth,
        navbarStyle:getComputedStyle(toolbar).position,
        active:[...document.querySelectorAll('.viewport>.sheet.is-active')].map(e=>e.id),
        counter:document.querySelector('.fm-story-counter').textContent.trim(),
        oneoff:left?[...left.querySelectorAll('tbody tr')].map(r=>[...r.querySelectorAll('td')].map(c=>c.textContent.trim())):null,
        monthly:right?[...right.querySelectorAll('tbody tr')].map(r=>[...r.querySelectorAll('td')].map(c=>c.textContent.trim())):null,
        quote:[...document.querySelectorAll('#budget .budgetv8-comparison strong')].map(e=>e.textContent.trim())
      };
    }""")
    assert not errors,(w,h,errors)
    assert state['active']==['overview'],(w,h,'startup',state['active'])
    assert state['counter'].startswith('1 / '),(w,h,state['counter'])
    assert state['oneoff'] and state['monthly'],(w,h,'tables missing')
    assert len(state['oneoff'])==8 and len(state['monthly'])==8,(w,h,'row count')
    assert state['oneoff'][-1]==['Standard development total','£8,625'],(w,h,'development total')
    assert state['monthly'][-1]==['Standard monthly total','£600/mo'],(w,h,'monthly total')
    assert state['quote']==['£5,750','£400/mo'],(w,h,'quote',state['quote'])
    assert state['oneoff'][-2]==['Custom backend, CRM and integrations','£1,875'],(w,h,'backend in wrong table')
    assert 'Backend maintenance and support' in state['monthly'][-2][0],(w,h,'recurring backend missing')
    if w<=1024:
        t,sw,nav,pdf=(state[k] for k in ('toolbar','switcher','nav','pdf'))
        assert state['navbarStyle']=='fixed',(w,h,'not fixed')
        assert t['h']<=58,(w,h,'menu too tall',t)
        assert abs(sw['t']-nav['t'])<16 and abs(nav['t']-pdf['t'])<16,(w,h,'menu stacked',sw,nav,pdf)
        assert sw['r']<=nav['l']+2,(w,h,'switch and nav overlap')
        assert nav['r']<=pdf['l']+2,(w,h,'nav and pdf overlap')
        assert nav['w']>=20,(w,h,'nav too narrow')
        assert t['l']>=-1 and t['r']<=w+1,(w,h,'toolbar clipped')

    await page.locator('.fm-story-next').click()
    await page.wait_for_timeout(100)
    for cls in ['.fm-story-prev','.fm-story-next']:
        el=page.locator(cls)
        assert await el.is_enabled(),(w,h,cls)
        await el.hover(force=True)
        colors=await el.evaluate("""el=>{
          const s=getComputedStyle(el);
          const rgb=t=>{
            const m=t.match(/rgba?\\(([^)]+)\\)/);
            return m?m[1].split(',').slice(0,3).map(v=>Number(v.trim())):[];
          };
          return {bg:s.backgroundColor,fg:s.color,foreRGB:rgb(s.color),backRGB:rgb(s.backgroundColor)};
        }""")
        fg=colors['foreRGB'];bg=colors['backRGB']
        assert len(fg)==3 and len(bg)==3,(w,h,cls,colors)
        lum=lambda rgb:sum(rgb)/3
        assert abs(lum(fg)-lum(bg))>65,(w,h,'low contrast arrow',cls,colors)
    await page.close()
    print('PASS_V26',browser.browser_type.name,w,h,
          json.dumps({'toolbarHeight':round(state['toolbar']['h'],1),
                      'navWidth':round(state['nav']['w'],1),
                      'navScrollWidth':state['navScrollWidth'],
                      'oneoffRows':len(state['oneoff']),'monthlyRows':len(state['monthly'])}),flush=True)

async def main():
    async with async_playwright() as p:
        for engine in (p.chromium,p.webkit):
            b=await engine.launch()
            sizes=SIZES if engine.name=='chromium' else [SIZES[i] for i in [0,2,3,5,7,9]]
            for w,h in sizes: await check(b,w,h)
            await b.close()
    print('V26_PRICING_SINGLE_ROW_AND_ARROW_QA_PASSED',flush=True)

asyncio.run(main())
