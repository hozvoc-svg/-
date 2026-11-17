"""The Quiet Money: dark premium infographic scenes with two recurring stick characters.

Joe (blue) is the everyday viewer; the Billionaire (gold, top hat) plays the rich.
Long-form scenes draw on the full 1920x1080 canvas; Shorts scenes (prefix v_) draw in the central
9:16 column that build.py's VERTICAL_FILL mode scales up to 1080x1920.
"""
import math, random
import cairo
from scenes import W, H, INK, clamp, ease, prog, rgba, text, text_w, rrect, line, vignette, snowfall, stick
from short_scenes import hook  # noqa: F401  (Shorts hook text, used by build.py)

BG1 = (0.02, 0.035, 0.08)
GOLD = (1.0, 0.78, 0.25)
BLUE = (0.30, 0.75, 1.0)
GREEN = (0.35, 1.0, 0.60)
RED = (1.0, 0.36, 0.40)
DIM = (0.60, 0.66, 0.78)
WHITE = (0.96, 0.97, 1.0)
CW = 608
X0 = (W - CW) / 2
_R = random.Random(7)
DUST = [(_R.random() * W, _R.random() * H, _R.random() * 2 + 0.6, _R.random() * 6.28, _R.random() * 0.6 + 0.2) for _ in range(90)]


# ---------------- primitives ----------------

def glow(c, x, y, r, col=GOLD, a=1.0):
    g = cairo.RadialGradient(x, y, 1, x, y, r)
    g.add_color_stop_rgba(0, *col, 0.5 * a)
    g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def big(c, s, x, y, size, col=WHITE, a=1.0, align="center", outline=0.0, family="Inter Display Black", glow_a=0.0):
    """Heavy display text; returns its width."""
    c.select_font_face(family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    e = c.text_extents(s)
    x0 = {"center": x - e.x_advance / 2, "left": x, "right": x - e.x_advance}[align]
    if glow_a > 0:
        glow(c, x0 + e.x_advance / 2, y - size * 0.35, max(e.x_advance * 0.7, size * 1.2), col, glow_a * a)
    c.new_path()
    c.move_to(x0, y)
    c.text_path(s)
    if outline:
        rgba(c, (0, 0, 0), 0.9 * a); c.set_line_width(size * outline); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgba(c, col, a)
    c.fill()
    return e.x_advance


def small(c, s, x, y, size=34, col=DIM, a=1.0, align="center", bold=False):
    return text(c, s, x, y, size, col, a, align=align, bold=bold)


def pop(t, t0, dur=0.35):
    """0 before t0, overshoots slightly to ~1.08 then settles at 1."""
    u = clamp((t - t0) / dur)
    if u <= 0:
        return 0.0
    return 1 + 0.12 * math.sin(u * math.pi) * (1 - u) * 2 if u < 1 else 1.0 if u >= 1 else u


def ap(t, t0, dur=0.4):
    return ease((t - t0) / dur)


def scaled(c, x, y, s, fn):
    if s <= 0.001:
        return
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(-x, -y); fn(); c.restore()


def card(c, x, y, w, h, a=1.0, col=(1, 1, 1), border=None, r=26):
    rgba(c, col, 0.07 * a); rrect(c, x, y, w, h, r); c.fill()
    c.set_line_width(2); rgba(c, border or (1, 1, 1), (0.5 if border else 0.18) * a); rrect(c, x, y, w, h, r); c.stroke()


def arrow(c, x1, y1, x2, y2, p=1.0, col=WHITE, w=6, a=1.0, head=22):
    if p <= 0:
        return
    xe, ye = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
    line(c, x1, y1, xe, ye, w, col, a)
    ang = math.atan2(ye - y1, xe - x1)
    rgba(c, col, a)
    c.move_to(xe + math.cos(ang) * 4, ye + math.sin(ang) * 4)
    c.line_to(xe - head * math.cos(ang - 0.45), ye - head * math.sin(ang - 0.45))
    c.line_to(xe - head * math.cos(ang + 0.45), ye - head * math.sin(ang + 0.45))
    c.close_path(); c.fill()


def money(v):
    if v >= 1e9:
        return f"${v / 1e9:,.1f}B".replace(".0B", "B")
    if v >= 1e6:
        return f"${v / 1e6:,.1f}M".replace(".0M", "M")
    return f"${v:,.0f}"


def coin(c, x, y, r=40, a=1.0, col=GOLD):
    c.save(); c.translate(x, y)
    rgba(c, tuple(v * 0.65 for v in col), a); c.arc(0, 4, r, 0, 2 * math.pi); c.fill()
    rgba(c, col, a); c.arc(0, 0, r, 0, 2 * math.pi); c.fill()
    c.set_line_width(r * 0.08); rgba(c, tuple(v * 0.75 for v in col), a); c.arc(0, 0, r * 0.78, 0, 2 * math.pi); c.stroke()
    big(c, "$", 0, r * 0.38, r * 1.05, tuple(v * 0.6 for v in col), a)
    c.restore()


def coin_stack(c, x, y, n, r=46, a=1.0, col=GOLD):
    for k in range(int(n)):
        c.save(); c.translate(x, y - k * 14); c.scale(1, 0.32)
        rgba(c, tuple(v * 0.62 for v in col), a); c.arc(0, 9, r, 0, 2 * math.pi); c.fill()
        rgba(c, col, a); c.arc(0, 0, r, 0, 2 * math.pi); c.fill()
        c.restore()


def coin_pile(c, x, y, w=420, rows=6, a=1.0):
    for r_ in range(rows):
        n = rows - r_
        for k in range(n):
            xx = x - (n - 1) * w / rows / 2 + k * w / rows
            coin_stack(c, xx, y - r_ * 60, 4, r=w / rows * 0.48, a=a)


def bill(c, x, y, w=150, a=1.0, rot=0.0):
    h = w * 0.45
    c.save(); c.translate(x, y); c.rotate(rot)
    rgba(c, (0.25, 0.62, 0.38), a); rrect(c, -w / 2, -h / 2, w, h, 8); c.fill()
    c.set_line_width(3); rgba(c, (0.6, 0.9, 0.65), a); rrect(c, -w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 6); c.stroke()
    big(c, "$", 0, h * 0.25, h * 0.7, (0.75, 1.0, 0.8), a)
    c.restore()


def cash_stack(c, x, y, n=5, w=170, a=1.0):
    for k in range(n):
        bill(c, x + (k % 2) * 4, y - k * 12, w, a)


def top_hat(c, x, y, s, col, a):
    rgba(c, (0.08, 0.08, 0.10), a)
    c.rectangle(x - 30 * s, y - 6 * s, 60 * s, 8 * s); c.fill()
    c.rectangle(x - 19 * s, y - 50 * s, 38 * s, 46 * s); c.fill()
    rgba(c, col, a); c.rectangle(x - 19 * s, y - 16 * s, 38 * s, 7 * s); c.fill()


def joe(c, x, y, s=1.0, a=1.0, T=0.0, **kw):
    """The everyday guy (blue)."""
    b = math.sin(T * 2.2) * 2 * s
    stick(c, x, y + b * 0, s, BLUE, a, **kw)
    glow(c, x, y - 118 * s, 40 * s, BLUE, 0.35 * a)


def rich(c, x, y, s=1.0, a=1.0, T=0.0, hat=True, **kw):
    """The billionaire (gold, top hat)."""
    glow(c, x, y - 60 * s, 160 * s, GOLD, 0.25 * a)
    stick(c, x, y, s, GOLD, a, **kw)
    if hat and not kw.get("lying"):
        top_hat(c, x, y - 132 * s, s, GOLD, a)


def bank(c, x, y, s=1.0, a=1.0):
    col = (0.80, 0.84, 0.92)
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, col, a)
    c.move_to(-170, -260); c.line_to(0, -340); c.line_to(170, -260); c.close_path(); c.fill()
    c.rectangle(-160, -255, 320, 22); c.fill()
    for k in range(5):
        c.rectangle(-140 + k * 64, -225, 26, 190); c.fill()
    c.rectangle(-180, -30, 360, 30); c.fill()
    big(c, "BANK", 0, -278, 30, BG1, a)
    c.restore()


def share_cert(c, x, y, w=200, a=1.0, label="SHARES", rot=0.0, col=GOLD):
    h = w * 0.62
    c.save(); c.translate(x, y); c.rotate(rot)
    rgba(c, (0.96, 0.93, 0.84), a); rrect(c, -w / 2, -h / 2, w, h, 6); c.fill()
    c.set_line_width(4); rgba(c, col, a); rrect(c, -w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 4); c.stroke()
    big(c, label, 0, -h * 0.05, w * 0.13, (0.35, 0.28, 0.12), a)
    for k in range(3):
        line(c, -w * 0.32, h * 0.12 + k * h * 0.11, w * 0.32, h * 0.12 + k * h * 0.11, 2.5, (0.6, 0.55, 0.45), a)
    c.restore()


