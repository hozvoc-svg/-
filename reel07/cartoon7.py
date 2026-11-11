import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel04'))
os.chdir(HERE)
from engine import *
import engine
def S(c, k): k = max(k, 1e-3); c.scale(k, k)

t_of, DUR = load_timing('align.json')
replay = t_of('You replay'); comeback = t_of('find the'); win = t_of('you win')
s2 = t_of("It's called"); brain = t_of('Your brain')
s3 = t_of('The catch'); body = t_of('Your body'); racing = t_of('Racing'); nosleep = t_of('no sleep')
s4 = t_of('So end'); calm = t_of('One calm'); letgo = t_of('then let')
s5 = t_of('Send this')

engine.BG += [(hx('070B1F'), hx('1B2453')), (hx('3B0A14'), hx('8E1B2E')), (hx('0B2B2A'), hx('1F7A6C'))]
NIGHT, ALARM, CALM = 6, 7, 8
NIGHT_TOP = hx('0B1030')
RED = hx('E63946')
YOU = dict(shirt=C['sky'], skin=C['skin2'], hairstyle=1)
THEM = dict(shirt=C['coral'], skin=C['skin1'], hairstyle=2)

# ---------- shared pieces ----------
def night_sky(c, t):
    random.seed(4)
    for k in range(40):
        x = random.uniform(0, W); y = random.uniform(0, 900); r = random.uniform(2, 5)
        circle(c, x, y, r, C['white'], 0.4 + 0.4 * abs(math.sin(t * 2 + k)))

def clock_text(t):
    """clock runs fast: starts 11:58 PM, races during the 'no sleep' part"""
    if t < racing: mins = 23 * 60 + 58 + int(t / 6)
    else: mins = 23 * 60 + 58 + int(racing / 6) + int((t - racing) * 55)
    mins %= 24 * 60
    h = mins // 60; m = mins % 60
    ampm = 'AM' if h < 12 else 'PM'; h = h % 12 or 12
    return f'{h}:{m:02d}', ampm

def bedroom(c, t, bgi=NIGHT, face='worried', sweat=0.0, clock=True):
    bg(c, bgi, t)
    if bgi == NIGHT: night_sky(c, t)
    rrect(c, 90, 1180, 900, 220, 40); fill(c, hx('3A2F6B'))
    rrect(c, 90, 1360, 30, 160, 10); fill(c, hx('2A2250')); rrect(c, 960, 1360, 30, 160, 10); fill(c, hx('2A2250'))
    rrect(c, 120, 1080, 240, 130, 50); fill(c, C['white'])
    c.save(); c.translate(250, 1080); c.rotate(-math.pi / 2)
    person(c, 0, 440, 0.9, t=t, face=face, sweat=sweat, **YOU)
    c.restore()
    rrect(c, 420, 1050, 570, 260, 60); fill(c, C['violet'])
    for k in range(3): line(c, 500 + k * 160, 1080, 540 + k * 160, 1290, 10, hx('6247D9'))
    if clock:
        rrect(c, 700, 940, 280, 110, 24); fill(c, C['ink'])
        hm, ap = clock_text(t)
        text_c(c, hm, 815, 995, 60, hx('FF4D4D')); text_c(c, ap, 935, 1005, 26, hx('FF4D4D'))

def cloud(c, x, y, s, w, h, col=C['white'], tail=(-1, 1)):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    tx, ty = tail
    circle(c, tx * (w / 2 - 40), h / 2 + 50, 22, col); circle(c, tx * (w / 2 - 80), h / 2 + 100, 14, col)
    rrect(c, -w / 2, -h / 2, w, h, min(h / 2, 120)); fill(c, col)
    for k in range(7):
        bx = -w / 2 + 40 + k * (w - 80) / 6
        circle(c, bx, -h / 2 + 10, 60 + 12 * math.sin(k * 1.7), col)
        circle(c, bx, h / 2 - 10, 55 + 10 * math.cos(k * 1.3), col)
    c.restore()

def speech(c, x, y, s, txt, col, tcol=C['white'], size=40, tail='left', w=None):
    if s <= 0: return
    c.save(); c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = w or c.text_extents(txt).width + 70; c.restore()
    bubble(c, x, y, w, size + 50, s, tail, txt, size, col, tcol)

