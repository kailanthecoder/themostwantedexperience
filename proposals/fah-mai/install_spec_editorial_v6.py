from pathlib import Path
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
import re,requests

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
if 'id="fahmai-spec-editorial-v6"' in html:
    print('SPEC_V6_ALREADY_INSTALLED')
    raise SystemExit(0)

assert re.search(r'<article\\b[^>]*\\bid="spec"[^>]*>',html), 'Spec article missing'
assert 'id="spec-delivery"' not in html
assert 'const spreadGroups = (() => {' in html, 'Updated storybook spread grouper missing'

scope=(root/'spec_brand_scope_v6.html').read_text(encoding='utf-8')
technical=(root/'spec_technical_v6.html').read_text(encoding='utf-8')
assert 'Spec' not in scope[:50] or 'specv6' in scope

brands={
    'react':'61DAFB',
    'nextdotjs':'000000',
    'typescript':'3178C6',
    'nodedotjs':'339933',
    'python':'3776AB',
    'postgresql':'4169E1'
}
session=requests.Session()
def icon(item):
    slug,color=item
    urls=[
        f'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{slug}.svg',
        f'https://cdn.jsdelivr.net/npm/simple-icons@v16/icons/{slug}.svg'
    ]
    last=None
    for url in urls:
        try:
            r=session.get(url,timeout=19)
            r.raise_for_status()
            svg=r.text
            assert '<svg' in svg and '<path' in svg and '</svg>' in svg, f'Invalid SVG from {url}'
            svg=svg.replace('<svg ',f'<svg fill="#{color}" ',1)
            payload=b64encode(svg.encode('utf-8')).decode('ascii')
            print('BRAND_LOGO',slug,len(svg),'source',url)
            return slug,'data:image/svg+xml;base64,'+payload
        except Exception as error:
            last=error
    raise RuntimeError(f'Missing official-style technology icon {slug}: {last}')

with ThreadPoolExecutor(max_workers=6) as pool:
    results=dict(pool.map(icon,brands.items()))
for slug,uri in results.items():
    placeholder='__TECH_'+slug.upper()+'__'
    assert technical.count(placeholder)==1,placeholder
    technical=technical.replace(placeholder,uri)
assert '__TECH_' not in technical

pattern=r'<article\b[^>]*\bid="spec"[^>]*>[\s\S]*?</article>'
match=re.search(pattern,html)
assert match, 'Spec article missing'
old_article=match.group(0)
body_start=re.search(r'<div class="sheet-body(?:\s+[^"]*)?"[^>]*>',old_article)
footer_start=re.search(r'<footer class="sheet-footer">',old_article)
assert body_start and footer_start and footer_start.start()>body_start.end(),'Spec body/footer not found'
prefix=old_article[:body_start.start()]
suffix=old_article[footer_start.start():]
spec_article=prefix+scope+'\n'+suffix
detail_prefix=prefix.replace('aria-labelledby="tab-spec"','aria-label="Spec: technical delivery"').replace('id="spec"','id="spec-delivery"').replace('role="tabpanel"','role="region"')
assert detail_prefix!=prefix and 'id="spec-delivery"' in detail_prefix
detail_prefix=detail_prefix.replace('class="sheet"','class="sheet specv6-detail" data-proposal-section="spec"')
tech_article=detail_prefix+technical+'\n'+suffix
html=html[:match.start()]+spec_article+'\n'+tech_article+html[match.end():]

# The cover remains single; Current's final page stands alone so the two
# Spec sheets face each other. Preserve later Design/Budget, Implementation
# and Examples spreads, with Proposed still by itself before Examples.
needle='''      } else if (sheets[i].id === "examples" && sheets[i + 1]?.id === "examples-client") {'''
assert html.count(needle)==1, 'Cannot locate explicit Examples spread rule'
replacement='''      } else if (sheets[i].id === "current-growth") {
        groups.push([i]);
        i += 1;
      } else if (sheets[i].id === "examples" && sheets[i + 1]?.id === "examples-client") {'''
html=html.replace(needle,replacement,1)
assert html.count('current-growth") {')>=1

style=(root/'spec_editorial_v6.css').read_text(encoding='utf-8')
assert '</head>' in html
html=html.replace('</head>','<style id="fahmai-spec-editorial-v6">'+style+'</style>\n</head>',1)

# These pieces are decorative and add no information. Remove the literal
# phrase too, rather than just letting its CSS hide it.
html=html.replace('VISUAL DIRECTIONS / EXPLORATORY CONCEPTS','',1)
assert 'id="spec-delivery"' in html
assert html.index('id="spec"')<html.index('id="spec-delivery"')<html.index('id="design"')
assert len(re.findall(r'<article\b[^>]*class="[^"]*\bsheet\b',html))==13

page.write_text(html,encoding='utf-8')
print('SPEC_V6_READY',len(html),'bytes',13,'pages','two Spec sheets',True,'logo_count',len(results))
