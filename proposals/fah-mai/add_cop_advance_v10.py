from pathlib import Path
import re

p=Path('proposals/fah-mai/index.html')
s=p.read_text(encoding='utf-8')
assert 'id="budget"' in s and 'id="implementation"' in s and 'id="implementation-evidence"' in s
assert 'id="fahmai-cop-advance-v10"' not in s
assert '—' not in s

def replace_once(old,new,label):
    global s
    count=s.count(old)
    assert count==1,f'{label}: expected exactly 1 occurrence, found {count}'
    s=s.replace(old,new,1)
    print('UPDATED',label)

# A short factual indication in Budget, with no changes to the agreed totals.
replace_once(
    '<div><span>01. Project commencement</span><strong>£2,750</strong><small>Due upfront to initiate development.</small></div>',
    '<div><span>01. Project commencement</span><strong>£2,750</strong><small>Any earlier $305 COP-billed advance is deducted from this payment.</small></div>',
    'Budget payment milestone'
)

# The fuller explanation belongs beside the delivery/payment process.
replace_once(
    '<div class="launch-payment-rule"><strong>Transparent payment structure.</strong> £2,750 at commencement plus £3,000 upon completed delivery equals £5,750 total development. Development tooling is included within this quotation; no separate AI membership advance is requested.</div>',
    '<div class="launch-payment-rule"><strong>Initial tooling advance: $305 USD equivalent, charged in Colombian pesos (COP).</strong> My AI account is linked to Colombia. I will pay the lowest suitable membership price; if it costs less, the unused balance will be credited against the total £5,750 development fee. The entire advance counts towards the £2,750 commencement milestone, never on top of it. The £3,000 balance is due on completed delivery.</div>',
    'Implementation advance and COP details'
)

replace_once(
    '<div class="launch-proof-intro"><b>Development resources are included within the quoted £5,750 fee.</b> The £2,750 commencement payment enables the agreed work. Software subscriptions are not presented as separate advance payments.</div>',
    '<div class="launch-proof-intro"><b>Development resources remain included in the £5,750 quotation.</b> An initial $305 USD-equivalent AI tooling advance, billed in COP because my account is linked to Colombia, is credited toward the £2,750 start payment. Any unspent amount also goes against the agreed project total, not an extra charge.</div>',
    'Evidence advance explanation'
)

replace_once(
    '<div class="launch-proof-takeaway"><strong>Two development payments:</strong> £2,750 at commencement and £3,000 on completed delivery. The ongoing £400/month service starts at launch or an agreed handover date.</div>',
    '<div class="launch-proof-takeaway"><strong>Two development milestones:</strong> £2,750 at commencement (less any prepaid $305 COP tooling advance) and £3,000 at delivery. The £400/month service starts at launch or agreed handover.</div>',
    'Evidence milestone reconciliation'
)

# The initial $305 is a prepaid part of the start milestone, not a third development charge.
# Currency FX is not guessed: conversion is based on actual payment evidence.
before='</head>'
css='''<style id="fahmai-cop-advance-v10">
#implementation .launch-payment-rule,
#implementation-evidence .launch-proof-intro {
  overflow-wrap:break-word!important;
}
</style>
'''
assert s.count(before)==1
s=s.replace(before,css+before,1)
assert s.count('id="fahmai-cop-advance-v10"')==1
assert s.count('$305')>=4
assert '—' not in s
assert len(re.findall(r'<article\b[^>]*\bclass="[^"]*\bsheet\b[^"]*"[^>]*>',s))==12
p.write_text(s,encoding='utf-8')
print('COP_ADVANCE_UPDATED',len(s),'bytes','A4 sheets 12','amount charged USD equivalent 305 in COP')
