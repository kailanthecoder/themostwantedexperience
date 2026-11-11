from pathlib import Path
import re,os

root=Path("proposals/fah-mai")
page=root/"index.html"
html=page.read_text(encoding="utf-8")
if 'id="fahmai-examples-readability-v15"' in html:
    print('EXAMPLES_V15_ALREADY_INSTALLED')
    raise SystemExit(0)
asset=root/"nwil-autoglass-preview-v15.webp"
assert asset.is_file() and asset.stat().st_size>12000,"Clean Autoglass screenshot must be captured first"
assert '<article' in html and 'id="examples"' in html and 'id="examples-client"' in html

# Replace the old inlined image containing the cookie dialog. Embed a real
# independently captured, cookie-free screenshot as a local asset.
article_match=re.search(r'<article\b[^>]*\bid="examples-client"[^>]*>[\s\S]*?</article>',html)
assert article_match,'Client examples A4 sheet not found'
article=article_match.group(0)
nwil=re.search(r'<a\b[^>]*href="https://nwilautoglass.com/"[^>]*>[\s\S]*?</a>',article)
assert nwil,'N W IL Auto Glass link not found'
old=nwil.group(0)
image_match=re.search(r'<img\b[^>]*class="example-screenshot"[^>]*>',old)
assert image_match,'N W IL image element missing'
tag=image_match.group(0)
assert 'data:image/webp;base64,' in tag,'Expected old embedded preview'
newtag=re.sub(r'\bsrc="[^"]+"','src="./nwil-autoglass-preview-v15.webp"',tag,count=1)
assert newtag!=tag
newtag=newtag.replace('loading="lazy"','loading="eager"')
newcard=old.replace(tag,newtag,1)
article=article.replace(old,newcard,1)
html=html[:article_match.start()]+article+html[article_match.end():]
print('FIXED_NWIL_PREVIEW','old src data-uri removed','local image asset',asset.stat().st_size)

# Provide a precise second-page continuation signal, not an extra full page,
# and keep a functional next-page action on the mobile continuous reader.
original='<div class="example-footer-note">Select any project to visit its website in a new tab.</div>'
assert html.count(original)==1,'Expected first Examples page note once'
cue='''<div class="example-footer-note">Select any project to visit its website in a new tab.</div>
<div class="examples-continue" aria-label="Continue to client project examples">
  <div class="examples-continue-text">
    <strong>More work to explore</strong>
    <small><span class="examples-continue-desktop">The client projects are on the facing page.</span><span class="examples-continue-mobile">Continue below for four client projects.</span></small>
  </div>
  <button class="examples-continue-action" data-continue-examples type="button" aria-label="Continue to client projects">
    <span class="examples-continue-desktop">See client work</span>
    <span class="examples-continue-mobile">Continue below</span>
    <span class="examples-continue-chevron" aria-hidden="true"></span>
  </button>
</div>'''
html=html.replace(original,cue,1)

css=(root/"examples_readability_v15.css").read_text(encoding="utf-8")
script='''(function(){
  const trigger=document.querySelector('#examples [data-continue-examples]');
  const target=document.getElementById('examples-client');
  const reader=document.querySelector('.viewport');
  if(!trigger||!target||!reader)return;
  trigger.addEventListener('click',()=>{
    target.scrollIntoView({
      behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',
      block:reader.dataset.readingMode==='vertical'?'start':'nearest',
      inline:'nearest'
    });
  });
})();'''
assert "</head>" in html and "</body>" in html
html=html.replace("</head>",'<style id="fahmai-examples-readability-v15">'+css+"</style>\n</head>",1)
html=html.replace("</body>",'<script id="fahmai-examples-continue-v15">'+script+"</script>\n</body>",1)

assert html.count('id="fahmai-examples-readability-v15"')==1
assert html.count('data-continue-examples')>=2
assert '—' not in html
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html))==12
page.write_text(html,encoding="utf-8")
print('EXAMPLES_V15_PUBLISHED_TO_WORKTREE',len(html),'bytes',12,'A4 pages')
