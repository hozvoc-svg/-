"""Vertical-first stickman scenes for mystery Shorts.

Every scene draws inside the central 9:16 column of the 16:9 canvas (x 656..1264), which build.py's
VERTICAL_FILL mode scales up to fill a 1080x1920 frame. Scenes work in local column coordinates:
0..CW wide, 0..H tall; visuals live in y 200..720 (the top holds the hook, the bottom the captions).
"""
import math, random
import cairo
from scenes import W, H, INK, DIM, RED, AMBER, clamp, ease, prog, rgba, text, rrect, line, vignette
from farm_scenes import stick, child, glow, lantern, _HIDE_LABELS, STARS

BG1, BG2 = (0.03, 0.04, 0.08), (0.08, 0.10, 0.18)
CW = 608
X0 = (W - CW) / 2
CYAN = (0.3, 0.93, 1.0)
GREEN = (0.35, 1.0, 0.5)
PAPER = (0.90, 0.86, 0.74)
NAVY = (0.30, 0.36, 0.44)


def col(c):
    """Enter column coordinates; scene content (y 200..800) is fitted between the hook and the captions."""
    c.translate(X0, 0)
    c.translate(CW / 2, 230)
    c.scale(0.75, 0.75)
    c.translate(-CW / 2, -200)


def hook(c, i, s, colr, size):
    """Pinned hook text at the top of a Short (screen coordinates), same look as the captions."""
    c.select_font_face("Inter Display Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    w = c.text_extents(s).x_advance
    if w > 980:
        size *= 980 / w
        c.set_font_size(size)
        w = 980
    y = 170 + i * 110
    c.new_path()
    c.move_to(540 - w / 2, y)
    c.text_path(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    rgba(c, (0, 0, 0), 0.95)
    c.set_line_width(size * 0.17)
    c.stroke_preserve()
    rgba(c, colr)
    c.fill()


def bg(c, top, bot, stars=False, T=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(-400, -400, CW + 800, H + 800)
    c.fill()
    if stars:
        for sx, sy, r, ph in STARS:
            x = sx * CW / W
            rgba(c, INK, 0.2 + 0.35 * (0.5 + 0.5 * math.sin(T * 1.2 + ph)))
            c.arc(x, sy, r, 0, 2 * math.pi)
            c.fill()


def sea(c, T, base, top=(0.10, 0.20, 0.30), bot=(0.02, 0.06, 0.10), amp=10):
    for L in range(3):
        f = L / 2
        colr = tuple(top[i] * (1 - f) + bot[i] * f for i in range(3))
        y0 = base + L * 70
        c.move_to(-400, H + 600)
        for x in range(-400, CW + 410, 16):
            c.line_to(x, y0 + amp * math.sin(x * 0.02 + T * 1.4 + L) + amp * 0.5 * math.sin(x * 0.05 - T * 2 + L))
        c.line_to(CW + 400, H + 600)
        c.close_path()
        rgba(c, colr)
        c.fill()


def plane(c, x, y, s=1.0, ang=0.0, colr=NAVY, a=1.0, prop_T=None):
    """Side view of a WWII-era single-engine plane, nose to the right."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    rgba(c, colr, a)
    c.move_to(-90, -6); c.curve_to(-40, -22, 50, -22, 80, -10); c.line_to(90, 0); c.line_to(80, 10)
    c.curve_to(40, 16, -40, 12, -90, 4); c.close_path(); c.fill()
    c.move_to(-80, -4); c.line_to(-104, -38); c.line_to(-90, -38); c.line_to(-60, -6); c.close_path(); c.fill()
    c.move_to(-10, 2); c.line_to(30, 2); c.line_to(10, 28); c.line_to(-20, 28); c.close_path(); c.fill()
    rgba(c, (0.6, 0.8, 0.95), 0.7 * a)
    c.move_to(10, -16); c.curve_to(20, -28, 45, -24, 50, -14); c.close_path(); c.fill()
    if prop_T is not None:
        h = 26 * abs(math.sin(prop_T * 40))
        line(c, 92, -h, 92, h, 4, (0.85, 0.85, 0.85), 0.7 * a)
    c.restore()


def paper(c, x, y, w, h, rot=0.0, a=1.0, colr=PAPER):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rgba(c, (0, 0, 0), 0.35 * a)
    c.rectangle(-w / 2 + 6, -h / 2 + 8, w, h)
    c.fill()
    rgba(c, colr, a)
    c.rectangle(-w / 2, -h / 2, w, h)
    c.fill()
    c.restore()


def big(c, s, x, y, size, colr=INK, a=1.0):
    """Bold outlined text, readable on any background."""
    c.select_font_face("Inter Display Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    w = c.text_extents(s).x_advance
    c.new_path()
    c.move_to(x - w / 2, y)
    c.text_path(s)
    rgba(c, (0, 0, 0), a)
    c.set_line_width(size * 0.16)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.stroke_preserve()
    rgba(c, colr, a)
    c.fill()


def pop(t, t0, dur=0.25):
    """Overshooting scale-in (0 -> 1.12 -> 1) starting at t0."""
    u = clamp((t - t0) / dur)
    return 0 if u <= 0 else (1 + 0.12 * math.sin(u * math.pi)) * ease(u)


# ================= Flight 19 =================

def sc_f19_takeoff(c, t, d, T, a):
    col(c)
    bg(c, (0.35, 0.55, 0.75), (0.85, 0.80, 0.70))
    sea(c, T, 640, (0.15, 0.35, 0.50), (0.05, 0.15, 0.25))
    for i in range(5):  # V formation drifting slowly across
        x = 330 - abs(i - 2) * 110 + 18 * t
        y = 300 + abs(i - 2) * 70 + i * 6 + 6 * math.sin(T * 2 + i)
        plane(c, x, y, 0.8, -0.04, prop_T=T)
    big(c, "DEC 5, 1945", CW / 2, 200, 44, AMBER, prog(t, 0.2, 0.6))


def sc_f19_compass(c, t, d, T, a):
    col(c)
    bg(c, (0.08, 0.08, 0.10), (0.15, 0.13, 0.12))
    for k, cx in enumerate((175, 435)):
        cy = 430
        rgba(c, (0.2, 0.2, 0.22))
        c.arc(cx, cy, 120, 0, 2 * math.pi)
        c.fill()
        rgba(c, (0.92, 0.92, 0.88))
        c.arc(cx, cy, 104, 0, 2 * math.pi)
        c.fill()
        for i, n in enumerate("NESW"):
            ang = i * math.pi / 2 - math.pi / 2
            text(c, n, cx + 78 * math.cos(ang), cy + 78 * math.sin(ang) + 12, 30, (0.15, 0.15, 0.18))
        spin = T * (7 + 3 * k) + k
        c.save()
        c.translate(cx, cy)
        c.rotate(spin)
        rgba(c, RED)
        c.move_to(0, -80); c.line_to(12, 0); c.line_to(-12, 0); c.close_path(); c.fill()
        rgba(c, (0.2, 0.2, 0.25))
        c.move_to(0, 80); c.line_to(12, 0); c.line_to(-12, 0); c.close_path(); c.fill()
        c.restore()
    s = pop(t, 0.6)
    if s:
        c.save(); c.translate(CW / 2, 660); c.scale(s, s)
        big(c, "BOTH COMPASSES OUT", 0, 0, 40, RED)
        c.restore()


def sc_f19_lost(c, t, d, T, a):
    col(c)
    bg(c, (0.05, 0.10, 0.16), (0.02, 0.05, 0.09))
    # simple Florida silhouette and the two positions
    rgba(c, (0.22, 0.28, 0.22))
    c.move_to(60, 200); c.line_to(230, 200); c.line_to(250, 330); c.line_to(300, 480); c.line_to(260, 560)
    c.line_to(200, 470); c.line_to(150, 330); c.line_to(60, 300); c.close_path(); c.fill()
    text(c, "FLORIDA", 170, 260, 26, INK)
    ap = prog(t, 0.3, 0.8)
    rgba(c, AMBER, ap)
    c.arc(220, 620, 14, 0, 2 * math.pi); c.fill()
    text(c, "where he thought", 220, 670, 26, AMBER, ap)
    ap = prog(t, d * 0.45, d * 0.6)
    pulse = 1 + 0.3 * math.sin(T * 5)
    rgba(c, RED, ap * 0.3)
    c.arc(470, 380, 30 * pulse, 0, 2 * math.pi); c.fill()
    rgba(c, RED, ap)
    c.arc(470, 380, 14, 0, 2 * math.pi); c.fill()
    text(c, "where they were", 470, 330, 26, RED, ap)
    text(c, "ATLANTIC", 470, 470, 26, (0.4, 0.6, 0.8), ap)


def sc_f19_night(c, t, d, T, a):
    col(c)
    bg(c, (0.01, 0.02, 0.05), (0.04, 0.06, 0.12), stars=True, T=T)
    sea(c, T, 640, (0.04, 0.08, 0.14), (0.01, 0.02, 0.05))
    for i in range(5):
        x = 120 + i * 90 + t * 20
        y = 300 + i * 50 + t * 25 * (1 + i * 0.2)
        plane(c, x, y, 0.75, 0.12 + 0.04 * i, colr=(0.18, 0.2, 0.26), prop_T=T)
    # fuel gauge
    c.save()
    c.translate(CW / 2, 600)
    rgba(c, (0.15, 0.15, 0.17))
    c.arc(0, 0, 70, math.pi, 2 * math.pi); c.fill()
    ang = math.pi + math.pi * (0.4 - 0.38 * prog(t, 0, d))
    line(c, 0, 0, 60 * math.cos(ang), 60 * math.sin(ang), 6, RED)
    text(c, "FUEL", 0, -20, 22, INK)
    c.restore()
    if t > d * 0.7 and (T % 0.8) < 0.5:
        big(c, "NO SIGNAL", CW / 2, 220, 44, RED)


def sc_f19_rescue(c, t, d, T, a):
    col(c)
    bg(c, (0.02, 0.03, 0.06), (0.06, 0.08, 0.14), stars=True, T=T)
    sea(c, T, 660, (0.04, 0.08, 0.14), (0.01, 0.02, 0.05))
    flash = prog(t, d * 0.6, d * 0.63) * (1 - prog(t, d * 0.63, d * 0.85))
    if t < d * 0.62:
        x = -80 + (CW + 160) * t / (d * 0.62) * 0.6
        plane(c, x, 360, 1.2, 0.0, colr=(0.35, 0.38, 0.42), prop_T=T)
        big(c, "13 MEN", x, 290, 34, AMBER)
    if flash > 0:
        glow(c, 300, 360, 340, (1.0, 0.6, 0.2), flash)
        rgba(c, (1, 1, 1), 0.35 * flash)
        c.paint()
    if t > d * 0.8:
        big(c, "GONE TOO", CW / 2, 300, 56, RED, prog(t, d * 0.8, d * 0.88))


def sc_f19_count(c, t, d, T, a):
    col(c)
    bg(c, (0.04, 0.05, 0.08), (0.08, 0.09, 0.13))
    sea(c, T, 720, (0.04, 0.08, 0.14), (0.01, 0.02, 0.05), amp=6)
    n = int(27 * prog(t, 0.2, d * 0.55))
    for i in range(n):
        x = 70 + (i % 9) * 58
        y = 250 + (i // 9) * 130
        stick(c, x, y + 90, 0.5, col=INK)
    big(c, f"{n} MEN", CW / 2, 220, 58, AMBER)
    big(c, "6 PLANES", CW / 2, 690, 48, INK, prog(t, d * 0.6, d * 0.7))


# ================= Somerton Man =================

def beach(c, T):
    bg(c, (0.55, 0.70, 0.85), (0.92, 0.85, 0.72))
    sea(c, T, 420, (0.25, 0.50, 0.65), (0.15, 0.35, 0.50), amp=6)
    rgba(c, (0.85, 0.76, 0.58))
    c.move_to(-400, 560); c.curve_to(200, 520, 400, 540, CW + 400, 500); c.line_to(CW + 400, H + 600); c.line_to(-400, H + 600)
    c.close_path(); c.fill()


def sc_som_beach(c, t, d, T, a):
    col(c)
    beach(c, T)
    stick(c, 300, 640, 1.3, col=(0.92, 0.92, 0.95), lying=-math.pi / 2)
    rgba(c, (0.35, 0.3, 0.25))
    c.rectangle(250, 560, 130, 20)
    c.fill()
    big(c, "DEC 1, 1948", CW / 2, 220, 44, AMBER, prog(t, 0.2, 0.6))
    s = pop(t, d * 0.55)
    if s:
        c.save(); c.translate(CW / 2, 330); c.scale(s, s); big(c, "NO ID", 0, 0, 72, RED); c.restore()


def sc_som_labels(c, t, d, T, a):
    col(c)
    bg(c, (0.12, 0.10, 0.10), (0.20, 0.17, 0.15))
    # jacket shape
    rgba(c, (0.25, 0.25, 0.3))
    c.move_to(160, 230); c.line_to(450, 230); c.line_to(520, 640); c.line_to(90, 640); c.close_path(); c.fill()
    line(c, CW / 2, 230, CW / 2, 640, 4, (0.12, 0.12, 0.15))
    rgba(c, (0.85, 0.85, 0.82))
    c.rectangle(250, 260, 110, 40)
    c.fill()
    cut = prog(t, 0.6, 1.4)
    if cut > 0:
        c.save()
        c.translate(305, 280)
        c.rotate(0.6 * cut)
        c.translate(200 * cut, 300 * cut)
        rgba(c, (0.85, 0.85, 0.82), 1 - cut)
        c.rectangle(-55, -20, 110, 40)
        c.fill()
        c.restore()
        rgba(c, (0.25, 0.25, 0.3))
        c.rectangle(250, 260, 110, 40)
        c.fill()
        c.set_dash([6, 5])
        line(c, 250, 280, 360, 280, 3, (0.7, 0.7, 0.7))
        c.set_dash([])
    big(c, "ALL LABELS CUT", CW / 2, 720, 42, RED, prog(t, d * 0.5, d * 0.6))


def sc_som_scrap(c, t, d, T, a):
    col(c)
    bg(c, (0.06, 0.05, 0.05), (0.12, 0.10, 0.09))
    glow(c, CW / 2, 430, 300, AMBER, 0.6)
    s = 0.6 + 0.4 * ease(prog(t, 0.2, 1.5))
    c.save()
    c.translate(CW / 2, 430)
    c.scale(s, s)
    paper(c, 0, 0, 380, 120, -0.05)
    c.select_font_face("Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(46)
    w = c.text_extents("Tamám Shud").x_advance
    c.move_to(-w / 2, 20)
    rgba(c, (0.15, 0.12, 0.1))
    c.show_text("Tamám Shud")
    c.restore()
    big(c, "“IT IS FINISHED”", CW / 2, 680, 42, AMBER, prog(t, d * 0.55, d * 0.65))


def sc_som_code(c, t, d, T, a):
    col(c)
    bg(c, (0.10, 0.08, 0.07), (0.18, 0.14, 0.12))
    c.save()
    c.translate(CW / 2, 450)
    c.rotate(-0.04)
    rgba(c, (0.35, 0.18, 0.12))
    c.rectangle(-230, -250, 460, 500)
    c.fill()
    paper(c, 0, 0, 420, 460)
    rows = ["WRGOABABD", "MLIAOI", "WTBIMPANETP", "MLIABOAIAQC", "ITTMTSAMSTGAB"]
    for i, r in enumerate(rows):
        n = int(len(r) * clamp((t - 0.3 - i * 0.5) / 0.5))
        c.select_font_face("Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(38)
        c.move_to(-180, -150 + i * 70)
        rgba(c, (0.15, 0.15, 0.25))
        c.show_text(r[:n])
    c.restore()
    big(c, "NEVER CRACKED", CW / 2, 760, 44, RED, prog(t, d * 0.6, d * 0.7))


def sc_som_dna(c, t, d, T, a):
    col(c)
    bg(c, (0.03, 0.05, 0.10), (0.06, 0.10, 0.18))
    for i in range(26):
        y = 200 + i * 20
        ph = i * 0.45 + T * 2
        x1 = CW / 2 + 110 * math.sin(ph)
        x2 = CW / 2 - 110 * math.sin(ph)
        line(c, x1, y, x2, y, 3, (0.5, 0.6, 0.8), 0.5)
        for x, colr in ((x1, CYAN), (x2, (1.0, 0.4, 0.6))):
            rgba(c, colr)
            c.arc(x, y, 7, 0, 2 * math.pi)
            c.fill()
    big(c, "2022", CW / 2, 200, 50, AMBER, prog(t, 0.2, 0.6))
    s = pop(t, d * 0.5)
    if s:
        c.save(); c.translate(CW / 2, 700); c.scale(s, s); big(c, "CARL WEBB", 0, 0, 62, GREEN); c.restore()


# ================= Roanoke =================

def forest_bg(c, T, top=(0.45, 0.55, 0.60), bot=(0.70, 0.66, 0.55)):
    bg(c, top, bot)
    r = random.Random(3)
    for k in range(22):
        x = r.randint(-300, CW + 300)
        h = r.randint(260, 420)
        rgba(c, (0.10, 0.16, 0.12))
        c.move_to(x - 50, 620); c.line_to(x, 620 - h); c.line_to(x + 50, 620); c.close_path(); c.fill()
    rgba(c, (0.35, 0.30, 0.20))
    c.rectangle(-400, 600, CW + 800, H + 600)
    c.fill()


def hut(c, x, y, s=1.0, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rgba(c, (0.40, 0.30, 0.20), a)
    c.rectangle(-60, -70, 120, 70)
    c.fill()
    rgba(c, (0.55, 0.45, 0.25), a)
    c.move_to(-75, -68); c.line_to(0, -130); c.line_to(75, -68); c.close_path(); c.fill()
    rgba(c, (0.15, 0.1, 0.08), a)
    c.rectangle(-15, -40, 30, 40)
    c.fill()
    c.restore()


def sc_roa_colony(c, t, d, T, a):
    col(c)
    forest_bg(c, T)
    for i, x in enumerate((110, 300, 490)):
        hut(c, x, 600, 1.0)
    for i in range(7):
        stick(c, 60 + i * 80, 690, 0.8, col=INK if i else AMBER, phase=T * 3 + i if i % 2 else None)
    big(c, "1587", CW / 2, 220, 64, AMBER, prog(t, 0.1, 0.5))
    big(c, "~115 SETTLERS", CW / 2, 300, 42, INK, prog(t, 0.6, 1.0))


def sc_roa_sail(c, t, d, T, a):
    col(c)
    bg(c, (0.55, 0.65, 0.75), (0.85, 0.80, 0.70))
    sea(c, T, 520, (0.2, 0.4, 0.55), (0.08, 0.2, 0.32))
    x = CW / 2 + 260 * prog(t, 0.2, d)
    c.save()
    c.translate(x, 540)
    c.scale(0.9, 0.9)
    rgba(c, (0.25, 0.16, 0.10))
    c.move_to(-120, -20); c.line_to(120, -20); c.line_to(90, 30); c.line_to(-90, 30); c.close_path(); c.fill()
    line(c, 0, -20, 0, -230, 7, (0.25, 0.16, 0.10))
    rgba(c, PAPER)
    c.move_to(-80, -210); c.line_to(80, -210); c.line_to(90, -60); c.line_to(-90, -60); c.close_path(); c.fill()
    c.restore()
    big(c, "BACK TO ENGLAND", CW / 2, 220, 40, INK, prog(t, 0.2, 0.7))
    yrs = int(3 * prog(t, d * 0.4, d * 0.85))
    big(c, f"{yrs} YEARS", CW / 2, 700, 60, RED, prog(t, d * 0.4, d * 0.5))


def sc_roa_empty(c, t, d, T, a):
    col(c)
    forest_bg(c, T, (0.35, 0.40, 0.45), (0.55, 0.52, 0.45))
    for x in (110, 300, 490):
        hut(c, x, 600, 1.0, a=1 - prog(t, 0.3, 1.5) * 0.85)
    stick(c, 300, 700, 1.0, col=AMBER, arms=(0.35, -1.0))
    big(c, "1590", CW / 2, 220, 64, AMBER, prog(t, 0.1, 0.5))
    s = pop(t, d * 0.5)
    if s:
        c.save(); c.translate(CW / 2, 330); c.scale(s, s); big(c, "EVERYONE GONE", 0, 0, 52, RED); c.restore()


def sc_roa_post(c, t, d, T, a):
    col(c)
    forest_bg(c, T, (0.30, 0.34, 0.38), (0.50, 0.46, 0.40))
    rgba(c, (0.42, 0.30, 0.18))
    c.rectangle(CW / 2 - 70, 200, 140, 560)
    c.fill()
    for k in range(6):
        line(c, CW / 2 - 60 + k * 24, 210, CW / 2 - 60 + k * 24, 750, 2, (0.32, 0.22, 0.13))
    word = "CROATOAN"
    n = int(len(word) * prog(t, 0.4, d * 0.7))
    c.save()
    c.translate(CW / 2 + 18, 230)
    c.rotate(math.pi / 2)
    c.select_font_face("Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(66)
    c.move_to(0, 0)
    rgba(c, (0.12, 0.07, 0.04))
    c.show_text(word[:n])
    c.restore()


def sc_roa_cross(c, t, d, T, a):
    col(c)
    bg(c, (0.20, 0.17, 0.14), (0.30, 0.25, 0.20))
    paper(c, CW / 2, 430, 420, 440, 0.02)
    ap = prog(t, 0.3, 0.8)
    line(c, CW / 2, 280, CW / 2, 560, 22, (0.6, 0.15, 0.12), ap)
    line(c, CW / 2 - 100, 380, CW / 2 + 100, 380, 22, (0.6, 0.15, 0.12), ap)
    text(c, "danger signal", CW / 2, 610, 30, (0.25, 0.2, 0.15), ap)
    if t > d * 0.5:
        s = pop(t, d * 0.5)
        c.save(); c.translate(CW / 2, 430); c.scale(s * 2.2, s * 2.2)
        line(c, -60, -60, 60, 60, 14, RED)
        line(c, -60, 60, 60, -60, 14, RED)
        c.restore()
        big(c, "NO CROSS", CW / 2, 740, 56, RED, prog(t, d * 0.55, d * 0.65))


def sc_roa_dare(c, t, d, T, a):
    col(c)
    forest_bg(c, T, (0.15, 0.18, 0.22), (0.30, 0.28, 0.25))
    glow(c, CW / 2, 480, 260, (0.9, 0.9, 1.0), 0.3)
    child(c, CW / 2, 640, 1.6, INK)
    big(c, "VIRGINIA DARE", CW / 2, 230, 48, AMBER, prog(t, 0.2, 0.7))
    text(c, "first English child born in America", CW / 2, 290, 26, INK, prog(t, 0.6, 1.1))
    big(c, "NEVER FOUND", CW / 2, 740, 54, RED, prog(t, d * 0.6, d * 0.7))


# ================= D.B. Cooper =================

def jet_cabin(c):
    bg(c, (0.16, 0.16, 0.18), (0.26, 0.25, 0.24))
    for k in range(4):
        y = 230 + k * 140
        rgba(c, (0.35, 0.38, 0.45))
        rrect(c, 40, y, 160, 110, 14); c.fill()
        rrect(c, CW - 200, y, 160, 110, 14); c.fill()


def sc_db_board(c, t, d, T, a):
    col(c)
    bg(c, (0.25, 0.30, 0.38), (0.45, 0.45, 0.48))
    # 727 silhouette
    rgba(c, (0.85, 0.85, 0.88))
    c.move_to(20, 420); c.curve_to(100, 380, 480, 380, 560, 410); c.line_to(590, 430); c.line_to(560, 450)
    c.curve_to(480, 470, 100, 470, 20, 440); c.close_path(); c.fill()
    c.move_to(60, 420); c.line_to(20, 320); c.line_to(70, 320); c.line_to(130, 415); c.close_path(); c.fill()
    for i in range(10):
        rgba(c, (0.2, 0.25, 0.35))
        c.arc(170 + i * 36, 422, 7, 0, 2 * math.pi); c.fill()
    stick(c, 300, 660, 1.3, col=INK)
    rgba(c, (0.1, 0.1, 0.12))
    c.rectangle(285, 535, 30, 70)  # dark suit
    c.fill()
    big(c, "NOV 24, 1971", CW / 2, 220, 44, AMBER, prog(t, 0.2, 0.6))
    big(c, "“DAN COOPER”", CW / 2, 300, 40, INK, prog(t, d * 0.5, d * 0.6))


def sc_db_note(c, t, d, T, a):
    col(c)
    jet_cabin(c)
    s = 0.5 + 0.7 * ease(prog(t, 0.2, 1.2))
    c.save()
    c.translate(CW / 2, 430)
    c.scale(s, s)
    paper(c, 0, 0, 360, 220, 0.04, colr=(0.97, 0.97, 0.95))
    c.select_font_face("Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(38)
    msg = "I HAVE A BOMB"
    w = c.text_extents(msg).x_advance
    c.move_to(-w / 2, 18)
    rgba(c, (0.1, 0.1, 0.12))
    c.show_text(msg)
    c.restore()


def sc_db_money(c, t, d, T, a):
    col(c)
    bg(c, (0.10, 0.12, 0.10), (0.18, 0.20, 0.16))
    n = int(28 * prog(t, 0.2, d * 0.5))
    r = random.Random(4)
    for i in range(n):
        x, y = r.randint(60, CW - 60), r.randint(260, 640)
        c.save(); c.translate(x, y); c.rotate(r.uniform(-0.6, 0.6))
        rgba(c, (0.55, 0.70, 0.45)); c.rectangle(-55, -25, 110, 50); c.fill()
        rgba(c, (0.35, 0.5, 0.3)); c.arc(0, 0, 14, 0, 2 * math.pi); c.fill()
        c.restore()
    big(c, "$200,000", CW / 2, 220, 70, GREEN, prog(t, 0.2, 0.6))
    ap = prog(t, d * 0.55, d * 0.65)
    for i in range(4):
        x = 110 + i * 130
        rgba(c, (0.85, 0.35, 0.2), ap)
        c.arc(x, 720, 50, math.pi, 2 * math.pi); c.fill()
    big(c, "+ 4 PARACHUTES", CW / 2, 800, 40, INK, ap)


def sc_db_jump(c, t, d, T, a):
    col(c)
    bg(c, (0.02, 0.03, 0.05), (0.05, 0.07, 0.08))
    # rain
    for i in range(70):
        x = (i * 53 + T * 300) % (CW + 100) - 50
        y = (i * 97 + T * 900) % H
        line(c, x, y, x - 8, y + 26, 2, (0.6, 0.7, 0.8), 0.35)
    # forest far below
    r = random.Random(8)
    for k in range(28):
        x = r.randint(-300, CW + 300)
        rgba(c, (0.03, 0.06, 0.04))
        c.move_to(x - 40, 800); c.line_to(x, 640 + r.randint(0, 60)); c.line_to(x + 40, 800); c.close_path(); c.fill()
    # rear stairs of the jet at the top
    rgba(c, (0.55, 0.55, 0.58))
    c.move_to(-400, 165); c.line_to(CW + 400, 195); c.line_to(CW + 400, 255); c.line_to(-400, 235); c.close_path(); c.fill()
    line(c, 380, 245, 470, 330, 10, (0.45, 0.45, 0.48))
    f = prog(t, d * 0.3, d)
    stick(c, 470 - 60 * f, 330 + 360 * f * f, 1.0, col=INK, arms=(1.2, -1.2), lying=0.4 * f)


def sc_db_found(c, t, d, T, a):
    col(c)
    bg(c, (0.55, 0.60, 0.65), (0.75, 0.70, 0.60))
    rgba(c, (0.30, 0.45, 0.55))
    c.rectangle(-400, 380, CW + 800, 120)
    c.fill()
    rgba(c, (0.75, 0.66, 0.50))
    c.rectangle(-400, 500, CW + 800, H + 600)
    c.fill()
    child(c, 200, 660, 1.4, AMBER, arms=(0.9, -0.3))
    ap = prog(t, d * 0.3, d * 0.45)
    for i in range(3):
        c.save(); c.translate(360 + i * 50, 640 - i * 6); c.rotate(-0.3 + i * 0.2)
        rgba(c, (0.6, 0.62, 0.45), ap); c.rectangle(-45, -20, 90, 40); c.fill(); c.restore()
    big(c, "1980", CW / 2, 220, 64, AMBER, prog(t, 0.1, 0.5))
    big(c, "$5,800 FOUND", CW / 2, 760, 48, GREEN, prog(t, d * 0.45, d * 0.55))


def sc_db_file(c, t, d, T, a):
    col(c)
    bg(c, (0.10, 0.10, 0.12), (0.16, 0.16, 0.18))
    paper(c, CW / 2, 450, 440, 520, -0.03, colr=(0.82, 0.72, 0.52))
    text(c, "FBI", CW / 2, 300, 60, (0.15, 0.12, 0.1))
    text(c, "CASE: NORJAK", CW / 2, 370, 34, (0.2, 0.15, 0.1))
    s = pop(t, d * 0.35)
    if s:
        c.save(); c.translate(CW / 2, 530); c.rotate(-0.2); c.scale(s, s)
        rgba(c, RED); c.set_line_width(8); rrect(c, -190, -55, 380, 100, 10); c.stroke()
        big(c, "UNSOLVED", 0, 20, 64, RED)
        c.restore()


# ================= Wow! signal =================

def sc_wow_dish(c, t, d, T, a):
    col(c)
    bg(c, (0.02, 0.03, 0.08), (0.08, 0.10, 0.20), stars=True, T=T)
    rgba(c, (0.08, 0.10, 0.08))
    c.rectangle(-400, 650, CW + 800, H + 600)
    c.fill()
    # Big Ear: a long flat reflector with a tilted panel
    rgba(c, (0.55, 0.58, 0.62))
    c.move_to(20, 640); c.line_to(CW - 20, 640); c.line_to(CW - 60, 600); c.line_to(60, 600); c.close_path(); c.fill()
    c.move_to(40, 600); c.line_to(140, 380); c.line_to(170, 380); c.line_to(80, 600); c.close_path(); c.fill()
    for k in range(4):
        r = 40 + 60 * ((T * 0.8 + k * 0.25) % 1)
        c.set_line_width(4)
        rgba(c, CYAN, 0.6 * (1 - ((T * 0.8 + k * 0.25) % 1)))
        c.arc(CW / 2, 250, r, 0.2 * math.pi, 0.8 * math.pi)
        c.stroke()
    big(c, "AUG 15, 1977", CW / 2, 220, 44, AMBER, prog(t, 0.1, 0.5))
    big(c, "BIG EAR · OHIO", CW / 2, 730, 40, INK, prog(t, 0.6, 1.1))


def printout(c, t, circle=0.0, wow=0.0):
    paper(c, CW / 2, 450, 460, 560, 0.0, colr=(0.95, 0.95, 0.92))
    r = random.Random(2)
    for row in range(14):
        y = 210 + row * 36
        for colm in range(8):
            ch = r.choice("1111 1 12 1 3 1")
            if colm == 4 and 5 <= row <= 10:
                ch = "6EQUJ5"[row - 5]
            text(c, ch, 120 + colm * 52, y, 26, (0.25, 0.25, 0.3), 1.0, bold=False)
    if circle:
        c.set_line_width(6)
        rgba(c, RED, circle)
        c.save(); c.translate(328, 300); c.scale(1, 3.2)
        c.arc(0, 0, 38, 0, 2 * math.pi * circle); c.restore(); c.stroke()
    if wow:
        c.select_font_face("Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
        c.set_font_size(70)
        c.move_to(380, 300)
        rgba(c, RED, wow)
        c.show_text("Wow!")


def sc_wow_print(c, t, d, T, a):
    col(c)
    bg(c, (0.20, 0.18, 0.16), (0.30, 0.27, 0.24))
    printout(c, t, circle=prog(t, d * 0.5, d * 0.9) if a.get("circle") else 0, wow=prog(t, d * 0.6, d * 0.8) if a.get("circle") else 0)
    if not a.get("circle"):
        big(c, "6EQUJ5", CW / 2, 790, 64, CYAN, prog(t, d * 0.5, d * 0.6))


def sc_wow_sky(c, t, d, T, a):
    col(c)
    bg(c, (0.01, 0.01, 0.04), (0.04, 0.03, 0.10), stars=True, T=T)
    pts = [(220, 300), (300, 260), (360, 330), (300, 400), (240, 470), (350, 500), (420, 430)]
    ap = prog(t, 0.2, 1.0)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        line(c, x0, y0, x1, y1, 2, (0.6, 0.7, 1.0), 0.6 * ap)
    for x, y in pts:
        rgba(c, INK, ap); c.arc(x, y, 6, 0, 2 * math.pi); c.fill()
    text(c, "SAGITTARIUS", CW / 2, 600, 32, (0.6, 0.7, 1.0), ap)
    sec = int(72 * prog(t, 0.3, d * 0.8))
    big(c, f"{sec} SECONDS", CW / 2, 220, 56, AMBER)


def sc_wow_search(c, t, d, T, a):
    col(c)
    bg(c, (0.01, 0.01, 0.04), (0.04, 0.03, 0.10), stars=True, T=T)
    for k in range(3):
        ang = -math.pi / 2 + 0.6 * math.sin(T * 0.6 + k * 2)
        x0, y0 = 120 + k * 180, 700
        c.set_line_width(40)
        rgba(c, CYAN, 0.08)
        c.move_to(x0, y0); c.line_to(x0 + 600 * math.cos(ang), y0 + 600 * math.sin(ang)); c.stroke()
        rgba(c, (0.6, 0.6, 0.65))
        c.arc(x0, y0, 40, math.pi, 2 * math.pi); c.fill()
    big(c, "NEVER", CW / 2, 300, 72, RED, prog(t, d * 0.4, d * 0.5))
    big(c, "CAME BACK", CW / 2, 380, 60, RED, prog(t, d * 0.5, d * 0.6))


# ================= Voynich manuscript =================

def book(c, open_=1.0, a=1.0, script=1.0, T=0.0):
    c.save()
    c.translate(CW / 2, 450)
    rgba(c, (0.40, 0.25, 0.15), a)
    c.rectangle(-280, -240, 560, 480)
    c.fill()
    for side in (-1, 1):
        rgba(c, (0.88, 0.80, 0.62), a)
        c.rectangle(-265 if side < 0 else 5, -225, 260, 450)
        c.fill()
    r = random.Random(5)
    # plant drawing on the left page
    rgba(c, (0.25, 0.5, 0.25), a)
    c.set_line_width(5)
    c.move_to(-135, 180); c.curve_to(-150, 80, -110, 20, -135, -60); c.stroke()
    for k in range(5):
        c.save(); c.translate(-135, 120 - k * 40); c.rotate((k % 2 - 0.5) * 1.4)
        c.scale(1, 0.45); c.arc(30, 0, 30, 0, 2 * math.pi); c.restore(); c.fill()
    rgba(c, (0.8, 0.3, 0.4), a)
    c.arc(-135, -80, 26, 0, 2 * math.pi); c.fill()
    # strange script on the right page
    rows = int(10 * script)
    for row in range(rows):
        x = 30
        y = -190 + row * 40
        rr = random.Random(row)
        while x < 240:
            wlen = rr.randint(2, 5)
            for _ in range(wlen):
                c.set_line_width(2.5)
                rgba(c, (0.30, 0.20, 0.12), a)
                k = rr.randint(0, 3)
                if k == 0:
                    c.arc(x + 5, y, 5, 0, 2 * math.pi)
                elif k == 1:
                    c.move_to(x, y + 6); c.curve_to(x + 4, y - 12, x + 10, y - 4, x + 8, y + 6)
                elif k == 2:
                    c.move_to(x, y - 8); c.line_to(x + 3, y + 6); c.line_to(x + 9, y - 6)
                else:
                    c.arc(x + 5, y, 5, math.pi, 2 * math.pi); c.line_to(x + 10, y + 8)
                c.stroke()
                x += 12
            x += 12
    c.restore()


def sc_voy_book(c, t, d, T, a):
    col(c)
    bg(c, (0.10, 0.08, 0.06), (0.18, 0.14, 0.10))
    glow(c, CW / 2, 450, 380, AMBER, 0.5)
    book(c, script=prog(t, 0.2, d * 0.8), T=T)
    big(c, "~240 PAGES", CW / 2, 760, 46, INK, prog(t, d * 0.5, d * 0.6))


def sc_voy_date(c, t, d, T, a):
    col(c)
    bg(c, (0.06, 0.06, 0.08), (0.12, 0.12, 0.15))
    yr = int(2025 - (2025 - 1404) * ease(prog(t, 0.2, d * 0.7)))
    big(c, str(yr), CW / 2, 460, 130, AMBER)
    big(c, "CARBON DATED", CW / 2, 260, 44, INK, prog(t, 0.1, 0.5))
    big(c, "1404 – 1438", CW / 2, 640, 48, CYAN, prog(t, d * 0.7, d * 0.8))


def sc_voy_script(c, t, d, T, a):
    col(c)
    bg(c, (0.10, 0.08, 0.06), (0.18, 0.14, 0.10))
    c.save()
    c.translate(-CW / 2 * 0.6, -450 * 0.6)
    c.scale(1.6, 1.6)
    book(c, script=1.0, T=T)
    c.restore()
    for i, lang in enumerate(["LATIN", "GREEK", "HEBREW", "ARABIC"]):
        ap = prog(t, 0.3 + i * 0.5, 0.6 + i * 0.5)
        y = 250 + i * 90
        big(c, lang, CW / 2 - 60, y, 40, INK, ap)
        c.save(); c.translate(CW / 2 + 140, y - 14)
        line(c, -18, -18, 18, 18, 8, RED, ap); line(c, -18, 18, 18, -18, 8, RED, ap)
        c.restore()


def sc_voy_codebreakers(c, t, d, T, a):
    col(c)
    bg(c, (0.08, 0.10, 0.08), (0.14, 0.16, 0.13))
    rgba(c, (0.25, 0.20, 0.15))
    c.rectangle(40, 560, CW - 80, 30)
    c.fill()
    for i, x in enumerate((140, 300, 460)):
        stick(c, x, 560, 1.1, col=INK, head_hold=1.0 if t > d * 0.5 and i != 1 else 0.0, arms=None)
        text(c, "?", x + 30, 330 - 10 * math.sin(T * 2 + i), 60, RED, prog(t, d * 0.3 + i * 0.3, d * 0.4 + i * 0.3))
    big(c, "WWII CODEBREAKERS", CW / 2, 230, 40, AMBER, prog(t, 0.1, 0.5))
    big(c, "FAILED", CW / 2, 720, 64, RED, prog(t, d * 0.55, d * 0.65))


def sc_voy_plant(c, t, d, T, a):
    col(c)
    bg(c, (0.88, 0.80, 0.62), (0.80, 0.70, 0.52))
    c.save()
    c.translate(CW / 2, 450)
    sw = 0.05 * math.sin(T)
    c.rotate(sw)
    rgba(c, (0.45, 0.30, 0.18))
    for k in range(5):  # strange roots
        c.set_line_width(8)
        c.move_to(0, 200); c.curve_to(-80 + k * 40, 240, -120 + k * 60, 260, -140 + k * 70, 300); c.stroke()
    rgba(c, (0.25, 0.5, 0.25))
    c.set_line_width(10)
    c.move_to(0, 200); c.curve_to(-20, 100, 30, 0, 0, -120); c.stroke()
    for k in range(6):
        c.save(); c.translate(0, 150 - k * 50); c.rotate((k % 2 - 0.5) * 1.6)
        c.scale(1, 0.4); c.arc(50, 0, 50, 0, 2 * math.pi); c.restore(); c.fill()
    for k in range(5):
        ang = k * 2 * math.pi / 5 + T * 0.2
        rgba(c, (0.75, 0.25, 0.35))
        c.arc(40 * math.cos(ang), -160 + 40 * math.sin(ang), 26, 0, 2 * math.pi); c.fill()
    rgba(c, (0.95, 0.8, 0.3))
    c.arc(0, -160, 22, 0, 2 * math.pi); c.fill()
    c.restore()
    big(c, "UNKNOWN PLANT", CW / 2, 230, 48, RED, prog(t, d * 0.3, d * 0.45))


def sc_voy_yale(c, t, d, T, a):
    col(c)
    bg(c, (0.14, 0.12, 0.14), (0.22, 0.18, 0.18))
    for k in range(5):  # shelves
        y = 220 + k * 110
        rgba(c, (0.30, 0.20, 0.12))
        c.rectangle(-400, y + 80, CW + 800, 14)
        c.fill()
        r = random.Random(k)
        x = -400
        while x < CW + 400:
            w = r.randint(16, 30)
            rgba(c, (r.uniform(0.2, 0.5), r.uniform(0.1, 0.3), r.uniform(0.1, 0.3)))
            c.rectangle(x, y + 80 - r.randint(60, 78), w, r.randint(60, 78))
            c.fill()
            x += w + 3
    glow(c, CW / 2, 480, 260, AMBER, 0.6)
    rgba(c, (0.12, 0.10, 0.10), 0.85)
    c.rectangle(CW / 2 - 150, 400, 300, 200)
    c.fill()
    big(c, "YALE UNIVERSITY", CW / 2, 470, 34, INK, prog(t, 0.2, 0.7))
    big(c, "0 WORDS READ", CW / 2, 560, 44, RED, prog(t, d * 0.45, d * 0.55))


def _scene(fn):
    def run(c, t, d, T, a):
        _HIDE_LABELS[0] = True
        fn(c, t, d, T, a)
    return run


SCENES = {k[3:]: _scene(v) for k, v in globals().items() if k.startswith("sc_")}
