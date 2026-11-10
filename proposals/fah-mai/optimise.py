from pathlib import Path
import re,base64,io
from PIL import Image
p=Path('proposals/fah-mai/index.html')
s=p.read_text()
before=len(s)
matches=re.findall(r'data:image/webp;base64,([a-zA-Z0-9+/=]+)',s)
for b64 in set(matches):
 raw=base64.b64decode(b64)
 if len(raw)<150000:
  print("SKIP SMALL transparent or logo asset",len(raw))
  continue
 im=Image.open(io.BytesIO(raw)).convert('RGB')
 im.thumbnail((1500,900),Image.Resampling.LANCZOS)
 o=io.BytesIO()
 im.save(o,format='WEBP',quality=68,method=6)
 out=base64.b64encode(o.getvalue()).decode()
 s=s.replace('data:image/webp;base64,'+b64,'data:image/webp;base64,'+out)
 print('OPTIMIZED',len(raw),'to',len(o.getvalue()),'dim',im.size)
p.write_text(s)
print('HTML SIZE',before,'->',len(s))
