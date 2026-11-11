import cairo, math, json, subprocess, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
chunks = []

def load_timing(path='align.json'):
    global chunks
    a = json.load(open(path))
    ch, st, en = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
    text = ''.join(ch)
    words = []; i = 0
    while i < len(ch):
        if ch[i].isspace(): i += 1; continue
        j = i
        while j < len(ch) and not ch[j].isspace(): j += 1
        words.append((text[i:j], st[i], en[j - 1])); i = j
    chunks.clear(); cur = []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 or w[0][-1] in '.,?:!':
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    def t_of(p, start=0): return st[text.find(p, start)]
    return t_of, en[-1] + 0.9
# ---------- palette ----------
def hx(s): s = s.lstrip('#'); return tuple(int(s[k:k + 2], 16) / 255 for k in (0, 2, 4))
C = dict(ink=hx('1A1433'), yellow=hx('FFD23F'), coral=hx('FF6B6B'), mint=hx('3DDC97'), sky=hx('4CC9F0'),
         pink=hx('F72585'), violet=hx('7B5CFF'), white=(1, 1, 1), skin1=hx('F5C6A5'), skin2=hx('C68863'),
         skin3=hx('8D5B3D'), hair1=hx('2B1B17'), hair2=hx('6B3E26'), pants=hx('2E2A5A'))
BG = [(hx('2B1E6B'), hx('6A3FD8')), (hx('0F4C75'), hx('3282B8')), (hx('5B1E5F'), hx('C2457E')),
      (hx('123B3A'), hx('1F8A70')), (hx('3A1C71'), hx('D76D77')), (hx('1A1433'), hx('5B3FD8'))]

# ---------- easing ----------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def pop(t, t0, d=0.4): return max(back((t - t0) / d), 0.001) if t >= t0 else 0.0
def lerp(a, b, x): return a + (b - a) * x

# ---------- primitives ----------
def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()
def fill(c, col, a=1.0): c.set_source_rgba(*col, a); c.fill()
def circle(c, x, y, r, col, a=1.0): c.arc(x, y, r, 0, 2 * math.pi); fill(c, col, a)
def line(c, x1, y1, x2, y2, w, col, a=1.0):
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(w); c.set_source_rgba(*col, a)
    c.move_to(x1, y1); c.line_to(x2, y2); c.stroke()
def heart(c, x, y, s, col, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 30); c.curve_to(-60, -10, -35, -55, 0, -25); c.curve_to(35, -55, 60, -10, 0, 30); c.close_path()
    fill(c, col, a); c.restore()
def star(c, x, y, r, col, a=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45; ang = -math.pi / 2 + k * math.pi / 5
        (c.move_to if k == 0 else c.line_to)(math.cos(ang) * rr, math.sin(ang) * rr)
    c.close_path(); fill(c, col, a); c.restore()
def text_c(c, s, x, y, size, col, bold=True, a=1.0):
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size); e = c.text_extents(s)
    c.move_to(x - e.width / 2 - e.x_bearing, y - e.height / 2 - e.y_bearing); c.set_source_rgba(*col, a); c.show_text(s)
def bubble(c, x, y, w, h, s, tail='left', txt=None, size=46, col=C['white'], tcol=C['ink']):
    if s <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.18); rrect(c, -w / 2 + 8, -h / 2 + 12, w, h, 36); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 36); fill(c, col)
    tx = -w / 4 if tail == 'left' else w / 4
    c.move_to(tx - 26, h / 2 - 2); c.line_to(tx + (-30 if tail == 'left' else 30), h / 2 + 46); c.line_to(tx + 26, h / 2 - 2); c.close_path(); fill(c, col)
    if txt: text_c(c, txt, 0, 0, size, tcol)
    c.restore()

