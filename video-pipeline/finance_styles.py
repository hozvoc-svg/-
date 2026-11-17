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


# ---------- 6. Blueprint / technical schematic ----------
def style_blueprint(c):
    rgba(c, (0.07, 0.22, 0.45)); c.paint()
    for i in range(0, W, 40):
        line(c, i, 0, i, H, 1 if i % 200 else 2, (0.6, 0.8, 1.0), 0.12 if i % 200 else 0.25)
    for j in range(0, H, 40):
        line(c, 0, j, W, j, 1 if j % 200 else 2, (0.6, 0.8, 1.0), 0.12 if j % 200 else 0.25)
    wh = (0.9, 0.95, 1.0)
    for k, (lab, x) in enumerate((("BUY", 380), ("BORROW", 960), ("DIE", 1540))):
        c.set_line_width(4); rgba(c, wh); rrect(c, x - 200, 420, 400, 240, 8); c.stroke()
        bold(c, f"STEP {k + 1}", x, 480, 34, (0.6, 0.85, 1.0), family="Inter")
        bold(c, lab, x, 590, 90 if len(lab) < 5 else 70, wh)
        if k < 2:
            line(c, x + 210, 540, x + 370, 540, 4, wh); c.move_to(x + 370, 540); c.line_to(x + 345, 525); c.line_to(x + 345, 555); c.close_path(); rgba(c, wh); c.fill()
    c.set_dash([12, 8]); line(c, 180, 760, 1740, 760, 2, wh, 0.7); c.set_dash([])
    text(c, "FIG. 1 — THE BILLIONAIRE TAX PLAYBOOK", 180, 820, 34, wh, align="left", bold=False)
    bold(c, "TAX PAID: ~0", W / 2, 260, 90, (1.0, 0.85, 0.4))


# ---------- 7. Chalkboard ----------
def style_chalk(c):
    rgba(c, (0.12, 0.20, 0.17)); c.paint()
    r = random.Random(5)
    for k in range(5000):
        rgba(c, (1, 1, 1), r.uniform(0.01, 0.04)); c.rectangle(r.uniform(0, W), r.uniform(0, H), 3, 1); c.fill()
    ch = (0.94, 0.94, 0.90)
    bold(c, "Salary  =  taxed up to 37%", 200, 330, 90, ch, family="Caveat", align="left")
    bold(c, "Stock growth  =  taxed 0%", 200, 500, 90, (1.0, 0.85, 0.45), family="Caveat", align="left")
    bold(c, "(until you sell)", 260, 590, 60, ch, family="Caveat", align="left")
    c.set_line_width(6); rgba(c, (1.0, 0.55, 0.55)); c.arc(1500, 470, 170, 0, 2 * math.pi); c.stroke()
    bold(c, "?!", 1500, 520, 150, (1.0, 0.55, 0.55), family="Caveat")
    rgba(c, (0.35, 0.25, 0.18)); c.rectangle(0, 1010, W, 70); c.fill()


# ---------- 8. Modern dashboard / glass UI ----------
def style_dashboard(c):
    g = cairo.LinearGradient(0, 0, W, H); g.add_color_stop_rgb(0, 0.10, 0.08, 0.22); g.add_color_stop_rgb(1, 0.02, 0.10, 0.18)
    c.set_source(g); c.paint()
    F.glow(c, 400, 250, 500, (0.6, 0.3, 1.0), 0.35); F.glow(c, 1500, 850, 500, (0.1, 0.8, 0.9), 0.3)

    def card(x, y, w, h):
        rgba(c, (1, 1, 1), 0.08); rrect(c, x, y, w, h, 28); c.fill()
        c.set_line_width(2); rgba(c, (1, 1, 1), 0.2); rrect(c, x, y, w, h, 28); c.stroke()
    card(140, 160, 760, 760); card(980, 160, 800, 360); card(980, 560, 800, 360)
    text(c, "Net worth", 200, 240, 38, (0.75, 0.75, 0.85), align="left", bold=False)
    bold(c, "$182.4B", 200, 340, 100, (1, 1, 1), align="left")
    pts = [(200, 820), (300, 780), (400, 800), (500, 690), (600, 640), (700, 560), (840, 430)]
    c.set_line_width(8); rgba(c, (0.35, 1.0, 0.65)); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke()
    text(c, "Taxable income", 1040, 240, 38, (0.75, 0.75, 0.85), align="left", bold=False)
    bold(c, "$0", 1040, 370, 120, (1.0, 0.45, 0.5), align="left")
    text(c, "Loans against stock", 1040, 640, 38, (0.75, 0.75, 0.85), align="left", bold=False)
    bold(c, "$2.1B", 1040, 770, 110, (0.4, 0.85, 1.0), align="left")


