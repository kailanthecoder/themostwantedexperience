from pathlib import Path
import base64,hashlib,re

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
if 'id="fahmai-pagespeed-v11"' in html:
    print('PAGESPEED_V11_ALREADY_INSTALLED')
    raise SystemExit(0)
assert html.count('—')==0, 'Do not reintroduce em dashes'

src=root/'pagespeed-evidence-v11.avif.b64'
asset=root/'pagespeed-evidence-v11.avif'
data=base64.b64decode(src.read_text(encoding='ascii').strip(),validate=True)
sha=hashlib.sha256(data).hexdigest()
assert sha=='d35b41245888a59bf4af66a80a86727fb739f69a913cee050fa30d83304a66ba',f'Speed evidence original asset mismatch: {sha}'
assert data[4:12]==b'ftypavif', 'Expected AVIF screenshot strip'
asset.write_bytes(data)
print('PAGESPEED_IMAGE_VERIFIED',len(data),'bytes, original screenshots 5')

pattern=r'<article\b[^>]*\bid="current"[^>]*>[\s\S]*?</article>'
m=re.search(pattern,html)
assert m,'Current sheet not found'
article=m.group(0)
assert article.count('<div class="audit-v5-carousel"')==1, 'Expected original website screenshot carousel'
assert article.count('<div class="audit-v5-observation"')==1, 'Expected mobile performance finding'
switch=(root/'pagespeed_toggle_v11.html').read_text(encoding='utf-8')
gallery=(root/'pagespeed_carousel_v11.html').read_text(encoding='utf-8')
article,n1=re.subn(r'(?=<div class="audit-v5-carousel")',lambda m:switch+'  ',article,count=1)
assert n1==1
article,n2=re.subn(r'(?=<div class="audit-v5-observation")',lambda m:gallery+'  ',article,count=1)
assert n2==1

# Avoid an all-caps micro-label in the new view; the page already explains
# that these are historical test screenshots.
article=article.replace('LIVE WEBSITE CAPTURES · NOVEMBER 2026','Google PageSpeed tests, 11 November 2026',1)
html=html[:m.start()]+article+html[m.end():]

css=(root/'pagespeed_carousel_v11.css').read_text(encoding='utf-8')
js=(root/'pagespeed_carousel_v11.js').read_text(encoding='utf-8')
assert '</head>' in html and '</body>' in html
html=html.replace('</head>','<style id="fahmai-pagespeed-v11">'+css+'</style>\n</head>',1)
html=html.replace('</body>','<script id="fahmai-pagespeed-carousel-v11">'+js+'</script>\n</body>',1)
assert html.count('ps-report-image')>1
assert html.count('id="fahmai-pagespeed-v11"')==1
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html))==12
assert '—' not in html
page.write_text(html,encoding='utf-8')
print('PAGESPEED_CAROUSEL_READY','page_count',12,'html_size',len(html),'slots',5,'modes',2)
