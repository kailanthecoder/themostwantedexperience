from pathlib import Path
import re
root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
script=(root/'storybook_spreads_v4.js').read_text(encoding='utf-8')
pattern=r'(<script id="fahmai-document-zoom-script">)[\s\S]*?(</script>)'
m=re.search(pattern,html)
assert m, 'Embedded storybook controller not found'
assert 'const spreadStart = i => i === 0 ? 0' in m.group(0), 'Expected prior grouping rule not found'
assert 'id="examples-client"' in html and 'id="examples"' in html and 'id="proposed"' in html
html,n=re.subn(pattern,lambda match:match.group(1)+script+match.group(2),html,count=1)
assert n==1
assert html.count('const spreadGroups = (() => {')==1
page.write_text(html,encoding='utf-8')
print('APPLIED_EXAMPLES_SPREAD_FIX',len(html),'bytes; document content and style unchanged')
