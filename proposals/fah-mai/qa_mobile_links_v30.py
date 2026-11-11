#!/usr/bin/env python3
"""Live link and action checks in immutable-image mobile viewer."""
import asyncio, os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
URL=os.getenv('FAHMAI_PREVIEW_URL') or (ROOT/'index.html').as_uri()

async def check(engine,w,h):
 b=await engine.launch()
 page=await b.new_page(viewport={'width':w,'height':h})
 errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 r=await page.goto(URL,wait_until='domcontentloaded',timeout=60000)
 assert r and r.status in ((0,200) if URL.startswith('file:') else (200,)),(w,h,'page status')
 await page.wait_for_timeout(240)
 hit=await page.locator('#overview > a.fm-fidelity-hit').evaluate_all("""es=>es.map(e=>({
   href:e.getAttribute('href'),box:e.getBoundingClientRect().toJSON(),
   style:getComputedStyle(e).display,events:getComputedStyle(e).pointerEvents
 }))""")
 assert len(hit)>=5,(w,h,'missing Overview anchors',hit)
 for a in hit:
  assert a['box']['width']>2 and a['box']['height']>1,(w,h,'zero-size hyperlink',a)
  assert a['events']=='auto' and a['style']!='none',(w,h,'link unclickable',a)
 assert any(a['href'].startswith('mailto:') for a in hit),(w,h,'email link missing')
 assert any(a['href'].startswith('tel:') for a in hit),(w,h,'phone link missing')
 await page.locator('#tab-current').click()
 await page.wait_for_timeout(300)
 current=await page.evaluate("""()=>[...document.querySelectorAll('.viewport >.sheet.is-active')].map(x=>x.id)""")
 assert current==['current'],(w,h,'Current tab failed',current)
 thumbs=page.locator('#current > button.fm-fidelity-hit[data-fm-action^="pagespeed:"]')
 assert await thumbs.count()==5,(w,h,'PageSpeed thumb interactions missing')
 await page.locator('#current > button.fm-fidelity-hit[data-fm-action="pagespeed:1"]').click(force=True)
 await page.wait_for_timeout(300)
 modal=page.locator('.ps-v22-dialog')
 assert await modal.evaluate('(e)=>e.open'),(w,h,'PageSpeed fullscreen did not open')
 title=await modal.locator('.ps-v22-report').text_content()
 assert 'Desktop' in title,(w,h,'wrong PageSpeed report selected',title)
 await modal.locator('.ps-v22-close').click()
 assert not await modal.evaluate('(e)=>e.open'),(w,h,'PageSpeed modal did not close')
 await page.locator('#tab-examples').click()
 await page.wait_for_timeout(300)
 active=await page.evaluate("""()=>[...document.querySelectorAll('.viewport >.sheet.is-active')].map(x=>x.id)""")
 assert active==['examples'],(w,h,'examples tab wrong',active)
 links=await page.locator('#examples > a.fm-fidelity-hit').evaluate_all("""es=>es.map(e=>e.getAttribute('href'))""")
 assert any('usemostwanted.com' in x for x in links),(w,h,'portfolio link missing',links)
 await page.locator('#examples > button.fm-fidelity-hit[data-fm-action="examples-continue"]').click(force=True)
 await page.wait_for_timeout(250)
 current=await page.evaluate("""()=>[...document.querySelectorAll('.viewport >.sheet.is-active')].map(x=>x.id)""")
 assert current==['examples-client'],(w,h,'examples continuation failed',current)
 assert not errors,(w,h,errors)
 print('CLICKABLE_MOBILE_PASS',engine.name,w,h,
       'overview_links',len(hit),'example_links',len(links),
       'pagespeed_modal',title,flush=True)
 await page.close();await b.close()

async def main():
 async with async_playwright() as p:
  for engine,w,h in [(p.chromium,320,568),(p.chromium,390,844),(p.chromium,768,1024),
                     (p.webkit,390,844),(p.webkit,430,932)]:
   await check(engine,w,h)
 print('ALL_MOBILE_LINKS_AND_EXAMPLE_ACTIONS_VERIFIED',flush=True)
asyncio.run(main())
