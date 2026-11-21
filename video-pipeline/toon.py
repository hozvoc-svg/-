"""Wordless stickman cartoon engine ("Stix & Bolt"): characters, props, camera, renderer and a tiny synth
for a score and sound effects that are timed to the same cue sheet as the animation.

An episode module defines:
    BPM, BEATS (length in beats), HOOK (top text), draw(c, t) and score(mix) / sfx(mix)
and is rendered with:  python3 toon.py <episode_module>   ->  out/<episode>.mp4 (1080x1920, 30 fps)
"""
import importlib, math, os, subprocess, sys, wave
from multiprocessing import Pool
import cairo
import numpy as np

W, H, FPS, SR = 1080, 1920, 30, 44100
INK = (0.08, 0.08, 0.10)
SKIN = (1.0, 0.98, 0.94)
RED = (0.93, 0.22, 0.24)
TAN = (0.94, 0.64, 0.32)
BROWN = (0.50, 0.30, 0.16)
LW = 9  # body line width (pixels at scale 1 of the canvas)


# ---------------------------------------------------------------- timing helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def back(x, k=1.70158):
    """Ease-out with a small overshoot (cartoon 'pop')."""
    x = clamp(x) - 1
    return 1 + x * x * ((k + 1) * x + k)


def lerp(a, b, u):
    if isinstance(a, tuple):
        return tuple(lerp(x, y, u) for x, y in zip(a, b))
    return a + (b - a) * u


def keys(ks, t, fn=ease):
    """Interpolate keyframes [(time, value), ...] (values: numbers or tuples)."""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t < t1:
            return lerp(v0, v1, fn((t - t0) / (t1 - t0)) if t1 > t0 else 1)
    return ks[-1][1]


def step(ks, t):
    """Discrete keyframes: the value of the last key at or before t."""
    v = ks[0][1]
    for tk, vk in ks:
        if t >= tk:
            v = vk
    return v


def rgba(c, col, a=1.0):
    c.set_source_rgba(col[0], col[1], col[2], a)


def fill_stroke(c, col, lw=6, a=1.0, ink=INK):
    rgba(c, col, a)
    c.fill_preserve()
    c.set_line_width(lw)
    rgba(c, ink, a)
    c.stroke()


def seg(c, p, q, w=LW, col=INK, a=1.0):
    c.set_line_width(w)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(c, col, a)
    c.move_to(*p)
    c.line_to(*q)
    c.stroke()


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def ellipse(c, x, y, rx, ry):
    c.save()
    c.translate(x, y)
    c.scale(max(rx, 0.01), max(ry, 0.01))
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()


