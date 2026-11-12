from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
F='/usr/share/fonts/opentype/inter/Inter-BlackItalic.otf'
SP='../gta6-breakdown/img/sprites/'
PINK=(255,45,149); CYAN=(0,229,255); DEEP=(26,4,48)
def grad(w,h):
    im=Image.new('RGB',(w,h)); px=im.load()
    for y in range(h):
        for x in range(0,w):
            t=y/h; s=x/w
            r=int(DEEP[0]*(1-t)+120*t*s+PINK[0]*0.55*t*(1-s)); g=int(DEEP[1]*(1-t)+20*t); b=int(DEEP[2]*(1-t)+90*t+60*s*t)
            px[x,y]=(min(r,255),g,min(b,255))
    return im
def sun(im,cx,cy,R):
    d=ImageDraw.Draw(im)
    for i in range(R,0,-2):
        t=i/R; d.ellipse([cx-i,cy-i,cx+i,cy+i],fill=(255,int(60+150*(1-t)),int(150*t)))
    for k in range(7):  # retro stripes
        y=cy+int(R*0.15)+k*int(R*0.12); d.rectangle([cx-R,y,cx+R,y+int(R*0.025)+k*4],fill=(40,5,60))
def palms(im,xs,base,h):
    d=ImageDraw.Draw(im)
    for x,sc in xs:
        top=(x+int(40*sc),base-int(h*sc)); d.line([(x,base),top],fill=(10,0,20),width=int(18*sc))
        for a in range(0,360,40):
            ex=top[0]+int(math.cos(math.radians(a))*160*sc); ey=top[1]+int(abs(math.sin(math.radians(a)))*60*sc)+int(40*sc)
            d.line([top,((top[0]+ex)//2,top[1]-int(30*sc)),(ex,ey)],fill=(10,0,20),width=int(14*sc),joint='curve')
def text(d,xy,s,size,fill,anchor='mm',stroke=0,sf=(0,0,0)):
    d.text(xy,s,font=ImageFont.truetype(F,size),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=sf)
mas=Image.open(SP+'m2_e0.png').convert('RGBA')
# ---------- avatar 800x800 (shown as circle)
av=grad(800,800); sun(av,400,330,260)
head=mas.crop((120,40,680,600)).resize((760,760),Image.LANCZOS)
glow=head.split()[3].filter(ImageFilter.GaussianBlur(18)); gl=Image.new('RGBA',head.size,CYAN+(0,)); gl.putalpha(glow)
av=av.convert('RGBA'); av.alpha_composite(gl,(20,90)); av.alpha_composite(head,(20,90))
av.convert('RGB').save('avatar.png')
# ---------- banner 2560x1440, safe area 1546x423 centred
W,H=2560,1440; bn=grad(W,H); sun(bn,W//2,H//2-40,520)
d=ImageDraw.Draw(bn)
for k in range(12):  # synthwave floor grid
    y=H//2+180+k*k*6; d.line([(0,y),(W,y)],fill=PINK,width=2)
for k in range(-20,21):
    d.line([(W//2+k*40,H//2+180),(W//2+k*260,H)],fill=PINK,width=2)
bn=bn.convert('RGBA'); m=mas.resize((560,560),Image.LANCZOS); bn.alpha_composite(m,(W//2-773-40,H//2-320))
d=ImageDraw.Draw(bn)
text(d,(W//2+130,H//2-80),'ROCCO GTA',190,(255,255,255),stroke=12,sf=PINK)
text(d,(W//2+130,H//2+70),'GTA 6 DETAILS  •  NEWS  •  GAMEPLAY',58,CYAN,stroke=5,sf=DEEP)
text(d,(W//2+130,H//2+150),'NEW SHORTS EVERY DAY',44,(255,230,120),stroke=4,sf=DEEP)
bn.convert('RGB').save('banner.png',quality=92)
# preview: safe area box
p=bn.copy(); ImageDraw.Draw(p).rectangle([W//2-773,H//2-211,W//2+773,H//2+211],outline=(255,255,0),width=6); p.convert('RGB').resize((1280,720)).save('banner_safezone_preview.png')
print('ok')
