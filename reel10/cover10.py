import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon10 as m
from engine import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
bg(c, 1, 1.0)
c.save(); c.translate(0, 100)
m.person(c, 300, 1500, 0.8, t=0.3, face='big', look=14, blush=True, **m.YOU)
m.person(c, 790, 1500, 0.8, t=1.3, face='worried', look=-14, flip=True, **m.FRIEND)
m.table(c, 1360)
m.rain_cloud(c, 790, 680, 1, 0.5)
m.speech(c, 760, 880, 1, '"I got fired..."', C['white'], C['ink'], 42, 'right')
for k in range(3): text_c(c, 'ha', 170 + k * 60, 960 - k * 30, 50, C['white'])
c.restore()
buf = np.ndarray((H, W, 4), np.uint8, surf.get_data()); img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
d = ImageDraw.Draw(img); F = '/usr/share/fonts/opentype/inter/'
def ct(txt, y, size, fill, font='Inter-Black.otf'):
    f = ImageFont.truetype(F + font, size); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=max(6, size // 12), stroke_fill=(20, 16, 40))
ct('WHY YOU LAUGH', 300, 110, (255, 255, 255))
ct('AT THE WORST', 420, 110, (255, 255, 255))
ct('MOMENT', 540, 130, (255, 210, 63))
img.save('cover_reel10.png')
