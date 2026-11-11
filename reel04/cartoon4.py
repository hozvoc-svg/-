import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *
import engine
def S(c, k): k = max(k, 1e-3); c.scale(k, k)

t_of, DUR = load_timing('align.json')
s1 = t_of('When you'); wander = t_of('So your'); s2 = t_of('Your brain'); anc = t_of('For our')
s3 = t_of('But here'); spot = t_of("It's called"); notice = t_of('People notice'); moment = t_of('That moment')
forgot = t_of('They forgot'); s4 = t_of('Follow')
engine.BG += [(hx('070B1F'), hx('1B2453')), (hx('2A1608'), hx('7A3E12')), (hx('140F2B'), hx('3B2A6B'))]
NIGHT, CAVE, STAGE = 6, 7, 8
YOU = dict(shirt=C['sky'], skin=C['skin2'], hairstyle=1)

def stars_bg(c, t):
    random.seed(4)
    for k in range(40):
        x = random.uniform(0, W); y = random.uniform(0, 900); r = random.uniform(2, 5)
        circle(c, x, y, r, C['white'], 0.4 + 0.4 * abs(math.sin(t * 2 + k)))
    circle(c, 860, 300, 90, (1, 0.95, 0.8)); circle(c, 900, 270, 80, BG_N_TOP)
BG_N_TOP = hx('0B1030')

def bedroom(c, t, eyes='open', face='worried', sweat=0.0):
    bg(c, NIGHT, t); stars_bg(c, t)
    # window frame
    c.set_line_width(14); c.set_source_rgba(1, 1, 1, 0.15); rrect(c, 640, 160, 400, 360, 20); c.stroke()
    # bed
    rrect(c, 90, 1180, 900, 220, 40); fill(c, hx('3A2F6B'))
    rrect(c, 90, 1360, 30, 160, 10); fill(c, hx('2A2250')); rrect(c, 960, 1360, 30, 160, 10); fill(c, hx('2A2250'))
    rrect(c, 120, 1080, 240, 130, 50); fill(c, C['white'])  # pillow
    # person lying: head on pillow
    c.save(); c.translate(250, 1080); c.rotate(-math.pi / 2)
    person(c, 0, 440, 0.9, t=t, face=face, look=0, sweat=sweat, **YOU)
    c.restore()
    # blanket
    rrect(c, 420, 1050, 570, 260, 60); fill(c, C['coral'])
    for k in range(3): line(c, 500 + k * 160, 1080, 540 + k * 160, 1290, 10, hx('E05656'))
    # clock
    rrect(c, 700, 1280 - 520, 0, 0, 0)
    rrect(c, 760, 640, 260, 120, 24); fill(c, C['ink'])
    blink = int(t * 2) % 2
    text_c(c, '3:00' if blink else '3 00', 860, 700, 64, hx('FF4D4D')); text_c(c, 'AM', 975, 715, 28, hx('FF4D4D'))

def thought(c, x, y, s, w, h, txt_lines, size=40):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    circle(c, -w / 2 + 30, h / 2 + 60, 16, C['white']); circle(c, -w / 2 + 6, h / 2 + 100, 10, C['white'])
    for (bx, by, r) in [(-w / 3, 0, h / 2), (0, -h / 6, h / 2 + 10), (w / 3, 0, h / 2), (-w / 6, h / 5, h / 2.2), (w / 6, h / 5, h / 2.2)]:
        circle(c, bx, by, r, C['white'])
    for i, ln in enumerate(txt_lines):
        text_c(c, ln, 0, (i - (len(txt_lines) - 1) / 2) * size * 1.25, size, C['ink'])
    c.restore()

def wave_memory(c, x, y, s, t):
    """mini comic: you wave back at someone who wasn't waving at you"""
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    circle(c, 0, 0, 230, C['white'])
    c.save(); c.arc(0, 0, 222, 0, 2 * math.pi); c.clip()
    rrect(c, -230, -230, 460, 460, 0); fill(c, hx('FFE8A3'))
    person(c, -90, 190, 0.42, t=t, face='big', look=12, armR=-2.7 + math.sin(t * 10) * 0.3, **YOU)
    person(c, 100, 190, 0.42, C['mint'], t + 1, face='smile', look=24, flip=True, armR=-2.7 + math.sin(t * 10) * 0.3, hairstyle=2)
    person(c, 200, 190, 0.42, C['yellow'], t + 2, face='big', look=-12, flip=True, hairstyle=0)
    c.restore(); c.restore()

