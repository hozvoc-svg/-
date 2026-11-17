import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel07'))
from engine import *
import engine
import cartoon7 as k7          # reuse stamp / speech helpers from reel 7
from cartoon7 import S, stamp, speech, RED
os.chdir(HERE)

t_of, DUR = load_timing('align.json')
someone = t_of('Someone'); andyou = t_of('and you'); smile = t_of('smile')
s1 = t_of("You're not"); called = t_of("It's called")
s2 = t_of('When a'); brain = t_of('your brain'); opposite = t_of('the opposite'); valve = t_of('Like a')
s3 = t_of('So next'); panic = t_of("don't panic"); say = t_of('Just say'); sorry = t_of('Sorry')
s4 = t_of('Send this')

YOU = dict(shirt=C['yellow'], skin=C['skin1'], hairstyle=0)
FRIEND = dict(shirt=C['violet'], skin=C['skin2'], hairstyle=2)

# ---------- pieces ----------
def rain_cloud(c, x, y, s, t):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    for (bx, by, r) in [(-60, 0, 60), (0, -30, 70), (60, 0, 60), (0, 20, 60)]: circle(c, bx, by, r, hx('7A8199'))
    for k in range(7):
        dy = (t * 500 + k * 47) % 200
        line(c, -70 + k * 23, 60 + dy, -74 + k * 23, 85 + dy, 6, C['sky'], 0.9)
    c.restore()

def table(c, y):
    rrect(c, 140, y, 800, 40, 14); fill(c, hx('8A5A3C'))
    rrect(c, 160, y + 40, 760, 160, 10); fill(c, hx('6B4430'))
    # two mugs
    for x in (330, 750):
        rrect(c, x - 30, y - 64, 60, 64, 10); fill(c, C['white'])
        c.set_line_width(8); c.set_source_rgb(1, 1, 1); c.arc(x + 32, y - 32, 16, -1.3, 1.3); c.stroke()

def scene0(c, t):
    bg(c, 1, t)
    title_pill(c, t, 0, None, 'THE WORST MOMENT TO LAUGH', RED)
    grin = t >= smile
    person(c, 300, 1500, 0.8, t=t, face='big' if grin else ('flat' if t < andyou else 'o'), look=14,
           sweat=clamp((t - andyou) / 1.0), blush=grin, **YOU)
    person(c, 790, 1500, 0.8, t=t + 1, face='worried', look=-14, flip=True, **FRIEND)
    table(c, 1360)
    rain_cloud(c, 790, 640, pop(t, someone, 0.5), t)
    if t >= someone:
        speech(c, 760, 840, pop(t, someone + 0.2, 0.35), '"I got fired..."', C['white'], C['ink'], 42, 'right')
    if andyou <= t < smile:
        # lips pressed, trying not to laugh
        stamp(c, 300, 820, pop(t, andyou + 0.2), "DON'T LAUGH", C['white'], C['ink'], 40, -0.05)
    if grin:
        stamp(c, 300, 820, pop(t, smile), '*SMILES*', C['yellow'], C['ink'], 50, -0.06)
        for k in range(3):
            text_c(c, 'ha', 170 + k * 60 + math.sin(t * 9 + k) * 6, 960 - k * 30, 44, C['white'], True, clamp((t - smile - k * 0.15) / 0.2))
        stamp(c, W / 2, 470, pop(t, smile + 0.4), 'WHY?!', RED, C['white'], 70, 0.04)

def scene1(c, t):
    lt = t - s1
    bg(c, 3, t)
    title_pill(c, lt, 0, None, "YOU'RE NOT A BAD PERSON", C['mint'])
    person(c, W / 2, 1500, 0.95, t=t, face='smile', look=0, **YOU)
    # halo + check badge
    c.save(); c.translate(W / 2, 1500 - 440 * 0.95 - 120); c.scale(1, 0.3)
    c.set_line_width(22); c.set_source_rgb(*C['yellow']); c.arc(0, 0, 110 * pop(t, s1 + 0.2), 0, 2 * math.pi); c.stroke(); c.restore()
    s = pop(t, s1 + 0.4)
    if s > 0:
        c.save(); c.translate(820, 980); S(c, s)
        circle(c, 0, 0, 90, C['mint']); line(c, -40, 0, -10, 35, 20, C['ink']); line(c, -10, 35, 45, -35, 20, C['ink']); c.restore()
    if t >= called:
        stamp(c, W / 2, 560, pop(t, called + 0.2), 'NERVOUS LAUGHTER', C['yellow'], C['ink'], 60, -0.03)

