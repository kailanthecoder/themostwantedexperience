from pathlib import Path
import re,html

path=Path('proposals/fah-mai/index.html')
source=path.read_text(encoding='utf-8')
marker='id="fahmai-chapter-boundaries-v14"'
assert marker not in source,'Chapter boundaries already installed'
assert '—' not in source
chapter_order=['overview','current','spec','budget','implementation','proposed','examples']
chapter_names={
 'overview':'Overview',
 'current':'Current',
 'spec':'Spec',
 'budget':'Budget',
 'implementation':'Implementation',
 'proposed':'Proposed',
 'examples':'Examples'
}
expected_pages={
 'overview':['overview'],
 'current':['current','current-journeys','current-growth'],
 'spec':['spec','spec-delivery'],
 'budget':['budget'],
 'implementation':['implementation','implementation-evidence'],
 'proposed':['proposed'],
 'examples':['examples','examples-client']
}
ids={id for pages in expected_pages.values() for id in pages}
pattern=r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>[\s\S]*?</article>'
pages=list(re.finditer(pattern,source))
assert len(pages)==12,f'Expected 12 pages, found {len(pages)}'
seen=[]
sections=[]
def revise(match):
    old=match.group(0)
    opening=re.match(r'<article\b[^>]*>',old)
    assert opening,'Missing opening article'
    page_id=re.search(r'\bid="([^"]+)"',opening.group(0)).group(1)
    assert page_id in ids,page_id
    chapter=next(k for k,p in expected_pages.items() if page_id in p)
    section_number=chapter_order.index(chapter)+1
    section_page=expected_pages[chapter].index(page_id)+1
    total=len(expected_pages[chapter])
    start=section_page==1
    seen.append(page_id)
    heading=chapter_names[chapter]
    badge=(f'<div class="chapter-banner" role="note" aria-label="Section {section_number} of 7, {heading}, page {section_page} of {total}">'
      f'<span class="chapter-banner-index">{section_number:02d}</span>'
      f'<strong class="chapter-banner-name">{html.escape(heading)}</strong>'
      f'<span class="chapter-banner-count">{section_page} of {total}</span></div>')
    footer=(f'<div class="chapter-footer-label" aria-hidden="true">'
      f'<strong>{html.escape(heading)}</strong><span>Section {section_number} of 7</span>'
      f'<span class="chapter-footer-page">{section_page}/{total}</span></div>')
    opener=opening.group(0)[:-1]+f' data-chapter="{chapter}" data-chapter-start="{"true" if start else "false"}" data-chapter-page="{section_page}">'
    revised=opener+old[opening.end():]
    body=re.search(r'<div class="sheet-body\b[^"]*"[^>]*>',revised)
    assert body,f'Missing body on {page_id}'
    revised=revised[:body.start()]+badge+revised[body.start():]
    revised,footercount=re.subn(r'(</footer>)',footer+r'\1',revised,count=1)
    assert footercount==1,f'No footer on {page_id}'
    if start and chapter!='overview':
        divider=(f'<div class="chapter-divider" data-chapter-divider="{chapter}" role="separator" aria-label="Start of section {section_number}, {heading}">'
        f'<span class="chapter-divider-index">{section_number:02d}</span><strong>{html.escape(heading)}</strong>'
        f'<span class="chapter-divider-line" aria-hidden="true"></span></div>\n')
        revised=divider+revised
    sections.append((page_id,chapter,section_page,total))
    return revised

out=re.sub(pattern,revise,source)
assert seen==[p for k in chapter_order for p in expected_pages[k]],f'Unexpected page sequence: {seen}'
assert out.count('class="chapter-banner"')==12
assert out.count('class="chapter-divider"')==6
assert out.count('class="chapter-footer-label"')==12
css=Path('proposals/fah-mai/chapter_boundaries_v14.css').read_text(encoding='utf-8')
js=Path('proposals/fah-mai/chapter_boundaries_v14.js').read_text(encoding='utf-8')
assert '</head>' in out and '</body>' in out
out=out.replace('</head>','<style id="fahmai-chapter-boundaries-v14">'+css+'</style>\n</head>',1)
out=out.replace('</body>','<script id="fahmai-chapter-track-v14">'+js+'</script>\n</body>',1)
assert '—' not in out
assert len(re.findall(pattern,out))==12
path.write_text(out,encoding='utf-8')
print('CHAPTER_BOUNDARIES_INSTALLED',len(out),'bytes',len(pages),'A4 pages',len(sections),'chapter labels',6,'chapter transitions')
print('PAGE_CHAPTERS',sections)