def stamp(c, x, y, s, txt, col, tcol=C['white'], size=50, rot=-0.06):
    if s <= 0: return
    c.save(); c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = c.text_extents(txt).width + 90
    c.translate(x, y); S(c, s); c.rotate(rot)
    c.set_source_rgba(0, 0, 0, 0.25); rrect(c, -w / 2 + 6, -size - 4, w, size * 2 + 8, size + 4); c.fill()
    rrect(c, -w / 2, -size - 10, w, size * 2 + 8, size + 4); fill(c, col)
    text_c(c, txt, 0, -6, size, tcol); c.restore()

def fight_dream(c, t, x, y, s, phase):
    """thought cloud with an imagined argument. phase: 0 arguing, 1 comeback, 2 win"""
    if s <= 0: return
    cloud(c, x, y, s, 820, 520)
    c.save(); c.translate(x, y); S(c, s)
    c.save(); rrect(c, -400, -250, 800, 500, 120); c.clip()
    shake = math.sin(t * 40) * 4 if phase == 0 else 0
    person(c, -200 + shake, 250, 0.5, t=t, face='big' if phase == 2 else ('flat' if phase == 1 else 'worried'),
           look=16, armR=-2.6 if phase == 2 else -0.4, armL=2.6 if phase == 2 else 0.15, **YOU)
    person(c, 200, 250, 0.5, t=t + 1, face='o' if phase >= 1 else 'big', look=-16, flip=True,
           sweat=0.7 if phase >= 1 else 0, **THEM)
    c.restore(); c.restore()

# ---------- scenes ----------
def scene0(c, t):
    bedroom(c, t, face='flat', sweat=0)
    title_pill(c, t, 0, None, 'FAKE ARGUMENTS?', RED)
    fight_dream(c, t, W / 2, 640, pop(t, 0.15, 0.5), 0)
    sp = [(0.45, 'YOU ALWAYS...', C['coral'], 720, 450, 'right'), (1.1, 'NO, YOU...', C['sky'], 340, 450, 'left'),
          (1.7, '!!!', C['coral'], 860, 560, 'right')]
    for t0, txt, col, x, y, tl in sp:
        speech(c, x, y, pop(t, t0, 0.35), txt, col, size=38, tail=tl)
    if t > 2.3:
        stamp(c, 460, 905, pop(t, 2.4), 'IT HAS A NAME', C['yellow'], C['ink'], 46, 0.04)

def scene1(c, t):
    lt = t - replay
    phase = 0 if t < comeback else (1 if t < win else 2)
    bedroom(c, t, face='flat' if phase < 2 else 'smile')
    title_pill(c, lt, 0, None, 'TAKE 47', C['violet'])
    fight_dream(c, t, W / 2, 640, 1.0, phase)
    # rewind icon while replaying
    if phase == 0:
        stamp(c, 400, 905, pop(t, replay + 0.2), '◀◀ REPLAY', C['white'], C['ink'], 40)
    if phase >= 1:
        speech(c, 360, 470, pop(t, comeback + 0.2, 0.35), '"ACTUALLY..."', C['sky'], size=40, tail='left')
        stamp(c, 460, 905, pop(t, comeback + 0.5), 'PERFECT COMEBACK', C['yellow'], C['ink'], 44)
    if phase == 2:
        stamp(c, 790, 400, pop(t, win), 'YOU WIN', C['mint'], C['ink'], 56, 0.12)
        for k in range(8):
            ang = k * math.pi / 4 + t; r = 300 + 40 * math.sin(t * 6 + k)
            star(c, W / 2 + math.cos(ang) * r * 1.3, 640 + math.sin(ang) * r * 0.8, 26, C['yellow'], 0.9, t * 3 + k)

