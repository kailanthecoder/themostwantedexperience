#!/usr/bin/env python3
"""Render immutable 2x A4 page facsimiles, then enable them ONLY on narrow screens.

The source HTML remains the desktop and print document; the mobile reader uses
pre-rendered images so iOS Safari cannot reshape fonts, grids or footer heights.
Generated artefacts are checked into Git alongside index.html.
"""
import asyncio, hashlib, io, re
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
HTML=ROOT/'index.html'
ASSET=ROOT/'assets'
PAGES=('overview','current','current-journeys','current-growth','spec',
       'spec-delivery','budget','implementation','implementation-evidence',
       'examples','examples-client')
CSS_ID='fahmai-mobile-facsimile-v29'
FILE_URI=HTML.as_uri()

async def render_images():
    ASSET.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        page=await browser.new_page(viewport={'width':1440,'height':1700},device_scale_factor=2)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(FILE_URI,wait_until='load',timeout=45000)
        await page.evaluate('document.fonts.ready')
        # Ask the site's own reader to use true 1x A4 layout. Forcing a style
        # alone raced its zoom controller and occasionally reset to 0.85x.
        await page.evaluate("""() => {
          const slider=document.querySelector('.fm-zoom-range');
          slider.value='1';
          slider.dispatchEvent(new Event('input',{bubbles:true}));
        }""")
        await page.wait_for_timeout(300)
        # Keep desktop A4 layout intact. A single sheet is selected per frame;
        # force 100% intrinsic CSS geometry and wait for its images to decode.
        for index,id in enumerate(PAGES,1):
            await page.evaluate("""id=>{
              document.querySelectorAll('.viewport > .sheet').forEach(sheet=>{
                const active=sheet.id===id;
                sheet.classList.toggle('is-active',active);
                sheet.style.setProperty('zoom','1','important');
                sheet.style.setProperty('display',active?'flex':'none','important');
                sheet.style.setProperty('transform','none','important');
              });
              const reader=document.querySelector('.viewport');
              reader.style.setProperty('overflow','visible','important');
              reader.style.setProperty('max-height','none','important');
              reader.style.setProperty('height','auto','important');
            }""",id)
            sheet=page.locator('article.sheet#'+id)
            await sheet.evaluate("""async e=>{
              await Promise.all([...e.querySelectorAll('img')].map(async i=>{
                if(i.loading==='lazy')i.loading='eager';
                if(!i.complete)await new Promise(r=>{
                  i.addEventListener('load',r,{once:true});
                  i.addEventListener('error',r,{once:true});
                  setTimeout(r,3000);
                });
                if(i.decode)await i.decode().catch(()=>{});
              }));
            }""")
            await page.wait_for_timeout(180)
            geom=await sheet.evaluate("""e=>{
              const b=e.getBoundingClientRect();
              const body=e.querySelector('.sheet-body');
              const footer=e.querySelector('.sheet-footer');
              const sign=e.querySelector('.personal-signoff');
              return {w:b.width,h:b.height,
                contentOverflow:e.scrollHeight-e.clientHeight,
                bodyOverflow:body?body.scrollHeight-body.clientHeight:0,
                signoffClipped:!!(sign&&body&&sign.getBoundingClientRect().bottom>body.getBoundingClientRect().bottom+1),
                footerClipped:!!(footer&&footer.getBoundingClientRect().bottom>b.bottom+2)};
            }""")
            assert 640<geom['w']<810 and abs(geom['h']/geom['w'] - 297/210)<.005,(id,geom)
            assert geom['contentOverflow']<4 and geom['bodyOverflow']<6,(id,geom)
            assert not geom['signoffClipped'] and not geom['footerClipped'],(id,geom)
            pixels=await sheet.screenshot(type='png',animations='disabled',timeout=30000)
            image=Image.open(io.BytesIO(pixels)).convert('RGB')
            # A stable 2x page without platform font substitutions.
            if image.size!=(1588,2246):
                image=image.resize((1588,2246),Image.Resampling.LANCZOS)
            filename=f'page-fidelity-{index:02d}.webp'
            path=ASSET/filename
            image.save(path,format='WEBP',quality=89,method=6)
            print('RENDERED_PAGE',index,id,image.size,len(pixels),'webp_bytes',path.stat().st_size,
                  'source_layout',geom,flush=True)
            if index==1:
                preview=image.copy()
                preview.thumbnail((640,900))
                out=io.BytesIO()
                preview.save(out,format='JPEG',quality=65,optimize=True)
                import base64
                enc=base64.b64encode(out.getvalue()).decode()
                print('FIDELITY_PREVIEW_B64_BEGIN')
                for i in range(0,len(enc),4096):
                    print('FIDELITY_PREVIEW_CHUNK',enc[i:i+4096])
                print('FIDELITY_PREVIEW_B64_END')
        await browser.close()
        assert not errors,errors
    print('ALL_11_A4_PAGES_RENDERED',flush=True)

