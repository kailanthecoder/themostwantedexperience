from pathlib import Path
import re

path=Path('proposals/fah-mai/index.html')
html=path.read_text(encoding='utf-8')
assert 'id="design"' in html and 'id="tab-design"' in html, 'The live Design page/tab is already missing'
assert html.count('These live websites may have been updated since my involvement. Select a card to open the current site.')==1
assert html.count('—')==11, 'Em dash count changed, inspect before modifying'
old_count=len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html))
assert old_count==13, f'Expected 13 sheets, found {old_count}'

# Remove the complete Design sheet, its menu tab, and its now-unreferenced
# site-specific CSS. Other references to website *design* remain untouched.
for pattern,what in [
    (r'\s*<article\b[^>]*\bid="design"[^>]*>[\s\S]*?</article>','Design A4 sheet'),
    (r'\s*<button\b[^>]*\bid="tab-design"[^>]*>[\s\S]*?</button>','Design navigation tab'),
    (r'\s*<style\b[^>]*\bid="fahmai-design-concepts-page-v1"[^>]*>[\s\S]*?</style>','Unused Design sheet stylesheet'),
]:
    html,n=re.subn(pattern,'',html,count=1)
    assert n==1, f'Missing {what}'
    print('REMOVED',what)

# Delete the entire Examples disclosure line, not just its text.
disclosure=r'<div class="example-footer-note">\s*These live websites may have been updated since my involvement\. Select a card to open the current site\.\s*</div>'
html,n=re.subn(disclosure,'',html,count=1)
assert n==1, 'Examples sentence is no longer in the expected element'
print('REMOVED Examples disclosure')

# Preserve section cohesion after the Design page disappears: cover alone;
# Current and Spec pages grouped by logical sequence; Budget alone,
# Implementation paired, Proposed alone; two Examples pages together.
anchor='''      } else if (sheets[i].id === "current-growth") {
        groups.push([i]);
        i += 1;
      } else if (sheets[i].id === "examples"'''
replacement='''      } else if (sheets[i].id === "current-growth" || sheets[i].id === "budget" || sheets[i].id === "proposed") {
        groups.push([i]);
        i += 1;
      } else if (sheets[i].id === "examples"'''
assert html.count(anchor)==1,'Cannot locate current spread grouping'
html=html.replace(anchor,replacement,1)

# Replace standalone em-dash calculator placeholders with a readable value.
html=html.replace('<strong id="breakeven">—</strong>','<strong id="breakeven">N/A</strong>')
html=html.replace("'—'","'N/A'")

# Remove every remaining em dash from copy / metadata, preserving readable
# punctuation rather than leaving sentences joined incorrectly.
html=html.replace(' — ', ', ')
html=html.replace('—', ', ')
assert '—' not in html, 'Found remaining em dash'

pages=re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html)
assert len(pages)==12, f'Expected 12 pages after Design removal, got {len(pages)}'
assert 'id="design"' not in html
assert 'id="tab-design"' not in html
assert 'These live websites may have been updated since my involvement.' not in html

path.write_text(html,encoding='utf-8')
print('CLEANUP_COMPLETE','pages',len(pages),'bytes',len(html),'em-dashes',html.count('—'),'disclaimer',False)