def clapper(c, x, y, s, t, txt):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -60, 460, 260, 20); fill(c, C['ink'])
    open_ = 0.35 * max(0, math.sin(t * 5))
    c.save(); c.translate(-230, -60); c.rotate(-open_)
    rrect(c, 0, -60, 460, 60, 10); fill(c, C['white'])
    for k in range(5):
        c.move_to(20 + k * 92, -60); c.line_to(70 + k * 92, -60); c.line_to(40 + k * 92, 0); c.line_to(-10 + k * 92, 0); c.close_path(); fill(c, C['ink'])
    c.restore()
    text_c(c, txt[0], 0, 20, 46, C['white']); text_c(c, txt[1], 0, 110, 40, C['yellow'])
    c.restore()

def scene2(c, t):
    lt = t - s2
    bg(c, 5, t)
    title_pill(c, lt, 0, None, 'IMAGINED INTERACTIONS', C['yellow'])
    # stage + the brain directing a rehearsal
    c.move_to(W / 2 - 60, 330); c.line_to(W / 2 + 60, 330); c.line_to(W / 2 + 380, 1450); c.line_to(W / 2 - 380, 1450); c.close_path()
    c.set_source_rgba(1, 0.95, 0.7, 0.16); c.fill()
    rrect(c, 60, 1450, 960, 90, 20); fill(c, hx('3B2A6B'))
    person(c, 380, 1450, 0.62, t=t, face='o' if t < brain + 1 else 'big', look=14, armR=-0.6, **YOU)
    person(c, 700, 1450, 0.62, t=t + 1, face='big', look=-14, flip=True, **THEM)
    clapper(c, W / 2, 560, pop(t, s2 + 0.3), t, ('REHEARSAL', 'TAKE 47'))
    if t > brain:
        stamp(c, W / 2, 940, pop(t, brain + 0.2), 'PRACTICE FOR WHAT SCARES YOU', C['mint'], C['ink'], 36, 0.03)
        # shield = safer real life
        s = pop(t, brain + 1.0)
        if s > 0:
            c.save(); c.translate(960, 1130); S(c, s * 0.8)
            c.move_to(0, -90); c.curve_to(70, -70, 90, -60, 90, -50); c.line_to(90, 10); c.curve_to(90, 70, 30, 100, 0, 120)
            c.curve_to(-30, 100, -90, 70, -90, 10); c.line_to(-90, -50); c.curve_to(-90, -60, -70, -70, 0, -90); fill(c, C['yellow'])
            line(c, -35, 10, -5, 45, 18, C['ink']); line(c, -5, 45, 45, -25, 18, C['ink']); c.restore()

def heart_meter(c, x, y, t, bpm):
    beat = (t * bpm / 60) % 1
    k = 1 + 0.22 * math.exp(-beat * 9)
    heart(c, x, y, 3.0 * k, hx('FF3355'))
    text_c(c, f'{int(bpm)} BPM', x, y + 150, 46, C['white'])

def scene3(c, t):
    lt = t - s3
    alarm = t >= body
    bedroom(c, t, bgi=ALARM if alarm else NIGHT, face='worried', sweat=clamp((t - body) / 1.2))
    title_pill(c, lt, 0, None, 'THE CATCH', RED)
    if not alarm:
        stamp(c, W / 2, 620, pop(t, s3 + 0.1), '?', C['yellow'], C['ink'], 90)
    else:
        bpm = lerp(68, 128, eo((t - body) / 2.0))
        heart_meter(c, 300, 600, t, bpm)
        # ECG line
        c.set_line_width(8); c.set_source_rgba(1, 1, 1, 0.85)
        for i in range(0, 61):
            xx = 480 + i * 9; ph = (i / 60 * 4 - t * 2) % 1
            yy = 600 - (120 if 0.45 < ph < 0.5 else (-60 if 0.5 <= ph < 0.55 else 0))
            (c.move_to if i == 0 else c.line_to)(xx, yy)
        c.stroke()
        stamp(c, 780, 420, pop(t, body + 0.3), 'FEELS REAL', C['white'], RED, 44, 0.08)
        if t > nosleep:
            stamp(c, W / 2, 880, pop(t, nosleep), 'NO SLEEP', C['yellow'], C['ink'], 56, -0.05)

