import numpy as np, random, sys
from PIL import Image, ImageFilter, ImageDraw
hdr=np.load('hdr.npy'); H,W,_=hdr.shape
exp=float(sys.argv[1]) if len(sys.argv)>1 else 6.0
x=hdr*exp
# particles: golden embers in HDR
random.seed(5); P=np.zeros_like(x); Pim=Image.new('RGB',(W,H)); d=ImageDraw.Draw(Pim)
for _ in range(int(140*W/1080)):
    px=random.gauss(W*0.42,W*0.22); py=random.uniform(H*0.08,H*0.75); s=random.choice([1,1,2,2,3,5,8])*W/1080
    a=random.randint(60,255) if s<4 else random.randint(25,70)
    d.ellipse([px-s,py-s,px+s,py+s],fill=(a,int(a*0.66),int(a*0.25)))
Pim=Image.blend(Pim,Pim.filter(ImageFilter.GaussianBlur(3*W/1080)),0.6)
x+=np.asarray(Pim,dtype=np.float64)/255*1.2
# bloom
def blur(a,r):
    im=Image.fromarray(np.clip(a/4*255,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im,dtype=np.float64)/255*4
br=np.clip(x-0.8,0,4)
x+=blur(br,W*0.01)*0.6+blur(br,W*0.04)*0.5+blur(br,W*0.1)*0.4
# ACES
a,b,c,dd,e=2.51,0.03,2.43,0.59,0.14
y=np.clip((x*(a*x+b))/(x*(c*x+dd)+e),0,1)
# grade: lift shadows slightly teal, warm highs
y=y**(1/1.05)
yy,xx=np.mgrid[0:H,0:W]; v=1-0.55*(((xx/W-0.5)**2+(yy/H-0.48)**2)*2.2); y*=np.clip(v,0,1)[...,None]
y+=np.random.default_rng(1).normal(0,0.012,y.shape)
out=Image.fromarray(np.clip(y*255,0,255).astype(np.uint8))
# chromatic aberration subtle
r,g,b=out.split(); from PIL import ImageChops
o=max(1,W//540); out=Image.merge('RGB',(ImageChops.offset(r,o,0),g,ImageChops.offset(b,-o,0)))
out.save(sys.argv[2] if len(sys.argv)>2 else 'test.png')
