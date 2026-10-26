"""Stickman scenes for sea mysteries (Mary Celeste): ocean, a two-masted brigantine, lifeboat, hold, court."""
import math, random
import cairo
from scenes import W, H, INK, DIM, RED, AMBER, clamp, ease, prog, rgba, text, text_w, rrect, line, vignette, check, xmark
from farm_scenes import stick, child, label, panel, glow, lantern, dust, _HIDE_LABELS, STARS

BG1, BG2 = (0.03, 0.05, 0.09), (0.10, 0.14, 0.22)
WOOD = (0.22, 0.15, 0.10)
DARKWOOD = (0.13, 0.09, 0.06)
SAIL = (0.86, 0.83, 0.74)
SEA_DAY = ((0.16, 0.27, 0.36), (0.05, 0.10, 0.16))
SEA_NIGHT = ((0.06, 0.10, 0.16), (0.01, 0.03, 0.06))
GREY_SKY = ((0.32, 0.37, 0.44), (0.62, 0.64, 0.66))
CYAN = (0.3, 0.93, 1.0)


# ---------- environment ----------

def sky(c, top, bot, stars=False, T=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    if stars:
        for sx, sy, r, ph in STARS:
            rgba(c, INK, 0.2 + 0.3 * (0.5 + 0.5 * math.sin(T * 1.1 + ph)))
            c.arc(sx, sy, r, 0, 2 * math.pi)
            c.fill()


def clouds(c, T, col=(0.75, 0.78, 0.82), a=0.25, y0=120):
    for k in range(5):
        x = (T * (10 + 4 * k) + k * 520) % (W + 900) - 450
        rgba(c, col, a)
        for j in range(4):
            c.arc(x + j * 70, y0 + k * 45 + 18 * math.sin(j + k), 60 - 8 * abs(j - 1.5), 0, 2 * math.pi)
            c.fill()


def sea_y(x, T, base, amp=14):
    return base + amp * math.sin(x * 0.012 + T * 1.3) + amp * 0.5 * math.sin(x * 0.031 - T * 1.9)


def sea(c, T, base=700, pal=SEA_DAY, amp=14, layers=4):
    for L in range(layers):
        y0 = base + L * (H - base) / layers * 0.8
        f = L / max(1, layers - 1)
        col = tuple(pal[0][i] * (1 - f) + pal[1][i] * f for i in range(3))
        c.move_to(-50, H + 50)
        for x in range(-50, W + 60, 20):
            c.line_to(x, sea_y(x + L * 140, T + L * 0.7, y0, amp * (1 + 0.4 * L)))
        c.line_to(W + 50, H + 50)
        c.close_path()
        rgba(c, col)
        c.fill()
        # foam crests
        for x in range(-50, W + 60, 90):
            y = sea_y(x + L * 140, T + L * 0.7, y0, amp * (1 + 0.4 * L))
            rgba(c, (0.85, 0.9, 0.95), 0.12 + 0.08 * L)
            c.arc(x + 30 * math.sin(T + x), y + 2, 3 + L, 0, 2 * math.pi)
            c.fill()


def ship(c, x, y, s=1.0, T=0.0, torn=0.0, rock=1.0, lit=0.0, crew=()):
    """Two-masted brigantine; (x, y) is the waterline centre. torn 0..1 shreds the square sails."""
    c.save()
    c.translate(x, y + 6 * math.sin(T * 1.1) * rock)
    c.rotate(0.035 * math.sin(T * 0.9) * rock)
    c.scale(s, s)
    # hull
    c.move_to(-260, -70)
    c.line_to(250, -70)
    c.curve_to(300, -70, 320, -95, 330, -110)
    c.line_to(310, -40)
    c.curve_to(240, 30, -200, 30, -250, 0)
    c.close_path()
    rgba(c, DARKWOOD)
    c.fill()
    line(c, -255, -62, 300, -62, 6, (0.35, 0.25, 0.16))
    line(c, -240, -30, 270, -30, 3, (0.30, 0.20, 0.12))
    # bowsprit
    line(c, 300, -95, 430, -150, 6, WOOD)
    # masts
    for mx, mh in ((110, 420), (-120, 400)):
        line(c, mx, -70, mx, -70 - mh, 9, WOOD)
    # square sails on the foremast (three yards)
    for k, (yy, wdt) in enumerate(((-150, 170), (-250, 150), (-345, 120))):
        line(c, 110 - wdt / 2 - 10, yy - 40, 110 + wdt / 2 + 10, yy - 40, 5, WOOD)
        rip = torn * (0.4 + 0.3 * k)
        c.move_to(110 - wdt / 2, yy - 40)
        c.line_to(110 + wdt / 2, yy - 40)
        c.curve_to(110 + wdt / 2 + 12, yy - 10, 110 + wdt / 2 + 6, yy + 20, 110 + wdt / 2 * (1 - rip), yy + 30)
        for j in range(5):  # ragged lower edge when torn
            xx = 110 + wdt / 2 * (1 - rip) - (wdt * (1 - rip)) * (j + 1) / 5
            c.line_to(xx, yy + 30 - (18 * rip if j % 2 else 0) + 4 * math.sin(T * 3 + j))
        c.curve_to(110 - wdt / 2 - 4, yy + 20, 110 - wdt / 2 - 10, yy - 10, 110 - wdt / 2, yy - 40)
        c.close_path()
        rgba(c, SAIL, 0.95)
        c.fill()
    # fore-and-aft mainsail
    c.move_to(-120, -110)
    c.line_to(-120, -440)
    c.curve_to(-170 + 10 * math.sin(T * 2), -330, -230, -200, -270, -110)
    c.close_path()
    rgba(c, SAIL, 0.9 * (1 - 0.6 * torn))
    c.fill()
    line(c, -120, -110, -290, -105, 5, WOOD)
    # jib
    c.move_to(110, -400)
    c.line_to(420, -150)
    c.line_to(170, -110)
    c.close_path()
    rgba(c, SAIL, 0.85)
    c.fill()
    # rigging
    for (x0, y0), (x1, y1) in (((110, -490), (430, -150)), ((110, -490), (-250, -70)), ((-120, -470), (-260, -70)),
                               ((-120, -470), (110, -470))):
        line(c, x0, y0, x1, y1, 1.5, (0.1, 0.08, 0.06), 0.8)
    # deck house with a window
    rgba(c, WOOD)
    c.rectangle(-60, -110, 110, 40)
    c.fill()
    rgba(c, (1, 0.75, 0.35) if lit else (0.05, 0.05, 0.06), 0.9 if lit else 1)
    c.rectangle(-30, -100, 30, 18)
    c.fill()
    if lit:
        glow(c, -15, -92, 70, AMBER, lit)
    for cx_, kw in crew:
        stick(c, cx_, -70, 0.55, **kw)
    c.restore()


def lifeboat(c, x, y, s=1.0, T=0.0, people=0):
    c.save()
    c.translate(x, y + 5 * math.sin(T * 1.6))
    c.rotate(0.06 * math.sin(T * 1.3))
    c.scale(s, s)
    for i in range(people):
        stick(c, -70 + i * (140 / max(1, people - 1)), -18, 0.45, col=INK if i else (1.0, 0.66, 0.22))
    c.move_to(-110, -20)
    c.line_to(110, -20)
    c.curve_to(100, 20, -100, 20, -110, -20)
    c.close_path()
    rgba(c, (0.45, 0.30, 0.18))
    c.fill()
    line(c, -110, -20, 110, -20, 5, (0.25, 0.16, 0.1))
    c.restore()


def barrel(c, x, y, s=1.0, empty=False, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.move_to(-30, -45)
    c.curve_to(-42, -15, -42, 15, -30, 45)
    c.line_to(30, 45)
    c.curve_to(42, 15, 42, -15, 30, -45)
    c.close_path()
    rgba(c, (0.55, 0.30, 0.18) if not empty else (0.35, 0.22, 0.15), a)
    c.fill()
    for yy in (-30, 30):
        line(c, -36, yy, 36, yy, 5, (0.2, 0.2, 0.22), a)
    c.restore()


def hold(c, T):
    rgba(c, (0.07, 0.05, 0.04))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(-2, 16):
        x = i * 150
        line(c, x, 0, x + 60, H, 12, (0.11, 0.08, 0.06))
    for k in range(4):
        line(c, -100, 140 + k * 260, W + 100, 140 + k * 260, 10, (0.10, 0.07, 0.05))


def cabin_bg(c):
    rgba(c, (0.17, 0.12, 0.09))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(-2, 26):
        line(c, i * 80, 0, i * 80, 820, 3, (0.12, 0.08, 0.06))
    rgba(c, (0.10, 0.07, 0.05))
    c.rectangle(-400, 820, W + 800, 600)
    c.fill()
    # porthole
    rgba(c, (0.25, 0.22, 0.18))
    c.arc(1600, 330, 90, 0, 2 * math.pi)
    c.fill()
    rgba(c, (0.35, 0.5, 0.6))
    c.arc(1600, 330, 70, 0, 2 * math.pi)
    c.fill()


# ---------- scenes ----------

def sc_open_sea(c, t, d, T, a):
    found = a.get("found")
    sky(c, *GREY_SKY)
    clouds(c, T, a=0.3)
    sea(c, T, 640, amp=16)
    sx = 1350 - 60 * t / d
    ship(c, sx, 700, 0.75, T, torn=0.7, rock=1.4)
    if found:
        # the Dei Gratia watching from the left, closer to the viewer
        ship(c, 330, 870, 0.9, T + 2, torn=0.0, crew=((0, dict(col=INK, arms=(0.35, -1.7))),))
        label(c, "Dei Gratia", 330, 470, 36, INK, prog(t, 0.4, 1.0))
        label(c, "Mary Celeste", sx, 230, 36, (1.0, 0.66, 0.22), prog(t, 0.8, 1.4))
    else:
        label(c, "Atlantic Ocean · 1872", 380, 140, 44, INK, prog(t, 0.3, 1.0))
    if t > d * 0.55:
        for k in range(3):
            text(c, "?", sx - 60 + k * 60, 300 - 12 * math.sin(T * 2 + k), 64, RED, prog(t, d * (0.55 + 0.08 * k), d * (0.62 + 0.08 * k)))


def sc_boarding(c, t, d, T, a):
    sky(c, *GREY_SKY)
    clouds(c, T, a=0.25)
    sea(c, T, 760, amp=10)
    c.save()
    c.translate(W / 2, 980)
    c.scale(1.9, 1.9)
    c.translate(-W / 2, -980)
    ship(c, W / 2 + 120, 860, 1.0, T, torn=0.7, rock=0.5)
    c.restore()
    # boarding party climbing onto the empty deck
    n = 3 if a.get("detail") else 2
    for i in range(n):
        p = prog(t, 0.3 + i * 0.5, 1.5 + i * 0.5)
        stick(c, 520 + i * 150, 820 - 10 * p, 1.2, col=INK if i else (1.0, 0.66, 0.22), phase=T * 5 + i if p < 1 else None, a=p)
    if not a.get("detail"):
        items = ["food: 6 months", "fresh water", "belongings", "crew: 0"]
        for i, s in enumerate(items):
            col = RED if i == 3 else INK
            label(c, s, 330, 160 + i * 95, 40, col, prog(t, d * (0.15 + 0.17 * i), d * (0.22 + 0.17 * i)))
    else:
        label(c, "first mate Oliver Deveau", 820, 560, 38, (1.0, 0.66, 0.22), prog(t, 0.5, 1.2))


def sc_title(c, t, d, T, a):
    sky(c, *SEA_NIGHT[::-1], stars=True, T=T)
    sea(c, T, 860, pal=SEA_NIGHT, amp=8, layers=3)
    ship(c, 1500, 870, 0.45, T, torn=0.7)
    s = 1 + 0.025 * t
    c.save()
    c.translate(W / 2, 430)
    c.scale(s, s)
    text(c, "THE MARY CELESTE", 0, 0, 120, INK, prog(t, 0, 0.6))
    text(c, "GHOST SHIP", 0, 140, 120, RED, prog(t, 0.3, 0.9))
    c.restore()
    w = 900 * prog(t, 0.6, 1.6)
    line(c, W / 2 - w / 2, 650, W / 2 + w / 2, 650, 6, RED)
    text(c, "1872  ·  Atlantic Ocean", W / 2, 720, 40, DIM, prog(t, 1.0, 1.8), bold=False)


def sc_ship_profile(c, t, d, T, a):
    sky(c, (0.55, 0.68, 0.80), (0.85, 0.85, 0.82))
    sea(c, T, 760, amp=8)
    ship(c, 900, 800, 1.2, T, rock=0.4)
    ap = prog(t, d * 0.3, d * 0.4)
    c.set_dash([14, 10])
    line(c, 900 - 300, 870, 900 + 400, 870, 4, AMBER, ap)
    c.set_dash([])
    label(c, "~31 m", 950, 950, 40, AMBER, ap)
    label(c, "built 1861 · Nova Scotia", 500, 160, 40, INK, prog(t, d * 0.45, d * 0.55))
    label(c, "first name: AMAZON", 1450, 160, 44, (1.0, 0.66, 0.22), prog(t, d * 0.55, d * 0.65))


def sc_bad_luck(c, t, d, T, a):
    sky(c, (0.10, 0.10, 0.14), (0.25, 0.25, 0.30))
    flash = 1.0 if (T % 4.3) < 0.12 else 0.0
    if flash:
        rgba(c, (1, 1, 1), 0.35)
        c.paint()
    clouds(c, T * 2, col=(0.15, 0.15, 0.18), a=0.8, y0=80)
    sea(c, T * 1.6, 700, pal=SEA_NIGHT, amp=26)
    ship(c, 960, 760, 0.8, T * 1.5, rock=2.5, torn=0.3)
    events = [("1861 · first captain dies", 0.1), ("collisions", 0.4), ("run aground in a storm", 0.6), ("1868 · renamed MARY CELESTE", 0.8)]
    for i, (s, k) in enumerate(events):
        col = (1.0, 0.66, 0.22) if i == 3 else INK
        label(c, s, 420 if i % 2 == 0 else 1500, 180 + i * 90, 38, col, prog(t, d * k, d * k + 0.6))


def sc_family(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 960, 260, T, 1.0, 1.2)
    stick(c, 760, 860, 1.4, col=(1.0, 0.66, 0.22))
    stick(c, 980, 860, 1.3, col=INK)
    child(c, 1120, 860, 1.0, INK)
    text(c, "Capt. Benjamin Briggs, 37", 760, 560, 34, (1.0, 0.66, 0.22), prog(t, 0.4, 1.0))
    text(c, "Sarah", 980, 600, 34, INK, prog(t, d * 0.45, d * 0.55))
    text(c, "Sophia, 2", 1140, 680, 32, INK, prog(t, d * 0.5, d * 0.6))
    ap = prog(t, d * 0.7, d * 0.8)
    c.save()
    c.translate(330, 520)
    c.rotate(-0.06)
    rgba(c, (0.9, 0.87, 0.78), ap)
    c.rectangle(-170, -150, 340, 300)
    c.fill()
    child(c, 0, 110, 1.0, (0.25, 0.22, 0.2), a=ap)
    text(c, "Arthur, 7 · stayed home", 0, -100, 26, (0.25, 0.2, 0.15), ap)
    c.restore()


def sc_crew(c, t, d, T, a):
    sky(c, (0.55, 0.68, 0.80), (0.85, 0.85, 0.82))
    sea(c, T, 820, amp=6)
    rgba(c, WOOD)
    c.rectangle(-400, 820, W + 800, 400)
    c.fill()
    for i in range(10):
        ap = prog(t, 0.2 + i * 0.25, 0.6 + i * 0.25)
        x = 260 + i * 155
        col = (1.0, 0.66, 0.22) if i == 0 else INK
        if i == 2:
            child(c, x, 820, 1.0, INK, a=ap)
        else:
            stick(c, x, 820, 1.15, col=col, a=ap)
    text(c, "10 people on board", W / 2, 230, 64, INK, prog(t, 2.6, 3.4))


def sc_cargo(c, t, d, T, a):
    hold(c, T)
    lantern(c, 300, 260, T, 1.0, 1.3)
    k = 0
    for row in range(4):
        for col in range(11):
            ap = prog(t, 0.2 + k * 0.03, 0.5 + k * 0.03)
            barrel(c, 300 + col * 140 + (row % 2) * 70, 900 - row * 110, 1.0, a=ap)
            k += 1
    text(c, "1,701", W / 2, 260, 150, (1.0, 0.66, 0.22), prog(t, 1.4, 2.0))
    text(c, "barrels of raw alcohol  →  Genoa", W / 2, 340, 44, INK, prog(t, 1.8, 2.4), bold=False)


def sc_map(c, t, d, T, a):
    rgba(c, (0.05, 0.10, 0.16))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(0, W, 80):
        line(c, i, 0, i, H, 1, DIM, 0.07)
    for j in range(0, H, 80):
        line(c, 0, j, W, j, 1, DIM, 0.07)
    # crude coastlines: North America (left), Europe & Africa (right)
    rgba(c, (0.20, 0.24, 0.20))
    c.move_to(-50, 100); c.line_to(260, 120); c.line_to(300, 300); c.line_to(250, 420); c.line_to(200, 600)
    c.line_to(120, 800); c.line_to(-50, 900); c.close_path(); c.fill()
    c.move_to(W + 50, 80); c.line_to(1600, 120); c.line_to(1560, 300); c.line_to(1640, 380); c.line_to(1580, 480)
    c.line_to(1620, 560); c.line_to(1540, 700); c.line_to(1560, 1000); c.line_to(W + 50, 1000); c.close_path(); c.fill()
    pts = {"New York": (300, 330), "Azores": (1130, 520), "Gibraltar": (1570, 560), "Genoa": (1790, 360)}
    for n, (x, y) in pts.items():
        rgba(c, INK)
        c.arc(x, y, 10, 0, 2 * math.pi)
        c.fill()
        text(c, n, x, y - 24, 32, INK)
    p = prog(t, 0.4, d * 0.45)
    route = [(300, 330), (720, 460), (1130, 520)]
    c.set_dash([16, 10])
    c.set_line_width(6)
    rgba(c, (1.0, 0.66, 0.22))
    c.move_to(*route[0])
    for i in range(1, len(route)):
        f = clamp(p * 2 - (i - 1))
        if f <= 0:
            break
        c.line_to(route[i - 1][0] + (route[i][0] - route[i - 1][0]) * f, route[i - 1][1] + (route[i][1] - route[i - 1][1]) * f)
    c.stroke()
    q = prog(t, d * 0.5, d * 0.9)
    rgba(c, CYAN)
    c.move_to(300, 360)
    c.line_to(300 + (1180 - 300) * q, 360 + (560 - 360) * q)
    c.stroke()
    c.set_dash([])
    label(c, "Mary Celeste · Nov 7", 560, 220, 34, (1.0, 0.66, 0.22), prog(t, 0.4, 1.0))
    label(c, "Dei Gratia · Nov 15", 640, 700, 34, CYAN, prog(t, d * 0.5, d * 0.6))


def sc_logbook(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 420, 300, T, 1.0, 1.2)
    c.save()
    c.translate(W / 2 + 60, 560)
    c.rotate(-0.03)
    rgba(c, (0.12, 0.13, 0.14))
    rrect(c, -380, -260, 760, 520, 14)
    c.fill()
    rgba(c, (0.35, 0.25, 0.15))
    c.set_line_width(14)
    rrect(c, -380, -260, 760, 520, 14)
    c.stroke()
    lines_ = ["Nov 24 ·  wind fresh", "Nov 25 ·  8 a.m.", "Santa Maria  6 mi SSW"]
    for i, s in enumerate(lines_):
        text(c, s, -320, -150 + i * 90, 40, (0.85, 0.85, 0.85), prog(t, 0.4 + i * 0.6, 0.9 + i * 0.6), align="left", bold=False, italic=True)
    ap = prog(t, d * 0.55, d * 0.65)
    text(c, "— LAST ENTRY —", 0, 180, 46, RED, ap)
    c.restore()


def sc_evidence(c, t, d, T, a):
    sky(c, *GREY_SKY)
    sea(c, T, 860, amp=8, layers=3)
    rgba(c, WOOD)
    c.rectangle(-400, 640, W + 800, 500)
    c.fill()
    for i in range(14):
        line(c, i * 150, 640, i * 150, 1100, 3, DARKWOOD)
    items = [("lifeboat: GONE", RED), ("sextant & chronometer: GONE", RED), ("~1 m of water in the hold", INK),
             ("pump: taken apart", (1.0, 0.66, 0.22)), ("hatches: open", INK)]
    for i, (s, col) in enumerate(items):
        ap = prog(t, d * (0.08 + 0.17 * i), d * (0.15 + 0.17 * i))
        panel(c, 330, 150 + i * 105, 1260, 85, ap)
        text(c, s, 400, 208 + i * 105, 42, col, ap, align="left")
    # empty davits where the lifeboat used to hang
    line(c, 1550, 640, 1550, 560, 8, DARKWOOD)
    line(c, 1550, 560, 1640, 560, 8, DARKWOOD)
    line(c, 1640, 560, 1640, 620 + 10 * math.sin(T * 2), 2, (0.8, 0.8, 0.8))


def sc_cabin(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 960, 240, T, 1.0, 1.2)
    # table, sea chest, sewing machine, toy
    rgba(c, WOOD)
    c.rectangle(600, 640, 520, 30)
    c.fill()
    line(c, 640, 670, 640, 820, 12, WOOD)
    line(c, 1080, 670, 1080, 820, 12, WOOD)
    rgba(c, (0.15, 0.15, 0.17))
    c.rectangle(660, 580, 140, 60)
    c.fill()
    rgba(c, (0.85, 0.82, 0.7))
    c.rectangle(860, 600, 120, 40)
    c.fill()
    rgba(c, (0.85, 0.3, 0.3))
    c.arc(1040, 625, 16, 0, 2 * math.pi)
    c.fill()
    rgba(c, (0.35, 0.22, 0.14))
    c.rectangle(250, 700, 230, 120)
    c.fill()
    for i, (s, x, y) in enumerate([("clothes", 360, 640), ("sewing machine", 730, 520), ("toys", 1040, 560),
                                   ("boots · pipes · sea chests", 1480, 720)]):
        label(c, s, x, y, 30, INK, prog(t, d * (0.1 + 0.12 * i), d * (0.17 + 0.12 * i)))
    label(c, "left in a hurry", W / 2, 120, 50, RED, prog(t, d * 0.75, d * 0.85))


def sc_tow(c, t, d, T, a):
    sky(c, (0.55, 0.68, 0.80), (0.88, 0.80, 0.70))
    clouds(c, T, a=0.3)
    sea(c, T, 700, amp=12)
    x = 400 + 900 * t / d
    ship(c, x, 760, 0.7, T, torn=0.2, crew=((0, dict(col=INK)), (60, dict(col=INK)), (-80, dict(col=(1.0, 0.66, 0.22)))))
    rgba(c, (0.45, 0.42, 0.38))
    c.move_to(W + 50, 700); c.line_to(1700, 690); c.line_to(1760, 560); c.line_to(1820, 600); c.line_to(W + 50, 520)
    c.close_path(); c.fill()
    label(c, "→ Gibraltar", 1700, 440, 40, INK, prog(t, 0.5, 1.2))
    label(c, "reward?", x, 300, 40, (1.0, 0.66, 0.22), prog(t, d * 0.55, d * 0.65))


def sc_court(c, t, d, T, a):
    rgba(c, (0.20, 0.15, 0.12))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    for i in range(5):  # tall windows
        x = 220 + i * 380
        g = cairo.LinearGradient(x, 0, x + 120, 600)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.25)
        g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.0)
        c.set_source(g)
        c.rectangle(x, 60, 120, 520)
        c.fill()
    rgba(c, DARKWOOD)
    c.rectangle(700, 520, 520, 300)
    c.fill()
    stick(c, 960, 520, 1.3, col=(1.0, 0.66, 0.22), arms=(0.35, -1.9 + 0.2 * math.sin(T * 3)))
    text(c, "Frederick Solly-Flood", 960, 230, 38, (1.0, 0.66, 0.22), prog(t, 0.4, 1.0))
    for i, s in enumerate(["MUTINY?", "MURDER?", "FRAUD?"]):
        label(c, s, 360 if i == 0 else (1560 if i == 1 else 960), 380 if i < 2 else 940, 48, RED, prog(t, d * (0.3 + 0.15 * i), d * (0.37 + 0.15 * i)))