def end_card(c, x, y, s, t):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -300, -150, 600, 300, 30); fill(c, C['ink'])
    c.set_line_width(10); c.set_source_rgba(1, 1, 1, 0.8); rrect(c, -270, -120, 540, 240, 20); c.stroke()
    text_c(c, 'THE END', 0, -20, 86, C['white']); text_c(c, '(on purpose)', 0, 70, 34, C['yellow'])
    c.restore()

def scene4(c, t):
    lt = t - s4
    sleeping = t >= letgo
    bedroom(c, t, bgi=CALM, face='smile', clock=False)
    title_pill(c, lt, 0, None, 'END THE SCENE', C['mint'])
    if not sleeping:
        end_card(c, W / 2, 620, pop(t, s4 + 0.2), t)
        if t > calm:
            speech(c, 330, 880, pop(t, calm + 0.1, 0.35), '"I said what I needed."', C['white'], C['ink'], 34, 'left')
    else:
        # card fades, Zs drift
        k = eo((t - letgo) / 0.5)
        end_card(c, W / 2, 620, (1 - k) * 1.0, t)
        for j in range(3):
            zt = ((t - letgo) - j * 0.4) % 1.8
            text_c(c, 'Z', 520 + zt * 60 + j * 30, 980 - zt * 160, 64 + j * 14, C['white'], True, clamp(1 - zt / 1.8))
        stamp(c, W / 2, 640, pop(t, letgo + 0.2), 'LET IT GO', C['white'], C['ink'], 50)

def phone(c, x, y, s, t, sent):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -400, 460, 800, 60); fill(c, C['ink'])
    rrect(c, -205, -370, 410, 740, 40); fill(c, hx('F2F2F7'))
    text_c(c, 'Share to', 0, -310, 40, C['ink'])
    for k, (col, nm) in enumerate([(C['coral'], 'bestie'), (C['mint'], 'roommate'), (C['sky'], 'sister')]):
        yy = -190 + k * 150
        circle(c, -120, yy, 50, col); text_c(c, nm, 20, yy, 36, C['ink'], bold=False)
        if k == 0:
            bx = 140
            rrect(c, bx - 60, yy - 32, 120, 64, 32); fill(c, (0.85, 0.85, 0.9) if sent else hx('0095F6'))
            text_c(c, 'Sent' if sent else 'Send', bx, yy, 30, C['ink'] if sent else C['white'])
    c.restore()

def scene5(c, t):
    lt = t - s5
    bg(c, 0, t)
    title_pill(c, lt, 0, None, 'SEND THIS TO...', C['coral'])
    # friend arguing in shower (small vignette)
    s = pop(t, s5 + 0.1)
    if s > 0:
        c.save(); c.translate(300, 820); S(c, s)
        circle(c, 0, 0, 220, hx('BDE6F5')); c.save(); c.arc(0, 0, 212, 0, 2 * math.pi); c.clip()
        for k in range(14):
            dx = -150 + k * 23; dy = ((t * 400 + k * 57) % 300) - 220
            line(c, dx, dy, dx, dy + 30, 6, C['sky'], 0.8)
        person(c, 0, 230, 0.45, t=t, face='big', armR=-2.4 + 0.4 * math.sin(t * 9), **THEM)
        c.restore(); c.restore()
        speech(c, 390, 560, pop(t, s5 + 0.6, 0.3), 'AND ANOTHER THING!', C['coral'], size=32, tail='left')
    sent = lt > 2.2
    phone(c, 760, 1050, pop(t, s5 + 0.4), t, sent)
    # tapping finger
    fx = lerp(W + 200, 760 + 140, eio((lt - 1.3) / 0.6)); fy = lerp(1500, 1050 - 190 + 40, eio((lt - 1.3) / 0.6))
    bk = eio((lt - 2.5) / 0.5); fx = lerp(fx, W + 250, bk); fy = lerp(fy, 1700, bk)
    circle(c, fx, fy, 40, C['skin1']); line(c, fx, fy, fx + 60, fy + 240, 80, C['skin1'])
    if lt > 2.6:
        stamp(c, 300, 1250, pop(t, s5 + 2.6), 'Follow @neuronbites', C['sky'], C['white'], 36, 0.0)

SC = [scene0, scene1, scene2, scene3, scene4, scene5]
SCENES = [0, replay, s2, s3, s4, s5, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
