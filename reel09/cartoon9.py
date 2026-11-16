import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel07'))
from engine import *
import engine
import cartoon7 as k7          # reuse stamp / speech helpers from reel 7
from cartoon7 import S, stamp, speech, RED
os.chdir(HERE)

t_of, DUR = load_timing('align.json')
fix = t_of("you'd fix"); butif = t_of('But if'); stay = t_of('You can stay')
s1 = t_of('Psychologists'); region = t_of('region')
s2 = t_of('Big pain'); mild = t_of('Mild pain')
s3 = t_of("That's why"); job = t_of('the okay job'); rel = t_of('the okay relationship'); hab = t_of('the okay habits'); last = t_of('last the')
s4 = t_of('"Fine" is'); s5 = t_of('Send this')

YOU = dict(shirt=C['yellow'], skin=C['skin2'], hairstyle=0)
OTHER = dict(shirt=C['mint'], skin=C['skin1'], hairstyle=2)
ROCK = hx('2A2140'); ROCK2 = hx('3B2F5C'); SOFA = hx('C2457E')

# ---------- pieces ----------
def cliff(c, t):
    """deep pit on the left, a comfy 'FINE' ledge on the right"""
    # ground at top
    rrect(c, 0, 520, W, 60, 0); fill(c, hx('4C3D80'))
    # pit walls
    c.move_to(0, 580); c.line_to(420, 580); c.line_to(420, 1560); c.line_to(0, 1560); c.close_path(); fill(c, ROCK)
    c.move_to(560, 580); c.line_to(W, 580); c.line_to(W, 1560); c.line_to(560, 1560); c.close_path(); fill(c, ROCK)
    rrect(c, 420, 580, 140, 980, 0); fill(c, hx('120C24'))
    # 'fine' ledge half-way on the right
    rrect(c, 560, 1000, 520, 70, 20); fill(c, ROCK2)

def sofa(c, x, y, s=1.0, webs=0.0):
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -170, -150, 340, 110, 40); fill(c, SOFA)
    rrect(c, -190, -70, 380, 90, 30); fill(c, hx('A33568'))
    rrect(c, -210, -120, 60, 150, 30); fill(c, SOFA); rrect(c, 150, -120, 60, 150, 30); fill(c, SOFA)
    line(c, -170, 20, -170, 50, 14, C['ink']); line(c, 170, 20, 170, 50, 14, C['ink'])
    if webs > 0: cobweb(c, 150, -150, 110 * webs)
    c.restore()

def cobweb(c, x, y, r):
    if r <= 2: return
    c.save(); c.translate(x, y); c.set_line_width(3); c.set_source_rgba(1, 1, 1, 0.7)
    for k in range(6):
        a = math.pi / 2 + k * math.pi / 10
        c.move_to(0, 0); c.line_to(math.cos(a) * r, math.sin(a) * r); c.stroke()
    for ring in (0.35, 0.65, 0.95):
        c.new_path()
        for k in range(6):
            a = math.pi / 2 + k * math.pi / 10
            (c.move_to if k == 0 else c.line_to)(math.cos(a) * r * ring, math.sin(a) * r * ring)
        c.stroke()
    c.restore()

def ladder(c, x, y0, y1):
    line(c, x - 40, y0, x - 40, y1, 12, hx('C08A55')); line(c, x + 40, y0, x + 40, y1, 12, hx('C08A55'))
    yy = y0
    while yy > y1: line(c, x - 40, yy, x + 40, yy, 10, hx('C08A55')); yy -= 70

def sign(c, x, y, s, txt, col, tcol=C['ink'], size=40):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    line(c, 0, 0, 0, 110, 12, hx('8A5A3C'))
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = c.text_extents(txt).width + 50
    rrect(c, -w / 2, -40, w, 80, 14); fill(c, col); text_c(c, txt, 0, 0, size, tcol)
    c.restore()