def scene0(c, t):
    bedroom(c, t, face='worried', sweat=clamp((t - 1.0) / 1.5))
    title_pill(c, t, 0, None, 'THE 3 AM CRINGE', C['coral'])
    wave_memory(c, 380, 640, pop(t, 0.6, 0.5), t)
    s = pop(t, 1.4)
    if s > 0:
        c.save(); c.translate(380, 900); S(c, s); c.rotate(-0.08)
        rrect(c, -170, -50, 340, 100, 50); fill(c, hx('FF4D4D')); text_c(c, 'WHY?!', 0, 0, 56, C['white']); c.restore()

def scene1(c, t):
    lt = t - s1
    bedroom(c, t, face='flat' if t < wander else 'worried')
    title_pill(c, lt, 0, None, 'NO DISTRACTIONS', C['sky'])
    s = pop(t, s1 + 0.6)
    if s > 0 and t < wander:  # phone off
        c.save(); c.translate(360, 700); S(c, s)
        rrect(c, -90, -160, 180, 320, 30); fill(c, C['ink']); rrect(c, -76, -140, 152, 280, 20); fill(c, hx('15152A'))
        c.set_line_width(10); c.set_source_rgba(1, 1, 1, 0.6); c.arc(0, 0, 40, -math.pi * 0.35, math.pi * 1.35); c.stroke()
        line(c, 0, -50, 0, -5, 10, C['white'], 0.6); c.restore()
        for k in range(3):
            zt = (t - s1 - 0.8 - k * 0.4) % 1.8
            text_c(c, 'z', 560 + zt * 60 + k * 30, 980 - zt * 140, 50 + k * 10, C['white'], True, clamp(1 - zt / 1.8))
    if t >= wander:
        mems = [('school, 2014', 270, 640), ('"you too!"', 760, 520), ('that voice crack', 400, 380)]
        for k, (txt, x, y) in enumerate(mems):
            sk = pop(t, wander + 0.2 + k * 0.7, 0.5)
            fl = math.sin(t * 2 + k) * 12
            thought(c, x, y + fl, sk, 380, 120, [txt], 38)
        # swirl
        c.set_line_width(8); c.set_source_rgba(*C['yellow'], 0.8)
        for k in range(3):
            c.new_sub_path(); c.arc(250, 950, 30 + k * 22, t * 4 + k, t * 4 + k + 4.0); c.stroke()

def scene2(c, t):
    lt = t - s2
    bg(c, CAVE, t)
    title_pill(c, lt, 0, None, 'WIRED FOR THE TRIBE', C['yellow'])
    # campfire
    fx, fy = 480, 1380
    for k in range(5): rrect(c, fx - 120 + k * 30, fy + 10, 140, 26, 13) if False else None
    line(c, fx - 100, fy + 30, fx + 100, fy + 10, 26, hx('5A3A1A')); line(c, fx - 100, fy + 10, fx + 100, fy + 30, 26, hx('5A3A1A'))
    for k, (col, sc) in enumerate([(hx('FF6B1A'), 1.0), (C['yellow'], 0.65), (C['white'], 0.3)]):
        fl = 1 + 0.08 * math.sin(t * 12 + k)
        c.save(); c.translate(fx, fy); c.scale(sc * fl, sc * fl * (1.1 + 0.05 * math.sin(t * 9)))
        c.move_to(0, -170); c.curve_to(70, -90, 90, -20, 0, 20); c.curve_to(-90, -20, -70, -90, 0, -170); fill(c, col); c.restore()
    g = cairo.RadialGradient(fx, fy - 60, 0, fx, fy - 60, 520); g.add_color_stop_rgba(0, 1, 0.6, 0.2, 0.28); g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
    c.set_source(g); c.arc(fx, fy - 60, 520, 0, 2 * math.pi); c.fill()
    tribe = hx('8B5A2B')
    person(c, 200, 1450, 0.62, tribe, t, face='smile', look=12, hairstyle=0, hair=C['hair2'])
    person(c, 760, 1450, 0.62, tribe, t + 1, face='smile', look=-12, flip=True, hairstyle=2)
    person(c, 480, 1180, 0.5, tribe, t + 2, face='smile', hairstyle=1)
    out = eio((t - anc) / 1.2)
    ox = lerp(880, 950, out)
    person(c, ox, 1450, 0.62, C['sky'], t + 3, face='worried' if t > anc else 'smile', look=-14, flip=True, sweat=out, skin=C['skin2'], hairstyle=1)
    if t > anc + 0.6:
        for k in range(2):
            ex = 900 - k * 70 + math.sin(t * 2) * 6; ey = 520 + k * 20
            circle(c, ex - 20, ey, 10, C['yellow'], 0.9); circle(c, ex + 20, ey, 10, C['yellow'], 0.9)
        s = pop(t, anc + 0.9)
        c.save(); c.translate(W / 2, 760); S(c, s); c.rotate(-0.05)
        rrect(c, -300, -60, 600, 120, 60); fill(c, hx('E63946')); text_c(c, 'REJECTED = DANGER', 0, 0, 52, C['white']); c.restore()
    s = pop(t, s2 + 0.5)
    if s > 0 and t < anc + 0.6:
        c.save(); c.translate(W / 2, 640); S(c, s)
        for (bx, by, r) in [(-70, -10, 85), (40, -50, 90), (90, 30, 75), (-20, 50, 80), (-100, 50, 60)]: circle(c, bx, by, r, C['pink'])
        text_c(c, 'SOCIAL', 0, 10, 46, C['white']); c.restore()

