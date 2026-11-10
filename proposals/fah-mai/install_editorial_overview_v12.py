from pathlib import Path
import requests,io,math
from PIL import Image,ImageOps,ImageEnhance,ImageFilter,ImageDraw

root=Path('proposals/fah-mai')
htmlpath=root/'index.html'
html=htmlpath.read_text(encoding='utf-8')
if 'id="fahmai-overview-campaign-v12"' in html:
    print('OVERVIEW_V12_ALREADY_INSTALLED')
    raise SystemExit(0)

sources={
 'fmh':('https://www.handpickedhotels.co.uk/images/hotels/norton-house/things-to-do/Scotch%20whisky%20experience/Worlds%20Largest%20Scotch%20Whisky%20Collection%20B.jpg', 'A real backlit wall of Scotch whisky bottles'),
 'bull':('https://www.stocktitan.net/news_covers/Brown_Forman_Announces_500_Million_Debt_Offering_1506232.webp','An isolated whisky-style oak cask in warm light'),
 'cask':('https://fahmaiholdings.com/wp-content/uploads/2026/05/Hades-Front.webp','Hades release, official Platinum Cask Olympians whisky bottle')
}
session=requests.Session()
session.headers.update({'User-Agent':'Mozilla/5.0 (compatible; editorial-photography/1.0)'})
images={}
for slug,(url,description) in sources.items():
    response=session.get(url,timeout=40)
    response.raise_for_status()
    image=Image.open(io.BytesIO(response.content)).convert('RGBA')
    assert image.width>=950 and image.height>=600,f'{slug}: source too small: {image.size}'
    images[slug]=image
    print('PHOTO_SOURCE',slug,image.size,len(response.content),'url',url)

S=800
def fit(image, center):
    return ImageOps.fit(image.convert('RGB'),(S,S),method=Image.Resampling.LANCZOS,centering=center)

def vignette(image, darkness=.20, bottom=.65):
    base=image.convert('RGB')
    overlay=Image.new('RGBA',(S,S),(0,0,0,0))
    px=overlay.load()
    for y in range(S):
        yf=y/(S-1)
        textfade=max(0,(yf-.39)/.58)
        # Image remains rich and detailed at top; text at bottom has deep plum contrast.
        shade=min(.90,darkness+bottom*textfade**1.35)
        for x in range(S):
            xf=x/(S-1)
            edge=max(0,abs(xf-.5)-.29)/.21
            side=min(.15,edge*.15)
            alpha=int(255*min(.92,shade+side))
            px[x,y]=(29,9,28,alpha)
    return Image.alpha_composite(base.convert('RGBA'),overlay).convert('RGB')

# Dramatic backlit shelves: preserve amber highlights and visual perspective.
wall=fit(images['fmh'],(.52,.48))
wall=ImageEnhance.Contrast(wall).enhance(1.06)
wall=ImageEnhance.Color(wall).enhance(.96)
wall=vignette(wall,.04,.76)

# A single oak cask hero: the barrel face is kept upper-center and crisply visible.
cask=fit(images['bull'],(.49,.40))
cask=ImageEnhance.Contrast(cask).enhance(1.15)
cask=ImageEnhance.Color(cask).enhance(.89)
cask=vignette(cask,.08,.76)

# Official Platinum Cask Hades release. Use the actual transparent product
# photograph and composite it over a dark editorial background; do not redraw
# the label or invent a bottle.
background=Image.new('RGB',(S,S))
draw=ImageDraw.Draw(background)
for y in range(S):
    t=y/(S-1)
    for x in range(S):
        rx=(x/S-.65)
        ry=(y/S-.32)
        glow=math.exp(-((rx/.36)**2+(ry/.45)**2)*1.3)
        rgb=(int(20+44*glow+32*t),int(13+15*glow+5*t),int(27+35*glow+27*t))
        background.putpixel((x,y),rgb)
# Subtle photographic warehouse texture prevents an artificial flat gradient.
texture=fit(images['bull'],(.65,.43)).filter(ImageFilter.GaussianBlur(32))
texture=ImageEnhance.Color(texture).enhance(.35)
texture.putalpha(58)
bg=Image.alpha_composite(background.convert('RGBA'),texture)
bottle=images['cask']
alpha=bottle.getchannel('A')
bbox=alpha.point(lambda p:255 if p>12 else 0).getbbox()
assert bbox,'Official branded bottle cutout has no alpha contents'
bottle=bottle.crop(bbox)
bottle.thumbnail((420,680),Image.Resampling.LANCZOS)
# Place the bottle on the upper-right, preserving a text-friendly left margin.
position=(int(S*.66-bottle.width*.5),42)
shadow=Image.new('RGBA',(S,S),(0,0,0,0))
mask=Image.new('L',(S,S),0)
mask.paste(bottle.getchannel('A'),position)
mask=mask.filter(ImageFilter.GaussianBlur(25))
shadow.paste((0,0,0,170),(0,0,S,S),mask)
bg=Image.alpha_composite(bg,shadow)
bg.alpha_composite(bottle,dest=position)
right=vignette(bg.convert('RGB'),.01,.50)

sprite=Image.new('RGB',(S*3,S),(0,0,0))
for index,img in enumerate((wall,cask,right)):
    sprite.paste(img,(index*S,0))
asset=root/'overview-photo-editorial-v12.webp'
sprite.save(asset,'WEBP',quality=88,method=6)
assert Image.open(asset).size==(2400,800)
print('EDITORIAL_SPRITE',asset,asset.stat().st_size,'size',(2400,800),'bottle_bbox',bbox,'composite_position',position)

style=r"""
<style id="fahmai-overview-campaign-v12">
/* Carefully selected original whisky photography, purpose-cropped at 800px per card.
   The existing pink-to-plum card gradients, shape, typography and layout are untouched. */
#overview .vision-card.vision-card-a::before,
#overview .vision-card.vision-card-b::before,
#overview .vision-card.vision-card-c::before {
  content:"" !important;
  inset:0 !important;
  width:100% !important;
  height:100% !important;
  background-image:url("./overview-photo-editorial-v12.webp") !important;
  background-size:300% 100% !important;
  background-repeat:no-repeat !important;
  opacity:.78 !important;
  filter:none !important;
  -webkit-print-color-adjust:exact !important;
  print-color-adjust:exact !important;
}
#overview .vision-card.vision-card-a::before {background-position:0% 50% !important;}
#overview .vision-card.vision-card-b::before {background-position:50% 50% !important;}
#overview .vision-card.vision-card-c::before {background-position:100% 50% !important;}
</style>
"""
assert html.count('</head>')==1
assert html.count('id="overview"')==1
assert '—' not in html
html=html.replace('</head>',style+'</head>',1)
htmlpath.write_text(html,encoding='utf-8')
print('OVERVIEW_V12_READY',len(html),'html bytes; three high-res cards', 'no other pages altered')
