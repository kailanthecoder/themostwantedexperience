import pathlib,requests,bs4,re,urllib.parse,json,base64,io,sys
from PIL import Image
p=pathlib.Path("proposals/fah-mai")
url="https://book.usemostwanted.com/"
s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0 Chrome/131 Safari/537.36"})
res=s.get(url,timeout=25)
print("BOOK STATUS",res.status_code,"FINAL",res.url,"BYTES",len(res.content),flush=True)
doc=bs4.BeautifulSoup(res.text,"html.parser")
cands=[]
for im in doc.select("img"):
 for attr in ("src","data-src","srcset"):
  raw=im.get(attr,"")
  if attr=="srcset":raw=raw.split(",")[0].strip().split(" ")[0]
  if raw and not raw.startswith("data:"):
   u=urllib.parse.urljoin(res.url,raw)
   if u not in [e["url"] for e in cands]:
    cands.append({"url":u,"alt":im.get("alt",""),"class":im.get("class",""),"context":str(im.parent)[:160]})
for m in re.finditer(r'(https?:)?//[^"\s<>]+\.(?:png|webp|jpg|jpeg)',res.text):
 u=urllib.parse.urljoin(res.url,m.group(0))
 if u not in [e["url"] for e in cands]:cands.append({"url":u,"alt":"","class":[],"context":"html"})
print("CANDIDATE URLS",len(cands),flush=True)
out=[]
for i,o in enumerate(cands[:35]):
 try:
  r=s.get(o["url"],timeout=20)
  if r.status_code!=200 or len(r.content)>9000000:continue
  im=Image.open(io.BytesIO(r.content)).convert("RGB")
  if im.width<100 or im.height<120:continue
  im.thumbnail((350,350))
  b=io.BytesIO();im.save(b,format="JPEG",quality=67,optimize=True)
  f=p/f"portrait-source-{i}.jpg"
  f.write_bytes(b.getvalue())
  (p/f"portrait-source-{i}.b64.txt").write_text(base64.b64encode(b.getvalue()).decode())
  out.append(dict(i=i,url=o["url"],alt=o["alt"],width=im.width,height=im.height,source_size=len(r.content)))
  print("CANDIDATE",i,o["url"],"SIZE",im.size,"ALT",o["alt"],flush=True)
 except Exception as exc:print("ERROR",i,str(exc)[:120],flush=True)
(p/"portrait-candidates.json").write_text(json.dumps(out,indent=2))
htmlpath=p/"index.html"
html=htmlpath.read_text()
soup=bs4.BeautifulSoup(html,"html.parser")
overview=soup.select_one("#overview")
assert overview is not None
body=overview.select_one(".sheet-body")
sections=[]
for c in body.children:
 if not getattr(c,'name',None): continue
 sections.append({"element":c.name,"class":c.get("class"),"html":str(c)[:12000],"text":c.get_text(' ',strip=True)[:1300]})
(p/"overview-dom-inspection.json").write_text(json.dumps(sections,ensure_ascii=False,indent=2))
print("OVERVIEW CHILDREN",[(x["element"],x["class"]) for x in sections],flush=True)
