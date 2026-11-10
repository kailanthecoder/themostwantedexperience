from pathlib import Path
from bs4 import BeautifulSoup
import re

path=Path("proposals/fah-mai/index.html")
s=path.read_text(encoding="utf-8")
assert len(s)>1000000 and 'id="tab-examples"' in s and 'id="glass-navigation-final-v9"' in s, "Unexpected existing site"
m=re.search(r'(<article\b[^>]*\bid="overview"[^>]*>)([\s\S]*?)(</article>)',s)
assert m, "Overview panel not found"
start, chunk, end = m.groups()
soup=BeautifulSoup(start+chunk+end,"html.parser")
heading=soup.select_one(".page-heading h1")
subtitle=soup.select_one(".page-heading .sub")
pitch=soup.select_one(".statement")
assert heading and subtitle and pitch

headline="Fah Mai Holdings Re-Envisioned: A Revenue Focused Ferrari-Design Brand Rehaul For All 3 Sectors"
new_sub=("An execution-led proposal to launch a 2026 A-tier web package that propels Fah Mai Holdings, "
         "Platinum Cask and Whisky Bull into a new era of digital leadership: future-proof technology, "
         "Ferrari-calibre design and stunningly responsive, AI-assisted websites.")
new_pitch=("Under Kailan’s leadership, Most Wanted specialises in the design-led, AI-assisted transformation "
           "that could catapult Fah Mai into its next phase of growth. I began developing all three websites "
           "with my existing technology stack, but reached my available AI-credit limit before completing them. "
           "This concise proposal outlines the vision, the commercial opportunity and a clear plan to deliver.")

heading.clear();heading.append(headline)
subtitle.clear();subtitle.append(new_sub)
pitch.clear();pitch.append(new_pitch)
updated = s[:m.start()]+str(soup.article)+s[m.end():]
assert len(updated)>1000000
assert updated.count(new_sub)==1 and updated.count(new_pitch)==1
path.write_text(updated,encoding="utf-8")
print("UPDATED_OVERVIEW",len(updated),headline,new_sub,new_pitch,sep="\n",flush=True)
