#!/usr/bin/env python3
"""Browser QA for mobile A4 proposal and overview-first behaviour."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

URL=(Path(__file__).parent/"index.html").resolve().as_uri()
SIZES=[(320,568),(360,740),(390,844),(430,932),(768,1024),(820,720),(1024,768),(1280,900),(1440,900)]

async def inspect(page):
    return await page.evaluate("""() => {
      const q=s=>document.querySelector(s);
      const rr=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
      const reader=q('.viewport');
      const active=[...document.querySelectorAll('.viewport > .sheet.is-active')];
      const paper=active[0];
      const body=paper?.querySelector('.sheet-body');
      const footer=paper?.querySelector('.sheet-footer');
      return {
        width:innerWidth,height:innerHeight,
        mode:reader?.dataset.readingMode,
        scrollY:scrollY,
        documentWidth:document.documentElement.scrollWidth,
        toolbar:rr(q('.toolbar')),nav:rr(q('.toolbar nav.tabs.proposal-sections')),
        rail:rr(q('.fm-zoom')),reader:rr(reader),
        paper:rr(paper),paperId:paper?.id,
        active:active.map(e=>e.id),
        counter:q('.fm-story-counter')?.textContent?.trim(),
        chapter:document.body.dataset.currentChapter,
        tab:q('#tab-overview')?.getAttribute('aria-selected'),
        pageCount:document.querySelectorAll('.viewport>.sheet').length,
        hiddenPages:[...document.querySelectorAll('.viewport>.sheet:not(.is-active)')].filter(e=>getComputedStyle(e).display!=='none').length,
        paperOverflow:paper?paper.scrollHeight-paper.clientHeight:0,
        bodyOverflow:body?body.scrollHeight-body.clientHeight:0,
        footer:rr(footer),
        cssZoom:paper?.style.zoom||'none'
      };
    }""")

async def check(browser,w,h):
    page=await browser.new_page(viewport={"width":w,"height":h},device_scale_factor=2 if w<600 else 1)
    errors=[]
    page.on("pageerror",lambda exc: errors.append(str(exc)))
    await page.goto(URL+"#budget",wait_until="domcontentloaded")
    await page.wait_for_timeout(750)
    start=await inspect(page)
    assert start["active"]==["overview"],f"{w}x{h}: not opening Overview: {start}"
    assert start["counter"].startswith("1 / "),f"{w}x{h}: counter {start['counter']}"
    assert start["scrollY"] < 3,f"{w}x{h}: restored scroll position"
    assert start["documentWidth"]<=w+3,f"{w}x{h}: horizontal document overflow"
    assert not errors,f"{w}x{h}: browser errors: {errors}"
    if w<=1024:
        assert start["mode"]=="paged",f"{w}x{h}: mode={start['mode']}"
        assert start["hiddenPages"]==0,f"{w}x{h}: inactive pages visible"
        assert start["paper"],f"{w}x{h}: no paper"
        assert start["paper"]["left"]>=-2 and start["paper"]["right"]<=w+2,f"{w}x{h}: paper clipped horizontally {start['paper']}"
        assert start["paper"]["top"]>=start["reader"]["top"]-2,f"{w}x{h}: paper clipped above reader"
        assert start["paper"]["bottom"]<=start["reader"]["bottom"]+2,f"{w}x{h}: paper clipped below reader"
        assert start["reader"]["top"]>=start["toolbar"]["bottom"]-2,f"{w}x{h}: toolbar overlaps document"
        assert start["reader"]["bottom"]<=start["rail"]["top"]+2,f"{w}x{h}: controls overlap document"
        assert start["nav"]["height"]>=32,f"{w}x{h}: nav menu collapsed"
        assert start["paperOverflow"]<=3,f"{w}x{h}: page overflows fixed A4 height by {start['paperOverflow']}"
        # Turn through all pages. Page advances may not create vertical
        # scrolling or reveal part of the previous/next A4 sheet.
        page_count=start["pageCount"]
        overflows=[]
        for index in range(1,page_count):
            await page.locator(".fm-story-next").click()
            await page.wait_for_timeout(50)
            cur=await inspect(page)
            if cur["paperOverflow"]>3 or cur["bodyOverflow"]>5:
                overflows.append({"index":index+1,"id":cur["paperId"],"paperOverflow":cur["paperOverflow"],"bodyOverflow":cur["bodyOverflow"]})
            assert len(cur["active"])==1,f"{w}x{h}: {index} visible sheet count {cur['active']}"
            assert cur["counter"].startswith(f"{index+1} / "),f"{w}x{h}: incorrect counter {cur['counter']}"
            assert cur["paper"]["left"]>=-2 and cur["paper"]["right"]<=w+2,f"{w}x{h}: clipped width on {cur['paperId']}"
            assert cur["paper"]["bottom"]<=cur["reader"]["bottom"]+2,f"{w}x{h}: clipped height on {cur['paperId']}"
            assert cur["scrollY"]<=2,f"{w}x{h}: body scrolled after navigation"
        print("CONTENT_OVERFLOW",browser.browser_type.name,w,h,json.dumps(overflows))
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(550)
        r=await inspect(page)
        assert r["active"]==["overview"] and r["counter"].startswith("1 / "),f"{w}x{h}: reload did not reset: {r}"
    print("PASS",browser.browser_type.name,f"{w}x{h}",json.dumps({k:start[k] for k in ["mode","paperId","counter","pageCount","documentWidth","paperOverflow","bodyOverflow","cssZoom"]}))
    await page.close()

async def main():
    async with async_playwright() as p:
        chromium=await p.chromium.launch()
        for w,h in SIZES:
            await check(chromium,w,h)
        await chromium.close()
        try:
            webkit=await p.webkit.launch()
        except Exception as exc:
            print("WEBKIT_NOT_AVAILABLE",str(exc)[:160])
        else:
            for w,h in [(320,568),(390,844),(430,932),(820,720)]:
                await check(webkit,w,h)
            await webkit.close()
    print("MOBILE_READER_QA_PASSED")

asyncio.run(main())
