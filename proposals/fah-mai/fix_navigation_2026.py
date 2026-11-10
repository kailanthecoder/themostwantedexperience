from pathlib import Path

p = Path("proposals/fah-mai/index.html")
html = p.read_text(encoding="utf-8")
marker = '<style id="fahmai-editorial-nav-2026">'
if marker in html:
    print("Already patched")
    raise SystemExit(0)

css = """
<style id="fahmai-editorial-nav-2026">
/* One understated navigation system. Retains the existing proposal view behaviour. */
@media screen {
  .toolbar{
    position:sticky!important;top:0!important;z-index:1000!important;
    padding:0 20px!important;
    background:rgba(255,253,254,.96)!important;
    border-bottom:1px solid #eadce4!important;
    box-shadow:0 2px 12px rgba(53,24,43,.035)!important;
    backdrop-filter:blur(16px)!important;
  }
  .toolbar-inner {
    max-width:1240px!important;min-height:70px!important;height:70px!important;
    margin:0 auto!important;padding:0!important;
    display:grid!important;grid-template-columns:190px minmax(0,1fr) 120px!important;
    gap:26px!important;align-items:center!important;justify-content:stretch!important;
    flex-flow:unset!important;
  }
  .nav-toprow{display:contents!important;}
  .view-switcher{display:none!important;}
  .site-identity{
    display:flex!important;align-items:center!important;gap:12px!important;
    min-width:0!important;grid-column:1!important;grid-row:1!important;
    color:#33222c!important;text-decoration:none!important;
  }
  .site-identity-mark{
    display:grid;place-items:center;width:34px;height:34px;flex:none;
    background:#23141d;color:white;border-radius:9px;
    font:800 12px/1 'Figtree',Arial,sans-serif;letter-spacing:-.7px;
  }
  .site-identity-word{
    display:flex;flex-direction:column;gap:4px;white-space:nowrap;
    font:800 11px/1 'Figtree',Arial,sans-serif!important;letter-spacing:.015em;
  }
  .site-identity-word small{
    font-size:8px;font-weight:650;letter-spacing:.14em;color:#a78698;
  }
  .proposal-sections,
  .proposal-sections[hidden] {
    display:flex!important;grid-column:2!important;grid-row:1!important;
    align-items:center!important;justify-content:center!important;
    width:100%!important;min-width:0!important;max-width:100%!important;
    overflow-x:auto!important;overflow-y:hidden!important;scrollbar-width:none!important;
    flex-wrap:nowrap!important;gap:1px!important;margin:0!important;padding:5px 0!important;
    border:none!important;background:transparent!important;
    -webkit-overflow-scrolling:touch!important;
  }
  .proposal-sections::-webkit-scrollbar{display:none!important}
  .proposal-sections .tab,
  .proposal-sections #tab-examples{
    display:inline-flex!important;align-items:center!important;justify-content:center!important;
    position:relative!important;flex:0 0 auto!important;
    min-height:38px!important;height:38px!important;
    padding:0 11px!important;margin:0!important;
    background:transparent!important;
    color:#6d5a67!important;
    border:0!important;border-radius:7px!important;
    box-shadow:none!important;
    font:700 11.5px/1 'Figtree','Poppins',Arial,sans-serif!important;
    letter-spacing:-.01em!important;white-space:nowrap!important;
    transition:background .16s ease,color .16s ease!important;
  }
  .proposal-sections .tab:hover,
  .proposal-sections #tab-examples:hover{
    background:#fbebf3!important;color:#b41c68!important;
  }
  .proposal-sections .tab[aria-selected="true"],
  .proposal-sections #tab-examples[aria-pressed="true"]{
    background:#f9e8f0!important;color:#a90e61!important;
    border:0!important;box-shadow:none!important;font-weight:800!important;
  }
  .proposal-sections .tab:focus-visible,
  .proposal-sections #tab-examples:focus-visible{
    outline:2px solid #d63882!important;outline-offset:2px!important;
  }
  .proposal-sections #tab-proposed{margin:0!important;background:transparent!important;color:#6d5a67!important;border:0!important;box-shadow:none!important}
  .proposal-sections #tab-proposed[aria-selected="true"]{background:#f9e8f0!important;color:#a90e61!important;border:0!important;box-shadow:none!important}
  .proposal-sections #tab-proposed:before,
  .proposal-sections #tab-proposed:after{display:none!important;content:none!important}
  .toolbar .tool-actions {
    grid-column:3!important;grid-row:1!important;display:flex!important;
    justify-content:flex-end!important;align-items:center!important;
    gap:0!important;padding:0!important;margin:0!important;
    border:0!important;width:auto!important;
  }
  .toolbar .pdf-btn {
    display:inline-flex!important;align-items:center!important;justify-content:center!important;
    min-height:36px!important;height:36px!important;
    padding:0 13px!important;border-radius:8px!important;
    background:#281720!important;color:white!important;
    border:1px solid #281720!important;
    font:800 10.5px/1 'Figtree','Poppins',Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;box-shadow:none!important;
  }
  .toolbar .pdf-btn:hover{background:#b82b73!important;border-color:#b82b73!important}
  .toolbar .status,.toolbar .tool-brand{display:none!important}
}
@media screen and (max-width:1050px) and (min-width:801px){
  .toolbar-inner{grid-template-columns:150px minmax(0,1fr) 105px!important;gap:10px!important}
  .site-identity-word{font-size:10px!important}
  .proposal-sections .tab,.proposal-sections #tab-examples{font-size:10.5px!important;padding:0 7px!important}
  .toolbar .pdf-btn{font-size:10px!important;padding:0 10px!important}
}
@media screen and (max-width:800px){
  .toolbar{padding:0 14px!important}
  .toolbar-inner{
    display:grid!important;grid-template-columns:1fr auto!important;
    grid-template-rows:57px 44px!important;gap:0 10px!important;
    height:101px!important;min-height:101px!important;padding:0!important;
  }
  .site-identity{grid-column:1!important;grid-row:1!important}
  .toolbar .tool-actions{grid-column:2!important;grid-row:1!important}
  .proposal-sections,.proposal-sections[hidden]{
    grid-column:1/3!important;grid-row:2!important;justify-content:flex-start!important;
    padding:0 0 7px!important;border-top:1px solid #f2e7ed!important;gap:2px!important;
  }
  .proposal-sections .tab,.proposal-sections #tab-examples{font-size:11px!important;padding:0 11px!important;height:34px!important;min-height:34px!important}
}
@media print{
  .toolbar{display:none!important}
}
</style>
"""
html = html.replace('</head>', css+'</head>', 1)
# Add a brand lockup to the existing toolbar but never change the proposal pages.
needle='<div class="toolbar"><div class="toolbar-inner">'
assert needle in html, 'Toolbar root markup changed'
html=html.replace(needle,needle+'<a class="site-identity" href="#overview" aria-label="Fah Mai proposal overview"><span class="site-identity-mark">MW</span><span class="site-identity-word">FAH MAI × MOST WANTED<small>PRIVATE PROPOSAL · 2026</small></span></a>',1)
# Relocate the existing Examples toggle inside the tab row.
js = """
<script id="fahmai-editorial-nav-bridge">
(function(){
  const nav = document.querySelector('.proposal-sections');
  const examples = document.getElementById('tab-examples');
  if(nav && examples){
    examples.classList.add('tab');
    examples.setAttribute('aria-label','View portfolio examples');
    nav.appendChild(examples);
    // Keep the section navigation in view while showing examples, too.
    nav.removeAttribute('hidden');
    const sections=[...nav.querySelectorAll('[data-target]')];
    const brand=document.querySelector('.site-identity');
    if(brand) brand.addEventListener('click',e=>{e.preventDefault();document.getElementById('tab-overview')?.click();});
    // When a proposal section is chosen, the existing controller restores proposal mode.
    nav.addEventListener('click',()=>nav.removeAttribute('hidden'));
    const keepVisible=new MutationObserver(()=>{if(nav.hidden)nav.removeAttribute('hidden');});
    keepVisible.observe(nav,{attributes:true,attributeFilter:['hidden']});
  }
})();
</script>
"""
html=html.replace('</body>',js+'</body>',1)
p.write_text(html,encoding="utf-8")
print('Applied one-row navigation CSS, retained proposal events and all content. bytes=',p.stat().st_size)
