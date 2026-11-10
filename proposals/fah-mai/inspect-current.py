from pathlib import Path
from bs4 import BeautifulSoup
import re,json
s=Path("proposals/fah-mai/index.html").read_text()
soup=BeautifulSoup(s,"html.parser")
toolbar=soup.select_one(".toolbar")
nav=soup.select_one("nav")
articles=soup.select("article.sheet")
v={
"size":len(s),
"toolbar":str(toolbar)[:3500] if toolbar else None,
"nav":str(nav)[:3600] if nav else None,
"articles":[{"id":x.get("id"),"class":x.get("class"),"heading":x.find("h1").get_text(" ",strip=True) if x.find("h1") else None,"start":str(x)[:220]} for x in articles],
"selectors":list(dict.fromkeys(re.findall(r"\.([a-zA-Z][\w-]+)",s[:s.find("</style>")+8])))[:130],
"main":str(soup.select_one('main'))[:500] if soup.select_one("main") else None,
"nav_parent":str(nav.parent)[:500] if nav else None,
"scripts":len(soup.select("script"))
}
Path("proposals/fah-mai/inspect-current.json").write_text(json.dumps(v,indent=2))
print("INSPECTED",len(s), len(articles),flush=True)
