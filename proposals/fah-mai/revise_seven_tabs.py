from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import re, io, base64, requests
from PIL import Image

path=Path("proposals/fah-mai/index.html")
html=path.read_text()
assert len(html)>500_000 and html.lstrip().lower().startswith("<!doctype html"), "Original proposal source missing or unexpectedly short"
assert "id=\"tab-examples\"" not in html, "Examples already inserted: refusing duplicate operation"

soup=BeautifulSoup(html,"html.parser")
brand_names=["brand-fmh","brand-bull","brand-pc"]
brand_elems=[soup.select_one("#overview ."+name) for name in brand_names]
mw=soup.select_one("#overview .mw-black")
signature=soup.select_one("#overview .signature-logo")
wave=soup.select_one("#overview .waveblock")
if any(v is None for v in brand_elems+[mw,signature,wave]):
 raise Exception("One of the official brandmarks is missing; cannot safely regenerate headers")
for e in brand_elems+[mw]:
 if not e.find("img"): raise Exception("Official image is missing in a header")
left="".join(str(e) for e in brand_elems)
right=str(mw)+str(signature)
header=f'''<div class="identity presentation-header">
 <section class="presented-group presented-to" aria-label="Presented to Louis on behalf of">
  <h2 class="presented-copy">Presented to Louis <span>on behalf of</span></h2>
  <div class="client-lockups">{left}</div>
 </section>
 <section class="presented-group presented-by" aria-label="Presented by Kailan on behalf of">
  <h2 class="presented-copy">Presented by Kailan <span>on behalf of</span></h2>
  <div class="presenter-lockups">{right}</div>
 </section>
 </div><div class="presentation-hairline"></div>
'''
pattern=r'<div class="identity">[\s\S]*?<div class="waveblock"'
html,count=re.subn(pattern,lambda m: header+'<div class="waveblock"',html)
assert count==6,f"Expected six headers, found {count}"

# Eyebrow labels should not occupy any of the printed A4 layout.
for rgx in [r'<div class="page-index">[\s\S]*?</div>',r'<div class="tagline">[\s\S]*?</div>']:
 html,count=re.subn(rgx,'',html)
 assert count==6, f"Expected six eyebrow groups for {rgx}; got {count}"
# Original header title is replaced verbatim with the user's requested copy.
headline="Fah Mai's Re-Envision: A Revenue Focused Ferrari-Design Brand Rehaul For All 3 Sectors"
heading_reg=r'(<article class="sheet is-active" id="overview"[\s\S]*?<h1>)[\s\S]*?(</h1>)'
html, count=re.subn(heading_reg,lambda m:m.group(1)+escape(headline,quote=False)+m.group(2),html,count=1)
assert count==1 and headline in html

# Amend navigation, interactive URLs, and visible document metadata to seven tabs.
nav_button='<button class="tab" id="tab-examples" role="tab" aria-controls="examples" aria-selected="false" data-target="examples" tabindex="-1">Examples</button>'
html,count=re.subn(r'(data-target="implementation" tabindex="-1">Implementation</button>)(</nav>)',lambda m:m.group(1)+nav_button+m.group(2),html,count=1)
assert count==1,"Implementation navigation control was not found"
html=html.replace('A4 · 6 SECTIONS','A4 · 7 TABS').replace("' / 06'","' / 07'")
# Replace toolbar's micro-eyebrow with readable brand label.
html=re.sub(r'<div class="tool-brand">[\s\S]*?</div>','<div class="tool-brand">FAH MAI <span>×</span> MOST WANTED</div>',html,count=1)

# Capture real, live examples; no fictional portfolio thumbnails.
sites=[
 ("Most Wanted","Website design, marketing and sales systems","https://usemostwanted.com/","mostwanted"),
 ("Spanish with Kailan","Spanish learning and lesson booking","https://spanish.workwithkailan.com/","spanish"),
 ("Closer with Kailan","High-ticket sales portfolio","https://closer.workwithkailan.com/","closer"),
 ("Work with Kailan","Life strategy and coaching","https://workwithkailan.com/","workwithkailan")
]
shots={}
try:
 from playwright.sync_api import sync_playwright
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for label,desc,url,key in sites:
   tab=browser.new_page(viewport={"width":1130,"height":700},device_scale_factor=1)
   try:
    response=tab.goto(url,wait_until="domcontentloaded",timeout=15000)
    tab.wait_for_timeout(650)
    if response and response.status<400:
     raw=tab.screenshot(type="jpeg",quality=60,animations="disabled")
     img=Image.open(io.BytesIO(raw)).convert("RGB")
     img.thumbnail((800,500))
     buf=io.BytesIO()
     img.save(buf,format="WEBP",quality=57,method=5)
     shots[key]='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
     print("EXAMPLE PHOTO",key,"HTTP",response.status,"BYTES",len(buf.getvalue()),flush=True)
    else:print("EXAMPLE UNAVAILABLE",key,response.status if response else "none",flush=True)
   except Exception as ex:print("EXAMPLE PHOTO FAILED",key,str(ex)[:160],flush=True)
   finally:tab.close()
  browser.close()
