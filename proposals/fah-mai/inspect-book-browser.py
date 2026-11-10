from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,requests,urllib.parse,base64,io
from PIL import Image
p=Path('proposals/fah-mai')
with sync_playwright() as q:
 b=q.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1360,'height':1000},device_scale_factor=1)
 page.goto('https://book.usemostwanted.com/',wait_until='domcontentloaded',timeout=60000)
 page.wait_for_timeout(2200)
 page.screenshot(path=str(p/'book-site-live.jpg'),type='jpeg',quality=78,full_page=False)
 data=page.evaluate(r"""() => ({
    title:document.title,
    images:[...document.querySelectorAll('img')].map((e,i)=>({i,src:e.currentSrc||e.src,alt:e.alt,w:e.naturalWidth,h:e.naturalHeight,display:getComputedStyle(e).display})),
    backgrounds:[...document.querySelectorAll('*')].map((e,i)=>({i,cls:typeof e.className==='string'?e.className.slice(0,90):'',bg:getComputedStyle(e).backgroundImage})).filter(x=>x.bg && x.bg!=='none').slice(0,80),
    resourceImages:performance.getEntriesByType('resource').filter(x=>/\.(png|jpg|jpeg|webp)(\?|$)/i.test(x.name)).slice(0,140).map(x=>x.name),
    htmlHasName:document.body.innerText.toLowerCase().includes('kailan')
 })""")
 print("RENDERED",data['title'],"IMAGES",len(data['images']),"BACKGROUNDS",len(data['backgrounds']),"resources",len(data['resourceImages']),flush=True)
 (p/'book-image-metadata.json').write_text(json.dumps(data,indent=2))
 candidates={}
 def add(url,reason):
  if not url or url.startswith('data:'):return
  candidates[url]=reason
 for im in data['images']:add(im['src'],"img "+im['alt'])
 for im in data['backgrounds']:
  for u in re.findall(r"url\\(['\"]?([^'\"\\)]+)",im['bg']):add(urllib.parse.urljoin(page.url,u),"css "+im['cls'])
 for u in data['resourceImages']:add(u,'resource')
 print('FOUND',len(candidates),'CANDIDATES',flush=True)
 session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 Chrome/130 Safari/537.36'
 items=[]
 for i,(url,why) in enumerate(candidates.items()):
  if i>75:break
  try:
   rr=session.get(url,timeout=18)
   if rr.status_code!=200 or len(rr.content)>8500000:continue
   im=Image.open(io.BytesIO(rr.content))
   if im.width<100 or im.height<110:continue
   im.thumbnail((450,450))
   img=im.convert('RGB')
   buf=io.BytesIO();img.save(buf,format='JPEG',quality=70,optimize=True)
   (p/f'portrait-candidate-{i}.jpg').write_bytes(buf.getvalue())
   (p/f'portrait-candidate-{i}.b64.txt').write_text(base64.b64encode(buf.getvalue()).decode())
   items.append({"i":i,"url":url,"why":why,"dimensions":list(im.size),"bytes":len(rr.content)})
   print('CANDIDATE',i,url[:160],why[:50],im.size,flush=True)
  except Exception as exc:print('FETCH ERROR',i,str(exc)[:150],flush=True)
 (p/'portrait-browser-candidates.json').write_text(json.dumps(items,indent=2))
 b.close()
