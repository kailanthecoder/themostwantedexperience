from pathlib import Path
p=Path("proposals/fah-mai/index.html")
s=p.read_text()
assert len(s)>1_000_000 and s.count('id="examples"')==1
marker='id="fahmai-side-by-side-presentation"'
assert marker not in s
style=r'''
<style id="fahmai-side-by-side-presentation">
/* Clear, visually centred presentation titles to the LEFT of each brand set. */
.presentation-header{height:122px!important;min-height:122px!important;padding:11px 26px 10px!important;grid-template-columns:minmax(0,1.24fr) minmax(0,1fr)!important;column-gap:12px!important}
.presentation-header .presented-group{min-height:100px!important;display:flex!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:9px!important}
.presentation-header .presented-to{padding-right:12px!important}
.presentation-header .presented-by{padding-left:1px!important}
.presentation-header .presented-copy{display:block!important;flex:0 0 132px!important;width:132px!important;min-width:0!important;text-align:left!important;margin:0!important;font-family:'Poppins','Figtree',Arial,sans-serif!important;font-size:16.2px!important;font-weight:800!important;line-height:1.16!important;letter-spacing:-.75px!important}
.presentation-header .presented-by .presented-copy{flex-basis:145px!important;width:145px!important}
.presentation-header .client-lockups{flex:1 1 auto!important;width:auto!important;min-width:0!important;justify-content:space-evenly!important;gap:6px!important;margin:0!important}
.presentation-header .brand-fmh{width:51px!important}.presentation-header .brand-fmh img{width:49px!important;height:49px!important;max-width:49px!important;max-height:49px!important}
.presentation-header .brand-bull{width:52px!important}.presentation-header .brand-bull img{width:49px!important;height:54px!important;max-width:49px!important;max-height:54px!important}
.presentation-header .brand-pc{width:126px!important}.presentation-header .brand-pc img{width:124px!important;height:50px!important;max-width:124px!important;max-height:50px!important}
.presentation-header .presenter-lockups{flex:1 1 auto!important;width:auto!important;min-width:0!important;gap:11px!important;align-items:center!important;justify-content:center!important}
.presentation-header .mw-black{width:58px!important;min-width:58px!important;max-width:58px!important}
.presentation-header .mw-black img{width:54px!important;height:54px!important;max-height:54px!important;max-width:54px!important;filter:brightness(0)!important}
.presentation-header .signature-logo{width:69px!important;height:40px!important;max-width:69px!important;max-height:40px!important}
@media(max-width:650px){
 .presentation-header{height:111px!important;min-height:111px!important;padding:6px 12px!important;gap:5px!important}
 .presentation-header .presented-group{gap:3px!important;min-height:94px!important}
 .presentation-header .presented-to{padding-right:4px!important}
 .presentation-header .presented-copy{font-size:10px!important;line-height:1.2!important;letter-spacing:-.2px!important;flex:0 0 75px!important;width:75px!important}
 .presentation-header .presented-by .presented-copy{flex:0 0 79px!important;width:79px!important}
 .presentation-header .client-lockups{gap:2px!important}
 .presentation-header .brand-fmh{width:31px!important}.presentation-header .brand-fmh img{width:30px!important;height:30px!important}
 .presentation-header .brand-bull{width:33px!important}.presentation-header .brand-bull img{width:32px!important;height:36px!important}
 .presentation-header .brand-pc{width:74px!important}.presentation-header .brand-pc img{width:72px!important;height:32px!important}
 .presentation-header .presenter-lockups{gap:4px!important}
 .presentation-header .mw-black{min-width:35px!important;width:35px!important;height:39px!important}
 .presentation-header .mw-black img{width:33px!important;height:33px!important}
 .presentation-header .signature-logo{width:42px!important;height:23px!important}
}
</style>
'''
assert '</head>' in s
p.write_text(s.replace('</head>',style+'</head>',1))
print('Applied side-by-side Louis and Kailan header arrangement',p.stat().st_size)
