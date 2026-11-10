from pathlib import Path
from base64 import b64encode
import re

root=Path('proposals/fah-mai')
p=root/'index.html'
s=p.read_text(encoding='utf-8')
marker='id="fahmai-identical-brand-header-2026"'
if marker in s:
    print('Brand-header fix already applied')
    raise SystemExit(0)

favicon=(root/'brand-assets/fmh_5.png')
assert favicon.is_file(), 'Official 300px FMH brandmark missing'
icon=b64encode(favicon.read_bytes()).decode('ascii')
# Use the official FMH full-colour 300×300 brandmark, cached in the repo itself.
favicon_markup=(
    '<link rel="icon" type="image/png" sizes="300x300" '
    'href="data:image/png;base64,'+icon+'">'
    '<link rel="apple-touch-icon" sizes="300x300" href="brand-assets/fmh_5.png">'
    '<meta name="theme-color" content="#e72982">'
)
# Existing document does not yet declare a favicon; remove obsolete icon links if present.
s=re.sub(r'<link\b(?=[^>]*\brel=["\'](?:shortcut icon|icon|apple-touch-icon)["\'])[^>]*>', '', s, flags=re.I)
s=s.replace('</head>',favicon_markup+'</head>',1)

css=r"""
<style id="fahmai-identical-brand-header-2026">
/*
  The brand/presenter strip is a fixed A4 design. Mobile already shrinks
  each A4 sheet via the existing document zoom, so it must NOT ALSO
  re-layout or miniaturise its logos and typography at mobile breakpoints.
  This rule set mirrors the desktop A4 header only, not the app navigation.
*/
@media screen and (max-width:800px) {
  .sheet .identity.presentation-header {
    box-sizing:border-box!important;
    display:grid!important;
    width:100%!important;
    height:112px!important;min-height:112px!important;
    padding:9px 29px!important;
    grid-template-columns:minmax(0,1.25fr) minmax(0,.95fr)!important;
    column-gap:16px!important;row-gap:14px!important;
    align-items:center!important;
  }
  .sheet .presentation-header .presented-group {
    min-height:0!important;height:100%!important;
    display:grid!important;
    grid-template-columns:108px minmax(0,1fr)!important;
    align-content:center!important;align-items:center!important;
    justify-content:initial!important;
    gap:12px!important;
  }
  .sheet .presentation-header .presented-to {
    padding:0 16px 0 0!important;
    border-right:1px solid rgba(210,140,175,.48)!important;
  }
  .sheet .presentation-header .presented-by {padding:0 0 0 2px!important;}
  .sheet .presentation-header .presented-copy,
  .sheet .presentation-header .presented-by .presented-copy {
    display:flex!important;flex-direction:column!important;
    align-items:flex-start!important;justify-content:center!important;
    width:auto!important;min-width:0!important;flex:initial!important;
    margin:0!important;gap:3px!important;
    font-family:'Poppins','Figtree',Arial,sans-serif!important;
    font-size:16.2px!important;font-weight:800!important;
    line-height:1.1!important;letter-spacing:normal!important;text-align:left!important;
  }
  .sheet .presentation-header .presented-copy .presentation-kicker {
    display:block!important;margin:0!important;
    font-size:10px!important;line-height:1.12!important;font-weight:800!important;
    letter-spacing:1.05px!important;text-transform:uppercase!important;color:#c42570!important;
  }
  .sheet .presentation-header .presented-copy strong{
    display:block!important;margin:0!important;
    font-size:21px!important;line-height:1.04!important;
    letter-spacing:-.6px!important;font-weight:900!important;color:#261d24!important;
  }
  .sheet .presentation-header .presented-copy .presentation-sub{
    display:block!important;margin:0!important;
    font-size:10.5px!important;line-height:1.2!important;
    font-weight:600!important;letter-spacing:0!important;color:#7c6e78!important;
  }
  .sheet .presentation-header .client-lockups,
  .sheet .presentation-header .presenter-lockups {
    display:flex!important;align-items:center!important;
    justify-content:flex-start!important;
    width:auto!important;min-width:0!important;flex:initial!important;
    height:62px!important;min-height:0!important;margin:0!important;
  }
  .sheet .presentation-header .client-lockups{gap:11px!important;}
  .sheet .presentation-header .presenter-lockups{gap:14px!important;}
  .sheet .presentation-header .client-lockups .original-brand{
    display:flex!important;align-items:center!important;justify-content:center!important;
    height:61px!important;min-height:61px!important;max-height:61px!important;
    min-width:0!important;flex:0 0 auto!important;
    padding:0!important;margin:0!important;opacity:1!important;
  }
  .sheet .presentation-header .original-brand.brand-fmh{width:51px!important;min-width:51px!important;}
  .sheet .presentation-header .original-brand.brand-bull{width:52px!important;min-width:52px!important;}
  .sheet .presentation-header .original-brand.brand-pc{width:126px!important;min-width:126px!important;}
  .sheet .presentation-header .original-brand.brand-fmh img{
    width:49px!important;height:49px!important;max-width:49px!important;max-height:49px!important;
  }
  .sheet .presentation-header .original-brand.brand-bull img{
    width:49px!important;height:54px!important;max-width:49px!important;max-height:54px!important;
  }
  .sheet .presentation-header .original-brand.brand-pc img{
    width:124px!important;height:50px!important;max-width:124px!important;max-height:50px!important;
  }
  .sheet .presentation-header .original-brand img {
    display:block!important;object-fit:contain!important;object-position:center!important;
    padding:0!important;mix-blend-mode:normal!important;margin:auto!important;
  }
  .sheet .presentation-header .mw-black {
    display:flex!important;align-items:center!important;justify-content:center!important;
    min-width:58px!important;max-width:58px!important;width:58px!important;
    height:61px!important;
    background:transparent!important;border:0!important;box-shadow:none!important;
    padding:0!important;margin:0!important;
  }
  .sheet .presentation-header .mw-black img {
    width:54px!important;height:54px!important;max-width:54px!important;max-height:54px!important;
    display:block!important;object-fit:contain!important;filter:brightness(0)!important;
    background:transparent!important;margin:0!important;
  }
  .sheet .presentation-header .signature-logo{
    display:block!important;width:69px!important;height:40px!important;
    min-width:69px!important;max-width:69px!important;max-height:40px!important;
    object-fit:contain!important;margin:0!important;
  }
  .sheet .presentation-hairline{
    height:1px!important;flex:0 0 1px!important;
    margin:0 40px!important;background:#ece2e7!important;
  }
}
</style>
"""
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding='utf-8')
print('Updated mobile A4 brandbar to match desktop and installed official FMH favicon.',
      'favicon_bytes=',favicon.stat().st_size,'page_bytes=',p.stat().st_size,
      'header_count=',s.count('class="identity presentation-header"'))
