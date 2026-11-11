#!/usr/bin/env python3
"""Regression: A4 content keeps exactly the same computed layout across devices.

The parent document viewer may resize, scroll and zoom, but headings, brand
logos, typography, grid columns and internal page padding must never change.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

FILE=(Path(__file__).parent/"index.html").resolve().as_uri()
PAGES=['overview','current','current-journeys','current-growth','spec','spec-delivery',
       'budget','implementation','implementation-evidence','examples','examples-client']
SELECTORS=[
 '.presentation-header','.presented-group','.presented-copy',
 '.client-lockups','.original-brand.brand-fmh','.original-brand.brand-bull',
 '.original-brand.brand-pc','.mw-black','.signature-logo',
 '.waveblock','.chapter-banner','.sheet-body',
 '.page-heading','.page-heading h1','.page-heading .sub',
 '.sheet-section','.example-grid','.example-media','.example-copy',
 '.example-copy h3','.example-copy p',
 '.budgetv8-card','.budgetv8-intro','.budgetv8-rate-tables',
 '.specv6-brand-content','.sheet-footer',
]
PROPS=['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing',
       'paddingTop','paddingRight','paddingBottom','paddingLeft',
       'marginTop','marginBottom',
       'backgroundColor','color','borderRadius']
async def state(page):
    return await page.evaluate("""([pages,selectors,props])=>{
      const sheets=[...document.querySelectorAll('.viewport>.sheet')];
      const initial=sheets.map(e=>[e,e.classList.contains('is-active')]);
      const states={};
      for(const id of pages){
        const root=document.getElementById(id);
        if(!root){states[id]={error:'missing sheet'};continue}
        // Force the target paper into layout for the style inspection.
        sheets.forEach(e=>e.classList.toggle('is-active',e===root));
        const styles={};
        for(const sel of selectors){
          const el=root.querySelector(sel);
          if(!el)continue;
          const cs=getComputedStyle(el);
          styles[sel]=Object.fromEntries(props.map(prop=>[prop,cs[prop]]));
        }
        states[id]=styles;
      }
      sheets.forEach((e,i)=>e.classList.toggle('is-active',initial[i][1]));
      return states;
    }""",[PAGES,SELECTORS,PROPS])

async def run(browser,device):
    sizes=[(1440,900),(390,844),(320,568),(768,1024),(1024,768)]
    states=[]
    for w,h in sizes:
        page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        await page.goto(FILE,wait_until='domcontentloaded')
        result=await state(page)
        states.append(result)
        await page.close()
    desktop=states[0]
    differences=[]
    for i,(w,h) in enumerate(sizes[1:],1):
        for p in PAGES:
            for selector,values in desktop[p].items():
                other=states[i][p].get(selector)
                if other is None:
                    differences.append((w,p,selector,'missing',values,None))
                    continue
                for prop,value in values.items():
                    if prop=='color' and selector=='.page-heading':continue
                    if other[prop]!=value:
                        differences.append((w,p,selector,prop,value,other[prop]))
    if differences:
        print('DIFFERENCES',browser.browser_type.name,json.dumps(differences[:100]),flush=True)
    assert not differences,f'{browser.browser_type.name}: {len(differences)} A4 design differences on mobile'
    print("IDENTICAL_A4_STYLES",browser.browser_type.name,len(PAGES),"pages",len(sizes),"viewport sizes",flush=True)

async def main():
    async with async_playwright() as p:
        for engine in [p.chromium,p.webkit]:
            browser=await engine.launch()
            await run(browser,engine.name)
            await browser.close()
    print("A4_GEOMETRY_IDENTICAL_ACROSS_MOBILE_DESKTOP",flush=True)

asyncio.run(main())
