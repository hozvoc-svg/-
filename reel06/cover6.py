import sys
sys.path.insert(0, '..')
from engine import *
import engine
engine.BG += [(hx('1E0B2E'), hx('6B1E5F'))]
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(surf)
bg(c,6,1.0)
hxp=W/2; hyp=900
c.save(); c.translate(hxp,hyp)
rrect(c,-110,-40,220,70,35); fill(c,C['skin1'])
for k in range(4): rrect(c,-95+k*52,10,36,80,18); fill(c,C['skin1'])
rrect(c,-150,-80,300,50,20); fill(c,hx('3D2B6B')); c.restore()
c.set_line_width(4); c.set_source_rgba(1,1,1,0.8)
for (x,y) in [(W/2-120,1360),(W/2+120,1360),(W/2,1160)]:
    c.move_to(hxp,hyp+80); c.curve_to(hxp,(hyp+y)/2,x,(hyp+y)/2,x,y); c.stroke()
person(c,W/2,1720,0.85,C['sky'],0.3,face='worried',armL=0.9,armR=-0.9,skin=C['skin2'],hairstyle=2,hair=C['hair2'])
buf=np.ndarray((H,W,4),np.uint8,surf.get_data()); img=Image.fromarray(buf[:,:,[2,1,0]].copy())
d=ImageDraw.Draw(img); F='/usr/share/fonts/opentype/inter/'
def ct(txt,y,size,fill,font='Inter-Black.otf'):
    f=ImageFont.truetype(F+font,size); w=d.textlength(txt,font=f)
    d.text(((W-w)/2,y),txt,font=f,fill=fill,stroke_width=max(6,size//12),stroke_fill=(20,16,40))
ct('3 MORE PHRASES',380,108,(255,255,255))
ct('MANIPULATORS USE',540,84,(230,57,70))
ct('PART 2',660,64,(255,210,63))
img.save('cover_reel06.png')
w,h=img.size; ch=int(w*4/3); y=(h-ch)//2
img.crop((0,y,w,y+ch)).resize((300,400)).save('/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/grid6.png')
