import cairo, math, json, subprocess, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
PREVIEW = len(sys.argv) > 1  # pass times to dump stills

# ---------- timing ----------
a = json.load(open('align.json'))
ch, st, en = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
text = ''.join(ch)
def t_of(p, start=0): return st[text.find(p, start)]
T = dict(
    s1=t_of('Number one'), ask=t_of('Ask them'), called=t_of("It's called"), helping=t_of('helping you'),
    s2=t_of('Number two'), good=t_of('Good.'), comp=t_of('Competent'), pratfall=t_of("That's the"),
    s3=t_of('Number three'), most=t_of('Most people'), sothey=t_of('so they'),
    s4=t_of('Number four'), soal=t_of('So always'), s5=t_of('Follow for'),
)
DUR = en[-1] + 0.9
SCENES = [0, T['s1'], T['s2'], T['s3'], T['s4'], T['s5'], DUR + 1]

words = []; i = 0
while i < len(ch):
    if ch[i].isspace(): i += 1; continue
    j = i
    while j < len(ch) and not ch[j].isspace(): j += 1
    words.append((text[i:j], st[i], en[j - 1])); i = j
chunks = []; cur = []
for w in words:
    cur.append(w)
    if len(cur) >= 3 or w[0][-1] in '.,?:!':
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

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

# ---------- scenes ----------
def scene0(c, t):
    bg(c, 0, t); lt = t
    person(c, W / 2, 1330, 1.15, C['violet'], t, face='big' if lt > 0.6 else 'o', armL=2.6 + math.sin(t * 6) * 0.15, armR=-2.6 - math.sin(t * 6) * 0.15, blush=True)
    s = pop(t, 0.2, 0.5)
    if s > 0:
        c.save(); c.translate(W / 2, 500); c.scale(s, s); c.rotate(math.sin(t * 2) * 0.05)
        for k in range(12):
            ang = k * math.pi / 6 + t * 0.8
            line(c, math.cos(ang) * 190, math.sin(ang) * 190, math.cos(ang) * 240, math.sin(ang) * 240, 14, C['yellow'])
        for (bx, by, r) in [(-70, -10, 85), (40, -50, 90), (90, 30, 75), (-20, 50, 80), (-100, 50, 60)]:
            circle(c, bx, by, r, C['pink'])
        for k in range(4):
            c.set_line_width(10); c.set_source_rgba(1, 1, 1, 0.55); c.arc(-60 + k * 45, -10 + (k % 2) * 30, 30, 0.2, 2.6); c.stroke()
        c.restore()
        for k in range(6):
            ang = k * 1.05 + t; star(c, W / 2 + math.cos(ang) * 330, 500 + math.sin(ang) * 230, 22, C['yellow'], 0.9, t * 2)
    title_pill(c, t, 0, None, '4 PSYCHOLOGY TRICKS', C['pink'])

def scene1(c, t):
    bg(c, 1, t); lt = t - T['s1']
    title_pill(c, lt, 0, '1', 'BEN FRANKLIN EFFECT', C['coral'])
    ask = t >= T['ask']; give = clamp((t - T['ask'] - 1.0) / 0.9); loved = t >= T['called']
    person(c, 300, 1400, 0.95, C['sky'], t, face='smile', look=12, armR=-1.4 if ask else -0.15, hairstyle=1, skin=C['skin2'])
    person(c, 780, 1400, 0.95, C['coral'], t + 1, face='big' if loved else 'smile', look=-12, flip=True,
           armR=lerp(-0.15, -1.3, eo(give * 3)) if give < 0.7 else -1.3, blush=loved, hairstyle=2, hair=C['hair2'])
    bubble(c, 330, 720, 470, 150, pop(t, T['ask'] + 0.1), 'left', 'Borrow your pen?', 44)
    if give > 0:
        px = lerp(650, 430, eio(give)); py = 1080 + math.sin(give * math.pi) * -80
        c.save(); c.translate(px, py); c.rotate(-0.6 + give * 0.4)
        rrect(c, -70, -11, 140, 22, 11); fill(c, C['yellow']); rrect(c, 40, -11, 30, 22, 8); fill(c, C['ink']); c.restore()
    if loved:
        for k in range(7):
            ht = (t - T['called'] - k * 0.35)
            if ht > 0:
                hy = 820 - ht * 160; a = clamp(1.6 - ht * 0.5)
                heart(c, 780 + math.sin(ht * 2.2 + k * 1.7) * 110 + (k % 3 - 1) * 60, hy + 80, 1.0 + 0.4 * math.sin(k * 2.1), C['pink'], a)
        s = pop(t, T['helping'], 0.5)
        if s > 0:
            c.save(); c.translate(W / 2, 420); c.scale(s, s)
            rrect(c, -260, -40, 520, 80, 40); fill(c, C['white'], 0.25)
            fw = 520 * eo((t - T['helping']) / 2.0); rrect(c, -260, -40, max(fw, 80), 80, 40); fill(c, C['pink'])
            text_c(c, 'LIKES YOU', 0, 0, 40, C['white']); c.restore()

