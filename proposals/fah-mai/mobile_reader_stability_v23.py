#!/usr/bin/env python3
"""Make the existing Fah Mai A4 proposal a stable single-page reader on narrow screens.
Preserve source sections, pricing, design, print styles and all desktop behaviour.
"""
from pathlib import Path
import hashlib
import re

root = Path("proposals/fah-mai")
target = root / "index.html"
source = target.read_text(encoding="utf-8")
assert "<script id=\"fahmai-document-zoom-script\">" in source
assert "fahmai-mobile-reader-v19" in source
assert "id=\"overview\"" in source
assert "id=\"budget\"" in source

# Move embedded bitmap artwork to separate, cacheable files. This massively
# reduces the initial document payload, especially on a mobile connection.
assets = root / "assets"
assets.mkdir(exist_ok=True)
extensions = {"png":"png", "jpeg":"jpg", "jpg":"jpg", "webp":"webp", "gif":"gif", "svg+xml":"svg", "avif":"avif"}
found = {}
def move_image(m):
    import base64
    mime, encoded = m.group(1).lower(), m.group(2)
    if mime not in extensions:
        return m.group(0)
    try:
        data = base64.b64decode(encoded, validate=True)
    except Exception:
        return m.group(0)
    digest = hashlib.sha256(data).hexdigest()[:16]
    name = f"inline-{digest}.{extensions[mime]}"
    outfile = assets / name
    if not outfile.exists():
        outfile.write_bytes(data)
    found[name] = len(data)
    return "./assets/" + name
source, replaced = re.subn(r'data:image/([a-zA-Z0-9.+-]+);base64,([A-Za-z0-9+/=]+)', move_image, source)
print(f"Moved {replaced} embedded image references into {len(found)} reusable assets")

# Disable an older resize script that raced the current reader for page zoom.
source, removed = re.subn(
    r'<script id="sheet-mobile-fit-v9">[\s\S]*?</script>', '', source, count=1)
assert removed == 1, "Expected obsolete competing zoom script"
# Unify the phone/tablet breakpoint rather than switching at 800px in JS.
source, n = re.subn(
    r'const mobile = \(\) => window\.innerWidth <= 800;',
    'const mobile = () => window.innerWidth <= 1024;', source, count=1)
assert n == 1, "Expected one mobile mode breakpoint"

original = '''    const fit = Math.min(1, Math.max(0.16, available / (documentWidth * pageCount)));'''
replacement = '''    // Fit the whole A4 page in the available mobile document window. Width
    // alone cropped short iPhones and let the controls cover the paper.
    const availableHeight = mobile()
      ? Math.max(160, window.innerHeight -
          (toolbar?.getBoundingClientRect().height || 94) -
          (rail?.getBoundingClientRect().height || 64) - 28)
      : Infinity;
    const heightFit = availableHeight / 1123;
    const fit = Math.min(1, Math.max(0.13,
      Math.min(available / (documentWidth * pageCount), heightFit)));'''
assert source.count(original) == 1, "Reader layout function unexpectedly changed"
source = source.replace(original, replacement, 1)

