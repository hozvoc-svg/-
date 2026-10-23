"""Cozy hand-drawn scene library (hills, cottage, rain, garden, night) on a 1920x1080 canvas."""
import math, random
import cairo
import numpy as np
from scenes import W, H, clamp, ease, prog, rgba, text, text_w, rrect, label

INK = (1.0, 0.98, 0.94)
BG1 = (0.10, 0.12, 0.20)
WARM = (1.0, 0.82, 0.50)
SKIN = (0.98, 0.84, 0.72)
HAIR = (0.25, 0.16, 0.12)
DRESS = (0.86, 0.30, 0.28)
GRAN_TOP = (0.45, 0.42, 0.62)
APRON = (0.96, 0.95, 0.90)
CAT = (0.95, 0.60, 0.28)
WOOD = (0.55, 0.36, 0.22)
LEAF = [(0.24, 0.48, 0.28), (0.30, 0.58, 0.32), (0.38, 0.66, 0.36)]

_r = random.Random(5)
STARS = [(_r.random() * W, _r.random() * H * 0.7, _r.random() * 1.8 + 0.4, _r.random() * 6) for _ in range(260)]
DROPS = [(_r.random(), _r.random(), _r.random()) for _ in range(140)]
FLIES = [(_r.random(), _r.random(), _r.random() * 6) for _ in range(70)]
_grain = None
_grain_buf = None


def grain(c, a=0.05):
    global _grain, _grain_buf
    if _grain is None:
        n = (np.random.default_rng(1).random((H, W)) * 255).astype(np.uint8)
        buf = np.zeros((H, W, 4), np.uint8)
        buf[..., 3] = n // 2
        _grain = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, W, H)
        _grain_buf = buf
    c.set_source_surface(_grain, 0, 0)
    c.paint_with_alpha(a)