def scene2(c, t):
    bg(c, 2, t); lt = t - T['s2']
    title_pill(c, lt, 0, '2', 'PRATFALL EFFECT', C['mint'])
    # slide screen
    rrect(c, 120, 430, 840, 470, 30); fill(c, C['white'], 0.95)
    for k, hgt in enumerate([120, 190, 260, 340]):
        g = eo((lt - 0.3 - k * 0.15) / 0.6)
        rrect(c, 230 + k * 170, 840 - hgt * g, 110, hgt * g + 1, 14); fill(c, [C['sky'], C['violet'], C['coral'], C['mint']][k])
    oops = t >= T['good'] - 0.9
    spill = clamp((t - (T['good'] - 0.9)) / 0.6)
    person(c, 430, 1360, 0.9, C['mint'], t, face='o' if oops and t < T['comp'] else ('big' if t >= T['comp'] else 'smile'),
           armR=-1.2 if not oops else lerp(-1.2, -2.2, spill), sweat=clamp(spill * 1.5) if oops and t < T['comp'] + 1 else 0, hairstyle=0)
    # coffee cup
    cx, cy = 610, 1050
    c.save(); c.translate(cx, cy); c.rotate(spill * 1.9)
    rrect(c, -40, -55, 80, 100, 14); fill(c, C['white']); rrect(c, -40, -30, 80, 22, 4); fill(c, C['coral'])
    c.restore()
    if spill > 0:
        for k in range(9):
            d = spill * (120 + k * 25); ang = 0.2 + k * 0.17
            circle(c, cx + 60 + math.cos(ang) * d, cy + math.sin(ang) * d * 0.9, 16 - k, hx('8B5A2B'), 0.9)
        c.save(); c.translate(740, 1360); c.scale(1, 0.25); circle(c, 0, 0, 90 * spill, hx('8B5A2B'), 0.8); c.restore()
    # audience heads
    for k, hxp in enumerate([180, 540, 900]):
        circle(c, hxp, 1465, 92, [C['hair1'], C['hair2'], C['ink']][k])
        if t >= T['comp']:
            ht = t - T['comp'] - k * 0.3
            s = pop(t, T['comp'] + k * 0.3)
            if s > 0:
                c.save(); c.translate(hxp, 1310 - min(ht, 1.5) * 40); c.scale(s, s)
                circle(c, 0, 0, 62, C['white']); heart(c, 0, 5, 0.85, C['pink']); c.restore()

def scene3(c, t):
    bg(c, 3, t); lt = t - T['s3']
    title_pill(c, lt, 0, '3', 'THE POWER OF SILENCE', C['sky'])
    talking = t >= T['most']
    person(c, 290, 1400, 0.95, C['yellow'], t, face='flat' if lt > 1.5 else 'smile', look=10, hairstyle=2, skin=C['skin3'])
    person(c, 790, 1400, 0.95, C['violet'], t + 2, flip=True, look=-10,
           face='big' if talking and int(t * 6) % 2 == 0 else ('worried' if lt > 1.5 else 'smile'),
           sweat=clamp((lt - 2.0) / 1.5) if not talking else 0, armR=-1.0 - 0.5 * math.sin(t * 8) if talking else -0.15,
           hairstyle=0, hair=C['hair2'])
    bubble(c, 300, 760, 210, 150, pop(t, T['s3'] + 0.6), 'left', '?', 90)
    if lt > 1.6 and not talking:
        s = pop(t, T['s3'] + 1.6)
        c.save(); c.translate(300, 560); c.scale(s, s)
        circle(c, 0, 0, 80, C['white']); c.set_line_width(10); c.set_source_rgb(*C['ink'])
        ang = (t - T['s3']) * 4; c.move_to(0, 0); c.line_to(math.cos(ang) * 55, math.sin(ang) * 55); c.stroke()
        c.move_to(0, 0); c.line_to(0, -40); c.stroke(); c.restore()
        dots = '.' * (1 + int(t * 3) % 3)
        bubble(c, 790, 760, 230, 140, s, 'right', dots, 80)
    if talking:
        for k in range(6):
            s = pop(t, T['most'] + k * 0.45, 0.3)
            if s > 0:
                bx = 760 + (k % 2) * 60 - 30; by = 850 - k * 100
                c.save(); c.translate(bx, by); c.scale(s, s)
                rrect(c, -200, -45, 400, 90, 45); fill(c, C['white'])
                for q in range(3): line(c, -150 + q * 0, -12 + q * 0, -150 + 300 - q * 80, -12, 0, C['ink'])
                line(c, -150, -12, 120 - (k % 3) * 40, -12, 14, C['ink'], 0.7)
                line(c, -150, 16, 40 + (k % 2) * 60, 16, 14, C['ink'], 0.4)
                c.restore()

