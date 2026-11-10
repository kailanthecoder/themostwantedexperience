from pathlib import Path
import re
p=Path("proposals/fah-mai/index.html")
s=p.read_text(encoding="utf-8")
assert 'id="fahmai-cop-advance-v10"' in s
assert '—' not in s
changes=[
("Any earlier $305 COP-billed advance is deducted from this payment.",
 "Any earlier 999,999 COP tooling advance (approximately $305 USD) is credited toward this payment."),
("Initial tooling advance: $305 USD equivalent, charged in Colombian pesos (COP).",
 "Initial tooling advance: 999,999 COP (approximately $305 USD)."),
("An initial $305 USD-equivalent AI tooling advance, billed in COP because my account is linked to Colombia, is credited toward the £2,750 start payment.",
 "An initial AI tooling advance of 999,999 COP (approximately $305 USD), billed in Colombian pesos because my account is linked to Colombia, is credited toward the £2,750 start payment."),
("£2,750 at commencement (less any prepaid $305 COP tooling advance) and £3,000 at delivery.",
 "£2,750 at commencement (less any prepaid tooling advance of 999,999 COP, approximately $305 USD) and £3,000 at delivery.")
]
for old,new in changes:
    n=s.count(old)
    assert n==1, f"Expected exactly one instance of {old!r}, found {n}"
    s=s.replace(old,new,1)
    print("FIXED",old,"TO",new)
assert "less any prepaid $305 COP tooling advance" not in s
assert "$305 COP" not in s
assert s.count("999,999 COP")>=4
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',s))==12
p.write_text(s,encoding="utf-8")
print("PRICE_CURRENCY_CLARIFIED",s.count("999,999 COP"),"instances; 12 pages")
