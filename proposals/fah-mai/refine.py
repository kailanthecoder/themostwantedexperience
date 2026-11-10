import pathlib, requests, base64, re
p=pathlib.Path("proposals/fah-mai/index.html")
html=p.read_text()
if 'id="fahmai-rounded-editorial-v4"' in html:
 print("Already redesigned")
 raise SystemExit(0)
imgURLs={
"casks":"https://www.platinumcask.com/assets/img-grid-Cask-Shop-land-2a419852df037ce0797de2d3a3fdfd692ee08465dfbadf1553b3b5d490bc1688.webp",
"bottles":"https://www.platinumcask.com/assets/img-grid-Whisky-Shop-land-324bd7ca5adcb645cda5036d11cc417f9872f147be96b880af39935af22a79c2.webp",
"fraction":"https://www.platinumcask.com/assets/img-grid-Cask-Fraction-land-37070f5fc16bcd2408acda43203a9fa31a4241a925dd3d892c2e9870013cc7f6.webp"}
s=requests.Session(); s.headers["User-Agent"]="Mozilla/5.0 Chrome/131 Safari/537.36"
data={}
for k,u in imgURLs.items():
 r=s.get(u,timeout=30);r.raise_for_status()
 assert r.content[:4]==b'RIFF',f"{k} does not look like a WEBP"
 data[k]="data:image/webp;base64,"+base64.b64encode(r.content).decode()
 print(k,len(r.content))
