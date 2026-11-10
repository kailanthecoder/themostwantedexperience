from pathlib import Path
import re
page=Path('proposals/fah-mai/index.html')
html=page.read_text(encoding='utf-8')
marker='id="fahmai-stage-icons-aligned-2026"'
if marker in html:
    print('Three-stage refinement already installed')
    raise SystemExit(0)

icons={
 '01':('CONSULT','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.5c0 4.4-3.8 8-8.5 8-1.1 0-2.2-.2-3.2-.6L4 20l1.2-4.2A7.7 7.7 0 0 1 3.5 11.5c0-4.4 3.8-8 8.5-8s8.5 3.6 8.5 8Z"/><path d="M8 11.5h8"/></svg>'),
 '02':('ACTIVATE','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10.5h19M7 15h4"/></svg>'),
 '03':('PREVIEW','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3.5" width="18" height="14" rx="2"/><path d="M8 21h8m-4-3.5V21m-3-11 2 2 4-4"/></svg>')
}
pattern=r'(<div class="stage-card">)\s*<span class="stage-no">(\d\d)</span>\s*(<p>[\s\S]*?</p>)\s*</div>'
def decorate(m):
    num=m.group(2)
    if num not in icons: raise ValueError('Unexpected stage '+num)
    title,svg=icons[num]
    return f'{m.group(1)}<div class="stage-head"><span class="stage-icon" aria-hidden="true">{svg}</span><span class="stage-step-label">{num} / {title}</span></div>{m.group(3)}</div>'
html,count=re.subn(pattern,decorate,html)
assert count==3,f'Expected three Overview stages, found {count}'
css=r"""
<style id="fahmai-stage-icons-aligned-2026">
/* Only the Overview's three-step process. Aligned icon, number and copy. */
@media screen, print {
  #overview .stage-runway {
    display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
    align-items:stretch!important;gap:12px!important;
  }
  #overview .stage-runway .stage-card {
    display:flex!important;flex-direction:column!important;align-items:stretch!important;
    justify-content:flex-start!important;gap:7px!important;
    box-sizing:border-box!important;min-width:0!important;
    min-height:98px!important;height:auto!important;
    padding:12px 12px 11px!important;margin:0!important;
    background:#fff!important;border:1px solid #eadce4!important;
    border-radius:10px!important;box-shadow:none!important;
    position:relative!important;overflow:hidden!important;
  }
  #overview .stage-runway .stage-card:nth-child(2),
  #overview .stage-runway .stage-card:nth-child(3) {
    background:#fff!important;border:1px solid #eadce4!important;
  }
  #overview .stage-runway .stage-card::before,
  #overview .stage-runway .stage-card::after {
    display:none!important;content:none!important;visibility:hidden!important;
  }
  #overview .stage-runway .stage-head {
    display:flex!important;flex-direction:row!important;align-items:center!important;
    justify-content:flex-start!important;gap:8px!important;
    width:100%!important;min-height:27px!important;height:27px!important;
    margin:0!important;padding:0!important;
  }
  #overview .stage-runway .stage-icon {
    display:grid!important;place-items:center!important;
    flex:0 0 27px!important;width:27px!important;min-width:27px!important;height:27px!important;
    margin:0!important;padding:0!important;
    border:1px solid #efc5d9!important;border-radius:8px!important;
    color:#bf2670!important;background:#fae7f0!important;
    box-shadow:none!important;
  }
  #overview .stage-runway .stage-icon svg {
    display:block!important;width:16px!important;height:16px!important;
    color:inherit!important;overflow:visible!important;
  }
  #overview .stage-runway .stage-step-label {
    display:inline-block!important;
    color:#b5226e!important;
    font:900 8.5px/1.25 'Figtree','Poppins',Arial,sans-serif!important;
    letter-spacing:1px!important;white-space:nowrap!important;
  }
  #overview .stage-runway .stage-card p {
    width:100%!important;display:block!important;min-width:0!important;
    margin:0!important;padding:0!important;
    color:#403440!important;
    font:700 10.6px/1.36 'Figtree','Poppins',Arial,sans-serif!important;
    text-align:left!important;letter-spacing:0!important;
    overflow-wrap:break-word!important;
  }
}
</style>"""
assert '</head>' in html
html=html.replace('</head>',css+'\n</head>',1)
page.write_text(html,encoding='utf-8')
print('Refined three stages with consistent line icons and layout; content unchanged, bytes',len(html))
