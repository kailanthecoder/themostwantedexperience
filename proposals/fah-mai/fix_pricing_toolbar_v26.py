#!/usr/bin/env python3
"""Targeted Fah Mai proposal edits: pricing clarity, one-row nav, arrow contrast.

Do not alter paper dimensions, fonts, exported PDF pagination, section copy,
standard valuations or the reader's overview-first / zoom logic.
"""
from pathlib import Path
import re

p = Path("proposals/fah-mai/index.html")
html = p.read_text(encoding="utf-8")
assert 'id="fahmai-fixed-paper-geometry-v25"' in html
assert 'id="budget"' in html
assert 'class="budgetv8-rate-tables"' in html
assert 'class="toolbar-inner"' in html
assert 'id="fahmai-budget-oneoff-v26"' not in html

start = html.index('<div class="budgetv8-rate-tables">')
end = html.index('</div>', start) + len('</div>')
previous = html[start:end]
assert previous.count('<table ') == 2
assert previous.count('Custom backend, CRM and integrations') == 1
assert previous.count('Hosting and maintenance — each brand') == 1

# Seven development deliverables on the LEFT; seven monthly service line-items
# on the RIGHT. This does NOT change a single GBP amount or the agreed scope.
oneoff = [
    ("Fah Mai Holdings website", "£1,500"),
    ("Whisky Bull website", "£1,500"),
    ("Platinum Cask website", "£1,500"),
    ("Fah Mai SEO / AI SEO setup", "£750"),
    ("Whisky Bull SEO / AI SEO setup", "£750"),
    ("Platinum Cask SEO / AI SEO setup", "£750"),
    ("Custom backend, CRM and integrations", "£1,875"),
]
ongoing = [
    ("Fah Mai hosting and maintenance", "£75/mo"),
    ("Whisky Bull hosting and maintenance", "£75/mo"),
    ("Platinum Cask hosting and maintenance", "£75/mo"),
    ("Fah Mai ongoing SEO / AI SEO", "£75/mo"),
    ("Whisky Bull ongoing SEO / AI SEO", "£75/mo"),
    ("Platinum Cask ongoing SEO / AI SEO", "£75/mo"),
    ("Backend maintenance and support", "£150/mo"),
]
assert sum(int(v.replace("£","").replace(",","")) for _,v in oneoff) == 8625
assert sum(int(v.replace("£","").replace("/mo","").replace(",","")) for _,v in ongoing) == 600

def price_table(label,heading,items,total_label,total,category):
    rows = '\n'.join(f'<tr><td>{name}</td><td>{amount}</td></tr>' for name,amount in items)
    return f'''<table aria-label="{label}" data-cost-type="{category}">
<thead><tr><th scope="col">{heading}</th><th scope="col">GBP</th></tr></thead>
<tbody>
{rows}
<tr class="budgetv8-rate-total"><td>{total_label}</td><td>{total}</td></tr>
</tbody></table>'''
new = '''<div class="budgetv8-rate-tables" aria-label="Separate one-time and monthly costs">
''' + price_table("One-time development cost breakdown","One-time development",oneoff,"Standard development total","£8,625","one-time") + '\n' + price_table("Ongoing monthly service cost breakdown","Monthly ongoing services",ongoing,"Standard monthly total","£600/mo","monthly") + '''
</div>'''
html = html[:start] + new + html[end:]

old_comp = '<div class="budgetv8-comparison"><span><b>One-time standard value</b><strong>£8,625</strong></span><span><b>One-time partnership quote</b><strong>£5,750</strong></span></div>'
new_comp = '<div class="budgetv8-comparison"><span><b>Your one-time development quote</b><strong>£5,750</strong></span><span><b>Your ongoing monthly quote</b><strong>£400/mo</strong></span></div>'
assert html.count(old_comp) == 1
html = html.replace(old_comp,new_comp,1)

