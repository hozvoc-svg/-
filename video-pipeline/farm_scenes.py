"""Stickman scenes for rural night mysteries (Hinterkaifeck): a lonely farm, a forest, snow, lanterns."""
import math, random
import cairo
from scenes import (W, H, INK, DIM, RED, AMBER, SNOW, clamp, ease, prog, rgba, text, text_w, rrect, label, line,
                    stick, snowfall, tree, vignette, xmark, check, STARS)

BG1, BG2 = (0.025, 0.03, 0.06), (0.08, 0.09, 0.15)
GROUND = (0.62, 0.66, 0.76)
WOOD = (0.16, 0.12, 0.10)
WALL = (0.30, 0.28, 0.30)
ROOF = (0.11, 0.09, 0.10)
FOREST = (0.03, 0.05, 0.06)
VICTIM = (0.42, 0.45, 0.55)
FAMILY = [("Andreas Gruber", "63"), ("Cäzilia Gruber", "72"), ("Viktoria Gabriel", "35"),
          ("Cäzilia", "7"), ("Josef", "2"), ("Maria Baumgartner", "44")]

_r = random.Random(5)
SMOKE = [(_r.random(), _r.random() * 6.28, _r.random()) for _ in range(26)]
_r = random.Random(9)
DUST = [(_r.random() * W, _r.random() * H, _r.random(), _r.random() * 6.28) for _ in range(60)]


# ---------- environment ----------

def night(c, T, top=BG1, bot=BG2, stars=True, moon=True):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    if stars:
        for sx, sy, r, ph in STARS:
            rgba(c, INK, 0.18 + 0.3 * (0.5 + 0.5 * math.sin(T * 1.1 + ph)))
            c.arc(sx, sy, r, 0, 2 * math.pi)
            c.fill()
    if moon:
        g = cairo.RadialGradient(1580, 190, 10, 1580, 190, 260)
        g.add_color_stop_rgba(0, 0.85, 0.88, 1.0, 0.25)
        g.add_color_stop_rgba(1, 0.85, 0.88, 1.0, 0)
        c.set_source(g)
        c.arc(1580, 190, 260, 0, 2 * math.pi)
        c.fill()
        rgba(c, (0.92, 0.93, 0.98))
        c.arc(1580, 190, 52, 0, 2 * math.pi)
        c.fill()
        # drifting cloud bands across the moon
        for k in range(3):
            x = (T * (14 + 6 * k) + k * 700) % (W + 1200) - 600
            rgba(c, top, 0.55)
            rrect(c, x, 150 + k * 46, 520 - k * 90, 34, 17)
            c.fill()


def treeline(c, base=760, seed=4, col=FOREST, scale=1.0, x0=-100, x1=W + 100):
    r = random.Random(seed)
    x = x0
    while x < x1:
        tree(c, x, base + r.randint(0, 30), int(r.randint(170, 280) * scale), col=col, snow=True)
        x += r.randint(38, 70) * scale


def field(c, base=800, col=GROUND):
    g = cairo.LinearGradient(0, base, 0, H)
    g.add_color_stop_rgb(0, col[0] * 0.75, col[1] * 0.75, col[2] * 0.8)
    g.add_color_stop_rgb(1, col[0] * 0.45, col[1] * 0.45, col[2] * 0.55)
    c.set_source(g)
    c.rectangle(-400, base, W + 800, H + 600 - base)
    c.fill()


def smoke(c, x, y, T, a=1.0):
    for u, ph, sp in SMOKE:
        k = (T * (0.06 + 0.05 * sp) + u) % 1.0
        px = x + 140 * k * k + 18 * math.sin(T * 0.8 + ph)
        py = y - 420 * k
        rgba(c, (0.75, 0.77, 0.85), a * 0.22 * (1 - k) * min(1, k * 8))
        c.arc(px, py, 14 + 60 * k, 0, 2 * math.pi)
        c.fill()


def glow(c, x, y, r, col=AMBER, a=1.0):
    g = cairo.RadialGradient(x, y, 2, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.55 * a)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def lantern(c, x, y, T, a=1.0, s=1.0):
    fl = 0.8 + 0.2 * math.sin(T * 11) * math.sin(T * 6.7)
    glow(c, x, y, 190 * s * fl, AMBER, a)
    rgba(c, (0.12, 0.10, 0.08), a)
    c.rectangle(x - 10 * s, y - 16 * s, 20 * s, 30 * s)
    c.fill()
    rgba(c, (1.0, 0.8, 0.4), a)
    c.rectangle(x - 6 * s, y - 11 * s, 12 * s, 20 * s)
    c.fill()


