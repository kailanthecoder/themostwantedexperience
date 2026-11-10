from pathlib import Path
import re
root=Path('proposals/fah-mai')
p=root/'index.html'
s=p.read_text(encoding='utf-8')
if 'id="fahmai-storybook-style-2026"' in s:
    print('Already installed')
    raise SystemExit(0)
css=(root/'storybook_2026.css').read_text()
js=(root/'storybook_2026.js').read_text()
assert '</head>' in s and '</body>' in s
assert '<div class="fm-zoom" role="group" aria-label="Proposal page zoom">' in s
assert '<script id="fahmai-document-zoom-script">' in s
s=s.replace('</head>','<style id="fahmai-storybook-style-2026">'+css+'</style></head>',1)
needle='<div class="fm-zoom" role="group" aria-label="Proposal page zoom">'
addition='''<button type="button" class="fm-story-prev" aria-label="Previous page" title="Previous page">‹</button>
  <output class="fm-story-counter" aria-live="polite" aria-label="Current pages">1–2 / 11</output>
  <button type="button" class="fm-story-next" aria-label="Next page" title="Next page">›</button>
  <span class="fm-story-separator" aria-hidden="true"></span>'''
s=s.replace(needle,needle+addition,1)
s,n=re.subn(r'<script id="fahmai-document-zoom-script">[\s\S]*?</script>',
            lambda m:'<script id="fahmai-document-zoom-script">'+js+'</script>',
            s,count=1)
assert n==1
p.write_text(s,encoding='utf-8')
print('Installed storybook; bytes',p.stat().st_size,'sheet count',len(re.findall(r'<article class="sheet',s)),'JS bytes',len(js))
