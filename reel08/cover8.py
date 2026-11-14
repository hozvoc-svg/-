import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon8 as m
from engine import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
m.split_bg(c, 0)
c.save(); c.translate(0, 120)
m.person(c, 270, 1500, 0.85, t=0.5, face='worried', look=10, armR=-0.9, **m.YOU); m.hand_phone(c, 205, 1290, 0.75, 0, 0)
m.desk(c, 760, 1170); m.person(c, 900, 1500, 0.85, t=1.5, face='o', look=-10, flip=True, **m.THEM); m.laptop(c, 665, 1165, 0.8)
m.speech(c, 290, 760, 1, 'YOU NEVER CALL!', m.RED, size=40, tail='left')
m.speech(c, 800, 900, 1, 'WHAT?!', C['white'], C['ink'], 44, 'right')
c.restore()
buf = np.ndarray((H, W, 4), np.uint8, surf.get_data()); img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
d = ImageDraw.Draw(img); F = '/usr/share/fonts/opentype/inter/'
def ct(txt, y, size, fill, font='Inter-Black.otf'):
    f = ImageFont.truetype(F + font, size); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=max(6, size // 12), stroke_fill=(20, 16, 40))
ct('YOU MISS THEM', 330, 104, (255, 255, 255))
ct('THEN YOU FIGHT?', 450, 104, (255, 210, 63))
ct("here's why", 580, 56, (255, 255, 255), 'Inter-Bold.otf')
img.save('cover_reel08.png')
