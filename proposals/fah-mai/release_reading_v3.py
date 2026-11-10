from pathlib import Path
from base64 import b64encode
import re,os

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
assert 'id="fahmai-document-zoom-script"' in html, 'Reader controller not found'
assert '<div class="viewport">' in html or 'class="viewport"' in html, 'A4 viewport not found'
assert 'id="fahmai-reading-flow-v3"' not in html, 'Already installed'

style=(root/'reading_flow_v3.css').read_text(encoding='utf-8')
script=(root/'storybook_reading_v3.js').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="fahmai-reading-flow-v3">'+style+'</style></head>',1)
html, replaced=re.subn(
    r'<script id="fahmai-document-zoom-script">[\s\S]*?</script>',
    lambda m:'<script id="fahmai-document-zoom-script">'+script+'</script>',
    html, count=1
)
assert replaced==1,'Storybook script replacement missing'

shot=Path('/tmp/fahmai_nwil_original.webp')
assert shot.is_file() and shot.stat().st_size>3000, 'Live NW IL Auto Glass capture not available'
bytes=shot.read_bytes()
assert bytes[:4]==b'RIFF' and b'WEBP' in bytes[:16], 'Not a valid WebP screenshot'
live_image='data:image/webp;base64,'+b64encode(bytes).decode('ascii')
old='https://image.thum.io/get/noanimate/width/720/crop/580/https://nwilautoglass.com/'
assert html.count(old)==1, 'Expected one NW IL Auto Glass outdated thumbnail'
html=html.replace(old,live_image,1)
# The real screenshot is embedded in the proposal itself, avoiding CORS/thumbnail failures.
card_flag='href="https://nwilautoglass.com/"'
assert html.count(card_flag)==1, 'NW IL example card missing'
html=html.replace(card_flag,card_flag+' data-preview-source="official-live-screenshot"',1)
page.write_text(html,encoding='utf-8')
print('RELEASE_PREPARED',len(html),'webp_bytes',len(bytes),'page_count',html.count('class="sheet'),
      'reader_version','v3','banner_data_embedded',live_image in html)
