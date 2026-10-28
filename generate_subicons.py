from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
p=Path(__file__).resolve().parent
source=p/'base_icons'; dest=p/'assets/subcategory'; dest.mkdir(exist_ok=True)
for group,ids in [(3,range(2,60,2)),(4,[0,2])]:
 for i in ids:
  im=Image.open(source/f'{group}_{i:04}.png').convert('RGBA');w,h=im.size;S=3
  a=im.getchannel('A').resize((w*S,h*S),Image.Resampling.LANCZOS)
  # Deep shadow and amber outline keep each original pictogram legible.
  outline=a.filter(ImageFilter.MaxFilter(9)); layer=Image.new('RGBA',(w*S,h*S)); layer.paste((66,32,7,230),(0,0,w*S,h*S),outline)
  grad=Image.new('RGBA',(w*S,h*S)); px=grad.load()
  for y in range(h*S):
   t=y/(h*S-1)
   for x in range(w*S):px[x,y]=(255,round(211-83*t),round(91-70*t),255)
  layer.paste(grad,(0,0),a)
  d=ImageDraw.Draw(layer)
  # A small tropical leaf, positioned clear of the central symbol.
  if group==3:
   d.ellipse((2*S,35*S,11*S,42*S),fill=(29,105,39,255),outline=(200,208,78,255),width=S)
   d.line((3*S,41*S,10*S,36*S),fill=(198,220,85,255),width=S)
  layer.resize((w,h),Image.Resampling.LANCZOS).save(dest/f'{group}_{i:04}.png')
