from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

root=Path("proposals/fah-mai")
page=root/"index.html"
s=page.read_text(encoding="utf-8")
if 'id="fahmai-start-overview-v18"' in s:
    print("V18_ALREADY_INSTALLED")
    raise SystemExit(0)
assert 'id="overview"' in s and 'id="spec-delivery"' in s
assert '—' not in s
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',s))==12

# Bundle real variable WOFF2 fonts locally, rather than depending on a third
# party network request when clients export the proposal to PDF.
fontpath=root/"fonts"
fontpath.mkdir(exist_ok=True)
url="https://fonts.googleapis.com/css2?family=Outfit:wght@300..900&family=Sora:wght@300..800&family=Source+Sans+3:wght@300..900&display=swap"
request=requests.get(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"},timeout=30)
request.raise_for_status()
css=request.text
latinfaces=re.findall(r'/\*\s*latin\s*\*/\s*@font-face\s*\{([^}]+)\}',css)
fonts=[
 ("Sora","sora-latin-v18.woff2"),
 ("Outfit","outfit-latin-v18.woff2"),
 ("Source Sans 3","source-sans-3-latin-v18.woff2")
]
for family,filename in fonts:
    matches=[face for face in latinfaces if f"font-family: '{family}'" in face]
    assert len(matches)==1,f"Expected one Latin variable face for {family}, found {len(matches)}"
    href=re.search(r'url\((https://fonts\.gstatic\.com/[^)]+)\)',matches[0])
    assert href,f"No WOFF2 link for {family}"
    response=requests.get(href.group(1),timeout=30)
    response.raise_for_status()
    data=response.content
    assert data.startswith(b'wOF2') and len(data)>10000,f"{family}: bad font"
    (fontpath/filename).write_bytes(data)
    print("FONT_BUNDLED",family,len(data),filename)

# Patch the actual startup paths. These currently restore #budget / #examples
# on load, which is the primary cause of starting on page seven.
old_first=""" const hash=location.hash.replace('#','');
 if(hash==='examples')activate('examples',false);
 else if(sections.has(hash))activate(hash,false);
 else activate('overview',false);"""
new_first=""" // Always start a new viewing session on the Overview, never a prior hash.
 activate('overview',false);
 try{history.replaceState(history.state,'',location.pathname+location.search)}catch(e){}"""
assert s.count(old_first)==1, "Legacy proposal hash initializer changed"
s=s.replace(old_first,new_first,1)

old_reader="""  const hash = location.hash.replace("#", "");
  const match = sheets.findIndex(sheet => sheet.id === hash);
  pageIndex = Math.max(0, match);
  layout();
  if (mode() === "vertical" && pageIndex > 0) requestAnimationFrame(() => jumpTo(pageIndex, false));"""
new_reader="""  // Cover always starts at index zero, regardless of previous section or hash.
  pageIndex = 0;
  layout();
  requestAnimationFrame(() => window.scrollTo({top:0, behavior:"instant"}));"""
assert s.count(old_reader)==1, "Storybook hash initializer changed"
s=s.replace(old_reader,new_reader,1)

# An early script runs before any layout code and disables browser history
# scroll restoration. A pageshow reset also handles browser back/forward cache.
early="""<script id="fahmai-start-overview-v18">(function(){
  try{history.scrollRestoration="manual"}catch(e){}
  try{sessionStorage.setItem("fahmai_last_proposal_section","overview")}catch(e){}
  try{if(location.hash)history.replaceState(history.state,"",location.pathname+location.search)}catch(e){}
  window.scrollTo({top:0,behavior:"instant"});
})();</script>"""
assert s.count("<head>")==1
s=s.replace("<head>","<head>\n"+early+"\n",1)
pageshow="""<script id="fahmai-overview-pageshow-v18">(function(){
  function resetInitialView(){
    try{history.scrollRestoration="manual"}catch(e){}
    try{sessionStorage.setItem("fahmai_last_proposal_section","overview")}catch(e){}
    try{if(location.hash)history.replaceState(history.state,"",location.pathname+location.search)}catch(e){}
    const selected=document.querySelector(".proposal-sections [aria-selected='true']")?.dataset.target;
    if(selected!=="overview"){
      document.getElementById("nav-proposal")?.click();
      document.getElementById("tab-overview")?.click();
    }
    window.scrollTo({top:0,behavior:"instant"});
    requestAnimationFrame(()=>window.scrollTo({top:0,behavior:"instant"}));
    const tabStrip=document.querySelector(".proposal-sections");
    if(tabStrip)tabStrip.scrollLeft=0;
  }
  window.addEventListener("pageshow",resetInitialView,{passive:true});
})();</script>"""
assert s.count("</body>")==1
s=s.replace("</body>",pageshow+"\n</body>",1)

# Seven unique icons live INSIDE the existing number column, preserving each
# capability row's two-column layout and avoiding extra textual wrapping.
icons=[
 '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 4l-4 16"/>',
 '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10.5h19M7 15h3"/>',
 '<circle cx="10.6" cy="10.5" r="6.6"/><path d="m15.4 15.4 5 5M7.7 11.7l2-2.5 2 1 1.7-2.4"/>',
 '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 '<path d="M4.7 17.8a9 9 0 1 1 14.6 0M12 13l4-4M9 20h6"/>',
 '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-2.2 2.4-3.4 5.4-3.4 9s1.2 6.6 3.4 9c2.2-2.4 3.4-5.4 3.4-9S14.2 5.4 12 3Z"/>',
 '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18M8 16l2.4 2.4L16 13"/>'
]
names=["code","payments","search","inventory","performance","localisation","booking"]
start=s.index('id="spec-delivery"')
end=s.index('</article>',start)
segment=s[start:end]
assert segment.count('<span class="specv6-num">')==7
for i,(name,icon) in enumerate(zip(names,icons),1):
    old=f'<span class="specv6-num">{i:02d}</span>'
    svg=f'<svg role="img" aria-label="{name}" viewBox="0 0 24 24" focusable="false">{icon}</svg>'
    new=f'<span class="specv6-num specv18-glyph" title="{name.title()}">{svg}<span class="specv18-icon-number">{i:02d}</span></span>'
    assert segment.count(old)==1,f"Missing {old}"
    segment=segment.replace(old,new,1)
s=s[:start]+segment+s[end:]
print("SEVEN_ICONS_ADDED",names)

# All of the historical CSS includes explicit font families. Remove the single
# older Google Fonts import; the final highest-specificity font rule applies
# the three new local fonts to all text, controls and PDF copy.
s,n=re.subn(r'<link\b[^>]*href="[^"]*fonts\.googleapis\.com[^"]*"[^>]*>','',s,flags=re.I)
if n:print("OLD_FONT_LINKS_REMOVED",n)
s,n=re.subn(r'@import\s+(?:url\()?["\']?https://fonts\.googleapis\.com[^;]+;','',s,flags=re.I)
if n:print("OLD_FONT_IMPORTS_REMOVED",n)

typography=(root/"site_fonts_icons_v18.css").read_text(encoding="utf-8")
assert "</head>" in s
s=s.replace("</head>",'<style id="fahmai-exclusive-fonts-icons-v18">'+typography+"</style>\n</head>",1)

# Markup doesn't change the content, counts, branding or book page count.
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',s))==12
assert s.count('class="specv6-num specv18-glyph"')==7
assert s.count('id="fahmai-exclusive-fonts-icons-v18"')==1
assert '—' not in s
page.write_text(s,encoding="utf-8")
print("OVERVIEW_FONTS_ICONS_V18_READY","bytes",len(s),"pages",12,"icons",7,"fonts",len(fonts))