def scene3(c, t):
    lt = t - s3
    bg(c, STAGE, t)
    title_pill(c, lt, 0, None, 'THE SPOTLIGHT EFFECT', C['mint'])
    # spotlight cone
    a = 0.30 if t < notice else 0.12
    c.move_to(W / 2 - 60, 330); c.line_to(W / 2 + 60, 330); c.line_to(W / 2 + 320, 1420); c.line_to(W / 2 - 320, 1420); c.close_path()
    c.set_source_rgba(1, 0.95, 0.7, a); c.fill()
    c.save(); c.translate(W / 2, 1420); c.scale(1, 0.18); circle(c, 0, 0, 320, (1, 0.95, 0.7), a + 0.1); c.restore()
    relaxed = t >= forgot
    person(c, W / 2, 1420, 0.8, t=t, face='big' if relaxed else ('worried' if t < notice + 0.5 else 'o'),
           sweat=0 if relaxed else clamp((t - s3) / 1.0), armL=-2.5 if relaxed else 0.15, armR=2.5 if relaxed else -0.15, **YOU)
    # imagined staring eyes before 'notice'
    if t < notice:
        for k in range(8):
            ang = k * math.pi / 4 + 0.3; x = W / 2 + math.cos(ang) * 400; y = 900 + math.sin(ang) * 380
            s = pop(t, s3 + 0.3 + k * 0.08, 0.3)
            if s > 0:
                c.save(); c.translate(x, y); S(c, s)
                c.save(); c.scale(1, 0.6); circle(c, 0, 0, 52, C['white']); c.restore(); circle(c, (W / 2 - x) * 0.05, (900 - y) * 0.05, 18, C['ink']); c.restore()
    else:
        # audience busy with phones
        for k, (x, y0) in enumerate([(110, 1250), (970, 1250), (150, 1480), (930, 1480)]):
            pr = clamp((t - notice) / 0.6)
            y = lerp(y0 + 500, y0, eo(pr))
            circle(c, x, y, 80, [C['hair1'], C['hair2'], C['ink'], C['hair2']][k])
            c.save(); c.translate(x + 40, y - 110); c.rotate(0.15)
            rrect(c, -36, -60, 72, 120, 14); fill(c, C['ink']); rrect(c, -28, -50, 56, 100, 8); fill(c, C['sky'], 0.85 + 0.15 * math.sin(t * 5 + k)); c.restore()
        if t >= moment and t < forgot:
            thought(c, 300, 620, pop(t, moment), 300, 130, ['that moment?'], 40)
        if t >= forgot:
            thought(c, 320, 620, pop(t, forgot), 330, 130, ['what moment?'], 40)
            s = pop(t, forgot + 0.4)
            c.save(); c.translate(780, 520); S(c, s); c.rotate(0.1)
            rrect(c, -190, -55, 380, 110, 55); fill(c, C['mint']); text_c(c, 'FORGOTTEN', 0, 0, 48, C['ink']); c.restore()

def scene4(c, t):
    lt = t - s4
    bedroom(c, t, face='smile')
    for k in range(3):
        zt = (lt - k * 0.4) % 1.8
        text_c(c, 'Z', 560 + zt * 60 + k * 30, 980 - zt * 160, 60 + k * 14, C['white'], True, clamp(1 - zt / 1.8))
    s2 = pop(lt, 0.2); tapped = lt > 1.2
    c.save(); c.translate(W / 2, 470); S(c, s2)
    rrect(c, -280, -75, 560, 150, 75); fill(c, (0.92, 0.92, 0.95) if tapped else C['sky'])
    text_c(c, 'Following' if tapped else 'Follow @neuronbites', 0, 0, 54 if tapped else 44, C['ink'] if tapped else C['white'])
    c.restore()
    fx = lerp(W / 2 + 480, W / 2 + 230, eio((lt - 0.4) / 0.5)); fy = lerp(1000, 520, eio((lt - 0.4) / 0.5))
    bk = eio((lt - 1.4) / 0.4); fx = lerp(fx, W + 200, bk); fy = lerp(fy, -300, bk)
    circle(c, fx, fy, 46, C['skin1']); line(c, fx, fy, fx + 70, fy + 260, 92, C['skin1'])

SC = [scene0, scene1, scene2, scene3, scene4]
SCENES = [0, s1, s2, s3, s4, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