def house_icon(c, x, y, s=1.0, col=WHITE, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); rgba(c, col, a)
    c.move_to(-60, -40); c.line_to(0, -90); c.line_to(60, -40); c.close_path(); c.fill()
    c.rectangle(-48, -42, 96, 72); c.fill()
    rgba(c, BG1, a); c.rectangle(-14, -2, 28, 32); c.fill()
    c.restore()


def jet_icon(c, x, y, s=1.0, col=WHITE, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); rgba(c, col, a)
    c.move_to(-80, 0); c.curve_to(-60, -14, 50, -14, 80, -4); c.line_to(80, 4); c.curve_to(50, 14, -60, 14, -80, 0); c.fill()
    c.move_to(-10, -6); c.line_to(-40, -50); c.line_to(-25, -50); c.line_to(20, -6); c.fill()
    c.move_to(-10, 6); c.line_to(-40, 50); c.line_to(-25, 50); c.line_to(20, 6); c.fill()
    c.move_to(-75, -2); c.line_to(-88, -30); c.line_to(-78, -30); c.line_to(-60, -4); c.fill()
    c.restore()


def yacht_icon(c, x, y, s=1.0, col=WHITE, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); rgba(c, col, a)
    c.move_to(-90, 0); c.line_to(90, 0); c.line_to(70, 30); c.line_to(-75, 30); c.close_path(); c.fill()
    c.move_to(-50, 0); c.line_to(-40, -26); c.line_to(50, -26); c.line_to(65, 0); c.close_path(); c.fill()
    c.rectangle(-25, -46, 55, 20); c.fill()
    c.restore()


def chart_icon(c, x, y, s=1.0, col=GREEN, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    pts = [(-60, 40), (-30, 10), (-5, 25), (25, -15), (60, -45)]
    c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    rgba(c, col, a); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke()
    arrow(c, 25, -15, 66, -50, 1, col, 10, a, 24)
    c.restore()


def factory_icon(c, x, y, s=1.0, col=WHITE, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); rgba(c, col, a)
    c.move_to(-70, 40); c.line_to(-70, -10); c.line_to(-35, 10); c.line_to(-35, -10); c.line_to(0, 10); c.line_to(0, -10)
    c.line_to(35, 10); c.line_to(35, -60); c.line_to(55, -60); c.line_to(55, 10); c.line_to(70, 10); c.line_to(70, 40); c.close_path(); c.fill()
    c.restore()


def tree_icon(c, x, y, s=1.0, col=GREEN, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.55, 0.40, 0.25), a); c.rectangle(-8, -10, 16, 50); c.fill()
    rgba(c, col, a); c.arc(0, -35, 38, 0, 2 * math.pi); c.fill(); c.arc(-25, -15, 26, 0, 2 * math.pi); c.fill(); c.arc(25, -15, 26, 0, 2 * math.pi); c.fill()
    c.restore()


