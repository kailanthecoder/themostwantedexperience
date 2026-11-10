from pathlib import Path
import re
p=Path("proposals/fah-mai/index.html")
s=p.read_text(encoding="utf-8")
# Restore the precise header that was present before the last unsolicited brand addition.
s,style_count=re.subn(r'<style id="fahmai-editorial-nav-2026">[\s\S]*?</style>\s*','',s,count=1)
s,script_count=re.subn(r'<script id="fahmai-editorial-nav-bridge">[\s\S]*?</script>\s*','',s,count=1)
s,brand_count=re.subn(r'<a class="site-identity" href="#overview"[\s\S]*?</a>','',s,count=1)
print("Removed previous intrusive header edits",style_count,script_count,brand_count)
assert (style_count,script_count,brand_count)==(1,1,1)
assert 'id="fahmai-mobile-zoom-2026"' not in s
assert 'id="fahmai-document-zoom-script"' not in s

css=r"""
<style id="fahmai-mobile-zoom-2026">
/* The original two-tier Proposal / Examples header is preserved on desktop. */
@media screen and (max-width:800px){
  html,body{max-width:100%!important;overflow-x:hidden!important}
  .toolbar{
    position:sticky!important;top:0!important;z-index:1000!important;
    background:rgba(255,251,253,.97)!important;
    border-bottom:1px solid #f0e0e8!important;
    box-shadow:0 4px 18px rgba(54,20,42,.055)!important;
    backdrop-filter:blur(16px)!important;
    -webkit-backdrop-filter:blur(16px)!important;
  }
  .toolbar-inner{
    max-width:none!important;width:100%!important;
    height:auto!important;min-height:0!important;
    display:flex!important;flex-direction:column!important;
    align-items:stretch!important;justify-content:initial!important;
    flex-wrap:nowrap!important;gap:7px!important;
    padding:10px 12px 7px!important;margin:0!important;
  }
  .nav-toprow{
    display:flex!important;flex-direction:row!important;
    align-items:center!important;justify-content:space-between!important;
    flex-wrap:nowrap!important;gap:8px!important;
    width:100%!important;min-width:0!important;margin:0!important;padding:0!important;
    border:0!important;
  }
  .view-switcher{
    display:inline-flex!important;flex:none!important;align-items:center!important;
    gap:2px!important;max-width:calc(100% - 108px)!important;
    margin:0!important;padding:3px!important;
    border-radius:99px!important;background:#f8eaf1!important;
    border:1px solid #f4d8e6!important;box-shadow:none!important;
  }
  .view-switch{
    min-height:34px!important;height:34px!important;min-width:0!important;
    padding:0 12px!important;margin:0!important;border-radius:99px!important;
    box-shadow:none!important;font:800 11.5px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:-.015em!important;white-space:nowrap!important;
  }
  .view-switch.is-current,.view-switch[aria-pressed="true"]{
    background:#e72982!important;color:#fff!important;
    box-shadow:none!important;
  }
  .tool-actions{
    display:flex!important;flex:none!important;align-items:center!important;justify-content:flex-end!important;
    width:auto!important;min-width:0!important;
    margin:0!important;padding:0!important;
    border:0!important;border-left:0!important;gap:0!important;
  }
  .toolbar .pdf-btn{
    min-height:36px!important;height:36px!important;
    padding:0 12px!important;border-radius:9px!important;
    background:white!important;color:#b32570!important;
    border:1px solid #eaa3c8!important;box-shadow:none!important;
    font:800 11px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:-.01em!important;white-space:nowrap!important;
  }
  .proposal-sections{
    width:100%!important;min-width:0!important;max-width:100%!important;
    height:43px!important;min-height:43px!important;
    display:flex!important;flex-direction:row!important;align-items:center!important;
    justify-content:flex-start!important;flex-wrap:nowrap!important;
    gap:4px!important;overflow-x:auto!important;overflow-y:hidden!important;
    margin:0!important;padding:3px 0 6px!important;
    scrollbar-width:none!important;-ms-overflow-style:none!important;
    scroll-snap-type:x proximity!important;touch-action:pan-x!important;
  }
  .proposal-sections[hidden]{display:none!important}
  .proposal-sections::-webkit-scrollbar{display:none!important}
  .proposal-sections .tab,
  .proposal-sections #tab-proposed{
    position:relative!important;flex:0 0 auto!important;
    display:inline-flex!important;align-items:center!important;justify-content:center!important;
    height:34px!important;min-height:34px!important;min-width:0!important;
    padding:0 13px!important;margin:0!important;
    color:#71606b!important;background:transparent!important;
    border:0!important;border-radius:9px!important;
    box-shadow:none!important;text-shadow:none!important;
    font:700 11.5px/1 "Figtree","Poppins",Arial,sans-serif!important;
    letter-spacing:0!important;white-space:nowrap!important;
    scroll-snap-align:center!important;
  }
  .proposal-sections .tab[aria-selected="true"],
  .proposal-sections #tab-proposed[aria-selected="true"]{
    color:#ab1b67!important;background:#f9e4ee!important;
    border:0!important;box-shadow:none!important;
    font-weight:800!important;
  }
  .proposal-sections .tab:hover{
    color:#b41f6b!important;background:#fff0f7!important;
  }
  .proposal-sections #tab-proposed::before,
  .proposal-sections #tab-proposed::after{content:none!important;display:none!important}
  .tool-brand,.status{display:none!important}
  .viewport{
    width:100%!important;max-width:100%!important;
    overflow-x:auto!important;overflow-y:visible!important;
    padding:12px 9px 92px!important;
    scrollbar-width:none!important;
    overscroll-behavior-x:contain!important;
    -webkit-overflow-scrolling:touch!important;
  }
  .viewport::-webkit-scrollbar{display:none!important}
  .viewport .sheet{
    width:210mm!important;min-width:210mm!important;max-width:none!important;
    height:297mm!important;min-height:297mm!important;max-height:none!important;
    margin:0 auto!important;transform:none!important;
    transform-origin:top left!important;
  }
}
@media screen and (max-width:350px){
  .view-switch{padding:0 9px!important;font-size:10.5px!important}
  .toolbar .pdf-btn{padding:0 9px!important;font-size:10px!important}
}
/* iPhone camera-inspired discreet zoom scrubber: visible only on touch-sized screens. */
.fm-zoom{
  display:none;
  --zoom-accent:#f6d7e7;
}
@media screen and (max-width:800px){
  .fm-zoom{
    position:fixed;z-index:5000;
    display:flex;align-items:center;gap:9px;
    width:min(254px,calc(100vw - 32px));height:44px;
    bottom:max(16px,env(safe-area-inset-bottom) + 11px);left:50%;
    transform:translateX(-50%);
    padding:0 12px;
    border-radius:100px;
    color:#fff;
    border:1px solid rgba(255,255,255,.14);
    background:rgba(30,19,29,.85);
    -webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
    box-shadow:0 4px 18px rgba(30,15,25,.16);
    font:700 11px/1 "Figtree","Poppins",Arial,sans-serif;
    user-select:none;-webkit-user-select:none;
    touch-action:pan-y;
  }
  .fm-zoom button{
    display:grid;place-items:center;flex:0 0 25px;
    width:25px;height:25px;min-width:0;padding:0;margin:0;
    border:0;border-radius:50%;background:transparent;
    color:#f7e6ef;font:700 19px/1 Arial,sans-serif;
    box-shadow:none;cursor:pointer;
  }
  .fm-zoom button:active{background:rgba(255,255,255,.15)}
  .fm-zoom .fm-zoom-range{
    flex:1 1 auto;min-width:0;width:100%;
    height:24px;cursor:ew-resize;background:transparent;
    -webkit-appearance:none;appearance:none;outline:0;
    touch-action:none;
  }
  .fm-zoom .fm-zoom-range::-webkit-slider-runnable-track{
    height:2px;border:0;border-radius:4px;
    background:linear-gradient(90deg,rgba(255,255,255,.45),rgba(255,255,255,.65));
  }
  .fm-zoom .fm-zoom-range::-webkit-slider-thumb{
    -webkit-appearance:none;appearance:none;
    width:14px;height:14px;border-radius:50%;
    background:#fff;border:2px solid #ffb4d8;box-shadow:0 0 0 3px rgba(233,77,147,.16);
    margin-top:-6px;
  }
  .fm-zoom .fm-zoom-range::-moz-range-track{height:2px;background:rgba(255,255,255,.65)}
  .fm-zoom .fm-zoom-range::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:#fff;border:2px solid #ffb4d8}
  .fm-zoom .fm-zoom-readout{
    display:inline-block;flex:0 0 34px;min-width:34px;text-align:center;
    font-size:11px;color:#ffbfdb;font-weight:850;font-variant-numeric:tabular-nums;
    letter-spacing:-.035em;
  }
}
@media print{.fm-zoom{display:none!important}}
</style>
"""
s=s.replace("</head>",css+"</head>",1)