# ---------- scenes ----------
def scene0(c, t):
    bg(c, 5, t); cliff(c, t)
    title_pill(c, t, 0, None, 'ROCK BOTTOM vs "FINE"', RED)
    # rock bottom guy: hits the bottom, then climbs out fast
    fall = eo(t / 0.6)
    climb = eio((t - fix) / 1.6) if t > fix else 0
    ladder(c, 300, 1560, 600) if t > fix - 0.2 else None
    y = lerp(lerp(700, 1560, fall), 590, climb)
    person(c, 200 if climb == 0 else 300, y, 0.45, t=t, face='worried' if climb < 1 else 'big',
           armL=-2.6 if 0 < climb < 1 else 0.15, armR=2.6 if 0 < climb < 1 else -0.15, **OTHER)
    sign(c, 140, 1390, pop(t, 0.5), 'ROCK BOTTOM', RED, C['white'], 30)
    if t > fix + 1.6: stamp(c, 150, 430, pop(t, fix + 1.6), 'OUT!', C['mint'], C['ink'], 44)
    # you: comfy on the 'fine' ledge
    sofa(c, 830, 1000, 0.75, webs=clamp((t - stay) / 2))
    person(c, 830, 1000, 0.45, t=t, face='flat', look=0, **YOU)
    sign(c, 980, 880, pop(t, butif), 'FINE', C['yellow'], C['ink'], 40)
    if t > stay:
        stamp(c, 800, 640, pop(t, stay + 0.2), 'YEARS LATER...', C['white'], C['ink'], 36, 0.06)

def scene1(c, t):
    lt = t - s1
    bg(c, 1, t)
    title_pill(c, lt, 0, None, 'REGION-BETA PARADOX', C['yellow'])
    # chart: bars of 'how long you stay' vs pain level
    x0, y0 = 170, 1350
    line(c, x0, y0, x0 + 760, y0, 8, C['white']); line(c, x0, y0, x0, y0 - 720, 8, C['white'])
    text_c(c, 'HOW LONG YOU STAY', x0 + 380, 470, 40, C['white'])
    bars = [('MILD', 650, C['yellow']), ('MEDIUM', 360, C['coral']), ('SEVERE', 160, RED)]
    for k, (lab, h, col) in enumerate(bars):
        g = eo((t - s1 - 0.4 - k * 0.25) / 0.7)
        bx = x0 + 70 + k * 240
        rrect(c, bx, y0 - h * g, 160, max(h * g, 1), 16); fill(c, col)
        text_c(c, lab, bx + 80, y0 + 50, 34, C['white'])
    if t > region + 1.0:
        c.save(); c.translate(x0 + 150, y0 - 700); S(c, pop(t, region + 1.0)); star(c, 0, 0, 40, C['white'], 1, t); c.restore()
    text_c(c, 'PAIN →', x0 + 380, y0 + 110, 34, C['white'], True, 0.8)

def scene2(c, t):
    lt = t - s2
    big = t < mild
    bg(c, 7 if big else 3, t)  # red alarm vs calm teal
    title_pill(c, lt, 0, None, 'BIG PAIN = ACTION' if big else 'MILD PAIN = IGNORE', RED if big else C['mint'])
    if big:
        person(c, W / 2, 1450, 0.8, t=t, face='o', sweat=clamp(lt / 0.8), armL=-2.6, armR=2.6, **YOU)
        for k in range(10):
            a = k * math.pi / 5 + t * 2
            line(c, W / 2 + math.cos(a) * 320, 900 + math.sin(a) * 320, W / 2 + math.cos(a) * 420, 900 + math.sin(a) * 420, 14, C['yellow'])
        stamp(c, W / 2, 560, pop(t, s2 + 0.2), 'FIX IT NOW!', C['white'], RED, 58)
    else:
        sofa(c, W / 2, 1450, 1.3, webs=0)
        person(c, W / 2, 1440, 0.75, t=t, face='flat', **YOU)
        # tiny ache, shrugged off
        s = pop(t, mild + 0.3)
        if s > 0:
            c.save(); c.translate(720, 960); S(c, s * 1.5)
            circle(c, 0, 0, 60, C['coral']); text_c(c, 'ow', 0, 0, 44, C['white']); c.restore()
        stamp(c, W / 2, 560, pop(t, mild + 0.6), '"IT\'S FINE."', C['white'], C['ink'], 58)

def scene3(c, t):
    lt = t - s3
    bg(c, 5, t)
    title_pill(c, lt, 0, None, 'THE "OKAY" TRAP', C['coral'])
    cards = [(job, 'OKAY JOB', C['sky']), (rel, 'OKAY RELATIONSHIP', C['pink']), (hab, 'OKAY HABITS', C['mint'])]
    for k, (t0, lab, col) in enumerate(cards):
        s = pop(t, t0, 0.35)
        if s <= 0: continue
        y = 560 + k * 230
        c.save(); c.translate(W / 2, y); S(c, s); c.rotate((-1) ** k * 0.03)
        rrect(c, -380, -90, 760, 180, 30); fill(c, col)
        text_c(c, lab, 0, 0, 56, C['ink'])
        cobweb(c, 380, -90, 90 * clamp((t - t0 - 0.4) / 1.5))
        c.restore()
    # calendar flipping years
    if t > last:
        yr = 2026 + int(clamp((t - last) / 1.0) * 5)
        s = pop(t, last)
        c.save(); c.translate(W / 2, 1300); S(c, s)
        rrect(c, -170, -120, 340, 240, 24); fill(c, C['white'])
        rrect(c, -170, -120, 340, 70, 24); fill(c, RED)
        text_c(c, 'STILL HERE', 0, -85, 30, C['white'])
        text_c(c, str(yr), 0, 30, 90, C['ink']); c.restore()

