import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon11 as m
from engine import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
bg(c, 5, 1.0)
m.chat_phone(c, W / 2 - 60, 1250, 1.05, 5, [('hey :)', True, 0), ('you there?', True, 0), ('???', True, 0)], ('Seen 2h ago', 0))
m.crack_heart(c, 860, 820, 0.7, 5, 1.0)
buf = np.ndarray((H, W, 4), np.uint8, surf.get_data()); img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
d = ImageDraw.Draw(img); F = '/usr/share/fonts/opentype/inter/'
def ct(txt, y, size, fill, font='Inter-Black.otf'):
    f = ImageFont.truetype(F + font, size); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=max(6, size // 12), stroke_fill=(20, 16, 40))
ct('BEING IGNORED', 300, 110, (255, 255, 255))
ct('HURTS LIKE', 420, 110, (255, 255, 255))
ct('REAL PAIN', 540, 130, (255, 77, 77))
img.save('cover_reel11.png')