def sc_sword(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 300, 250, T, 1.0, 1.2)
    c.save()
    c.translate(900, 520)
    c.rotate(-0.25)
    line(c, -420, 0, 300, 0, 18, (0.75, 0.77, 0.8))
    line(c, 300, 0, 360, 0, 18, (0.75, 0.77, 0.8))
    line(c, -440, -60, -440, 60, 16, (0.6, 0.5, 0.2))
    line(c, -560, 0, -440, 0, 20, (0.3, 0.2, 0.12))
    for k in range(4):
        rgba(c, (0.45, 0.25, 0.15))
        c.arc(-200 + k * 110, 2, 9 + 3 * (k % 2), 0, 2 * math.pi)
        c.fill()
    c.restore()
    label(c, "stains", 760, 380, 40, INK, prog(t, d * 0.15, d * 0.25))
    ap = prog(t, d * 0.4, d * 0.5)
    label(c, "NOT BLOOD", 1350, 720, 56, (0.35, 1.0, 0.5), ap)
    label(c, "no signs of a fight", 760, 900, 40, INK, prog(t, d * 0.7, d * 0.8))


def sc_reward(c, t, d, T, a):
    rgba(c, (0.08, 0.09, 0.12))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    cx_, cy_, R = 760, 560, 260
    rgba(c, (0.25, 0.28, 0.35))
    c.arc(cx_, cy_, R, 0, 2 * math.pi)
    c.fill()
    p = prog(t, 0.4, 1.6)
    c.move_to(cx_, cy_)
    c.arc(cx_, cy_, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi / 6 * p)
    c.close_path()
    rgba(c, (1.0, 0.66, 0.22))
    c.fill()
    label(c, "≈ 1/6 of the value", 1400, 470, 48, (1.0, 0.66, 0.22), prog(t, 1.4, 2.0))
    label(c, "doubts remained", 1400, 590, 40, INK, prog(t, d * 0.4, d * 0.5))
    ap = prog(t, d * 0.7, d * 0.8)
    text(c, "10 people · never found", W / 2, 1000, 50, RED, ap)


