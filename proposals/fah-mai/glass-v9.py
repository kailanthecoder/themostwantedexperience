from pathlib import Path
import re, html, json
from bs4 import BeautifulSoup

p=Path("proposals/fah-mai/index.html")
src=p.read_text()
assert len(src)>1_000_000, f"Unexpectedly short source: {len(src)}"
assert 'id="tab-examples"' in src and 'id="tab-proposed"' in src and 'id="overview"' in src
assert 'id="glass-navigation-final-v9"' not in src

# 1. Place the proposals tab in the visually separated sixth position.
m=re.search(r'(<nav\b[^>]*class="tabs"[^>]*>)([\s\S]*?)(</nav>)',src)
assert m,"Could not locate existing navigation"
start,contents,end=m.groups()
buttons={}
for match in re.finditer(r'<button\b[\s\S]*?</button>',contents):
    token=match.group(0)
    target=re.search(r'data-target="([^"]+)"',token)
    assert target,token[:180]
    buttons[target.group(1)]=token
desired=['overview','current','spec','budget','implementation','proposed','examples']
assert len(buttons)==7 and set(buttons)==set(desired), list(buttons)
buttons['proposed']=re.sub(r'>Proposed</button>',r'>Proposals</button>',buttons['proposed'])
buttons['proposed']=buttons['proposed'].replace('class="tab"','class="tab tab-proposals"')
assert '>Proposals</button>' in buttons['proposed']
newnav=start+''.join(buttons[k] for k in desired)+end
src=src[:m.start()]+newnav+src[m.end():]

# 2. Keep A4 print order synchronized with the seven top tabs.
matches=list(re.finditer(r'<article\b[^>]*class="sheet[^"]*"[^>]*>[\s\S]*?</article>',src))
assert len(matches)==7, f"Expected seven A4 articles; got {len(matches)}"
sheets={}
for x in matches:
    token=x.group(0)
    idmatch=re.search(r'<article\b[^>]*id="([^"]+)"',token)
    assert idmatch
    sheets[idmatch.group(1)]=token
assert set(sheets)==set(desired),list(sheets)

# 3. Rewrite the requested overview content: clear, persuasive and specific.
overview_soup=BeautifulSoup(sheets['overview'],'html.parser')
overview=overview_soup.find('article')
heading=overview.select_one('.page-heading h1')
intro=overview.select_one('.page-heading .sub')
statement=overview.select_one('.statement')
assert heading and intro and statement, 'Could not find overview title, intro or key pitch block'

new_heading="Fah Mai Holdings Re-Envisioned: A Revenue Focused Ferrari-Design Brand Rehaul For All 3 Sectors"
new_sub=("An execution-led proposal for a 2026 A-tier web package across Fah Mai Holdings, "
         "Platinum Cask and Whisky Bull: stunningly responsive, AI-assisted sites, future-ready "
         "technology and industry-leading design.")
new_pitch=("Under Kailan’s leadership, Most Wanted specialises in exactly the kind of digital transformation "
           "that can propel Fah Mai into its next growth phase. I set out to demonstrate the vision "
           "by building the three sites with my existing AI-assisted tech stack, but reached my available "
           "AI credits before completing them. This concise proposal sets out the design direction, "
           "commercial opportunity and plan to deliver.")

heading.clear()
heading.append(new_heading)
intro.clear()
intro.append(new_sub)
statement.clear()
statement.append(new_pitch)
sheets['overview']=str(overview)
src=src[:matches[0].start()]+''.join(sheets[k] for k in desired)+src[matches[-1].end():]

