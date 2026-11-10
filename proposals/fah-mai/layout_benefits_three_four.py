from pathlib import Path
p=Path('proposals/fah-mai/index.html')
s=p.read_text(encoding='utf-8')
mark='id="fahmai-three-top-four-bottom-benefits-2026"'
if mark in s: print('Already applied'); raise SystemExit(0)
assert '</head>' in s and s.count('Unbeatable Design')>0
style="""<style id="fahmai-three-top-four-bottom-benefits-2026">
/* The Overview's seven icon-and-label benefits: 3 on row 1, 4 on row 2. */
@media screen, print {
  #overview .roadmap-callout .promise-grid {
    display:grid!important;
    grid-template-columns:repeat(12,minmax(0,1fr))!important;
    grid-template-rows:repeat(2,minmax(0,1fr))!important;
    gap:8px 7px!important;
  }
  #overview .roadmap-callout .promise-grid .promise:nth-child(1){grid-column:1/5!important;grid-row:1!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(2){grid-column:5/9!important;grid-row:1!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(3){grid-column:9/13!important;grid-row:1!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(5){grid-column:1/4!important;grid-row:2!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(4){grid-column:4/7!important;grid-row:2!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(6){grid-column:7/10!important;grid-row:2!important}
  #overview .roadmap-callout .promise-grid .promise:nth-child(7){grid-column:10/13!important;grid-row:2!important}
}
</style>"""
p.write_text(s.replace('</head>',style+'\n</head>',1),encoding='utf-8')
print('Patched exact 3-top/4-bottom icon layout, unchanged content and other styles.')
