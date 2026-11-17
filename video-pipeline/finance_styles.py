"""One sample frame per visual style for the finance channel, all on the same story beat:
'The richest Americans paid a true tax rate of 3.4%' (ProPublica, 2021)."""
import math, os, random, sys
import cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import text, rrect, line, rgba
import farm_scenes as F

W, H = 1920, 1080
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "finance_styles")


def bold(c, s, x, y, size, col, a=1.0, family="Inter Display Black", align="center", outline=0.0, ocol=(0, 0, 0)):
    c.select_font_face(family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    w = c.text_extents(s).x_advance
    x0 = {"center": x - w / 2, "left": x, "right": x - w}[align]
    c.new_path()
    c.move_to(x0, y)
    c.text_path(s)
    if outline:
        rgba(c, ocol, a); c.set_line_width(size * outline); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgba(c, col, a)
    c.fill()
    return w


def coin_stack(c, x, y, n, r=46, col=(1.0, 0.78, 0.25)):
    for k in range(n):
        yy = y - k * 14
        c.save(); c.translate(x, yy); c.scale(1, 0.32)
        rgba(c, tuple(v * 0.7 for v in col)); c.arc(0, 8, r, 0, 2 * math.pi); c.fill()
        rgba(c, col); c.arc(0, 0, r, 0, 2 * math.pi); c.fill()
        c.restore()


# ---------- 1. Dark infographic (navy + gold, glowing stick figures) ----------
def style_dark(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.03, 0.05, 0.11); g.add_color_stop_rgb(1, 0.01, 0.02, 0.05)
    c.set_source(g); c.paint()
    for i in range(0, W, 80):
        line(c, i, 0, i, H, 1, (0.3, 0.4, 0.6), 0.06)
    for j in range(0, H, 80):
        line(c, 0, j, W, j, 1, (0.3, 0.4, 0.6), 0.06)
    # two bars
    for i, (lab, val, colr, x) in enumerate((("YOU", 0.32, (0.3, 0.75, 1.0), 640), ("BILLIONAIRES", 0.034, (1.0, 0.78, 0.25), 1280))):
        h = 520 * val / 0.32
        F.glow(c, x, 880 - h, 220, colr, 0.25)
        rgba(c, colr); rrect(c, x - 110, 880 - h, 220, h, 14); c.fill()
        bold(c, f"{val * 100:.1f}%" if val < 0.1 else "~30%", x, 860 - h - 30, 96, colr)
        bold(c, lab, x, 950, 46, (0.85, 0.88, 0.95))
    F.stick(c, 400, 880, 1.4, col=(0.3, 0.75, 1.0), head_hold=1.0)
    coin_stack(c, 1560, 880, 14)
    F.stick(c, 1560, 690, 1.3, col=(1.0, 0.78, 0.25), arms=(0.4, -2.2))
    bold(c, "TRUE TAX RATE", W / 2, 120, 70, (0.95, 0.96, 1.0))
    text(c, "Source: ProPublica, 2021", W / 2, 1040, 26, (0.5, 0.55, 0.65), bold=False)


# ---------- 2. Paper doodle / whiteboard explainer ----------
def style_paper(c):
    rgba(c, (0.96, 0.94, 0.89)); c.paint()
    r = random.Random(3)
    for k in range(4000):  # paper grain
        rgba(c, (0.6, 0.55, 0.45), r.uniform(0.02, 0.06)); c.rectangle(r.uniform(0, W), r.uniform(0, H), 2, 2); c.fill()
    ink = (0.12, 0.12, 0.14)

    def wobble(x0, y0, x1, y1, w=6):
        c.set_line_width(w); rgba(c, ink); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(x0, y0)
        for k in range(1, 9):
            f = k / 8
            c.line_to(x0 + (x1 - x0) * f + r.uniform(-2, 2), y0 + (y1 - y0) * f + r.uniform(-2, 2))
        c.stroke()
    # worker
    wobble(420, 760, 420, 620); c.arc(420, 590, 32, 0, 2 * math.pi); c.set_line_width(6); c.stroke()
    wobble(420, 660, 360, 720); wobble(420, 660, 480, 700); wobble(420, 760, 380, 860); wobble(420, 760, 460, 860)
    rgba(c, (0.9, 0.25, 0.2)); rrect(c, 300, 300, 240, 160, 10); c.fill()
    bold(c, "-30%", 420, 405, 72, (1, 1, 1))
    # rich guy with top hat on money bags
    for k, (x, y) in enumerate(((1380, 820), (1500, 830), (1440, 740))):
        rgba(c, (0.55, 0.75, 0.35)); c.arc(x, y, 70, 0, 2 * math.pi); c.fill(); c.set_line_width(5); rgba(c, ink); c.arc(x, y, 70, 0, 2 * math.pi); c.stroke()
        bold(c, "$", x, y + 26, 70, ink)
    wobble(1440, 670, 1440, 540); c.arc(1440, 510, 32, 0, 2 * math.pi); c.set_line_width(6); c.stroke()
    rgba(c, ink); c.rectangle(1405, 430, 70, 50); c.fill(); c.rectangle(1390, 478, 100, 10); c.fill()
    wobble(1440, 580, 1520, 520); wobble(1440, 580, 1370, 620)
    rgba(c, (0.25, 0.65, 0.35)); rrect(c, 1330, 240, 240, 160, 10); c.fill()
    bold(c, "-3.4%", 1450, 345, 72, (1, 1, 1))
    wobble(620, 380, 1300, 330, 5)
    bold(c, "Same country. Different rules.", W / 2, 150, 72, ink, family="Caveat")
    bold(c, "WHY?", W / 2, 1000, 90, (0.9, 0.25, 0.2))


# ---------- 3. Bold kinetic typography (black / white / red) ----------
def style_kinetic(c):
    rgba(c, (0.02, 0.02, 0.02)); c.paint()
    bold(c, "THE 25 RICHEST", 160, 300, 110, (1, 1, 1), align="left")
    bold(c, "AMERICANS PAID", 160, 430, 110, (1, 1, 1), align="left")
    bold(c, "3.4%", 160, 790, 380, (0.95, 0.15, 0.2), align="left")
    rgba(c, (0.95, 0.15, 0.2)); c.rectangle(1280, 520, 12, 330); c.fill()
    bold(c, "TRUE TAX", 1330, 620, 80, (1, 1, 1), align="left")
    bold(c, "RATE", 1330, 710, 80, (1, 1, 1), align="left")
    text(c, "2014–2018 · ProPublica", 1335, 800, 36, (0.6, 0.6, 0.6), align="left", bold=False)


# ---------- 4. Flat vector illustration (bright, isometric-ish city) ----------
def style_flat(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.55, 0.78, 0.95); g.add_color_stop_rgb(1, 0.85, 0.93, 0.98)
    c.set_source(g); c.paint()
    rgba(c, (0.40, 0.70, 0.45)); c.rectangle(0, 820, W, 260); c.fill()
    # bank
    rgba(c, (0.95, 0.95, 0.97)); c.rectangle(1200, 420, 520, 400); c.fill()
    rgba(c, (0.85, 0.86, 0.90)); c.move_to(1170, 420); c.line_to(1460, 280); c.line_to(1750, 420); c.close_path(); c.fill()
    for k in range(5):
        rgba(c, (0.80, 0.82, 0.88)); c.rectangle(1240 + k * 100, 470, 40, 330); c.fill()
    bold(c, "BANK", 1460, 400, 56, (0.25, 0.3, 0.45))
    # skyscraper with money
    rgba(c, (0.25, 0.35, 0.55)); c.rectangle(200, 260, 260, 560); c.fill()
    for r_ in range(9):
        for k in range(4):
            rgba(c, (1.0, 0.85, 0.4) if (r_ + k) % 3 else (0.5, 0.65, 0.85)); c.rectangle(225 + k * 60, 290 + r_ * 58, 36, 36); c.fill()
    # flow of money from bank to tower
    for k in range(7):
        x = 520 + k * 95; y = 600 - 40 * math.sin(k / 6 * math.pi)
        c.save(); c.translate(x, y); c.rotate(-0.2)
        rgba(c, (0.35, 0.70, 0.40)); rrect(c, -40, -22, 80, 44, 6); c.fill()
        bold(c, "$", 0, 14, 36, (0.95, 0.98, 0.95)); c.restore()
    rgba(c, (1, 1, 1)); rrect(c, 560, 120, 800, 140, 30); c.fill()
    bold(c, "BORROW, DON'T SELL", 960, 215, 72, (0.15, 0.25, 0.45))
    text(c, "Loans are not income → no income tax", 960, 330, 40, (0.15, 0.25, 0.45))


# ---------- 5. Archive / newspaper documentary ----------
def style_archive(c):
    rgba(c, (0.12, 0.10, 0.08)); c.paint()
    c.save(); c.translate(960, 560); c.rotate(-0.03)
    rgba(c, (0, 0, 0), 0.5); c.rectangle(-600, -440, 1220, 900); c.fill()
    rgba(c, (0.90, 0.86, 0.76)); c.rectangle(-620, -460, 1220, 900); c.fill()
    bold(c, "THE DAILY LEDGER", -10, -370, 70, (0.12, 0.10, 0.08), family="DM Serif Display")
    line(c, -580, -340, 560, -340, 4, (0.12, 0.10, 0.08)); line(c, -580, -330, 560, -330, 2, (0.12, 0.10, 0.08))
    bold(c, "BILLIONAIRES PAID", -10, -220, 92, (0.12, 0.10, 0.08), family="DM Serif Display")
    bold(c, "JUST 3.4% IN TAX", -10, -110, 92, (0.65, 0.12, 0.10), family="DM Serif Display")
    r = random.Random(4)
    for col_ in range(3):
        for k in range(14):
            y = -40 + k * 30
            line(c, -560 + col_ * 380, y, -560 + col_ * 380 + r.uniform(250, 340), y, 6, (0.35, 0.32, 0.28), 0.6)
    c.restore()
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1100); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.7)
    c.set_source(g); c.paint()


STYLES = [("1_dark_infographic", style_dark), ("2_paper_doodle", style_paper), ("3_kinetic_type", style_kinetic),
          ("4_flat_vector", style_flat), ("5_archive_newspaper", style_archive)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in STYLES:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        fn(cairo.Context(s))
        s.write_to_png(os.path.join(OUT, name + ".png"))
        print(name)