def scale_beam(c, t, left_w, right_w):
    """balance scale; weights decide tilt"""
    cx, cy = W / 2, 980
    tilt = clamp((left_w - right_w) * 0.35, -0.35, 0.35)
    line(c, cx, cy, cx, 1450, 22, C['white']); rrect(c, cx - 160, 1440, 320, 40, 16); fill(c, C['white'])
    c.save(); c.translate(cx, cy); c.rotate(-tilt)
    line(c, -360, 0, 360, 0, 20, C['white']); circle(c, 0, 0, 26, C['yellow'])
    pans = []
    for side in (-1, 1):
        px = side * 360
        c.save(); c.translate(px, 0); c.rotate(tilt)
        line(c, -110, 210, 0, 0, 5, C['white']); line(c, 110, 210, 0, 0, 5, C['white'])
        c.move_to(-140, 210); c.line_to(140, 210); c.curve_to(110, 270, -110, 270, -140, 210); fill(c, C['white'])
        c.restore()
    c.restore()
    return cx, cy, tilt

def weight(c, x, y, s, col, txt, size=40):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    c.move_to(-110, 0); c.line_to(110, 0); c.line_to(80, -150); c.line_to(-80, -150); c.close_path(); fill(c, col)
    rrect(c, -30, -185, 60, 40, 14); fill(c, col)
    text_c(c, txt, 0, -70, size, C['white']); c.restore()

def steam_valve(c, t, x, y, s):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -150, 460, 300, 70); fill(c, hx('9AA3B5'))
    rrect(c, -260, -170, 520, 50, 25); fill(c, hx('7A8199'))
    rrect(c, -30, -240, 60, 80, 14); fill(c, RED)
    text_c(c, 'STRESS', 0, 20, 64, C['ink'])
    # steam puffs = laughs
    for k in range(5):
        pt = (t * 1.2 + k / 5) % 1
        r = 30 + pt * 60
        circle(c, math.sin(k * 2 + t) * 40 * pt, -260 - pt * 380, r, C['white'], 0.95 * (1 - pt * 0.7))
        text_c(c, 'HA', math.sin(k * 2 + t) * 40 * pt, -260 - pt * 380, 26 + pt * 30, C['ink'], True, 0.95 * (1 - pt * 0.7))
    c.restore()

def scene2(c, t):
    lt = t - s2
    bg(c, 5, t)
    if t < valve:
        title_pill(c, lt, 0, None, 'TOO MUCH FEELING', C['coral'])
        lw = eo((t - s2 - 0.2) / 0.6) * 1.0
        rw = eo((t - opposite) / 0.6) * 1.0 if t > opposite else 0
        cx, cy, tilt = scale_beam(c, t, lw, rw)
        # weights sit in pans (follow beam tilt)
        for side, w, col, txt in ((-1, lw, RED, 'STRESS'), (1, rw, C['yellow'], 'LAUGH')):
            px = cx + side * 360 * math.cos(tilt); py = cy - side * 360 * math.sin(tilt) + 214
            weight(c, px, py, pop(t, s2 + 0.2 if side < 0 else opposite, 0.4), col, txt, 38)
        if t > brain:
            # brain icon
            s = pop(t, brain)
            c.save(); c.translate(W / 2, 600); S(c, s)
            for (bx, by, r) in [(-50, 0, 70), (20, -30, 75), (70, 20, 60), (-10, 40, 65)]: circle(c, bx, by, r, C['pink'])
            line(c, 0, -80, 0, 90, 8, hx('C2185B')); c.restore()
        if t > opposite + 0.6:
            stamp(c, W / 2, 760, pop(t, opposite + 0.6), 'BALANCED', C['mint'], C['ink'], 46, 0.03)
    else:
        title_pill(c, t - valve, 0, None, 'A PRESSURE VALVE', C['sky'])
        steam_valve(c, t, W / 2, 1300, pop(t, valve, 0.4) * 1.35)

