from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).resolve().parent; res=p/'dist/Crash_Bandicoot_PSP_Theme';out=p/'screenshots';out.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=lambda n:ImageFont.truetype(font,n)
cats=[(1,'Settings'),(2,'Photo'),(3,'Music'),(4,'Video'),(5,'TV'),(6,'Game'),(7,'Network'),(8,'Extras')]
sections={'settings':(1,14,'Network Update',16,'USB Connection'),'photo':(2,6,'Camera',2,'Memory Stick'),'music':(3,2,'Memory Stick',4,'UMD'),'video':(4,2,'Memory Stick',4,'UMD'),'game':(6,8,'Game Sharing',10,'Saved Data Utility'),'network':(7,48,'Internet Browser',46,'RSS Channel')}
def alpha(img,alpha):
 a=img.getchannel('A').point(lambda x:int(x*alpha));img=img.copy();img.putalpha(a);return img
def render(name,cat,item,label,other,otherlabel):
 canvas=Image.open(res/'1_0000.png').convert('RGBA'); d=ImageDraw.Draw(canvas); idx=[x[0] for x in cats].index(cat)
 for k,(num,_) in enumerate(cats):
  x=110+(k-idx)*82-32
  if x<480 and x+64>0:
   icon=Image.open(res/f'2_{num:04}.png').convert('RGBA');canvas.alpha_composite(alpha(icon,1 if k==idx else .62),(x,48))
 d=ImageDraw.Draw(canvas);d.text((110,103),cats[idx][1],font=F(11),fill='white',anchor='mt',stroke_width=1,stroke_fill='#171717')
 for j,(iid,txt) in enumerate([(item,label),(other,otherlabel)]):
  y=137+j*64;icon=Image.open(res/f'3_{iid:04}.png').convert('RGBA');canvas.alpha_composite(alpha(icon,1 if not j else .55),(86,y-24));d=ImageDraw.Draw(canvas);d.text((149,y-7),txt,font=F(13),fill='white' if not j else '#dedede',stroke_width=1,stroke_fill='#151515')
 d.text((464,8),'12:00',font=F(10),fill='white',anchor='ra',stroke_width=1,stroke_fill='#111')
 canvas.convert('RGB').save(out/f'{name}_simulation.png')
for n,args in sections.items():render(n,*args)
Image.open(p/'assets/wallpaper/wallpaper.png').save(out/'wallpaper.png')
# Artificial product image and simulated XMB, composited; not a hardware photo.
im=Image.open(p/'assets/mockup_source.png').convert('RGB');screen=Image.open(out/'game_simulation.png').convert('RGB').resize((568,322),Image.Resampling.LANCZOS);im.paste(screen,(484,222));im.save(out/'psp_go_concept_mockup.png')