def heavy_text(c, s, x, y, size, col=(1, 1, 1), a=1.0, outline=0.16):
    c.select_font_face("Inter Display Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.new_path()
    c.move_to(x - e.x_advance / 2, y)
    c.text_path(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_line_width(size * outline)
    rgba(c, INK, a)
    c.stroke_preserve()
    rgba(c, col, a)
    c.fill()


# ---------------------------------------------------------------- Stix (the stickman)
STIX = dict(x=540, y=1500, s=3.0, facing=1, lean=0.0, tilt=0.0, dy=0.0, hip=-66,
            aF=(0.25, 0.0), aB=(-0.25, 0.0), lF=(0.16, 0.0), lB=(-0.16, 0.0),
            eyes="open", look=(0.0, 0.0), mouth="smile", mo=0.0, brows=0.0, red=0.0, squash=0.0,
            steam=0.0, shake=0.0, T=0.0)


def walk(phase, amp=1.0):
    """Leg/arm angles for a walk cycle (phase in radians)."""
    sw = math.sin(phase) * amp
    return dict(lF=(0.42 * sw, -0.35 * max(0, -sw)), lB=(-0.42 * sw, -0.35 * max(0, sw)),
                aF=(-0.45 * sw, 0.25), aB=(0.45 * sw, 0.25), dy=-abs(math.cos(phase)) * 4 * amp)


def stix(c, **kw):
    """Draw Stix; returns world positions of the hands and head (for props)."""
    P = dict(STIX, **kw)
    s, f = P["s"], P["facing"]
    x0 = P["x"] + (math.sin(P["T"] * 55) * 4 * P["shake"])
    y0 = P["y"]

    def Wp(lx, ly):
        return (x0 + f * lx * s, y0 + (ly + P["dy"]) * s)

    c.save()
    sq = P["squash"]
    c.translate(x0, y0)
    c.scale(1 + sq * 0.6, 1 - sq)
    c.translate(-x0, -y0)
    hip = (0.0, P["hip"])
    ln = P["lean"]
    neck = (hip[0] + 64 * math.sin(ln), hip[1] - 64 * math.cos(ln))
    sh = (neck[0] - 6 * math.sin(ln), neck[1] + 6 * math.cos(ln))
    hd_ang = ln + P["tilt"]
    head = (neck[0] + 40 * math.sin(hd_ang), neck[1] - 40 * math.cos(hd_ang))
    lw = LW * s / 3.0

    def limb(root, ang, l1, l2):
        a1, bend = ang
        k = (root[0] + l1 * math.sin(a1), root[1] + l1 * math.cos(a1))
        e = (k[0] + l2 * math.sin(a1 + bend), k[1] + l2 * math.cos(a1 + bend))
        return k, e

    hands = {}
    for name, ang in (("B", P["aB"]),):  # back arm behind the body
        k, e = limb(sh, ang, 30, 30)
        seg(c, Wp(*sh), Wp(*k), lw); seg(c, Wp(*k), Wp(*e), lw)
        hands[name] = Wp(*e)
    for ang in (P["lB"], P["lF"]):
        k, e = limb(hip, ang, 34, 34)
        seg(c, Wp(*hip), Wp(*k), lw); seg(c, Wp(*k), Wp(*e), lw)
    seg(c, Wp(*hip), Wp(*neck), lw)
    k, e = limb(sh, P["aF"], 30, 30)
    seg(c, Wp(*sh), Wp(*k), lw); seg(c, Wp(*k), Wp(*e), lw)
    hands["F"] = Wp(*e)
    # head
    hx, hy = Wp(*head)
    c.save()
    c.translate(hx, hy)
    c.scale(f * s, s)
    c.rotate(P["tilt"] + ln)
    face(c, P)
    c.restore()
    c.restore()
    if P["steam"] > 0:
        steam(c, hx, hy - 50 * s, s, P["steam"], P["T"])
    hands["head"] = (hx, hy)
    return hands


def face(c, P):
    r = 36
    skin = lerp(SKIN, (1.0, 0.45, 0.40), clamp(P["red"]))
    c.arc(0, 0, r, 0, 2 * math.pi)
    fill_stroke(c, skin, 5.5)
    lx, ly = P["look"]
    eyes, mo = P["eyes"], P["mo"]
    for ex in (-9, 15):
        ey = -4
        if eyes in ("open", "wide", "angry", "sad"):
            rx, ry, pr = (8, 10, 4.6) if eyes != "wide" else (11, 13.5, 3.4)
            ellipse(c, ex, ey, rx, ry)
            fill_stroke(c, (1, 1, 1), 2.6)
            c.arc(ex + lx * (rx - pr - 1), ey + ly * (ry - pr - 1), pr, 0, 2 * math.pi)
            rgba(c, INK); c.fill()
        elif eyes == "happy":
            c.arc(ex, ey + 4, 7, math.pi * 1.15, math.pi * 1.85)
            c.set_line_width(4); rgba(c, INK); c.stroke()
        elif eyes == "closed":
            seg(c, (ex - 7, ey + 1), (ex + 7, ey + 1), 4)
    b = P["brows"] + (0.5 if eyes == "angry" else 0) - (0.45 if eyes == "sad" else 0)
    if abs(b) > 0.05 or eyes in ("angry", "sad", "wide"):
        for ex, sg in ((-9, 1), (15, -1)):
            lift = -17 if eyes != "wide" else -22
            seg(c, (ex - 8, lift - 4 * b * sg), (ex + 8, lift + 4 * b * sg), 4.2)
    mx, my = 3, 15
    m = P["mouth"]
    if m == "smile":
        c.arc(mx, my - 6, 11, 0.2 * math.pi, 0.8 * math.pi)
        c.set_line_width(4); rgba(c, INK); c.stroke()
    elif m == "grin":
        c.move_to(mx - 14, my - 2)
        c.curve_to(mx - 10, my + 14, mx + 10, my + 14, mx + 14, my - 2)
        c.close_path()
        fill_stroke(c, (0.55, 0.10, 0.12), 3.5)
        seg(c, (mx - 11, my), (mx + 11, my), 3, (1, 1, 1))
    elif m == "open":
        ellipse(c, mx, my, 7 + 6 * mo, 3 + 13 * mo)
        fill_stroke(c, (0.45, 0.08, 0.10), 3.5)
    elif m == "o":
        ellipse(c, mx, my + 1, 4.5, 5.5)
        fill_stroke(c, (0.45, 0.08, 0.10), 3)
    elif m == "frown":
        c.arc(mx, my + 12, 10, 1.2 * math.pi, 1.8 * math.pi)
        c.set_line_width(4); rgba(c, INK); c.stroke()
    elif m == "flat":
        seg(c, (mx - 8, my), (mx + 8, my), 4)
    elif m == "wavy":
        c.move_to(mx - 12, my)
        for i in range(1, 7):
            c.line_to(mx - 12 + i * 4, my + (3 if i % 2 else -3))
        c.set_line_width(3.5); rgba(c, INK); c.stroke()
    elif m == "chew":
        k = abs(math.sin(P["T"] * 18))
        ellipse(c, mx, my, 8, 2 + 5 * k)
        fill_stroke(c, (0.45, 0.08, 0.10), 3)
    # signature red cap
    c.move_to(-r - 1, -8)
    c.arc(0, -8, r + 1, math.pi, 2 * math.pi)
    c.close_path()
    fill_stroke(c, RED, 5)
    rrect(c, 8, -14, 42, 11, 5)
    fill_stroke(c, RED, 4.5)
    c.arc(0, -8 - r, 6, 0, 2 * math.pi)
    fill_stroke(c, (1, 1, 1), 3.5)


def steam(c, x, y, s, amt, T):
    for i in range(5):
        u = (T * 1.6 + i / 5) % 1
        px = x + math.sin(i * 2.1 + T * 3) * 30 * s / 3 + (i - 2) * 22
        py = y - u * 160
        rr = (14 + 26 * u) * s / 3
        c.arc(px, py, rr, 0, 2 * math.pi)
        rgba(c, (1, 1, 1), amt * (1 - u) * 0.9)
        c.fill()


# ---------------------------------------------------------------- Bolt (the dog)
BOLT = dict(x=500, y=1500, s=2.4, facing=1, gait=None, sit=0.0, head=0.0, eye="open", look=(0.3, 0.0),
            jaw=0.0, tail=0.0, belly=0.0, ears=0.0, whistle=0.0, T=0.0, squash=0.0, dy=0.0, tongue=0.0)


def bolt(c, **kw):
    P = dict(BOLT, **kw)
    s, f = P["s"], P["facing"]
    c.save()
    c.translate(P["x"], P["y"] + P["dy"])
    sq = P["squash"]
    c.scale(f * s * (1 + sq * 0.5), s * (1 - sq))
    T = P["T"]
    g = P["gait"]
    sw = math.sin(g) if g is not None else 0.0
    sit = P["sit"]
    lw = 3.6
    # hind legs
    if sit < 0.5:
        for hx, ph in ((-30, 0), (-14, math.pi)):
            a = 0.35 * math.sin((g or 0) + ph) if g is not None else 0
            seg(c, (hx, -22), (hx + 22 * math.sin(a), -22 + 22 * math.cos(a)), lw)
    else:
        ellipse(c, -26, -14, 22, 14)
        fill_stroke(c, TAN, 3)
        seg(c, (-16, -2), (2, -2), lw)
    # tail
    ta = 0.9 + 0.5 * math.sin(T * (10 + 14 * P["tail"])) * (0.3 + P["tail"])
    c.move_to(-44, -44 + sit * 20)
    c.curve_to(-60, -56 + sit * 20, -62 - 10 * math.cos(ta), -70 + sit * 18, -58 - 22 * math.cos(ta), -88 + sit * 16)
    c.set_line_width(lw * 1.4); rgba(c, INK); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    # body (rotates upright when sitting)
    c.save()
    c.translate(-40, -18)
    c.rotate(-0.55 * sit)
    c.translate(40, 18)
    rb = 48 + 22 * P["belly"]
    ellipse(c, 0, -40 - 8 * P["belly"], rb, 26 + 14 * P["belly"])
    fill_stroke(c, TAN, 3.4)
    ellipse(c, -14, -50, 14, 9)
    rgba(c, BROWN, 0.55); c.fill()
    chest = (34, -30)
    neck = (44, -58)
    c.restore()
    # front legs (always vertical to the floor)
    cx = 30 if sit < 0.5 else 20
    for fx, ph in ((cx, math.pi), (cx + 16, 0)):
        a = 0.35 * math.sin((g or 0) + ph) if g is not None else 0
        top = -24 - 30 * sit
        seg(c, (fx, top), (fx + 22 * math.sin(a), 0), lw)
    # head
    hb = -72 - 36 * sit - 8 * P["belly"]
    c.save()
    c.translate(54 - 8 * sit, hb)
    c.rotate(-P["head"])
    ear_lift = P["ears"]
    c.move_to(-16, -24)
    c.curve_to(-34, -24 - 16 * ear_lift, -40, 6 - 30 * ear_lift, -26, 18 - 34 * ear_lift)
    c.curve_to(-18, 10, -12, -8, -16, -24)
    fill_stroke(c, BROWN, 3)
    c.arc(0, 0, 28, 0, 2 * math.pi)
    fill_stroke(c, TAN, 3.4)
    # snout + jaw
    jaw = P["jaw"]
    if jaw > 0.02:
        c.save()
        c.translate(14, 12)
        c.rotate(0.6 * jaw)
        ellipse(c, 16, 4, 18, 8)
        fill_stroke(c, TAN, 3)
        c.restore()
        ellipse(c, 26, 8, 16, 7 * jaw + 2)
        rgba(c, (0.45, 0.08, 0.10)); c.fill()
    ellipse(c, 24, 4 - 4 * jaw, 20, 13)
    fill_stroke(c, (0.98, 0.80, 0.55), 3)
    ellipse(c, 42, -2 - 4 * jaw, 7, 5.5)
    rgba(c, INK); c.fill()
    if P["tongue"] > 0.05:
        c.save(); c.translate(40, 10); c.rotate(0.5)
        ellipse(c, 0, 10 * P["tongue"], 8, 6 + 14 * P["tongue"])
        fill_stroke(c, (1.0, 0.45, 0.55), 2.5)
        c.restore()
    if P["whistle"] > 0:
        ellipse(c, 34, 14, 3.5, 4)
        fill_stroke(c, (0.45, 0.08, 0.10), 2)
    # eye
    e = P["eye"]
    lx, ly = P["look"]
    if e in ("open", "half"):
        ellipse(c, 6, -8, 8, 9)
        fill_stroke(c, (1, 1, 1), 2.4)
        c.arc(6 + lx * 3.5, -8 + ly * 4, 4.2, 0, 2 * math.pi)
        rgba(c, INK); c.fill()
        if e == "half":
            c.save()
            ellipse(c, 6, -8, 9.5, 10.5)
            c.clip()
            c.rectangle(-6, -22, 24, 13)
            rgba(c, TAN); c.fill()
            c.restore()
            seg(c, (-2, -9), (14, -9), 2.6)
    elif e == "puppy":
        ellipse(c, 6, -6, 15, 16)
        fill_stroke(c, (1, 1, 1), 2.4)
        c.arc(6, -4, 11.5, 0, 2 * math.pi)
        rgba(c, INK); c.fill()
        for px, py, pr in ((2, -9, 4.2), (10, 1, 2.2)):
            c.arc(px, py, pr, 0, 2 * math.pi)
            rgba(c, (1, 1, 1)); c.fill()
        seg(c, (-6, -28), (14, -24), 2.6)
    elif e == "happy":
        c.arc(6, -4, 7, math.pi * 1.15, math.pi * 1.85)
        c.set_line_width(3); rgba(c, INK); c.stroke()
    c.restore()
    c.restore()


# ---------------------------------------------------------------- props & set
def kitchen(c, T):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 1.0, 0.93, 0.78)
    g.add_color_stop_rgb(1, 0.99, 0.84, 0.66)
    c.set_source(g)
    c.paint()
    # wallpaper dots
    for j in range(16):
        for i in range(9):
            x = i * 130 + (65 if j % 2 else 0)
            y = 80 + j * 105
            c.arc(x, y, 7, 0, 2 * math.pi)
            rgba(c, (1, 1, 1), 0.45); c.fill()
    # window
    rrect(c, 90, 540, 330, 380, 24)
    fill_stroke(c, (0.62, 0.85, 1.0), 9)
    c.arc(330, 640, 40, 0, 2 * math.pi); rgba(c, (1.0, 0.92, 0.45)); c.fill()
    for k in range(2):
        cx = (130 + 60 * k + T * 12) % 420 + 60
        if 120 < cx < 400:
            for dx, rr in ((-22, 20), (0, 28), (24, 20)):
                c.arc(cx + dx, 760 + 70 * k, rr, 0, 2 * math.pi)
                rgba(c, (1, 1, 1)); c.fill()
    seg(c, (255, 540), (255, 920), 9); seg(c, (90, 730), (420, 730), 9)
    # clock
    c.arc(820, 700, 78, 0, 2 * math.pi)
    fill_stroke(c, (1, 1, 1), 9)
    a = (int(T) % 60) / 60 * 2 * math.pi
    seg(c, (820, 700), (820 + 52 * math.sin(a), 700 - 52 * math.cos(a)), 6, RED)
    seg(c, (820, 700), (820 + 34 * math.sin(T * 0.05), 700 - 34 * math.cos(T * 0.05)), 8)
    # floor
    c.rectangle(0, 1500, W, H - 1500)
    rgba(c, (0.82, 0.92, 0.98)); c.fill()
    for i in range(-2, 12):
        for j in range(5):
            if (i + j) % 2 == 0:
                x0 = i * 120 + (j * 30)
                c.move_to(x0, 1500 + j * 84)
                c.line_to(x0 + 120, 1500 + j * 84)
                c.line_to(x0 + 150, 1500 + (j + 1) * 84)
                c.line_to(x0 + 30, 1500 + (j + 1) * 84)
                c.close_path()
                rgba(c, (0.64, 0.82, 0.94)); c.fill()
    seg(c, (0, 1500), (W, 1500), 9)


TABLE = dict(x0=70, x1=600, top=1130)


def table(c):
    x0, x1, top = TABLE["x0"], TABLE["x1"], TABLE["top"]
    for lx in (x0 + 40, x1 - 60):
        rrect(c, lx, top + 20, 26, 1530 - top - 20, 8)
        fill_stroke(c, (0.62, 0.38, 0.20), 7)
    rrect(c, x0, top, x1 - x0, 36, 12)
    fill_stroke(c, (0.75, 0.47, 0.25), 8)


LAYERS = [  # (kind, height) bottom -> top
    ("bread", 34), ("lettuce", 22), ("tomato", 20), ("cheese", 18), ("ham", 20), ("lettuce", 22),
    ("cheese", 18), ("tomato", 20), ("ham", 20), ("lettuce", 22), ("cheese", 18), ("tomato", 20),
    ("ham", 20), ("top", 46)]
LCOL = dict(bread=(0.96, 0.78, 0.45), top=(0.96, 0.72, 0.38), lettuce=(0.45, 0.80, 0.30),
            tomato=(0.93, 0.27, 0.22), cheese=(1.0, 0.82, 0.22), ham=(0.98, 0.62, 0.66))


def layer(c, kind, cx, y, w, h):
    """Draw one sandwich layer with its bottom edge at y."""
    col = LCOL[kind]
    if kind == "top":
        c.move_to(cx - w / 2, y)
        c.curve_to(cx - w / 2, y - h * 1.2, cx + w / 2, y - h * 1.2, cx + w / 2, y)
        c.close_path()
        fill_stroke(c, col, 6)
        for sx in (-50, -10, 34, 70):
            ellipse(c, cx + sx, y - h * 0.55 - abs(sx) * 0.08, 6, 3.5)
            rgba(c, (1, 0.96, 0.85)); c.fill()
    elif kind == "lettuce":
        c.move_to(cx - w / 2 - 14, y)
        n = 9
        for i in range(n + 1):
            xx = cx - w / 2 - 14 + i * (w + 28) / n
            c.line_to(xx, y - h + (8 if i % 2 else 0))
        c.line_to(cx + w / 2 + 14, y)
        c.close_path()
        fill_stroke(c, col, 5)
    elif kind == "cheese":
        c.rectangle(cx - w / 2 - 6, y - h, w + 12, h)
        fill_stroke(c, col, 5)
        for dx in (-w / 2 + 10, w / 2 - 30):
            c.move_to(cx + dx, y); c.line_to(cx + dx + 20, y); c.line_to(cx + dx + 10, y + 16); c.close_path()
            fill_stroke(c, col, 4)
    else:
        rrect(c, cx - w / 2 + (4 if kind == "tomato" else 0), y - h, w - (8 if kind == "tomato" else 0), h, h / 2.2)
        fill_stroke(c, col, 5)


def sandwich(c, cx, base, n, wobble=0.0, drop=None, w=210):
    """Stack of the first n layers on a base line; drop=(index, u) animates layer `index` falling in."""
    y = base
    for i, (kind, h) in enumerate(LAYERS[:n]):
        off = wobble * (i / max(1, n)) ** 1.4 * 40
        yy = y
        if drop and drop[0] == i:
            u = drop[1]
            yy = y - (1 - min(1, u / 0.6)) ** 2 * 900 if u < 0.6 else y
        layer(c, kind, cx + off, yy, w, h)
        y -= h
    return y


def knife(c, x, y, ang, s=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    rrect(c, -14, -12, 70, 24, 10)
    fill_stroke(c, (0.40, 0.25, 0.15), 5)
    c.move_to(56, -18); c.line_to(270, -18); c.curve_to(300, -18, 300, 10, 270, 22); c.line_to(56, 22); c.close_path()
    fill_stroke(c, (0.86, 0.90, 0.95), 5)
    seg(c, (80, -6), (240, -6), 4, (1, 1, 1), 0.8)
    c.restore()


def bulb(c, x, y, a, s=1.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * a, s * a)
    for i in range(8):
        an = i * math.pi / 4
        seg(c, (math.cos(an) * 62, math.sin(an) * 62), (math.cos(an) * 84, math.sin(an) * 84), 6, (1.0, 0.85, 0.2))
    c.arc(0, -6, 42, 0, 2 * math.pi)
    fill_stroke(c, (1.0, 0.92, 0.35), 6)
    rrect(c, -18, 34, 36, 26, 6)
    fill_stroke(c, (0.7, 0.72, 0.76), 5)
    c.restore()


def heart(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.move_to(0, 12)
    c.curve_to(-26, -6, -14, -30, 0, -14)
    c.curve_to(14, -30, 26, -6, 0, 12)
    c.close_path()
    rgba(c, RED, a); c.fill_preserve()
    c.set_line_width(4); rgba(c, INK, a); c.stroke()
    c.restore()


def sparkle(c, x, y, r, a=1.0, col=(1, 1, 1)):
    if a <= 0:
        return
    c.move_to(x, y - r)
    for k in range(4):
        an = k * math.pi / 2
        c.curve_to(x, y, x, y, x + r * math.cos(an + math.pi / 2) * (1 if k % 2 == 0 else 1),
                   y + r * math.sin(an + math.pi / 2))
    c.close_path()
    rgba(c, col, a); c.fill()


def dust_cloud(c, x, y, T, a=1.0, r=170):
    """Classic cartoon fight cloud with things flying out."""
    rng = np.random.default_rng(int(T * 12))
    for i in range(14):
        an = i / 14 * 2 * math.pi + T * 2
        rr = r * (0.55 + 0.2 * math.sin(T * 9 + i))
        c.arc(x + math.cos(an) * rr * 0.9, y + math.sin(an) * rr * 0.6, r * 0.42, 0, 2 * math.pi)
        rgba(c, (1, 1, 1), a); c.fill()
    for i in range(6):
        an = rng.random() * 2 * math.pi
        px, py = x + math.cos(an) * r * 1.05, y + math.sin(an) * r * 0.7
        kind = ["lettuce", "tomato", "cheese", "ham"][int(rng.integers(4))]
        c.save(); c.translate(px, py); c.rotate(an); c.scale(0.35, 0.35)
        layer(c, kind, 0, 0, 120, 26)
        c.restore()
    for i in range(3):
        an = rng.random() * 6.28
        sparkle(c, x + math.cos(an) * r * 0.5, y + math.sin(an) * r * 0.4, 26, a, (1, 0.85, 0.2))


def camera(c, cx, cy, z):
    c.translate(W / 2, H / 2)
    c.scale(z, z)
    c.translate(-cx, -cy)


# ---------------------------------------------------------------- renderer
def _render_chunk(args):
    mod, f0, f1, path = args
    ep = importlib.import_module(mod)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                           "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for fr in range(f0, f1):
        c = cairo.Context(surf)
        c.set_antialias(cairo.ANTIALIAS_BEST)
        ep.draw(c, fr / FPS)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


def render(mod, out_dir="out", tmp="tmp"):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    ep = importlib.import_module(mod)
    dur = ep.BEATS * 60.0 / ep.BPM
    n = int(round(dur * FPS))
    name = mod.split(".")[-1]
    os.makedirs(out_dir, exist_ok=True); os.makedirs(tmp, exist_ok=True)
    k = os.cpu_count() * 2
    bounds = [n * i // k for i in range(k + 1)]
    jobs = [(mod, bounds[i], bounds[i + 1], os.path.join(tmp, f"{name}_part{i:02d}.mp4")) for i in range(k)]
    with Pool(os.cpu_count()) as pool:
        parts = pool.map(_render_chunk, jobs)
    lst = os.path.join(tmp, f"{name}_parts.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{os.path.abspath(p)}'\n" for p in parts)
    audio = os.path.join(tmp, f"{name}_audio.wav")
    m = Mix(dur + 1.5)
    ep.score(m)
    ep.sfx(m)
    m.save(audio)
    out = os.path.join(out_dir, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", audio,
                    "-filter_complex", "[1:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]", "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out, round(dur, 2), "s")
    return out


# ---------------------------------------------------------------- synth
def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def midi(name):
    """'C5' -> 72, 'F#3' -> 54."""
    return NOTE[name[:-1]] + 12 * (int(name[-1]) + 1)


def _t(sec):
    return np.arange(int(sec * SR)) / SR


def _rng(seed=[0]):
    seed[0] += 1
    return np.random.default_rng(seed[0])


def band(sig, lo=None, hi=None):
    """Brick-wall-ish FFT band filter (fine for short one-shots)."""
    F = np.fft.rfft(sig)
    fr = np.fft.rfftfreq(len(sig), 1 / SR)
    mask = np.ones_like(fr)
    if lo:
        mask *= 1 / (1 + (lo / np.maximum(fr, 1)) ** 4)
    if hi:
        mask *= 1 / (1 + (fr / hi) ** 4)
    return np.fft.irfft(F * mask, len(sig)).astype(np.float32)


def noise(sec):
    return _rng().standard_normal(int(sec * SR)).astype(np.float32)


def env_ad(n, a=0.004, d=6.0):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t * d)


# --- instruments
def pluck(f, dur=0.6, bright=1.0):
    t = _t(dur)
    s = sum((1 / k ** 1.3) * np.exp(-t * (6 + 5 * k / bright)) * np.sin(2 * np.pi * f * k * t) for k in range(1, 7))
    return (s * np.minimum(1, t / 0.003)).astype(np.float32)


def glock(f, dur=1.2):
    t = _t(dur)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 9) \
        + 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 16)
    return (s * np.minimum(1, t / 0.001)).astype(np.float32)


def brass(f, dur=0.5, rel=0.15):
    t = _t(dur + rel)
    envl = np.minimum(1, t / 0.035) * np.where(t > dur, np.exp(-(t - dur) * 20), 1)
    br = 4 + 6 * np.minimum(1, t / 0.08)
    s = sum(np.exp(-k / br) / k * np.sin(2 * np.pi * f * k * t * (1 + 0.002 * np.sin(2 * np.pi * 5 * t))) for k in range(1, 12))
    return (s * envl).astype(np.float32)


def reed(f, dur=0.18):
    """Bassoon-ish staccato for the sneaky theme."""
    t = _t(dur + 0.06)
    envl = np.minimum(1, t / 0.01) * np.where(t > dur, np.exp(-(t - dur) * 40), 1)
    s = sum(np.exp(-k / 5) / k * np.sin(2 * np.pi * f * k * t) for k in (1, 3, 5, 7, 2, 4))
    return (s * envl * 0.9).astype(np.float32)


def pad(freqs, dur, att=0.4, rel=0.8):
    t = _t(dur + rel)
    envl = np.minimum(1, t / att) * np.where(t > dur, np.exp(-(t - dur) * 4), 1)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0.004):
            s += sum(np.exp(-k / 2.5) / k * np.sin(2 * np.pi * f * (1 + det) * k * t + k) for k in range(1, 5))
    return (s * envl / len(freqs) / 2).astype(np.float32)


def hum(f, dur):
    t = _t(dur + 0.05)
    envl = np.minimum(1, t / 0.04) * np.where(t > dur, np.exp(-(t - dur) * 30), 1)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.2)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    return ((np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * envl * 0.8).astype(np.float32)


def kick():
    t = _t(0.35)
    return (np.sin(2 * np.pi * (50 * t + 120 * (1 - np.exp(-t * 35)) / 35)) * np.exp(-t * 10)).astype(np.float32)


def snare(brush=True):
    n = noise(0.22)
    t = _t(0.22)
    s = band(n, 1500, 9000) * np.exp(-t * (18 if brush else 28)) + (0 if brush else 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30))
    return (s * 0.7).astype(np.float32)