zoom=r"""
<div class="fm-zoom" role="group" aria-label="Proposal page zoom">
  <button type="button" class="fm-zoom-minus" aria-label="Zoom out">−</button>
  <input class="fm-zoom-range" type="range" min="0.75" max="2.5" value="1" step="0.05" aria-label="Adjust document zoom">
  <button type="button" class="fm-zoom-plus" aria-label="Zoom in">+</button>
  <output class="fm-zoom-readout" aria-live="off">1×</output>
</div>
<script id="fahmai-document-zoom-script">
(function(){
  const input=document.querySelector('.fm-zoom-range');
  const readout=document.querySelector('.fm-zoom-readout');
  const minus=document.querySelector('.fm-zoom-minus');
  const plus=document.querySelector('.fm-zoom-plus');
  const viewport=document.querySelector('.viewport');
  if(!input||!viewport)return;
  const pages=[...viewport.querySelectorAll('.sheet')];
  const min=.75,max=2.5;
  const clamp=v=>Math.min(max,Math.max(min,Math.round(v*20)/20));
  let factor=1;
  try{
    const stored=Number(sessionStorage.getItem('fahmai_mobile_zoom')||1);
    if(Number.isFinite(stored))factor=clamp(stored);
  }catch(e){}
  function render(preserveScroll){
    const mobile=window.matchMedia('(max-width:800px)').matches;
    input.value=String(factor);
    readout.textContent=(Math.round(factor*100)/100).toLocaleString('en-US',{maximumFractionDigits:2})+'×';
    if(!mobile){
      pages.forEach(p=>p.style.removeProperty('zoom'));
      return;
    }
    // A4's default CSS width is 794px. The indicated 1x fits the page to device width.
    const available=Math.max(280,viewport.clientWidth-18);
    const relative=available/794;
    const prevWidth=Math.max(1,viewport.scrollWidth);
    const oldCenter=(viewport.scrollLeft+viewport.clientWidth/2)/prevWidth;
    pages.forEach(p=>p.style.setProperty('zoom',String(relative*factor),'important'));
    requestAnimationFrame(()=>{
      const overflow=Math.max(0,viewport.scrollWidth-viewport.clientWidth);
      if(overflow>0){
        viewport.scrollLeft=preserveScroll
          ?Math.min(overflow,Math.max(0,oldCenter*viewport.scrollWidth-viewport.clientWidth/2))
          :overflow/2;
      }else viewport.scrollLeft=0;
    });
  }
  function update(v){
    factor=clamp(Number(v));
    try{sessionStorage.setItem('fahmai_mobile_zoom',String(factor));}catch(e){}
    render(true);
  }
  input.addEventListener('input',()=>update(input.value));
  minus.addEventListener('click',()=>update(factor-.25));
  plus.addEventListener('click',()=>update(factor+.25));
  // Two-finger pinch on the paper works as a camera-style direct scale gesture.
  let pinchStart=null;
  viewport.addEventListener('touchstart',e=>{
    if(e.touches.length===2){
      pinchStart={
        distance:Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY),
        factor
      };
    }
  },{passive:true});
  viewport.addEventListener('touchmove',e=>{
    if(pinchStart&&e.touches.length===2){
      const distance=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
      update(pinchStart.factor*(distance/Math.max(1,pinchStart.distance)));
    }
  },{passive:true});
  viewport.addEventListener('touchend',e=>{if(e.touches.length<2)pinchStart=null;},{passive:true});
  window.addEventListener('resize',()=>render(false),{passive:true});
  // Keep tab navigation usable while zoomed; recentre new pages when changing tabs.
  document.querySelectorAll('.proposal-sections .tab, .view-switch').forEach(btn=>{
    btn.addEventListener('click',()=>{
      if(btn.classList.contains('tab'))btn.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
      requestAnimationFrame(()=>render(false));
    });
  });
  render(false);
})();
</script>
"""
s=s.replace("</body>",zoom+"</body>",1)
p.write_text(s,encoding="utf-8")
print("Restored original desktop header; installed compact mobile header and camera-like zoom.",p.stat().st_size)
