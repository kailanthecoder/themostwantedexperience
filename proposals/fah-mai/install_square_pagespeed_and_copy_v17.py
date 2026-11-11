from pathlib import Path
import re
from bs4 import BeautifulSoup
from PIL import Image

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
if 'id="fahmai-pagespeed-square-v17"' in html:
    print('GALLERY_V17_ALREADY_INSTALLED')
    raise SystemExit(0)
assert '—' not in html

# Produce five individually-addressable exact image slices from the original
# historical 11 November PageSpeed evidence. Use PNG without re-compression.
atlas=root/'pagespeed-evidence-v11.avif'
original=Image.open(atlas).convert('RGB')
assert original.size==(2300,320),f'Unexpected original report atlas size: {original.size}'
files=[
 'pagespeed-fmh-mobile-v17.png',
 'pagespeed-fmh-desktop-v17.png',
 'pagespeed-whiskybull-desktop-v17.png',
 'pagespeed-platinum-mobile-v17.png',
 'pagespeed-platinum-desktop-v17.png'
]
for i,name in enumerate(files):
    tile=original.crop((i*460,0,(i+1)*460,320))
    assert tile.size==(460,320)
    dest=root/name
    tile.save(dest,format='PNG',optimize=True)
    print('CREATED_REPORT_IMAGE',name,dest.stat().st_size,'pixels',tile.size)

# Replace only Current's PageSpeed gallery. Other reports and all A4 pages
# are untouched, as are the PDF-only historical mobile evidence images.
replacement=(root/'pagespeed_square_gallery_v17.html').read_text(encoding='utf-8')
pattern=r'<section\b[^>]*class="ps-evidence"[^>]*>[\s\S]*?</section>'
match=re.search(pattern,html)
assert match,'Legacy PageSpeed gallery not found'
assert 'ps-report-image' in match.group(0)
assert 'ps-print-evidence' in match.group(0)
html=html[:match.start()]+replacement+html[match.end():]

# Remove obsolete PageSpeed JS with its references to the deleted report dots.
old_script=r'<script id="fahmai-pagespeed-carousel-v11">[\s\S]*?</script>'
script=(root/'pagespeed_square_gallery_v17.js').read_text(encoding='utf-8')
assert len(re.findall(old_script,html))==1,'Expected exactly one old PageSpeed interaction script'
html=re.sub(old_script,'<script id="fahmai-pagespeed-square-v17">'+script+'</script>',html,count=1)
css=(root/'pagespeed_square_gallery_v17.css').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="fahmai-pagespeed-square-style-v17">'+css+'</style>\n</head>',1)

# Use Kailan explicitly for his individual professional work. Refer to both
# Kailan and Louis by name for moments where the proposal refers to both.
changes=[
 ('We discuss the vision in person at your office or over Zoom.',
  'Kailan and Louis discuss the vision in person at the office or over Zoom.',1),
 ('We confirm Phase 1, including funding for AI development credits.',
  'Kailan and Louis confirm Phase 1, including funding for AI development credits.',1),
 ('Ask us for past-work case studies.',
  'Ask Kailan for past-work case studies.',1),
 ('How we get there',
  'Kailan’s approach',1),
 ('Co-designed by me',
  'Co-designed by Kailan',2)
]
for old,new,expected in changes:
    n=html.count(old)
    assert n==expected,f'Unexpected count for {old!r}: {n}, expected {expected}'
    html=html.replace(old,new)
    print('COPY_REVISED',old,'->',new,'instances',n)

parsed=BeautifulSoup(html,'html.parser')
pronouns=re.compile(r"\b(?:we|we're|we've|we'll|we'd|our|ours|us|ourselves)\b",re.I)
for section in parsed.select('.viewport>.sheet'):
    body=section.select_one('.sheet-body')
    if body:
        remaining=[word for word in pronouns.findall(body.get_text(' ',strip=True)) if word != 'US']
        assert not remaining, f'First-person plural copy remains on {section.get("id")}: {remaining}'
assert len(parsed.select('.viewport>.sheet'))==12
assert not parsed.select('#current .ps-source-toggle')
assert not parsed.select('#current .audit-v5-carousel')
assert len(parsed.select('#current .ps-v17-thumb'))==5
assert len(parsed.select('#current .ps-v17-square'))==1
assert len(parsed.select('#current .ps-print-evidence figure'))==2
assert '—' not in html
page.write_text(html,encoding='utf-8')
print('GALLERY_V17_INSTALLED','HTML_BYTES',len(html),'CHAPTERS',12,'THUMBNAILS',5,'FIRST_PERSON_PLURAL',0)
