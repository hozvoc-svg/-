from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import math, random
S=1080; F='/usr/share/fonts/opentype/inter/'
CY=(0,240,255); MG=(255,40,200); GD=(255,210,60); WH=(255,255,255)
def bg():
    im=Image.new('RGB',(S,S),(6,4,16)); g=Image.new('RGB',(270,270),(0,0,0)); d=ImageDraw.Draw(g)
    d.ellipse([-40,-20,200,220],fill=(60,10,110)); d.ellipse([120,110,330,320],fill=(0,60,120))
    return ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(50)).resize((S,S)))
def glow(layer,radii=(4,14,40,90),k=(1.0,0.9,0.7,0.6)):
    out=layer.copy()
    for r,w in zip(radii,k):
        b=layer.filter(ImageFilter.GaussianBlur(r)); b=Image.eval(b,lambda v:min(255,int(v*w*1.6)))
        out=ImageChops.add(out,b)
    return out
def chroma(im,o=6):
    r,g,b=im.split()
    return Image.merge('RGB',(ImageChops.offset(r,o,0),g,ImageChops.offset(b,-o,0)))
def catmull(pts,n=12):
    out=[];P=pts+pts[:3]
    for i in range(len(pts)):
        p0,p1,p2,p3=P[i],P[i+1],P[i+2],P[i+3]
        for t in [j/n for j in range(n)]:
            t2,t3=t*t,t*t*t
            out.append(tuple(0.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t2+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t3) for k in (0,1)))
    return out
def sparks(d,cx,cy,n,rmin,rmax,cols,ang=(0,360),seed=3):
    random.seed(seed)
    for _ in range(n):
        a=math.radians(random.uniform(*ang)); r1=random.uniform(rmin,rmax); L=random.uniform(10,70)
        x1,y1=cx+math.cos(a)*r1,cy+math.sin(a)*r1; x2,y2=cx+math.cos(a)*(r1+L),cy+math.sin(a)*(r1+L)
        d.line([(x1,y1),(x2,y2)],fill=random.choice(cols),width=random.choice([2,3,4]))
    for _ in range(n):
        a=math.radians(random.uniform(*ang)); r1=random.uniform(rmin,rmax*1.3); s=random.uniform(2,6)
        x,y=cx+math.cos(a)*r1,cy+math.sin(a)*r1; d.ellipse([x-s,y-s,x+s,y+s],fill=random.choice(cols))
def keyhole(d,cx,cy,s,fill):
    r=s*0.22
    d.ellipse([cx-r,cy-s*0.32-r,cx+r,cy-s*0.32+r],fill=fill)
    d.polygon([(cx-r*0.55,cy-s*0.3),(cx+r*0.55,cy-s*0.3),(cx+r*1.0,cy+s*0.36),(cx-r*1.0,cy+s*0.36)],fill=fill)

# ---------- A: neon head with exploding mind ----------
head=[(330,1010),(355,820),(300,690),(270,520),(320,350),(440,235),(580,205),(710,245),(800,340),(835,450),(845,540),(905,650),(860,690),(865,740),(850,780),(855,830),(790,870),(690,880),(680,1010)]
pts=catmull(head)
L=Image.new('RGB',(S,S)); d=ImageDraw.Draw(L)
# gradient outline: draw segments colored cyan->magenta
for i in range(len(pts)-1):
    t=i/len(pts); col=tuple(int(CY[k]*(1-t)+MG[k]*t) for k in range(3))
    d.line([pts[i],pts[i+1]],fill=col,width=12)
# brain network
random.seed(7); nodes=[]
while len(nodes)<55:
    x,y=random.uniform(360,780),random.uniform(280,600)
    if (x-570)**2/210**2+(y-440)**2/170**2<1: nodes.append((x,y))
for i,a in enumerate(nodes):
    ds=sorted(nodes,key=lambda b:(a[0]-b[0])**2+(a[1]-b[1])**2)[1:4]
    for b in ds: d.line([a,b],fill=(0,90,150),width=2)
for x,y in nodes: d.ellipse([x-5,y-5,x+5,y+5],fill=(0,170,230))
# light rays from keyhole
cx,cy=570,450
for k in range(11):
    a=math.radians(-200+k*20); d.line([(cx,cy),(cx+math.cos(a)*700,cy+math.sin(a)*700)],fill=(55,40,8),width=5)