# Override only navigation chrome, never any A4 page rule. Scroll long tab labels
# within a single row on exceptionally narrow phones rather than wrapping the menu.
css = r'''
<style id="fahmai-one-row-nav-and-pricing-v26">
@media screen {
  /* Explicit colours for both arrow states; avoid white-on-white inherited hover. */
  html body .fm-zoom .fm-story-next:not(:disabled):hover,
  html body .fm-zoom .fm-story-next:not(:disabled):focus-visible{
    color:#fff!important;-webkit-text-fill-color:#fff!important;
    background:#a71e66!important;border-color:#a71e66!important;
  }
  html body .fm-zoom .fm-story-prev:not(:disabled):hover,
  html body .fm-zoom .fm-story-prev:not(:disabled):focus-visible{
    color:#3a2031!important;-webkit-text-fill-color:#3a2031!important;
    background:#f1dbe7!important;border-color:#ecd0df!important;
  }
  html body .fm-zoom .fm-zoom-minus:not(:disabled):hover,
  html body .fm-zoom .fm-zoom-plus:not(:disabled):hover,
  html body .fm-zoom .fm-zoom-fit:not(:disabled):hover{
    background:#f4e1ec!important;color:#42263a!important;
    -webkit-text-fill-color:#42263a!important;
  }
}
@media screen and (max-width:1024px){
  html body .toolbar{
    position:fixed!important;top:0!important;left:0!important;right:0!important;
    z-index:1500!important;
  }
  html body .toolbar .toolbar-inner{
    display:flex!important;flex-flow:row nowrap!important;
    align-items:center!important;justify-content:space-between!important;
    width:100%!important;max-width:100%!important;
    box-sizing:border-box!important;
    height:52px!important;min-height:52px!important;max-height:52px!important;
    padding:0 8px!important;margin:0!important;
    gap:5px!important;overflow:visible!important;
  }
  html body .toolbar .nav-toprow{display:contents!important}
  html body .toolbar .view-switcher{
    order:0!important;grid-row:auto!important;grid-column:auto!important;
    display:inline-flex!important;align-items:center!important;
    flex:0 0 auto!important;width:auto!important;max-width:none!important;
    min-width:0!important;min-height:0!important;
    gap:0!important;padding:2px!important;margin:0!important;
    white-space:nowrap!important;
  }
  html body .toolbar .view-switch{
    display:inline-flex!important;justify-content:center!important;align-items:center!important;
    flex:0 0 auto!important;height:32px!important;min-height:32px!important;
    font:750 10px/1 "Source Sans 3",sans-serif!important;
    padding:0 9px!important;margin:0!important;
    white-space:nowrap!important;
  }
  html body .toolbar nav.tabs.proposal-sections{
    order:1!important;grid-row:auto!important;grid-column:auto!important;
    display:flex!important;flex:1 1 auto!important;
    width:auto!important;min-width:0!important;max-width:none!important;
    height:38px!important;min-height:38px!important;max-height:38px!important;
    align-items:center!important;justify-content:flex-start!important;
    flex-flow:row nowrap!important;flex-wrap:nowrap!important;
    gap:2px!important;padding:1px 0!important;margin:0!important;
    overflow-x:auto!important;overflow-y:hidden!important;
    scroll-snap-type:none!important;scrollbar-width:none!important;
    overscroll-behavior-x:contain!important;-webkit-overflow-scrolling:touch!important;
    white-space:nowrap!important;
  }
  html body .toolbar nav.tabs.proposal-sections[hidden]{display:none!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    flex:0 0 auto!important;
    height:32px!important;min-height:32px!important;
    padding:0 7px!important;margin:0!important;
    font:750 10px/1 "Source Sans 3",sans-serif!important;
    letter-spacing:0!important;
    white-space:nowrap!important;border-radius:8px!important;
  }
  html body .toolbar .tool-actions{
    order:2!important;grid-row:auto!important;grid-column:auto!important;
    display:flex!important;flex:0 0 auto!important;
    justify-self:auto!important;align-items:center!important;
    width:auto!important;min-width:0!important;
    padding:0!important;margin:0!important;
  }
  html body .toolbar .pdf-btn{
    flex:0 0 auto!important;
    height:34px!important;min-height:34px!important;
    font:750 10px/1 "Source Sans 3",sans-serif!important;
    padding:0 9px!important;margin:0!important;
    white-space:nowrap!important;border-radius:10px!important;
  }
  /* The document reader measures the actual menu height; its page layout stays untouched. */
}
@media screen and (max-width:540px){
  html body .toolbar .toolbar-inner{gap:3px!important;padding:0 5px!important}
  html body .toolbar .view-switch{font-size:9px!important;padding:0 6px!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    font-size:9px!important;padding:0 5px!important;
  }
  html body .toolbar .pdf-btn{font-size:9px!important;padding:0 6px!important}
}
@media screen and (max-width:360px){
  html body .toolbar .toolbar-inner{gap:2px!important;padding:0 4px!important}
  html body .toolbar .view-switch{font-size:8px!important;padding:0 4px!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    font-size:8px!important;padding:0 4px!important;
  }
  html body .toolbar .pdf-btn{font-size:8px!important;padding:0 5px!important}
}
</style>
'''
html = html.replace('</head>',css+'</head>',1)
assert html.count('id="fahmai-one-row-nav-and-pricing-v26"') == 1
p.write_text(html,encoding='utf-8')
print('UPDATED_HTML_BYTES',p.stat().st_size)
print('ONEOFF_ITEMS',len(oneoff),'TOTAL_GBP',8625)
print('MONTHLY_ITEMS',len(ongoing),'TOTAL_GBP',600)
print('PARTNERSHIP_DEVELOPMENT',5750,'PARTNERSHIP_MONTHLY',400)
