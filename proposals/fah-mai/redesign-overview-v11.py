from pathlib import Path
from bs4 import BeautifulSoup
import re,io,requests,base64
from PIL import Image

path=Path("proposals/fah-mai/index.html")
src=path.read_text()
assert len(src)>1_000_000 and "id=\"overview\"" in src and "id=\"tab-examples\"" in src
assert 'id="fahmai-first-page-statement-v11"' not in src

url="https://book.usemostwanted.com/kailan-profile-cutout.png"
r=requests.get(url,timeout=25,headers={"User-Agent":"Mozilla/5.0 Chrome/131"})
r.raise_for_status()
img=Image.open(io.BytesIO(r.content))
assert img.width>=300 and img.height>=300 and img.mode in ("RGBA","P","LA"),("Unexpected portrait",img.mode,img.size)
portrait="data:image/png;base64,"+base64.b64encode(r.content).decode()

def icon(name):
 paths={
  "bolt":'<path d="m13 2-3 8h7l-9 12 3-9H5z"/>',
  "check":'<circle cx="12" cy="12" r="9"/><path d="m8.2 12 2.5 2.5 5.1-5.4"/>',
  "shield":'<path d="M12 2 4 5v6c0 5.3 3.7 8.7 8 11 4.3-2.3 8-5.7 8-11V5l-8-3Z"/><path d="m8.3 12 2.7 2.7 4.8-5"/>',
  "diamond":'<path d="m12 2 9 10-9 10L3 12 12 2Z"/><path d="M3 12h18"/>',
  "tag":'<path d="M11 3H4v7l10 10 7-7L11 3Z"/><circle cx="8" cy="8" r="1"/>',
  "infinity":'<path d="M6 16.1C3.6 16.1 2 14.4 2 12s1.7-4.1 4-4.1c4.1 0 7.3 8.2 12 8.2 2.3 0 4-1.7 4-4.1s-1.7-4.1-4-4.1C13.3 7.9 10.1 16.1 6 16.1Z"/>',
  "headset":'<path d="M3 14v-3a9 9 0 0 1 18 0v3"/><path d="M3 13h3v7H5a2 2 0 0 1-2-2v-5ZM21 13h-3v7h1a2 2 0 0 0 2-2v-5Z"/>'
 }
 assert name in paths
 return '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[name]+'</svg>'

features=[
 ("Fast Execution","bolt"),
 ("Right First Time","check"),
 ("Future Proofed","shield"),
 ("Unbeatable Design","diamond"),
 ("Competitive Pricing","tag"),
 ("Unlimited Features","infinity"),
 ("Ongoing Support","headset")
]
icons_html=''.join(f'<div class="promise">{icon(ic)}<span>{label}</span></div>' for label,ic in features)

new_block=f'''<div class="sheet-section statement-firstpage">
  <div class="vision-intro">Under Kailan’s leadership, Most Wanted specialises in the design-led, AI-assisted transformation that could catapult Fah Mai into its next phase of growth. I began developing all three websites with my existing technology stack, but reached my available AI-credit limit before completing them. This proposal lays out the vision and a clear path to delivery.</div>
  <div class="vision-grid" aria-label="Three group design outcomes">
    <div class="vision-card vision-card-a"><strong>A Confidence &amp; Transparency Led FMH Shape-Up</strong></div>
    <div class="vision-card vision-card-b"><strong>A Breathtakingly User-Friendly Auctioning System For WB</strong></div>
    <div class="vision-card vision-card-c"><strong>Re-Envisioned Frontend, A Powerfully Simple Backend.</strong></div>
  </div>
  <div class="roadmap-callout">
    <div class="roadmap-title">A 3-Stage, <span>10–20 Day Plan</span> To Re-Envision FMH &amp; Subsidiaries.</div>
    <div class="promise-grid">{icons_html}</div>
  </div>
  <div class="stage-runway" aria-label="Three next steps">
    <div class="stage-card"><span class="stage-no">01</span><p>We discuss the vision in person at your office or over Zoom.</p></div>
    <div class="stage-card"><span class="stage-no">02</span><p>We confirm Phase 1, including funding for AI development credits.</p></div>
    <div class="stage-card"><span class="stage-no">03</span><p>First drafts arrive within three days. The project deposit is then taken.</p></div>
  </div>
  <div class="personal-signoff">
    <div class="signoff-photo"><img src="{portrait}" alt="Portrait of Kailan Spall from the Most Wanted booking website"></div>
    <div class="signoff-content">
      <div class="signoff-message">Thank you for considering my proposal,</div>
      <div class="signoff-yours">Yours truly,</div>
      <div class="signoff-name">Kailan Spall</div>
      <div class="signoff-position">Owner of Most Wanted <span>(and, if all goes well, your #1 salesman)</span></div>
      <div class="signoff-contact"><a href="mailto:mr@kailanspall.com">mr@kailanspall.com</a><span class="signoff-contact-separator">/</span><a href="tel:+573016349877">+57 301 634 9877</a></div>
    </div>
  </div>
</div>'''