def scene4(c, t):
    bg(c, 4, t); lt = t - T['s4']
    title_pill(c, lt, 0, '4', 'PEAK-END RULE', C['yellow'])
    # curve
    def f(x):  # x 0..1 -> y
        return 0.45 + 0.08 * math.sin(x * 9) - 0.42 * math.exp(-((x - 0.35) / 0.07) ** 2) - 0.38 * math.exp(-((x - 0.97) / 0.06) ** 2) * 1.0
    X0, X1, Y0, Y1 = 90, 990, 760, 1420
    prog = eio(lt / 3.6)
    c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    pts = [(X0 + (X1 - X0) * k / 300, Y0 + (Y1 - Y0) * f(k / 300)) for k in range(301)]
    # area fill
    c.move_to(X0, Y1 + 100)
    n = max(2, int(300 * prog))
    for p in pts[:n]: c.line_to(*p)
    c.line_to(pts[n - 1][0], Y1 + 100); c.close_path(); fill(c, C['white'], 0.12)
    c.move_to(*pts[0])
    for p in pts[:n]: c.line_to(*p)
    c.set_source_rgb(*C['white']); c.stroke()
    # rails ties
    for k in range(0, n, 12): circle(c, *pts[k], 7, C['yellow'])
    # cart
    px, py = pts[n - 1]; p2 = pts[max(0, n - 4)]; ang = math.atan2(py - p2[1], px - p2[0]) if n > 4 else 0
    c.save(); c.translate(px, py); c.rotate(ang); c.scale(1.4, 1.4)
    rrect(c, -60, -80, 120, 62, 18); fill(c, C['coral']); circle(c, -35, -12, 16, C['ink']); circle(c, 35, -12, 16, C['ink'])
    circle(c, 0, -110, 32, C['skin1']); circle(c, -10, -115, 5, C['ink']); circle(c, 10, -115, 5, C['ink'])
    line(c, -20, -95, 20, -95, 0, C['ink'])
    line(c, -25, -100, -50, -150 - math.sin(t * 10) * 10, 12, C['skin1']); line(c, 25, -100, 50, -150 + math.sin(t * 10) * 10, 12, C['skin1'])
    c.restore()
    peak = pts[int(0.35 * 300)]; end = pts[int(0.97 * 300)]
    for (pt, lbl, tt) in [(peak, 'PEAK', 0.35), (end, 'END', 0.97)]:
        s = pop(lt, 3.6 * tt * 0.9 + 0.3)
        if s > 0:
            c.save(); c.translate(pt[0], pt[1] - 140); c.scale(s, s)
            star(c, 0, 0, 60, C['yellow'], 1, t); text_c(c, lbl, 0, -95, 48, C['white']); c.restore()
    if t >= T['soal']:
        random.seed(3)
        for k in range(60):
            ct = t - T['soal']; cx0 = end[0] - 100 + random.uniform(-300, 200); vy = random.uniform(-900, -400); vx = random.uniform(-250, 250)
            x = cx0 + vx * ct; y = end[1] - 150 + vy * ct + 900 * ct * ct
            c.save(); c.translate(x, y); c.rotate(ct * random.uniform(3, 9))
            rrect(c, -10, -5, 20, 10, 3); fill(c, random.choice([C['yellow'], C['mint'], C['sky'], C['pink'], C['white']])); c.restore()