def scene3(c, t):
    lt = t - s3
    bg(c, 3, t)
    title_pill(c, lt, 0, None, 'NEXT TIME', C['mint'])
    calm = t >= sorry + 1.0
    person(c, 300, 1500, 0.8, t=t, face='smile' if t >= say else 'worried', look=14, **YOU)
    person(c, 790, 1500, 0.8, t=t + 1, face='big' if calm else 'worried', look=-14, flip=True, **FRIEND)
    table(c, 1360)
    if t >= panic and t < say:
        stamp(c, W / 2, 620, pop(t, panic), "DON'T PANIC", C['white'], C['ink'], 60, -0.04)
    if t >= sorry:
        speech(c, W / 2, 620, pop(t, sorry, 0.35), '"Sorry, I laugh when I\'m nervous."', C['yellow'], C['ink'], 36, 'left', w=900)
    if calm:
        speech(c, 790, 860, pop(t, sorry + 1.0, 0.3), 'SAME!', C['white'], C['ink'], 48, 'right')
        for k in range(4):
            hh = ((t - sorry) * 0.7 + k / 4) % 1
            heart(c, 470 + k * 50 + math.sin(t * 3 + k) * 20, 1150 - hh * 250, 0.9, hx('FF6FA5'), 1 - hh)

def phone10(c, x, y, s, t, sent):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -400, 460, 800, 60); fill(c, C['ink'])
    rrect(c, -205, -370, 410, 740, 40); fill(c, hx('F2F2F7'))
    text_c(c, 'Share to', 0, -310, 40, C['ink'])
    for k, (col, nm) in enumerate([(C['coral'], 'that friend'), (C['mint'], 'bestie'), (C['sky'], 'sister')]):
        yy = -190 + k * 150
        circle(c, -140, yy, 46, col); text_c(c, nm, 0, yy, 30, C['ink'], bold=False)
        if k == 0:
            bx = 140
            rrect(c, bx - 60, yy - 32, 120, 64, 32); fill(c, (0.85, 0.85, 0.9) if sent else hx('0095F6'))
            text_c(c, 'Sent' if sent else 'Send', bx, yy, 30, C['ink'] if sent else C['white'])
    c.restore()

def scene4(c, t):
    lt = t - s4
    bg(c, 0, t)
    title_pill(c, lt, 0, None, 'SEND THIS TO...', C['coral'])
    s = pop(t, s4 + 0.1)
    if s > 0:
        c.save(); c.translate(290, 900); S(c, s)
        circle(c, 0, 0, 210, hx('2B1E6B'))
        c.save(); c.arc(0, 0, 202, 0, 2 * math.pi); c.clip()
        person(c, 0, 360, 0.75, t=t, face='big', blush=True, **FRIEND)
        c.restore(); c.restore()
        text_c(c, 'the friend who', 290, 1160, 40, C['white'], True, clamp((lt - 0.4) / 0.3))
        text_c(c, 'laughed at the', 290, 1215, 40, C['white'], True, clamp((lt - 0.4) / 0.3))
        text_c(c, 'worst moment', 290, 1270, 40, C['yellow'], True, clamp((lt - 0.4) / 0.3))
    sent = lt > 1.4
    phone10(c, 780, 1000, pop(t, s4 + 0.3), t, sent)
    fx = lerp(W + 200, 780 + 140, eio((lt - 0.7) / 0.5)); fy = lerp(1500, 1000 - 190 + 40, eio((lt - 0.7) / 0.5))
    bk = eio((lt - 1.7) / 0.4); fx = lerp(fx, W + 250, bk); fy = lerp(fy, 1700, bk)
    circle(c, fx, fy, 40, C['skin1']); line(c, fx, fy, fx + 60, fy + 240, 80, C['skin1'])
    if lt > 1.7:
        stamp(c, 290, 1410, pop(t, s4 + 1.7), 'Follow @neuronbites', C['sky'], C['white'], 34, 0.0)

SC = [scene0, scene1, scene2, scene3, scene4]
SCENES = [0, s1, s2, s3, s4, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