def shaker():
    t = _t(0.07)
    return (band(noise(0.07), 5000) * np.exp(-t * 60) * 0.5).astype(np.float32)


def tom(f=110):
    t = _t(0.4)
    return (np.sin(2 * np.pi * (f * t + f * 0.6 * (1 - np.exp(-t * 20)) / 20)) * np.exp(-t * 8)).astype(np.float32)


def cymbal(dur=1.6):
    t = _t(dur)
    return (band(noise(dur), 6000) * np.exp(-t * 2.5) * 0.45).astype(np.float32)


# --- sound effects
def fx_step():
    t = _t(0.09)
    return (band(noise(0.09), 80, 900) * np.exp(-t * 50) * 1.4).astype(np.float32)


def fx_slide(f0, f1, dur=0.9):
    t = _t(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    f = f * (1 + 0.025 * np.sin(2 * np.pi * 6 * t))
    envl = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.08)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * envl * 0.6 + band(noise(dur), 1000, 4000) * envl * 0.03).astype(np.float32)


def fx_ding():
    return (glock(hz(96), 1.6) * 0.7 + glock(hz(103), 1.6) * 0.4).astype(np.float32)


def fx_sniff():
    out = np.zeros(int(0.5 * SR), np.float32)
    for k in range(3):
        n = band(noise(0.09), 1500 + 400 * k, 6000) * np.hanning(int(0.09 * SR)).astype(np.float32)
        i = int(k * 0.15 * SR)
        out[i:i + len(n)] += n * 0.9
    return out