except Exception as ex:print("BROWSER PHOTO TOOL UNAVAILABLE",str(ex)[:200],flush=True)

card_html=[]
for label,desc,url,key in sites:
 image=shots.get(key)
 preview=(f'<img class="example-screenshot" src="{image}" alt="{escape(label)} website screenshot" loading="eager">' if image
  else f'<div class="example-fallback"><strong>{escape(label)}</strong></div>')
 card_html.append(f'''<a class="example-card" href="{escape(url)}" target="_blank" rel="noopener noreferrer">
  <div class="example-media">{preview}</div>
  <div class="example-copy"><div><h3>{escape(label)}</h3><p>{escape(desc)}</p></div><span class="example-arrow" aria-hidden="true">↗</span></div>
 </a>''')
example_sheet=f'''<article class="sheet" id="examples" role="tabpanel" aria-labelledby="tab-examples">
 <div class="sheet-cap"></div>{header}{str(wave)}
 <div class="sheet-body">
  <div class="page-heading"><div class="page-heading-copy">
   <h1>Selected <em>work.</em><br>Four live examples.</h1>
   <p class="sub">A selection of websites, brand experiences and conversion-focused projects.</p>
  </div></div>
  <div class="sheet-section examples-section">
   <div class="example-grid">{''.join(card_html)}</div>
   <div class="example-footer-note">Each card opens the website in a new browser tab.</div>
  </div>
 </div>
 <footer class="sheet-footer"></footer>
</article>'''
html,count=re.subn(r'</article></main><script>',lambda m:'</article>'+example_sheet+'</main><script>',html,count=1)
assert count==1,"Could not locate end of implementation sheet / beginning of main script"