def scene5(c, t):
    bg(c, 5, t); lt = t - T['s5']
    s = pop(lt, 0.0, 0.5)
    c.save(); c.translate(W / 2, 900); c.scale(s, s)
    rrect(c, -330, -560, 660, 1120, 80); fill(c, C['ink']); rrect(c, -305, -535, 610, 1070, 62); fill(c, C['white'])
    circle(c, 0, -360, 110, C['violet']); person_mini = None
    text_c(c, '@neuronbites', 0, -200, 52, C['ink'])
    for k, (num, lbl) in enumerate([('120', 'posts'), ('48K', 'followers'), ('1M', 'likes')]):
        text_c(c, num, -200 + k * 200, -100, 44, C['ink']); text_c(c, lbl, -200 + k * 200, -55, 28, C['ink'], False, 0.6)
    tapped = lt > 1.2
    btn = C['white'] if tapped else C['sky']
    rrect(c, -230, 30, 460, 110, 30); fill(c, (0.92, 0.92, 0.95) if tapped else C['sky'])
    text_c(c, 'Following' if tapped else 'Follow', 0, 85, 50, C['ink'] if tapped else C['white'])
    for k in range(6): rrect(c, -270 + (k % 3) * 185, 200 + (k // 3) * 185, 170, 170, 16); fill(c, [C['coral'], C['mint'], C['yellow'], C['sky'], C['pink'], C['violet']][k], 0.85)
    c.restore()
    # finger
    bk = eio((lt - 1.7) / 0.5); fx = lerp(lerp(W / 2 + 400, W / 2 + 60, eio((lt - 0.5) / 0.6)), W / 2 + 500, bk); fy = lerp(lerp(1700, 1010, eio((lt - 0.5) / 0.6)), 1900, bk) + (12 if 1.1 < lt < 1.4 else 0)
    circle(c, fx, fy, 46, C['skin1']); line(c, fx, fy, fx + 70, fy + 260, 92, C['skin1'])
    if tapped:
        r = (lt - 1.2) * 400
        c.set_line_width(8); c.set_source_rgba(*C['yellow'], clamp(1 - (lt - 1.2))); c.arc(W / 2, 985, r, 0, 2 * math.pi); c.stroke()
        sp = pop(lt, 1.5)
        c.save(); c.translate(W / 2 + 290, 330); c.rotate(0.15); c.scale(max(sp, 0.001), max(sp, 0.001))
        rrect(c, -150, -60, 300, 120, 60); fill(c, C['yellow']); text_c(c, 'PART 2', 0, 0, 56, C['ink']); c.restore()
        for k in range(5):
            ht = lt - 1.3 - k * 0.2
            if ht > 0: heart(c, W / 2 - 300 + k * 140, 1500 - ht * 300, 1.0, C['pink'], clamp(1.5 - ht))

SC = [scene0, scene1, scene2, scene3, scene4, scene5]

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
    lines = [parts] if d.textlength(full, font=fCap) < W - 140 else [parts[:2], parts[2:]]
    y = 1610
    age = t - c[0][1]; sc = 1 + 0.08 * max(0, 1 - age / 0.15)
    for ln in lines:
        s = ' '.join(ln); x = (W - d.textlength(s, font=fCap)) / 2
        for w in ln:
            d.text((x, y), w, font=fCap, fill=ACC if w == cur else (255, 255, 255), stroke_width=9, stroke_fill=(20, 16, 40))
            x += d.textlength(w + ' ', font=fCap)
        y += 100

def frame(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    idx = max(k for k in range(6) if SCENES[k] <= t)
    # subtle camera push
    lt = t - SCENES[idx]; z = 1 + 0.03 * eio(lt / 6)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    SC[idx](c, t); c.restore()
    # circular reveal transition from previous scene
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

if PREVIEW:
    for s in sys.argv[1:]:
        frame(float(s)).resize((540, 960)).save(f'/tmp/claude-0/-home-user--/eedeb946-f1d8-5985-8482-23b174c808ae/scratchpad/c_{s}.png')
    sys.exit()

N = int(DUR * FPS)
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', 'cartoon_video.mp4'], stdin=subprocess.PIPE)
for f in range(N):
    p.stdin.write(frame(f / FPS).tobytes())
p.stdin.close(); p.wait()
print('frames', N, 'dur', DUR, 'T', {k: round(v, 2) for k, v in T.items()})