def sc_doyle(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 1250, 300, T, 1.0, 1.2)
    rgba(c, WOOD)
    c.rectangle(600, 640, 760, 30)
    c.fill()
    stick(c, 760, 860, 1.4, col=INK, arms=(0.9 + 0.15 * math.sin(T * 8), -0.2))
    rgba(c, (0.9, 0.87, 0.78))
    c.rectangle(850, 600, 220, 40)
    c.fill()
    label(c, "Arthur Conan Doyle · 1884", 760, 440, 40, (1.0, 0.66, 0.22), prog(t, 0.4, 1.0))
    ap = prog(t, d * 0.45, d * 0.55)
    c.save()
    c.translate(1520, 600)
    c.rotate(0.05)
    rgba(c, (0.88, 0.84, 0.72), ap)
    c.rectangle(-230, -200, 460, 400)
    c.fill()
    text(c, "“MARIE CELESTE”", 0, -120, 38, (0.25, 0.18, 0.12), ap)
    for k in range(5):
        line(c, -180, -60 + k * 40, 180 - (k % 2) * 60, -60 + k * 40, 4, (0.45, 0.4, 0.35), ap)
    c.restore()
    label(c, "fiction, not fact", 1520, 880, 40, RED, prog(t, d * 0.75, d * 0.85))


