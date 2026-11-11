#!/usr/bin/env python3
"""Check the *actual visual artefact* on iOS Safari/WebKit and Chromium.

Images are the source of mobile page pixels, so no text/layout can reflow.
Confirm complete full-page fit, image decoding, navigation and print fallback.
"""
import asyncio, os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
ORIGIN=os.getenv('FAHMAI_PREVIEW_URL') or (ROOT/'index.html').as_uri()
SIZES=((280,568),(320,568),(360,640),(375,667),(390,844),(393,852),
       (414,896),(430,932),(540,720),(768,1024),(820,1180),(1024,768),
       (568,320),(844,390),(932,430))
IDS=('overview','current','current-journeys','current-growth','spec','spec-delivery',
     'budget','implementation','implementation-evidence','examples','examples-client')

async def check(browser,w,h):
    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=2 if w<600 else 1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    result=await page.goto(ORIGIN,wait_until='domcontentloaded',timeout=60000)
    assert result and result.status==200,(browser.browser_type.name,w,h,'bad response',result.status if result else None)
    await page.wait_for_timeout(380)
    async def state():
        return await page.evaluate("""() => {
          const rr=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,w:r.width,h:r.height}};
          const p=document.querySelector('.viewport>.sheet.is-active');
          const im=p?.querySelector('img.fm-page-fidelity');
          const nav=document.querySelector('.toolbar');
          const reader=document.querySelector('.viewport');
          const imageStyle=im?getComputedStyle(im):null;
          const source=p?.querySelector('.sheet-body');
          return {
            id:p?.id,mode:reader?.dataset.readingMode,active:document.querySelectorAll('.viewport>.sheet.is-active').length,
            paper:rr(p),img:rr(im),reader:rr(reader),toolbar:rr(nav),
            complete:im?.complete,natural:[im?.naturalWidth,im?.naturalHeight],imgDisplay:imageStyle?.display,
            sourceDisplay:source?getComputedStyle(source).display:null,
            sourceOpacity:source?getComputedStyle(source).opacity:null,
            page:document.querySelector('.fm-story-counter')?.textContent.trim(),
            bodyScrollWidth:document.documentElement.scrollWidth,
            screenWidth:innerWidth,screenHeight:innerHeight
          };
        }""")
    a=await state()
    assert a['id']=='overview' and a['page'].startswith('1 / '),(w,h,'overview-first',a)
    assert a['mode']=='paged',(w,h,'wrong mobile mode')
    assert a['active']==1,(w,h,'multiple pages')
    assert a['screenWidth']==w,(w,h,'viewport differs')
    assert a['bodyScrollWidth']<=w+2,(w,h,'horizontal scroll')
    assert a['sourceDisplay']=='none',(w,h,'raw text still rendered, could reflow',a)
    assert a['imgDisplay']=='block',(w,h,'static page missing')
    assert a['img']['w']>=a['paper']['w']-2 and a['img']['w']<=a['paper']['w']+2,(w,h,'image does not fill page width')
    print('IMAGE_GEOMETRY',browser.browser_type.name,w,h,a['paper'],a['img'],a['reader'],flush=True)
    assert abs(a['img']['h']-a['paper']['h'])<2,(w,h,'page height/image mismatch')
    assert a['paper']['left']>=-2 and a['paper']['right']<=w+2,(w,h,'page clipped horizontally')
    assert a['paper']['bottom']<=a['reader']['bottom']+2,(w,h,'page clipped vertically')
    if not a['complete']:
        await page.wait_for_timeout(1000)
        a=await state()
    assert a['complete'] and a['natural']==[1588,2246],(w,h,'image did not decode',a)
    assert not errors,(w,h,'JS errors',errors)
    assert a['toolbar']['h']<=56,(w,h,'toolbar wrapped',a)
    if w in (320,390,430,768,1024,568):
        for idx,id in enumerate(IDS[1:],2):
            await page.locator('.fm-story-next').click()
            await page.wait_for_timeout(70)
            b=await state()
            if not b['complete']:
                await page.wait_for_timeout(800)
                b=await state()
            assert b['id']==id and b['page'].startswith(f'{idx} / '),(w,h,idx,'bad page',b)
            assert b['imgDisplay']=='block' and b['sourceDisplay']=='none',(w,h,idx,'HTML exposed')
            assert b['complete'] and b['natural']==[1588,2246],(w,h,idx,'missing image',b)
            assert b['img']['w']>=b['paper']['w']-2 and b['img']['w']<=b['paper']['w']+2,(w,h,idx,'width')
            assert b['img']['h']<=b['reader']['h']+2,(w,h,idx,'bottom')
            assert len(errors)==0,(w,h,'javascript errors',errors)
    await page.close()
    print('STATIC_A4_PASS',browser.browser_type.name,w,h,
          'paper',round(a['paper']['w'],1),round(a['paper']['h'],1),
          'menu',round(a['toolbar']['h'],1),'full_res',a['natural'],flush=True)

async def print_fallback(browser):
    page=await browser.new_page(viewport={'width':1440,'height':1100})
    await page.goto(ORIGIN,wait_until='domcontentloaded')
    await page.emulate_media(media='print')
    d=await page.evaluate("""()=>{
      const p=document.querySelector('#overview');
      return {
        source:getComputedStyle(p.querySelector('.sheet-body')).display,
        image:getComputedStyle(p.querySelector('.fm-page-fidelity')).display,
        count:document.querySelectorAll('.viewport>.sheet').length
      };
    }""")
    assert d['source']!='none' and d['image']=='none' and d['count']==11,d
    print('PRINT_ORIGINAL_A4_KEPT',d,flush=True)
    await page.close()

async def main():
    async with async_playwright() as p:
        for engine in [p.chromium,p.webkit]:
            browser=await engine.launch()
            use=SIZES if engine.name=='chromium' else [SIZES[i] for i in (0,1,3,4,6,7,9,11,12)]
            for w,h in use: await check(browser,w,h)
            if engine.name=='chromium': await print_fallback(browser)
            await browser.close()
    print('NO_REFLOW_A4_READER_VERIFIED_ON_WEBKIT_AND_CHROMIUM',flush=True)

asyncio.run(main())
