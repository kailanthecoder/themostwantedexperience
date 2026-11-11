#!/usr/bin/env python3
"""Preserve native clickable proposal links and interactive examples on mobile
without letting the A4 images reflow. Add transparent positioned hit regions.
"""
import asyncio, html, re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
FILE=ROOT/'index.html'
IDS=('overview','current','current-journeys','current-growth','spec','spec-delivery',
     'budget','implementation','implementation-evidence','examples','examples-client')

async def inspect():
    result={}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        page=await browser.new_page(viewport={'width':1440,'height':1700})
        await page.goto(FILE.as_uri(),wait_until='load')
        await page.evaluate('document.fonts.ready')
        await page.evaluate("""() => {
          const z=document.querySelector('.fm-zoom-range');z.value='1';z.dispatchEvent(new Event('input',{bubbles:true}));
        }""")
        await page.wait_for_timeout(250)
        for id in IDS:
            await page.evaluate("""id => {
              document.querySelectorAll('.viewport > .sheet').forEach(el=>{
                el.classList.toggle('is-active',el.id===id);
                el.style.setProperty('zoom','1','important');
                el.style.setProperty('display',el.id===id?'flex':'none','important');
              });
            }""",id)
            items=await page.evaluate("""id => {
              const paper=document.getElementById(id),r=paper.getBoundingClientRect();
              const pct=(el)=>{
                const b=el.getBoundingClientRect();
                const x=(b.left-r.left)/r.width*100,y=(b.top-r.top)/r.height*100,
                  w=b.width/r.width*100,h=b.height/r.height*100;
                if(!(w>0.6&&h>0.5&&x>=0&&y>=0&&x+w<=100.2&&y+h<=100.2))return null;
                return {x:+x.toFixed(4),y:+y.toFixed(4),w:+w.toFixed(4),h:+h.toFixed(4)};
              };
              const links=[...paper.querySelectorAll('a[href]')].filter(a=>!a.classList.contains('fm-fidelity-hit')).map(a=>{
                const box=pct(a);
                if(!box)return null;
                return {kind:'link',box,href:a.getAttribute('href'),
                  label:a.getAttribute('aria-label')||a.innerText.trim()||a.title||a.getAttribute('href'),
                  target:a.getAttribute('target')||''};
              }).filter(Boolean);
              const buttons=[...paper.querySelectorAll('button')].map(b=>{
                let action=null;
                if(id==='current'&&b.classList.contains('ps-v17-thumb'))action='pagespeed:'+b.dataset.psSlide;
                if(id==='current'&&b.classList.contains('ps-v22-expand'))action='pagespeed-full';
                if(id==='examples'&&b.hasAttribute('data-continue-examples'))action='examples-continue';
                const box=action?pct(b):null;
                return box?{kind:'button',box,action,label:b.getAttribute('aria-label')||b.innerText.trim()||action}:null;
              }).filter(Boolean);
              return [...links,...buttons];
            }""",id)
            result[id]=items
            print('HIT_REGIONS',id,len(items),[(e['kind'],e.get('href') or e.get('action')) for e in items],flush=True)
        await browser.close()
    return result

def update(regions):
    s=FILE.read_text(encoding='utf-8')
    assert 'id="fahmai-mobile-facsimile-v29"' in s
    assert 'fm-fidelity-link-hit-v30' not in s
    old='>:not(.fm-page-fidelity){'
    new='>:not(.fm-page-fidelity):not(.fm-fidelity-hit){'
    assert s.count(old)==1,('Unexpected mobile hide-rule count',s.count(old))
    s=s.replace(old,new,1)

    def boxstyle(b):
        return f"left:{b['x']:.4f}%;top:{b['y']:.4f}%;width:{b['w']:.4f}%;height:{b['h']:.4f}%;"

    total=0
    for id in IDS:
        tags=[]
        for e in regions[id]:
            style=boxstyle(e['box'])
            label=html.escape(e['label'][:180],quote=True)
            if e['kind']=='link':
                href=html.escape(e['href'],quote=True)
                target=e['target'] or ('_blank' if e['href'].startswith(('https:','http:')) else '')
                attr=f' target="{html.escape(target,quote=True)}" rel="noopener noreferrer"' if target else ''
                tags.append(f'<a class="fm-fidelity-hit" href="{href}" aria-label="{label}" style="{style}"{attr}></a>')
            else:
                action=html.escape(e['action'],quote=True)
                tags.append(f'<button type="button" class="fm-fidelity-hit" data-fm-action="{action}" aria-label="{label}" style="{style}"></button>')
        rx=re.compile(r'(<article\b[^>]*\bid="'+re.escape(id)+r'"[^>]*>)([\s\S]*?)(</article>)',re.I)
        m=rx.search(s)
        assert m
        assert 'fm-page-fidelity' in m.group(2)
        assert 'fm-fidelity-hit' not in m.group(2)
        s=s[:m.start()]+m.group(1)+m.group(2)+''.join(tags)+m.group(3)+s[m.end():]
        total+=len(tags)

    css=r'''
<style id="fm-fidelity-link-hit-v30">
 html body .viewport>.sheet>.fm-fidelity-hit{display:none!important}
 @media screen and (max-width:1024px){
  html body .viewport[data-reading-mode="paged"]>.sheet.is-active>.fm-fidelity-hit{
    box-sizing:border-box!important;display:block!important;position:absolute!important;
    z-index:8!important;margin:0!important;padding:0!important;
    border:0!important;border-radius:0!important;
    background:transparent!important;box-shadow:none!important;
    color:transparent!important;font-size:0!important;
    opacity:0!important;pointer-events:auto!important;cursor:pointer!important;
    touch-action:manipulation!important;
  }
  html body .viewport[data-reading-mode="paged"]>.sheet.is-active>.fm-fidelity-hit:focus-visible{
    opacity:1!important;outline:2px solid #b92372!important;outline-offset:1px!important;
    background:rgba(225,55,133,.08)!important;
  }
 }
 @media print{ html body .viewport>.sheet>.fm-fidelity-hit{display:none!important} }
</style>
'''
    js=r'''
<script id="fm-fidelity-hit-handlers-v30">(function(){
"use strict";
document.addEventListener("click",function(event){
 const hit=event.target.closest(".fm-fidelity-hit[data-fm-action]");
 if(!hit)return;
 const action=hit.dataset.fmAction||"";
 if(action.startsWith("pagespeed:")){
   const n=action.split(":")[1];
   document.querySelector('#current .ps-v17-thumb[data-ps-slide="'+n+'"]')?.click();
   document.querySelector('#current .ps-v22-expand')?.click();
 }else if(action==="pagespeed-full"){
   document.querySelector('#current .ps-v22-expand')?.click();
 }else if(action==="examples-continue"){
   document.querySelector('#examples [data-continue-examples]')?.click();
 }
});
})();</script>
'''
    s=s.replace('</head>',css+'</head>',1).replace('</body>',js+'</body>',1)
    FILE.write_text(s,encoding='utf-8')
    print('CLICKABLE_HOT_REGIONS_INSTALLED',total,'HTML_BYTES',FILE.stat().st_size,flush=True)

async def main():
    update(await inspect())
if __name__=='__main__':asyncio.run(main())
