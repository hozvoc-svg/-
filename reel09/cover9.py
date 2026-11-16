import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon9 as m
from engine import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
bg(c, 5, 1.0)
c.save(); c.translate(0, 180)
m.cliff(c, 1.0); m.ladder(c, 300, 1560, 600)
m.person(c, 300, 1100, 0.45, t=0.3, face='worried', armL=-2.6, armR=2.6, **m.OTHER)
m.sign(c, 140, 1390, 1, 'ROCK BOTTOM', m.RED, C['white'], 30)
m.sofa(c, 830, 1000, 0.75, webs=1.0); m.person(c, 830, 1000, 0.45, t=0.3, face='flat', **m.YOU)
m.sign(c, 980, 880, 1, 'FINE', C['yellow'], C['ink'], 40)
c.restore()
buf = np.ndarray((H, W, 4), np.uint8, surf.get_data()); img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
d = ImageDraw.Draw(img); F = '/usr/share/fonts/opentype/inter/'
def ct(txt, y, size, fill, font='Inter-Black.otf'):
    f = ImageFont.truetype(F + font, size); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=max(6, size // 12), stroke_fill=(20, 16, 40))
ct('WHY "FINE" IS', 300, 110, (255, 255, 255))
ct('WORSE THAN', 420, 110, (255, 255, 255))
ct('ROCK BOTTOM', 540, 124, (255, 210, 63))
img.save('cover_reel09.png')
