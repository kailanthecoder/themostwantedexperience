#!/usr/bin/env python3
"""Restore identical A4 page geometry on mobile and desktop.

Mobile responsive styling belongs on the controls and surrounding reader, NOT
inside the 210 x 297 mm print document. Keep the actual paper's CSS independent
of the outer window width; use the existing reader's zoom to fit it.
"""
from pathlib import Path
import re

p=Path("proposals/fah-mai/index.html")
html=p.read_text(encoding="utf-8")
assert 'id="fahmai-responsive-reader-v23"' in html
assert 'id="examples-client"' in html
assert 'id="overview"' in html

# Earlier mobile styles were accidentally changing all the printed page's
# typography, brand identity spacing and grid layout using viewport-wide media
# queries. Remove just those media rules; desktop A4 styles remain unchanged.
remove_from={
  "verified-original-brand-logos",
  "fahmai-rounded-editorial-v4",
  "fahmai-presentation-header-seven-tabs",
  "fahmai-side-by-side-presentation",
  "fahmai-visual-polish-nov11",
  "fahmai-identical-brand-header-2026",
  "fahmai-current-editorial-v5",
  "fahmai-spec-editorial-v6",
  "fahmai-budget-investment-v8",
  "fahmai-examples-readability-v15",
}

def strip_mobile_media(style):
    removed=[]
    for m in re.finditer(r'@media\s*([^{}]+)\s*\{',style):
        if not re.search(r'max-width\s*:',m.group(1),re.I):
            continue
        # The original source blocks have no @media nesting. Handle CSS
        # declarations within a block by balancing rule braces.
        start=m.start()
        if any(a<=start<b for a,b in removed):
            continue
        i=m.end()
        depth=1
        while i<len(style) and depth:
            if style[i]=='{':
                depth+=1
            elif style[i]=='}':
                depth-=1
            i+=1
        assert depth==0, "Unbalanced @media CSS"
        removed.append((start,i))
    for a,b in reversed(removed):
        style=style[:a]+style[b:]
    return style,len(removed)

count=0
for key in remove_from:
    rx=re.compile(r'(<style\b[^>]*\bid="'+re.escape(key)+r'"[^>]*>)([\s\S]*?)(</style>)')
    m=rx.search(html)
    assert m,f"Missing style {key}"
    stripped,n=strip_mobile_media(m.group(2))
    assert n>=1,f"Expected mobile media queries in {key}"
    html=html[:m.start()]+m.group(1)+stripped+m.group(3)+html[m.end():]
    count+=n
    print("DISABLED_MOBILE_PAPER_STYLES",key,n)
print("TOTAL_PAPER_OVERRIDES_DISABLED",count)

# Earlier lazy-load transform accidentally appended attributes after <img/>.
# Repair proper HTML syntax; load only the visible Overview's images initially.
html,n=re.subn(r'/\s+loading="lazy"\s+decoding="async">',' loading="lazy" decoding="async" />',html)
print("REPAIRED_IMAGE_TAGS",n)
a=html.find('id="examples"')
assert a>=0
before,after=html[:a],html[a:]
after,e=re.subn(r'(<img\b[^>]*\bloading=)"eager"',r'\1"lazy"',after)
html=before+after
print("DEFERRED_EXAMPLES_IMAGES",e)

# 17px legacy section footer contained a 49px-tall label. Give the two
# Examples pages a genuine 50px footer, allowing label and counter to fit
# without creating an invisible 36px overflow. Content has headroom above it.
css=r'''
<style id="fahmai-fixed-paper-geometry-v25">
/* The A4 paper never has an alternate mobile layout. Browser viewport
   changes ONLY the paper zoom and the reader controls around it. */
@media screen,print {
 #examples > footer.sheet-footer,
 #examples-client > footer.sheet-footer{
   box-sizing:border-box!important;
   min-height:52px!important;
   height:52px!important;
   flex:0 0 52px!important;
   overflow:visible!important;
 }
 #examples > footer.sheet-footer .chapter-footer-label,
 #examples-client > footer.sheet-footer .chapter-footer-label {
   box-sizing:border-box!important;
   min-height:0!important;
   max-height:52px!important;
   height:100%!important;
   align-items:center!important;
 }
}
</style>
'''
assert 'id="fahmai-fixed-paper-geometry-v25"' not in html
html=html.replace('</head>',css+'</head>',1)

# Avoid fractional zoom generated from imperative layout constraints from
# ever warping the intrinsic A4 CSS; only the outer screen-size fit changes.
assert 'const fit = Math.min(1,' in html
p.write_text(html,encoding="utf-8")
print("UPDATED_HTML_BYTES",p.stat().st_size)