def scene4(c, t):
    lt = t - s4
    bg(c, 3, t)
    title_pill(c, lt, 0, None, '"FINE" ≠ STAY', C['yellow'])
    # stairs up and out
    for k in range(6):
        rrect(c, 120 + k * 150, 1500 - k * 130, 150, 130 + k * 130, 0); fill(c, hx('2E6B62'))
    sofa(c, 200, 1500, 0.8, webs=1.0)
    stamp(c, W / 2, 560, pop(t, s4 + 0.3), 'GET UP.', C['white'], C['ink'], 64, -0.04)
    k = clamp(lt / 1.8)
    step = min(5, int(k * 6))
    hop = abs(math.sin(k * 6 * math.pi)) * 30
    px = 195 + step * 150 if lt > 0.3 else 200; py = (1500 - step * 130 if lt > 0.3 else 1500) - hop
    person(c, px, py, 0.5, t=t, face='big' if lt > 0.3 else 'flat', armL=-2.6 if lt > 1.8 else 0.15, armR=2.6 if lt > 1.8 else -0.15, **YOU)
    if lt > 1.8:
        for j in range(6):
            a = j * math.pi / 3 + t
            star(c, 945 + math.cos(a) * 140, 700 + math.sin(a) * 100, 22, C['yellow'], 0.9, t * 3)

def phone9(c, x, y, s, t, sent):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -400, 460, 800, 60); fill(c, C['ink'])
    rrect(c, -205, -370, 410, 740, 40); fill(c, hx('F2F2F7'))
    text_c(c, 'Share to', 0, -310, 40, C['ink'])
    for k, (col, nm) in enumerate([(C['coral'], 'that friend'), (C['mint'], 'bestie'), (C['sky'], 'brother')]):
        yy = -190 + k * 150
        circle(c, -140, yy, 46, col); text_c(c, nm, 0, yy, 30, C['ink'], bold=False)
        if k == 0:
            bx = 140
            rrect(c, bx - 60, yy - 32, 120, 64, 32); fill(c, (0.85, 0.85, 0.9) if sent else hx('0095F6'))
            text_c(c, 'Sent' if sent else 'Send', bx, yy, 30, C['ink'] if sent else C['white'])
    c.restore()

def scene5(c, t):
    lt = t - s5
    bg(c, 0, t)
    title_pill(c, lt, 0, None, 'SEND THIS TO...', C['coral'])
    s = pop(t, s5 + 0.1)
    if s > 0:
        c.save(); c.translate(290, 900); S(c, s)
        circle(c, 0, 0, 210, hx('2B1E6B'))
        c.save(); c.arc(0, 0, 202, 0, 2 * math.pi); c.clip()
        sofa(c, 0, 170, 0.8, webs=1.0); person(c, 0, 165, 0.42, t=t, face='flat', **OTHER)
        c.restore(); c.restore()
        text_c(c, 'stuck at "fine"', 290, 1160, 40, C['yellow'], True, clamp((lt - 0.4) / 0.3))
    sent = lt > 1.4
    phone9(c, 780, 1000, pop(t, s5 + 0.3), t, sent)
    fx = lerp(W + 200, 780 + 140, eio((lt - 0.7) / 0.5)); fy = lerp(1500, 1000 - 190 + 40, eio((lt - 0.7) / 0.5))
    bk = eio((lt - 1.7) / 0.4); fx = lerp(fx, W + 250, bk); fy = lerp(fy, 1700, bk)
    circle(c, fx, fy, 40, C['skin1']); line(c, fx, fy, fx + 60, fy + 240, 80, C['skin1'])
    if lt > 1.7:
        stamp(c, 290, 1300, pop(t, s5 + 1.7), 'Follow @neuronbites', C['sky'], C['white'], 34, 0.0)

SC = [scene0, scene1, scene2, scene3, scene4, scene5]
SCENES = [0, s1, s2, s3, s4, s5, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