def sc_theories(c, t, d, T, a):
    sky(c, *SEA_NIGHT[::-1])
    sea(c, T, 760, pal=SEA_NIGHT, amp=12)
    cards = [("SEA MONSTER", 0.1), ("PIRATES", 0.25), ("WATERSPOUT", 0.4), ("SEAQUAKE", 0.55)]
    for i, (s, k) in enumerate(cards):
        ap = prog(t, d * k, d * k + 0.5)
        x = 300 + i * 440
        panel(c, x - 190, 260, 380, 300, ap)
        text(c, s, x, 440, 44, INK, ap)
        if t > d * 0.75 and i in (0, 1):
            xmark(c, x + 150, 300, 26, prog(t, d * 0.75, d * 0.8))
    # tentacle silhouette for fun
    ap = prog(t, d * 0.15, d * 0.3)
    c.set_line_width(26)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(c, (0.02, 0.04, 0.06), ap)
    c.move_to(300, 1000)
    c.curve_to(300, 850, 380 + 30 * math.sin(T * 2), 820, 330, 720 + 20 * math.sin(T * 2))
    c.stroke()


def sc_fraud(c, t, d, T, a):
    cabin_bg(c)
    lantern(c, 960, 250, T, 1.0, 1.2)
    stick(c, 700, 860, 1.4, col=(1.0, 0.66, 0.22), arms=(0.35, -1.0))
    stick(c, 1220, 860, 1.4, col=CYAN, arms=(-1.0, -0.35))
    text(c, "Briggs", 700, 560, 36, (1.0, 0.66, 0.22))
    text(c, "Morehouse", 1220, 560, 36, CYAN)
    label(c, "insurance fraud?", W / 2, 180, 52, RED, prog(t, 0.4, 1.0))
    ap = prog(t, d * 0.45, d * 0.55)
    label(c, "Briggs owned part of the ship", W / 2, 320, 38, INK, ap)
    if ap > 0:
        xmark(c, W / 2, 440, 30, prog(t, d * 0.7, d * 0.75))


