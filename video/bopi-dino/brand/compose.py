"""Compose avatar.png (800x800) and banner.png (2560x1440) from the Blender renders avatar_raw.png / banner_raw.png."""
from PIL import Image, ImageDraw, ImageFont
import random, math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
F = '../fonts/Fredoka-Bold.ttf'
def font(sz): return ImageFont.truetype(F, sz)
def radial(w, h, c1, c2):
    im = Image.new('RGB', (w, h), c2); d = ImageDraw.Draw(im); R = int(math.hypot(w, h) / 2)
    for r in range(R, 0, -4):
        t = r / R; d.ellipse([w/2-r, h/2-r, w/2+r, h/2+r], fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
    return im
def bubbles(im, n, seed, rmin, rmax):
    random.seed(seed); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(n):
        x = random.randint(0, im.size[0]); y = random.randint(0, im.size[1]); r = random.randint(rmin, rmax)
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, 40), outline=(255, 255, 255, 170), width=max(2, r // 12))
        d.ellipse([x-r*0.55, y-r*0.6, x-r*0.2, y-r*0.3], fill=(255, 255, 255, 190))
    im.alpha_composite(ov); return im
# avatar
bg = radial(800, 800, (255, 226, 90), (255, 140, 40)).convert('RGBA'); bg = bubbles(bg, 10, 1, 18, 45)
bg.alpha_composite(Image.open('avatar_raw.png').convert('RGBA'), (0, 60)); bg.convert('RGB').save('avatar.png')
# banner (safe area for all devices: 1546x423 in the centre)
W, H = 2560, 1440; bg = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(bg)
for y in range(H): t = y / H; d.line([(0, y), (W, y)], fill=(int(90+60*t), int(190+30*t), 255, 255))
bg = bubbles(bg, 40, 2, 20, 70); ImageDraw.Draw(bg).ellipse([-400, 1000, W+400, 2200], fill=(120, 215, 120, 255))
b = Image.open('banner_raw.png').convert('RGBA'); b = b.crop(b.getbbox()); s = 440 / b.size[1]; b = b.resize((int(b.size[0]*s), 440), Image.LANCZOS)
x0, y0 = (W-1546)//2, (H-423)//2; bg.alpha_composite(b, (x0+30, y0-10)); d = ImageDraw.Draw(bg); tx = x0+30+b.size[0]+50
d.text((tx, y0+5), "Bopi Dino", font=font(180), fill=(255, 215, 50), stroke_width=14, stroke_fill=(90, 40, 120))
d.text((tx+6, y0+225), "Kids Songs • New song every day!", font=font(62), fill=(255, 255, 255), stroke_width=8, stroke_fill=(40, 90, 170))
d.text((tx+6, y0+310), "Sing • Dance • Learn good habits", font=font(52), fill=(255, 255, 255), stroke_width=7, stroke_fill=(40, 90, 170))
bg.convert('RGB').save('banner.png'); print('ok')
