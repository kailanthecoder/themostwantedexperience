#!/usr/bin/env python3
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

URI=(Path(__file__).parent/'index.html').resolve().as_uri()
SELECTORS=[
 '#overview', '#overview .sheet-cap','#overview .presentation-header','#overview .waveblock',
 '#overview .sheet-body','#overview .page-heading','#overview .statement-firstpage',
 '#overview .vision-intro','#overview .vision-grid','#overview .vision-card',
 '#overview .roadmap-callout','#overview .roadmap-title','#overview .promise-grid',
 '#overview .stage-runway','#overview .stage-card','#overview .personal-signoff',
 '#overview .signoff-photo','#overview .signoff-content','#overview .sheet-footer',
 '.toolbar','.toolbar-inner','.nav-toprow','.view-switcher','.proposal-sections',
 '.proposal-sections .tab','.tool-actions','.pdf-btn','.fm-zoom'
]
async def test(p,browser,w,h):
 page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
 await page.goto(URI,wait_until='domcontentloaded')
 await page.evaluate("() => document.fonts.ready")
 await page.wait_for_timeout(650)
 d=await page.evaluate("""(sels)=>{
 const rr=e=>{if(!e)return null;const r=e.getBoundingClientRect();const s=getComputedStyle(e);
  return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1),right:+r.right.toFixed(1),bottom:+r.bottom.toFixed(1),
   fontSize:s.fontSize,lineHeight:s.lineHeight,position:s.position,overflow:s.overflow,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,display:s.display}};
 const sheet=document.querySelector('#overview'), paper=rr(sheet), zoom=parseFloat(sheet.style.zoom)||1;
 const boxes=Object.fromEntries(sels.map(sel=>[sel,rr(document.querySelector(sel))]));
 const rel=e=>{const r=e.getBoundingClientRect();return {x:+((r.x-sheet.getBoundingClientRect().x)/zoom).toFixed(1),y:+((r.y-sheet.getBoundingClientRect().y)/zoom).toFixed(1),w:+(r.width/zoom).toFixed(1),h:+(r.height/zoom).toFixed(1),bottom:+((r.bottom-sheet.getBoundingClientRect().y)/zoom).toFixed(1),right:+((r.right-sheet.getBoundingClientRect().x)/zoom).toFixed(1)}};
 const promises=[...document.querySelectorAll('#overview .promise')].map((el,i)=>({name:el.innerText,i,rect:rel(el),icon:rel(el.querySelector('svg')),span:rel(el.querySelector('span')),spanScrollWidth:el.querySelector('span')?.scrollWidth,spanWidth:el.querySelector('span')?.clientWidth}));
 const body=sheet.querySelector('.sheet-body'),foot=sheet.querySelector('.sheet-footer'),sign=sheet.querySelector('.personal-signoff');
 return {viewport:[innerWidth,innerHeight],paper:paper,cssZoom:zoom,
   rel:Object.fromEntries(sels.filter(sel=>sel.startsWith('#overview')).map(sel=>[sel,rel(document.querySelector(sel))])),
   boxes:Object.fromEntries(Object.entries(boxes).filter(([sel])=>!sel.startsWith('#overview'))),
   hiddenSignoffPixels:Math.max(0,(sign.getBoundingClientRect().bottom-body.getBoundingClientRect().bottom)/zoom),
   bodyBottomToFooter:(foot.getBoundingClientRect().top-body.getBoundingClientRect().bottom)/zoom,
   promises};
 }""",SELECTORS)
 print('DIAGNOSTIC',browser.browser_type.name,f'{w}x{h}',json.dumps(d,ensure_ascii=False),flush=True)
 await page.close()

async def main():
 async with async_playwright() as p:
  for engine in [p.chromium,p.webkit]:
   b=await engine.launch()
   for w,h in [(390,844),(320,568),(832,1805),(1280,900)]:
    await test(p,b,w,h)
   await b.close()
asyncio.run(main())
