import sys, os
sys.path.insert(0, '..')
from engine import *
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(surf)
bg(c,2,1.0)
heart(c,W/2,1060,4.0,C['pink'])
circle(c,W/2-52,1000,21,C['white']); circle(c,W/2+52,1000,21,C['white'])
for k in range(8):
    ang=k*math.pi/4+0.3; heart(c,W/2+math.cos(ang)*320,1060+math.sin(ang)*210,0.7,C['white'],0.85)
person(c,250,1700,0.75,C['sky'],0.5,face='smile',look=14,hairstyle=1,skin=C['skin2'])
person(c,830,1700,0.75,C['coral'],1.3,face='big',look=-16,flip=True,blush=True,armR=-2.5,hairstyle=2,hair=C['hair2'])
buf=np.ndarray((H,W,4),np.uint8,surf.get_data()); img=Image.fromarray(buf[:,:,[2,1,0]].copy())
d=ImageDraw.Draw(img); F='/usr/share/fonts/opentype/inter/'
def ct(txt,y,size,fill,font='Inter-Black.otf'):
    f=ImageFont.truetype(F+font,size); w=d.textlength(txt,font=f)
    d.text(((W-w)/2,y),txt,font=f,fill=fill,stroke_width=max(6,size//12),stroke_fill=(20,16,40))
ct('5 SIGNS',380,150,(255,210,63))
ct('SOMEONE SECRETLY',560,84,(255,255,255))
ct('LIKES YOU',660,110,(255,255,255))
img.save('cover_reel02.png')
w,h=img.size; ch=int(w*4/3); y=(h-ch)//2
img.crop((0,y,w,y+ch)).resize((300,400)).save('/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/grid2.png')
