import requests, re, json, pathlib, bs4
u='https://fahmaiholdings.com/'
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 Chrome/130 Safari/537.36'
r=s.get(u,timeout=30);r.raise_for_status()
soup=bs4.BeautifulSoup(r.text,'html.parser')
fonts=[]
def pick(src,text):
 for rule in re.findall(r'(?:font-family\s*:\s*[^;}]+|font-weight\s*:\s*[^;}]+)',text,re.I):
  if rule not in [v['rule'] for v in fonts]:fonts.append({'source':src,'rule':rule[:220]})
pick('html',r.text)
links=[a.get('href') for a in soup.select('link[rel=stylesheet][href]')]
for href in links[:26]:
 try:
  u2=requests.compat.urljoin(u,href)
  css=s.get(u2,timeout=18).text
  pick(u2,css)
 except Exception as e: print('FETCH ERR',str(e)[:150])
p=pathlib.Path('proposals/fah-mai/font-inspection.json')
p.write_text(json.dumps({'title':soup.title.text if soup.title else '', 'stylesheet_count':len(links),'fonts':fonts[:150]},indent=2))
print('FONTS',len(fonts),[f['rule'] for f in fonts[:20]])
