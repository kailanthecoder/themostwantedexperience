#!/usr/bin/env python3
"""Regression suite for ALL user-visible Fah Mai Overview defects on mobile.

Browser renders (with web fonts ready), verifies no text collision / no hidden
sign-off / one top row / full A4 paper and navigation controls.
"""
import asyncio, json, math
from pathlib import Path
from playwright.async_api import async_playwright

URL=(Path(__file__).parent/'index.html').resolve().as_uri()
PORTRAIT=[(280,640),(320,568),(360,640),(375,667),(390,844),(393,852),(414,896),(430,932),
          (540,720),(768,1024),(820,1180),(1024,768),(1280,900),(1440,900)]
LANDSCAPE=[(568,320),(667,375),(844,390),(932,430)]
async def get(page):
    return await page.evaluate("""() => {
      const rect=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}}
      const pr=document.querySelector('#overview'),body=pr.querySelector('.sheet-body'),foot=pr.querySelector('.sheet-footer'),
      sign=pr.querySelector('.personal-signoff'),callout=pr.querySelector('.roadmap-callout'),grid=pr.querySelector('.promise-grid');
      const toolbar=document.querySelector('.toolbar'),inner=toolbar.querySelector('.toolbar-inner'),
      switcher=toolbar.querySelector('.view-switcher'),nav=toolbar.querySelector('.proposal-sections'),pdf=toolbar.querySelector('.pdf-btn'),
      viewport=document.querySelector('.viewport');
      const promises=[...pr.querySelectorAll('.promise')].map(el=>({text:el.innerText.trim(),
        box:rect(el),icon:rect(el.querySelector('svg')),label:rect(el.querySelector('span')),
        scrollWidth:el.scrollWidth,clientWidth:el.clientWidth}));
      const cards=[...pr.querySelectorAll('.stage-card')].map(el=>({card:rect(el),head:rect(el.querySelector('.stage-head')),copy:rect(el.querySelector('p'))}));
      const all=[...document.querySelectorAll('.viewport>.sheet')];
      return {
        innerWidth,innerHeight,
        toolbar:rect(toolbar),toolbarInner:rect(inner),switcher:rect(switcher),
        nav:rect(nav),navScrollWidth:nav.scrollWidth,navClientWidth:nav.clientWidth,navPosition:getComputedStyle(toolbar).position,pdf:rect(pdf),
        paper:rect(pr),paperScrollHeight:pr.scrollHeight,paperClientHeight:pr.clientHeight,
        reader:rect(viewport),body:rect(body),foot:rect(foot),sign:rect(sign),callout:rect(callout),grid:rect(grid),
        promise:promises,stages:cards,
        active:all.filter(e=>e.classList.contains('is-active')).map(e=>e.id),
        counter:document.querySelector('.fm-story-counter')?.textContent,
        fontCheck:document.fonts.status,
        bodyOverflow:document.documentElement.scrollWidth-innerWidth
      };
    }""")