sparks(d,cx,cy,140,230,520,[GD,CY,MG,WH],ang=(-150,40))
L=glow(L)
im=ImageChops.add(bg(),L)
d=ImageDraw.Draw(im)
kh=Image.new('RGB',(S,S)); keyhole(ImageDraw.Draw(kh),cx,cy+10,250,GD); im=ImageChops.add(im,glow(kh,(6,20,60,140)))
keyhole(ImageDraw.Draw(im),cx,cy+10,275,(20,10,30))
keyhole(ImageDraw.Draw(im),cx,cy+10,250,GD)
chroma(im,5).save('A_neon_head.png')

# ---------- B: glitch eye ----------
L=Image.new('RGB',(S,S)); d=ImageDraw.Draw(L); c=S/2
top=[(c-430+i*8.6, c-math.sin(math.pi*i/100)*250) for i in range(101)]
bot=[(c+430-i*8.6, c+math.sin(math.pi*i/100)*250) for i in range(101)]
d.line(top+bot+[top[0]],fill=WH,width=14)
for k in range(72):
    a=math.radians(k*5); r1,r2=110,215; col=CY if k%2 else MG
    d.line([(c+math.cos(a)*r1,c+math.sin(a)*r1),(c+math.cos(a)*r2,c+math.sin(a)*r2)],fill=col,width=5)
d.ellipse([c-215,c-215,c+215,c+215],outline=CY,width=8)
sparks(d,c,c,90,470,560,[CY,MG,GD])
L=glow(L)
im=ImageChops.add(bg(),L)
kh=Image.new('RGB',(S,S)); keyhole(ImageDraw.Draw(kh),c,c+10,190,GD); im=ImageChops.add(im,glow(kh,(6,20,60,120)))
ImageDraw.Draw(im).ellipse([c-108,c-108,c+108,c+108],fill=(8,4,20))
keyhole(ImageDraw.Draw(im),c,c+10,190,GD)
# glitch slices
random.seed(11)
for _ in range(9):
    y=random.randint(250,830); h=random.randint(8,40); dx=random.randint(-60,60)
    sl=im.crop((0,y,S,y+h)); im.paste(sl,(dx,y))
im=chroma(im,8)
d=ImageDraw.Draw(im)
for y in range(0,S,6): d.line([(0,y),(S,y)],fill=(0,0,0),width=1)
im.save('B_glitch_eye.png')

# ---------- C: neon monogram with lightning ----------
L=Image.new('RGB',(S,S)); d=ImageDraw.Draw(L)
fnt=ImageFont.truetype(F+'Inter-Black.otf',430)
d.text((c-215,c+10),'P',font=fnt,anchor='mm',fill=(0,0,0),stroke_width=12,stroke_fill=CY)
d.text((c+215,c+10),'U',font=fnt,anchor='mm',fill=(0,0,0),stroke_width=12,stroke_fill=CY)
bolt=[(x*0.8+60,y) for x,y in [(640,170),(470,520),(600,520),(420,920),(760,430),(620,430),(760,170)]]
d.polygon(bolt,fill=GD)
d.ellipse([c-470,c-470,c+470,c+470],outline=MG,width=10)
sparks(d,c,c,120,380,560,[CY,MG,GD,WH])
im=ImageChops.add(bg(),glow(L,(3,12,35,80),(0.6,0.5,0.4,0.35)))
ImageDraw.Draw(im).text((c-215,c+10),'P',font=fnt,anchor='mm',fill=(10,6,25))
ImageDraw.Draw(im).text((c+215,c+10),'U',font=fnt,anchor='mm',fill=(10,6,25))
ImageDraw.Draw(im).polygon(bolt,fill=(255,250,220))
chroma(im,6).save('C_neon_monogram.png')

# comparison sheet with circle previews
sheet=Image.new('RGB',(1200,560),(250,250,250)); sd=ImageDraw.Draw(sheet)
fl=ImageFont.truetype(F+'Inter-Bold.otf',34)
for i,(f,lab) in enumerate([('A_neon_head.png','A'),('B_glitch_eye.png','B'),('C_neon_monogram.png','C')]):
    p=Image.open(f).resize((340,340)); m=Image.new('L',(340,340),0); ImageDraw.Draw(m).ellipse([0,0,339,339],fill=255)
    sheet.paste(p,(40+i*390,40),m)
    q=Image.open(f).resize((90,90)); m2=Image.new('L',(90,90),0); ImageDraw.Draw(m2).ellipse([0,0,89,89],fill=255)
    sheet.paste(q,(165+i*390,420),m2)
    sd.text((40+i*390,400),lab,font=fl,fill=(0,0,0))
sheet.save('compare.png')