def sc_barrels(c, t, d, T, a):
    hold(c, T)
    lantern(c, 1600, 260, T, 1.0, 1.2)
    k = 0
    for row in range(3):
        for col in range(10):
            empty = (row * 10 + col) in (3, 7, 12, 15, 18, 21, 24, 26, 28)
            ap = 1.0
            barrel(c, 260 + col * 150 + (row % 2) * 75, 900 - row * 120, 1.05, empty=empty and t > d * 0.3, a=ap)
            if empty and t > d * 0.3:
                text(c, "EMPTY", 260 + col * 150 + (row % 2) * 75, 905 - row * 120, 20, RED, prog(t, d * 0.3, d * 0.35))
            k += 1
    label(c, "9 empty barrels · red oak", W / 2, 200, 46, RED, prog(t, d * 0.3, d * 0.4))
    # vapor
    ap = prog(t, d * 0.65, d * 0.8)
    for i in range(18):
        x = (i * 113 + T * 20) % W
        y = 560 - ((T * 25 + i * 37) % 300)
        rgba(c, (0.55, 0.95, 1.0), 0.10 * ap)
        c.arc(x, y, 40 + (i % 3) * 15, 0, 2 * math.pi)
        c.fill()
    label(c, "alcohol vapor", W / 2, 330, 40, CYAN, ap)