def fx_chomp():
    t = _t(0.16)
    crunch = band(noise(0.16), 500, 5000) * (np.random.default_rng(5).random(len(t)) > 0.55) * np.exp(-t * 18)
    thump = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 30)
    return ((crunch * 0.9 + thump * 0.7)).astype(np.float32)


def fx_scratch():
    dur = 0.45
    t = _t(dur)
    sweep = np.where(t < 0.18, 1 - t / 0.18 * 0.85, 0.15 + (t - 0.18) / 0.27 * 0.6)
    ph = 2 * np.pi * np.cumsum(900 * sweep) / SR
    s = band(noise(dur), 300, 6000) * (0.5 + 0.5 * np.sin(ph)) * np.minimum(1, (dur - t) / 0.05)
    return (s * 1.1).astype(np.float32)


def fx_burp():
    dur = 0.42
    t = _t(dur)
    f = 95 - 25 * t / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = sum(np.sin(k * ph) / k for k in range(1, 14))
    am = 0.6 + 0.4 * np.sin(2 * np.pi * 28 * t)
    envl = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.06)
    return (band(saw * am * envl, 60, 1800) * 0.9).astype(np.float32)


def fx_steam(dur=1.6):
    t = _t(dur)
    f = 1500 + 700 * t / dur
    envl = np.minimum(1, t / dur * 1.2) * np.minimum(1, (dur - t) / 0.1)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 + band(noise(dur), 2500, 9000) * 0.6
    return (s * envl * 0.6).astype(np.float32)


