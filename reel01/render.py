import json, math, random, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
a=json.load(open('align.json'))
ch,st,en=a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']
text=''.join(ch)
# words
words=[];i=0
while i<len(ch):
    if ch[i].isspace(): i+=1; continue
    j=i
    while j<len(ch) and not ch[j].isspace(): j+=1
    words.append((text[i:j],st[i],en[j-1],i)); i=j
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','voice.mp3']))+0.8
# chunks of up to 3 words, break at punctuation
chunks=[];cur=[]
for w in words:
    cur.append(w)
    if len(cur)>=3 or w[0][-1] in '.,?:!':
        chunks.append(cur);cur=[]
if cur: chunks.append(cur)
def t_of(phrase):
    k=text.find(phrase); return st[k]
sections=[(0,'4 PSYCHOLOGY\nTRICKS',None),
 (t_of('Number one'),'BEN FRANKLIN\nEFFECT','01'),
 (t_of('Number two'),'PRATFALL\nEFFECT','02'),
 (t_of('Number three'),'THE POWER\nOF SILENCE','03'),
 (t_of('Number four'),'PEAK-END\nRULE','04'),
 (t_of('Follow for'),'PART 2\nTOMORROW',None)]
F='/usr/share/fonts/opentype/inter/'
fBig=ImageFont.truetype(F+'Inter-Black.otf',118)
fNum=ImageFont.truetype(F+'Inter-Black.otf',300)
fCap=ImageFont.truetype(F+'Inter-ExtraBold.otf',86)
fSm=ImageFont.truetype(F+'Inter-SemiBold.otf',38)
ACC=(255,210,60)
# static background
bg=Image.new('RGB',(W,H))
d=ImageDraw.Draw(bg)
for y in range(H):
    c=int(8+14*(y/H)); d.line([(0,y),(W,y)],fill=(c,c,c+10))
random.seed(1)
grain=[Image.effect_noise((W,H),18).convert('L') for _ in range(4)]
def glow(t):
    g=Image.new('RGB',(W//4,H//4),(0,0,0)); gd=ImageDraw.Draw(g)
    for k,(col,ph) in enumerate([((90,40,160),0),((20,80,160),2),((150,110,20),4)]):
        x=W//8+math.sin(t*0.3+ph)*90; y=H//8+math.cos(t*0.23+ph*1.3)*170
        r=110; gd.ellipse([x-r,y-r,x+r,y+r],fill=col)
    return g.filter(ImageFilter.GaussianBlur(45)).resize((W,H))
def center(d,txt,font,y,fill,spacing=10):
    bb=d.multiline_textbbox((0,0),txt,font=font,align='center',spacing=spacing)
    d.multiline_text(((W-(bb[2]-bb[0]))/2,y),txt,font=font,fill=fill,align='center',spacing=spacing)
os.makedirs('frames',exist_ok=True)
N=int(dur*FPS)
for f in range(N):
    t=f/FPS
    img=Image.blend(bg,glow(t),0.55) if True else bg
    img=Image.composite(Image.new('RGB',(W,H),(255,255,255)),img,grain[f%4].point(lambda v:12 if v>140 else 0))
    d=ImageDraw.Draw(img)
    # section
    sec=[s for s in sections if s[0]<=t][-1]
    age=t-sec[0]; pop=min(1,age/0.25)
    if sec[2]:
        d.text((W/2,560),sec[2],font=fNum,fill=(255,255,255,),anchor='mm') if False else None
        nl=ImageDraw.Draw(img)
        center(nl,sec[2],fNum,300+int((1-pop)*40),tuple(int(v*0.18*pop+20*(1-pop)) for v in (255,255,255)))
    center(d,sec[1],fBig,560+int((1-pop)*60),tuple(int(v*pop) for v in ACC))
    # caption
    ck=[c for c in chunks if c[0][1]-0.05<=t]
    if ck and t<=ck[-1][-1][2]+0.6:
        c=ck[-1]
        parts=[(w[0].upper(),w[1]<=t) for w in c]
        full=' '.join(p[0] for p in parts)
        # wrap if wide
        fw=d.textlength(full,font=fCap)
        lines=[parts] if fw<W-140 else [parts[:2],parts[2:]]
        y=1180
        for ln in lines:
            s=' '.join(p[0] for p in ln); x=(W-d.textlength(s,font=fCap))/2
            for wtxt,on in ln:
                d.text((x,y),wtxt,font=fCap,fill=ACC if on and wtxt==[p for p in parts if p[1]][-1][0] else (255,255,255),stroke_width=7,stroke_fill=(0,0,0))
                x+=d.textlength(wtxt+' ',font=fCap)
            y+=105
    # progress bar + handle
    d.rectangle([0,H-10,int(W*t/dur),H],fill=ACC)
    center(d,'@yourhandle  •  daily psychology',fSm,H-230,(150,150,160))
    img.save(f'frames/{f:05d}.jpg',quality=90)
print(N,dur)