def sc_flame(c, t, d, T, a):
    rgba(c, (0.05, 0.05, 0.07))
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()
    # lab model: a box with paper cubes
    rgba(c, (0.6, 0.7, 0.8), 0.25)
    c.rectangle(560, 380, 800, 400)
    c.fill()
    c.set_line_width(5)
    rgba(c, (0.7, 0.8, 0.9))
    c.rectangle(560, 380, 800, 400)
    c.stroke()
    for i in range(6):
        rgba(c, (0.9, 0.88, 0.8))
        c.rectangle(620 + i * 125, 700, 70, 70)
        c.fill()
    burst = prog(t, d * 0.35, d * 0.45) * (1 - prog(t, d * 0.55, d * 0.7))
    if burst > 0:
        g = cairo.LinearGradient(560, 0, 1360, 0)
        g.add_color_stop_rgba(0, 0.2, 0.5, 1.0, 0.0)
        g.add_color_stop_rgba(0.5, 0.35, 0.65, 1.0, 0.8 * burst)
        g.add_color_stop_rgba(1, 0.2, 0.5, 1.0, 0.0)
        c.set_source(g)
        c.rectangle(560, 380, 800, 300)
        c.fill()
        glow(c, 960, 530, 520, (0.3, 0.6, 1.0), burst)
    stick(c, 300, 900, 1.3, col=INK, arms=(0.35, -1.2))
    label(c, "Andrea Sella · UCL · 2006", 360, 220, 38, INK, prog(t, 0.4, 1.0))
    label(c, "nothing burned", 1600, 760, 44, (0.35, 1.0, 0.5), prog(t, d * 0.7, d * 0.8))