style=r'''
<style id="fahmai-presentation-header-seven-tabs">
/* Heading / card typography based on Fah Mai's Poppins and Figtree website. */
.page-index,.heading-top,.tagline,.tag-note,.small-label,.feature-index,.footer-kicker,.footer-right,.footer-page,.presenter-label,.proofline .small-label{display:none!important}
.sheet-footer{height:17px!important;min-height:17px!important;margin-top:auto!important;border-top:1px solid #f0e7ec!important;padding:0!important}
.sheet-footer>*{display:none!important}
.sheet-cap{height:4px!important;min-height:4px!important;background:linear-gradient(90deg,#e72982 0%,#ff91c3 48%,#e72982 100%)!important}
.presentation-header{box-sizing:border-box!important;width:100%!important;height:141px!important;min-height:141px!important;padding:13px 38px 9px!important;display:grid!important;grid-template-columns:minmax(0,1.24fr) minmax(0,1fr)!important;column-gap:25px!important;align-items:center!important;justify-content:stretch!important}
.presented-group{min-width:0!important;min-height:114px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important}
.presented-to{border-right:1px solid #e9d9e2!important;padding-right:21px!important}
.presented-by{padding-left:2px!important}
.presented-copy{display:block!important;text-align:center!important;margin:0 0 10px!important;color:#231b22!important;font-family:'Poppins','Figtree',Arial,sans-serif!important;font-size:16.2px!important;font-weight:800!important;line-height:1.14!important;letter-spacing:-.65px!important}
.presented-copy span{display:block!important;font-weight:800!important}
.presentation-header .client-lockups{width:100%!important;height:61px!important;min-height:61px!important;gap:17px!important;align-items:center!important;justify-content:center!important;flex:0 0 61px!important}
.presentation-header .client-lockups .original-brand{height:61px!important;min-height:61px!important;display:flex!important;align-items:center!important;justify-content:center!important;margin:0!important;padding:0!important;min-width:0!important;flex:0 0 auto!important;opacity:1!important}
.presentation-header .original-brand img{display:block!important;object-fit:contain!important;object-position:center center!important;margin:auto!important;padding:0!important;mix-blend-mode:normal!important}
.presentation-header .brand-fmh{width:63px!important}.presentation-header .brand-fmh img{height:58px!important;width:58px!important;max-height:58px!important;max-width:58px!important}
.presentation-header .brand-bull{width:66px!important}.presentation-header .brand-bull img{height:60px!important;width:55px!important;max-height:60px!important;max-width:55px!important}
.presentation-header .brand-pc{width:151px!important}.presentation-header .brand-pc img{width:145px!important;max-width:145px!important;height:54px!important;max-height:54px!important}
.presentation-header .presenter-lockups{width:100%!important;height:61px!important;min-height:61px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:22px!important;margin:0!important}
.presentation-header .mw-black{display:flex!important;align-items:center!important;justify-content:center!important;width:61px!important;height:61px!important;min-width:61px!important;max-width:61px!important;background:transparent!important;border:0!important;box-shadow:none!important;margin:0!important;padding:0!important}
.presentation-header .mw-black img{display:block!important;object-fit:contain!important;width:56px!important;height:56px!important;max-width:56px!important;max-height:56px!important;filter:brightness(0)!important;margin:0!important;background:transparent!important}
.presentation-header .presenter-separator{display:none!important}
.presentation-header .signature-logo{display:block!important;width:79px!important;height:44px!important;max-width:79px!important;max-height:44px!important;object-fit:contain!important;margin:0!important}
.presentation-hairline{height:1px!important;background:#ece2e7!important;flex:0 0 1px!important;margin:0 40px!important}
.waveblock{margin:0!important;flex-shrink:0!important}
.sheet-body{padding-top:19px!important}
.page-heading .page-heading-copy{max-width:100%!important}
#overview .page-heading h1{font-size:28px!important;line-height:1.14!important;letter-spacing:-1.05px!important;font-weight:800!important;max-width:690px!important}
.page-heading{padding-bottom:11px!important}
.sheet-section{padding-top:15px!important}
.tool-brand{font-family:'Figtree',Arial,sans-serif!important;letter-spacing:0!important;text-transform:none!important;font-weight:800!important;font-size:11px!important}
.toolbar .status{display:none!important}
.examples-section{padding-top:17px!important}
.example-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.example-card{display:block;overflow:hidden;background:#fff;border:1px solid #eee1e7;border-radius:18px;text-decoration:none;color:#261e25;box-shadow:0 6px 18px rgba(51,27,38,.035);transition:transform .18s,box-shadow .18s}
.example-card:hover{transform:translateY(-2px);box-shadow:0 9px 22px rgba(67,21,46,.12)}
.example-media{height:170px;width:100%;overflow:hidden;background:linear-gradient(125deg,#31242f,#e72c85)}
.example-screenshot{display:block;width:100%;height:100%;object-fit:cover;object-position:top center}
.example-fallback{height:100%;width:100%;display:flex;align-items:center;justify-content:center;padding:15px;color:#fff;font-family:'Poppins',sans-serif;font-size:21px;text-align:center}
.example-copy{padding:15px 17px 17px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.example-copy h3{font-family:'Poppins',sans-serif!important;font-size:15px!important;font-weight:800!important;letter-spacing:-.4px;margin:0 0 4px}
.example-copy p{margin:0;font-size:10.5px;line-height:1.44;color:#736970}
.example-arrow{color:#e72982;font-weight:800;font-size:24px}
.example-footer-note{font-size:10px;color:#8d7e86;margin:18px 3px 0}
@media(max-width:650px){
 .presentation-header{height:121px!important;min-height:121px!important;padding:10px 15px 6px!important;gap:7px!important;grid-template-columns:minmax(0,1.27fr) minmax(0,1fr)!important}
 .presented-group{min-height:103px!important}
 .presented-copy{font-size:11px!important;letter-spacing:-.25px!important;line-height:1.17!important;margin-bottom:9px!important}
 .presented-to{padding-right:8px!important}
 .presentation-header .client-lockups{gap:5px!important;height:46px!important;min-height:46px!important;flex-basis:46px!important}
 .presentation-header .original-brand{height:46px!important;min-height:46px!important}
 .presentation-header .brand-fmh{width:40px!important}.presentation-header .brand-fmh img{width:37px!important;height:37px!important}
 .presentation-header .brand-bull{width:42px!important}.presentation-header .brand-bull img{width:39px!important;height:43px!important}
 .presentation-header .brand-pc{width:90px!important}.presentation-header .brand-pc img{width:87px!important;height:40px!important}
 .presentation-header .presenter-lockups{gap:6px!important;height:45px!important;min-height:45px!important}
 .presentation-header .mw-black{height:43px!important;width:43px!important;min-width:43px!important}
 .presentation-header .mw-black img{width:40px!important;height:40px!important}
 .presentation-header .signature-logo{height:28px!important;width:51px!important}
 .presentation-hairline{margin:0 15px!important}
 #overview .page-heading h1{font-size:25px!important}
 .example-grid{gap:8px!important}.example-media{height:136px!important}.example-copy{padding:9px 10px 12px!important}
 .example-copy h3{font-size:11px!important}.example-copy p{font-size:8.5px!important}
}
@media print{
 .presentation-header .client-lockups .original-brand img,
 .presentation-header .mw-black img,.presentation-header .signature-logo{print-color-adjust:exact!important;-webkit-print-color-adjust:exact!important}
 .example-card{box-shadow:none!important;break-inside:avoid!important}
}
</style>
'''
assert '</head>' in html
html=html.replace('</head>',style+'</head>',1)
path.write_text(html)
print("PATCHED:",path.stat().st_size,"characters, images:",len(shots),"new tabs:",html.count('id="tab-examples"'),"new sheets:",html.count('id="examples"'),flush=True)
