from pathlib import Path
import base64,hashlib,re
from PIL import Image

folder=Path('proposals/fah-mai')
b64=(folder/'overview-photo-strip-v9.b64.txt').read_text(encoding='utf-8').strip()
photo=base64.b64decode(b64,validate=True)
sha=hashlib.sha256(photo).hexdigest()
assert sha=='a1d1cc6c5684979c99f1847f33b41d2a22e71b15e513ac6bc1e8adf616939716',f'Photo asset differs from supplied images: {sha}'
filename=folder/'overview-photo-strip-v9.webp'
filename.write_bytes(photo)
im=Image.open(filename)
assert im.format=='WEBP' and im.size==(360,120),f'Invalid image mosaic: {im.format} {im.size}'
print('USER_PHOTO_STRIP_VERIFIED',sha,'pixels',im.size,'bytes',len(photo))

html_path=folder/'index.html'
html=html_path.read_text(encoding='utf-8')
if 'id="fahmai-overview-photo-refresh-v9"' in html:
    print('SITE_ALREADY_UPDATED')
    raise SystemExit(0)
assert 'id="overview"' in html
for classname in ('vision-card-a','vision-card-b','vision-card-c'):
    assert classname in html
assert '—' not in html

# The current photograph layer on each card has opacity 0.22.
# Lower to 0.15, a 7-percentage-point reduction, without touching the
# existing gradient, card text, dimensions, border or storybook UI.
css='''
<style id="fahmai-overview-photo-refresh-v9">
/* Three photographs provided by the client, matching cards from left to right.
   Keep the exact pink/black gradients, outlines, labels and A4 layout. */
#overview .vision-card.vision-card-a::before,
#overview .vision-card.vision-card-b::before,
#overview .vision-card.vision-card-c::before {
    content:"" !important;
    inset:0 !important;
    width:100% !important;
    height:100% !important;
    background-image:url("./overview-photo-strip-v9.webp") !important;
    background-size:300% 100% !important;
    background-repeat:no-repeat !important;
    opacity:.15 !important;
    filter:saturate(.75) contrast(1.13) !important;
}
#overview .vision-card.vision-card-a::before { background-position:0% 50% !important; }
#overview .vision-card.vision-card-b::before { background-position:50% 50% !important; }
#overview .vision-card.vision-card-c::before { background-position:100% 50% !important; }
@media print {
 #overview .vision-card::before {
   print-color-adjust:exact!important;
   -webkit-print-color-adjust:exact!important;
 }
}
</style>
'''
assert '</head>' in html
html=html.replace('</head>',css+'\n</head>',1)
html_path.write_text(html,encoding='utf-8')
print('OVERVIEW_BRAND_PHOTOS_UPDATED',len(html),'bytes', 'opacity 0.22 -> 0.15', 'images: Fah Mai, Whisky Bull, Platinum Cask')