def sc_pump(c, t, d, T, a):
    hold(c, T)
    water = 0.4 + 0.25 * prog(t, 0, d)
    rgba(c, (0.15, 0.3, 0.45), 0.7)
    c.rectangle(-400, H * (1 - water * 0.6), W + 800, H)
    c.fill()
    # dismantled pump parts
    line(c, 760, 620, 760, 300, 26, (0.45, 0.45, 0.48))
    for k, (x, y, r) in enumerate(((900, 450, 0.6), (1000, 380, -0.4), (1080, 500, 1.1))):
        c.save(); c.translate(x, y); c.rotate(r + 0.05 * math.sin(T + k))
        rgba(c, (0.55, 0.55, 0.58)); c.rectangle(-50, -12, 100, 24); c.fill(); c.restore()
    label(c, "coal dust?", 1450, 300, 44, INK, prog(t, d * 0.2, d * 0.3))
    ap = prog(t, d * 0.45, d * 0.55)
    # chronometer
    c.save()
    c.translate(1450, 600)
    rgba(c, (0.85, 0.75, 0.4), ap)
    c.arc(0, 0, 90, 0, 2 * math.pi)
    c.fill()
    rgba(c, (0.95, 0.95, 0.9), ap)
    c.arc(0, 0, 72, 0, 2 * math.pi)
    c.fill()
    c.rotate(T * 3)
    line(c, 0, 0, 0, -60, 6, (0.1, 0.1, 0.1), ap)
    c.restore()
    label(c, "chronometer wrong?", 1450, 760, 40, RED, ap)