def embed_images():
    html=HTML.read_text(encoding='utf-8')
    assert '<article' in html and 'id="overview"' in html
    assert CSS_ID not in html,'Already installed, refusing to duplicate'
    for i,id in enumerate(PAGES,1):
        rx=re.compile(r'(<article\b[^>]*\bid="'+re.escape(id)+r'"[^>]*>)([\s\S]*?)(</article>)',re.I)
        m=rx.search(html)
        assert m,'Missing page '+id
        src=f'./assets/page-fidelity-{i:02d}.webp'
        assert (ASSET/f'page-fidelity-{i:02d}.webp').stat().st_size>10000
        tag=f'<img class="fm-page-fidelity" src="{src}" alt="{id.replace("-"," ").title()} — full A4 proposal page" width="1588" height="2246" decoding="async" loading="{"eager" if i==1 else "lazy"}" draggable="false" aria-hidden="true"/>'
        assert 'fm-page-fidelity' not in m.group(2)
        # At the end of each paper, no layout influence on desktop.
        html=html[:m.start()] + m.group(1)+m.group(2)+tag+m.group(3)+html[m.end():]
    # Put the page image in front of any source HTML (which stays present for
    # desktop, links, accessibility, editing and print).
    CSS=r'''
<style id="fahmai-mobile-facsimile-v29">
/* Static artwork is genuinely hidden on desktop/print (existing HTML keeps
   the original accessible & print-ready document). */
html body .viewport>.sheet>.fm-page-fidelity{
 display:none!important;
}
@media screen and (max-width:1024px){
 html body .viewport[data-reading-mode="paged"]>.sheet.is-active{
   position:relative!important;isolation:isolate!important;
   overflow:hidden!important;
 }
 html body .viewport[data-reading-mode="paged"]>.sheet.is-active:is(#overview,#current,#current-journeys,#current-growth,#spec,#spec-delivery,#budget,#implementation,#implementation-evidence,#examples,#examples-client)>:not(.fm-page-fidelity){
   display:none!important;
 }
 html body .viewport[data-reading-mode="paged"]>.sheet>.fm-page-fidelity,
 html body .viewport[data-reading-mode="paged"]>.sheet.is-active>.fm-page-fidelity{
   position:absolute!important;display:block!important;
   box-sizing:border-box!important;inset:0!important;
   width:100%!important;min-width:100%!important;max-width:100%!important;
   height:100%!important;min-height:100%!important;max-height:100%!important;
   margin:0!important;padding:0!important;border:0!important;
   object-fit:fill!important;object-position:center center!important;
   pointer-events:none!important;user-select:none!important;
   z-index:2!important;overflow:hidden!important;
   -webkit-user-drag:none!important;
 }
 /* Reliable page dimensions are independent of font loading, browser engines
    and screen orientation. Existing zoom / Next / Previous controls stay live. */
 html body .viewport[data-reading-mode="paged"]>.sheet.is-active{
   contain:layout paint!important;
 }
}
@media print {
 html body .viewport>.sheet>.fm-page-fidelity{display:none!important}
}
</style>
'''
    html=html.replace('</head>',CSS+'</head>',1)
    HTML.write_text(html,encoding='utf-8')
    print('EMBEDDED_IMAGES',len(PAGES),'HTML_BYTES',HTML.stat().st_size,flush=True)

if __name__=='__main__':
    asyncio.run(render_images())
    embed_images()
    print('MOBILE_FACSIMILE_READY',flush=True)
