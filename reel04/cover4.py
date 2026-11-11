import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon4 as m
from engine import *
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(surf)
c.save(); c.translate(0,250); m.bedroom(c,0.6,face='worried',sweat=0.8); c.restore()
c.rectangle(0,0,W,250); c.set_source_rgb(*m.BG_N_TOP); c.fill()
m.wave_memory(c,300,1060,0.9,0.3)
buf=np.ndarray((H,W,4),np.uint8,surf.get_data()); img=Image.fromarray(buf[:,:,[2,1,0]].copy())
d=ImageDraw.Draw(img); F='/usr/share/fonts/opentype/inter/'
def ct(txt,y,size,fill,font='Inter-Black.otf'):
    f=ImageFont.truetype(F+font,size); w=d.textlength(txt,font=f)
    d.text(((W-w)/2,y),txt,font=f,fill=fill,stroke_width=max(6,size//12),stroke_fill=(20,16,40))
ct('WHY YOU REMEMBER',360,80,(255,255,255))
ct('CRINGE MOMENTS',460,96,(255,210,63))
ct('AT 3 AM',580,130,(255,77,77))
img.save('cover_reel04.png')
w,h=img.size; ch=int(w*4/3); y=(h-ch)//2
img.crop((0,y,w,y+ch)).resize((300,400)).save('/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/grid4.png')
