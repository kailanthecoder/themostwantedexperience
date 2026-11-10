from pathlib import Path
import re

root=Path('proposals/fah-mai')
page=root/'index.html'
html=page.read_text(encoding='utf-8')
if 'id="fahmai-budget-investment-v8"' in html:
    print('BUDGET_V8_ALREADY_INSTALLED')
    raise SystemExit(0)
budget=(root/'budget_investment_v8.html').read_text(encoding='utf-8')
style=(root/'budget_investment_v8.css').read_text(encoding='utf-8')
assert '£5,750' in budget and '£400' in budget
assert '$11,500' in budget and '$800' in budget
assert '£10,550' in budget
assert budget.count('<table')==2

article_pat=r'<article\b[^>]*\bid="budget"[^>]*>[\s\S]*?</article>'
matched=re.search(article_pat,html)
assert matched, 'Budget A4 article not found'
article=matched.group(0)
body_start=re.search(r'<div class="sheet-body(?: [^"]*)?"[^>]*>',article)
footer_start=re.search(r'<footer class="sheet-footer">',article)
assert body_start and footer_start and body_start.start()<footer_start.start()
updated=article[:body_start.start()]+budget+'\n'+article[footer_start.start():]
assert 'class="sheet-body budgetv8-body"' in updated
assert 'id="invest"' not in updated and '$305' not in updated
html=html[:matched.start()]+updated+html[matched.end():]

# Remove the now-obsolete calculator event handlers so missing inputs do not
# throw exceptions and break the tab / PDF export.
old_calculator=r"\n const invest=document\.getElementById\('invest'\),margin=document\.getElementById\('margin'\),result=document\.getElementById\('breakeven'\);[\s\S]*?\n invest\.addEventListener\('input',calc\);margin\.addEventListener\('input',calc\);calc\(\);"
html,n=re.subn(old_calculator,'',html,count=1)
assert n==1, f'Obsolete ROI calculator JS was not removed: {n}'

assert '</head>' in html
html=html.replace('</head>','<style id="fahmai-budget-investment-v8">'+style+'</style>\n</head>',1)

assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',html))==12
assert '—' not in html,'Do not reintroduce prohibited long dashes'
page.write_text(html,encoding='utf-8')
print('BUDGET_V8_INSTALLED',len(html),'bytes, pages=12, calculator_removed=yes, standard_rates=$11,500+$800/month, partnership=GBP5750+GBP400/month')
