from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
S=1080; ACC=(255,210,60); F='/usr/share/fonts/opentype/inter/'
def bg(size):
    im=Image.new('RGB',(size,size),(10,10,18))
    g=Image.new('RGB',(size//4,size//4),(0,0,0)); d=ImageDraw.Draw(g)
    q=size//4
    d.ellipse([q*0.05,q*0.0,q*0.75,q*0.7],fill=(70,35,140))
    d.ellipse([q*0.35,q*0.4,q*1.05,q*1.1],fill=(20,70,150))
    g=g.filter(ImageFilter.GaussianBlur(q*0.18)).resize((size,size))
    return Image.blend(im,g,0.6)
def keyhole(d,cx,cy,s,fill):
    r=s*0.22
    d.ellipse([cx-r,cy-s*0.32-r,cx+r,cy-s*0.32+r],fill=fill)
    d.polygon([(cx-r*0.55,cy-s*0.3),(cx+r*0.55,cy-s*0.3),(cx+r*1.0,cy+s*0.36),(cx-r*1.0,cy+s*0.36)],fill=fill)
# profile photo
im=bg(S); d=ImageDraw.Draw(im)
c=S/2
for w,col in [(30,ACC)]:
    d.ellipse([c-330,c-330,c+330,c+330],outline=col,width=w)
# open arc gap = "unlocked": cover a slice of ring
d.pieslice([c-360,c-360,c+360,c+360],-70,-30,fill=None)
ring=Image.new('L',(S,S),0); rd=ImageDraw.Draw(ring)
rd.ellipse([c-345,c-345,c+345,c+345],outline=255,width=30)
rd.pieslice([c-400,c-400,c+400,c+400],-65,-35,fill=0)
im=bg(S); im.paste(Image.new('RGB',(S,S),ACC),(0,0),ring); d=ImageDraw.Draw(im)
keyhole(d,c,c+30,560,(255,255,255))
im.save('profile_photo.png')
# small preview as circle
p=im.resize((220,220)); m=Image.new('L',(220,220),0); ImageDraw.Draw(m).ellipse([0,0,219,219],fill=255)
pv=Image.new('RGB',(220,220),(255,255,255)); pv.paste(p,(0,0),m); pv.save('preview_circle.png')
# highlight covers
fT=ImageFont.truetype(F+'Inter-Black.otf',150)
for name,label in [('tricks','TRICKS'),('love','LOVE'),('mind','MIND'),('start','START')]:
    h=bg(S); hd=ImageDraw.Draw(h)
    hd.ellipse([c-300,c-300,c+300,c+300],outline=ACC,width=14)
    hd.text((c,c),label,font=ImageFont.truetype(F+'Inter-Black.otf',150 if len(label)<=5 else 125),fill=ACC,anchor='mm')
    h.save(f'highlight_{name}.png')
print('ok')