def serif(c, s, x, y, size, col=INK, a=1.0, bold=True, italic=False):
    c.select_font_face("DejaVu Serif", cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    e = c.text_extents(s)
    # soft shadow for legibility
    rgba(c, (0, 0, 0), 0.35 * a)
    c.move_to(x - e.x_advance / 2 + 3, y + 3)
    c.show_text(s)
    rgba(c, col, a)
    c.move_to(x - e.x_advance / 2, y)
    c.show_text(s)
    c.new_path()


def mix(a, b, f):
    return tuple(a[i] * (1 - f) + b[i] * f for i in range(3))


# ---------- environment ----------

def sky(c, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


def day_sky(c, dusk=0.0):
    sky(c, mix((0.42, 0.68, 0.92), (0.38, 0.33, 0.55), dusk), mix((0.84, 0.93, 0.98), (1.0, 0.70, 0.50), dusk))


def stars(c, T, a=1.0):
    for sx, sy, r, ph in STARS:
        rgba(c, INK, a * (0.3 + 0.5 * (0.5 + 0.5 * math.sin(T * 1.1 + ph))))
        c.arc(sx, sy, r, 0, 2 * math.pi)
        c.fill()


def cloud(c, x, y, s=1.0, a=0.95, col=(1, 1, 1)):
    for dx, dy, r in [(-70, 10, 42), (-25, -18, 55), (30, -8, 50), (75, 12, 38), (0, 18, 45)]:
        rgba(c, mix(col, (0.80, 0.85, 0.92), 0.25), a)
        c.arc(x + dx * s, y + (dy + 6) * s, r * s, 0, 2 * math.pi)
        c.fill()
    for dx, dy, r in [(-70, 10, 42), (-25, -18, 55), (30, -8, 50), (75, 12, 38), (0, 18, 45)]:
        rgba(c, col, a)
        c.arc(x + dx * s, y + dy * s, r * s * 0.94, 0, 2 * math.pi)
        c.fill()


def clouds(c, T, speed=12, n=6, ymax=380, a=0.95, col=(1, 1, 1)):
    for i in range(n):
        x = (i * 397 + T * speed * (0.6 + 0.15 * (i % 3))) % (W + 500) - 250
        cloud(c, x, 90 + (i * 131) % ymax, 0.8 + 0.25 * (i % 3), a, col)


def hill(c, base, amp, col, phase=0.0, freq=1.0, scroll=0.0):
    c.move_to(-100, H + 100)
    for x in range(-100, W + 121, 20):
        xx = x + scroll
        y = base - amp * (0.6 * math.sin(xx * 0.0021 * freq + phase) + 0.4 * math.sin(xx * 0.0047 * freq + phase * 2))
        c.line_to(x, y)
    c.line_to(W + 120, H + 100)
    c.close_path()
    rgba(c, col)
    c.fill()


def grass(c, T, y0, col=(0.30, 0.55, 0.30), n=90, h=26):
    c.set_line_width(4)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        x = i * (W / n) + (i * 37) % 17
        sway = 8 * math.sin(T * 1.4 + i * 0.5)
        rgba(c, col)
        c.move_to(x, y0)
        c.curve_to(x, y0 - h * 0.5, x + sway * 0.5, y0 - h * 0.8, x + sway, y0 - h)
        c.stroke()


def flowers(c, T, y0, y1, n=60, seed=3):
    r = random.Random(seed)
    for i in range(n):
        x = r.random() * W
        y = y0 + r.random() * (y1 - y0)
        col = r.choice([(1, 1, 1), (1, 0.85, 0.3), (0.95, 0.55, 0.65)])
        sw = 3 * math.sin(T * 1.5 + i)
        for k in range(5):
            ang = k * 2 * math.pi / 5
            rgba(c, col)
            c.arc(x + sw + 5 * math.cos(ang), y + 5 * math.sin(ang), 4, 0, 2 * math.pi)
            c.fill()
        rgba(c, (1, 0.8, 0.2))
        c.arc(x + sw, y, 3, 0, 2 * math.pi)
        c.fill()


def big_tree(c, x, y, s, T, night=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    trunk = mix((0.42, 0.28, 0.18), (0.08, 0.08, 0.12), night)
    rgba(c, trunk)
    c.move_to(-40, 0); c.curve_to(-30, -120, -35, -220, -20, -300); c.line_to(20, -300)
    c.curve_to(35, -220, 30, -120, 40, 0); c.close_path(); c.fill()
    line_w = 18
    c.set_line_width(line_w); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for bx, by in [(-140, -330), (150, -320), (0, -400)]:
        c.move_to(0, -250); c.line_to(bx, by); c.stroke()
    sway = 6 * math.sin(T * 0.6)
    blobs = [(-160, -360, 110), (160, -350, 115), (0, -440, 130), (-80, -480, 100), (90, -470, 105),
             (-230, -300, 80), (230, -290, 85), (0, -330, 110)]
    for k, cols in enumerate(LEAF):
        for i, (bx, by, r) in enumerate(blobs):
            off = (2 - k) * 10
            rgba(c, mix(cols, (0.05, 0.08, 0.14), night))
            c.arc(bx + sway * (1 + i % 2) * 0.5 - off * 0.3, by + off, r * (1 - k * 0.12), 0, 2 * math.pi)
            c.fill()
    c.restore()


def house(c, x, y, s=1.0, lit=0.0, night=0.0, T=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    wall = mix((0.97, 0.95, 0.90), (0.20, 0.22, 0.32), night)
    roof = mix((0.80, 0.25, 0.20), (0.22, 0.10, 0.12), night)
    # chimney + smoke
    rgba(c, mix((0.55, 0.30, 0.25), (0.12, 0.08, 0.1), night))
    c.rectangle(90, -250, 40, 80); c.fill()
    for k in range(5):
        f = ((T * 0.25 + k * 0.2) % 1.0)
        rgba(c, (0.9, 0.9, 0.92), 0.5 * (1 - f) * (1 - night * 0.6))
        c.arc(110 + 30 * f + 10 * math.sin(T + k), -260 - 160 * f, 14 + 18 * f, 0, 2 * math.pi); c.fill()
    rgba(c, wall)
    c.rectangle(-180, -160, 360, 160); c.fill()
    rgba(c, roof)
    c.move_to(-215, -150); c.line_to(0, -290); c.line_to(215, -150); c.close_path(); c.fill()
    win = mix((0.60, 0.78, 0.92), WARM, max(lit, night * 0.0))
    for wx in (-130, 60):
        rgba(c, mix(win, WARM, lit))
        c.rectangle(wx, -120, 70, 60); c.fill()
        if lit:
            g = cairo.RadialGradient(wx + 35, -90, 5, wx + 35, -90, 150)
            g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.45 * lit)
            g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
            c.set_source(g); c.arc(wx + 35, -90, 150, 0, 2 * math.pi); c.fill()
        rgba(c, mix((0.25, 0.55, 0.35), (0.08, 0.15, 0.12), night))
        c.rectangle(wx - 22, -124, 18, 68); c.rectangle(wx + 74, -124, 18, 68); c.fill()
    rgba(c, mix(WOOD, (0.1, 0.07, 0.06), night))
    rrect(c, -40, -100, 70, 100, 30); c.fill()
    c.restore()


def girl(c, x, y, s=1.0, phase=None, face=1, arm=None, sit=False):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    sw = 0 if phase is None else math.sin(phase)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if not sit:
        c.set_line_width(9); rgba(c, SKIN)
        for sg in (1, -1):
            c.move_to(sg * 10, -50); c.line_to(sg * 10 + sg * 0 + 14 * sw * sg, 0); c.stroke()
    else:
        c.set_line_width(9); rgba(c, SKIN)
        c.move_to(0, -50); c.line_to(40, -50); c.line_to(40, -10); c.stroke()
    rgba(c, DRESS)
    c.move_to(-14, -120); c.line_to(14, -120); c.line_to(34, -46); c.line_to(-34, -46); c.close_path(); c.fill()
    c.set_line_width(8); rgba(c, SKIN)
    a = arm if arm is not None else 0.3 * sw
    c.move_to(10, -112); c.line_to(10 + 34 * math.sin(0.4 + a), -112 + 34 * math.cos(0.4 + a)); c.stroke()
    c.move_to(-10, -112); c.line_to(-10 - 34 * math.sin(0.4 - a), -112 + 34 * math.cos(0.4 - a)); c.stroke()
    rgba(c, HAIR); c.arc(0, -146, 30, 0, 2 * math.pi); c.fill()
    rgba(c, SKIN); c.arc(6, -142, 23, 0, 2 * math.pi); c.fill()
    rgba(c, HAIR)
    c.arc(0, -150, 30, math.pi, 2 * math.pi); c.fill()
    c.rectangle(-30, -152, 16, 34); c.fill()
    rgba(c, (0.95, 0.55, 0.55), 0.6); c.arc(18, -134, 5, 0, 2 * math.pi); c.fill()
    rgba(c, (0.2, 0.15, 0.15)); c.arc(16, -144, 3, 0, 2 * math.pi); c.fill()
    c.restore()


def grandma(c, x, y, s=1.0, face=1, sit=False, knit=None):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if not sit:
        c.set_line_width(11); rgba(c, (0.35, 0.3, 0.3))
        for sg in (1, -1):
            c.move_to(sg * 14, -60); c.line_to(sg * 14, 0); c.stroke()
    rgba(c, GRAN_TOP)
    c.move_to(-26, -160); c.line_to(26, -160); c.line_to(44, -55); c.line_to(-44, -55); c.close_path(); c.fill()
    rgba(c, APRON)
    c.move_to(-10, -130); c.line_to(22, -130); c.line_to(34, -60); c.line_to(-14, -60); c.close_path(); c.fill()
    c.set_line_width(10); rgba(c, GRAN_TOP)
    k = 0 if knit is None else 0.15 * math.sin(knit)
    c.move_to(14, -150); c.line_to(44, -110 + 10 * k); c.stroke()
    rgba(c, (0.85, 0.85, 0.88)); c.arc(0, -190, 31, 0, 2 * math.pi); c.fill()
    rgba(c, SKIN); c.arc(6, -186, 25, 0, 2 * math.pi); c.fill()
    rgba(c, (0.85, 0.85, 0.88)); c.arc(-22, -214, 15, 0, 2 * math.pi); c.fill()
    c.arc(0, -196, 30, math.pi * 1.05, math.pi * 1.9); c.fill()
    c.set_line_width(3); rgba(c, (0.2, 0.15, 0.15))
    c.arc(17, -188, 4, math.pi * 0.1, math.pi * 0.9); c.stroke()
    rgba(c, (0.95, 0.55, 0.55), 0.6); c.arc(22, -176, 5, 0, 2 * math.pi); c.fill()
    if knit is not None:
        rgba(c, (0.85, 0.35, 0.40)); c.arc(48, -110, 16, 0, 2 * math.pi); c.fill()
        c.set_line_width(3); rgba(c, (0.9, 0.85, 0.6))
        c.move_to(40, -130 + 6 * math.sin(knit * 3)); c.line_to(62, -95); c.stroke()
    c.restore()


def cat(c, x, y, s=1.0, T=0.0, sleep=True, walk=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, CAT)
    c.save(); c.scale(1, 0.62); c.arc(0, -50, 60, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
    tw = 10 * math.sin(T * 1.2)
    c.move_to(-50, -15); c.curve_to(-90, -10, -95 + tw, -60, -70 + tw, -70); c.stroke()
    hx, hy = 52, -58
    c.arc(hx, hy, 30, 0, 2 * math.pi); c.fill()
    for sg in (-1, 1):
        c.move_to(hx + sg * 24, hy - 14); c.line_to(hx + sg * 16, hy - 44); c.line_to(hx + sg * 2, hy - 26); c.close_path(); c.fill()
    rgba(c, (0.85, 0.48, 0.20))
    for k in range(3):
        c.set_line_width(5); c.move_to(-20 + k * 20, -82); c.line_to(-14 + k * 20, -60); c.stroke()
    rgba(c, (0.3, 0.2, 0.15)); c.set_line_width(3)
    if sleep:
        for sg in (-1, 1):
            c.arc(hx + sg * 11, hy - 2, 6, 0.2, math.pi - 0.2); c.stroke()
    else:
        for sg in (-1, 1):
            c.arc(hx + sg * 11, hy - 4, 4, 0, 2 * math.pi); c.fill()
    c.restore()


def window_frame(c, x, y, w, h, col=(0.95, 0.93, 0.88), round_top=False):
    c.set_line_width(18)
    rgba(c, col)
    if round_top:
        c.arc(x + w / 2, y + w / 2, w / 2, 0, 2 * math.pi)
        c.stroke()
        c.set_line_width(8)
        c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + w); c.stroke()
        c.move_to(x, y + w / 2); c.line_to(x + w, y + w / 2); c.stroke()
        return
    c.rectangle(x, y, w, h); c.stroke()
    c.set_line_width(10)
    c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + h); c.stroke()
    c.move_to(x, y + h / 2); c.line_to(x + w, y + h / 2); c.stroke()


def rain_lines(c, T, x, y, w, h, amount=1.0, a=0.45):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_line_width(2)
    n = int(160 * amount)
    for i in range(n):
        rx = (i * 97.3) % 1
        ry = (i * 0.618) % 1
        px = x + rx * w + ((T * 120 + i * 13) % 60)
        py = y + ((ry * h + T * 900 * (0.8 + 0.4 * rx)) % (h + 60)) - 60
        rgba(c, (0.85, 0.90, 1.0), a)
        c.move_to(px, py); c.line_to(px - 6, py + 34); c.stroke()
    c.restore()


def glass_drops(c, T, x, y, w, h, amount=1.0):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    n = int(len(DROPS) * amount)
    for i, (rx, ry, sp) in enumerate(DROPS[:n]):
        px = x + rx * w
        fall = ((ry + T * 0.05 * (0.3 + sp)) % 1.2) - 0.1
        py = y + fall * h
        rgba(c, (0.92, 0.96, 1.0), 0.20)
        c.set_line_width(4)
        c.move_to(px, py - 50 * sp); c.line_to(px, py); c.stroke()
        rgba(c, (0.95, 0.98, 1.0), 0.55)
        c.arc(px, py, 4 + 4 * sp, 0, 2 * math.pi); c.fill()
    c.restore()


def steam(c, x, y, T, a=0.5, s=1.0):
    c.set_line_width(6 * s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(3):
        f = (T * 0.4 + k / 3) % 1
        rgba(c, (1, 1, 1), a * math.sin(f * math.pi))
        bx = x + (k - 1) * 18 * s
        c.move_to(bx, y - 10 * s - f * 40 * s)
        c.curve_to(bx + 12 * s, y - 30 * s - f * 60 * s, bx - 12 * s, y - 50 * s - f * 70 * s, bx + 6 * s, y - 70 * s - f * 80 * s)
        c.stroke()


def glow(c, x, y, r, col=WARM, a=0.5):
    g = cairo.RadialGradient(x, y, 5, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def fireflies(c, T, x0, y0, w, h, n=60, a=1.0):
    for i, (rx, ry, ph) in enumerate(FLIES[:n]):
        x = x0 + (rx * w + 40 * math.sin(T * 0.3 + ph)) % w
        y = y0 + (ry * h + 25 * math.sin(T * 0.4 + ph * 2))
        b = a * clamp(0.5 + 0.8 * math.sin(T * 1.3 + ph * 3))
        glow(c, x, y, 26, (0.85, 1.0, 0.45), 0.5 * b)
        rgba(c, (0.95, 1.0, 0.7), b)
        c.arc(x, y, 3.5, 0, 2 * math.pi); c.fill()


def interior(c, wall=(0.93, 0.80, 0.62), floor=(0.62, 0.42, 0.28), dim=0.0):
    sky(c, mix(wall, (0.15, 0.15, 0.25), dim), mix(mix(wall, (0.8, 0.6, 0.45), 0.3), (0.12, 0.12, 0.2), dim))
    rgba(c, mix(floor, (0.1, 0.08, 0.1), dim))
    c.rectangle(-400, 860, W + 800, 600); c.fill()
    for i in range(0, W + 200, 160):
        rgba(c, (0, 0, 0), 0.08)
        c.rectangle(i, 860, 4, 300); c.fill()


def jars(c, x, y, n=6):
    cols = [(0.85, 0.20, 0.25), (0.95, 0.55, 0.15), (0.45, 0.15, 0.40), (0.95, 0.75, 0.20), (0.75, 0.25, 0.30), (0.40, 0.55, 0.20)]
    rgba(c, WOOD); c.rectangle(x - 20, y, n * 85 + 20, 18); c.fill()
    for i in range(n):
        jx = x + i * 85
        rgba(c, cols[i % 6], 0.9); rrect(c, jx, y - 80, 60, 80, 12); c.fill()
        rgba(c, (1, 1, 1), 0.3); c.rectangle(jx + 10, y - 66, 8, 50); c.fill()
        rgba(c, (0.95, 0.92, 0.85)); c.rectangle(jx - 3, y - 92, 66, 16); c.fill()


def table(c, x, y, w):
    rgba(c, WOOD); c.rectangle(x, y, w, 24); c.fill()
    rgba(c, mix(WOOD, (0, 0, 0), 0.25))
    c.rectangle(x + 20, y + 24, 20, 860 + 60 - y); c.rectangle(x + w - 40, y + 24, 20, 860 + 60 - y); c.fill()


def chair(c, x, y):
    rgba(c, mix(WOOD, (0, 0, 0), 0.1))
    c.rectangle(x - 60, y, 120, 16); c.rectangle(x - 60, y - 140, 14, 140)
    c.rectangle(x - 55, y + 16, 12, 120); c.rectangle(x + 45, y + 16, 12, 120); c.fill()


def stove(c, x, y):
    rgba(c, (0.25, 0.25, 0.28)); rrect(c, x, y - 200, 220, 200, 10); c.fill()
    rgba(c, (0.95, 0.55, 0.2), 0.8); c.rectangle(x + 60, y - 110, 100, 50); c.fill()
    rgba(c, (0.35, 0.35, 0.4)); c.rectangle(x - 10, y - 214, 240, 18); c.fill()


def kettle(c, x, y):
    rgba(c, (0.75, 0.30, 0.25)); c.save(); c.scale(1, 0.8); c.arc(x, y / 0.8 - 40, 45, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_line_width(8); c.arc(x, y - 70, 30, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.move_to(x + 38, y - 40); c.line_to(x + 75, y - 70); c.stroke()


# ---------- scenes ----------

def sc_title(c, t, d, T, a):
    day_sky(c, 0.15)
    clouds(c, T)
    hill(c, 720, 50, (0.55, 0.75, 0.50), 1.0)
    hill(c, 820, 40, (0.42, 0.66, 0.40), 2.5)
    big_tree(c, 1250, 760, 1.0, T)
    house(c, 1180, 790, 0.9, T=T)
    hill(c, 930, 25, (0.34, 0.58, 0.34), 4.0)
    flowers(c, T, 900, 1060)
    ap = prog(t, 0.5, 2.0)
    rgba(c, (0.12, 0.10, 0.18), 0.45 * ap)
    rrect(c, 120, 220, 1000, 350, 40)
    c.fill()
    serif(c, "A Rainy Summer", 620, 330, 92, INK, ap)
    serif(c, "at Grandma's Hill House", 620, 440, 64, INK, ap)
    serif(c, "a cozy bedtime story", 620, 520, 40, (1, 0.93, 0.75), prog(t, 1.5, 3.0), bold=False, italic=True)


def sc_train(c, t, d, T, a):
    ev = a.get("evening", 0.0) + 0.25 * prog(t, 0, d) * a.get("evening", 0)
    day_sky(c, ev)
    clouds(c, T, speed=6)
    hill(c, 640, 60, mix((0.60, 0.76, 0.58), (0.55, 0.50, 0.55), ev), 1.0, scroll=T * 20)
    hill(c, 760, 50, mix((0.48, 0.70, 0.42), (0.45, 0.42, 0.45), ev), 2.0, scroll=T * 60)
    # river glint
    rgba(c, (0.70, 0.85, 0.98), 0.8)
    rx = (1400 - T * 60) % (W + 600) - 300
    c.save(); c.scale(1, 0.25); c.arc(rx, 790 / 0.25, 160, 0, 2 * math.pi); c.restore(); c.fill()
    # train
    ty = 830
    for k in range(3):
        x = 520 + k * 300
        rgba(c, (0.85, 0.28, 0.25)); rrect(c, x, ty - 120, 280, 110, 18); c.fill()
        rgba(c, (0.98, 0.94, 0.85)); c.rectangle(x, ty - 70, 280, 18); c.fill()
        for wnd in range(4):
            rgba(c, (0.75, 0.88, 0.98) if not (k == 1 and wnd == 1) else (1.0, 0.85, 0.5))
            rrect(c, x + 20 + wnd * 64, ty - 108, 48, 34, 6); c.fill()
        for wh in (50, 230):
            rgba(c, (0.2, 0.2, 0.22)); c.arc(x + wh, ty - 6, 18, 0, 2 * math.pi); c.fill()
    rgba(c, (0.45, 0.40, 0.38)); c.rectangle(-100, ty + 10, W + 200, 10); c.fill()
    # front hill and poles scrolling fast
    hill(c, 960, 30, mix((0.36, 0.60, 0.34), (0.32, 0.36, 0.38), ev), 3.0, scroll=T * 220)
    for k in range(6):
        px = (k * 420 - T * 260) % (W + 400) - 200
        rgba(c, (0.35, 0.25, 0.20)); c.rectangle(px, 640, 12, 360); c.fill()
        c.rectangle(px - 30, 660, 72, 8); c.fill()
    grass(c, T, 1000, n=70)


def sc_busstop(c, t, d, T, a):
    day_sky(c, 0.1)
    clouds(c, T)
    hill(c, 640, 70, (0.55, 0.74, 0.52), 0.5)
    rgba(c, (0.62, 0.60, 0.58))
    c.move_to(-100, 900); c.line_to(W + 100, 900); c.line_to(W + 100, 1000); c.line_to(-100, 1000); c.fill()
    for side_y in (880, 1040):
        for k in range(30):
            rgba(c, (0.25, 0.48, 0.28)); c.arc(k * 70, side_y, 52, 0, 2 * math.pi); c.fill()
        r = random.Random(side_y)
        for k in range(40):
            rgba(c, (0.98, 0.65, 0.75)); c.arc(r.random() * W, side_y - 30 + r.random() * 40, 7, 0, 2 * math.pi); c.fill()
    bx = -500 + 1700 * prog(t, 0.5, d * 0.75)
    rgba(c, (0.30, 0.50, 0.80)); rrect(c, bx, 760, 420, 170, 24); c.fill()
    rgba(c, (0.85, 0.93, 1.0))
    for wnd in range(5):
        rrect(c, bx + 20 + wnd * 78, 780, 62, 60, 8); c.fill()
    rgba(c, (0.2, 0.2, 0.22))
    for wh in (80, 340):
        c.arc(bx + wh, 935, 30, 0, 2 * math.pi); c.fill()
    rgba(c, (0.4, 0.4, 0.4)); c.rectangle(1500, 700, 10, 200); c.fill()
    rgba(c, (0.95, 0.85, 0.30)); c.arc(1505, 690, 34, 0, 2 * math.pi); c.fill()
    if t > d * 0.8:
        girl(c, bx + 470, 960, 0.9, phase=None)


def sc_path(c, t, d, T, a):
    day_sky(c, 0.2)
    clouds(c, T)
    hill(c, 500, 40, (0.55, 0.74, 0.52), 1.5)
    c.move_to(-100, H + 100); c.line_to(-100, 900); c.curve_to(600, 820, 1100, 420, W + 100, 360)
    c.line_to(W + 100, H + 100); c.close_path()
    rgba(c, (0.45, 0.70, 0.40)); c.fill()
    c.set_line_width(70); rgba(c, (0.86, 0.78, 0.60))
    c.move_to(200, H + 50); c.curve_to(700, 900, 1100, 700, 1600, 420); c.stroke()
    flowers(c, T, 700, 1060, 90)
    house(c, 1720, 420, 0.55, T=T)
    p = prog(t, 0, d)
    # point on the path bezier
    def bez(u):
        pts = [(200, H + 50), (700, 900), (1100, 700), (1600, 420)]
        x = sum(cf * pt[0] for cf, pt in zip([(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3], pts))
        y = sum(cf * pt[1] for cf, pt in zip([(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3], pts))
        return x, y
    gx, gy = bez(0.15 + 0.45 * p)
    girl(c, gx, gy, 0.95, phase=T * 5)
    rgba(c, (0.95, 0.80, 0.25)); rrect(c, gx - 75, gy - 60, 46, 56, 8); c.fill()
    grass(c, T, 1080, n=80, h=40)


def chicken(c, x, y, s, T, k):
    peck = max(0.0, math.sin(T * 2.2 + k * 1.7)) ** 6
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.62, 0.38, 0.22)); c.save(); c.scale(1.25, 1); c.arc(0, -40, 34, 0, 2 * math.pi); c.restore(); c.fill()
    c.move_to(-40, -50); c.line_to(-62, -82); c.line_to(-30, -66); c.fill()
    hx, hy = 34, -72 + 34 * peck
    c.arc(hx, hy, 18, 0, 2 * math.pi); c.fill()
    rgba(c, (0.90, 0.20, 0.20)); c.arc(hx, hy - 18, 7, 0, 2 * math.pi); c.fill()
    rgba(c, (0.98, 0.75, 0.20)); c.move_to(hx + 16, hy - 4); c.line_to(hx + 30, hy + 2); c.line_to(hx + 16, hy + 6); c.fill()
    c.set_line_width(4); c.move_to(-8, -8); c.line_to(-8, 0); c.move_to(10, -8); c.line_to(10, 0); c.stroke()
    c.restore()


def mist(c, T, a=0.5):
    for k in range(4):
        y = 640 + k * 90
        x = (T * (8 + k * 4)) % 400 - 200
        g = cairo.LinearGradient(0, y - 60, 0, y + 60)
        g.add_color_stop_rgba(0, 1, 1, 1, 0)
        g.add_color_stop_rgba(0.5, 1, 1, 1, a * (0.8 - k * 0.15))
        g.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(g); c.rectangle(x - 200, y - 60, W + 600, 120); c.fill()


def sc_hill_house(c, t, d, T, a):
    if a.get("morning"):
        sky(c, (0.62, 0.74, 0.92), (1.0, 0.86, 0.74))
        glow(c, 300, 600, 500, (1, 0.85, 0.6), 0.6)
        clouds(c, T, speed=5, col=(1, 0.95, 0.92))
    else:
        day_sky(c, 0.1)
        clouds(c, T)
    hill(c, 700, 40, (0.58, 0.76, 0.54), 0.3)
    c.move_to(-100, H + 100); c.line_to(-100, 900); c.curve_to(500, 760, 1300, 740, W + 100, 860)
    c.line_to(W + 100, H + 100); c.close_path(); rgba(c, (0.44, 0.68, 0.40)); c.fill()
    big_tree(c, 1060, 800, 1.5, T)
    house(c, 960, 840, 1.25, T=T)
    if a.get("morning"):
        mist(c, T, 0.45 * (1 - 0.6 * prog(t, 0, d)))
        if a.get("chickens"):
            for k, (cx, cy) in enumerate([(1350, 990), (1500, 1020), (1620, 970), (1430, 1060), (1720, 1040)]):
                chicken(c, cx, cy, 0.9, T, k)
            grandma(c, 1220, 1000, 1.3, face=1)
            girl(c, 1820, 1060, 1.25, face=-1)
        flowers(c, T, 920, 1070, 70)
        grass(c, T, 1080, n=80, h=36)
        return
    if t > d * 0.55:
        grandma(c, 925, 840, 0.8 * prog(t, d * 0.55, d * 0.65) + 0.001)
    girl(c, 600, 960, 1.0, face=1)
    flowers(c, T, 920, 1070, 70)
    grass(c, T, 1080, n=80, h=36)


def kitchen_base(c, T, night=0.0):
    interior(c, dim=night * 0.4)
    wx, wy = 760, 180
    c.save(); c.rectangle(wx, wy, 420, 320); c.clip()
    if night:
        sky(c, (0.10, 0.14, 0.30), (0.25, 0.25, 0.45)); stars(c, T, 0.8)
    else:
        day_sky(c, 0.0); clouds(c, T, speed=8, n=3, ymax=150)
        hill(c, 450, 30, (0.45, 0.70, 0.42), 1.0)
    c.restore()
    window_frame(c, wx, wy, 420, 320)
    jars(c, 140, 360, 6)
    jars(c, 1330, 360, 5)
    stove(c, 140, 860)
    kettle(c, 300, 646)
    table(c, 820, 700, 640)


def sc_kitchen(c, t, d, T, a):
    kitchen_base(c, T)
    rgba(c, (0.80, 0.55, 0.25)); c.save(); c.scale(1, 0.55); c.arc(1030, 680 / 0.55, 70, math.pi, 2 * math.pi); c.restore(); c.fill()
    if a.get("steam"):
        steam(c, 300, 560, T, 0.6)
        for x in (980, 1260):
            rgba(c, (0.95, 0.95, 1.0)); c.rectangle(x - 22, 655, 44, 45); c.fill()
            steam(c, x, 650, T + x, 0.5, 0.6)
        grandma(c, 1390, 900, 1.4, face=-1)
        girl(c, 900, 900, 1.35)
    else:
        grandma(c, 1500, 900, 1.45, face=-1)
        girl(c, 720, 900, 1.35)
    chair(c, 560, 700)
    cat(c, 560, 700, 0.9, T)
    glow(c, 970, 340, 700, (1, 0.9, 0.7), 0.25)


def sc_rain_window(c, t, d, T, a):
    amt = prog(t, 0, d * 0.7) if a.get("start") else 1.0
    interior(c, wall=(0.78, 0.70, 0.62), dim=0.3)
    wx, wy, ww, wh = 460, 110, 1000, 700
    c.save(); c.rectangle(wx, wy, ww, wh); c.clip()
    sky(c, mix((0.55, 0.72, 0.90), (0.55, 0.60, 0.68), amt), mix((0.80, 0.88, 0.95), (0.72, 0.76, 0.80), amt))
    clouds(c, T, speed=5, n=5, col=mix((1, 1, 1), (0.82, 0.84, 0.88), amt))
    hill(c, 760, 30, mix((0.45, 0.68, 0.42), (0.38, 0.52, 0.42), amt), 1.0)
    big_tree(c, 1150, 860, 1.1, T * (1 + amt))
    rain_lines(c, T, wx, wy, ww, wh, amt, 0.5)
    c.restore()
    glass_drops(c, T, wx, wy, ww, wh, amt)
    window_frame(c, wx, wy, ww, wh)
    rgba(c, (0.95, 0.92, 0.86)); c.rectangle(wx - 60, wy + wh, ww + 120, 40); c.fill()
    rgba(c, (0.75, 0.40, 0.28)); c.move_to(560, 810); c.line_to(640, 810); c.line_to(625, 740); c.line_to(575, 740); c.fill()
    for k in range(5):
        rgba(c, LEAF[k % 3]); c.save(); c.translate(600 + (k - 2) * 18, 720); c.rotate((k - 2) * 0.35 + 0.05 * math.sin(T))
        c.scale(0.5, 1); c.arc(0, -30, 30, 0, 2 * math.pi); c.restore(); c.fill()
    rgba(c, (0.95, 0.95, 1.0)); c.rectangle(1280, 760, 60, 50); c.fill()
    steam(c, 1310, 750, T, 0.55, 0.8)


def sc_rain_room(c, t, d, T, a):
    lamp = prog(t, 0.5, 3.0) if a.get("lamp") else 0.0
    interior(c, wall=(0.70, 0.66, 0.66), dim=0.35)
    wx, wy, ww, wh = 260, 160, 620, 520
    c.save(); c.rectangle(wx, wy, ww, wh); c.clip()
    sky(c, (0.55, 0.60, 0.68), (0.72, 0.76, 0.80))
    big_tree(c, 650, 900, 0.9, T * 2)
    rain_lines(c, T, wx, wy, ww, wh, 1.0, 0.5)
    c.restore()
    glass_drops(c, T, wx, wy, ww, wh, 0.7)
    window_frame(c, wx, wy, ww, wh)
    rgba(c, (0.92, 0.90, 0.85)); c.rectangle(220, 680, 700, 40); c.fill()
    girl(c, 480, 680, 1.0, sit=True)
    rgba(c, (0.55, 0.65, 0.85), 0.9); c.move_to(420, 520); c.curve_to(380, 600, 400, 670, 430, 680)
    c.line_to(560, 680); c.curve_to(560, 620, 540, 560, 500, 520); c.close_path(); c.fill()
    cat(c, 680, 680, 0.75, T)
    # armchair + grandma
    rgba(c, (0.55, 0.30, 0.30)); rrect(c, 1250, 560, 340, 330, 50); c.fill()
    rgba(c, (0.65, 0.38, 0.36)); rrect(c, 1290, 700, 260, 120, 20); c.fill()
    grandma(c, 1420, 760, 1.05, face=-1, sit=True, knit=T * 2)
    # lamp
    rgba(c, (0.3, 0.25, 0.2)); c.rectangle(1680, 420, 10, 460); c.fill()
    rgba(c, (0.95, 0.85, 0.6)); c.move_to(1620, 430); c.line_to(1750, 430); c.line_to(1715, 340); c.line_to(1655, 340); c.fill()
    if lamp:
        glow(c, 1685, 420, 700, WARM, 0.45 * lamp)
    rgba(c, (0.95, 0.95, 1.0)); c.rectangle(1130, 760, 50, 40); c.fill()
    steam(c, 1155, 755, T, 0.5, 0.7)
    rgba(c, WOOD); c.rectangle(1080, 800, 160, 16); c.rectangle(1150, 816, 16, 60); c.fill()


def sc_garden(c, t, d, T, a):
    sky(c, (0.50, 0.70, 0.92), (1.0, 0.88, 0.65))
    clouds(c, T, speed=6, col=(1, 0.97, 0.92))
    glow(c, 1600, 260, 600, (1, 0.9, 0.6), 0.5)
    hill(c, 640, 40, (0.55, 0.72, 0.48), 2.0)
    rgba(c, (0.45, 0.66, 0.38)); c.rectangle(-400, 680, W + 800, 600); c.fill()
    # beds
    for row in range(3):
        y = 760 + row * 110
        rgba(c, (0.45, 0.30, 0.22)); rrect(c, 120, y, 1100, 60, 20); c.fill()
        for k in range(8):
            x = 180 + k * 135
            sw = 4 * math.sin(T * 1.3 + k + row)
            rgba(c, LEAF[(k + row) % 3])
            c.arc(x + sw, y - 20, 34, 0, 2 * math.pi); c.fill()
            if row == 0:
                for j in range(3):
                    rgba(c, (0.90, 0.20, 0.18)); c.arc(x - 14 + j * 14 + sw, y - 10 + (j % 2) * 10, 10, 0, 2 * math.pi); c.fill()
    # sunflowers
    for k in range(4):
        x = 1350 + k * 140
        sw = 10 * math.sin(T * 0.9 + k)
        c.set_line_width(10); rgba(c, (0.30, 0.55, 0.28))
        c.move_to(x, 900); c.curve_to(x, 700, x + sw, 600, x + sw, 480 + k * 20); c.stroke()
        for p in range(12):
            ang = p * math.pi / 6
            rgba(c, (1.0, 0.80, 0.15)); c.arc(x + sw + 34 * math.cos(ang), 480 + k * 20 + 34 * math.sin(ang), 16, 0, 2 * math.pi); c.fill()
        rgba(c, (0.45, 0.28, 0.12)); c.arc(x + sw, 480 + k * 20, 26, 0, 2 * math.pi); c.fill()
    if a.get("puddles") or a.get("basket"):
        for px, py, r in [(400, 1010, 120), (900, 1040, 90), (1500, 1000, 150)]:
            c.save(); c.translate(px, py); c.scale(1, 0.22)
            g = cairo.LinearGradient(0, -r, 0, r)
            g.add_color_stop_rgb(0, 0.55, 0.75, 0.95); g.add_color_stop_rgb(1, 0.85, 0.92, 1.0)
            c.set_source(g); c.arc(0, 0, r, 0, 2 * math.pi); c.fill(); c.restore()
            rgba(c, (1, 1, 1), 0.8); c.arc(px + r * 0.3, py - 4, 16, 0, 2 * math.pi); c.fill()
    if a.get("butterflies"):
        for k in range(3):
            bx = 600 + 300 * k + 120 * math.sin(T * 0.5 + k)
            by = 560 + 60 * math.sin(T * 0.8 + k * 2)
            fl = abs(math.sin(T * 9 + k))
            rgba(c, [(1, 0.75, 0.3), (0.95, 0.95, 1), (0.7, 0.6, 1)][k])
            for sg in (-1, 1):
                c.save(); c.translate(bx, by); c.scale(fl * sg, 1); c.arc(14, 0, 14, 0, 2 * math.pi); c.restore(); c.fill()
        # snail
        sx = 700 + t * 4
        rgba(c, (0.80, 0.70, 0.55)); rrect(c, sx - 30, 735, 80, 16, 8); c.fill()
        rgba(c, (0.70, 0.45, 0.25)); c.arc(sx, 725, 22, 0, 2 * math.pi); c.fill()
    gx = 900 if a.get("basket") else 1250
    girl(c, gx, 1060, 1.3, phase=T * 4 if a.get("basket") else None)
    grandma(c, gx - 240, 1060, 1.35, face=1)
    if a.get("basket"):
        rgba(c, (0.75, 0.55, 0.30)); rrect(c, gx - 185, 920, 90, 60, 14); c.fill()
        for j in range(4):
            rgba(c, (0.90, 0.20, 0.18)); c.arc(gx - 170 + j * 20, 918, 11, 0, 2 * math.pi); c.fill()
        cat(c, gx + 200, 1060, 0.6, T, sleep=False)


def sc_river(c, t, d, T, a):
    sky(c, (0.48, 0.70, 0.93), (0.95, 0.92, 0.80))
    clouds(c, T, speed=5)
    hill(c, 560, 60, (0.55, 0.73, 0.50), 0.7)
    hill(c, 660, 40, (0.46, 0.68, 0.42), 1.9)
    rgba(c, (0.42, 0.66, 0.38)); c.rectangle(-400, 700, W + 800, 600); c.fill()
    # river winding across the bottom
    c.move_to(-100, 820); c.curve_to(500, 760, 1100, 980, W + 100, 860)
    c.line_to(W + 100, 1010); c.curve_to(1100, 1120, 500, 900, -100, 990); c.close_path()
    g = cairo.LinearGradient(0, 760, 0, 1100)
    g.add_color_stop_rgb(0, 0.55, 0.78, 0.95); g.add_color_stop_rgb(1, 0.35, 0.60, 0.85)
    c.set_source(g); c.fill()
    for k in range(26):
        x = (k * 83 + T * 40) % (W + 100) - 50
        y = 860 + 90 * math.sin(k * 1.7) * 0.6 + 30 * ((k % 3) - 1)
        rgba(c, (1, 1, 1), 0.35 + 0.25 * math.sin(T * 2 + k))
        c.set_line_width(3); c.move_to(x, y); c.line_to(x + 30, y); c.stroke()
    for k in range(8):
        rgba(c, (0.60, 0.62, 0.65)); c.save(); c.translate(150 + k * 240, 1000 + (k % 2) * 30); c.scale(1, 0.5)
        c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); c.fill()
    if a.get("boat"):
        for k in range(2):
            f = ((T * 0.02 + k * 0.35) % 1.0)
            bx = 1100 + f * 900
            by = 880 + 40 * math.sin(f * 6) + 6 * math.sin(T * 2 + k)
            rgba(c, (0.98, 0.97, 0.92))
            c.move_to(bx - 40, by); c.line_to(bx + 40, by); c.line_to(bx + 26, by + 16); c.line_to(bx - 26, by + 16); c.fill()
            c.move_to(bx - 20, by); c.line_to(bx, by - 34); c.line_to(bx + 20, by); c.fill()
    if a.get("bridge"):
        rgba(c, WOOD); c.rectangle(560, 800, 520, 30); c.fill()
        rgba(c, (0.75, 0.70, 0.62))
        for k in range(6):
            c.rectangle(570 + k * 100, 700, 12, 100)
        c.rectangle(560, 700, 520, 12); c.fill()
        rgba(c, mix(WOOD, (0, 0, 0), 0.25)); c.rectangle(580, 830, 20, 120); c.rectangle(1040, 830, 20, 120); c.fill()
        girl(c, 760, 800, 1.2, sit=True)
        grandma(c, 900, 800, 1.25, face=1, sit=True)
        dx = 820 + 160 * math.sin(T * 0.4)
        dy = 640 + 30 * math.sin(T * 1.1)
        rgba(c, (0.30, 0.55, 0.95)); c.set_line_width(5); c.move_to(dx - 26, dy); c.line_to(dx + 26, dy); c.stroke()
        rgba(c, (0.85, 0.92, 1.0), 0.6)
        for sg in (-1, 1):
            c.save(); c.translate(dx + sg * 4, dy - 6); c.scale(0.4, 1); c.arc(0, -10, 14, 0, 2 * math.pi); c.restore(); c.fill()
    else:
        p = prog(t, 0, d)
        girl(c, 400 + 500 * p, 760, 1.15, phase=T * 4)
        grandma(c, 260 + 500 * p, 760, 1.2, face=1)
    grass(c, T, 760, (0.36, 0.60, 0.34), n=60, h=60)
    grass(c, T, 1080, n=80, h=40)


def sc_tree(c, t, d, T, a):
    dusk = 0.5 * prog(t, 0, d) if a.get("dusk") else 0.0
    day_sky(c, 0.15 + dusk)
    clouds(c, T, speed=6)
    hill(c, 700, 50, mix((0.58, 0.74, 0.55), (0.55, 0.50, 0.50), dusk), 1.3)
    hill(c, 800, 40, mix((0.50, 0.70, 0.46), (0.48, 0.45, 0.45), dusk), 2.4)
    c.set_line_width(14); rgba(c, (0.70, 0.85, 0.98))
    c.move_to(-50, 900); c.curve_to(500, 820, 900, 900, 1400, 800); c.stroke()
    c.move_to(-100, H + 100); c.line_to(-100, 930); c.curve_to(400, 860, 900, 880, W + 100, 960)
    c.line_to(W + 100, H + 100); c.close_path(); rgba(c, mix((0.42, 0.66, 0.38), (0.40, 0.42, 0.40), dusk)); c.fill()
    big_tree(c, 700, 930, 1.8, T, night=dusk * 0.4)
    # swing from the left branch
    px, py = 470, 420
    ang = 0.35 * math.sin(T * 1.6) if a.get("swing") else 0.04 * math.sin(T)
    L = 360
    sx, sy = px + L * math.sin(ang), py + L * math.cos(ang)
    c.set_line_width(5); rgba(c, (0.85, 0.80, 0.65))
    for off in (-40, 40):
        c.move_to(px + off, py); c.line_to(sx + off, sy); c.stroke()
    rgba(c, WOOD); c.rectangle(sx - 60, sy, 120, 14); c.fill()
    if a.get("swing"):
        girl(c, sx - 10, sy + 6, 0.85, sit=True)
    else:
        grandma(c, 1050, 960, 1.05, face=-1)
        girl(c, 880, 960, 1.0)
    for k in range(20):
        lx = 300 + (k * 71) % 800
        ly = 960 + (k * 37) % 70
        rgba(c, (1, 0.95, 0.6), 0.25 * (0.5 + 0.5 * math.sin(T * 1.5 + k)))
        c.save(); c.translate(lx, ly); c.scale(1, 0.4); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); c.fill()
    grass(c, T, 1080, n=80, h=36)


def sc_evening_room(c, t, d, T, a):
    kitchen_base(c, T, night=1.0)
    rgba(c, (0, 0, 0), 0.25); c.rectangle(-400, -600, W + 800, H + 1200); c.fill()
    # lamp hanging over the table
    rgba(c, (0.2, 0.18, 0.16)); c.rectangle(1137, 0, 6, 330); c.fill()
    rgba(c, (0.95, 0.75, 0.40)); c.move_to(1060, 400); c.line_to(1220, 400); c.line_to(1170, 330); c.line_to(1110, 330); c.fill()
    glow(c, 1140, 420, 900, WARM, 0.55)
    # pot on the stove, bowls, candle
    rgba(c, (0.35, 0.35, 0.40)); rrect(c, 230, 580, 140, 70, 10); c.fill()
    if a.get("steam"):
        steam(c, 300, 575, T, 0.6)
        for x in (960, 1300):
            rgba(c, (0.95, 0.93, 0.88)); c.save(); c.scale(1, 0.5); c.arc(x, 690 / 0.5, 50, 0, math.pi); c.restore(); c.fill()
            steam(c, x, 680, T + x, 0.45, 0.6)
    fl = 0.8 + 0.2 * math.sin(T * 11) * math.sin(T * 5.3)
    rgba(c, (0.98, 0.95, 0.88)); c.rectangle(1125, 620, 30, 80); c.fill()
    glow(c, 1140, 600, 120, (1, 0.75, 0.3), 0.7 * fl)
    rgba(c, (1, 0.8, 0.3)); c.save(); c.translate(1140, 605); c.scale(1, 1.6 * fl); c.arc(0, 0, 9, 0, 2 * math.pi); c.restore(); c.fill()
    girl(c, 840, 900, 1.35)
    grandma(c, 1450, 900, 1.4, face=-1)
    chair(c, 1650, 700)
    cat(c, 1650, 700, 0.85, T)


def night_base(c, T):
    sky(c, (0.04, 0.06, 0.16), (0.16, 0.18, 0.36))
    stars(c, T)
    rgba(c, (0.98, 0.96, 0.85)); c.arc(1600, 200, 60, 0, 2 * math.pi); c.fill()
    glow(c, 1600, 200, 260, (0.9, 0.9, 1.0), 0.25)
    hill(c, 760, 50, (0.08, 0.10, 0.20), 1.0)
    c.move_to(-100, H + 100); c.line_to(-100, 860); c.curve_to(500, 800, 1200, 800, W + 100, 880)
    c.line_to(W + 100, H + 100); c.close_path(); rgba(c, (0.06, 0.08, 0.14)); c.fill()


def sc_night_sky(c, t, d, T, a):
    night_base(c, T)
    big_tree(c, 420, 880, 1.3, T, night=1.0)
    house(c, 380, 900, 1.0, lit=1.0, night=1.0, T=T)
    # two figures on the porch steps, wrapped in a blanket
    rgba(c, (0.10, 0.10, 0.16))
    c.arc(700, 860, 34, 0, 2 * math.pi); c.arc(770, 850, 38, 0, 2 * math.pi); c.fill()
    rgba(c, (0.30, 0.30, 0.50)); rrect(c, 650, 870, 170, 90, 30); c.fill()
    if a.get("fireflies"):
        fireflies(c, T, 0, 700, W, 330, 70, prog(t, 0.5, d * 0.4))


def sc_bedroom(c, t, d, T, a):
    dark = 0.35 + (0.4 * prog(t, 0, d) if a.get("dark") else 0.0)
    interior(c, wall=(0.70, 0.62, 0.70), floor=(0.45, 0.32, 0.25), dim=dark)
    rgba(c, (0.25, 0.22, 0.30), 0.9)
    c.move_to(-100, -100); c.line_to(900, -100); c.line_to(-100, 520); c.close_path(); c.fill()
    # round window with moon
    wx, wy, ww = 1180, 160, 380
    c.save(); c.arc(wx + ww / 2, wy + ww / 2, ww / 2, 0, 2 * math.pi); c.clip()
    sky(c, (0.06, 0.08, 0.20), (0.16, 0.18, 0.36))
    stars(c, T, 0.8)
    rgba(c, (0.98, 0.96, 0.85)); c.arc(wx + 250, wy + 130, 46, 0, 2 * math.pi); c.fill()
    glow(c, wx + 250, wy + 130, 180, (0.9, 0.9, 1.0), 0.25)
    if a.get("rain"):
        rain_lines(c, T, wx, wy, ww, ww, 0.8, 0.45)
    c.restore()
    if a.get("rain"):
        c.save(); c.arc(wx + ww / 2, wy + ww / 2, ww / 2, 0, 2 * math.pi); c.clip()
        glass_drops(c, T, wx, wy, ww, ww, 0.6); c.restore()
    window_frame(c, wx, wy, ww, ww, (0.85, 0.80, 0.75), round_top=True)
    # moonbeam
    c.move_to(wx + 40, wy + 300); c.line_to(wx + 340, wy + 300); c.line_to(1100, 1000); c.line_to(500, 1000); c.close_path()
    rgba(c, (0.85, 0.88, 1.0), 0.08); c.fill()
    # bed with patchwork quilt
    rgba(c, WOOD); c.rectangle(260, 600, 40, 300); c.rectangle(1080, 700, 30, 200); c.fill()
    rgba(c, (0.98, 0.97, 0.95)); rrect(c, 300, 640, 220, 90, 40); c.fill()
    pal = [(0.85, 0.40, 0.40), (0.95, 0.75, 0.40), (0.45, 0.60, 0.80), (0.55, 0.75, 0.50), (0.80, 0.55, 0.75)]
    breath = 4 * math.sin(T * 0.9)
    for i in range(8):
        for j in range(3):
            rgba(c, pal[(i * 3 + j * 2) % 5])
            c.rectangle(440 + i * 80, 690 + j * 60 - breath * (1 - j / 3), 80, 60); c.fill()
    rgba(c, (0, 0, 0), 0.15)
    for i in range(9):
        c.rectangle(440 + i * 80, 690 - breath, 2, 180); c.fill()
    rgba(c, HAIR); c.arc(420, 650, 40, 0, 2 * math.pi); c.fill()
    rgba(c, SKIN); c.arc(440, 660, 30, 0, 2 * math.pi); c.fill()
    rgba(c, HAIR); c.arc(425, 645, 38, math.pi * 1.0, math.pi * 1.75); c.fill()
    c.set_line_width(3); rgba(c, (0.2, 0.15, 0.15)); c.arc(452, 660, 6, 0.2, math.pi - 0.2); c.stroke()
    cat(c, 1010, 700, 0.6, T)
    rgba(c, (0, 0, 0), 0.25 * dark); c.rectangle(-400, -600, W + 800, H + 1200); c.fill()
    glow(c, 1370, 350, 500, (0.85, 0.88, 1.0), 0.12)


def sc_outro(c, t, d, T, a):
    night_base(c, T)
    house(c, 960, 900, 0.9, lit=1.0, night=1.0, T=T)
    fireflies(c, T, 0, 700, W, 330, 40)
    serif(c, "Sleep well", W / 2, 360, 96, INK, prog(t, 0, 1.0))
    ap = prog(t, d * 0.35, d * 0.5)
    rgba(c, (0.85, 0.35, 0.35), ap); rrect(c, W / 2 - 200, 450, 400, 90, 45); c.fill()
    text(c, "SUBSCRIBE", W / 2, 510, 40, INK, ap)
    serif(c, "a new cozy story every week", W / 2, 620, 36, (1, 0.93, 0.75), ap, bold=False, italic=True)


def vignette(c):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.4, W / 2, H / 2, H * 1.1)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.05, 0.02, 0.0, 0.45)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    grain(c, 0.06)


def snowfall(c, T, amount=1.0, wind=1.0):
    pass


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}
