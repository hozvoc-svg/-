import sys,subprocess,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
F='/usr/share/fonts/opentype/inter/Inter-BlackItalic.otf'
g=json.load(open('shots_good.json'))
C=[('map',51,['THE GTA 6','MAP IS HUGE'],(0,229,255)),('night',49,['VICE CITY','AFTER DARK'],(255,45,149)),('floridaman',12,['FLORIDA MAN','IS BACK'],(255,230,0))]
mas=Image.open('img/sprites/m2_e0.png').convert('RGBA').resize((480,480),Image.LANCZOS)
for name,ix,lines,col in C:
    s=g[ix]; t=(s['start']+s['end'])/2
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',s['src'],'-frames:v','1','covers/_f.png'])
    im=Image.open('covers/_f.png').convert('RGB')
    if s['lb']:
        import numpy as np; m=np.asarray(im.convert('L'),float).mean(1)
        U=[y for y in range(400,960) if m[y]<5]; D=[y for y in range(960,1550) if m[y]<5]
        up,dn=(max(U)+4,min(D)-4) if U and D else (672,1268)
        band=im.crop((0,up,1080,dn)); bh=dn-up
        bg=band.resize((int(1080*1920/bh),1920)).crop((0,0,1080,1920)).filter(ImageFilter.GaussianBlur(30))
        bg=ImageEnhance.Brightness(bg).enhance(0.55)
        fg=band.resize((1080*13//10,bh*13//10)).crop((108,0,1188,bh*13//10)); bg.paste(fg,(0,560)); im=bg
    im=ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.3)).enhance(1.12).convert('RGBA')
    g2=Image.new('L',(1,1920)); [g2.putpixel((0,y),int(max(0,(y-1000)/920)*190)) for y in range(1920)]
    sh=Image.new('RGBA',(1080,1920),(0,0,0,255)); sh.putalpha(g2.resize((1080,1920))); im.alpha_composite(sh)
    d=ImageDraw.Draw(im); y=1300
    for i,tx in enumerate(lines):
        size=190
        while ImageFont.truetype(F,size).getlength(tx)>980: size-=6
        f=ImageFont.truetype(F,size)
        d.text((546,y+8),tx,font=f,fill='black',anchor='mm',stroke_width=14,stroke_fill='black')
        d.text((540,y),tx,font=f,fill='white' if i==0 else col,anchor='mm',stroke_width=12,stroke_fill='black'); y+=size+10
    bf=ImageFont.truetype(F,70); d.rounded_rectangle([60,150,370,260],28,fill=(255,45,149)); d.text((215,205),'GTA 6',font=bf,fill='white',anchor='mm')
    im.alpha_composite(mas,(620,1500)); im.convert('RGB').save(f'covers/{name}_cover.jpg',quality=93)
print('ok')
