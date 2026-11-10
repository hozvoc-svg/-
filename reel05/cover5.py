import sys
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon5 as m
from engine import *
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(surf)
bg(c,0,1.0)
m.phone(c,W/2,1240,460,760,300,1.0)
m.thumb(c,W/2+110,1500,0.6)
c.save(); c.translate(850,900); c.rotate(0.15); circle(c,0,0,90,hx('E63946')); text_c(c,'?!',0,0,80,C['white']); c.restore()
buf=np.ndarray((H,W,4),np.uint8,surf.get_data()); img=Image.fromarray(buf[:,:,[2,1,0]].copy())
d=ImageDraw.Draw(img); F='/usr/share/fonts/opentype/inter/'
def ct(txt,y,size,fill,font='Inter-Black.otf'):
    f=ImageFont.truetype(F+font,size); w=d.textlength(txt,font=f)
    d.text(((W-w)/2,y),txt,font=f,fill=fill,stroke_width=max(6,size//12),stroke_fill=(20,16,40))
ct('WHY YOU',370,100,(255,255,255))
ct("CAN'T STOP",490,130,(255,210,63))
ct('SCROLLING',640,110,(255,255,255))
img.save('cover_reel05.png')
w,h=img.size; ch=int(w*4/3); y=(h-ch)//2
img.crop((0,y,w,y+ch)).resize((300,400)).save('/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/grid5.png')