def fx_whimper():
    dur = 0.8
    t = _t(dur)
    f = 900 + 500 * np.sin(np.pi * t / dur) - 200 * t
    f = f * (1 + 0.03 * np.sin(2 * np.pi * 9 * t))
    envl = np.sin(np.pi * t / dur) ** 0.7
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * envl * 0.35).astype(np.float32)


def fx_sigh():
    dur = 1.1
    t = _t(dur)
    envl = np.sin(np.pi * t / dur) ** 1.5
    return (band(noise(dur), 200, 1600) * envl * 0.8).astype(np.float32)


def fx_tear():
    t = _t(0.32)
    crackle = (np.random.default_rng(9).random(len(t)) > 0.7).astype(np.float32)
    return (band(noise(0.32), 800, 7000) * crackle * np.minimum(1, (0.32 - t) / 0.05) * 1.2).astype(np.float32)


def fx_slurp():
    dur = 0.38
    t = _t(dur)
    f = 300 + 900 * t / dur
    envl = np.sin(np.pi * t / dur)
    return ((np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + band(noise(dur), 1500, 6000) * 0.25) * envl).astype(np.float32)


def fx_pop(f=700):
    t = _t(0.15)
    fr = f * 1.6 * np.exp(-t * 14) + f
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 26) * 0.7).astype(np.float32)


