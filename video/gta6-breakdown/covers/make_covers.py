from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
F='/usr/share/fonts/opentype/inter/Inter-BlackItalic.otf'
C=[('characters','cand/t2_1_6.5.png',['NOT A REAL','PERSON?!'],(255,230,0)),
   ('lighting','cand/t2_2_0.5.png',['INSANE','LIGHTING'],(0,229,255)),
   ('vicecity','cand/t2_3_20.png',['VICE CITY','IS BACK'],(255,45,149))]
mas=Image.open('../img/sprites/m2_e0.png').convert('RGBA').resize((520,520),Image.LANCZOS)
for name,src,lines,col in C:
    im=Image.open(src).convert('RGB').resize((1080,1920))
    im=ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.35)).enhance(1.15).convert('RGBA')
    # darken bottom half for text legibility
    g=Image.new('L',(1,1920)); [g.putpixel((0,y),int(max(0,(y-900)/1020)*200)) for y in range(1920)]
    sh=Image.new('RGBA',(1080,1920),(0,0,0,255)); sh.putalpha(g.resize((1080,1920))); im.alpha_composite(sh)
    d=ImageDraw.Draw(im)
    y=1180
    for i,t in enumerate(lines):
        size=200
        while ImageFont.truetype(F,size).getlength(t)>980: size-=6
        f=ImageFont.truetype(F,size)
        d.text((540+6,y+8),t,font=f,fill=(0,0,0),anchor='mm',stroke_width=14,stroke_fill=(0,0,0))
        d.text((540,y),t,font=f,fill=(255,255,255) if i==0 else col,anchor='mm',stroke_width=12,stroke_fill=(0,0,0))
        y+=size+10
    # GTA 6 badge
    bf=ImageFont.truetype(F,70); d.rounded_rectangle([60,150,370,260],28,fill=(255,45,149)); d.text((215,205),'GTA 6',font=bf,fill='white',anchor='mm')
    glow=mas.split()[3].filter(ImageFilter.GaussianBlur(16)); gl=Image.new('RGBA',mas.size,col+(0,)); gl.putalpha(glow)
    im.alpha_composite(gl,(600,1480)); im.alpha_composite(mas,(600,1480))
    im.convert('RGB').save(f'{name}_cover.jpg',quality=93)
print('ok')
