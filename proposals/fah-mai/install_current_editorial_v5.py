from pathlib import Path
from base64 import b64encode
import re

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
assert 'id="fahmai-current-editorial-v5"' not in html, 'Already installed'
files={
    'current':'current_visual_v5.html',
    'current-journeys':'current_brand_opportunities_v5.html',
    'current-growth':'current_commercial_v5.html'
}
new=root.joinpath(files['current']).read_text(encoding='utf-8')
for brand in ('fmh','bull','cask'):
    filename=Path('/tmp/fahmai_current_capture_'+brand+'.webp')
    assert filename.is_file() and filename.stat().st_size>3000, f'Missing live screenshot {filename}'
    b=filename.read_bytes()
    assert b[:4]==b'RIFF' and b'WEBP' in b[:16],f'Not WebP: {filename}'
    uri='data:image/webp;base64,'+b64encode(b).decode('ascii')
    old='__CURRENT_SHOT_'+brand.upper()+'__'
    assert old in new
    new=new.replace(old,uri,1)
    print('SITE_CAPTURE',brand,len(b))
assert '__CURRENT_SHOT_' not in new

for id,filename in files.items():
    content=new if id=='current' else root.joinpath(filename).read_text(encoding='utf-8')
    pattern=r'<article\b[^>]*\bid="'+re.escape(id)+r'"[^>]*>[\s\S]*?</article>'
    m=re.search(pattern,html)
    assert m, f'Missing article {id}'
    original=m.group(0)
    begin=re.search(r'<div class="sheet-body\b[^"]*"[^>]*>',original)
    footer=re.search(r'<footer class="sheet-footer">',original)
    assert begin and footer and footer.start()>begin.start(),id
    updated=original[:begin.start()]+content+'\n'+original[footer.start():]
    assert updated.count('<footer class="sheet-footer">')==1
    html=html[:m.start()]+updated+html[m.end():]
    print('REBUILT_PAGE',id,'old_text_length',len(re.sub('<[^>]+>',' ',original)),'new_body_chars',len(content))

# Strip thin decorative arrows from copy on all proposal pages. Buttons outside the
# sheets remain unchanged, so storybook back/next affordances still function.
def strip_copy_arrows(m):
    return m.group(0).replace('↗','').replace('→','').replace('➜','').replace('⇢','')
html,count=re.subn(r'<article\b[^>]*class="[^"]*\bsheet\b[^"]*"[^>]*>[\s\S]*?</article>',strip_copy_arrows,html)
assert count==12,f'Expected 12 A4 sheets, found {count}'
style=root.joinpath('current_editorial_v5.css').read_text(encoding='utf-8')
js=root.joinpath('current_carousel_v5.js').read_text(encoding='utf-8')
assert '</head>' in html and '</body>' in html
html=html.replace('</head>','<style id="fahmai-current-editorial-v5">'+style+'</style>\n</head>',1)
html=html.replace('</body>','<script id="fahmai-current-carousel-v5">'+js+'</script>\n</body>',1)
page.write_text(html,encoding='utf-8')
print('EDITORIAL_V5_READY','html_bytes',len(html),'pages',count,'arrow_copy_removed',True)