def fx_boing(dur=0.7):
    t = _t(dur)
    f = 180 * (1 + 0.35 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4) * 0.7).astype(np.float32)


def fx_clang():
    t = _t(1.0)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in
            ((830, 0.5, 6), (1650, 0.35, 8), (2390, 0.3, 10), (3720, 0.2, 14)))
    return ((s + band(noise(1.0), 200, 3000) * np.exp(-t * 40) * 0.4) * 0.6).astype(np.float32)


def fx_whoosh(dur=0.35):
    t = _t(dur)
    envl = np.sin(np.pi * t / dur) ** 2
    return (band(noise(dur), 400, 3000) * envl * 0.6).astype(np.float32)


def fx_jump():
    return fx_slide(300, 900, 0.25) * 0.8


class Mix:
    """Stereo mixing buffer with a cheap stereo room reverb."""

    def __init__(self, dur):
        self.L = np.zeros(int(dur * SR), np.float32)
        self.R = np.zeros_like(self.L)

    def put(self, t, sig, g=1.0, pan=0.0):
        i = int(t * SR)
        if i >= len(self.L) or i < 0:
            return
        n = min(len(sig), len(self.L) - i)
        self.L[i:i + n] += sig[:n] * g * math.sqrt((1 - pan) / 2) * 1.414
        self.R[i:i + n] += sig[:n] * g * math.sqrt((1 + pan) / 2) * 1.414

    def save(self, path):
        L, R = self.L.copy(), self.R.copy()
        for d, g in ((0.031, 0.25), (0.047, 0.2), (0.071, 0.16), (0.113, 0.12), (0.173, 0.08)):
            k = int(d * SR)
            L[k:] += g * self.R[:-k]
            R[k:] += g * self.L[:-k]
        st = np.stack([L, R], 1)
        st = np.tanh(st / max(1e-6, np.abs(st).max()) * 1.3) * 0.85
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((st * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    render(sys.argv[1])