m=re.search(r'(<article\b[^>]*\bid="overview"[^>]*>)([\s\S]*?)(</article>)',src)
assert m, "Overview page not found"
soup=BeautifulSoup(m.group(0),"html.parser")
target=soup.select_one(".sheet-section")
assert target and target.select_one(".feature-columns") and target.select_one(".inkbox"), "Old summary cards or pilot callout not found"
target.replace_with(BeautifulSoup(new_block,"html.parser").select_one(".statement-firstpage"))
updated=src[:m.start()]+str(soup.article)+src[m.end():]
assert 'id="tab-examples"' in updated and updated.count('A Breathtakingly User-Friendly Auctioning System For WB')==1

style=r'''
<style id="fahmai-first-page-statement-v11">
/* The first sheet is a designed one-page statement, not an extra scrolling webpage. */
#overview .sheet-body{padding-top:16px!important;padding-bottom:11px!important}
#overview .page-heading{padding-bottom:9px!important}
#overview .page-heading h1{font-size:26.5px!important;line-height:1.145!important;letter-spacing:-.9px!important;max-width:710px!important}
#overview .page-heading .sub{font-size:11.4px!important;line-height:1.48!important;margin-top:6px!important;font-weight:600!important}
#overview .sheet-section.statement-firstpage{display:flex!important;flex-direction:column!important;gap:10px!important;padding-top:9px!important;margin-top:0!important}
#overview .vision-intro{
 padding:10px 14px!important;background:#faf4f7!important;border-left:3px solid #dd227c!important;
 border-radius:0 11px 11px 0!important;color:#43343e!important;
 font-family:'Figtree',sans-serif!important;font-size:11px!important;line-height:1.45!important;
 font-weight:650!important;letter-spacing:0!important;
}
#overview .vision-grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
 gap:11px!important;width:100%!important;justify-items:center!important}
#overview .vision-card{
 position:relative!important;box-sizing:border-box!important;overflow:hidden!important;isolation:isolate!important;
 display:flex!important;align-items:flex-end!important;padding:18px 16px 17px!important;
 width:100%!important;max-width:203px!important;aspect-ratio:1 / 1!important;min-width:0!important;
 border:1px solid rgba(255,255,255,.15)!important;border-radius:16px!important;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.23),0 9px 18px rgba(50,14,37,.085)!important;
 color:#fff!important;text-align:left!important;
}
#overview .vision-card::before{
 content:"";pointer-events:none;position:absolute;z-index:-1;inset:-35%;
 border-radius:50%;transform:rotate(-24deg);
 background:radial-gradient(ellipse at 75% 15%,rgba(255,206,238,.42),transparent 32%),radial-gradient(ellipse at 0% 95%,rgba(0,0,0,.54),transparent 43%);
}
#overview .vision-card::after{
 content:"";pointer-events:none;position:absolute;z-index:-1;
 inset:10px;border-radius:10px;border:1px solid rgba(255,255,255,.115);
}
#overview .vision-card-a{background:radial-gradient(circle at 68% 5%,#dd2f9d 0%,transparent 49%),linear-gradient(140deg,#150e22 7%,#421339 54%,#e12f8a 100%)!important}
#overview .vision-card-b{background:radial-gradient(circle at 20% 17%,#f95ba7 0%,transparent 48%),linear-gradient(145deg,#29122d 2%,#9a195d 59%,#100c19 100%)!important}
#overview .vision-card-c{background:radial-gradient(circle at 90% 90%,#f646a5 0%,transparent 50%),linear-gradient(135deg,#100d19 2%,#2f1534 53%,#ab1c76 100%)!important}
#overview .vision-card strong{
 font-family:'Poppins',Arial,sans-serif!important;font-size:15.1px!important;
 font-weight:800!important;line-height:1.38!important;letter-spacing:-.37px!important;
 color:white!important;text-shadow:0 1px 8px rgba(20,6,14,.28)!important;max-width:100%!important;
}
#overview .roadmap-callout{
 box-sizing:border-box!important;width:100%!important;display:grid!important;
 grid-template-columns:minmax(0, .87fr) minmax(0,1.28fr)!important;
 align-items:center!important;column-gap:16px!important;padding:15px 19px!important;
 border-radius:18px!important;
 background:radial-gradient(circle at 91% -20%,rgba(251,54,155,.43),transparent 53%),
 linear-gradient(120deg,#160f1d 0%,#361534 55%,#6c194c 100%)!important;
 border:1px solid rgba(244,72,158,.24)!important;
 color:white!important;min-height:116px!important;box-shadow:0 8px 20px rgba(41,17,31,.1)!important;
}
#overview .roadmap-title{
 font-family:'Poppins',Arial,sans-serif!important;font-size:18px!important;font-weight:800!important;
 line-height:1.33!important;letter-spacing:-.55px!important;max-width:280px!important;
}
#overview .roadmap-title span{color:#ff93c5!important}
#overview .promise-grid{
 display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;
 grid-template-rows:repeat(2, minmax(0,1fr))!important;
 gap:8px 7px!important;align-items:stretch!important;width:100%!important;
}
#overview .promise{display:flex!important;align-items:center!important;justify-content:flex-start!important;
 gap:5px!important;min-width:0!important;padding:0!important;color:#fff!important;
 font-family:'Figtree',Arial,sans-serif!important;font-size:9.2px!important;font-weight:750!important;
 line-height:1.2!important}
#overview .promise svg{flex:0 0 18px!important;width:18px!important;height:18px!important;opacity:.95!important;stroke:#ffb4d8!important}
#overview .stage-runway{
 display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
 gap:9px!important;width:100%!important;
}
#overview .stage-card{
 box-sizing:border-box!important;min-height:84px!important;display:flex!important;align-items:flex-start!important;gap:10px!important;
 padding:13px 11px!important;border-radius:13px!important;
 border:1px solid #f1e0e8!important;background:#fffafd!important;
}
#overview .stage-card:nth-child(2){background:#ffe9f3!important;border-color:#f6d4e5!important}
#overview .stage-card:nth-child(3){background:#f8eff4!important}
#overview .stage-no{display:grid!important;place-items:center!important;flex:0 0 30px!important;height:30px!important;
 background:linear-gradient(135deg,#ec2487,#ab166b)!important;border-radius:50%!important;
 color:#fff!important;font-family:'Poppins',sans-serif!important;font-size:11px!important;font-weight:800!important}
#overview .stage-card p{margin:1px 0 0!important;color:#3b3039!important;font-family:'Figtree',sans-serif!important;
 font-size:10.7px!important;font-weight:700!important;line-height:1.38!important}
#overview .personal-signoff{
 min-height:124px!important;box-sizing:border-box!important;
 display:grid!important;grid-template-columns:122px minmax(0,1fr)!important;align-items:stretch!important;gap:18px!important;
 padding:0 17px 0 0!important;overflow:hidden!important;border-radius:16px!important;
 border:1px solid #e8d3df!important;
 background:linear-gradient(120deg,#fae6f0 0%,#fffafd 42%,#fff 100%)!important;
}
#overview .signoff-photo{display:flex!important;align-items:flex-end!important;justify-content:center!important;
 position:relative!important;overflow:hidden!important;min-height:124px!important;
 background:radial-gradient(circle at 38% 23%,#fff 0%,#f8c8e0 60%,#ed95bd 100%)!important}
#overview .signoff-photo img{display:block!important;width:130px!important;height:135px!important;
 object-fit:cover!important;object-position:center 18%!important;margin-bottom:-4px!important}
#overview .signoff-content{display:flex!important;flex-direction:column!important;justify-content:center!important;
 gap:1px!important;min-width:0!important;padding:7px 0!important;color:#2f222c!important}
#overview .signoff-message{font-family:'Figtree',sans-serif!important;font-size:12.3px!important;font-weight:750!important;line-height:1.32!important}
#overview .signoff-yours{font-size:10.6px!important;font-weight:600!important;line-height:1.2!important}
#overview .signoff-name{font-family:'Poppins',sans-serif!important;font-size:19.5px!important;line-height:1.25!important;
 font-weight:900!important;letter-spacing:-.65px!important;color:#20141f!important}
#overview .signoff-position{font-size:10.5px!important;line-height:1.38!important;font-weight:800!important}
#overview .signoff-position span{font-weight:650!important}
#overview .signoff-contact{display:flex!important;flex-wrap:wrap!important;gap:7px!important;align-items:center!important;
 margin-top:2px!important;font-size:10.4px!important;font-weight:800!important}
#overview .signoff-contact a{color:#b11a68!important;text-decoration:none!important}
#overview .signoff-contact-separator{color:#b696a5!important}
@media print{
 #overview .vision-card,#overview .roadmap-callout,#overview .personal-signoff,#overview .stage-card{
  print-color-adjust:exact!important;-webkit-print-color-adjust:exact!important;box-shadow:none!important}
 #overview .sheet-section.statement-firstpage{gap:9px!important}
}
</style>
'''
assert '</head>' in updated
updated=updated.replace('</head>',style+'</head>',1)
path.write_text(updated)
print('REDESIGNED',path.stat().st_size,'bytes','portrait alpha',img.mode,'dimensions',img.size,flush=True)
