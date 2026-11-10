from pathlib import Path
from bs4 import BeautifulSoup
import re

root=Path('proposals/fah-mai')
path=root/'index.html'
text=path.read_text(encoding='utf-8')
assert 'id="design"' not in text,'Design section already exists'
assert 'id="tab-design"' not in text,'Design tab already exists'
assert len(re.findall(r'<article\b[^>]*class="sheet',text))>=5

match=re.search(r'<article\b[^>]*\bid="spec"[^>]*>[\s\S]*?</article>',text)
assert match,'Cannot locate exact Spec sheet'
spec=BeautifulSoup(match.group(0),'html.parser').find('article')
assert spec is not None
spec['id']='design'
spec['aria-labelledby']='tab-design'
spec['role']='tabpanel'
body=spec.select_one('.sheet-body')
assert body is not None
markup=(root/'design_concepts_page.html').read_text(encoding='utf-8')
concept=BeautifulSoup(markup,'html.parser').select_one('.design-concepts')
assert concept and len(concept.select('.design-concept-card'))==3
body.clear()
body.append(concept)
new_article=str(spec)
assert 'id="design"' in new_article
text=text[:match.end()]+'\n'+new_article+'\n'+text[match.end():]
tab_match=re.search(r'<button\b[^>]*\bid="tab-spec"[^>]*>[\s\S]*?</button>',text)
assert tab_match,'Cannot locate Spec navigation tab'
design_tab=(tab_match.group(0)
    .replace('id="tab-spec"','id="tab-design"',1)
    .replace('data-target="spec"','data-target="design"',1)
    .replace('aria-controls="spec"','aria-controls="design"',1)
    .replace('>Spec</button>','>Design</button>',1))
assert 'id="tab-design"' in design_tab
assert '>Design</button>' in design_tab
text=text[:tab_match.end()]+'\n'+design_tab+text[tab_match.end():]
style=(root/'design_concepts_page.css').read_text(encoding='utf-8')
assert '</head>' in text
text=text.replace('</head>','<style id="fahmai-design-concepts-page-v1">'+style+'</style>\n</head>',1)
path.write_text(text,encoding='utf-8')
print('NEW_DESIGN_PAGE_INSTALLED',len(text),'bytes',
      'position_after_spec',text.index('id="spec"')<text.index('id="design"')<text.index('id="budget"'),
      'nav_position',text.index('id="tab-spec"')<text.index('id="tab-design"')<text.index('id="tab-budget"'),
      'mockups',len(concept.select('.design-concept-card')))