# Add final mobile styles only; leave A4 printing and existing desktop styling
# untouched. The paper is a real single A4 sheet, not a vertically stacked feed.
mobile_css = r'''
<style id="fahmai-responsive-reader-v23">
@media screen and (max-width:1024px) {
 html,html body{
   width:100%!important;height:100%!important;
   max-width:100vw!important;max-height:100dvh!important;
   overflow:hidden!important;overscroll-behavior:none!important;
 }
 html body .toolbar{
   position:fixed!important;top:0!important;left:0!important;right:0!important;
   bottom:auto!important;width:100%!important;max-width:100vw!important;
   z-index:1500!important;overflow:visible!important;
 }
 html body .toolbar .toolbar-inner{
   display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;
   grid-template-rows:auto auto!important;gap:4px 8px!important;
   width:100%!important;max-width:100%!important;
   height:auto!important;max-height:none!important;min-height:0!important;
   padding:7px clamp(7px,2vw,12px)!important;
   overflow:visible!important;box-sizing:border-box!important;
 }
 html body .toolbar .nav-toprow{display:contents!important}
 html body .toolbar .view-switcher{
   grid-row:1!important;grid-column:1!important;
   justify-self:start!important;min-width:0!important;max-width:100%!important;
 }
 html body .toolbar .tool-actions{
   grid-row:1!important;grid-column:2!important;
   justify-self:end!important;min-width:0!important;width:auto!important;
 }
 html body .toolbar nav.tabs.proposal-sections{
   grid-row:2!important;grid-column:1/-1!important;
   display:flex!important;width:100%!important;max-width:100%!important;
   height:39px!important;min-height:39px!important;max-height:39px!important;
   margin:0!important;gap:4px!important;white-space:nowrap!important;
   overflow-x:auto!important;overflow-y:hidden!important;
   scrollbar-width:none!important;-webkit-overflow-scrolling:touch!important;
 }
 html body .toolbar nav.tabs.proposal-sections::-webkit-scrollbar{display:none!important}
 html body .toolbar nav.tabs.proposal-sections button.tab{
   flex:0 0 auto!important;min-height:34px!important;height:34px!important;
   padding:0 10px!important;white-space:nowrap!important;
 }
 html body .viewport[data-reading-mode="paged"]{
   position:fixed!important;
   top:var(--fm-mobile-toolbar-height,94px)!important;
   bottom:var(--fm-mobile-rail-height,82px)!important;
   left:0!important;right:0!important;
   box-sizing:border-box!important;display:flex!important;
   flex-direction:row!important;align-items:flex-start!important;
   justify-content:flex-start!important;
   width:100%!important;height:auto!important;max-width:100vw!important;
   min-height:0!important;max-height:none!important;
   margin:0!important;padding:8px!important;
   overflow:auto!important;overscroll-behavior:contain!important;
   -webkit-overflow-scrolling:touch!important;
   background:#faf7fa!important;
   scroll-snap-type:none!important;
 }
 html body .viewport[data-reading-mode="paged"] > .sheet,
 html body .viewport[data-reading-mode="paged"] > .sheet:not(.is-active){
   display:none!important;
 }
 html body .viewport[data-reading-mode="paged"] > .sheet.is-active{
   display:flex!important;flex-direction:column!important;flex-shrink:0!important;
   position:relative!important;
   width:210mm!important;min-width:210mm!important;max-width:210mm!important;
   height:297mm!important;min-height:297mm!important;max-height:297mm!important;
   margin:auto!important;padding:0!important;
   overflow:hidden!important;
   box-sizing:border-box!important;
   scroll-snap-align:none!important;
   border-radius:2px!important;
 }
 html body .viewport[data-reading-mode="paged"] > .sheet .sheet-body{
   flex:1 1 auto!important;min-height:0!important;
 }
 html body .viewport[data-reading-mode="paged"] > .chapter-divider{display:none!important}
 html body .fm-zoom{
   position:fixed!important;z-index:1600!important;top:auto!important;
   left:50%!important;right:auto!important;
   bottom:calc(8px + env(safe-area-inset-bottom,0px))!important;
   transform:translateX(-50%)!important;
   width:min(364px,calc(100vw - 16px))!important;
   max-width:calc(100vw - 16px)!important;
   height:56px!important;min-height:56px!important;
   padding:6px!important;gap:5px!important;
   overflow:hidden!important;
 }
 html body .fm-zoom button{touch-action:manipulation!important}
 html body .fm-zoom .fm-story-prev,
 html body .fm-zoom .fm-story-next{
   flex:0 0 36px!important;width:36px!important;min-width:36px!important;
   height:38px!important;min-height:38px!important;
 }
 html body .fm-zoom .fm-story-counter{min-width:52px!important}
 html body .fm-zoom .fm-zoom-minus,
 html body .fm-zoom .fm-zoom-plus{
   flex:0 0 28px!important;width:28px!important;min-width:28px!important;
 }
 html body .fm-zoom .fm-zoom-fit{
   flex:0 0 34px!important;width:34px!important;min-width:34px!important;
 }
 html body .ps-v22-dialog{
   position:fixed!important;inset:0!important;
   width:100vw!important;height:100dvh!important;
 }
}
@media screen and (max-width:360px){
 html body .toolbar .toolbar-inner{gap:3px 5px!important;padding:5px 6px!important}
 html body .toolbar .view-switch{font-size:10px!important;padding:0 7px!important}
 html body .toolbar .pdf-btn{font-size:9px!important;padding:0 7px!important}
 html body .toolbar nav.tabs.proposal-sections button.tab{font-size:11px!important;padding:0 8px!important}
 html body .fm-zoom{gap:3px!important;padding:5px!important}
}
@media screen and (max-height:550px) and (max-width:1024px){
 html body .toolbar .toolbar-inner{padding-top:3px!important;padding-bottom:3px!important}
 html body .viewport[data-reading-mode="paged"]{padding:4px!important}
}
@media print{
 html body .viewport[data-reading-mode="paged"]{position:static!important}
 html body .viewport[data-reading-mode="paged"] > .sheet,
 html body .viewport[data-reading-mode="paged"] > .sheet:not(.is-active){
   display:flex!important;zoom:1!important;width:210mm!important;
   height:297mm!important;min-height:297mm!important;overflow:hidden!important;
 }
}
</style>
'''
assert "id=\"fahmai-responsive-reader-v23\"" not in source
source = source.replace("</head>", mobile_css + "</head>", 1)

