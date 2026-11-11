#!/usr/bin/env python3
"""Verify the ACTUAL commit-pinned GitHubraw URL in live browsers."""
import asyncio, base64, os
from playwright.async_api import async_playwright
SHA='d2cef47aa6b8ff2f06e0999c1e14e4f9894e25ee'
URL='https://githubraw.com/kailanthecoder/themostwantedexperience/'+SHA+'/proposals/fah-mai/'

async def verify(browser,w,h,screenshot=False):
    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=2 if w<600 else 1)
    errors=[]
    page.on('pageerror',lambda err: errors.append(str(err)))
    response=await page.goto(URL,wait_until='domcontentloaded',timeout=60000)
    assert response and response.status==200,(w,h,response.status if response else 'no response')
    await page.evaluate('document.fonts.ready')
    await page.wait_for_timeout(800)
    status=await page.evaluate("""()=>{
      const p=document.querySelector('#overview'),a=document.querySelector('.toolbar'),
        sw=document.querySelector('.view-switcher'),nav=document.querySelector('.proposal-sections'),pdf=document.querySelector('.pdf-btn'),
        body=p.querySelector('.sheet-body'),foot=p.querySelector('.sheet-footer'),sign=p.querySelector('.personal-signoff');
      const r=e=>{const x=e.getBoundingClientRect();return {left:x.left,right:x.right,top:x.top,bottom:x.bottom,width:x.width,height:x.height}};
      const imgs=[...p.querySelectorAll('img[src^="./assets/"]')];
      return {
        loaded:!!document.getElementById('fahmai-zero-overlap-v28'),
        page:[...document.querySelectorAll('.viewport>.sheet.is-active')].map(e=>e.id),
        counter:document.querySelector('.fm-story-counter').textContent.trim(),
        toolbar:r(a),switcher:r(sw),nav:r(nav),pdf:r(pdf),
        navScroll:nav.scrollWidth,navClient:nav.clientWidth,
        body:r(body),foot:r(foot),sign:r(sign),
        fontReady:document.fonts.status,
        soraLoaded:document.fonts.check('700 12px Sora'),
        outfitLoaded:document.fonts.check('600 12px Outfit'),
        sourceSansLoaded:document.fonts.check('600 12px "Source Sans 3"'),
        imgs:imgs.map(e=>({src:e.getAttribute('src'),complete:e.complete,width:e.naturalWidth})),
        benefit:[...p.querySelectorAll('.promise')].map(e=>{
          const icon=e.querySelector('svg'),span=e.querySelector('span');
          return {label:e.innerText,rect:r(e),icon:r(icon),span:r(span)}
        })
      };
    }""")
    assert status['loaded'],(w,h,'public CDN still stale')
    assert status['page']==['overview'],(w,h,'wrong page',status['page'])
    assert status['counter'].startswith('1 / '),(w,h,status['counter'])
    assert status['fontReady']=='loaded',(w,h,'fonts')
    assert status['soraLoaded'] and status['outfitLoaded'] and status['sourceSansLoaded'],(w,h,'font assets blocked',status)
    assert not errors,(w,h,'JavaScript errors',errors)
    assert status['toolbar']['height']<=(55 if w<=1024 else 80),(w,h,'toolbar unexpectedly tall')
    assert abs(status['nav']['top']-status['switcher']['top'])<16 and abs(status['nav']['top']-status['pdf']['top'])<16,(w,h,'toolbar wrap')
    assert status['switcher']['right']<=status['nav']['left']+2 and status['nav']['right']<=status['pdf']['left']+2,(w,h,'toolbar overlap')
    assert status['sign']['bottom']<status['body']['bottom']-2,(w,h,'signoff clipped')
    assert status['sign']['bottom']<status['foot']['top']-2,(w,h,'signoff behind footer')
    assert len(status['benefit'])==7,(w,h,'missing benefit icons')
    for el in status['benefit']:
        assert el['icon']['right']<el['span']['left'],(w,h,'label touches icon',el)
        assert el['span']['right']<=el['rect']['right']+1,(w,h,'benefit text clips',el)
    if w>=375:
        assert status['navScroll']<=status['navClient']+3,(w,h,'tabs horizontally clipped')
    unloaded=[i for i in status['imgs'] if not i['complete'] or i['width']<1]
    assert not unloaded,(w,h,'first-page brand images missing',unloaded)
    print('PINNED_PUBLIC_PASS',browser.browser_type.name,f'{w}x{h}',
          'toolbar',round(status['toolbar']['height']),
          'navScroll',status['navScroll'],'navWidth',status['navClient'],
          'fontsLoaded',status['fontReady'],
          'brandImages',len(status['imgs']),flush=True)
    if screenshot:
        jpeg=await page.screenshot(type='jpeg',quality=73,full_page=False)
        encoded=base64.b64encode(jpeg).decode('ascii')
        print('PUBLIC_SCREENSHOT_BEGIN',len(encoded),flush=True)
        for idx in range(0,len(encoded),4096):
            print('PUBLIC_SCREENSHOT_CHUNK',encoded[idx:idx+4096],flush=True)
        print('PUBLIC_SCREENSHOT_END',flush=True)
    await page.close()

async def main():
    async with async_playwright() as p:
        for eng in [p.chromium,p.webkit]:
            b=await eng.launch()
            for w,h in ([(320,568),(390,844),(430,932),(768,1024),(1280,900)] if eng.name=='chromium' else [(320,568),(390,844),(430,932)]):
                await verify(b,w,h,screenshot=(w==390 and eng.name=='webkit'))
            await b.close()
    print('LIVE_PUBLIC_GITHUBRAW_QA_PASSED',flush=True)

asyncio.run(main())
