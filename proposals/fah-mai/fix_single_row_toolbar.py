from pathlib import Path
p=Path('proposals/fah-mai/index.html')
html=p.read_text(encoding='utf-8')
marker='id="fahmai-single-line-toolbar-2026"'
if marker in html:
    print('Toolbar already patched')
    raise SystemExit(0)
assert 'class="nav-toprow"' in html
assert 'class="view-switcher"' in html
assert 'class="tabs proposal-sections"' in html
assert 'class="tool-actions"' in html
css=r"""
<style id="fahmai-single-line-toolbar-2026">
/* Fix existing controls in place: one row at all screen sizes. */
@media screen {
  html body .toolbar{
    position:sticky!important;top:0!important;z-index:1000!important;
    background:rgba(255,251,253,.97)!important;
    border-bottom:1px solid #eddce6!important;
    backdrop-filter:blur(16px)!important;
    -webkit-backdrop-filter:blur(16px)!important;
  }
  html body .toolbar .toolbar-inner{
    box-sizing:border-box!important;
    width:100%!important;max-width:1300px!important;
    height:66px!important;min-height:66px!important;
    padding:0 18px!important;margin:0 auto!important;
    display:flex!important;flex-direction:row!important;
    align-items:center!important;justify-content:flex-start!important;
    flex-wrap:nowrap!important;gap:13px!important;
  }
  html body .toolbar .nav-toprow{
    display:contents!important;
    width:auto!important;min-width:0!important;
    border:0!important;padding:0!important;margin:0!important;
  }
  html body .toolbar .view-switcher{
    order:0!important;flex:0 0 auto!important;min-width:0!important;
    display:inline-flex!important;align-items:center!important;
    gap:2px!important;padding:3px!important;margin:0!important;
    border-radius:100px!important;
    border:1px solid #f2d4e4!important;
    background:#f7eaf1!important;
    box-shadow:none!important;
  }
  html body .toolbar .view-switch{
    flex:0 0 auto!important;min-width:0!important;
    height:37px!important;min-height:37px!important;
    padding:0 17px!important;margin:0!important;
    border:0!important;border-radius:100px!important;
    box-shadow:none!important;
    font:800 12px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;
  }
  html body .toolbar .view-switch.is-current,
  html body .toolbar .view-switch[aria-pressed="true"]{
    color:white!important;background:#e72982!important;
    box-shadow:none!important;
  }
  html body .toolbar nav.tabs.proposal-sections{
    order:1!important;
    flex:1 1 auto!important;min-width:0!important;max-width:none!important;
    width:auto!important;height:48px!important;min-height:48px!important;
    display:flex!important;flex-flow:row nowrap!important;
    align-items:center!important;justify-content:flex-start!important;
    gap:3px!important;
    padding:3px 2px!important;margin:0!important;
    overflow-x:auto!important;overflow-y:hidden!important;
    scroll-snap-type:x proximity!important;
    overscroll-behavior-x:contain!important;
    -webkit-overflow-scrolling:touch!important;
    scrollbar-width:none!important;
    border:0!important;background:transparent!important;
  }
  html body .toolbar nav.tabs.proposal-sections::-webkit-scrollbar{display:none!important}
  html body .toolbar nav.tabs.proposal-sections[hidden]{display:none!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    position:relative!important;
    flex:0 0 auto!important;min-width:0!important;width:auto!important;
    display:inline-flex!important;align-items:center!important;justify-content:center!important;
    height:36px!important;min-height:36px!important;
    padding:0 12px!important;margin:0!important;
    border:1px solid transparent!important;border-radius:9px!important;
    background:transparent!important;background-image:none!important;
    color:#756471!important;
    box-shadow:none!important;text-shadow:none!important;
    font:750 12px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;
    scroll-snap-align:center!important;
    transition:background .15s ease,color .15s ease!important;
  }
  html body .toolbar nav.tabs.proposal-sections button.tab[aria-selected="true"],
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed[aria-selected="true"]{
    background:#f9e7f0!important;background-image:none!important;
    border:1px solid #f1cde0!important;
    color:#b31868!important;font-weight:850!important;
    box-shadow:none!important;
  }
  html body .toolbar nav.tabs.proposal-sections button.tab:not([aria-selected="true"]):hover,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed:not([aria-selected="true"]):hover{
    background:#fff0f7!important;color:#ba2973!important;
  }
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed::before,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed::after{
    display:none!important;content:none!important;
  }
  html body .toolbar .tool-actions{
    order:2!important;flex:0 0 auto!important;
    width:auto!important;min-width:0!important;
    display:flex!important;align-items:center!important;justify-content:flex-end!important;
    margin:0!important;padding:0!important;gap:0!important;
    border:0!important;
  }
  html body .toolbar .pdf-btn{
    height:38px!important;min-height:38px!important;
    padding:0 15px!important;margin:0!important;
    border:1px solid #e6a1c1!important;border-radius:100px!important;
    background:white!important;color:#ac1e67!important;
    box-shadow:none!important;
    font:800 11.5px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;
  }
  html body .toolbar .pdf-btn:hover{background:#fff1f8!important}
  html body .toolbar .tool-brand,html body .toolbar .status{display:none!important}
}
@media screen and (max-width:1000px){
  html body .toolbar .toolbar-inner{gap:8px!important;padding:0 11px!important}
  html body .toolbar .view-switch{padding:0 11px!important;font-size:11px!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    padding:0 10px!important;font-size:11.5px!important;
  }
  html body .toolbar .pdf-btn{padding:0 12px!important;font-size:11px!important}
}
@media screen and (max-width:800px){
  html body .toolbar .toolbar-inner{
    height:56px!important;min-height:56px!important;max-height:56px!important;
    gap:6px!important;padding:0 8px!important;
  }
  html body .toolbar .view-switcher{padding:2px!important;gap:1px!important}
  html body .toolbar .view-switch{
    height:32px!important;min-height:32px!important;
    padding:0 9px!important;
    font-size:10.5px!important;
  }
  html body .toolbar nav.tabs.proposal-sections{
    height:39px!important;min-height:39px!important;gap:2px!important;
    padding:2px 1px!important;
  }
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
    height:32px!important;min-height:32px!important;
    padding:0 9px!important;font-size:10.5px!important;
    border-radius:8px!important;
  }
  html body .toolbar .pdf-btn{
    height:34px!important;min-height:34px!important;
    padding:0 10px!important;border-radius:10px!important;
    font-size:10px!important;
  }
}
@media screen and (max-width:360px){
  html body .toolbar .toolbar-inner{gap:5px!important;padding:0 6px!important}
  html body .toolbar .view-switch{padding:0 7px!important;font-size:10px!important}
  html body .toolbar .pdf-btn{padding:0 8px!important;font-size:9.5px!important}
  html body .toolbar nav.tabs.proposal-sections button.tab,
  html body .toolbar nav.tabs.proposal-sections button#tab-proposed{font-size:10px!important;padding:0 8px!important}
}
</style>
"""
html=html.replace('</head>',css+'</head>',1)
js=r"""
<script id="fahmai-one-line-toolbar-scroll-2026">
(function(){
  const nav=document.querySelector('.toolbar nav.proposal-sections');
  if(!nav)return;
  let lastId='';
  const nudge=()=>{
    if(nav.hidden)return;
    const current=nav.querySelector('[aria-selected="true"]');
    if(!current||current.id===lastId)return;
    lastId=current.id;
    const target=current.offsetLeft+current.offsetWidth/2-nav.clientWidth/2;
    nav.scrollTo({left:Math.max(0,target),behavior:'smooth'});
  };
  nav.addEventListener('click',()=>requestAnimationFrame(nudge));
  nav.addEventListener('keydown',()=>requestAnimationFrame(nudge));
  document.querySelector('#nav-proposal')?.addEventListener('click',()=>requestAnimationFrame(nudge));
  window.addEventListener('hashchange',nudge);
  // The selected section is always accessible after direct links and page turns.
  requestAnimationFrame(nudge);
})();
</script>
"""
html=html.replace('</body>',js+'</body>',1)
p.write_text(html,encoding='utf-8')
print("Patched only toolbar CSS and selected-tab scroll behaviour; HTML bytes:",len(html))
