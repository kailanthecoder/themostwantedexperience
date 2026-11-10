from pathlib import Path
p=Path('proposals/fah-mai/index.html')
s=p.read_text()
assert len(s)>1_000_000 and 'id="glass-navigation-final-v9"' in s
assert 'id="glass-nav-contrast-v10"' not in s
css=r'''
<style id="glass-nav-contrast-v10">
@media screen {
 .tabs #tab-proposed,
 .tabs #tab-proposed[aria-selected="false"]{
  opacity:1!important;filter:none!important;visibility:visible!important;
  color:#fff!important;-webkit-text-fill-color:#fff!important;
  background:linear-gradient(110deg,#a6125e 0%,#d82e7e 100%)!important;
  border:1.5px solid #8e1551!important;
  font-family:'Poppins','Figtree',Arial,sans-serif!important;
  font-weight:900!important;font-size:14px!important;
  text-shadow:0 1px 2px rgba(54,2,31,.08)!important;
  box-shadow:0 5px 14px rgba(157,23,84,.2),inset 0 1px 0 rgba(255,255,255,.23)!important;
 }
 .tabs #tab-proposed[aria-selected="true"]{
  color:#fff!important;-webkit-text-fill-color:#fff!important;
  opacity:1!important;
  background:linear-gradient(115deg,#761144,#b81868)!important;
  border:2px solid #761144!important;
  box-shadow:0 5px 18px rgba(117,17,68,.3)!important;
 }
}
@media screen and (max-width:590px){
 .tabs{width:100%!important;display:flex!important;flex-wrap:wrap!important;
  justify-content:center!important;align-content:center!important;
  overflow-x:visible!important;overflow-y:visible!important;
  gap:7px 6px!important;padding:3px 0!important}
 .tabs .tab{font-size:12.1px!important;font-weight:800!important;
  height:41px!important;min-height:41px!important;padding:0 10.5px!important;
  line-height:1.1!important;flex:0 0 auto!important}
 .tabs #tab-proposed{font-size:12.7px!important;font-weight:900!important;
  margin-left:14px!important;padding:0 11px!important}
 .tabs #tab-proposed:before{left:-10px!important;top:8px!important;height:25px!important}
 .toolbar-inner{gap:7px 10px!important}
}
@media screen and (max-width:365px){
 .tabs{gap:5px 4px!important}
 .tabs .tab{font-size:11px!important;padding:0 8px!important;height:39px!important;min-height:39px!important}
 .tabs #tab-proposed{font-size:11.3px!important;margin-left:9px!important;padding:0 9px!important}
}
</style>
'''
s=s.replace('</head>',css+'</head>',1)
p.write_text(s)
print('Contrast and mobile two-row navigation applied',len(s),flush=True)
