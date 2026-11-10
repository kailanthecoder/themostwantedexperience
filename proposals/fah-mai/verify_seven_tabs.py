from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from pypdf import PdfReader
import io,base64,json
d=Path('proposals/fah-mai').resolve()
path=d/'index.html'
src=path.read_text()
assert len(src)>500000 and src.count('id="tab-examples"')==1 and src.count('id="examples"')==1
assert src.count("Presented to Louis")>=7 and src.count("Presented by Kailan")>=7
assert "Fah Mai's Re-Envision: A Revenue Focused Ferrari-Design Brand Rehaul For All 3 Sectors" in src
names=['overview','current','spec','proposed','budget','implementation','examples']
shots=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1200,'height':1290},device_scale_factor=1)
 page.goto(path.as_uri(),wait_until='domcontentloaded',timeout=60000)
 page.evaluate('() => document.fonts.ready')
 page.wait_for_timeout(500)
 assert page.locator('[role="tab"]').count()==7
 assert page.locator('article.sheet').count()==7
 for tab in names:
  page.locator(f'#tab-{tab}').click(timeout=10000)
  page.wait_for_timeout(150)
  el=page.locator(f'#'+tab)
  metrics=page.evaluate("""(k) => {
   let x=document.getElementById(k),header=x.querySelector('.presentation-header'), body=x.querySelector('.sheet-body');
   let header_imgs=[...header.querySelectorAll('img')];
   let footer=x.querySelector('.sheet-footer').getBoundingClientRect().top;
   let content=[...body.children].map(el=>Math.round(el.getBoundingClientRect().bottom));
   return {tab:k,dimensions:[x.clientWidth,x.clientHeight],scroll:x.scrollHeight,heading:x.querySelector('h1')?.innerText,
      footerY:Math.round(footer),contentBottom:Math.max(...content),visible:getComputedStyle(x).display,
      images:header_imgs.map(img=>({alt:img.alt,okay:img.naturalWidth>0,center:Math.round(img.getBoundingClientRect().top+img.getBoundingClientRect().height/2)})),
      eyebrow:x.querySelector('.page-index')?.offsetHeight||0,
      headerLabels:[...header.querySelectorAll('.presented-copy')].map(el=>el.innerText)}}""",tab)
  print('CHECK',json.dumps(metrics,ensure_ascii=False),flush=True)
  assert metrics['dimensions'][0] in (793,794,795) and metrics['dimensions'][1]>=1120
  assert metrics['images'] and all(i['okay'] for i in metrics['images'])
  assert max(i['center'] for i in metrics['images'])-min(i['center'] for i in metrics['images'])<=6
  assert metrics['eyebrow']==0
  if metrics['contentBottom']>metrics['footerY']+6:
   print('WARNING CONTENT TOUCHING FOOTER',tab,metrics['contentBottom']-metrics['footerY'],flush=True)
  shots.append(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
 # Navigation click via actual browser
 page.locator('#tab-examples').click()
 assert page.locator('#examples').evaluate('(el)=>getComputedStyle(el).display')!='none'
 assert page.locator('#examples .example-card').count()==4
 for card in page.locator('#examples .example-card').all():
  assert card.get_attribute('href').startswith('https://')
 mobile=browser.new_page(viewport={'width':430,'height':930},device_scale_factor=1)
 mobile.goto(path.as_uri(),wait_until='domcontentloaded',timeout=60000)
 mobile.wait_for_timeout(200)
 mobile.screenshot(path=str(d/'Fah-Mai-Seven-Tabs-Mobile.png'),full_page=False)
 page.pdf(path=str(d/'Fah-Mai-Seven-Tabs-A4.pdf'),format='A4',print_background=True,
  margin={'top':'0','right':'0','bottom':'0','left':'0'},prefer_css_page_size=True)
 browser.close()
pdf=d/'Fah-Mai-Seven-Tabs-A4.pdf'
assert len(PdfReader(pdf).pages)==7,'Must export exactly seven A4 sheets'
print('FINAL PDF',len(PdfReader(pdf).pages),'pages',round(pdf.stat().st_size/1e6,2),'MB',flush=True)
W,H=392,553
contact=Image.new('RGB',(W*4+70,H*2+50),'#ece8ec')
for i,im in enumerate(shots):
 im.thumbnail((W,H))
 contact.paste(im,(14+(i%4)*(W+14),14+(i//4)*(H+14)))
jpeg=d/'Fah-Mai-Seven-Tabs-Contact.jpg'
contact.save(jpeg,quality=78,optimize=True)
(d/'Fah-Mai-Seven-Tabs-Contact.b64.txt').write_text(base64.b64encode(jpeg.read_bytes()).decode())