# ---------- 9. Retro pixel art ----------
def style_pixel(c):
    rgba(c, (0.12, 0.10, 0.25)); c.paint()
    px = 20
    r = random.Random(2)
    for k in range(120):
        rgba(c, (1, 1, 1), 0.7); c.rectangle(r.randrange(0, W, px), r.randrange(0, 600, px), px // 2, px // 2); c.fill()
    rgba(c, (0.20, 0.55, 0.30)); c.rectangle(0, 820, W, 260); c.fill()
    for x in range(0, W, px * 2):
        rgba(c, (0.15, 0.45, 0.25)); c.rectangle(x, 820, px, px); c.fill()
    for k in range(10):  # pixel coin pile
        for j in range(10 - k):
            rgba(c, (1.0, 0.82, 0.2) if (j + k) % 2 else (0.95, 0.65, 0.1)); c.rectangle(1300 + j * 40 + k * 20, 800 - k * 40, 40, 40); c.fill()
    rgba(c, (0.95, 0.85, 0.7)); c.rectangle(500, 600, 80, 80); c.fill()
    rgba(c, (0.2, 0.4, 0.9)); c.rectangle(480, 680, 120, 140); c.fill()
    bold(c, "TAX: 37%", 540, 560, 64, (1.0, 0.4, 0.4), family="Audiowide")
    bold(c, "TAX: 3.4%", 1500, 340, 64, (0.4, 1.0, 0.5), family="Audiowide")
    bold(c, "LEVEL 1: THE RICH", W / 2, 150, 80, (1.0, 0.9, 0.3), family="Audiowide")


# ---------- 10. Paper cut-out collage ----------
def style_cutout(c):
    rgba(c, (0.93, 0.89, 0.80)); c.paint()

    def paper(x, y, w, h, colr, rot):
        c.save(); c.translate(x, y); c.rotate(rot)
        rgba(c, (0, 0, 0), 0.25); c.rectangle(-w / 2 + 10, -h / 2 + 12, w, h); c.fill()
        rgba(c, colr); c.rectangle(-w / 2, -h / 2, w, h); c.fill(); c.restore()
    paper(520, 520, 700, 520, (0.85, 0.30, 0.25), -0.05)
    paper(1350, 560, 760, 560, (0.20, 0.45, 0.55), 0.04)
    paper(960, 200, 1100, 150, (0.98, 0.96, 0.90), -0.01)
    bold(c, "TWO TAX SYSTEMS", 960, 235, 90, (0.12, 0.12, 0.14), family="Anton")
    bold(c, "WORKERS", 520, 470, 90, (0.98, 0.96, 0.90), family="Anton")
    bold(c, "PAY ON EVERY CHECK", 520, 580, 52, (0.98, 0.96, 0.90), family="Anton")
    bold(c, "BILLIONAIRES", 1350, 510, 90, (0.98, 0.96, 0.90), family="Anton")
    bold(c, "PAY WHEN THEY CHOOSE", 1350, 620, 52, (0.98, 0.96, 0.90), family="Anton")
    for k in range(6):  # torn tape pieces
        x = [250, 790, 1000, 1700, 640, 1260][k]; y = [270, 270, 290, 300, 790, 850][k]
        paper(x, y, 140, 40, (0.95, 0.92, 0.70), 0.3 * (1 if k % 2 else -1))


STYLES += [("6_blueprint", style_blueprint), ("7_chalkboard", style_chalk), ("8_glass_dashboard", style_dashboard),
           ("9_pixel_art", style_pixel), ("10_paper_cutout", style_cutout)]