async def check(browser,w,h):
    mobile=w<=1024
    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=2 if w<600 else 1)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    await page.goto(URL+'#budget',wait_until='domcontentloaded')
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(300)
    v=await get(page)
    assert not errors,(w,h,'js errors',errors)
    assert v['active']==['overview'],(w,h,'failed overview startup',v['active'])
    assert v['counter'].strip().startswith('1 / '),(w,h,'counter',v['counter'])
    assert v['bodyOverflow']<=2,(w,h,'full-page horizontal overflow',v['bodyOverflow'])
    assert v['fontCheck']=='loaded',(w,h,'fonts not loaded')
    B=v['body'];F=v['foot'];S=v['sign'];G=v['grid'];C=v['callout']
    assert S['bottom'] <= B['bottom']-2,(w,h,'sign-off clipped',S,B)
    assert S['bottom'] < F['top']-2,(w,h,'sign-off behind footer')
    assert G['left']>=C['left'] and G['right']<=C['right']+1,(w,h,'benefits out of banner')
    promises=v['promise']
    assert len(promises)==7,(w,h,'wrong promise count')
    for promise in promises:
        b=promise['box'];i=promise['icon'];l=promise['label']
        assert b['left']>=G['left']-1 and b['right']<=G['right']+1,(w,h,'promise outside grid',promise)
        assert i['right']<l['left']-0.1,(w,h,'icon touches label',promise)
        assert l['left']>=b['left'] and l['right']<=b['right']+1,(w,h,'label beyond own grid cell',promise)
        assert l['bottom']<=b['bottom']+1,(w,h,'label below grid cell',promise)
        assert promise['scrollWidth']<=promise['clientWidth']+2,(w,h,'promise text overflow',promise)
    for i in range(len(promises)):
        a=promises[i]['box']
        for j in range(i+1,len(promises)):
            b=promises[j]['box']
            ox=min(a['right'],b['right'])-max(a['left'],b['left'])
            oy=min(a['bottom'],b['bottom'])-max(a['top'],b['top'])
            assert ox<=0.8 or oy<=0.8,(w,h,'colliding promises',promises[i],promises[j])
    for stage in v['stages']:
        assert stage['copy']['bottom']<stage['card']['bottom']+1,(w,h,'stage text overflow',stage)
        assert stage['head']['bottom']<stage['copy']['top']+2,(w,h,'stage icon and copy overlap',stage)
    if mobile:
        a,n,sw,pdf=(v[k] for k in ('toolbar','nav','switcher','pdf'))
        assert v['navPosition']=='fixed',(w,h,'menu not fixed',v['navPosition'])
        assert a['height']<=54,(w,h,'menu wrapped',a)
        assert abs(sw['top']-n['top'])<=16 and abs(pdf['top']-n['top'])<=16,(w,h,'menu on two lines',sw,n,pdf)
        assert sw['right']<=n['left']+2,(w,h,'switch overlaps menu')
        assert n['right']<=pdf['left']+2,(w,h,'menu overlaps export')
        assert n['width']>=15,(w,h,'unusable menu')
        assert v['paper']['left']>=-2 and v['paper']['right']<=w+2,(w,h,'A4 cropped horizontally')
        assert v['paper']['bottom']<=v['reader']['bottom']+2,(w,h,'A4 cropped below controls')
        assert v['reader']['top']>=a['bottom']-2,(w,h,'toolbar obscures paper')
        if w>=375:
            assert v['navScrollWidth']<=v['navClientWidth']+3,(w,h,'menu tabs not all visible',v['navScrollWidth'],v['navClientWidth'])
    # Tap through all pages after fonts load; no navigation resets or hidden sheets.
    if w in (320,390,768,1024):
        for k in range(1,11):
            await page.locator('.fm-story-next').click()
            st=await page.evaluate("""() => ({
              counter:document.querySelector('.fm-story-counter')?.textContent.trim(),
              ids:[...document.querySelectorAll('.viewport>.sheet.is-active')].map(x=>x.id)
            })""")
            assert len(st['ids'])==1,(w,h,k,st)
            assert st['counter'].startswith(f'{k+1} / '),(w,h,k,st)
    await page.close()
    print('CLEAN_V28',browser.browser_type.name,w,h,'navWidth',round(v['nav']['width']),
          'navScroll',v['navScrollWidth'],'paper',round(v['paper']['height']),
          'signoffBottom',round(v['sign']['bottom']),'bodyBottom',round(v['body']['bottom']),flush=True)

async def main():
    async with async_playwright() as p:
        for engine in (p.chromium,p.webkit):
            b=await engine.launch()
            for w,h in (PORTRAIT+LANDSCAPE if engine.name=='chromium' else
                        [PORTRAIT[i] for i in (0,1,4,6,7,9,11,13)]+[(844,390)]):
                await check(b,w,h)
            await b.close()
    print('OVERVIEW_VISUAL_COLLISION_CHECK_PASSED',flush=True)

asyncio.run(main())
