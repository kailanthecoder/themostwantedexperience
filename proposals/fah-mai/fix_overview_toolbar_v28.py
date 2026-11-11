#!/usr/bin/env python3
"""Harden Fah Mai's A4 Overview and truly one-row mobile navigation.

Scope: CSS only. Preserve all copy, pricing, page count, PDF geometry,
brand assets, functional controls, and the three site logos.
"""
from pathlib import Path
p=Path("proposals/fah-mai/index.html")
s=p.read_text(encoding="utf-8")
assert 'id="fahmai-one-row-nav-and-pricing-v26"' in s
assert 'id="fahmai-fixed-paper-geometry-v25"' in s
assert 'id="overview"' in s
assert 'id="fahmai-zero-overlap-v28"' not in s
css=r'''
<style id="fahmai-zero-overlap-v28">
/* This is the SAME A4 page on every device. Keep the visual design on the
   paper fixed and scale only the complete page in the existing reader. */
@media screen, print {
  /* One full-width heading and seven generously spaced, readable benefits.
     The prior 4-item row inside a half-width column caused icon collisions. */
  html body #overview .roadmap-callout {
    box-sizing:border-box!important;
    display:grid!important;
    grid-template-columns:minmax(0,1fr)!important;
    grid-template-rows:auto auto!important;
    gap:9px 0!important;
    align-items:stretch!important;
    min-height:0!important;
    height:auto!important;
    padding:13px 18px!important;
  }
  html body #overview .roadmap-title{
    box-sizing:border-box!important;display:block!important;
    width:100%!important;max-width:none!important;
    margin:0!important;
    font-family:"Sora",sans-serif!important;
    font-size:15px!important;
    line-height:1.26!important;
    font-weight:750!important;
    letter-spacing:-.42px!important;
    white-space:normal!important;
  }
  html body #overview .roadmap-callout .promise-grid{
    box-sizing:border-box!important;display:grid!important;
    width:100%!important;min-width:0!important;
    max-width:100%!important;
    grid-template-columns:repeat(12,minmax(0,1fr))!important;
    grid-template-rows:repeat(2,minmax(23px,auto))!important;
    gap:5px 8px!important;
    justify-items:stretch!important;align-items:center!important;
    overflow:visible!important;
  }
  html body #overview .roadmap-callout .promise-grid .promise{
    display:flex!important;flex-direction:row!important;
    align-items:center!important;justify-content:flex-start!important;
    min-width:0!important;max-width:100%!important;width:100%!important;
    gap:7px!important;overflow:visible!important;
    font-family:"Source Sans 3",sans-serif!important;
    font-size:10px!important;font-weight:750!important;
    line-height:1.2!important;white-space:normal!important;
    padding:0!important;margin:0!important;
  }
  html body #overview .roadmap-callout .promise-grid .promise svg{
    box-sizing:border-box!important;
    flex:0 0 17px!important;min-width:17px!important;max-width:17px!important;
    width:17px!important;height:17px!important;max-height:17px!important;
    display:block!important;overflow:visible!important;
  }
  html body #overview .roadmap-callout .promise-grid .promise span{
    box-sizing:border-box!important;
    display:block!important;flex:1 1 auto!important;
    min-width:0!important;max-width:100%!important;
    overflow-wrap:break-word!important;word-break:normal!important;
    white-space:normal!important;
    font-family:"Source Sans 3",sans-serif!important;
    font-size:10px!important;font-weight:760!important;
    line-height:1.18!important;letter-spacing:0!important;
  }
  /* Four across the first row; three across the second. Each has a real
     available column, so even the longest label cannot cross into the next. */
  html body #overview .promise-grid .promise:nth-child(1){grid-column:1/4!important;grid-row:1!important}
  html body #overview .promise-grid .promise:nth-child(2){grid-column:4/7!important;grid-row:1!important}
  html body #overview .promise-grid .promise:nth-child(3){grid-column:7/10!important;grid-row:1!important}
  html body #overview .promise-grid .promise:nth-child(4){grid-column:10/13!important;grid-row:1!important}
  html body #overview .promise-grid .promise:nth-child(5){grid-column:1/5!important;grid-row:2!important}
  html body #overview .promise-grid .promise:nth-child(6){grid-column:5/9!important;grid-row:2!important}
  html body #overview .promise-grid .promise:nth-child(7){grid-column:9/13!important;grid-row:2!important}
}
/* Mobile toolbar: all labels remain on ONE actual row, not a 2-row grid.
   Keep 32-34px tappable height and progressively smaller text on phones.
   The paper itself is never resized by these media queries. */
@media screen and (max-width:1024px){
 html body .toolbar{position:fixed!important;inset:0 0 auto!important;z-index:1500!important}
 html body .toolbar .toolbar-inner{
   display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;
   align-items:center!important;justify-content:space-between!important;
   box-sizing:border-box!important;
   height:48px!important;min-height:48px!important;max-height:48px!important;
   width:100%!important;max-width:100%!important;
   padding:0 6px!important;gap:4px!important;
   overflow:hidden!important;margin:0 auto!important;
 }
 html body .toolbar .nav-toprow{display:contents!important}
 html body .toolbar .view-switcher,
 html body .toolbar .tool-actions{
   grid-column:auto!important;grid-row:auto!important;justify-self:auto!important;
   flex:0 0 auto!important;width:auto!important;max-width:none!important;
   min-width:0!important;margin:0!important;
 }
 html body .toolbar .view-switcher{
   display:inline-flex!important;align-items:center!important;
   padding:2px!important;gap:0!important;
 }
 html body .toolbar .view-switch{
   display:inline-flex!important;align-items:center!important;justify-content:center!important;
   flex:0 0 auto!important;
   padding:0 7px!important;
   height:32px!important;min-height:32px!important;
   font:750 9px/1 "Source Sans 3",sans-serif!important;
   white-space:nowrap!important;
 }
 html body .toolbar nav.tabs.proposal-sections{
   display:flex!important;flex:1 1 auto!important;order:1!important;
   grid-row:auto!important;grid-column:auto!important;
   align-items:center!important;justify-content:space-between!important;
   flex-flow:row nowrap!important;flex-wrap:nowrap!important;
   box-sizing:border-box!important;min-width:0!important;
   width:auto!important;max-width:none!important;
   height:38px!important;min-height:38px!important;max-height:38px!important;
   padding:0!important;margin:0!important;gap:1px!important;
   overflow-x:auto!important;overflow-y:hidden!important;scrollbar-width:none!important;
   scroll-snap-type:none!important;
 }
 html body .toolbar nav.tabs.proposal-sections[hidden]{display:none!important}
 html body .toolbar nav.tabs.proposal-sections button.tab,
 html body .toolbar nav.tabs.proposal-sections button#tab-proposed {
   box-sizing:border-box!important;
   flex:0 0 auto!important;
   height:32px!important;min-height:32px!important;
   padding:0 5px!important;margin:0!important;
   font:750 9px/1 "Source Sans 3",sans-serif!important;
   letter-spacing:0!important;white-space:nowrap!important;
 }
 html body .toolbar .tool-actions{
   order:2!important;display:flex!important;align-items:center!important;
   padding:0!important;gap:0!important;
 }
 html body .toolbar .pdf-btn{
   box-sizing:border-box!important;
   height:32px!important;min-height:32px!important;
   padding:0 7px!important;margin:0!important;
   font:750 9px/1 "Source Sans 3",sans-serif!important;
   white-space:nowrap!important;
 }
}
@media screen and (max-width:430px){
 html body .toolbar .toolbar-inner{padding:0 4px!important;gap:2px!important}
 html body .toolbar .view-switch{font-size:8px!important;padding:0 4px!important}
 html body .toolbar nav.tabs.proposal-sections{gap:0!important;justify-content:space-between!important}
 html body .toolbar nav.tabs.proposal-sections button.tab,
 html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
   font-size:8px!important;padding:0 3px!important;
 }
 html body .toolbar .pdf-btn{font-size:8px!important;padding:0 5px!important}
}
@media screen and (max-width:360px){
 html body .toolbar .toolbar-inner{padding:0 3px!important;gap:1px!important}
 html body .toolbar .view-switch{font-size:7.5px!important;padding:0 3px!important}
 html body .toolbar nav.tabs.proposal-sections button.tab,
 html body .toolbar nav.tabs.proposal-sections button#tab-proposed{
   font-size:7.5px!important;padding:0 2px!important;
 }
 html body .toolbar .pdf-btn{font-size:7.5px!important;padding:0 4px!important}
}
/* Cursor and touch states must retain contrast on both the active bright
   pink Next arrow and the muted Previous arrow. */
@media screen{
 html body .fm-zoom .fm-story-next:not(:disabled),
 html body .fm-zoom .fm-story-next:not(:disabled):hover,
 html body .fm-zoom .fm-story-next:not(:disabled):active,
 html body .fm-zoom .fm-story-next:not(:disabled):focus-visible{
   background:#c92a79!important;color:#fff!important;
   -webkit-text-fill-color:#fff!important;
 }
 html body .fm-zoom .fm-story-prev:not(:disabled),
 html body .fm-zoom .fm-story-prev:not(:disabled):hover,
 html body .fm-zoom .fm-story-prev:not(:disabled):active,
 html body .fm-zoom .fm-story-prev:not(:disabled):focus-visible{
   background:#f6eaf0!important;color:#4b3042!important;
   -webkit-text-fill-color:#4b3042!important;
 }
}
</style>
'''
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding="utf-8")
print('V28_PATCH_OK',len(s))
