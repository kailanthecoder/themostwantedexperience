from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from pypdf import PdfReader
import io,base64,json
d=Path('proposals/fah-mai').resolve()
p=d/'index.html'
s=p.read_text()
assert len(s)>1_000_000 and 'id="fahmai-first-page-statement-v11"' in s
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1220,'height':1340},device_scale_factor=1)
 page.goto(p.as_uri(),wait_until='domcontentloaded',timeout=60000)
 page.evaluate("() => document.fonts.ready")
 page.wait_for_timeout(400)
 assert page.locator('nav.tabs button.tab').count()==7
 assert page.locator('#overview .vision-card').count()==3
 assert page.locator('#overview .promise svg').count()==7
 assert page.locator('#overview .stage-card').count()==3
 assert page.locator('#overview .signoff-photo img').count()==1
 assert page.locator('#overview .signoff-contact a').count()==2
 q=page.evaluate("""() => {
  const root=document.querySelector('#overview'),f=root.querySelector('.sheet-footer');
  const selectors=['.page-heading','.vision-intro','.vision-grid','.roadmap-callout','.stage-runway','.personal-signoff','.sheet-footer'];
  return {sheet:[root.clientWidth,root.clientHeight],scrollHeight:root.scrollHeight,blocks:selectors.map(sel=>{const n=root.querySelector(sel),r=n.getBoundingClientRect();return {name:sel,top:Math.round(r.top),bottom:Math.round(r.bottom),height:Math.round(r.height)}}),font:getComputedStyle(root.querySelector('h1')).fontFamily,cardDims:[...root.querySelectorAll('.vision-card')].map(x=>{let r=x.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]}),portraitLoaded:root.querySelector('.signoff-photo img').naturalWidth>0};
 }""")
 print('PAGE_CHECK',json.dumps(q),flush=True)
 assert q['portraitLoaded'],"Booking portrait failed"
 assert len(q['cardDims'])==3 and all(abs(x[0]-x[1])<=2 for x in q['cardDims']),q['cardDims']
 assert q['blocks'][-2]['bottom']<=q['blocks'][-1]['top']+3, 'Signoff overlaps A4 footer'
 assert q['scrollHeight']<=q['sheet'][1]+4, 'Content overflows A4 sheet'
 img=Image.open(io.BytesIO(page.locator('#overview').screenshot())).convert('RGB')
 io2=io.BytesIO();img.save(io2,format='JPEG',quality=80,optimize=True)
 (d/'overview-v11-a4.jpg').write_bytes(io2.getvalue())
 (d/'overview-v11-a4.b64.txt').write_text(base64.b64encode(io2.getvalue()).decode())
 page.screenshot(path=str(d/'overview-v11-desktop.jpg'),type='jpeg',quality=75,full_page=False)
 (d/'overview-v11-desktop.b64.txt').write_text(base64.b64encode((d/'overview-v11-desktop.jpg').read_bytes()).decode())
 mobile=b.new_page(viewport={'width':390,'height':830},device_scale_factor=1,is_mobile=True,has_touch=True)
 mobile.goto(p.as_uri(),wait_until='domcontentloaded',timeout=60000)
 mobile.wait_for_timeout(300)
 m=mobile.evaluate("""() => {let x=document.querySelector('#overview');let r=x.getBoundingClientRect();return {w:window.innerWidth,overflow:document.documentElement.scrollWidth,canvasRight:Math.round(r.right),zoom:getComputedStyle(x).zoom}}""")
 print('MOBILE_CHECK',json.dumps(m),flush=True)
 assert m['overflow']<=m['w']+5
 page.pdf(path=str(d/'Fah-Mai-Proposal-Glass.pdf'),format='A4',print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'},prefer_css_page_size=True)
 b.close()
n=len(PdfReader(d/'Fah-Mai-Proposal-Glass.pdf').pages)
print('PDF_PAGES',n,'SIZE', (d/'Fah-Mai-Proposal-Glass.pdf').stat().st_size,flush=True)
assert n==7, 'Must have exactly 7 A4 pages'