css=r"""
<style id="fahmai-rounded-editorial-v4">
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800;900&display=swap');
:root{--pink:#e72982;--pink2:#f276ad;--deep:#251d25;--muted:#6d6269;--line:#f0dfe7}
body{font-family:'Figtree',Arial,sans-serif;font-weight:500;letter-spacing:-.1px;color:var(--deep)}
h1,h2,h3,.feature-index,.audit-brand,.small-label,.tag,.phase-status,.tool-brand{font-family:'Poppins',sans-serif}
.toolbar{background:linear-gradient(105deg,#fff 0%,#fffafd 38%,#fce6f0 100%);border-bottom:1px solid #f2d7e3;box-shadow:0 2px 14px rgba(110,46,77,.045)}
.toolbar-inner{max-width:1030px}
.tab{font-family:'Figtree',sans-serif;font-weight:800}
.tab[aria-selected="true"]{color:#241b21;border-bottom-color:#e72982}
.pdf-btn{background:#e72982;border-color:#e72982;border-radius:9px;font-family:'Figtree',sans-serif;font-weight:800}
.sheet-cap{background:linear-gradient(90deg,#dc2078,#fa8db7 54%,#de2478)}
.identity{display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;align-items:center!important;gap:14px!important;min-height:99px!important;height:99px!important;padding:8px 40px!important}
.client-lockups{display:flex!important;align-items:center!important;justify-content:center!important;gap:19px!important;height:82px!important;min-width:0!important}
.client-lockups .original-brand{display:flex!important;justify-content:center!important;align-items:center!important;height:82px!important;margin:0!important;position:relative!important}
.client-lockups .original-brand img{object-fit:contain!important;display:block!important;margin:auto!important}
.original-brand.brand-fmh{width:68px!important;min-width:68px!important}
.original-brand.brand-fmh img{height:58px!important;width:58px!important;max-width:58px!important;max-height:58px!important}
.original-brand.brand-bull{width:80px!important;min-width:80px!important}
.original-brand.brand-bull img{height:67px!important;width:62px!important;max-width:62px!important;max-height:67px!important}
.original-brand.brand-pc{width:154px!important;min-width:154px!important}
.original-brand.brand-pc img{width:148px!important;height:61px!important;max-height:61px!important;max-width:148px!important}
.identity-right{position:relative!important;border-left:1px solid #eedfe6!important;display:flex!important;align-items:center!important;justify-content:center!important;min-width:165px!important;height:82px!important;padding:7px 0 0 13px!important}
.presenter-label{position:absolute!important;left:16px!important;top:1px!important;margin:0!important;font-size:7px!important;line-height:1!important;color:#867780!important;letter-spacing:1.15px!important}
.presenter-lockups{display:flex!important;height:70px!important;align-items:center!important;justify-content:center!important;gap:10px!important}
.mw-black{width:63px!important;min-width:63px!important;height:64px!important;display:flex!important;align-items:center!important;justify-content:center!important;padding:0!important;background:transparent!important;border:0!important}
.mw-black img{display:block!important;object-fit:contain!important;filter:brightness(0)!important;background:transparent!important;width:56px!important;height:56px!important;max-width:56px!important;max-height:56px!important}
.presenter-separator{height:23px!important;background:#e9dae2!important}
.signature-logo{width:65px!important;height:37px!important;max-width:65px!important;max-height:37px!important;object-fit:contain!important}
.heading-top{font-family:'Figtree',sans-serif;font-weight:800!important;letter-spacing:1px!important}
.page-heading h1{font-family:'Poppins',sans-serif!important;font-size:35px!important;font-weight:800!important;line-height:1.13!important;letter-spacing:-1.2px!important}
.page-heading .sub{font-size:12px!important;font-weight:600!important}
.sheet-section{padding-top:15px!important}
.tagline{margin-bottom:11px!important}
.tag{font-family:'Poppins',sans-serif;font-weight:800}
.statement{background:linear-gradient(100deg,rgba(30,18,14,.96),rgba(30,18,14,.78) 65%,rgba(30,18,14,.45)),url('__CASKS__') center/cover!important;color:#fff!important;display:flex!important;align-items:flex-end!important;min-height:158px!important;border-radius:21px!important;padding:23px 26px!important;font-family:'Poppins',sans-serif!important;font-weight:700!important;font-size:20.5px!important;line-height:1.35!important;letter-spacing:-.6px!important;max-width:none!important}
.statement strong{font-weight:800!important;color:#fff!important}
.accent-line{display:none!important}
.feature-columns{gap:12px!important;margin-top:14px!important}
.feature{border-radius:18px!important;padding:15px 16px!important;min-height:132px!important;border:1px solid #f0e2e7!important;background:#f9f6f7!important}
.feature:nth-child(2){background:#fce2ed!important;border-color:#f7d2e3!important}
.feature:nth-child(3){background:linear-gradient(135deg,#272026,#4f2b3c)!important;color:#fff!important;border-color:transparent!important}
.feature:nth-child(3) h3{color:#fff!important}
.feature:nth-child(3) p{color:#eedde6!important}
.feature h3{font-size:15px!important;font-weight:800!important;line-height:1.25!important;margin:6px 0!important;letter-spacing:-.3px!important}
.feature p{font-size:11px!important;line-height:1.55!important}
.feature-index{font-size:9px!important;font-weight:800!important}
.inkbox{background:linear-gradient(115deg,#211820,#50313f)!important;border-radius:19px!important;padding:17px 22px!important;margin-top:17px!important;gap:18px!important;align-items:center!important}
.inkbox h3{font-weight:800!important;font-size:16.5px!important;letter-spacing:-.45px!important}
.inkbox p{font-size:10.5px!important;line-height:1.55!important}
.proofline{padding:12px 0!important;font-size:10px!important;gap:8px!important}
.fineprint{font-size:8px!important;margin:5px 0 10px!important}
.brand-audit{display:grid!important;gap:11px!important;border:0!important}
.brand-audit-row{border:0!important;border-radius:18px!important;min-height:135px!important;grid-template-columns:24px 106px minmax(0,1fr)!important;gap:10px!important;padding:17px 17px!important;overflow:hidden!important}
.brand-audit-row:nth-child(1){background:#fceaf2!important}
.brand-audit-row:nth-child(2){background:linear-gradient(100deg,rgba(35,22,22,.96),rgba(35,22,22,.84)),url('__BOTTLES__') center/cover!important;color:#fff!important}
.brand-audit-row:nth-child(3){background:linear-gradient(100deg,rgba(39,24,25,.96),rgba(39,24,25,.84)),url('__FRACTION__') center/cover!important;color:#fff!important}
.brand-audit-row:nth-child(n+2) .audit-main strong,.brand-audit-row:nth-child(n+2) .audit-brand{color:#fff!important}
.brand-audit-row:nth-child(n+2) .audit-main p{color:#f1e8eb!important}
.brand-audit-row:nth-child(n+2) .audit-action b{color:#fff!important}
.audit-main strong{font-family:'Poppins',sans-serif!important;font-weight:800!important;line-height:1.25!important}
.audit-main p{font-size:10.5px!important;line-height:1.5!important;margin:6px 0 8px!important}
.audit-action{font-size:8px!important}
.audit-action b{font-size:9px!important}
.callout-outline{border:0!important;background:#fbf0f5!important;border-radius:16px!important;margin-top:14px!important;padding:14px 17px!important;line-height:1.5!important}
.spec-list,.phases,.budget-table{border:0!important}
.spec-item{background:#faf7f8!important;border:1px solid #f1e7eb!important;border-radius:18px!important;margin-bottom:10px!important;padding:15px 16px!important;grid-template-columns:27px minmax(0,1fr) 130px!important;gap:12px!important}
.spec-item:nth-child(2){background:#ffedf5!important;border-color:#fbdeeb!important}
.spec-item:nth-child(4){background:#2c222c!important;color:white!important}
.spec-item:nth-child(4) p,.spec-item:nth-child(4) .spec-output b{color:#f3e9ed!important}
.spec-item:nth-child(4) h3{color:#fff!important}
.spec-item h3{font-size:13px!important;font-weight:800!important;line-height:1.25!important}
.spec-item p{font-size:10.4px!important;line-height:1.5!important}
.spec-output{font-size:8px!important}
.limits{border-radius:16px!important;margin-top:auto!important;background:#faf0f4!important}
.phases{display:grid!important;gap:11px!important}
.phase{border:0!important;border-radius:18px!important;margin:0!important;padding:18px 18px!important;grid-template-columns:88px minmax(0,1fr)!important;gap:16px!important;background:#f9f4f6!important}
.phase:nth-child(2){background:linear-gradient(100deg,rgba(33,18,23,.97),rgba(33,18,23,.82)),url('__CASKS__') center/cover!important;color:#fff!important}
.phase:nth-child(2) h3,.phase:nth-child(2) .phase-days{color:#fff!important}
.phase:nth-child(2) p{color:#f3e8ed!important}
.phase:nth-child(3){background:#ffedf5!important}
.phase h3{font-size:15px!important;font-weight:800!important;line-height:1.2!important}
.phase p{font-size:10.8px!important;line-height:1.52!important}
.phase-days b{font-size:16px!important}
.funnel{border-radius:14px!important;margin-top:12px!important;padding:14px!important;background:#fff0f6!important}
.budget-line{border:1px solid #f0e2e9!important;border-radius:15px!important;margin:9px 0 0!important;padding:14px 16px!important;background:#fff!important}
.budget-line:nth-of-type(3){background:#fff4f8!important}
.budget-line strong{font-family:'Poppins',sans-serif;font-weight:800!important;font-size:12.5px!important}
.roi-model{background:linear-gradient(120deg,#fceaf2,#fff3f8)!important;border-radius:20px!important;margin-top:14px!important;padding:18px!important}
.delivery-line{border:1px solid #f0e5ea!important;border-radius:15px!important;margin-bottom:9px!important;padding:15px!important;background:#fbf7f9!important}
.delivery-line:nth-child(2n){background:#fff0f6!important}
.final-ask{border-radius:19px!important;background:linear-gradient(110deg,#2a1e27,#502e42)!important}
.final-ask h3{font-family:'Poppins',sans-serif;font-weight:800!important}
@media(max-width:650px){
 .identity{padding:6px 17px!important;height:86px!important;min-height:86px!important;gap:5px!important}
 .client-lockups{gap:7px!important;height:67px!important}
 .client-lockups .original-brand{height:67px!important}
 .original-brand.brand-fmh{width:40px!important;min-width:40px!important}
 .original-brand.brand-fmh img{height:39px!important;width:39px!important}
 .original-brand.brand-bull{width:48px!important;min-width:48px!important}
 .original-brand.brand-bull img{height:52px!important;width:46px!important}
 .original-brand.brand-pc{width:85px!important;min-width:85px!important}
 .original-brand.brand-pc img{width:85px!important;max-width:85px!important}
 .identity-right{min-width:105px!important;height:67px!important;padding-left:5px!important}
 .presenter-label{font-size:5px!important;left:8px!important}
 .presenter-lockups{gap:4px!important}
 .mw-black{width:44px!important;min-width:44px!important;height:48px!important}
 .mw-black img{width:39px!important;height:39px!important}
 .signature-logo{width:40px!important;height:25px!important}
}
@media print{
 body{font-family:'Figtree',Arial,sans-serif!important}
 .statement,.phase,.brand-audit-row,.inkbox{print-color-adjust:exact!important;-webkit-print-color-adjust:exact!important}
 .mw-black{background:transparent!important}
}
</style>
"""
for key,tag in [("casks","__CASKS__"),("bottles","__BOTTLES__"),("fraction","__FRACTION__")]:
 css=css.replace(tag,data[key])
assert "</head>" in html
html=html.replace("</head>",css+"</head>",1)
p.write_text(html)
print("SAVED",len(html),"image references",*[html.count(data[k]) for k in data])
