import requests, bs4, re, json, pathlib,urllib.parse
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 Chrome/133 Safari/537.36'
u="https://www.platinumcask.com/"
h=s.get(u,timeout=25);h.raise_for_status();html=h.text
soup=bs4.BeautifulSoup(html,'html.parser')
images=[]
def add(source,context):
 if not source or source.startswith('data:'):return
 url=urllib.parse.urljoin(u,source)
 if not any(x['url']==url for x in images):images.append({'url':url,'context':context[:150]})
for im in soup.select('img,source'):
 for att in ['src','srcset','data-src','data-original','data-srcset']:
  z=im.get(att)
  if z:
   if att.endswith('srcset'):z=z.split(',')[0].strip().split(' ')[0]
   add(z,'tag '+str(im.get('alt',''))+' '+str(im.get('class',[])))
for mat in re.finditer(r"""(?i)(?:url\(['"]?([^)'"]+)|["']([^'"]+\.(?:webp|jpg|jpeg|png)(?:\?[^'"]*)?)["'])""",html):
 z=mat.group(1) or mat.group(2)
 add(z,'html:'+html[max(mat.start()-100,0):mat.end()+100].replace('\n',' '))
for sh in soup.select('link[rel=stylesheet][href]')[:12]:
 try:
  txt=s.get(urllib.parse.urljoin(u,sh['href']),timeout=13).text
  for m in re.finditer(r"url\(['\"]?([^)'\"\s]+)",txt):
   add(urllib.parse.urljoin(sh['href'],m.group(1)),str(sh.get('href',''))[:60]+': '+txt[max(m.start()-100,0):m.end()+80][:140])
 except Exception as e:pass
images=[x for x in images if re.search(r'cask|banner|shop|whole|fraction|bottle|whisk|collection|hero|bg',x['url']+' '+x['context'],re.I)]
p=pathlib.Path('proposals/fah-mai/image-candidates.json');p.write_text(json.dumps(images[:120],indent=2))
print("IMAGE CANDIDATES",len(images),*[(x['url'][:120],x['context'][:50]) for x in images[:25]],sep='\n')
