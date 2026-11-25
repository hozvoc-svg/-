"""Cover for ep01 Short: clean frame (no captions) + bold text. -> out/cover.png (1080x1920), out/cover_preview.jpg"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
src = sys.argv[1]
img = Image.open(src).convert('RGB')
img = ImageEnhance.Color(img).enhance(1.15); img = ImageEnhance.Contrast(img).enhance(1.05)
W, H = img.size
# shift the frame down so the title sits above Bopi's eyes; the gap on top is a soft, stretched copy of the wall
D = 300
top = img.crop((0, 0, W, 260)).resize((W, D + 260)).filter(ImageFilter.GaussianBlur(18))
new = Image.new('RGB', (W, H)); new.paste(top, (0, 0))
grad = Image.linear_gradient('L').resize((W, 120))
new.paste(img.crop((0, 0, W, H - D)), (0, D))
new.paste(top.crop((0, D, W, D + 120)), (0, D), Image.eval(grad, lambda v: 255 - v))
img = new
F = os.path.join(HERE, '..', 'fonts', 'Fredoka-Bold.ttf')
d = ImageDraw.Draw(img, 'RGBA')

def text(cx, y, s, size, fill, stroke, sw, rot=0):
    f = ImageFont.truetype(F, size)
    bb = d.textbbox((0, 0), s, font=f, stroke_width=sw)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    layer = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    # drop shadow
    sh = Image.new('RGBA', layer.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.text((30 - bb[0] + 8, 30 - bb[1] + 10), s, font=f, fill=(0, 0, 0, 140), stroke_width=sw, stroke_fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    layer = Image.alpha_composite(layer, sh); ld = ImageDraw.Draw(layer)
    ld.text((30 - bb[0], 30 - bb[1]), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    if rot: layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (int(cx - layer.width / 2), int(y)), layer)

# top title
text(W / 2, 40, 'OH NO!', 230, (255, 255, 255), (200, 30, 30), 16, rot=4)
text(W / 2, 300, 'SUGAR BUGS!', 150, (255, 215, 50), (74, 42, 96), 14, rot=-3)
# bottom badge (above the Shorts UI zone)
f = ImageFont.truetype(F, 78); s = 'BRUSH YOUR TEETH SONG'
bb = d.textbbox((0, 0), s, font=f); w = bb[2] - bb[0]; h = bb[3] - bb[1]
y0 = 1690; pad = 34
d.rounded_rectangle((W / 2 - w / 2 - pad, y0 - 24, W / 2 + w / 2 + pad, y0 + h + 40), 48, fill=(255, 120, 40, 245), outline=(255, 255, 255, 255), width=8)
d.text((W / 2 - w / 2 - bb[0], y0 - bb[1] + 8), s, font=f, fill=(255, 255, 255))
img.save('out/cover.png')
img.resize((540, 960), Image.LANCZOS).save('out/cover_preview.jpg', quality=90)
print('ok')