def sc_lifeboat(c, t, d, T, a):
    sky(c, *GREY_SKY)
    clouds(c, T, a=0.3)
    sea(c, T, 600, amp=16)
    gone = prog(t, d * 0.35, d)
    sx = 900 + 900 * gone
    ship(c, sx, 680, 0.7 * (1 - 0.4 * gone), T, torn=0.5)
    # rope snapping
    if t < d * 0.35:
        c.set_line_width(3)
        rgba(c, (0.85, 0.8, 0.7))
        c.move_to(760, 820)
        c.curve_to(800, 860, 820, 760, sx - 200, 700)
        c.stroke()
    lifeboat(c, 640, 860, 1.3, T, people=6)
    label(c, "the rope snaps?", 640, 520, 40, RED, prog(t, d * 0.3, d * 0.4))


def sc_wreck(c, t, d, T, a):
    sky(c, (0.30, 0.55, 0.75), (0.95, 0.80, 0.60))
    sea(c, T, 700, pal=((0.10, 0.45, 0.55), (0.03, 0.2, 0.3)), amp=10)
    rgba(c, (0.65, 0.55, 0.35))
    c.move_to(-50, 900); c.curve_to(300, 860, 700, 920, 1100, 880); c.line_to(1100, 1200); c.line_to(-50, 1200); c.close_path(); c.fill()
    sink = prog(t, d * 0.3, d * 0.9)
    c.save()
    c.translate(0, 120 * sink)
    ship(c, 1150, 760, 0.8, T, torn=0.9, rock=0.3)
    c.restore()
    label(c, "1885 · reef near Haiti", 500, 200, 44, INK, prog(t, 0.4, 1.0))
    label(c, "insurance fraud", 1450, 300, 44, RED, prog(t, d * 0.45, d * 0.55))


def sc_unsolved(c, t, d, T, a):
    sky(c, *SEA_NIGHT[::-1])
    rows = ["Why leave a ship that could float?", "Where did ten people go?", "Why take only the lifeboat?",
            "What really happened?"]
    for i, s in enumerate(rows):
        ap = prog(t, 0.3 + i * d * 0.15, 0.8 + i * d * 0.15)
        y = 280 + i * 160
        panel(c, 360, y - 70, 1200, 110, ap)
        text(c, "?", 440, y + 5, 70, RED, ap)
        text(c, s, 510, y, 46, INK, ap, align="left")


def sc_outro(c, t, d, T, a):
    sky(c, *SEA_NIGHT[::-1], stars=True, T=T)
    sea(c, T, 820, pal=SEA_NIGHT, amp=8, layers=3)
    ship(c, 1550, 840, 0.4, T, torn=0.7)
    text(c, "What do you think happened?", W / 2, 230, 74, INK, prog(t, 0, 0.5))
    for i, (s, col) in enumerate([("Alcohol vapor", CYAN), ("Broken pump", (1.0, 0.66, 0.22)), ("Something else", RED)]):
        label(c, s, 480 + i * 480, 390, 40, col, prog(t, 0.8 + i * 0.6, 1.3 + i * 0.6))
    ap = prog(t, d * 0.5, d * 0.6)
    pulse = 1 + 0.05 * math.sin(T * 6)
    c.save()
    c.translate(W / 2, 620)
    c.scale(pulse, pulse)
    rgba(c, RED, ap)
    rrect(c, -230, -60, 460, 120, 60)
    c.fill()
    text(c, "SUBSCRIBE", 0, 18, 52, INK, ap)
    c.restore()


def _scene(fn):
    def run(c, t, d, T, a):
        _HIDE_LABELS[0] = "vx" in a
        fn(c, t, d, T, a)
    return run


SCENES = {k[3:]: _scene(v) for k, v in globals().items() if k.startswith("sc_")}
