import sys
src=open('cartoon.py').read().split('if PREVIEW:')[0]
exec(src)
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(surf)
t=2.0
bg(c,0,t)
# brain with rays
c.save(); c.translate(W/2,1000); c.scale(1.1,1.1)
for k in range(12):
    ang=k*math.pi/6; line(c,math.cos(ang)*190,math.sin(ang)*190,math.cos(ang)*245,math.sin(ang)*245,14,C['yellow'])
for (bx,by,r) in [(-70,-10,85),(40,-50,90),(90,30,75),(-20,50,80),(-100,50,60)]: circle(c,bx,by,r,C['pink'])
for k in range(4):
    c.set_line_width(10); c.set_source_rgba(1,1,1,0.55); c.arc(-60+k*45,-10+(k%2)*30,30,0.2,2.6); c.stroke()
c.restore()
for k in range(6):
    ang=k*1.05+0.4; star(c,W/2+math.cos(ang)*360,1000+math.sin(ang)*280,24,C['yellow'],0.95,ang)
person(c,250,1700,0.75,C['sky'],0.5,face='big',look=14,armR=-2.4,hairstyle=1,skin=C['skin2'])
person(c,830,1700,0.75,C['coral'],1.3,face='big',look=-14,flip=True,armR=-2.4,blush=True,hairstyle=2,hair=C['hair2'])
heart(c,830,1180,1.3,C['pink']); heart(c,900,1100,0.9,C['pink'],0.8)
buf=np.ndarray((H,W,4),np.uint8,surf.get_data()); img=Image.fromarray(buf[:,:,[2,1,0]].copy())
d=ImageDraw.Draw(img); F='/usr/share/fonts/opentype/inter/'
def ct(txt,y,size,fill,font='Inter-Black.otf'):
    f=ImageFont.truetype(F+font,size); w=d.textlength(txt,font=f)
    d.text(((W-w)/2,y),txt,font=f,fill=fill,stroke_width=max(6,size//12),stroke_fill=(20,16,40))
ct('4 PSYCHOLOGY',330,128,(255,255,255))
ct('TRICKS',470,200,(255,210,63))
ct('that work almost too well',700,58,(255,255,255),'Inter-ExtraBold.otf')
img.save('cover_reel01.png')
img.resize((540,960)).save('/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/cover_prev.png')