# 4. Brighter navigation in frosted glass. Distinct pink sixth tab.
css=r'''
<style id="glass-navigation-final-v9">
@media screen{
 html{scroll-padding-top:120px}
 .toolbar{
  position:sticky!important;top:0!important;z-index:1000!important;
  background:linear-gradient(115deg,rgba(255,255,255,.94) 0%,rgba(255,249,252,.88) 55%,rgba(251,225,239,.93) 100%)!important;
  -webkit-backdrop-filter:blur(25px) saturate(165%)!important;
  backdrop-filter:blur(25px) saturate(165%)!important;
  border-bottom:1px solid rgba(215,111,165,.3)!important;
  box-shadow:0 10px 28px rgba(67,27,52,.105),inset 0 1px 0 rgba(255,255,255,.9)!important;
 }
 .toolbar-inner{box-sizing:border-box!important;max-width:1380px!important;width:100%!important;
  display:grid!important;grid-template-columns:auto minmax(0,1fr) auto!important;align-items:center!important;
  gap:16px!important;min-height:83px!important;height:auto!important;padding:10px 20px!important}
 .tool-brand{font-family:'Poppins','Figtree',Arial,sans-serif!important;color:#231824!important;
  font-size:14px!important;font-weight:900!important;letter-spacing:-.28px!important;white-space:nowrap!important}
 .tool-brand span{color:#e72982!important;font-weight:900!important;margin:0 4px!important}
 .tabs{min-width:0!important;max-width:100%!important;display:flex!important;align-items:center!important;
  justify-content:flex-start!important;flex-wrap:nowrap!important;gap:5px!important;
  overflow-x:auto!important;overflow-y:hidden!important;white-space:nowrap!important;
  scrollbar-width:none!important;scrollbar-color:transparent transparent!important;
  padding:6px 3px!important;-webkit-overflow-scrolling:touch!important;scroll-snap-type:x proximity}
 .tabs::-webkit-scrollbar{display:none!important}
 .tabs .tab{box-sizing:border-box!important;position:relative!important;flex:0 0 auto!important;
  scroll-snap-align:center!important;border:1px solid transparent!important;border-radius:11px!important;
  padding:0 13px!important;min-height:45px!important;height:45px!important;
  font-family:'Poppins','Figtree',Arial,sans-serif!important;font-size:13.2px!important;
  font-weight:800!important;letter-spacing:-.16px!important;line-height:1!important;text-transform:none!important;
  background:rgba(255,255,255,.48)!important;color:#362b34!important;
  box-shadow:none!important;transition:background .15s,color .15s,box-shadow .15s!important}
 .tabs .tab:hover{background:#fff!important;color:#b42468!important;border-color:rgba(227,86,146,.15)!important}
 .tabs .tab[aria-selected="true"]{
  background:linear-gradient(120deg,#db2178,#f04496)!important;color:white!important;
  border:1px solid rgba(195,27,104,.35)!important;
  box-shadow:0 4px 13px rgba(211,35,113,.22),inset 0 1px 0 rgba(255,255,255,.35)!important}
 .tabs #tab-proposed{margin-left:19px!important;background:rgba(255,225,238,.95)!important;
  color:#9f155e!important;border:1px solid rgba(214,40,118,.53)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.8)!important}
 .tabs #tab-proposed:before{content:'';position:absolute;left:-12px;top:8px;height:27px;
  width:1px;background:#d9a4bc}
 .tabs #tab-proposed[aria-selected="true"]{background:linear-gradient(120deg,#c91369,#eb348a)!important;
  color:#fff!important;border-color:#bc145c!important;
  box-shadow:0 5px 16px rgba(193,32,106,.24)!important}
 .tool-actions{display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:9px!important}
 .tool-actions .status{display:none!important}
 .pdf-btn{font-family:'Poppins','Figtree',Arial,sans-serif!important;font-size:12px!important;
  font-weight:800!important;min-height:46px!important;padding:0 18px!important;
  border-radius:12px!important;background:linear-gradient(115deg,#e72982,#fa559f)!important;
  color:#fff!important;box-shadow:0 5px 14px rgba(212,31,114,.19)!important;white-space:nowrap!important}
 .pdf-btn:hover{filter:brightness(1.06)}
 .sheet .page-heading h1{font-size:37px!important;font-weight:900!important;line-height:1.13!important;
  letter-spacing:-1.12px!important}
 .sheet .page-heading .sub{font-size:13.3px!important;font-weight:600!important;line-height:1.57!important;color:#665c64!important}
 .sheet .statement{font-size:15px!important;font-weight:700!important;line-height:1.45!important}
 #overview .page-heading h1{font-size:28.3px!important;line-height:1.18!important}
 .feature h3,.spec-item h3,.phase h3{font-weight:800!important}
}
@media screen and (max-width:1190px){
 .toolbar-inner{grid-template-columns:minmax(0,1fr) auto!important;gap:8px 12px!important;min-height:0!important;padding:9px 16px 10px!important}
 .tool-brand{grid-column:1!important;grid-row:1!important;font-size:13px!important}
 .tool-actions{grid-column:2!important;grid-row:1!important}
 .tabs{grid-row:2!important;grid-column:1/-1!important;gap:7px!important;padding:4px 0 3px!important}
 .tabs .tab{font-size:14px!important;height:46px!important;min-height:46px!important;padding:0 17px!important}
 .pdf-btn{font-size:11px!important;min-height:40px!important;padding:0 13px!important}
}
@media screen and (max-width:590px){
 .toolbar-inner{padding:9px 12px 8px!important}
 .tool-brand{font-size:12.7px!important}
 .pdf-btn{font-size:10px!important;min-height:37px!important;padding:0 11px!important}
 .tabs{gap:6px!important}
 .tabs .tab{font-size:13.7px!important;min-height:44px!important;height:44px!important;padding:0 15px!important}
 .tabs #tab-proposed{margin-left:21px!important}
 .viewport{box-sizing:border-box!important;width:100%!important;max-width:100%!important;
  overflow-x:hidden!important;padding:12px 8px 24px!important}
 .sheet{margin-left:auto!important;margin-right:auto!important;max-width:none!important}
}
@media print{
 .toolbar{display:none!important}
 .sheet .page-heading h1{font-size:35px!important;font-weight:900!important}
 #overview .page-heading h1{font-size:28px!important}
}
</style>
'''
assert '</head>' in src
src=src.replace('</head>',css+'</head>',1)

# Mobile shrink-to-fit rather than sideways-scrolling an A4 sheet.
js=r'''
<script id="sheet-mobile-fit-v9">
(function(){
 function fit(){
  var compact=window.innerWidth<800;
  var factor=compact?Math.min(1,Math.max(.25,(window.innerWidth-18)/794)):1;
  document.querySelectorAll('article.sheet').forEach(function(el){
   if(compact){el.style.zoom=String(factor)}else{el.style.removeProperty('zoom')}
  });
 }
 fit();
 window.addEventListener('resize',fit,{passive:true});
 document.querySelectorAll('nav.tabs button.tab').forEach(function(tab){
  tab.addEventListener('click',function(){
   if(window.innerWidth<1190){tab.scrollIntoView({block:'nearest',inline:'center',behavior:'smooth'})}
  });
 });
 window.addEventListener('beforeprint',function(){
  document.querySelectorAll('article.sheet').forEach(function(el){el.style.zoom='1'})
 });
 window.addEventListener('afterprint',fit);
})();
</script>'''
assert '</body>' in src
src=src.replace('</body>',js+'</body>',1)
p.write_text(src)
print('UPDATED',p.stat().st_size, 'bytes')
print('HEADLINE',new_heading)
print('SUB',new_sub)
print('PITCH',new_pitch)
print('TABS',desired)
