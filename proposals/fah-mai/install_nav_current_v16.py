from pathlib import Path
import re

root=Path('proposals/fah-mai')
page=root/'index.html'
source=page.read_text(encoding='utf-8')
if 'id="fahmai-navigation-current-v16"' in source:
    print('NAV_CURRENT_V16_ALREADY_INSTALLED')
    raise SystemExit(0)
assert '—' not in source
assert source.count('id="current"')==1
assert source.count('class="ps-source-toggle"')==1
assert source.count('class="audit-v5-carousel"')==1
assert source.count('class="ps-evidence"')==1

# Remove the entire previous websites-view selector AND all three historical
# homepage screenshots. Keep the five original PageSpeed reports and analytics.
article_pattern=r'<article\b[^>]*\bid="current"[^>]*>[\s\S]*?</article>'
match=re.search(article_pattern,source)
assert match,'Current A4 sheet missing'
article=match.group(0)
toggle=article.index('<div class="ps-source-toggle"')
reports=article.index('<section class="ps-evidence"')
assert toggle<reports
removed=article[toggle:reports]
assert 'Website screenshots' in removed and 'audit-v5-carousel' in removed
assert removed.count('audit-v5-slide')>=3
article=article[:toggle]+article[reports:]
assert 'Website screenshots' not in article
assert 'audit-v5-carousel' not in article
assert 'ps-source-toggle' not in article
assert 'ps-evidence' in article
source=source[:match.start()]+article+source[match.end():]
print('REMOVED_WEBSITE_SCREENSHOTS',len(removed),'bytes; preserved five PageSpeed reports')

# The PageSpeed carousel previously required a two-button view selector.
# With screenshots removed it must initialise independently.
old='if(!screenshot||dots.length!==5||toggle.length!==2)return;'
new='if(!screenshot||dots.length!==5)return;'
assert source.count(old)==1,'Expected original carousel initialiser'
source=source.replace(old,new,1)
print('PAGESPEED_CAROUSEL_REMAINS_INTERACTIVE')

# Insert a final isolated CSS override, preserving A4 typography/structure.
css=(root/'nav_and_pagespeed_v16.css').read_text(encoding='utf-8')
assert source.count('</head>')==1
source=source.replace('</head>','<style id="fahmai-navigation-current-v16">'+css+'</style>\n</head>',1)

# Center selected chapter tabs within their *own* overflow region. Avoid
# scrollIntoView() because that can unexpectedly scroll the document vertically.
script=r'''(function(){
 "use strict";
 const nav=document.querySelector('.toolbar nav.tabs.proposal-sections');
 if(!nav)return;
 function reveal(tab){
   if(!tab||!nav.contains(tab))return;
   const outer=nav.getBoundingClientRect(),rect=tab.getBoundingClientRect();
   const left=nav.scrollLeft+(rect.left-outer.left)-(outer.width-rect.width)/2;
   nav.scrollTo({left:Math.max(0,left),behavior:"smooth"});
 }
 nav.addEventListener("click",e=>{
   const tab=e.target.closest('button.tab');
   if(tab)requestAnimationFrame(()=>reveal(tab));
 });
 nav.addEventListener("keydown",e=>{
   if(e.key==="ArrowLeft"||e.key==="ArrowRight"){
     requestAnimationFrame(()=>reveal(document.activeElement));
   }
 });
})();'''
assert source.count('</body>')==1
source=source.replace('</body>','<script id="fahmai-nav-scroll-control-v16">'+script+'</script>\n</body>',1)
assert 'class="ps-source-toggle"' not in source
assert 'class="audit-v5-carousel"' not in source
assert source.count('class="ps-evidence"')==1
assert source.count('id="fahmai-navigation-current-v16"')==1
assert source.count('id="fahmai-nav-scroll-control-v16"')==1
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',source))==12
assert '—' not in source
page.write_text(source,encoding='utf-8')
print('NAV_CURRENT_V16_INSTALLED',len(source),'bytes','12 A4 pages')