def farm(c, x, y, s=1.0, lights=(0, 0, 0), T=0.0, smoke_a=0.0, door=0.0, barn_light=0.0, attic=0.0):
    """House (left) and barn (right) under one long roof; (x, y) = bottom-left corner."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if smoke_a:
        smoke(c, 250, -330, T, smoke_a)
    # walls
    rgba(c, WALL)
    c.rectangle(0, -210, 380, 210)
    c.fill()
    rgba(c, WOOD)
    c.rectangle(380, -240, 460, 240)
    c.fill()
    for i in range(12):  # barn planks
        line(c, 400 + i * 38, -235, 400 + i * 38, -4, 3, (0.10, 0.07, 0.06))
    # one continuous roof
    c.move_to(-30, -205)
    c.line_to(170, -345)
    c.line_to(700, -365)
    c.line_to(870, -235)
    c.close_path()
    rgba(c, ROOF)
    c.fill()
    rgba(c, SNOW, 0.75)
    c.move_to(-30, -205)
    c.line_to(170, -345)
    c.line_to(700, -365)
    c.line_to(870, -235)
    c.line_to(850, -232)
    c.line_to(700, -350)
    c.line_to(175, -330)
    c.line_to(-10, -203)
    c.close_path()
    c.fill()
    # chimney
    rgba(c, (0.2, 0.18, 0.2))
    c.rectangle(232, -365, 36, 60)
    c.fill()
    # attic hatch window
    rgba(c, (0.05, 0.05, 0.07))
    c.rectangle(420, -320, 70, 40)
    c.fill()
    if attic:
        rgba(c, AMBER, attic)
        c.rectangle(420, -320, 70, 40)
        c.fill()
        glow(c, 455, -300, 120, AMBER, attic * 0.8)
    # house windows
    for i, wx in enumerate((50, 160, 270)):
        lit = lights[i] if i < len(lights) else 0
        rgba(c, (0.06, 0.06, 0.09))
        c.rectangle(wx, -160, 64, 74)
        c.fill()
        if lit:
            fl = 0.85 + 0.15 * math.sin(T * 7 + i)
            rgba(c, (1.0, 0.72, 0.32), lit * fl)
            c.rectangle(wx, -160, 64, 74)
            c.fill()
            glow(c, wx + 32, -120, 110, AMBER, lit * 0.6)
        line(c, wx + 32, -160, wx + 32, -86, 4, (0.18, 0.16, 0.18))
        line(c, wx, -123, wx + 64, -123, 4, (0.18, 0.16, 0.18))
    rgba(c, (0.12, 0.09, 0.08))
    c.rectangle(330, -130, 40, 130)  # house door
    c.fill()
    # barn door (opens to the right)
    rgba(c, (0.03, 0.03, 0.04))
    c.rectangle(560, -180, 160, 180)
    c.fill()
    if barn_light:
        rgba(c, (1.0, 0.7, 0.3), barn_light * 0.8)
        c.rectangle(560, -180, 160 * min(1, door + 0.05), 180)
        c.fill()
    rgba(c, (0.22, 0.16, 0.12))
    c.rectangle(560 + 150 * door, -180, 160 * (1 - door * 0.85), 180)
    c.fill()
    line(c, 560 + 150 * door, -180, 720, -0, 5, (0.12, 0.08, 0.06))
    c.restore()


def snow_steps(c, pts, p, a=1.0, col=(0.20, 0.22, 0.32), size=1.0):
    """Single trail of footprints along a polyline, revealed up to fraction p."""
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.hypot(b[0] - a_[0], b[1] - a_[1]) for a_, b in seg]
    total = sum(lens)
    n = int(total / 34)
    for i in range(int(n * p)):
        dist = i * 34
        for (a_, b), L in zip(seg, lens):
            if dist <= L:
                f = dist / L
                px, py = a_[0] + (b[0] - a_[0]) * f, a_[1] + (b[1] - a_[1]) * f
                nx, ny = -(b[1] - a_[1]) / L, (b[0] - a_[0]) / L
                side = 7 if i % 2 else -7
                c.save()
                c.translate(px + nx * side, py + ny * side)
                c.scale(size, 0.5 * size)
                c.arc(0, 0, 7, 0, 2 * math.pi)
                c.restore()
                rgba(c, col, a)
                c.fill()
                break
            dist -= L


def dust(c, T, a=0.5):
    for x0, y0, sp, ph in DUST:
        x = (x0 + 12 * math.sin(T * 0.3 + ph)) % W
        y = (y0 - T * (6 + 10 * sp)) % H
        rgba(c, (1, 0.85, 0.6), a * (0.2 + 0.4 * sp))
        c.arc(x, y, 1.2 + 1.8 * sp, 0, 2 * math.pi)
        c.fill()


def panel(c, x, y, w, h, a=1.0, col=(0.10, 0.11, 0.17)):
    rgba(c, col, 0.92 * a)
    rrect(c, x, y, w, h, 18)
    c.fill()


def interior(c, col=(0.10, 0.08, 0.08)):
    rgba(c, col)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(-2, 26):  # wall planks
        line(c, i * 80, 0, i * 80, 820, 3, (0.06, 0.05, 0.05))
    rgba(c, (0.07, 0.05, 0.05))
    c.rectangle(-400, 820, W + 800, 600)
    c.fill()


def rough_stick(c, x, y, s, col, a=1.0, **kw):
    stick(c, x, y, s, col=col, a=a, **kw)


def child(c, x, y, s, col=INK, a=1.0, **kw):
    stick(c, x, y, s * 0.62, col=col, a=a, **kw)


# ---------- scenes ----------

def sc_farm_open(c, t, d, T, a):
    night(c, T)
    treeline(c, 700, seed=2)
    field(c, 760)
    farm(c, 520, 830, 1.05, lights=(0, 0.9 * prog(t, d * 0.25, d * 0.35), 0), T=T, smoke_a=prog(t, 0.5, 2.5))
    if a.get("caption_cows"):
        pass
    snowfall(c, T, 0.25, 0.4)


def sc_tracks(c, t, d, T, a):
    night(c, T)
    treeline(c, 640, seed=6, scale=0.9)
    field(c, 700)
    farm(c, 1100, 860, 0.85, T=T)
    p = prog(t, 0.4, d * 0.7)
    snow_steps(c, [(120, 720), (420, 820), (780, 880), (1150, 905)], p, size=1.3)
    if t > d * 0.75:
        ap = prog(t, d * 0.75, d * 0.85)
        label(c, "no tracks going back", 640, 520, 44, RED, ap)
        xmark(c, 400, 980, 26, ap)
    label(c, "from the forest", 300, 600, 36, (0.7, 0.85, 1.0), prog(t, d * 0.2, d * 0.3))
    snowfall(c, T, 0.3, 0.3)


def sc_title(c, t, d, T, a):
    night(c, T, moon=False)
    treeline(c, 1010, seed=8, col=(0.02, 0.03, 0.04))
    s = 1 + 0.025 * t
    c.save()
    c.translate(W / 2, 470)
    c.scale(s, s)
    text(c, "THE HINTERKAIFECK", 0, 0, 112, INK, prog(t, 0, 0.6))
    text(c, "MURDERS", 0, 135, 120, RED, prog(t, 0.3, 0.9))
    c.restore()
    w = 900 * prog(t, 0.6, 1.6)
    line(c, W / 2 - w / 2, 670, W / 2 + w / 2, 670, 6, RED)
    text(c, "1922  ·  Bavaria, Germany", W / 2, 740, 40, DIM, prog(t, 1.0, 1.8), bold=False)
    snowfall(c, T, 0.3, 0.3)


def sc_map(c, t, d, T, a):
    rgba(c, (0.06, 0.07, 0.10))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(0, W, 80):
        line(c, i, 0, i, H, 1, DIM, 0.07)
    for j in range(0, H, 80):
        line(c, 0, j, W, j, 1, DIM, 0.07)
    # Danube
    c.set_line_width(10)
    rgba(c, (0.25, 0.42, 0.65), 0.7)
    c.move_to(200, 300)
    c.curve_to(600, 380, 900, 260, 1250, 330)
    c.curve_to(1500, 380, 1650, 300, 1850, 360)
    c.stroke()
    text(c, "Danube", 420, 300, 30, (0.4, 0.6, 0.85), 0.8, bold=False)
    pts = [("Munich", 980, 900, INK), ("Ingolstadt", 1000, 330, INK), ("Schrobenhausen", 780, 560, INK)]
    for i, (n, x, y, col) in enumerate(pts):
        ap = prog(t, 0.3 + i * 0.4, 0.7 + i * 0.4)
        rgba(c, col, ap)
        c.arc(x, y, 12, 0, 2 * math.pi)
        c.fill()
        text(c, n, x + 26, y + 12, 38, col, ap, align="left")
    fx, fy = 930, 470
    ap = prog(t, d * 0.3, d * 0.4)
    pulse = 1 + 0.25 * math.sin(T * 4)
    rgba(c, RED, ap * 0.35)
    c.arc(fx, fy, 30 * pulse, 0, 2 * math.pi)
    c.fill()
    rgba(c, RED, ap)
    c.arc(fx, fy, 14, 0, 2 * math.pi)
    c.fill()
    text(c, "Hinterkaifeck", fx + 30, fy - 18, 44, RED, ap, align="left")
    ap2 = prog(t, d * 0.5, d * 0.65)
    c.set_dash([16, 12])
    line(c, fx, fy + 20, 980, 880, 4, AMBER, ap2)
    c.set_dash([])
    label(c, "~70 km north of Munich", 1400, 700, 40, AMBER, ap2)


def sc_layout(c, t, d, T, a):
    night(c, T, stars=False, moon=False)
    treeline(c, 760, seed=3)
    field(c, 800)
    c.save()
    c.translate(W / 2, 880)
    c.scale(1.35, 1.35)
    farm(c, -430, 0, 1.0, T=T, lights=(0.6, 0, 0.6))
    c.restore()
    ap = prog(t, d * 0.25, d * 0.35)
    label(c, "HOUSE", W / 2 - 330, 300, 44, INK, ap)
    label(c, "BARN", W / 2 + 280, 300, 44, INK, ap)
    ap = prog(t, d * 0.45, d * 0.55)
    # inner passage arrow
    c.set_dash([14, 10])
    line(c, W / 2 - 200, 760, W / 2 + 160, 760, 6, AMBER, ap)
    c.set_dash([])
    c.move_to(W / 2 + 180, 760)
    c.line_to(W / 2 + 150, 740)
    c.line_to(W / 2 + 150, 780)
    c.close_path()
    rgba(c, AMBER, ap)
    c.fill()
    label(c, "connected inside", W / 2, 200, 40, AMBER, ap)


def sc_family(c, t, d, T, a):
    night(c, T, moon=False)
    treeline(c, 820, seed=11, col=(0.03, 0.04, 0.05))
    field(c, 860)
    xs = [300, 620, 940, 1260, 1540]
    for i in range(5):
        ap = prog(t, 0.6 + i * 1.3, 1.1 + i * 1.3)
        y = 880 - 20 * (1 - ap)
        if i >= 3:
            child(c, xs[i], y, 1.3 if i == 3 else 1.0, INK, ap)
        else:
            stick(c, xs[i], y, 1.25, col=INK, a=ap)
        n, age = FAMILY[i]
        text(c, n, xs[i], 600 if i < 3 else 700, 32, INK, ap)
        text(c, age, xs[i], 645 if i < 3 else 745, 30, AMBER, ap, bold=False)
    text(c, "The Gruber family", W / 2, 240, 60, INK, prog(t, 0.2, 1.0))


def sc_secret(c, t, d, T, a):
    interior(c)
    lantern(c, W / 2, 330, T, 1.0, 1.3)
    stick(c, 760, 860, 1.4, col=INK)
    stick(c, 1160, 860, 1.3, col=INK)
    text(c, "Andreas", 760, 560, 36, INK)
    text(c, "Viktoria", 1160, 560, 36, INK)
    if a.get("war"):
        ap = prog(t, d * 0.35, d * 0.45)
        c.save()
        c.translate(1550, 420)
        rgba(c, (0.85, 0.82, 0.72), ap)
        c.rectangle(-200, -150, 400, 300)
        c.fill()
        text(c, "KARL GABRIEL", 0, -80, 36, (0.15, 0.12, 0.1), ap)
        text(c, "killed in action, 1914", 0, -30, 28, (0.3, 0.25, 0.2), ap, bold=False)
        text(c, "body never identified", 0, 20, 28, RED, prog(t, d * 0.6, d * 0.7), bold=False)
        c.restore()
    else:
        ap = prog(t, d * 0.4, d * 0.5)
        c.save()
        c.translate(W / 2, 220)
        c.rotate(-0.04)
        rgba(c, RED, ap)
        c.set_line_width(6)
        rrect(c, -330, -60, 660, 110, 10)
        c.stroke()
        text(c, "CONVICTED · 1915", 0, 15, 56, RED, ap)
        c.restore()


def sc_neighbour(c, t, d, T, a):
    night(c, T, moon=False)
    field(c, 860)
    farm(c, 1060, 870, 0.75, T=T, lights=(0.7, 0, 0))
    # small neighbour house
    rgba(c, WALL)
    c.rectangle(120, 690, 260, 180)
    c.fill()
    c.move_to(100, 695)
    c.line_to(250, 600)
    c.line_to(400, 695)
    c.close_path()
    rgba(c, ROOF)
    c.fill()
    stick(c, 470, 870, 1.2, col=AMBER)
    label(c, "Lorenz Schlittenbauer", 470, 560, 36, AMBER, prog(t, 0.4, 1.0))
    stick(c, 1000, 870, 1.15, col=INK)
    child(c, 1060, 870, 0.9, INK)
    text(c, "Viktoria & Josef", 1030, 600, 30, INK, prog(t, 1.0, 1.6))
    ap = prog(t, d * 0.35, d * 0.45)
    for k in range(3):
        text(c, "?", 730 + k * 70, 520 - 20 * math.sin(T * 2 + k), 70, RED, ap * prog(t, d * (0.35 + 0.1 * k), d * (0.45 + 0.1 * k)))
    label(c, "Who is Josef's father?", 760, 300, 46, INK, ap)
    snowfall(c, T, 0.2, 0.3)


def sc_maid_leaves(c, t, d, T, a):
    night(c, T)
    treeline(c, 700, seed=12)
    field(c, 760)
    farm(c, 1050, 830, 0.8, T=T, lights=(0, 0.5, 0))
    x = 950 - t * 70
    stick(c, x, 880, 1.15, col=INK, phase=T * 5)
    rgba(c, (0.35, 0.22, 0.14))
    c.rectangle(x + 18, 830, 40, 30)
    c.fill()
    label(c, "the maid quits", x, 620, 38, INK, prog(t, 0.5, 1.2))
    ap = prog(t, d * 0.35, d * 0.45)
    for k, s in enumerate(["footsteps...", "noises in the attic..."]):
        text(c, s, 1430 + k * 30, 470 + k * 70, 36, (0.75, 0.82, 1.0), ap * (0.6 + 0.4 * math.sin(T * 3 + k)), italic=True, bold=False)
    snowfall(c, T, 0.3)


def sc_signs(c, t, d, T, a):
    night(c, T, stars=False, moon=False)
    items = [("Footprints from the forest, none going back", "steps"), ("A Munich newspaper nobody bought", "paper"),
             ("A set of house keys goes missing", "keys"), ("Someone tried to break the tool-shed lock", "lock")]
    for i, (s, icon) in enumerate(items):
        ap = prog(t, 0.6 + i * (d * 0.2), 1.1 + i * (d * 0.2))
        y = 230 + i * 190
        panel(c, 300, y - 80, 1320, 140, ap)
        cx, cy = 400, y - 10
        if icon == "steps":
            for k in range(4):
                c.save(); c.translate(cx - 30 + k * 20, cy + 20 - k * 14); c.scale(1, 0.55)
                c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); rgba(c, SNOW, ap); c.fill()
        elif icon == "paper":
            rgba(c, (0.85, 0.82, 0.72), ap); c.rectangle(cx - 35, cy - 30, 70, 56); c.fill()
            for k in range(4):
                line(c, cx - 25, cy - 18 + k * 12, cx + 25, cy - 18 + k * 12, 3, (0.3, 0.3, 0.3), ap)
        elif icon == "keys":
            c.set_line_width(7); rgba(c, AMBER, ap); c.arc(cx - 15, cy, 16, 0, 2 * math.pi); c.stroke()
            line(c, cx, cy, cx + 40, cy, 7, AMBER, ap); line(c, cx + 30, cy, cx + 30, cy + 14, 6, AMBER, ap)
        else:
            rgba(c, DIM, ap); rrect(c, cx - 28, cy - 8, 56, 44, 6); c.fill()
            c.set_line_width(8); rgba(c, DIM, ap); c.arc(cx, cy - 8, 20, math.pi, 1.75 * math.pi); c.stroke()
            line(c, cx + 14, cy - 20, cx + 34, cy - 36, 5, RED, ap)
        text(c, s, 480, y + 12, 44, INK, ap, align="left")


def sc_attic(c, t, d, T, a):
    rgba(c, (0.04, 0.035, 0.04))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    # rafters
    for i in range(-3, 14):
        line(c, W / 2, 80, i * 170, H, 10, (0.10, 0.07, 0.06))
    for k in range(5):
        y = 250 + k * 170
        line(c, -100, y, W + 100, y, 8, (0.09, 0.06, 0.05))
    px = 500 + 700 * prog(t, d * 0.2, d * 0.8)
    lantern(c, px + 40, 760, T, 1.0, 1.4)
    stick(c, px, 900, 1.3, col=(0.85, 0.75, 0.6), phase=T * 3 if 0.2 * d < t < 0.8 * d else None, arms=(0.35, -1.6))
    dust(c, T, 0.4)
    # unseen presence: a shadow slipping away at the edge of the light
    ap = prog(t, d * 0.55, d * 0.6) * (1 - prog(t, d * 0.75, d * 0.85))
    stick(c, 1700, 900, 1.3, col=(0.0, 0.0, 0.0), a=ap * 0.9)
    label(c, "nothing there", 960, 200, 44, INK, prog(t, d * 0.85, d * 0.95))


def sc_refuse(c, t, d, T, a):
    night(c, T, moon=False)
    field(c, 860)
    farm(c, 1150, 870, 0.7, T=T, lights=(0.7, 0.7, 0))
    stick(c, 700, 870, 1.25, col=INK)
    text(c, "Andreas", 700, 590, 32, INK)
    for i in range(2):
        stick(c, 980 + i * 120, 870, 1.15, col=DIM, arms=(0.35, -1.2) if i == 0 else None)
    label(c, "“We can help you.”", 1100, 380, 40, DIM, prog(t, d * 0.2, d * 0.3))
    label(c, "“No. I'll handle it myself.”", 640, 300, 44, AMBER, prog(t, d * 0.5, d * 0.6))


def sc_arrival(c, t, d, T, a):
    day = 1 - prog(t, d * 0.6, d)
    top = tuple(BG1[i] * (1 - day) + (0.35, 0.40, 0.55)[i] * day for i in range(3))
    bot = tuple(BG2[i] * (1 - day) + (0.75, 0.62, 0.55)[i] * day for i in range(3))
    night(c, T, top=top, bot=bot, stars=day < 0.3, moon=False)
    treeline(c, 700, seed=12)
    field(c, 760)
    farm(c, 1050, 830, 0.8, T=T, lights=(0.8 * (1 - day), 0.8 * (1 - day), 0))
    w = prog(t, 0, d * 0.5)
    x = 150 + 750 * w
    stick(c, x, 890, 1.15, col=AMBER, phase=T * 5 if w < 1 else None)
    rgba(c, (0.35, 0.22, 0.14))
    c.rectangle(x + 18, 840, 40, 30)
    c.fill()
    sx = x - 110 if w < 1 else 790 - 600 * prog(t, d * 0.55, d * 0.9)
    stick(c, sx, 890, 1.1, col=DIM, phase=T * 5 if (w < 1 or t > d * 0.55) else None)
    label(c, "Maria Baumgartner, 44", 600, 560, 38, AMBER, prog(t, 0.5, 1.2))
    label(c, "Friday, March 31, 1922", 460, 200, 46, INK, prog(t, 0.2, 0.9))


def sc_barn_night(c, t, d, T, a):
    night(c, T, top=(0.01, 0.01, 0.03), bot=(0.04, 0.04, 0.08))
    treeline(c, 700, seed=2, col=(0.02, 0.03, 0.04))
    field(c, 760, (0.35, 0.38, 0.46))
    n = a.get("n", 4)
    door = 0.6 + 0.4 * math.sin(T * 0.5)
    farm(c, 380, 830, 1.15, T=T, door=door, barn_light=0.5 + 0.2 * math.sin(T * 9))
    # figures disappearing one by one towards the barn door
    for i in range(n):
        st, en = d * (0.1 + 0.2 * i), d * (0.25 + 0.2 * i)
        if t < st:
            x = 1600 - i * 40
            ap = 1.0
        else:
            f = prog(t, st, en)
            x = 1600 - i * 40 - (1600 - i * 40 - 1150) * f
            ap = 1 - prog(t, en - 0.4, en)
        if ap > 0:
            fn = child if i == 3 else stick
            fn(c, x, 880, 1.1, col=VICTIM, a=ap, phase=T * 4 + i if st < t < en else None)
    rgba(c, (0, 0, 0), 0.25)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


def sc_house_dark(c, t, d, T, a):
    night(c, T, top=(0.01, 0.01, 0.03), bot=(0.04, 0.04, 0.08))
    treeline(c, 700, seed=2, col=(0.02, 0.03, 0.04))
    field(c, 760, (0.35, 0.38, 0.46))
    l1 = 1 - prog(t, d * 0.35, d * 0.4)
    l2 = 1 - prog(t, d * 0.6, d * 0.65)
    farm(c, 380, 830, 1.15, lights=(l1, l2, 0), T=T)
    for i, (k, s) in enumerate([(0.35, "Maria · the maid's room"), (0.6, "Josef · his cot")]):
        label(c, s, 1500, 380 + i * 100, 36, DIM, prog(t, d * k, d * k + 0.6))
    ap = prog(t, d * 0.8, d * 0.9)
    label(c, "6 people. 1 night.", W / 2, 180, 60, RED, ap)


def sc_days_after(c, t, d, T, a):
    night(c, T, top=(0.30, 0.34, 0.45), bot=(0.62, 0.60, 0.62), stars=False, moon=False)
    treeline(c, 700, seed=12, col=(0.10, 0.13, 0.14))
    field(c, 760, (0.80, 0.82, 0.88))
    farm(c, 400, 830, 1.0, T=T, smoke_a=1.0)
    days = ["Sat · Apr 1", "Sun · Apr 2", "Mon · Apr 3"]
    k = min(2, int(3 * t / d))
    panel(c, 1350, 160, 430, 120, 1.0)
    text(c, days[k], 1565, 240, 50, INK)
    for i, s in enumerate(["cattle fed", "food eaten", "chimney smoking"]):
        label(c, s, 1565, 450 + i * 110, 40, AMBER, prog(t, d * (0.2 + 0.2 * i), d * (0.28 + 0.2 * i)))


def sc_absent(c, t, d, T, a):
    rgba(c, (0.22, 0.20, 0.20))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    rgba(c, (0.08, 0.16, 0.12))
    c.rectangle(560, 120, 800, 330)
    c.fill()
    text(c, "1.4.1922", 960, 300, 70, (0.9, 0.9, 0.85), 0.8, bold=False)
    for r in range(2):
        for k in range(5):
            x, y = 380 + k * 290, 720 + r * 200
            rgba(c, WOOD)
            c.rectangle(x - 90, y - 60, 180, 22)
            c.fill()
            if not (r == 0 and k == 2):
                child(c, x, y + 60, 1.0, INK)
    ap = prog(t, d * 0.3, d * 0.4)
    c.set_line_width(5)
    c.set_dash([10, 8])
    rgba(c, RED, ap)
    c.arc(960, 690, 110, 0, 2 * math.pi)
    c.stroke()
    c.set_dash([])
    label(c, "Cäzilia, 7 · absent", 960, 540, 38, RED, ap)
    if t > d * 0.6:
        label(c, "Sunday: the family misses church", 960, 90, 40, AMBER, prog(t, d * 0.6, d * 0.7))


def sc_mechanic(c, t, d, T, a):
    night(c, T, top=(0.35, 0.40, 0.52), bot=(0.70, 0.66, 0.64), stars=False, moon=False)
    treeline(c, 700, seed=12, col=(0.10, 0.13, 0.14))
    field(c, 760, (0.70, 0.72, 0.78))
    farm(c, 250, 830, 1.0, T=T)
    # machine
    mx = 1280
    rgba(c, (0.25, 0.27, 0.30))
    rrect(c, mx - 90, 760, 180, 110, 10)
    c.fill()
    c.save()
    c.translate(mx + 90, 790)
    c.rotate(T * 2 if t < d * 0.7 else 0)
    c.set_line_width(6)
    rgba(c, DIM)
    c.arc(0, 0, 36, 0, 2 * math.pi)
    c.stroke()
    line(c, -36, 0, 36, 0, 5, DIM)
    c.restore()
    stick(c, mx - 150, 880, 1.15, col=AMBER, arms=(0.9 + 0.3 * math.sin(T * 6), 1.2))
    label(c, "Albert Hofner, mechanic", mx - 150, 600, 36, AMBER, prog(t, 0.3, 1.0))
    if (T % 2.2) < 0.9 and t > d * 0.25:
        text(c, "WOOF", 700, 560 + 10 * math.sin(T * 9), 40, (0.85, 0.85, 0.9), 0.8)
    label(c, "~4.5 hours alone", 1600, 260, 42, INK, prog(t, d * 0.45, d * 0.55))
    # the attic hatch: is someone watching?
    ap = prog(t, d * 0.75, d * 0.85)
    c.save()
    c.translate(250, 830)
    rgba(c, (1, 1, 1), ap * (0.6 + 0.4 * math.sin(T * 5)))
    c.arc(445, -300, 4, 0, 2 * math.pi)
    c.arc(463, -300, 4, 0, 2 * math.pi)
    c.fill()
    c.restore()


def sc_discovery(c, t, d, T, a):
    night(c, T, top=(0.30, 0.34, 0.45), bot=(0.62, 0.60, 0.62), stars=False, moon=False)
    treeline(c, 700, seed=12, col=(0.10, 0.13, 0.14))
    field(c, 760, (0.70, 0.72, 0.78))
    door = prog(t, d * 0.55, d * 0.8)
    farm(c, 300, 830, 1.05, T=T, door=door)
    w = prog(t, 0, d * 0.5)
    for i in range(3):
        x = 1750 - i * 110 - 700 * w
        stick(c, x, 880, 1.1, col=AMBER if i == 0 else INK, phase=T * 5 + i if w < 1 else None)
    label(c, "Tuesday, April 4, 1922", 450, 160, 46, INK, prog(t, 0.2, 0.9))
    label(c, "Schlittenbauer", 1050, 560, 34, AMBER, prog(t, d * 0.3, d * 0.4))


def sc_money(c, t, d, T, a):
    interior(c)
    lantern(c, 600, 330, T, 1.0, 1.2)
    # chest with money
    rgba(c, WOOD)
    rrect(c, 760, 600, 420, 220, 12)
    c.fill()
    for k in range(6):
        x = 820 + k * 55
        rgba(c, (0.55, 0.7, 0.45))
        c.rectangle(x, 560 - (k % 2) * 10, 48, 60)
        c.fill()
    for k in range(5):
        rgba(c, AMBER)
        c.arc(1100 - k * 18, 575 - (k % 2) * 6, 16, 0, 2 * math.pi)
        c.fill()
    ap = prog(t, d * 0.35, d * 0.45)
    label(c, "money left untouched", 970, 440, 48, AMBER, ap)
    ap = prog(t, d * 0.65, d * 0.75)
    label(c, "not a robbery?", 1500, 260, 48, RED, ap)
    stick(c, 400, 860, 1.3, col=(0.6, 0.65, 0.8), arms=(0.5, -1.3))
    text(c, "POLICE", 400, 560, 30, (0.6, 0.65, 0.8))


def sc_board(c, t, d, T, a):
    rgba(c, (0.28, 0.20, 0.14))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    r = random.Random(3)
    cards = []
    for i in range(16):
        x, y = 200 + (i % 6) * 280 + r.randint(-30, 30), 180 + (i // 6) * 270 + r.randint(-20, 20)
        cards.append((x, y))
    ap_all = prog(t, 0.2, d * 0.5)
    shown = int(len(cards) * ap_all)
    for i in range(shown):
        x, y = cards[i]
        if i:
            line(c, cards[i - 1][0], cards[i - 1][1] - 40, x, y - 40, 3, RED, 0.8)
    for i in range(shown):
        x, y = cards[i]
        c.save()
        c.translate(x, y)
        c.rotate((i % 3 - 1) * 0.05)
        rgba(c, (0.90, 0.88, 0.80))
        c.rectangle(-90, -70, 180, 140)
        c.fill()
        stick(c, 0, 50, 0.55, col=(0.2, 0.2, 0.22))
        rgba(c, RED)
        c.arc(0, -60, 8, 0, 2 * math.pi)
        c.fill()
        c.restore()
    label(c, "100+ people questioned", W / 2, 1010, 46, INK, prog(t, d * 0.5, d * 0.6))
    if a.get("seer"):
        ap = prog(t, d * 0.65, d * 0.75)
        glow(c, 1600, 800, 220, (0.6, 0.5, 1.0), ap)
        rgba(c, (0.75, 0.7, 1.0), ap * 0.8)
        c.arc(1600, 800, 80, 0, 2 * math.pi)
        c.fill()
        label(c, "even clairvoyants", 1600, 640, 36, (0.8, 0.75, 1.0), ap)


def sc_suspect(c, t, d, T, a):
    rgba(c, (0.06, 0.06, 0.08))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    g = cairo.RadialGradient(620, 300, 20, 620, 500, 600)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.25)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    c.set_source(g)
    c.paint()
    for k in range(5):  # height chart
        line(c, 360, 300 + k * 130, 880, 300 + k * 130, 2, DIM, 0.4)
    col = a.get("col", AMBER)
    stick(c, 620, 880, 2.2, col=col)
    rgba(c, (0.1, 0.1, 0.12))
    c.rectangle(470, 760, 300, 90)
    c.fill()
    text(c, a.get("name", "?"), 620, 822, 34, INK)
    for i, s in enumerate(a.get("points", [])):
        ap = prog(t, d * (0.15 + 0.17 * i), d * (0.22 + 0.17 * i))
        panel(c, 1000, 220 + i * 150, 780, 110, ap)
        text(c, s, 1040, 290 + i * 150, 38, INK, ap, align="left")
    if a.get("verdict"):
        ap = prog(t, d * 0.85, d * 0.92)
        c.save()
        c.translate(620, 450)
        c.rotate(-0.15)
        rgba(c, RED, ap)
        c.set_line_width(8)
        rrect(c, -260, -60, 520, 110, 10)
        c.stroke()
        text(c, a["verdict"], 0, 18, 54, RED, ap)
        c.restore()


def sc_soldier(c, t, d, T, a):
    night(c, T, top=(0.12, 0.10, 0.10), bot=(0.30, 0.22, 0.18), stars=False, moon=False)
    rgba(c, (0.12, 0.09, 0.07))
    c.rectangle(-400, 820, W + 800, 700)
    c.fill()
    for k in range(9):  # barbed wire posts
        x = 100 + k * 220
        line(c, x, 820, x, 700, 8, (0.2, 0.15, 0.12))
    line(c, 0, 730, W, 740, 3, (0.35, 0.3, 0.28))
    line(c, 0, 770, W, 765, 3, (0.35, 0.3, 0.28))
    x = 760 + 200 * prog(t, d * 0.4, d)
    stick(c, x, 820, 1.4, col=INK, phase=T * 4 if t > d * 0.4 else None)
    c.move_to(x - 30, 820 - 1.4 * 135)
    c.line_to(x + 30, 820 - 1.4 * 135)
    c.line_to(x, 820 - 1.4 * 160)
    c.close_path()
    rgba(c, (0.35, 0.40, 0.30))
    c.fill()
    label(c, "Karl Gabriel", x, 520, 40, INK, prog(t, 0.3, 1.0))
    label(c, "Did he survive the war?", W / 2, 200, 50, AMBER, prog(t, d * 0.3, d * 0.4))
    text(c, "?", x + 160, 640 - 10 * math.sin(T * 2), 110, RED, prog(t, d * 0.5, d * 0.6))


def sc_stranger(c, t, d, T, a):
    night(c, T)
    treeline(c, 700, seed=6)
    field(c, 760)
    farm(c, 640, 830, 1.0, T=T, attic=0.3 + 0.2 * math.sin(T * 2), lights=(0.6, 0, 0.5))
    x = 1700 - 400 * prog(t, 0.3, d * 0.6)
    stick(c, x, 880, 1.1, col=(0.0, 0.0, 0.0), phase=T * 4 if t < d * 0.6 else None)
    glow(c, x, 820, 80, (0.4, 0.5, 0.7), 0.4)
    label(c, "traveling workers? thieves?", 1500, 300, 42, INK, prog(t, d * 0.2, d * 0.3))
    label(c, "someone who knew their routine", 1500, 400, 38, AMBER, prog(t, d * 0.6, d * 0.7))
    snowfall(c, T, 0.25, 0.3)


def sc_demolition(c, t, d, T, a):
    night(c, T, top=(0.35, 0.40, 0.52), bot=(0.70, 0.66, 0.64), stars=False, moon=False)
    treeline(c, 700, seed=12, col=(0.10, 0.13, 0.14))
    field(c, 760, (0.42, 0.45, 0.38))
    down = prog(t, 0.5, d * 0.5)
    c.save()
    c.translate(0, 300 * down * down)
    c.rectangle(-400, -600, W + 800, 830 + 600)
    c.clip()
    farm(c, 500, 830, 1.0, T=T)
    c.restore()
    for i in range(3):
        stick(c, 1450 + i * 120, 880, 1.1, col=INK, arms=(0.8, -1.4 + 0.4 * math.sin(T * 6 + i)))
    label(c, "1923: the farm is torn down", 600, 180, 46, INK, prog(t, 0.2, 0.9))
    ap = prog(t, d * 0.55, d * 0.65)
    if ap:
        c.save()
        c.translate(1000, 520)
        c.rotate(-0.5 + 0.05 * math.sin(T * 2))
        line(c, -150, 0, 130, 0, 14, WOOD, ap)
        c.move_to(110, -20)
        c.line_to(190, -70)
        c.line_to(200, -60)
        c.line_to(135, 25)
        c.close_path()
        rgba(c, (0.55, 0.57, 0.62), ap)
        c.fill()
        c.restore()
        glow(c, 1000, 520, 260, AMBER, ap * 0.4)
        label(c, "the weapon, hidden in the attic", 1000, 360, 40, RED, ap)


def sc_academy(c, t, d, T, a):
    rgba(c, (0.12, 0.14, 0.18))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    panel(c, 260, 130, 1400, 520, 1.0, (0.18, 0.22, 0.30))
    text(c, "CASE FILE · HINTERKAIFECK", 960, 230, 52, INK, prog(t, 0.2, 0.8))
    text(c, "Reviewed 2007 · Police Academy, Fürstenfeldbruck", 960, 300, 34, DIM, prog(t, 0.6, 1.2), bold=False)
    text(c, "Most likely suspect:", 760, 440, 44, INK, prog(t, d * 0.3, d * 0.4), align="right")
    ap = prog(t, d * 0.4, d * 0.5)
    rgba(c, (0.02, 0.02, 0.03), ap)
    c.rectangle(800, 395, 560, 60)
    c.fill()
    label(c, "name withheld", 1080, 560, 40, RED, prog(t, d * 0.6, d * 0.7))
    for i in range(4):
        stick(c, 520 + i * 300, 1000, 1.0, col=(0.6, 0.65, 0.8), arms=(0.9, -0.9))


def sc_unsolved(c, t, d, T, a):
    night(c, T, stars=False, moon=False)
    rows = ["Who was walking in the attic?", "Why did the killer stay for days?", "Why was the money left behind?",
            "Who did it?"]
    for i, s in enumerate(rows):
        ap = prog(t, 0.3 + i * d * 0.2, 0.8 + i * d * 0.2)
        y = 300 + i * 160
        panel(c, 360, y - 70, 1200, 110, ap)
        text(c, "?", 440, y + 5, 70, RED, ap)
        text(c, s, 510, y, 48, INK, ap, align="left")


def sc_memorial(c, t, d, T, a):
    dawn = prog(t, 0, d)
    bot = tuple(BG2[i] * (1 - dawn) + (0.72, 0.45, 0.38)[i] * dawn for i in range(3))
    night(c, T, bot=bot, moon=False)
    treeline(c, 760, seed=4, col=(0.02, 0.025, 0.03))
    rgba(c, (0.04, 0.05, 0.06))
    c.rectangle(-400, 800, W + 800, 700)
    c.fill()
    # wayside cross
    cx = 960
    line(c, cx, 800, cx, 480, 18, (0.02, 0.02, 0.03))
    line(c, cx - 90, 560, cx + 90, 560, 18, (0.02, 0.02, 0.03))
    c.move_to(cx - 70, 470)
    c.line_to(cx, 420)
    c.line_to(cx + 70, 470)
    c.close_path()
    rgba(c, (0.02, 0.02, 0.03))
    c.fill()
    for i, (n, age) in enumerate(FAMILY):
        ap = prog(t, 0.5 + i * 0.5, 1.0 + i * 0.5)
        x = 260 + i * 280
        text(c, n, x, 900 + (i % 2) * 46, 26, INK, ap, bold=False)
    text(c, "HINTERKAIFECK  ·  1922", W / 2, 250, 72, INK, prog(t, d * 0.55, d * 0.7))


def sc_outro(c, t, d, T, a):
    night(c, T)
    treeline(c, 820, seed=8, col=(0.02, 0.03, 0.04))
    field(c, 860)
    text(c, "Who do you think did it?", W / 2, 260, 80, INK, prog(t, 0, 0.5))
    opts = [("The neighbor", AMBER), ("The husband", INK), ("A stranger in the attic", (0.7, 0.8, 1.0))]
    for i, (s, col) in enumerate(opts):
        label(c, s, 480 + i * 480, 420, 40, col, prog(t, 0.8 + i * 0.6, 1.3 + i * 0.6))
    ap = prog(t, d * 0.5, d * 0.6)
    pulse = 1 + 0.05 * math.sin(T * 6)
    c.save()
    c.translate(W / 2, 660)
    c.scale(pulse, pulse)
    rgba(c, RED, ap)
    rrect(c, -230, -60, 460, 120, 60)
    c.fill()
    text(c, "SUBSCRIBE", 0, 18, 52, INK, ap)
    c.restore()
    stick(c, W / 2 - 420, 900, 1.3, arms=(0.35, -2.0), a=ap)
    snowfall(c, T, 0.3, 0.3)


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}
