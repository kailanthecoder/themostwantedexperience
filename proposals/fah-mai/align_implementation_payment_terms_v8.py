from pathlib import Path
import re

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
if 'id="fahmai-implementation-payment-alignment-v8"' in html:
    print('IMPLEMENTATION_V8_ALREADY_ALIGNED')
    raise SystemExit(0)

parts={
    'implementation':'implementation_terms_aligned_v8.html',
    'implementation-evidence':'implementation_evidence_aligned_v8.html'
}
for sheet_id,file in parts.items():
    content=(root/file).read_text(encoding='utf-8')
    article_pat=r'<article\b[^>]*\bid="'+re.escape(sheet_id)+r'"[^>]*>[\s\S]*?</article>'
    match=re.search(article_pat,html)
    assert match,'Expected Implementation sheet missing '+sheet_id
    article=match.group(0)
    body_start=re.search(r'<div class="sheet-body\b[^"]*"[^>]*>',article)
    footer_start=re.search(r'<footer class="sheet-footer">',article)
    assert body_start and footer_start and footer_start.start()>body_start.start()
    replacement=article[:body_start.start()]+content+'\n'+article[footer_start.start():]
    html=html[:match.start()]+replacement+html[match.end():]
    print('ALIGNED',sheet_id,'body_bytes',len(content))
css=(root/'implementation_evidence_aligned_v8.css').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="fahmai-implementation-payment-alignment-v8">'+css+'</style>\n</head>',1)
assert '$305' not in html,'Old advance still present outside the aligned sheets'
assert '—' not in html,'Do not reintroduce em dashes'
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html))==12
page.write_text(html,encoding='utf-8')
print('IMPLEMENTATION_PAYMENT_ALIGNMENT_COMPLETE',len(html))