def lock_icon(c, x, y, s=1.0, col=GOLD, a=1.0, shut=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_line_width(16); rgba(c, col, a)
    lift = (1 - shut) * 40
    c.arc(0, -40 - lift, 42, math.pi, 0); c.stroke()
    line(c, -42, -40 - lift, -42, -10 - lift * 0.0, 16, col, a)
    line(c, 42, -40 - lift, 42, -10 - lift, 16, col, a)
    rrect(c, -70, -20, 140, 110, 18); c.fill()
    rgba(c, BG1, a); c.arc(0, 25, 14, 0, 2 * math.pi); c.fill(); c.rectangle(-6, 25, 12, 30); c.fill()
    c.restore()


def doc(c, x, y, w, h, a=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    rgba(c, (0, 0, 0), 0.35 * a); rrect(c, -w / 2 + 10, -h / 2 + 14, w, h, 10); c.fill()
    rgba(c, (0.96, 0.95, 0.92), a); rrect(c, -w / 2, -h / 2, w, h, 10); c.fill()
    c.restore()


def stamp(c, s, x, y, size, col, p, rot=-0.12):
    if p <= 0:
        return
    sc = 1 + 1.5 * (1 - ease(p / 1.0)) if p < 1 else 1
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    a = clamp(p * 2)
    w = text_w(c, s, size) * 1.25 + 60
    c.set_line_width(size * 0.12); rgba(c, col, a)
    rrect(c, -w / 2, -size * 0.95, w, size * 1.35, 14); c.stroke()
    big(c, s, 0, size * 0.32, size, col, a)
    c.restore()


def gravestone(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.45, 0.48, 0.56), a)
    c.move_to(-110, 0); c.line_to(-110, -220); c.arc(0, -220, 110, math.pi, 0); c.line_to(110, 0); c.close_path(); c.fill()
    rgba(c, (0.32, 0.35, 0.42), a); c.rectangle(-150, 0, 300, 26); c.fill()
    big(c, "R.I.P.", 0, -210, 54, (0.22, 0.24, 0.30), a)
    coin(c, 0, -110, 36, a)
    c.restore()


def bg(c, T, a=None, glows=True):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.035, 0.055, 0.12)
    g.add_color_stop_rgb(1, 0.010, 0.018, 0.045)
    c.set_source(g)
    c.rectangle(-W, -H, 3 * W, 3 * H); c.fill()
    off = (T * 8) % 80
    c.set_line_width(1)
    rgba(c, (0.35, 0.45, 0.65), 0.07)
    for i in range(-1, W // 80 + 2):
        c.move_to(i * 80 + off, -50); c.line_to(i * 80 + off, H + 50)
    for j in range(-1, H // 80 + 2):
        c.move_to(-50, j * 80 + off * 0.5); c.line_to(W + 50, j * 80 + off * 0.5)
    c.stroke()
    if glows:
        glow(c, 380 + 60 * math.sin(T * 0.21), 260, 620, (0.25, 0.35, 0.9), 0.22)
        glow(c, 1560 + 60 * math.cos(T * 0.17), 860, 620, (0.9, 0.6, 0.15), 0.12)
    for x, y, r, ph, sp in DUST:
        yy = (y - T * 14 * sp) % H
        rgba(c, (0.9, 0.85, 0.7), 0.10 + 0.12 * (0.5 + 0.5 * math.sin(T * 1.3 + ph)))
        c.arc(x + 8 * math.sin(T * 0.5 + ph), yy, r, 0, 2 * math.pi); c.fill()
    if a is not None and a.get("chap"):
        pass


def chapter_tag(c, t, s):
    """Gold chapter pill that slides in at the top-left for the first seconds of a chapter."""
    if not s or t > 5.2:
        return
    p = ap(t, 0.2, 0.5) * (1 - ap(t, 4.6, 0.5))
    c.save(); c.translate(-40 * (1 - p), 0)
    w = text_w(c, s.upper(), 30) + 70
    rgba(c, GOLD, 0.95 * p); rrect(c, 80, 60, w, 62, 31); c.fill()
    text(c, s.upper(), 80 + w / 2, 102, 30, BG1, p)
    c.restore()


def source(c, s, a=1.0):
    small(c, s, W / 2, H - 30, 24, (0.5, 0.55, 0.66), a)


def step_header(c, t, n, word, y=250):
    small(c, f"STEP {n}", W / 2, y - 150, 44, GOLD, ap(t, 0.1), bold=True)
    s = pop(t, 0.35, 0.45)
    scaled(c, W / 2, y, s, lambda: big(c, word, W / 2, y, 190, WHITE, 1, glow_a=0.35))


# ---------------- long-form scenes ----------------

def sc_zero_tax(c, t, d, T, a):
    bg(c, T)
    coin_pile(c, 1450, 900, 520, 6)
    rich(c, 1450, 560, 1.5, T=T, arms=(0.6, -2.4))
    small(c, f"FEDERAL INCOME TAX · {a.get('year', '2018')}", 640, 300, 40, DIM, ap(t, 0.2), bold=True)
    v = 48_000_000 * (1 - ease((t - 0.4) / 1.6))
    s = money(max(0, v)) if v > 1 else "$0"
    col = GREEN if v <= 1 else WHITE
    big(c, s, 640, 560, 230 if v <= 1 else 150, col, ap(t, 0.3), glow_a=0.5 if v <= 1 else 0)
    small(c, "One of the richest people on Earth", 640, 660, 36, DIM, ap(t, 2.4))
    stamp(c, "100% LEGAL", 640, 820, 70, GREEN, (t - 4.2) / 0.5)


def sc_vs_teacher(c, t, d, T, a):
    bg(c, T)
    line(c, W / 2, 140, W / 2, 960, 2, (1, 1, 1), 0.15)
    scaled(c, W / 2, 540, pop(t, 0.2), lambda: big(c, "VS", W / 2, 570, 80, GOLD))
    # left: teacher
    joe(c, 480, 860, 1.6, T=T, head_hold=1.0 if t > 4 else 0.0)
    small(c, "TEACHER", 480, 220, 48, BLUE, ap(t, 0.2), bold=True)
    small(c, "$60,000 salary", 480, 275, 34, DIM, ap(t, 0.3))
    p = ap(t, 1.0, 3.0)
    card(c, 180, 330, 600, 140, ap(t, 0.5))
    rgba(c, RED, 0.85); rrect(c, 205, 400, 550 * p * 0.85, 40, 20); c.fill()
    small(c, "Taxes paid", 205, 380, 30, DIM, ap(t, 0.5), align="left")
    big(c, f"≈ ${int(11000 * p):,}", 755, 382, 44, RED, ap(t, 0.8), align="right")
    # right: billionaire
    coin_pile(c, 1440, 900, 380, 5, ap(t, 0.4))
    rich(c, 1440, 640, 1.4, T=T)
    small(c, "BILLIONAIRE", 1440, 220, 48, GOLD, ap(t, 0.3), bold=True)
    small(c, "$100,000,000,000+", 1440, 275, 34, DIM, ap(t, 0.4))
    card(c, 1140, 330, 600, 140, ap(t, 0.6))
    small(c, "Federal income tax", 1165, 380, 30, DIM, ap(t, 0.6), align="left")
    big(c, "$0", 1715, 382, 44, GREEN, ap(t, 0.9), align="right")


def sc_rate_bars(c, t, d, T, a):
    bg(c, T)
    big(c, "TRUE TAX RATE", W / 2, 150, 72, WHITE, ap(t, 0.1))
    base = 880
    for lab, val, colr, x, t0 in (("Typical household", 14.0, BLUE, 700, 0.6), ("25 richest Americans", 3.4, GOLD, 1220, 1.4)):
        p = ap(t, t0 + d * 0.35, 1.2)
        h = 470 * val / 14.0 * p
        glow(c, x, base - h, 220, colr, 0.25 * p)
        rgba(c, colr); rrect(c, x - 120, base - h, 240, max(h, 1), 14); c.fill()
        if p > 0.05:
            big(c, f"{val * p:.1f}%", x, base - h - 30, 96, colr, p)
        small(c, lab, x, base + 60, 40, WHITE, ap(t, t0), bold=True)
    joe(c, 430, base, 1.2, T=T, a=ap(t, 0.8))
    rich(c, 1500, base, 1.2, T=T, a=ap(t, 1.6), arms=(0.5, -2.3))
    p = ap(t, 2.5)
    card(c, 640, 190, 640, 80, p, border=GOLD)
    small(c, "Wealth grew $401B  ·  Taxes paid $13.6B", W / 2, 243, 34, WHITE, p, bold=True)
    source(c, "Source: ProPublica, “The Secret IRS Files” (2021), IRS data 2014–2018", ap(t, 1))


def sc_question(c, t, d, T, a):
    bg(c, T)
    tilt = 0.18 * ap(t, 0.8, 1.5)
    cx, cy = W / 2, 430
    rgba(c, (0.8, 0.84, 0.92)); c.rectangle(cx - 10, cy, 20, 430); c.fill(); c.rectangle(cx - 120, cy + 420, 240, 24); c.fill()
    c.save(); c.translate(cx, cy); c.rotate(-tilt)
    line(c, -520, 0, 520, 0, 14, (0.8, 0.84, 0.92))
    c.restore()
    for side, lab, val, colr in ((-1, "TEACHER", "14%", BLUE), (1, "BILLIONAIRE", "3.4%", GOLD)):
        px = cx + side * 520 * math.cos(tilt)
        py = cy - side * 520 * math.sin(tilt)
        line(c, px, py, px - 120, py + 180, 3, DIM); line(c, px, py, px + 120, py + 180, 3, DIM)
        rgba(c, colr, 0.9); c.move_to(px - 150, py + 180); c.curve_to(px - 100, py + 250, px + 100, py + 250, px + 150, py + 180); c.close_path(); c.fill()
        big(c, val, px, py + 165, 80, colr)
        small(c, lab, px, py + 300, 36, WHITE, bold=True)
    scaled(c, cx, 250, pop(t, d * 0.45), lambda: big(c, "HOW?", cx, 270, 150, GOLD, glow_a=0.4))


def sc_title(c, t, d, T, a):
    bg(c, T)
    words = [("BUY.", WHITE, 0.2), ("BORROW.", GOLD, 0.8), ("DIE.", RED, 1.4)]
    c.select_font_face("Inter Display Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(170)
    ws = [c.text_extents(wd).x_advance for wd, _, _ in words]
    x = W / 2 - (sum(ws) + 50 * 2) / 2
    for (wd, colr, t0), w in zip(words, ws):
        s = pop(t, t0, 0.4)
        scaled(c, x + w / 2, 540, s, lambda wd=wd, colr=colr, x=x: big(c, wd, x, 600, 170, colr, align="left", glow_a=0.3))
        x += w + 50
    small(c, "THE BILLIONAIRE TAX PLAYBOOK", W / 2, 760, 46, DIM, ap(t, 2.0), bold=True)
    sweep = (t * 0.5) % 2.0
    if sweep < 1:
        g = cairo.LinearGradient(sweep * 2400 - 300, 0, sweep * 2400, 0)
        g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(0.5, 1, 1, 1, 0.07); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(g); c.paint()


def sc_two_money(c, t, d, T, a):
    bg(c, T)
    big(c, "THE TAX SYSTEM TAXES INCOME, NOT WEALTH", W / 2, 230, 58, WHITE, ap(t, d * 0.25))
    for i, (lab, sub, colr, x) in enumerate((("INCOME", "Taxed on every paycheck", BLUE, 560), ("WEALTH", "Taxed only when you sell", GOLD, 1360))):
        p = ap(t, d * 0.55 + i * 0.4)
        c.save(); c.translate(0, 60 * (1 - p))
        card(c, x - 330, 330, 660, 560, p, border=colr)
        if i == 0:
            cash_stack(c, x, 560, 5, 220, p)
        else:
            chart_icon(c, x, 520, 1.8, GREEN, p)
        big(c, lab, x, 740, 90, colr, p)
        small(c, sub, x, 810, 36, WHITE, p)
        c.restore()
    chapter_tag(c, t, a.get("chap"))


def sc_paycheck(c, t, d, T, a):
    bg(c, T)
    joe(c, 1600, 860, 1.6, T=T, arms=(0.9, -0.9))
    cuts = [("Federal tax", RED), ("State tax", (1.0, 0.55, 0.3)), ("Social Security", (0.9, 0.4, 0.7)), ("Medicare", (0.7, 0.5, 1.0))]
    u = (t % 8.0) / 8.0
    x = 250 + 1150 * ease(u / 0.9)
    w = 520
    for k, (lab, colr) in enumerate(cuts):
        tk = 0.15 + k * 0.17
        if u > tk:
            q = clamp((u - tk) / 0.3)
            rx, ry = 400 + k * 260, 520 - 330 * ease(q)
            rgba(c, colr, 1 - q * 0.6); rrect(c, rx - 90, ry - 30, 180, 60, 10); c.fill()
            small(c, lab, rx, ry - 50, 30, colr, 1 - q * 0.6, bold=True)
            w -= 70
    card(c, x - w / 2, 470, w, 160, 1, border=GREEN)
    big(c, "PAYCHECK", x, 545, 48, WHITE)
    small(c, f"${4000 - int((520 - w) / 70) * 420:,}", x, 600, 38, GREEN, bold=True)
    big(c, "TAXED BEFORE YOU SEE IT", W / 2, 960, 60, WHITE, ap(t, 0.3))


def sc_stock_grow(c, t, d, T, a):
    bg(c, T)
    x0, y0, x1, y1 = 260, 860, 1460, 260
    line(c, x0, y0, x1 + 40, y0, 3, DIM, 0.5); line(c, x0, y0, x0, y1 - 40, 3, DIM, 0.5)
    p = ap(t, 0.5, d * 0.45)
    rng = random.Random(3)
    pts = []
    n = 60
    for k in range(n + 1):
        u = k / n
        v = u ** 2.2 + 0.03 * math.sin(k * 1.7) * u
        pts.append((x0 + (x1 - x0) * u, y0 - (y0 - y1) * v))
    m = max(2, int(n * p) + 1)
    c.set_line_width(8); c.set_line_join(cairo.LINE_JOIN_ROUND); rgba(c, GREEN)
    c.move_to(*pts[0])
    for q in pts[1:m]:
        c.line_to(*q)
    c.stroke()
    hx, hy = pts[m - 1]
    glow(c, hx, hy, 70, GREEN, 0.6); rgba(c, WHITE); c.arc(hx, hy, 10, 0, 2 * math.pi); c.fill()
    val = 1e6 * (1000 ** p)
    big(c, money(val), 1500, 300, 110, GREEN, align="left")
    small(c, "VALUE OF YOUR SHARES", 1500, 200, 32, DIM, align="left", bold=True)
    q = ap(t, d * 0.55)
    card(c, 1490, 460, 400, 170, q, border=GOLD)
    small(c, "Tax owed on growth", 1690, 520, 32, DIM, q)
    big(c, "$0", 1690, 600, 80, GOLD, q, glow_a=0.4)
    stamp(c, "UNREALIZED GAIN", 1690, 800, 40, GOLD, (t - d * 0.8) / 0.5)


def sc_salary_vs_stock(c, t, d, T, a):
    bg(c, T)
    coin_stack(c, 420, 860, 2, 40, ap(t, 0.3))
    small(c, "SALARY", 420, 680, 40, BLUE, ap(t, 0.3), bold=True)
    big(c, "$81,840", 420, 760, 64, WHITE, ap(t, 0.5))
    p = ap(t, d * 0.45, 2.0)
    for k in range(5):
        coin_stack(c, 1000 + k * 170, 900, int(38 * p * (0.75 + 0.25 * math.sin(k * 2.1 + 1))), 70)
    small(c, "STOCK", 1340, 220, 40, GOLD, ap(t, d * 0.45), bold=True)
    big(c, "$100B+", 1340, 330, 120, GOLD, ap(t, d * 0.5), glow_a=0.4)
    rich(c, 720, 880, 1.3, T=T, arms=(0.4, -2.2), a=ap(t, 0.2))
    source(c, "Amazon proxy statements: Jeff Bezos's base salary was $81,840 for years", ap(t, 1))


def sc_step_buy(c, t, d, T, a):
    bg(c, T)
    step_header(c, t, 1, "BUY")
    items = [("STOCKS", chart_icon, GREEN), ("COMPANIES", factory_icon, WHITE), ("REAL ESTATE", house_icon, WHITE), ("LAND", tree_icon, GREEN)]
    for k, (lab, fn, colr) in enumerate(items):
        x = 360 + k * 400
        p = pop(t, d * 0.35 + k * 0.45)
        def draw(x=x, fn=fn, colr=colr, lab=lab):
            card(c, x - 160, 470, 320, 360, 1, border=GOLD)
            fn(c, x, 640, 1.5, col=colr)
            big(c, lab, x, 790, 38, WHITE)
        scaled(c, x, 650, p, draw)
    chapter_tag(c, t, a.get("chap"))


def sc_never_sell(c, t, d, T, a):
    bg(c, T)
    shut = ap(t, 1.6, 0.6)
    p = 1 - 0.4 * shut
    rgba(c, RED, p); rrect(c, W / 2 - 280, 330, 560, 200, 100); c.fill()
    big(c, "SELL", W / 2, 470, 120, WHITE, p)
    cx = W / 2 + 420 - 260 * ap(t, 0.3, 1.0)
    cy = 640 - 110 * ap(t, 0.3, 1.0)
    rgba(c, WHITE); c.move_to(cx, cy); c.line_to(cx + 22, cy + 70); c.line_to(cx + 36, cy + 44); c.line_to(cx + 64, cy + 56); c.close_path(); c.fill()
    lock_icon(c, W / 2 + 330, 470, 1.2, GOLD, shut, shut=ap(t, 2.0, 0.4))
    big(c, "NO SALE  =  NO TAX", W / 2, 760, 96, GOLD, ap(t, d * 0.4), glow_a=0.3)
    rich(c, 300, 900, 1.2, T=T, arms=(0.3, -0.3))


def sc_need_cash(c, t, d, T, a):
    bg(c, T)
    rich(c, W / 2, 900, 1.6, T=T, head_hold=1.0 if t > d * 0.7 else 0.0)
    icons = [(house_icon, 520, 360, "MANSIONS"), (jet_icon, 960, 250, "JETS"), (yacht_icon, 1400, 360, "YACHTS")]
    for k, (fn, x, y, lab) in enumerate(icons):
        p = pop(t, d * 0.25 + k * 0.5)
        def draw(fn=fn, x=x, y=y, lab=lab):
            rgba(c, (1, 1, 1), 0.08); c.arc(x, y, 130, 0, 2 * math.pi); c.fill()
            fn(c, x, y + 10, 1.2)
            small(c, lab, x, y + 100, 30, GOLD, bold=True)
        scaled(c, x, y, p, draw)
    scaled(c, W / 2, 560, pop(t, d * 0.75), lambda: big(c, "CASH?", W / 2, 600, 110, GREEN, glow_a=0.4))


def sc_sell_tax(c, t, d, T, a):
    bg(c, T)
    cx, cy, r = 700, 560, 300
    frac = 0.238 * ap(t, 1.0, 1.5)
    rgba(c, GOLD); c.move_to(cx, cy); c.arc(cx, cy, r, -math.pi / 2 + frac * 2 * math.pi, 1.5 * math.pi); c.close_path(); c.fill()
    off = 40 * ap(t, 2.5)
    mid = -math.pi / 2 + frac * math.pi
    ox, oy = cx + off * math.cos(mid), cy + off * math.sin(mid)
    rgba(c, RED); c.move_to(ox, oy); c.arc(ox, oy, r, -math.pi / 2, -math.pi / 2 + frac * 2 * math.pi); c.close_path(); c.fill()
    big(c, "$1B SALE", cx, cy + r + 90, 60, WHITE)
    small(c, "Capital gains tax", 1280, 360, 40, DIM, ap(t, 0.5), align="left")
    big(c, "20% + 3.8%", 1280, 470, 96, WHITE, ap(t, 0.7), align="left")
    big(c, f"-${int(238 * ap(t, 1.0, 2.0))}M", 1280, 650, 130, RED, ap(t, 1.0), align="left", glow_a=0.3)
    small(c, "gone to the IRS", 1280, 720, 40, DIM, ap(t, 1.5), align="left")


def sc_borrow_bank(c, t, d, T, a):
    bg(c, T)
    step_header(c, t, 2, "BORROW", 230)
    bank(c, 1500, 900, 1.3)
    rich(c, 380, 900, 1.5, T=T, arms=(1.2, -0.3))
    u = ap(t, d * 0.35, 1.6)
    for k in range(3):
        share_cert(c, 560 + 700 * u + k * 16, 720 - k * 20 - 80 * math.sin(u * math.pi), 200, 1 - 0.5 * ap(t, d * 0.35 + 1.6, 0.4), rot=-0.1 + k * 0.05)
    small(c, "SHARES AS COLLATERAL", 960, 560, 34, GOLD, ap(t, d * 0.35) * (1 - ap(t, d * 0.6)), bold=True)
    v = ap(t, d * 0.65, 1.4)
    if v > 0:
        cash_stack(c, 1300 - 760 * v, 820 - 60 * math.sin(v * math.pi), 6, 180)
        small(c, "CASH LOAN", 1300 - 760 * v, 700, 34, GREEN, 1, bold=True)
    chapter_tag(c, t, a.get("chap"))


def sc_loan_not_income(c, t, d, T, a):
    bg(c, T)
    s = pop(t, 0.2)
    scaled(c, W / 2, 470, s, lambda: (big(c, "LOAN", 560, 520, 170, GREEN, glow_a=0.3), big(c, "INCOME", 1410, 520, 170, BLUE)))
    p = ap(t, 0.8, 0.5)
    line(c, 900, 440, 1020, 440, 14, WHITE, p); line(c, 900, 490, 1020, 490, 14, WHITE, p)
    line(c, 990, 400, 930, 530, 14, RED, ap(t, 1.2, 0.3))
    q = ap(t, d * 0.55)
    card(c, 560, 640, 800, 160, q, border=GOLD)
    small(c, "Income tax on borrowed money", W / 2, 705, 36, DIM, q)
    big(c, "$0", W / 2, 775, 70, GOLD, q)


def sc_loan_math(c, t, d, T, a):
    bg(c, T)
    big(c, "THE BILLIONAIRE MATH", W / 2, 160, 64, WHITE, ap(t, 0.1))
    p1 = ap(t, d * 0.15)
    card(c, 160, 240, 760, 560, p1, border=GREEN)
    small(c, "PORTFOLIO", 540, 320, 36, DIM, p1, bold=True)
    big(c, "$100M", 540, 440, 120, WHITE, p1)
    small(c, "grows 7% a year", 540, 520, 36, DIM, p1)
    g = ap(t, d * 0.25, 2.0)
    big(c, f"+${7 * g:.1f}M", 540, 690, 110, GREEN, p1, glow_a=0.3)
    p2 = ap(t, d * 0.5)
    card(c, 1000, 240, 760, 560, p2, border=RED)
    small(c, "LOAN TO LIVE ON", 1380, 320, 36, DIM, p2, bold=True)
    big(c, "$3M", 1380, 440, 120, WHITE, p2)
    small(c, "at 4% interest", 1380, 520, 36, DIM, p2)
    i = ap(t, d * 0.55, 2.0)
    big(c, f"-${int(120 * i)}K", 1380, 690, 110, RED, p2)
    q = ap(t, d * 0.8)
    card(c, 560, 860, 800, 110, q, border=GOLD)
    big(c, "INCOME TAX PAID: $0", W / 2, 935, 56, GOLD, q)


def sc_filings(c, t, d, T, a):
    bg(c, T)
    big(c, "IT'S IN PUBLIC FILINGS", W / 2, 170, 64, WHITE, ap(t, 0.1))
    docs = [("TESLA · PROXY STATEMENT", "Shares pledged as collateral", "to secure personal loans", 0.3, 560, -0.03),
            ("ORACLE · PROXY STATEMENT", "Shares pledged to secure", "credit lines", d * 0.6, 1360, 0.03)]
    for head, l1, l2, t0, x, rot in docs:
        p = ap(t, t0, 0.5)
        if p <= 0:
            continue
        c.save(); c.translate(0, 80 * (1 - p))
        doc(c, x, 580, 640, 600, p, rot)
        c.save(); c.translate(x, 580); c.rotate(rot)
        big(c, head, 0, -220, 36, (0.1, 0.12, 0.18), p)
        for k in range(3):
            line(c, -250, -150 + k * 40, 250 - k * 60, -150 + k * 40, 6, (0.75, 0.75, 0.75), p)
        hl = ap(t, t0 + 0.8, 0.8)
        rgba(c, (1.0, 0.85, 0.2), 0.55 * p); c.rectangle(-270, -20, 540 * hl, 110); c.fill()
        big(c, l1, 0, 20, 36, (0.1, 0.12, 0.18), p)
        big(c, l2, 0, 70, 36, (0.1, 0.12, 0.18), p)
        for k in range(3):
            line(c, -250, 150 + k * 40, 250 - k * 90, 150 + k * 40, 6, (0.75, 0.75, 0.75), p)
        c.restore(); c.restore()


def sc_rollover(c, t, d, T, a):
    bg(c, T)
    cx, cy, r = 760, 560, 260
    labels = ["NEW LOAN", "PAYS OLD LOAN", "BORROW AGAIN"]
    rot = T * 0.6
    for k in range(3):
        a0 = rot + k * 2 * math.pi / 3
        c.set_line_width(12); rgba(c, GOLD, 0.9)
        c.arc(cx, cy, r, a0 + 0.25, a0 + 2 * math.pi / 3 - 0.25); c.stroke()
        ae = a0 + 2 * math.pi / 3 - 0.25
        hx, hy = cx + r * math.cos(ae), cy + r * math.sin(ae)
        tang = ae + math.pi / 2
        rgba(c, GOLD); c.move_to(hx + 24 * math.cos(tang), hy + 24 * math.sin(tang))
        c.line_to(hx - 18 * math.cos(tang) + 18 * math.cos(ae), hy - 18 * math.sin(tang) + 18 * math.sin(ae))
        c.line_to(hx - 18 * math.cos(tang) - 18 * math.cos(ae), hy - 18 * math.sin(tang) - 18 * math.sin(ae)); c.close_path(); c.fill()
        la = -math.pi / 2 + k * 2 * math.pi / 3
        lx, ly = cx + (r + 200) * math.cos(la), cy + (r + 70) * math.sin(la) + (0 if k == 0 else 60)
        small(c, labels[k], lx, ly, 34, WHITE, ap(t, 0.3 + k * 0.4), bold=True)
    yr = 1 + int(29 * ap(t, 0.5, d * 0.8))
    big(c, f"YEAR {yr}", cx, cy + 25, 76, WHITE)
    for k, (lab, colr, g) in enumerate((("WEALTH", GREEN, 1.0), ("DEBT", RED, 0.25))):
        x = 1480 + k * 220
        h = 520 * g * (0.2 + 0.8 * ap(t, 0.5, d * 0.8))
        rgba(c, colr); rrect(c, x - 70, 860 - h, 140, h, 12); c.fill()
        small(c, lab, x, 910, 34, colr, bold=True)


def sc_step_die(c, t, d, T, a):
    bg(c, T, glows=False)
    glow(c, W / 2, 620, 600, (0.4, 0.5, 0.8), 0.2)
    step_header(c, t, 3, "DIE", 260)
    gravestone(c, W / 2, 920, 1.25, ap(t, 0.8))
    for k in range(5):
        x = 600 + k * 180
        if k == 2:
            continue
        rgba(c, (1.0, 0.85, 0.5), 0.6); c.rectangle(x - 6, 880, 12, 40); c.fill()
        glow(c, x, 870, 40 + 6 * math.sin(T * 9 + k), (1.0, 0.7, 0.3), 0.8)
    chapter_tag(c, t, a.get("chap"))


def sc_step_up(c, t, d, T, a):
    bg(c, T)
    base = 860
    p1 = ap(t, 0.3)
    rgba(c, BLUE, p1); rrect(c, 300, base - 30, 220, 30, 6); c.fill()
    small(c, "BOUGHT FOR", 410, base + 50, 30, DIM, p1, bold=True)
    big(c, "$1M", 410, base - 50, 60, BLUE, p1)
    p2 = ap(t, 1.5, 1.5)
    rgba(c, GOLD); rrect(c, 650, base - 600 * p2, 220, 600 * p2 + 1, 6); c.fill()
    small(c, "WORTH AT DEATH", 760, base + 50, 30, DIM, p2, bold=True)
    big(c, "$1B", 760, base - 600 * p2 - 30, 80, GOLD, p2)
    t3 = d * 0.42
    s3 = ap(t, t3, 1.4)
    rgba(c, BLUE, 0.4 + 0.6 * s3); rrect(c, 1080, base - 30 - 570 * s3, 220, 30 + 570 * s3, 6); c.fill()
    small(c, "HEIRS' NEW COST", 1190, base + 50, 30, DIM, ap(t, t3), bold=True)
    big(c, "$1B" if s3 > 0.95 else "$1M", 1190, base - 30 - 570 * s3 - 30, 70, BLUE, ap(t, t3))
    if s3 > 0:
        c.save(); c.set_dash([18, 14]); line(c, 640, base - 600, 1320, base - 600, 3, GOLD, s3); c.restore()
        arrow(c, 1360, base - 20, 1360, base - 560, s3, GOLD, 8)
        small(c, "STEP-UP", 1460, base - 300, 40, GOLD, s3, bold=True)
    t4 = d * 0.68
    q = ap(t, t4)
    card(c, 1420, 160, 440, 260, q, border=RED)
    small(c, "Taxable gain", 1640, 220, 32, DIM, q)
    big(c, "$999M", 1640, 310, 80, RED, q)
    line(c, 1490, 285, 1790, 285, 10, WHITE, ap(t, t4 + 1.0, 0.4) * q)
    big(c, "≈ $0", 1640, 395, 64, GREEN, ap(t, t4 + 1.2))


def sc_estate(c, t, d, T, a):
    bg(c, T)
    small(c, "ESTATE TAX", 520, 260, 44, DIM, ap(t, 0.2), bold=True)
    big(c, "40%", 520, 440, 200, RED, ap(t, 0.3), glow_a=0.3)
    small(c, "on fortunes above ~$15M per person", 520, 520, 34, WHITE, ap(t, 0.6))
    for k in range(5):
        u = ((t * 0.7 + k * 0.2) % 1.0)
        x = 760 + 520 * u
        if t > d * 0.45 and x > 1150:
            x = 1150
        arrow(c, x - 120, 380 + k * 60, x, 380 + k * 60, 1, RED, 6, 0.7)
    p = pop(t, d * 0.45)
    def shield():
        rgba(c, GOLD, 0.95)
        c.move_to(1300, 250); c.curve_to(1420, 300, 1500, 290, 1540, 270); c.line_to(1540, 520)
        c.curve_to(1520, 680, 1380, 760, 1300, 800); c.curve_to(1220, 760, 1080, 680, 1060, 520); c.line_to(1060, 270)
        c.curve_to(1100, 290, 1180, 300, 1300, 250); c.close_path(); c.fill()
        big(c, "TRUSTS", 1300, 540, 64, BG1)
    scaled(c, 1300, 520, p, shield)
    small(c, "+ armies of lawyers", 1300, 880, 40, GOLD, ap(t, d * 0.6), bold=True)


def sc_heirs_repay(c, t, d, T, a):
    bg(c, T)
    for k in range(3):
        stick(c, 300 + k * 130, 900, 1.0, GOLD, 1)
    small(c, "HEIRS", 430, 960, 34, GOLD, 1, bold=True)
    for k in range(6):
        share_cert(c, 860, 820 - k * 40, 240, 1)
    v = ap(t, d * 0.25, 1.4)
    share_cert(c, 860 + 640 * v, 580 - 120 * math.sin(v * math.pi), 240, 1 - 0.7 * ap(t, d * 0.25 + 1.4), rot=0.1)
    bank(c, 1560, 900, 1.0)
    debt = 1 - ap(t, d * 0.4, 1.8)
    card(c, 1300, 120, 520, 150, 1, border=RED if debt > 0.01 else GREEN)
    small(c, "LOANS OWED", 1560, 175, 32, DIM)
    big(c, money(300e6 * debt) if debt > 0.005 else "$0", 1560, 245, 64, RED if debt > 0.005 else GREEN)
    stamp(c, "KEEP THE REST", 860, 360, 50, GOLD, (t - d * 0.65) / 0.5)


def sc_cycle(c, t, d, T, a):
    bg(c, T)
    nodes = [("BUY", (W / 2, 260), WHITE), ("BORROW", (W / 2 + 430, 760), GOLD), ("DIE", (W / 2 - 430, 760), RED)]
    for k in range(3):
        (_, (x1, y1), _), (_, (x2, y2), _) = nodes[k], nodes[(k + 1) % 3]
        ang = math.atan2(y2 - y1, x2 - x1)
        sx, sy = x1 + 150 * math.cos(ang), y1 + 150 * math.sin(ang)
        ex, ey = x2 - 150 * math.cos(ang), y2 - 150 * math.sin(ang)
        arrow(c, sx, sy, ex, ey, ap(t, 0.5 + k * 0.6, 0.6), DIM, 6, 0.8)
        u = (T * 0.5 + k / 3) % 1
        glow(c, sx + (ex - sx) * u, sy + (ey - sy) * u, 30, GOLD, ap(t, 2.5))
    for k, (lab, (x, y), colr) in enumerate(nodes):
        scaled(c, x, y, pop(t, k * 0.6), lambda lab=lab, x=x, y=y, colr=colr: (
            card(c, x - 150, y - 80, 300, 160, 1, border=colr), big(c, lab, x, y + 25, 64, colr)))
    q = ap(t, d * 0.5)
    small(c, "INCOME TAX", W / 2, 580, 36, DIM, q, bold=True)
    big(c, "≈ 0", W / 2, 690, 110, GREEN, q, glow_a=0.3)
    gen = 1 + int(2.99 * ap(t, d * 0.55, d * 0.4))
    small(c, f"GENERATION {gen}", W / 2, 1000, 36, GOLD, q, bold=True)


def sc_legal(c, t, d, T, a):
    bg(c, T)
    cx, cy = 560, 540
    rgba(c, (0.8, 0.84, 0.92)); c.rectangle(cx - 8, cy - 220, 16, 420); c.fill(); c.rectangle(cx - 110, cy + 190, 220, 24); c.fill()
    sw = 0.08 * math.sin(T * 1.2)
    c.save(); c.translate(cx, cy - 200); c.rotate(sw)
    line(c, -230, 0, 230, 0, 10, (0.8, 0.84, 0.92))
    for s_ in (-1, 1):
        line(c, s_ * 230, 0, s_ * 230 - 70, 150, 3, DIM); line(c, s_ * 230, 0, s_ * 230 + 70, 150, 3, DIM)
        rgba(c, GOLD); c.move_to(s_ * 230 - 100, 150); c.curve_to(s_ * 230 - 60, 200, s_ * 230 + 60, 200, s_ * 230 + 100, 150); c.close_path(); c.fill()
    c.restore()
    stamp(c, "100% LEGAL", 1340, 400, 110, GREEN, (t - 0.5) / 0.5)
    q = ap(t, d * 0.35)
    card(c, 960, 600, 760, 220, q, border=GOLD)
    small(c, "“Buy, Borrow, Die”", 1340, 680, 44, GOLD, q, bold=True)
    small(c, "popularized by Prof. Edward McCaffery", 1340, 740, 34, WHITE, q)
    small(c, "USC Gould School of Law", 1340, 785, 30, DIM, q)
    chapter_tag(c, t, a.get("chap"))


def sc_proposals(c, t, d, T, a):
    bg(c, T)
    cx, by = 960, 880
    col = (0.80, 0.84, 0.92)
    rgba(c, col); c.arc(cx, 470, 150, math.pi, 0); c.fill()
    c.rectangle(cx - 12, 260, 24, 70); c.fill()
    c.rectangle(cx - 230, 470, 460, 30); c.fill()
    for k in range(7):
        c.rectangle(cx - 210 + k * 66, 510, 26, 220); c.fill()
    c.rectangle(cx - 280, 730, 560, 40); c.fill()
    for k, (lab, x) in enumerate((("Tax billionaires'\nunrealized gains", 380), ("End the step-up\nat death", 1540))):
        p = ap(t, 0.4 + k * d * 0.25)
        card(c, x - 250, 360, 500, 260, p, border=WHITE)
        for j, ln in enumerate(lab.split("\n")):
            small(c, ln, x, 460 + j * 56, 42, WHITE, p, bold=True)
        stamp(c, "NOT LAW", x, 690, 60, RED, (t - d * 0.6 - k * 0.3) / 0.5)


def sc_risk(c, t, d, T, a):
    bg(c, T)
    x0, x1, y0 = 200, 1100, 300
    p = ap(t, 0.3, d * 0.35)
    pts = [(x0 + (x1 - x0) * k / 40, y0 + 80 * math.sin(k * 0.9) * 0.3 + (k / 40) ** 2 * 480) for k in range(41)]
    m = max(2, int(40 * p) + 1)
    c.set_line_width(8); rgba(c, RED); c.move_to(*pts[0])
    for q in pts[1:m]:
        c.line_to(*q)
    c.stroke()
    small(c, "YOUR COLLATERAL", x0, 240, 32, DIM, ap(t, 0.2), align="left", bold=True)
    fl = ap(t, d * 0.25) * (0.75 + 0.25 * (math.sin(T * 10) > 0))
    card(c, 1180, 250, 600, 220, fl, border=RED)
    big(c, "⚠ MARGIN CALL", 1480, 350, 62, RED, fl)
    small(c, "add collateral or sell now", 1480, 420, 34, WHITE, fl)
    r = ap(t, d * 0.6, d * 0.3)
    small(c, "BORROWING RATES", 1180, 600, 32, DIM, ap(t, d * 0.6), align="left", bold=True)
    rpts = [(1180 + 600 * k / 20, 900 - (40 if k < 12 else 40 + (k - 12) * 50)) for k in range(21)]
    m2 = max(2, int(20 * r) + 1)
    c.set_line_width(7); rgba(c, GOLD); c.move_to(*rpts[0])
    for q in rpts[1:m2]:
        c.line_to(*q)
    c.stroke()
    small(c, "2010s", 1200, 950, 28, DIM, ap(t, d * 0.6), align="left")
    small(c, "2022 →", 1640, 950, 28, GOLD, ap(t, d * 0.75), align="left", bold=True)
    rich(c, 650, 950, 1.0, T=T, head_hold=1.0, a=ap(t, d * 0.25))


def sc_zero_list(c, t, d, T, a):
    bg(c, T)
    big(c, "YEARS THEY PAID $0", W / 2, 160, 64, WHITE, ap(t, 0.1))
    rows = [("ELON MUSK", "2018", 0.12), ("JEFF BEZOS", "2007 · 2011", 0.25), ("MICHAEL BLOOMBERG", "recent years", 0.62),
            ("CARL ICAHN", "2 years", 0.70), ("GEORGE SOROS", "3 years in a row", 0.78)]
    for k, (name, yrs, f0) in enumerate(rows):
        p = ap(t, d * f0, 0.45)
        y = 250 + k * 145
        c.save(); c.translate(80 * (1 - p), 0)
        card(c, 360, y, 1200, 115, p)
        stick(c, 440, y + 100, 0.62, GOLD, p)
        top_hat(c, 440, y + 100 - 132 * 0.62, 0.62, GOLD, p)
        big(c, name, 510, y + 72, 46, WHITE, p, align="left")
        small(c, yrs, 1380, y + 70, 32, DIM, p, align="right", bold=True)
        big(c, "$0", 1480, y + 78, 64, GREEN, p, align="center")
        c.restore()
    q = ap(t, d * 0.35)
    small(c, "Bezos 2011: also claimed a $4,000 child tax credit", W / 2, 1000, 32, GOLD, q * (1 - ap(t, d * 0.6)), bold=True)
    source(c, "Source: ProPublica, “The Secret IRS Files” (2021)", ap(t, 1))


def sc_scale(c, t, d, T, a):
    bg(c, T)
    big(c, "SAME TRICK. DIFFERENT SCALE.", W / 2, 160, 64, WHITE, ap(t, 0.1))
    p1 = ap(t, d * 0.35)
    card(c, 160, 240, 760, 620, p1, border=BLUE)
    joe(c, 540, 600, 1.2, T=T, a=p1)
    small(c, "PORTFOLIO $50,000", 540, 310, 36, DIM, p1, bold=True)
    small(c, "borrow 3%", 540, 705, 34, DIM, p1)
    big(c, "$1,500", 540, 790, 100, BLUE, p1)
    p2 = ap(t, d * 0.65)
    card(c, 1000, 240, 760, 620, p2, border=GOLD)
    coin_pile(c, 1380, 640, 300, 4, p2)
    rich(c, 1380, 470, 0.7, T=T, a=p2, arms=(0.5, -2.3))
    small(c, "FORTUNE $100,000,000,000", 1380, 310, 36, DIM, p2, bold=True)
    small(c, "borrow 3%", 1380, 705, 34, DIM, p2)
    big(c, f"${3 * ap(t, d * 0.68, 1.5):.1f}B".replace(".0B", "B"), 1380, 790, 100, GOLD, p2, glow_a=0.4)
    q = ap(t, 0.4)
    small(c, "SECURITIES-BASED LINE OF CREDIT", W / 2, 950, 36, GOLD, q, bold=True)


def sc_story(c, t, d, T, a):
    bg(c, T)
    x0, x1, ty = 200, 1720, 820
    line(c, x0, ty, x1, ty, 4, DIM, 0.6)
    ages = [(30, 0.03), (50, 0.18), (80, 0.62)]
    for age, f in ages:
        x = x0 + (x1 - x0) * (age - 30) / 50
        p = ap(t, d * f)
        rgba(c, GOLD, p); c.arc(x, ty, 14, 0, 2 * math.pi); c.fill()
        small(c, f"AGE {age}", x, ty + 60, 32, GOLD, p, bold=True)
    u = clamp((t / d - 0.03) / 0.62)
    age = 30 + 50 * ease(u)
    px = x0 + (x1 - x0) * (age - 30) / 50
    dead = t > d * 0.64
    if not dead:
        rich(c, px, ty - 10, 1.1, T=T, phase=T * 6 if 0.02 < u < 0.99 else None)
    else:
        gravestone(c, x1, ty - 10, 0.55, ap(t, d * 0.64))
        for k in range(3):
            stick(c, x1 - 330 + k * 90, ty - 10, 0.8, GOLD, ap(t, d * 0.66))
    worth = 0.05e9 + 4.95e9 * ap(t, d * 0.18, d * 0.12) + 15e9 * ap(t, d * 0.3, d * 0.32)
    borrowed = 1.5e9 * ap(t, d * 0.3, d * 0.32)
    p = ap(t, d * 0.1)
    card(c, 160, 150, 500, 190, p, border=GOLD)
    small(c, "ALEX'S SHARES", 410, 210, 30, DIM, p, bold=True)
    big(c, money(worth), 410, 300, 80, GOLD, p)
    p = ap(t, d * 0.18)
    card(c, 710, 150, 500, 190, p, border=BLUE)
    small(c, "SALARY", 960, 210, 30, DIM, p, bold=True)
    big(c, "$1", 960, 300, 80, BLUE, p)
    p = ap(t, d * 0.3)
    card(c, 1260, 150, 500, 190, p, border=GREEN)
    small(c, "BORROWED TO LIVE ON", 1510, 210, 30, DIM, p, bold=True)
    big(c, money(borrowed) if borrowed > 1 else "$0", 1510, 300, 80, GREEN, p)
    q = ap(t, d * 0.84)
    card(c, 560, 420, 800, 170, q, border=RED)
    small(c, "Income tax on $20B of growth", W / 2, 480, 34, DIM, q)
    big(c, "≈ $0", W / 2, 560, 80, GREEN, q, glow_a=0.3)
    chapter_tag(c, t, a.get("chap"))


LESSONS = ["Own assets, not just a salary", "Hold investments for the long term", "Use 401(k), IRA and Roth IRA",
           "The step-up works for families too", "Debt is a tool, not free money"]


def sc_lessons(c, t, d, T, a):
    bg(c, T)
    n = a.get("n", 0)
    upto = n + (1 if n == 3 else 0)
    big(c, "WHAT YOU CAN USE", W / 2, 170, 64, WHITE)
    for k, s in enumerate(LESSONS):
        if k > upto:
            break
        t0 = 0.3 if k == n else (-1 if k < n else d * 0.5)
        p = ap(t, t0) if k >= n else 1.0
        y = 300 + k * 140
        hi = k >= n
        c.save(); c.translate(-60 * (1 - p), 0)
        card(c, 360, y - 10, 1200, 110, p, border=GOLD if hi else None)
        rgba(c, GOLD if hi else DIM, p); c.arc(440, y + 45, 34, 0, 2 * math.pi); c.fill()
        big(c, str(k + 1), 440, y + 62, 44, BG1, p)
        big(c, s, 510, y + 65, 52 if hi else 46, WHITE if hi else DIM, p, align="left", family="Inter Display Black" if hi else "Inter")
        c.restore()
    joe(c, 1720, 960, 1.1, T=T, wave=T * 4 if n == 0 else None)
    chapter_tag(c, t, a.get("chap"))


def sc_accounts(c, t, d, T, a):
    bg(c, T)
    big(c, "YOUR UNTAXED GROWTH", W / 2, 170, 64, WHITE, ap(t, 0.1))
    accs = [("401(k)", "Invest before tax", "Often with an employer match", BLUE),
            ("Traditional IRA", "Invest before tax", "Pay tax when you withdraw", BLUE),
            ("Roth IRA", "Grows tax free", "Tax-free withdrawals in retirement", GREEN)]
    for k, (h, s1, s2, colr) in enumerate(accs):
        x = 400 + k * 560
        p = pop(t, d * 0.25 + k * 0.5)
        def draw(x=x, h=h, s1=s1, s2=s2, colr=colr):
            card(c, x - 250, 280, 500, 520, 1, border=colr)
            coin(c, x, 420, 60, 1, GOLD)
            big(c, h, x, 580, 60, colr)
            small(c, s1, x, 650, 36, WHITE, bold=True)
            small(c, s2, x, 705, 28, DIM)
        scaled(c, x, 540, p, draw)
    source(c, "US accounts. Rules and limits change yearly: check irs.gov", ap(t, 1))


def sc_outro(c, t, d, T, a):
    bg(c, T)
    logo(c, W / 2, 340, 150, T)
    big(c, "THE QUIET MONEY", W / 2, 600, 96, WHITE, ap(t, 0.3))
    small(c, "How money really works, from the inside", W / 2, 665, 38, DIM, ap(t, 0.6))
    p = pop(t, d * 0.35)
    def btn():
        rgba(c, (0.85, 0.15, 0.18)); rrect(c, W / 2 - 230, 730, 460, 110, 55); c.fill()
        big(c, "SUBSCRIBE", W / 2, 805, 56, WHITE)
    scaled(c, W / 2, 785, p, btn)
    cx = W / 2 + 260 - 120 * ap(t, d * 0.35, 0.8)
    cy = 900 - 60 * ap(t, d * 0.35, 0.8)
    if p > 0:
        rgba(c, WHITE); c.move_to(cx, cy); c.line_to(cx + 22, cy + 70); c.line_to(cx + 36, cy + 44); c.line_to(cx + 64, cy + 56); c.close_path(); c.fill()
    small(c, "Education only. Not financial advice.", W / 2, 1010, 28, DIM, ap(t, d * 0.75))


def logo(c, x, y, r, T=0.0, a=1.0, halo=0.45):
    """Channel mark: a gold coin with a keyhole ('money, from the inside')."""
    glow(c, x, y, r * 2.2, GOLD, halo * a)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 0.90, 0.55, a); g.add_color_stop_rgba(1, 0.85, 0.58, 0.12, a)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_line_width(r * 0.07); rgba(c, (0.65, 0.42, 0.08), a); c.arc(x, y, r * 0.84, 0, 2 * math.pi); c.stroke()
    rgba(c, BG1, a)
    c.arc(x, y - r * 0.18, r * 0.24, 0, 2 * math.pi); c.fill()
    c.move_to(x - r * 0.11, y - r * 0.08); c.line_to(x - r * 0.2, y + r * 0.45); c.line_to(x + r * 0.2, y + r * 0.45); c.line_to(x + r * 0.11, y - r * 0.08); c.close_path(); c.fill()


# ---------------- thumbnail ----------------

def thumbnail(c):
    bg(c, 3.0)
    glow(c, 1450, 600, 700, GOLD, 0.35)
    coin_pile(c, 1450, 1000, 640, 7)
    rich(c, 1450, 600, 2.0, T=0, arms=(0.7, -2.5))
    joe(c, 1000, 1040, 1.5, head_hold=1.0)
    vignette(c)
    big(c, "$0", 120, 520, 440, GOLD, align="left", outline=0.06, glow_a=0.5)
    big(c, "TAX.", 140, 720, 170, WHITE, align="left", outline=0.08)
    rgba(c, RED); rrect(c, 130, 790, 640, 130, 20); c.fill()
    big(c, "LEGALLY", 450, 890, 110, WHITE)


# ---------------- Shorts scenes (central 9:16 column) ----------------

def colbox(c):
    """Enter column coordinates (0..CW wide, content y 200..800), fitted between the hook and the captions."""
    c.translate(X0, 0)
    c.translate(CW / 2, 230)
    c.scale(0.8, 0.8)
    c.translate(-CW / 2, -200)


def v_bg(c, T):
    bg(c, T)


def sc_v_zero(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, a.get("label", "FEDERAL INCOME TAX"), CW / 2, 215, 30, DIM, ap(t, 0.1), bold=True)
    v = 48_000_000 * (1 - ease((t - 0.2) / 1.2))
    big(c, money(v) if v > 1 else "$0", CW / 2, 360, 150 if v <= 1 else 92, GREEN if v <= 1 else WHITE, glow_a=0.5 if v <= 1 else 0)
    coin_pile(c, CW / 2, 800, 360, 5)
    rich(c, CW / 2, 570, 0.9, T=T, arms=(0.6, -2.4))
    c.restore()


def sc_v_rates(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, "TRUE TAX RATE", CW / 2, 240, 34, WHITE, 1, bold=True)
    base = 700
    for lab, val, colr, x, t0 in (("You", 14.0, BLUE, 170, 0.2), ("Top 25 richest", 3.4, GOLD, 440, 0.6)):
        p = ap(t, t0, 1.0)
        h = 360 * val / 14 * p
        rgba(c, colr); rrect(c, x - 90, base - h, 180, max(1, h), 12); c.fill()
        big(c, f"{val * p:.1f}%", x, base - h - 20, 64, colr, p)
        small(c, lab, x, base + 40, 26, WHITE, ap(t, t0), bold=True)
    c.restore()


def sc_v_buy(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, "STEP 1", CW / 2, 250, 30, GOLD, 1, bold=True)
    scaled(c, CW / 2, 340, pop(t, 0.1), lambda: big(c, "BUY", CW / 2, 370, 130, WHITE, glow_a=0.3))
    for k, fn in enumerate((chart_icon, factory_icon, house_icon)):
        x = 110 + k * 194
        scaled(c, x, 560, pop(t, 0.6 + k * 0.3), lambda fn=fn, x=x: (card(c, x - 85, 470, 170, 180, 1, border=GOLD), fn(c, x, 560, 0.9)))
    big(c, "NEVER SELL", CW / 2, 750, 64, GOLD, ap(t, d * 0.55))
    c.restore()


def sc_v_borrow(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, "STEP 2", CW / 2, 250, 30, GOLD, 1, bold=True)
    scaled(c, CW / 2, 340, pop(t, 0.1), lambda: big(c, "BORROW", CW / 2, 370, 110, GOLD, glow_a=0.3))
    bank(c, 440, 720, 0.6)
    rich(c, 120, 720, 0.9, T=T, arms=(1.2, -0.3))
    u = ap(t, 0.5, 1.2)
    share_cert(c, 170 + 230 * u, 590 - 50 * math.sin(u * math.pi), 120, 1 - 0.6 * ap(t, 1.7, 0.3))
    v = ap(t, d * 0.45, 1.2)
    if v > 0:
        cash_stack(c, 420 - 260 * v, 620, 5, 110)
    big(c, "LOAN ≠ INCOME", CW / 2, 790, 52, GREEN, ap(t, d * 0.6))
    c.restore()


def sc_v_die(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, "STEP 3", CW / 2, 250, 30, GOLD, 1, bold=True)
    scaled(c, CW / 2, 340, pop(t, 0.1), lambda: big(c, "DIE", CW / 2, 370, 130, RED, glow_a=0.3))
    gravestone(c, CW / 2, 720, 0.8, ap(t, 0.4))
    c.restore()


def sc_v_stepup(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    small(c, "HEIRS' TAX COST", CW / 2, 215, 30, DIM, 1, bold=True)
    base = 700
    rgba(c, BLUE); rrect(c, 90, base - 30, 160, 30, 6); c.fill()
    big(c, "$1M", 170, base - 50, 48, BLUE, 1 - ap(t, d * 0.4, 0.3))
    small(c, "cost basis", 170, base + 40, 26, DIM)
    p = ap(t, 0.4, 1.0)
    rgba(c, GOLD); rrect(c, 360, base - 380 * p, 160, 380 * p + 1, 6); c.fill()
    big(c, "$1B", 440, base - 380 * p - 20, 56, GOLD, p)
    small(c, "at death", 440, base + 40, 26, DIM, p)
    s = ap(t, d * 0.4, 1.0)
    if s > 0:
        rgba(c, BLUE, 0.6 + 0.4 * s); rrect(c, 90, base - 30 - 350 * s, 160, 30 + 350 * s, 6); c.fill()
        small(c, "STEP-UP ↑", 170, base - 30 - 350 * s - 60, 32, GOLD, s, bold=True)
    big(c, "TAX: $0", CW / 2, 800, 64, GREEN, ap(t, d * 0.7), glow_a=0.3)
    c.restore()


def sc_v_salary(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    coin_stack(c, 150, 720, 2, 34)
    small(c, "SALARY", 150, 560, 28, BLUE, 1, bold=True)
    big(c, "$81,840", 150, 620, 44, WHITE)
    p = ap(t, d * 0.35, 1.5)
    for k in range(2):
        coin_stack(c, 380 + k * 120, 760, int(24 * p), 55)
    small(c, "STOCK", 440, 260, 28, GOLD, ap(t, d * 0.35), bold=True)
    big(c, "$100B+", 440, 340, 72, GOLD, ap(t, d * 0.4), glow_a=0.4)
    c.restore()


def sc_v_cycle(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    for k, (lab, colr) in enumerate((("BUY", WHITE), ("BORROW", GOLD), ("DIE", RED))):
        y = 300 + k * 160
        scaled(c, CW / 2, y, pop(t, 0.1 + k * 0.35), lambda y=y, lab=lab, colr=colr: (card(c, 104, y - 60, 400, 110, 1, border=colr), big(c, lab, CW / 2, y + 18, 60, colr)))
        if k < 2:
            arrow(c, CW / 2, y + 55, CW / 2, y + 95, ap(t, 0.4 + k * 0.35), DIM, 5)
    big(c, "TAX ≈ 0", CW / 2, 800, 70, GREEN, ap(t, d * 0.5), glow_a=0.3)
    c.restore()


def sc_v_logo(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    logo(c, CW / 2, 420, 110, T)
    big(c, "THE QUIET MONEY", CW / 2, 640, 50, WHITE, ap(t, 0.2))
    small(c, "Follow for part 2", CW / 2, 700, 28, GOLD, ap(t, 0.5), bold=True)
    c.restore()


def sc_v_margin(c, t, d, T, a):
    v_bg(c, T); c.save(); colbox(c)
    p = ap(t, 0.2, d * 0.5)
    pts = [(60 + 490 * k / 30, 300 + (k / 30) ** 2 * 360 + 20 * math.sin(k)) for k in range(31)]
    m = max(2, int(30 * p) + 1)
    c.set_line_width(7); rgba(c, RED); c.move_to(*pts[0])
    for q in pts[1:m]:
        c.line_to(*q)
    c.stroke()
    fl = ap(t, d * 0.4) * (0.75 + 0.25 * (math.sin(T * 10) > 0))
    big(c, "MARGIN CALL", CW / 2, 790, 64, RED, fl, glow_a=0.3)
    c.restore()


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}
