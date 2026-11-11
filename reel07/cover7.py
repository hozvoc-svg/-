import sys, os
sys.path.insert(0, '..'); sys.path.insert(0, '.')
import cartoon7 as m
from engine import *
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
bg(c, m.NIGHT, 0.6); m.night_sky(c, 0.6)
m.bg = lambda *a: None; m.night_sky = lambda *a: None
c.save(); c.translate(0, 330); m.bedroom(c, 0.6, face='flat'); c.restore()
m.fight_dream(c, 1.7, W / 2, 1000, 0.85, 0)
m.speech(c, 720, 830, 1, 'YOU ALWAYS...', C['coral'], size=38, tail='right')
m.speech(c, 360, 830, 1, 'NO, YOU...', C['sky'], size=38, tail='left')
buf = np.ndarray((H, W, 4), np.uint8, surf.get_data()); img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
d = ImageDraw.Draw(img); F = '/usr/share/fonts/opentype/inter/'
def ct(txt, y, size, fill, font='Inter-Black.otf'):
    f = ImageFont.truetype(F + font, size); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=max(6, size // 12), stroke_fill=(20, 16, 40))
ct('FAKE ARGUMENTS', 330, 104, (255, 255, 255))
ct('IN YOUR HEAD?', 450, 120, (255, 210, 63))
ct('psychology has a name for it', 600, 50, (255, 255, 255), 'Inter-Bold.otf')
img.save('cover_reel07.png')
w, h = img.size; ch = int(w * 4 / 3); y = (h - ch) // 2
img.crop((0, y, w, y + ch)).resize((300, 400)).save(os.path.join(os.environ.get('PREVIEW_DIR', '/tmp'), 'grid7.png'))
