from pathlib import Path
p=Path("proposals/fah-mai/index.html")
s=p.read_text(encoding="utf-8")
key='id="fahmai-mobile-menu-correction-2026"'
if key in s:
  print("Already patched")
  raise SystemExit(0)
css=r"""
<style id="fahmai-mobile-menu-correction-2026">
/* Correct one inherited legacy CTA override. Keep the original design and structure. */
@media screen and (max-width:800px) {
  html body .toolbar .tabs.proposal-sections button#tab-proposed {
    display:inline-flex!important;align-items:center!important;justify-content:center!important;
    flex:0 0 auto!important;position:relative!important;
    width:auto!important;min-width:0!important;height:34px!important;min-height:34px!important;
    margin:0!important;padding:0 13px!important;
    border:0!important;border-radius:9px!important;
    background:transparent!important;background-color:transparent!important;background-image:none!important;
    color:#71606b!important;
    box-shadow:none!important;text-shadow:none!important;
    font:700 11.5px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;
    outline-offset:2px!important;
  }
  html body .toolbar .tabs.proposal-sections button#tab-proposed[aria-selected="true"] {
    background:#f9e4ee!important;background-image:none!important;
    color:#ab1b67!important;border:0!important;box-shadow:none!important;font-weight:800!important;
  }
  html body .toolbar .tabs.proposal-sections button#tab-proposed:not([aria-selected="true"]):hover{
    background:#fff0f7!important;background-image:none!important;color:#b41f6b!important;
  }
  html body .toolbar .tabs.proposal-sections button#tab-proposed::before,
  html body .toolbar .tabs.proposal-sections button#tab-proposed::after {
    content:none!important;display:none!important;
    background:none!important;border:0!important;box-shadow:none!important;
  }
}
</style>
"""
assert '</head>' in s
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding="utf-8")
print("Patched legacy Proposed mobile styling; no structural changes.",p.stat().st_size)
