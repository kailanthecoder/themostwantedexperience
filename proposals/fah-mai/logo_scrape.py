import requests, bs4, re, json, io, subprocess, urllib.parse, pathlib
from PIL import Image
D=pathlib.Path("proposals/fah-mai/brand-assets")
D.mkdir(parents=True,exist_ok=True)
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 Chrome/130 Safari/537.36"})
sites={"fmh":"https://fahmaiholdings.com/","whiskybull":"https://www.whiskybull.com/","platinum":"https://www.platinumcask.com/","mostwanted":"https://usemostwanted.com/"}
all={}
for brand,url in sites.items():
 print("VISITING",brand,url,flush=True)
 try:
  r=s.get(url,timeout=24);print("STATUS",r.status_code,len(r.content),flush=True);r.raise_for_status()
  soup=bs4.BeautifulSoup(r.text,"html.parser")
  c=[]
  def add(src,why,score):
   if not src or src.startswith("data:"):return
   src=urllib.parse.urljoin(url,src)
   if src not in [x["url"] for x in c]:c.append({"url":src,"why":why,"score":score})
  for im in soup.select("img,source"):
   parent=" ".join(str(p.get("class",[]))+" "+str(p.get("id","")) for p in list(im.parents)[:4] if hasattr(p,"get"))
   attrs=" ".join(str(im.get(k,"")) for k in ["alt","class","id","src","data-src","title"])
   score=(70 if "logo" in attrs.lower() else 0)+(40 if re.search("logo|header|navbar|brand|masthead",parent,re.I) else 0)+(12 if re.search("fah|mai|whisky|bull|platinum|wanted|fmh",attrs,re.I) else 0)
   if score>=40:
    for at in ["src","data-src","data-original"]:
     if im.get(at):add(im[at],attrs[:95]+" p:"+parent[:65],score)
  for im in soup.select("link[rel]"):
   if "icon" in str(im.get("rel","")).lower():add(im.get("href"),"favicon",5)
  for style in soup.select("style"):
   for m in re.finditer(r"url\(\s*['\"]?([^'\"\)]+)",style.text):
    if re.search("logo|brand|fmh|whisky|bull",style.text[max(0,m.start()-125):m.end()+60],re.I):add(m.group(1),"CSS logo",30)
  for sh in soup.select('link[rel="stylesheet"][href]')[:8]:
   try:
    css=s.get(urllib.parse.urljoin(url,sh["href"]),timeout=10).text
    for m in re.finditer(r"url\(\s*['\"]?([^'\"\)]+)",css):
     if re.search("logo|brand|fmh|whisky|bull",css[max(0,m.start()-80):m.end()+45],re.I):add(urllib.parse.urljoin(sh["href"],m.group(1)),"CSS logo",30)
   except Exception as e:print("CSS ERROR",str(e)[:80])
  c=sorted(c,key=lambda x:-x["score"])
  data=[]
  for i,item in enumerate(c[:22]):
   try:
    u=item["url"];rr=s.get(u,timeout=15)
    b=rr.content
    if rr.status_code!=200 or len(b)>3500000 or len(b)<150:continue
    if b.lstrip().startswith(b"<svg") or b[:200].find(b"<svg")>=0:ext="svg";dim="svg"
    else:
     im=Image.open(io.BytesIO(b));dim=str(im.size)
     if min(im.size)<40:continue
     ext=im.format.lower()
     if ext=="jpeg":ext="jpg"
     if ext not in ("png","jpg","webp","gif"):continue
    path=D/(brand+"_"+str(i)+'.'+ext);path.write_bytes(b)
    data.append({"file":str(path),"url":u,"dimension":dim,"why":item["why"],"score":item["score"]})
    print("ASSET",brand,i,dim,u,flush=True)
    if len(data)>=8:break
   except Exception as e:print("ASSET ERROR",str(e)[:85])
  all[brand]=data
 except Exception as e:all[brand]={"error":str(e)};print("SITE ERROR",brand,str(e),flush=True)
(D/"manifest.json").write_text(json.dumps(all,indent=2))
