"""Stickman scene library drawn with cairo on a 1920x1080 logical canvas."""
import math, random
import cairo

W, H = 1920, 1080
INK = (0.95, 0.96, 0.98)
DIM = (0.55, 0.60, 0.70)
RED = (0.92, 0.22, 0.24)
AMBER = (1.0, 0.66, 0.22)
SNOW = (0.86, 0.90, 0.97)
BG1, BG2 = (0.03, 0.05, 0.10), (0.09, 0.12, 0.21)

_rng = random.Random(7)
STARS = [(_rng.random() * W, _rng.random() * H * 0.6, _rng.random() * 1.6 + 0.5, _rng.random() * 6) for _ in range(110)]
FLAKES = [(_rng.random() * W, _rng.random() * H, _rng.random(), _rng.random() * 6) for _ in range(170)]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return ease((t - a) / (b - a)) if b > a else float(t >= a)


def rgba(c, col, a=1.0):
    c.set_source_rgba(col[0], col[1], col[2], a)


# ---------- primitives ----------

def text(c, s, x, y, size=48, col=INK, a=1.0, align="center", bold=True, italic=False):
    c.select_font_face("Inter", cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    e = c.text_extents(s)
    dx = {"center": -e.x_advance / 2, "left": 0, "right": -e.x_advance}[align]
    c.move_to(x + dx, y)
    rgba(c, col, a)
    c.show_text(s)
    c.new_path()
    return e.x_advance


def text_w(c, s, size, bold=True):
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    return c.text_extents(s).x_advance


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def label(c, s, x, y, size=34, col=INK, a=1.0, bg=(0, 0, 0), bga=0.55):
    w = text_w(c, s, size)
    rgba(c, bg, bga * a)
    rrect(c, x - w / 2 - 18, y - size - 8, w + 36, size + 28, 12)
    c.fill()
    text(c, s, x, y + 4, size, col, a)


def line(c, x1, y1, x2, y2, w=6, col=INK, a=1.0):
    c.set_line_width(w)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(c, col, a)
    c.move_to(x1, y1)
    c.line_to(x2, y2)
    c.stroke()


def stick(c, x, y, s=1.0, col=INK, a=1.0, phase=None, arms=None, lying=0.0, wave=None, head_hold=0.0):
    """Stick figure standing with feet at (x, y). phase -> walking, lying -> rotation (rad)."""
    c.save()
    c.translate(x, y)
    if lying:
        c.rotate(lying)
    c.scale(s, s)
    lw = 7
    sw = 0.0 if phase is None else math.sin(phase)
    bob = 0.0 if phase is None else abs(math.cos(phase)) * 3
    hip = (0, -52 - bob)
    neck = (0, -100 - bob)
    head = (0, -118 - bob)
    lg = 0.42 * sw
    for sgn in (1, -1):
        ang = sgn * (0.18 + lg) if phase is not None else sgn * 0.2
        line(c, hip[0], hip[1], math.sin(ang) * 54, hip[1] + math.cos(ang) * 54, lw, col, a)
    line(c, *hip, *neck, lw, col, a)
    if head_hold:
        for sgn in (1, -1):
            ex, ey = sgn * 30, -88 - bob
            line(c, *neck, ex, ey, lw, col, a)
            line(c, ex, ey, sgn * 16, head[1] - 4, lw, col, a)
    else:
        al = arms if arms is not None else ((-0.5 * sw, 0.5 * sw) if phase is not None else (0.35, -0.35))
        for i, sgn in enumerate((1, -1)):
            ang = al[i]
            if wave is not None and i == 1:
                ang = -2.6 + 0.35 * math.sin(wave)
            line(c, *neck, math.sin(ang + sgn * 0.15) * 46, neck[1] + math.cos(ang + sgn * 0.15) * 46, lw, col, a)
    c.arc(head[0], head[1], 17, 0, 2 * math.pi)
    rgba(c, col, a)
    c.fill()
    c.restore()


# ---------- environment ----------

def sky(c, top=BG1, bot=BG2, stars=True, T=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    if stars:
        for sx, sy, r, ph in STARS:
            rgba(c, INK, 0.25 + 0.35 * (0.5 + 0.5 * math.sin(T * 1.3 + ph)))
            c.arc(sx, sy, r, 0, 2 * math.pi)
            c.fill()


def snowfall(c, T, amount=1.0, wind=1.0):
    n = int(len(FLAKES) * amount)
    for i, (x0, y0, sp, ph) in enumerate(FLAKES[:n]):
        x = (x0 + wind * (40 + 50 * sp) * T + 18 * math.sin(T * 0.9 + ph)) % (W + 40) - 20
        y = (y0 + (50 + 90 * sp) * T) % (H + 40) - 20
        rgba(c, SNOW, 0.35 + 0.5 * sp)
        c.arc(x, y, 1.6 + 2.6 * sp, 0, 2 * math.pi)
        c.fill()


def far_mountains(c, col=(0.12, 0.16, 0.27), base=700, seed=3):
    r = random.Random(seed)
    c.move_to(-50, H)
    x = -50
    c.line_to(x, base)
    while x < W + 50:
        x += r.randint(120, 260)
        c.line_to(x, base - r.randint(60, 260))
        x += r.randint(80, 200)
        c.line_to(x, base - r.randint(0, 80))
    c.line_to(W + 50, H)
    c.close_path()
    rgba(c, col)
    c.fill()


def tree(c, x, y, h=160, col=(0.06, 0.10, 0.12), a=1.0, snow=True):
    rgba(c, col, a)
    c.rectangle(x - h * 0.04, y - h * 0.18, h * 0.08, h * 0.18)
    c.fill()
    for i in range(3):
        w = h * (0.42 - i * 0.1)
        top = y - h * (0.45 + i * 0.22)
        bot = y - h * (0.12 + i * 0.22)
        c.move_to(x - w, bot)
        c.line_to(x, top)
        c.line_to(x + w, bot)
        c.close_path()
        rgba(c, col, a)
        c.fill()
        if snow:
            c.move_to(x - w * 0.35, top + (bot - top) * 0.35)
            c.line_to(x, top)
            c.line_to(x + w * 0.35, top + (bot - top) * 0.35)
            c.close_path()
            rgba(c, SNOW, 0.55 * a)
            c.fill()


# wide slope: summit at right, forest at bottom-left
SL_X0, SL_Y0, SL_X1, SL_Y1 = W + 100, 280, -100, 930
SL_ANG = math.atan2(SL_Y1 - SL_Y0, SL_X0 - SL_X1)


def slope_y(x):
    return SL_Y0 + (SL_X0 - x) * (SL_Y1 - SL_Y0) / (SL_X0 - SL_X1)


def slope(c, forest=True):
    c.move_to(SL_X1, SL_Y1)
    c.line_to(SL_X0, SL_Y0)
    c.line_to(SL_X0, H + 300)
    c.line_to(SL_X1, H + 300)
    c.close_path()
    g = cairo.LinearGradient(0, SL_Y0, 0, H)
    g.add_color_stop_rgb(0, 0.78, 0.83, 0.92)
    g.add_color_stop_rgb(1, 0.45, 0.52, 0.66)
    c.set_source(g)
    c.fill()
    if forest:
        r = random.Random(11)
        for i in range(14):
            x = 20 + i * 38 + r.randint(-10, 10)
            tree(c, x, slope_y(x) + 30 + r.randint(0, 40), r.randint(130, 210))


def tent(c, x, y, s=1.0, cut=0.0, buried=0.0, crushed=0.0, glow=0.0):
    """Tent sitting on the slope at (x, y). cut 0..1 draws the knife slash."""
    c.save()
    c.translate(x, y)
    c.rotate(-SL_ANG)
    c.scale(s, s)
    h = 70 * (1 - 0.6 * crushed)
    c.move_to(-110, 0)
    c.line_to(-80, -h)
    c.line_to(90, -h + 6 * crushed)
    c.line_to(110, 0)
    c.close_path()
    rgba(c, (0.22, 0.30, 0.20))
    c.fill_preserve()
    rgba(c, (0.10, 0.14, 0.10))
    c.set_line_width(4)
    c.stroke()
    if glow:
        rgba(c, AMBER, 0.35 * glow)
        c.rectangle(-70, -h + 10, 140, h - 14)
        c.fill()
    if cut > 0:
        pts = [(-50, -h + 14), (-30, -h + 26), (-10, -h + 20), (10, -h + 34), (30, -h + 28), (55, -h + 42)]
        n = cut * (len(pts) - 1)
        c.set_line_width(7)
        rgba(c, RED)
        c.move_to(*pts[0])
        for i in range(1, len(pts)):
            f = clamp(n - (i - 1))
            if f <= 0:
                break
            px = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f
            py = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f
            c.line_to(px, py)
        c.stroke()
    if buried > 0:
        c.move_to(-130, 4)
        c.curve_to(-120, -h * buried * 1.1, 40, -h * buried * 0.9, 130, 4)
        c.close_path()
        rgba(c, SNOW)
        c.fill()
    c.restore()


def footprints(c, x0, y0, x1, y1, p, lanes=8, spread=16, wobble=1.0, a=1.0):
    steps = 60
    shown = int(steps * p)
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for lane in range(lanes):
        off = (lane - (lanes - 1) / 2) * spread
        for i in range(shown):
            f = i / steps
            side = 4 if i % 2 else -4
            wob = wobble * 6 * math.sin(i * 0.7 + lane)
            px = x0 + dx * f + nx * (off + side + wob)
            py = y0 + dy * f + ny * (off + side + wob)
            c.save()
            c.translate(px, py)
            c.scale(1, 0.55)
            c.arc(0, 0, 4.2, 0, 2 * math.pi)
            c.restore()
            rgba(c, (0.25, 0.30, 0.42), 0.8 * a)
            c.fill()


def vignette(c):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.6)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


def qmark(c, x, y, size, a):
    text(c, "?", x, y, size, RED, a)


def xmark(c, x, y, r=22, a=1.0):
    line(c, x - r, y - r, x + r, y + r, 8, RED, a)
    line(c, x - r, y + r, x + r, y - r, 8, RED, a)


def check(c, x, y, r=22, a=1.0):
    c.set_line_width(8)
    rgba(c, (0.35, 0.85, 0.5), a)
    c.move_to(x - r, y)
    c.line_to(x - r * 0.3, y + r * 0.7)
    c.line_to(x + r, y - r * 0.8)
    c.stroke()


# ---------- scenes: f(c, t, d, T, args) ----------

def sc_tent_night(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c)
    slope(c)
    tx = 1250
    tent(c, tx, slope_y(tx) + 6, 1.5, cut=prog(t, d * 0.55, d * 0.85), buried=0.25)
    snowfall(c, T, 1.0, 1.6)


def sc_footprints(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c)
    slope(c)
    tx = 1350
    tent(c, tx, slope_y(tx) + 6, 1.0, cut=1, buried=0.4)
    p = prog(t, 0.3, d * 0.8)
    footprints(c, tx - 120, slope_y(tx - 120) + 40, 520, slope_y(520) + 40, p,
               lanes=6, wobble=0.3 if a.get("orderly") else 1.0)
    if a.get("orderly"):
        label(c, "~1.5 km", 950, 380, 40, a=prog(t, 1.0, 2.0))
        label(c, "8 or 9 sets of tracks", 950, 460, 34, AMBER, prog(t, d * 0.3, d * 0.4))
    else:
        label(c, "-30°C", 1600, 160, 56, (0.6, 0.85, 1.0), prog(t, d * 0.3, d * 0.45))
    snowfall(c, T, 0.6)


def sc_questions(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=860)
    for i in range(9):
        x = 360 + i * 150
        stick(c, x, 860, 1.2, col=(0.75, 0.8, 0.9))
        qmark(c, x, 650 - 10 * math.sin(T * 2 + i), 90, prog(t, 0.4 + i * 0.25, 0.7 + i * 0.25))
    label(c, "Why did they leave the tent?", W / 2, 280, 64, a=prog(t, 3.0, 4.0))
    snowfall(c, T, 0.5)


def sc_title(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=900)
    s = 1 + 0.03 * t
    c.save()
    c.translate(W / 2, 470)
    c.scale(s, s)
    text(c, "THE DYATLOV PASS", 0, 0, 120, INK, prog(t, 0, 0.6))
    text(c, "INCIDENT", 0, 130, 120, RED, prog(t, 0.3, 0.9))
    c.restore()
    w = 900 * prog(t, 0.6, 1.6)
    line(c, W / 2 - w / 2, 670, W / 2 + w / 2, 670, 6, RED)
    text(c, "1959  ·  Northern Ural Mountains", W / 2, 740, 40, DIM, prog(t, 1.0, 1.8), bold=False)
    snowfall(c, T, 0.6)


NAMES9 = ["Igor Dyatlov", "Zinaida Kolmogorova", "Lyudmila Dubinina", "Alexander Kolevatov",
          "Rustem Slobodin", "Yuri Krivonischenko", "Yuri Doroshenko", "Nikolai Thibeaux-Brignolles",
          "Semyon Zolotaryov"]


def sc_group(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=880)
    rgba(c, SNOW)
    c.rectangle(-400, 880, W + 800, 600)
    c.fill()
    for i in range(10):
        x = 330 + i * 140
        ap = prog(t, 0.2 + i * 0.18, 0.6 + i * 0.18)
        col = AMBER if i == 0 and t > d * 0.45 else INK
        stick(c, x, 880 - 20 * (1 - ap), 1.15, col=col, a=ap)
    text(c, "Ural Polytechnic Institute  ·  January 1959", W / 2, 230, 48, INK, prog(t, 0.5, 1.5))
    text(c, "10 students & graduates", W / 2, 300, 40, DIM, prog(t, 1.0, 2.0), bold=False)
    if t > d * 0.45:
        label(c, "Igor Dyatlov, 23 — leader", 330, 640, 36, AMBER, prog(t, d * 0.45, d * 0.52))
    snowfall(c, T, 0.5)


def sc_map(c, t, d, T, a):
    rgba(c, (0.07, 0.09, 0.14))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    c.set_line_width(1)
    for i in range(0, W, 80):
        line(c, i, 0, i, H, 1, DIM, 0.08)
    for j in range(0, H, 80):
        line(c, 0, j, W, j, 1, DIM, 0.08)
    # Ural ridge
    for k in range(9):
        x, y = 1120 + 40 * math.sin(k), 120 + k * 95
        c.move_to(x - 40, y + 30)
        c.line_to(x, y - 30)
        c.line_to(x + 40, y + 30)
        c.close_path()
        rgba(c, (0.25, 0.30, 0.42))
        c.fill()
    pts = [("Sverdlovsk", 760, 930), ("Ivdel", 860, 520), ("Vizhai", 930, 400), ("Otorten", 1110, 170)]
    p = prog(t, 0.5, d * 0.6)
    segs = len(pts) - 1
    c.set_line_width(6)
    c.set_dash([18, 12])
    rgba(c, RED)
    c.move_to(pts[0][1], pts[0][2])
    for i in range(1, len(pts)):
        f = clamp(p * segs - (i - 1))
        if f <= 0:
            break
        c.line_to(pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f, pts[i - 1][2] + (pts[i][2] - pts[i - 1][2]) * f)
    c.stroke()
    c.set_dash([])
    for i, (n, x, y) in enumerate(pts):
        ap = prog(p * segs, i - 0.2, i + 0.1)
        rgba(c, AMBER if n == "Otorten" else INK, ap)
        c.arc(x, y, 12, 0, 2 * math.pi)
        c.fill()
        text(c, n, x - 30, y + 10, 38, AMBER if n == "Otorten" else INK, ap, align="right")
    label(c, "Category III — the hardest level", 1500, 820, 40, AMBER, prog(t, d * 0.4, d * 0.5))


def ground_scene(c, T, base=860):
    sky(c, T=T)
    far_mountains(c, base=base - 40)
    rgba(c, SNOW)
    c.rectangle(-400, base, W + 800, 700)
    c.fill()


def sc_goodbye(c, t, d, T, a):
    ground_scene(c, T)
    for i in range(9):
        x = 900 + i * 95 + t * 60
        stick(c, x, 860, 0.95, phase=T * 5 + i, a=1 - prog(t, d * 0.7, d))
    yx = 760 - max(0, t - 2.5) * 50
    stick(c, yx, 860, 1.0, col=AMBER, wave=T * 8 if t < 3.5 else None, phase=None if t < 3.5 else T * 5)
    label(c, "Yuri Yudin", yx, 640, 38, AMBER, prog(t, 0.5, 1.2))
    snowfall(c, T, 0.6)


def sc_walking(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=760)
    for k in range(18):
        x = (k * 160 - T * 90) % (W + 300) - 150
        tree(c, x, 860, 170 + (k * 37) % 90)
    rgba(c, SNOW)
    c.rectangle(-400, 860, W + 800, 700)
    c.fill()
    for i in range(9):
        stick(c, 520 + i * 100, 860, 0.95, phase=T * 6 + i * 0.7)
    if t > d * 0.45:
        ap = prog(t, d * 0.45, d * 0.55)
        c.save()
        c.translate(1500, 330)
        c.rotate(0.06)
        rgba(c, (0.93, 0.90, 0.80), ap)
        c.rectangle(-210, -130, 420, 260)
        c.fill()
        text(c, "EVENING OTORTEN", 0, -60, 34, (0.15, 0.15, 0.2), ap)
        for j in range(5):
            line(c, -170, -10 + j * 26, 170 - (j % 2) * 60, -10 + j * 26, 4, (0.4, 0.4, 0.45), ap)
        c.restore()
    label(c, "Diaries & cameras recovered", 520, 200, 38, a=prog(t, d * 0.15, d * 0.25))
    snowfall(c, T, 0.5)


def sc_camp(c, t, d, T, a):
    dusk = prog(t, 0, d)
    top = tuple(BG1[i] * dusk + (0.20, 0.12, 0.28)[i] * (1 - dusk) for i in range(3))
    sky(c, top=top, T=T, stars=dusk > 0.5)
    far_mountains(c)
    slope(c)
    tx = 1250
    tent(c, tx, slope_y(tx) + 6, 1.3, glow=prog(t, d * 0.75, d * 0.85) * (1 - prog(t, d * 0.95, d)))
    label(c, "Kholat Syakhl — “Dead Mountain”", 1300, 200, 46, a=prog(t, d * 0.15, d * 0.25))
    ap = prog(t, d * 0.45, d * 0.55)
    label(c, "forest (shelter)", 250, 520, 34, (0.6, 0.85, 1.0), ap)
    label(c, "open slope", tx, 420, 34, AMBER, ap)
    snowfall(c, T, 0.4)


def sc_calendar(c, t, d, T, a):
    sky(c, T=T, stars=False)
    day = int(1 + 19 * prog(t, 0.3, d * 0.8))
    c.save()
    c.translate(W / 2, H / 2 - 20)
    rgba(c, (0.95, 0.95, 0.97))
    rrect(c, -230, -260, 460, 520, 26)
    c.fill()
    rgba(c, RED)
    c.rectangle(-230, -260, 460, 110)
    c.fill()
    text(c, "FEBRUARY 1959", 0, -190, 40, INK)
    late = day >= 12
    text(c, str(day), 0, 120, 230, RED if late else (0.12, 0.14, 0.2))
    c.restore()
    if late:
        label(c, "No telegram.", 1450, 400, 46, RED, prog(t, d * 0.35, d * 0.45))
    if day >= 20:
        label(c, "Search begins", 1450, 520, 46, AMBER)
    label(c, "Telegram due: Feb 12", 450, 400, 40, a=prog(t, 0.2, 0.8))


def sc_search(c, t, d, T, a):
    sky(c, T=T, top=(0.12, 0.16, 0.26), bot=(0.35, 0.42, 0.55), stars=False)
    far_mountains(c, col=(0.25, 0.30, 0.42))
    slope(c, forest=False)
    tx = 1300
    tent(c, tx, slope_y(tx) + 6, 1.4, buried=0.55, crushed=0.5, cut=prog(t, d * 0.75, d * 0.92))
    for i in range(4):
        x = 480 + i * 90 + 380 * prog(t, 0, d * 0.45)
        stick(c, x, slope_y(x) + 4, 0.9, phase=T * 5 + i if t < d * 0.45 else None)
    if t > d * 0.45:
        items = ["boots", "coats", "food", "equipment"]
        for i, s in enumerate(items):
            label(c, s, 1050 + i * 180, 220, 34, a=prog(t, d * 0.45 + i * 0.4, d * 0.5 + i * 0.4))
    label(c, "Feb 26, 1959", 300, 160, 44, AMBER, prog(t, 0.2, 0.8))
    snowfall(c, T, 0.3, 0.6)


def sc_cedar(c, t, d, T, a):
    sky(c, T=T)
    rgba(c, (0.80, 0.85, 0.93))
    c.rectangle(-400, 860, W + 800, 700)
    c.fill()
    for k in range(7):
        tree(c, 150 + k * 280, 870, 300, a=0.6)
    # big cedar
    rgba(c, (0.16, 0.11, 0.08))
    c.rectangle(560, 140, 70, 730)
    c.fill()
    for i in range(6):
        y = 220 + i * 110
        line(c, 595, y, 595 - 160 + i * 10, y + 60, 14, (0.10, 0.16, 0.12))
        line(c, 595, y + 40, 595 + 170 - i * 10, y + 100, 14, (0.10, 0.16, 0.12))
    ap = prog(t, d * 0.65, d * 0.75)
    for i in range(5):
        line(c, 640, 800 - i * 80, 680, 790 - i * 80, 6, AMBER, ap)
    if ap > 0:
        label(c, "branches broken up to 5 m", 950, 420, 34, AMBER, ap)
    fl = 0.7 + 0.3 * math.sin(T * 13) * math.sin(T * 7.3)
    g = cairo.RadialGradient(900, 850, 5, 900, 850, 260)
    g.add_color_stop_rgba(0, 1, 0.6, 0.2, 0.55 * fl)
    g.add_color_stop_rgba(1, 1, 0.5, 0.1, 0)
    c.set_source(g)
    c.arc(900, 850, 260, 0, 2 * math.pi)
    c.fill()
    for k in range(3):
        c.move_to(870 + k * 25, 865)
        c.line_to(882 + k * 25, 820 - 20 * fl * (1 + k % 2))
        c.line_to(895 + k * 25, 865)
        rgba(c, AMBER, 0.9)
        c.fill()
    bp = prog(t, d * 0.2, d * 0.35)
    stick(c, 1080, 862, 0.9, col=(0.22, 0.27, 0.38), a=bp, lying=-math.pi / 2)
    stick(c, 1230, 862, 0.9, col=(0.22, 0.27, 0.38), a=bp, lying=-math.pi / 2)
    label(c, "Doroshenko", 1030, 760, 30, a=bp)
    label(c, "Krivonischenko", 1250, 700, 30, a=bp)
    snowfall(c, T, 0.4)


def sc_between(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c)
    slope(c)
    tx = 1500
    tent(c, tx, slope_y(tx) + 6, 0.8, buried=0.4, cut=1)
    names = [("Dyatlov", 820), ("Kolmogorova", 1080), ("Slobodin", 1280)]
    for i, (n, x) in enumerate(names):
        ap = prog(t, d * 0.25 + i * 0.7, d * 0.25 + i * 0.7 + 0.5)
        stick(c, x, slope_y(x) + 8, 0.6, col=(0.25, 0.30, 0.42), a=ap, lying=-math.pi / 2 - SL_ANG)
        label(c, n, x, slope_y(x) - 90, 30, a=ap)
    ap = prog(t, d * 0.55, d * 0.65)
    c.set_line_width(5)
    c.set_dash([14, 10])
    rgba(c, AMBER, ap)
    c.move_to(760, slope_y(760) - 150)
    c.line_to(1420, slope_y(1420) - 150)
    c.stroke()
    c.set_dash([])
    label(c, "heading back up to the tent", 1100, slope_y(1100) - 210, 32, AMBER, ap)
    snowfall(c, T, 0.4)


def sc_ravine(c, t, d, T, a):
    sky(c, T=T, top=(0.20, 0.28, 0.42), bot=(0.55, 0.62, 0.72), stars=False)
    c.move_to(-100, 520)
    c.line_to(700, 540)
    c.curve_to(820, 560, 860, 860, 960, 880)
    c.curve_to(1060, 860, 1100, 560, 1220, 540)
    c.line_to(W + 100, 520)
    c.line_to(W + 100, H + 100)
    c.line_to(-100, H + 100)
    c.close_path()
    rgba(c, (0.22, 0.18, 0.15))
    c.fill()
    melt = prog(t, d * 0.5, d)
    top = 520 + 120 * melt
    c.rectangle(760, top, 400, 880 - top)
    rgba(c, SNOW, 0.92)
    c.fill()
    for i in range(4):
        stick(c, 860 + i * 60, 875, 0.42, col=(0.25, 0.3, 0.4), lying=-math.pi / 2)
    line(c, 1250, top, 1250, 875, 5, AMBER)
    line(c, 1230, top, 1270, top, 5, AMBER)
    line(c, 1230, 875, 1270, 875, 5, AMBER)
    text(c, "4 m of snow", 1290, (top + 875) / 2 + 14, 40, AMBER, align="left")
    label(c, "May 1959", 400, 220, 54, a=prog(t, d * 0.4, d * 0.5))
    text(c, "~2 months later", 400, 300, 36, INK, prog(t, 0.3, 1.0), bold=False)
    r = 60 + 6 * math.sin(T * 2)
    rgba(c, (1, 0.85, 0.4), 0.9 * prog(t, d * 0.4, d * 0.6))
    c.arc(1650, 200, r, 0, 2 * math.pi)
    c.fill()


def sc_injuries(c, t, d, T, a):
    sky(c, T=T, stars=False)
    who = [("Thibeaux-Brignolles", "skull"), ("Dubinina", "chest"), ("Zolotaryov", "chest"), ("Kolevatov", None)]
    for i, (n, hit) in enumerate(who):
        x = 420 + i * 360
        stick(c, x, 800, 2.0, col=(0.45, 0.5, 0.62))
        text(c, n, x, 880, 34, INK, prog(t, 0.2 + i * 0.3, 0.6 + i * 0.3))
        if hit:
            start = d * (0.18 if hit == "skull" else 0.33)
            ap = prog(t, start, start + 0.5)
            yy = 800 - (236 if hit == "skull" else 170)
            pr = 34 + 6 * math.sin(T * 6)
            c.set_line_width(7)
            rgba(c, RED, ap)
            c.arc(x, yy, pr, 0, 2 * math.pi)
            c.stroke()
            text(c, "skull fracture" if hit == "skull" else "chest fractures", x, 940, 30, RED, ap, bold=False)
    label(c, "Almost no external wounds", W / 2, 180, 50, AMBER, prog(t, d * 0.55, d * 0.62))
    label(c, "Traces of radiation on some clothing", W / 2, 280, 38, (0.55, 1.0, 0.55), prog(t, d * 0.8, d * 0.87))


def sc_classified(c, t, d, T, a):
    rgba(c, (0.07, 0.07, 0.09))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    c.save()
    c.translate(W / 2, H / 2)
    c.rotate(-0.03)
    rgba(c, (0.92, 0.89, 0.80))
    c.rectangle(-480, -420, 960, 840)
    c.fill()
    dark = (0.15, 0.15, 0.18)
    text(c, "CRIMINAL CASE  ·  1959", 0, -330, 44, dark)
    for j in range(5):
        line(c, -400, -250 + j * 40, 400 - (j % 3) * 90, -250 + j * 40, 5, (0.55, 0.53, 0.5))
    q = "“...a compelling natural force...”"
    n = int(len(q) * prog(t, d * 0.25, d * 0.55))
    rgba(c, (1, 0.9, 0.3), 0.6 * (n > 0))
    c.rectangle(-410, -10, 820 * n / len(q), 70)
    c.fill()
    text(c, q[:n], -400, 40, 44, dark, align="left", italic=True)
    for j in range(4):
        line(c, -400, 150 + j * 40, 380 - (j % 2) * 120, 150 + j * 40, 5, (0.55, 0.53, 0.5))
    sp = prog(t, d * 0.68, d * 0.74)
    if sp > 0:
        c.save()
        c.translate(120, 280)
        c.rotate(-0.22)
        s = 2.2 - 1.2 * sp
        c.scale(s, s)
        c.set_line_width(8)
        rgba(c, RED, sp)
        rrect(c, -230, -60, 460, 110, 10)
        c.stroke()
        text(c, "CLASSIFIED", 0, 22, 72, RED, sp)
        c.restore()
    c.restore()


def icon(c, kind, x, y, a, T):
    if kind == "rocket":
        c.move_to(x, y - 60); c.line_to(x + 22, y + 30); c.line_to(x - 22, y + 30); c.close_path()
        rgba(c, INK, a); c.fill()
        c.move_to(x - 12, y + 34); c.line_to(x, y + 70 + 8 * math.sin(T * 20)); c.line_to(x + 12, y + 34)
        rgba(c, AMBER, a); c.fill()
    elif kind == "people":
        stick(c, x - 30, y + 60, 0.6, a=a); stick(c, x + 30, y + 60, 0.6, a=a)
    elif kind == "yeti":
        for k, (dx, dy) in enumerate([(-18, 30), (18, -10)]):
            c.save(); c.translate(x + dx, y + dy); c.scale(1, 1.6)
            c.arc(0, 0, 16, 0, 2 * math.pi); c.restore(); rgba(c, INK, a); c.fill()
    elif kind == "wave":
        for k in range(3):
            c.set_line_width(6); rgba(c, INK, a * (1 - k * 0.25))
            c.arc(x - 40, y, 30 + k * 26, -0.8, 0.8); c.stroke()
    elif kind == "avalanche":
        c.move_to(x - 70, y + 50); c.line_to(x + 10, y - 60); c.line_to(x + 70, y + 50); c.close_path()
        rgba(c, INK, a); c.fill()
        c.move_to(x - 10, y - 30); c.line_to(x + 20, y - 40); c.line_to(x + 40, y + 10); c.close_path()
        rgba(c, (0.6, 0.85, 1.0), a); c.fill()


def sc_theories(c, t, d, T, a):
    sky(c, T=T, stars=False)
    cards = [("Military test", "rocket"), ("Mansi / prisoners", "people"), ("Yeti", "yeti"),
             ("Infrasound", "wave"), ("Avalanche", "avalanche")]
    for i, (n, k) in enumerate(cards):
        ap = prog(t, 0.2 + i * (d - 1) / 6, 0.5 + i * (d - 1) / 6)
        x = 240 + i * 360
        y = 560 + 30 * (1 - ap)
        rgba(c, (0.14, 0.17, 0.27), ap)
        rrect(c, x - 150, y - 200, 300, 380, 24)
        c.fill()
        icon(c, k, x, y - 60, ap, T)
        text(c, n, x, y + 120, 32, INK, ap)
    label(c, "THE THEORIES", W / 2, 200, 60, a=prog(t, 0, 0.5))


def sc_rocket(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=900)
    p = prog(t, 0.3, d * 0.9)
    pts = []
    for k in range(40):
        f = p - k * 0.008
        if f < 0:
            break
        x = 200 + 1500 * f
        y = 700 - 520 * math.sin(f * math.pi * 0.9)
        pts.append((x, y))
    for k, (x, y) in enumerate(pts):
        rgba(c, AMBER, 0.6 * (1 - k / 40))
        c.arc(x, y, 18 * (1 - k / 45), 0, 2 * math.pi)
        c.fill()
    if pts:
        g = cairo.RadialGradient(pts[0][0], pts[0][1], 4, pts[0][0], pts[0][1], 140)
        g.add_color_stop_rgba(0, 1, 0.7, 0.3, 0.8)
        g.add_color_stop_rgba(1, 1, 0.5, 0.1, 0)
        c.set_source(g)
        c.arc(pts[0][0], pts[0][1], 140, 0, 2 * math.pi)
        c.fill()
    label(c, "Orange lights reported in the sky", W / 2, 980, 40, AMBER, prog(t, d * 0.6, d * 0.7))
    label(c, "Theory 1: secret military test", W / 2, 140, 44, a=prog(t, 0, 0.6))


def sc_yeti(c, t, d, T, a):
    sky(c, T=T)
    for k in range(12):
        tree(c, k * 180, 920, 380, a=0.9)
    ap = prog(t, d * 0.6, d * 0.75)
    c.save()
    c.translate(1300, 900)
    rgba(c, (0.02, 0.02, 0.03), ap)
    c.save(); c.scale(1, 1.5); c.arc(0, -260, 150, 0, 2 * math.pi); c.restore(); c.fill()
    c.arc(0, -560, 80, 0, 2 * math.pi); c.fill()
    for sgn in (1, -1):
        rgba(c, RED, ap * (0.7 + 0.3 * math.sin(T * 3)))
        c.arc(sgn * 26, -570, 9, 0, 2 * math.pi); c.fill()
    c.restore()
    label(c, "Theory 2: someone attacked them", W / 2, 140, 44, a=prog(t, 0, 0.6))
    ap2 = prog(t, d * 0.3, d * 0.4)
    label(c, "No fight  ·  Nothing stolen", 600, 520, 44, RED, ap2)


def sc_infrasound(c, t, d, T, a):
    sky(c, T=T)
    c.move_to(400, 900); c.line_to(800, 330); c.line_to(1200, 900); c.close_path()
    rgba(c, (0.70, 0.76, 0.86)); c.fill()
    for k in range(6):
        r = ((T * 120 + k * 90) % 540)
        c.set_line_width(5)
        rgba(c, (0.6, 0.85, 1.0), 0.7 * (1 - r / 540))
        c.arc(800, 330, r, -0.9, 0.9)
        c.stroke()
    stick(c, 1500 + 6 * math.sin(T * 30), 900, 1.4, head_hold=1)
    rgba(c, SNOW); c.rectangle(-400, 900, W + 800, 500); c.fill()
    label(c, "Infrasound  ·  below 20 Hz", W / 2, 140, 44, a=prog(t, 0, 0.6))
    label(c, "Broken bones?", 1500, 520, 44, RED, prog(t, d * 0.7, d * 0.8))


def sc_objections(c, t, d, T, a):
    sky(c, T=T, stars=False)
    icon(c, "avalanche", 300, 300, prog(t, 0, 0.6), T)
    text(c, "Avalanche theory", 420, 320, 56, INK, prog(t, 0, 0.6), align="left")
    rows = ["Slope too gentle (~23°)", "No avalanche debris found", "Hours after they went to sleep"]
    starts = [0.42, 0.6, 0.78]
    for i, s in enumerate(rows):
        ap = prog(t, d * starts[i], d * starts[i] + 0.4)
        y = 520 + i * 150
        rgba(c, (0.14, 0.17, 0.27), ap)
        rrect(c, 300, y - 70, 1320, 110, 18)
        c.fill()
        xmark(c, 380, y - 15, 24, ap)
        text(c, s, 450, y, 48, INK, ap, align="left")


def sc_study(c, t, d, T, a):
    sky(c, T=T, stars=False)
    xs = [(1959, 360), (2019, 960), (2021, 1560)]
    line(c, 300, 260, 1620, 260, 5, DIM)
    for i, (yr, x) in enumerate(xs):
        ap = prog(t, i * d * 0.2, i * d * 0.2 + 0.5)
        rgba(c, RED if yr == 2021 else INK, ap)
        c.arc(x, 260, 16, 0, 2 * math.pi)
        c.fill()
        text(c, str(yr), x, 220, 40, INK, ap)
    text(c, "case reopened", 960, 320, 30, DIM, prog(t, d * 0.2, d * 0.3), bold=False)
    ap = prog(t, d * 0.4, d * 0.5)
    rgba(c, (0.93, 0.92, 0.88), ap)
    rrect(c, 1100, 400, 640, 420, 18)
    c.fill()
    dark = (0.15, 0.15, 0.2)
    text(c, "Communications", 1420, 480, 38, dark, ap)
    text(c, "Earth & Environment", 1420, 530, 38, dark, ap)
    text(c, "2021", 1420, 590, 32, RED, ap)
    for j in range(4):
        line(c, 1160, 650 + j * 36, 1680 - (j % 2) * 120, 650 + j * 36, 5, (0.6, 0.6, 0.6), ap)
    for i, (n, org, x) in enumerate([("Johan Gaume", "EPFL", 380), ("Alexander Puzrin", "ETH Zurich", 760)]):
        stick(c, x, 860, 1.5, a=ap)
        text(c, n, x, 920, 34, INK, ap)
        text(c, org, x, 965, 30, DIM, ap, bold=False)


def sc_slab(c, t, d, T, a):
    """Cross-section of the cut slope. mode build: snow loads then slab releases. hit: aftermath."""
    sky(c, T=T)
    hit = a.get("mode") == "hit"
    ang = math.radians(28)
    # slope line through (W/2, H/2) rising to the right
    def sy(x):
        return 640 - (x - 960) * math.tan(ang)
    cut_x0, cut_x1 = 820, 1080
    floor = sy(cut_x0)
    c.move_to(-100, sy(-100))
    c.line_to(cut_x0, floor)
    c.line_to(cut_x1, floor)
    c.line_to(cut_x1, sy(cut_x1))
    c.line_to(W + 100, sy(W + 100))
    c.line_to(W + 100, H + 200)
    c.line_to(-100, H + 200)
    c.close_path()
    rgba(c, (0.70, 0.76, 0.86))
    c.fill()
    # wind-loaded snow above the cut
    load = 1.0 if hit else prog(t, d * 0.45, d * 0.8)
    th = 70 * load
    released = 1.0 if hit else prog(t, d * 0.84, d * 0.97)
    if th > 0:
        shift = released * 150
        c.save()
        c.translate(-shift * math.cos(ang), shift * math.sin(ang) * 0.6)
        c.move_to(cut_x1, sy(cut_x1))
        c.line_to(cut_x1 + 380, sy(cut_x1 + 380))
        c.line_to(cut_x1 + 380, sy(cut_x1 + 380) - th)
        c.line_to(cut_x1, sy(cut_x1) - th)
        c.close_path()
        rgba(c, (0.95, 0.97, 1.0))
        c.fill_preserve()
        c.set_line_width(3)
        rgba(c, (0.5, 0.6, 0.75))
        c.stroke()
        c.restore()
    # tent in the cut (sits flat)
    crushed = released
    c.save()
    c.translate(950, floor)
    h = 80 * (1 - 0.65 * crushed)
    c.move_to(-110, 0); c.line_to(-80, -h); c.line_to(80, -h); c.line_to(110, 0); c.close_path()
    rgba(c, (0.22, 0.30, 0.20)); c.fill()
    c.restore()
    if not hit:
        wp = prog(t, d * 0.4, d * 0.85)
        for k in range(7):
            ox = (T * 400 + k * 160) % 900
            x = 1900 - ox
            y = sy(x) - 120 - (k % 3) * 40
            line(c, x, y, x - 70, y + 70 * math.tan(ang) * 0.5, 5, (0.6, 0.85, 1.0), 0.8 * wp)
        label(c, "1. cut into the slope", 950, floor + 110, 34, a=prog(t, d * 0.15, d * 0.25))
        label(c, "2. wind loads snow above", 1500, 260, 34, (0.6, 0.85, 1.0), wp)
        if released > 0:
            label(c, "3. slab releases", 1200, 160, 40, RED, released)
            line(c, cut_x1 + 380, sy(cut_x1 + 380) - 70, cut_x1 + 380, sy(cut_x1 + 380) + 6, 6, RED, released)
    else:
        label(c, "slab: a few meters", 1350, 330, 38, a=prog(t, 0.3, 0.9))
        ap = prog(t, d * 0.45, d * 0.6)
        label(c, "Snow simulation code from Disney's Frozen", W / 2, 140, 40, AMBER, ap)
        ap2 = prog(t, d * 0.82, d * 0.9)
        for k in range(3):
            stick(c, 880 + k * 60, floor - 6, 0.38, col=INK, a=ap2, lying=-math.pi / 2)
        line(c, 830, floor - 2, 1070, floor - 2, 5, AMBER, ap2)
        label(c, "lying on skis", 950, floor + 110, 34, AMBER, ap2)
    snowfall(c, T, 0.5, 1.8)


def sc_flee(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c)
    slope(c)
    tx = 1400
    later = prog(t, d * 0.78, d * 0.9)
    tent(c, tx, slope_y(tx) + 6, 1.0, cut=1, crushed=0.5, buried=0.3 + 0.4 * later)
    p = prog(t, 0.5, d * 0.7)
    for i in range(9):
        f = clamp(p - i * 0.03)
        x = tx - 80 - (tx - 520) * f
        stick(c, x, slope_y(x) + 6, 0.55, phase=T * 6 + i if 0 < f < 1 else None, a=1 - later)
    if later > 0:
        label(c, "weeks later: wind & fresh snow", 1100, 220, 42, AMBER, later)
    snowfall(c, T, 0.4 + 0.6 * later, 1.0 + 2.0 * later)


def sc_unsolved(c, t, d, T, a):
    sky(c, T=T, stars=False)
    rows = [("Why they fled the tent", True), ("Chest & skull injuries", True), ("Little visible debris", True),
            ("Traces of radiation", False)]
    for i, (s, ok) in enumerate(rows):
        ap = prog(t, 0.3 + i * 0.8, 0.7 + i * 0.8) if ok else prog(t, d * 0.2, d * 0.3)
        y = 300 + i * 160
        rgba(c, (0.14, 0.17, 0.27), ap)
        rrect(c, 360, y - 70, 1200, 110, 18)
        c.fill()
        if ok:
            check(c, 440, y - 15, 24, ap)
        else:
            text(c, "?", 440, y + 5, 70, RED, ap)
        text(c, s, 510, y, 48, INK, ap, align="left")


def sc_memorial(c, t, d, T, a):
    dawn = prog(t, 0, d)
    bot = tuple(BG2[i] * (1 - dawn) + (0.75, 0.45, 0.35)[i] * dawn for i in range(3))
    sky(c, bot=bot, T=T)
    far_mountains(c, col=(0.05, 0.06, 0.10), base=820)
    rgba(c, (0.05, 0.06, 0.10))
    c.rectangle(-400, 820, W + 800, 700)
    c.fill()
    for i in range(9):
        stick(c, 360 + i * 150, 820, 1.1, col=(0.02, 0.02, 0.04))
    for i, n in enumerate(NAMES9):
        ap = prog(t, 0.4 + i * 0.35, 0.9 + i * 0.35)
        text(c, n, 360 + i * 150, 880 + (i % 2) * 44, 24, INK, ap, bold=False)
    text(c, "DYATLOV PASS", W / 2, 300, 96, INK, prog(t, d * 0.55, d * 0.7))


def sc_outro(c, t, d, T, a):
    sky(c, T=T)
    far_mountains(c, base=900)
    if a.get("short"):
        text(c, "Would you have run?", W / 2, 360, 80, INK, prog(t, 0, 0.5))
    else:
        text(c, "What really happened?", W / 2, 300, 80, INK, prog(t, 0, 0.5))
        text(c, "Tell me in the comments", W / 2, 390, 44, DIM, prog(t, 1.0, 1.6), bold=False)
    ap = prog(t, d * 0.5, d * 0.6)
    pulse = 1 + 0.05 * math.sin(T * 6)
    c.save()
    c.translate(W / 2, 640)
    c.scale(pulse, pulse)
    rgba(c, RED, ap)
    rrect(c, -230, -60, 460, 120, 60)
    c.fill()
    text(c, "SUBSCRIBE", 0, 18, 52, INK, ap)
    c.restore()
    stick(c, W / 2 - 420, 900, 1.3, arms=(0.35, -2.0), a=ap)
    snowfall(c, T, 0.5)


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}
