from pathlib import Path

p=Path('proposals/fah-mai/index.html')
html=p.read_text(encoding='utf-8')
marker='id="fahmai-overview-benefits-stages-refinement-2026"'
if marker in html:
    print('Overview refinement already installed')
    raise SystemExit(0)

assert '<div class="promise-grid">' in html
assert 'Unbeatable Design' in html
assert 'Competitive Pricing' in html
assert '<div class="stage-runway"' in html
assert html.count('We discuss the vision in person at your office or over Zoom.')==1

style=r"""
<style id="fahmai-overview-benefits-stages-refinement-2026">
/* Overview: intentionally position Unbeatable Design on benefit row two. */
@media screen, print {
  #overview .promise-grid .promise:nth-child(1){order:1!important}
  #overview .promise-grid .promise:nth-child(2){order:2!important}
  #overview .promise-grid .promise:nth-child(3){order:3!important}
  #overview .promise-grid .promise:nth-child(4){order:5!important}
  #overview .promise-grid .promise:nth-child(5){order:4!important}
  #overview .promise-grid .promise:nth-child(6){order:6!important}
  #overview .promise-grid .promise:nth-child(7){order:7!important}

  /* A quiet, connected three-step sequence; no loud multi-coloured boxes. */
  #overview .stage-runway {
    position:relative!important;
    display:grid!important;
    grid-template-columns:repeat(3,minmax(0,1fr))!important;
    gap:12px!important;
    width:100%!important;
    align-items:stretch!important;
    isolation:isolate!important;
  }
  #overview .stage-runway .stage-card {
    position:relative!important;
    display:grid!important;
    grid-template-columns:30px minmax(0,1fr)!important;
    column-gap:10px!important;
    align-items:start!important;
    box-sizing:border-box!important;
    min-height:84px!important;
    height:auto!important;
    margin:0!important;
    padding:15px 13px 12px!important;
    background:linear-gradient(150deg,#fff 0%,#fffbfd 100%)!important;
    border:1px solid #ecdbe5!important;
    border-radius:12px!important;
    box-shadow:0 3px 10px rgba(77,36,56,.035)!important;
    overflow:visible!important;
  }
  #overview .stage-runway .stage-card:nth-child(2),
  #overview .stage-runway .stage-card:nth-child(3) {
    background:linear-gradient(150deg,#fff 0%,#fffbfd 100%)!important;
    border-color:#ecdbe5!important;
  }
  /* A small top-edge line creates consistency without the generic full-frame glow. */
  #overview .stage-runway .stage-card::before {
    content:""!important;
    position:absolute!important;
    top:-1px!important;left:13px!important;right:13px!important;
    height:3px!important;
    background:linear-gradient(90deg,#e42982,#f7b1d1)!important;
    border-radius:0 0 4px 4px!important;
    opacity:.9!important;
    pointer-events:none!important;
  }
  /* The connector makes the next step unmistakable. */
  #overview .stage-runway .stage-card::after {
    content:"›"!important;
    position:absolute!important;
    top:50%!important;
    right:-13px!important;
    transform:translateY(-50%)!important;
    display:grid!important;place-items:center!important;
    width:14px!important;height:19px!important;
    border-radius:99px!important;
    background:#fff!important;
    color:#cc3882!important;
    font:800 22px/1 'Figtree',Arial,sans-serif!important;
    z-index:2!important;
    pointer-events:none!important;
  }
  #overview .stage-runway .stage-card:last-child::after{content:none!important;display:none!important}
  #overview .stage-runway .stage-no {
    display:grid!important;
    place-items:center!important;
    flex:0 0 30px!important;
    width:30px!important;height:30px!important;
    margin:0!important;
    padding:0!important;
    border:1px solid #f3cade!important;
    border-radius:50%!important;
    background:#fdeaf3!important;
    color:#b5216b!important;
    box-shadow:none!important;
    font:800 11px/1 'Poppins','Figtree',Arial,sans-serif!important;
    letter-spacing:-.15px!important;
  }
  #overview .stage-runway .stage-card p {
    display:block!important;
    margin:1px 0 0!important;
    padding:0!important;
    color:#43333e!important;
    font:700 10.5px/1.43 'Figtree',Arial,sans-serif!important;
    letter-spacing:-.08px!important;
    text-align:left!important;
    overflow-wrap:break-word!important;
  }
}
@media print{
  #overview .stage-runway .stage-card {box-shadow:none!important}
}
</style>
"""
html=html.replace('</head>',style+'</head>',1)
p.write_text(html,encoding='utf-8')
print('Applied benefits row and stage-card improvements',len(html),'bytes')