def bg(c, idx, t):
    top, bot = BG[idx]
    g = cairo.LinearGradient(0, 0, W * 0.3, H); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    c.set_source(g); c.paint()
    random.seed(idx * 13)
    for k in range(7):  # soft blobs
        bx = random.uniform(0, W) + math.sin(t * 0.4 + k) * 40; by = random.uniform(0, H) + math.cos(t * 0.3 + k) * 60
        r = random.uniform(180, 380)
        rg = cairo.RadialGradient(bx, by, 0, bx, by, r); rg.add_color_stop_rgba(0, 1, 1, 1, 0.10); rg.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(rg); c.arc(bx, by, r, 0, 2 * math.pi); c.fill()
    for k in range(26):  # drifting dots
        dx = (random.uniform(0, W) + t * random.uniform(8, 25)) % W; dy = (random.uniform(0, H) - t * random.uniform(10, 40)) % H
        circle(c, dx, dy, random.uniform(3, 7), C['white'], 0.18)

# ---------- character ----------
def person(c, x, y, s, shirt, t, skin=None, hair=None, face='smile', look=0, armL=0.15, armR=-0.15,
           blush=False, sweat=0.0, flip=False, hairstyle=0):
    skin = skin or C['skin1']; hair = hair or C['hair1']
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    bob = math.sin(t * 3.2) * 5
    c.save(); c.scale(1, 0.2); circle(c, 0, 0, 110, (0, 0, 0), 0.22); c.restore()
    line(c, -30, -150, -32, -12, 40, C['pants']); line(c, 30, -150, 32, -12, 40, C['pants'])
    circle(c, -38, -8, 24, C['ink']); circle(c, 38, -8, 24, C['ink'])
    c.translate(0, bob)
    # arms behind torso edge
    for side, ang in ((-1, armL), (1, armR)):
        sx, sy = side * 66, -300
        ex, ey = sx + math.sin(ang * side) * 150 * side, sy + math.cos(ang) * 150
        line(c, sx, sy, ex, ey, 36, shirt); circle(c, ex, ey, 22, skin)
    rrect(c, -78, -340, 156, 205, 60); fill(c, shirt)
    c.move_to(-28, -340); c.line_to(0, -300); c.line_to(28, -340); c.close_path(); fill(c, C['white'], 0.85)
    # head
    hy = -440
    circle(c, 0, hy, 92, skin)
    c.save(); c.arc(0, hy, 94, 0, 2 * math.pi); c.clip()
    if hairstyle == 0: circle(c, -8, hy - 70, 95, hair)
    elif hairstyle == 1: rrect(c, -100, hy - 110, 200, 85, 40); fill(c, hair)
    c.restore()
    if hairstyle == 2:  # bun
        circle(c, 0, hy - 105, 38, hair); c.save(); c.arc(0, hy, 94, 0, 2 * math.pi); c.clip(); circle(c, 0, hy - 80, 90, hair); c.restore()
    blink = 0.15 if (t * 1.0) % 3.7 < 0.12 else 1.0
    for ex in (-30, 30):
        c.save(); c.translate(ex + look, hy - 5); c.scale(1, blink); circle(c, 0, 0, 11, C['ink']); c.restore()
    if blush:
        circle(c, -52, hy + 22, 16, C['pink'], 0.35); circle(c, 52, hy + 22, 16, C['pink'], 0.35)
    my = hy + 35; c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgb(*C['ink'])
    if face == 'smile': c.arc(look, my - 12, 26, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    elif face == 'big':
        c.arc(look, my - 8, 30, 0, math.pi); c.close_path(); fill(c, C['ink'])
        c.arc(look, my + 12, 14, math.pi * 1.1, math.pi * 1.9); fill(c, C['coral'])
    elif face == 'o': circle(c, look, my, 14, C['ink'])
    elif face == 'flat': c.move_to(look - 20, my); c.line_to(look + 20, my); c.stroke()
    elif face == 'worried': c.arc(look, my + 18, 24, 1.2 * math.pi, 1.8 * math.pi); c.stroke()
    if sweat > 0:
        c.save(); c.translate(80, hy - 40 + sweat * 30); c.scale(1, 1.3); circle(c, 0, 0, 14, C['sky'], 1 - sweat * 0.5); c.restore()
    c.restore()

def title_pill(c, t, t0, num, label, col):
    s = pop(t, t0 + 0.05, 0.45)
    if s <= 0: return
    c.save(); c.translate(W / 2, 250); c.scale(s, s)
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(58)
    w = c.text_extents(label).width + (150 if num else 80)
    c.set_source_rgba(0, 0, 0, 0.25); rrect(c, -w / 2 + 6, -55 + 10, w, 110, 55); c.fill()
    rrect(c, -w / 2, -55, w, 110, 55); fill(c, C['white'])
    if num:
        circle(c, -w / 2 + 58, 0, 40, col); text_c(c, num, -w / 2 + 58, 0, 44, C['white'])
        text_c(c, label, 45, 0, 58, C['ink'])
    else: text_c(c, label, 0, 0, 58, C['ink'])
    c.restore()

# ---------- captions (PIL) ----------
F = '/usr/share/fonts/opentype/inter/'
fCap = ImageFont.truetype(F + 'Inter-Black.otf', 82)
ACC = (255, 210, 63)
def captions(img, t):
    ck = [c for c in chunks if c[0][1] - 0.05 <= t]
    if not ck or t > ck[-1][-1][2] + 0.6: return
    c = ck[-1]; d = ImageDraw.Draw(img)
    parts = [w[0].upper() for w in c]; spoken = [w for w in c if w[1] <= t]
    cur = spoken[-1][0].upper() if spoken else None
    full = ' '.join(parts)
    lines = []; curl = []
    for p_ in parts:
        if curl and d.textlength(' '.join(curl + [p_]), font=fCap) > W - 140: lines.append(curl); curl = []
        curl.append(p_)
    lines.append(curl)
    y = 1610
    age = t - c[0][1]; sc = 1 + 0.08 * max(0, 1 - age / 0.15)
    for ln in lines:
        s = ' '.join(ln); x = (W - d.textlength(s, font=fCap)) / 2
        for w in ln:
            d.text((x, y), w, font=fCap, fill=ACC if w == cur else (255, 255, 255), stroke_width=9, stroke_fill=(20, 16, 40))
            x += d.textlength(w + ' ', font=fCap)
        y += 100

def frame(t, SCENES, SC, DUR):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    idx = max(k for k in range(len(SC)) if SCENES[k] <= t)
    lt = t - SCENES[idx]; z = 1 + 0.03 * eio(lt / 6)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    SC[idx](c, t); c.restore()
    if idx > 0 and lt < 0.45:
        prev = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); pc = cairo.Context(prev); SC[idx - 1](pc, t)
        r = eio(lt / 0.45) * 1250
        c.save(); c.rectangle(0, 0, W, H); c.arc_negative(W / 2, H / 2, r, 2 * math.pi, 0); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip()
        c.set_source_surface(prev); c.paint(); c.restore()
        c.set_line_width(26); c.set_source_rgb(*C['yellow']); c.arc(W / 2, H / 2, r, 0, 2 * math.pi); c.stroke()
    buf = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    img = Image.fromarray(buf[:, :, [2, 1, 0]].copy())
    captions(img, t)
    d = ImageDraw.Draw(img); d.rectangle([0, H - 12, int(W * t / DUR), H], fill=ACC)
    return img

def run(SCENES, SC, DUR, out='cartoon_video.mp4', preview=None):
    if preview:
        for s in preview:
            frame(float(s), SCENES, SC, DUR).resize((540, 960)).save(f'/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/c_{s}.png')
        return
    N = int(DUR * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(N): p.stdin.write(frame(f / FPS, SCENES, SC, DUR).tobytes())
    p.stdin.close(); p.wait()
