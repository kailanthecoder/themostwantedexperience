from pathlib import Path
import base64,io,json
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
d=Path("proposals/fah-mai").resolve()
html=d/"index.html"
source=html.read_text()
assert len(source)>1_000_000
assert 'id="glass-navigation-final-v9"' in source
tabs=["overview","current","spec","budget","implementation","proposed","examples"]
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  desktop=browser.new_page(viewport={"width":1390,"height":1140},device_scale_factor=1)
  desktop.goto(html.as_uri(),wait_until="domcontentloaded",timeout=60000)
  desktop.evaluate("() => document.fonts.ready")
  desktop.wait_for_timeout(600)
  buttons=desktop.locator("nav.tabs button.tab")
  actual=[buttons.nth(i).get_attribute("data-target") for i in range(buttons.count())]
  print("DESKTOP TABS",actual,flush=True)
  assert actual==tabs
  assert buttons.nth(5).inner_text().strip()=="Proposals"
  desktop.locator("#tab-proposed").click()
  desktop.wait_for_timeout(120)
  assert desktop.locator("#proposed").evaluate("(e)=>getComputedStyle(e).display")!="none", "Proposals tab failed to activate"
  desktop.locator("#tab-overview").click()
  assert desktop.locator("#overview h1").inner_text().startswith("Fah Mai Holdings Re-Envisioned:")
  assert "2026 A-tier web package" in desktop.locator("#overview .page-heading .sub").inner_text()
  assert "Under Kailan’s leadership" in desktop.locator("#overview .statement").inner_text()
  desktop.screenshot(path=str(d/"Fah-Mai-Glass-Desktop.jpg"),type="jpeg",quality=80,full_page=False)
  desktopMetrics=desktop.evaluate("""() => ({
    toolbar: (()=>{let r=document.querySelector('.toolbar').getBoundingClientRect();return {width:Math.round(r.width),height:Math.round(r.height)}})(),
    tabs:[...document.querySelectorAll('nav.tabs .tab')].map(x=>({name:x.innerText,rect:Math.round(x.getBoundingClientRect().width),inview: x.getBoundingClientRect().left < window.innerWidth})),
    heading:document.querySelector('#overview h1').innerText,
    overflow:document.documentElement.scrollWidth>window.innerWidth+5
   })""")
  print("DESKTOP",json.dumps(desktopMetrics),flush=True)
  assert not desktopMetrics["overflow"]
  for width in (768,390):
    page=browser.new_page(viewport={"width":width,"height":860},device_scale_factor=1,is_mobile=True,has_touch=True)
    page.goto(html.as_uri(),wait_until="domcontentloaded",timeout=60000)
    page.evaluate("() => document.fonts.ready")
    page.wait_for_timeout(260)
    page.locator('#tab-proposed').click()
    page.wait_for_timeout(150)
    assert page.locator('#proposed').evaluate("(e)=>getComputedStyle(e).display")!="none"
    page.locator('#tab-overview').click()
    m=page.evaluate("""() => {
      let q=document.querySelector('#overview'),v=document.querySelector('.viewport'),a=document.querySelector('.toolbar-inner'),n=document.querySelector('.tabs');
      return {w:window.innerWidth,scroll:document.documentElement.scrollWidth,bodyScroll:document.body.scrollWidth,
        zoom:getComputedStyle(q).zoom,sheetLeft:Math.round(q.getBoundingClientRect().left),sheetRight:Math.round(q.getBoundingClientRect().right),
        toolbarHeight:Math.round(a.getBoundingClientRect().height),navScroll:n.scrollWidth,navWidth:n.clientWidth,
        h1Bottom:Math.round(q.querySelector('h1').getBoundingClientRect().bottom)}
     }""")
    print("MOBILE",json.dumps(m),flush=True)
    if width==390:
      page.screenshot(path=str(d/"Fah-Mai-Glass-Mobile.jpg"),type="jpeg",quality=79,full_page=False)
    assert m["sheetLeft"]>=-3 and m["sheetRight"]<=m["w"]+7, f"A4 sheet exceeds mobile viewport: {m}"
    assert m["scroll"]<=m["w"]+20, f"horizontal overflow at {width}: {m}"
    page.close()
  # Print PDF at desktop width to ensure seven physical A4 pages.
  desktop.pdf(path=str(d/"Fah-Mai-Proposal-Glass.pdf"),format="A4",print_background=True,
    margin={"top":"0","right":"0","bottom":"0","left":"0"},prefer_css_page_size=True)
  browser.close()
pdf=d/"Fah-Mai-Proposal-Glass.pdf"
count=len(PdfReader(pdf).pages)
print("PDF",count,"pages",pdf.stat().st_size,"bytes",flush=True)
assert count==7, f"Expected seven A4 sheets; rendered {count}"
for name in ["Fah-Mai-Glass-Desktop.jpg","Fah-Mai-Glass-Mobile.jpg"]:
  d.joinpath(name.replace(".jpg",".b64.txt")).write_text(base64.b64encode(d.joinpath(name).read_bytes()).decode())