# The toolbar and bottom controls have variable heights on browsers with
# dynamic safe areas. Derive fixed-reader boundaries from measured controls.
mobile_js = r'''
<script id="fahmai-responsive-controller-v23">(function(){
 "use strict";
 const reader=document.querySelector(".viewport");
 const toolbar=document.querySelector(".toolbar");
 const rail=document.querySelector(".fm-zoom");
 if(!reader||!toolbar||!rail)return;
 let queued=false;
 function boundaries(){
   queued=false;
   if(window.innerWidth>1024)return;
   const top=Math.ceil(toolbar.getBoundingClientRect().height);
   const bottom=Math.ceil(rail.getBoundingClientRect().height)+24;
   document.documentElement.style.setProperty("--fm-mobile-toolbar-height",top+"px");
   document.documentElement.style.setProperty("--fm-mobile-rail-height",bottom+"px");
 }
 function queue(){
   if(queued)return;
   queued=true;
   requestAnimationFrame(boundaries);
 }
 boundaries();
 if(window.ResizeObserver){
   const observer=new ResizeObserver(queue);
   observer.observe(toolbar);observer.observe(rail);
 }
 window.addEventListener("resize",queue,{passive:true});
 window.addEventListener("orientationchange",queue,{passive:true});
 window.addEventListener("pageshow",function(){
   // A restored Safari page must not restore its old scroll position.
   if(window.scrollY)window.scrollTo({top:0,left:0,behavior:"instant"});
   queue();
 });
 document.addEventListener("visibilitychange",function(){
   if(!document.hidden)queue();
 });
 queue();
})();</script>
'''
source = source.replace("</body>", mobile_js + "</body>", 1)

# Defer all offscreen HTML images so iPhone Safari does not decode every slide
# when opening Overview. Eager-load only the first (Overview) slide.
img_count = 0
def defer(m):
    global img_count
    tag=m.group(0)
    if 'loading=' in tag or 'decoding=' in tag:
        return tag
    img_count+=1
    return tag[:-1] + ' loading="lazy" decoding="async">'
overview_end = source.find('</article>', source.find('id="overview"'))
source = source[:overview_end] + re.sub(r'<img\b[^>]*>', defer, source[overview_end:])
print(f"Marked {img_count} offscreen slide images for lazy decoding")
target.write_text(source,encoding="utf-8")
print(f"FINAL_HTML_BYTES={target.stat().st_size}")
print(f"ASSET_BYTES={sum(found.values())}")
