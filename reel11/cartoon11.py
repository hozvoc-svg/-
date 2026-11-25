import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel07'))
from engine import *
import engine
import cartoon7 as k7          # reuse stamp / speech helpers from reel 7
from cartoon7 import S, stamp, speech, RED
os.chdir(HERE)

t_of, DUR = load_timing('align.json')
notjust = t_of('Not just'); literally = t_of('Literally')
s1 = t_of('In a famous'); played = t_of('people played'); stopped = t_of('Then the')
s2 = t_of('Brain scans'); pain = t_of('physical pain')
s3 = t_of("That's why"); onread = t_of('left on read'); punch = t_of('like a punch')
s4 = t_of("You're not"); wired = t_of('Your brain')
s5 = t_of('Send this')

YOU = dict(shirt=C['sky'], skin=C['skin1'], hairstyle=2)
P2 = dict(shirt=C['coral'], skin=C['skin2'], hairstyle=0)
P3 = dict(shirt=C['mint'], skin=C['skin3'], hairstyle=1)
BLUE = hx('0095F6')

# ---------- pieces ----------
def chat_phone(c, x, y, s, t, msgs, status=None):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -250, -420, 500, 840, 60); fill(c, C['ink'])
    rrect(c, -225, -390, 450, 780, 40); fill(c, hx('F2F2F7'))
    rrect(c, -225, -390, 450, 110, 40); fill(c, C['white'])
    circle(c, -150, -335, 34, C['coral']); text_c(c, 'them', -40, -335, 34, C['ink'])
    yy = -200
    for txt, mine, t0 in msgs:
        k = pop(t, t0, 0.3)
        if k <= 0: continue
        c.save(); c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(34)
        w = c.text_extents(txt).width + 60; c.restore()
        bx = 200 - w / 2 if mine else -200 + w / 2
        c.save(); c.translate(bx, yy); S(c, k)
        rrect(c, -w / 2, -40, w, 80, 34); fill(c, BLUE if mine else hx('E5E5EA'))
        text_c(c, txt, 0, 0, 34, C['white'] if mine else C['ink']); c.restore()
        yy += 110
    if status:
        txt, t0 = status
        text_c(c, txt, 120, yy - 40, 28, hx('8E8E93'), False, clamp((t - t0) / 0.3))
    c.restore()

def crack_heart(c, x, y, s, t, split):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    for side in (-1, 1):
        c.save(); c.translate(side * split * 40, split * 20); c.rotate(side * split * 0.25)
        c.rectangle(0 if side > 0 else -200, -200, 200, 400); c.clip()
        heart(c, 0, 0, 4.0, hx('FF3D7F')); c.restore()
    if split > 0:
        c.set_line_width(10); c.set_source_rgb(*C['ink'])
        c.move_to(0, -100); c.line_to(-20, -40); c.line_to(18, 10); c.line_to(-10, 70); c.line_to(0, 110)
        c.new_path()
    c.restore()

def bandaid(c, x, y, s, rot=0.5):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s); c.rotate(rot)
    rrect(c, -120, -40, 240, 80, 40); fill(c, hx('F2C094'))
    rrect(c, -40, -36, 80, 72, 12); fill(c, hx('E3A774'))
    for i in range(3):
        for j in range(2): circle(c, -20 + i * 20, -12 + j * 24, 4, hx('C98B5A'))
    c.restore()

def scene0(c, t):
    bg(c, 5, t)
    title_pill(c, t, 0, None, 'BEING IGNORED', RED)
    chat_phone(c, W / 2, 960, 1.15, t, [('hey :)', True, 0.2), ('you there?', True, 0.9), ('???', True, 1.6)],
               ('Seen 2h ago', 2.0))
    if t > notjust:
        split = eo((t - literally) / 0.4) if t > literally else 0
        crack_heart(c, 860, 420, pop(t, notjust, 0.4) * 0.6, t, split)
    if t > literally:
        stamp(c, 300, 430, pop(t, literally + 0.1), 'IT HURTS', RED, C['white'], 52, -0.06)

def scene1(c, t):
    lt = t - s1
    bg(c, 1, t)
    title_pill(c, lt, 0, None, 'THE BALL GAME TEST', C['yellow'])
    pos = {'you': (W / 2, 1520), 'a': (230, 1150), 'b': (850, 1150)}
    excluded = t >= stopped + 0.4
    person(c, *pos['a'], 0.6, t=t, face='big', look=14, armR=-2.2, **P2)
    person(c, *pos['b'], 0.6, t=t + 1, face='big', look=-14, flip=True, armR=-2.2, **P3)
    person(c, *pos['you'], 0.7, t=t + 2, face='worried' if excluded else 'big',
           armL=-2.5 if not excluded else -1.2, armR=2.5 if not excluded else 1.2, sweat=0.6 if excluded else 0, **YOU)
    # ball path
    hands = {'you': (W / 2, 1100), 'a': (300, 830), 'b': (780, 830)}
    seq = ['a', 'you', 'b', 'a', 'you', 'b'] if not excluded else ['a', 'b']
    period = 0.55
    tt = (t - s1) / period if not excluded else (t - stopped) / period
    i = int(tt) % len(seq); f = tt - int(tt)
    p0 = hands[seq[i]]; p1 = hands[seq[(i + 1) % len(seq)]]
    bx = lerp(p0[0], p1[0], f); by = lerp(p0[1], p1[1], f) - math.sin(f * math.pi) * 160
    circle(c, bx, by, 34, C['yellow']); c.set_line_width(5); c.set_source_rgb(*C['ink']); c.arc(bx, by, 34, 0, 2 * math.pi); c.stroke()
    if excluded:
        speech(c, W / 2 + 230, 900, pop(t, stopped + 0.6, 0.3), '...me?', C['white'], C['ink'], 40, 'left')
        stamp(c, W / 2, 470, pop(t, stopped + 0.9), 'LEFT OUT', RED, C['white'], 56, -0.04)

def brain_side(c, x, y, s, t, glow):
    c.save(); c.translate(x, y); S(c, s)
    for (bx, by, r) in [(-120, -20, 150), (20, -90, 160), (150, -10, 140), (40, 70, 140), (-90, 90, 110), (210, 90, 90)]:
        circle(c, bx, by, r, C['pink'])
    c.set_line_width(10); c.set_source_rgb(*hx('C2185B'))
    for k in range(6):
        c.move_to(-200 + k * 70, -120 + (k % 2) * 40); c.curve_to(-170 + k * 70, -40, -230 + k * 70, 20, -190 + k * 70, 100); c.stroke()
    line(c, 120, 180, 170, 330, 60, hx('E05A97'))
    if glow > 0:
        r = 120 + 25 * math.sin(t * 10)
        g = cairo.RadialGradient(10, -40, 0, 10, -40, r); g.add_color_stop_rgba(0, 1, 0.15, 0.15, 0.95 * glow); g.add_color_stop_rgba(1, 1, 0.1, 0.1, 0)
        c.set_source(g); c.arc(10, -40, r, 0, 2 * math.pi); c.fill()
    c.restore()

def scene2(c, t):
    lt = t - s2
    bg(c, 5, t)
    title_pill(c, lt, 0, None, 'BRAIN SCANS', C['sky'])
    # scanner ring
    s = pop(t, s2 + 0.1)
    c.save(); c.translate(W / 2, 930); S(c, s)
    c.new_path(); c.set_line_width(40); c.set_source_rgba(1, 1, 1, 0.25); c.arc(0, 0, 420, 0, 2 * math.pi); c.stroke()
    sweep = (t * 1.5) % 1
    c.set_line_width(40); c.set_source_rgba(*C['sky'], 0.8); c.new_path(); c.arc(0, 0, 420, sweep * 6.28, sweep * 6.28 + 0.8); c.stroke()
    c.restore()
    brain_side(c, W / 2 - 30, 900, s * 0.85, t, clamp((t - s2 - 0.8) / 0.6))
    if t > pain:
        stamp(c, W / 2, 1500, pop(t, pain), 'SAME AREA AS PHYSICAL PAIN', RED, C['white'], 40, 0.03)

def glove(c, x, y, s):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, 60, -70, 200, 140, 30); fill(c, C['white'])
    circle(c, -20, 0, 120, RED); rrect(c, -20, -110, 120, 220, 40); fill(c, RED)
    circle(c, -60, -60, 30, hx('FF6B6B'))
    c.restore()

def scene3(c, t):
    lt = t - s3
    bg(c, 7 if t > punch else 1, t)
    title_pill(c, lt, 0, None, 'LEFT ON READ', C['coral'])
    hit = t > punch + 0.25
    shake = math.sin(t * 60) * 18 * clamp(1 - (t - punch - 0.25) / 0.5) if hit else 0
    chat_phone(c, 380 + shake, 960, 1.0, t, [('so... are we good?', True, s3 - 1)], ('Read 9:41 PM', onread))
    if t > punch:
        k = eo((t - punch) / 0.25)
        glove(c, lerp(W + 300, 780, k), 900, 1.2)
    if hit:
        s = pop(t, punch + 0.25, 0.3)
        c.save(); c.translate(560, 620); S(c, s); c.rotate(-0.1)
        star(c, 0, 0, 170, C['yellow'], 1, 0); text_c(c, 'POW!', 0, 10, 70, RED); c.restore()

def scene4(c, t):
    lt = t - s4
    bg(c, 3, t)
    title_pill(c, lt, 0, None, 'WIRED FOR PEOPLE', C['mint'])
    person(c, W / 2, 1500, 0.8, t=t, face='smile' if t > wired else 'worried', look=0, **YOU)
    stamp(c, W / 2, 560, pop(t, s4 + 0.1), 'NOT OVERREACTING', C['white'], C['ink'], 54, -0.04)
    for k, (x, kw) in enumerate([(200, P2), (880, P3)]):
        e = eo((t - wired - k * 0.2) / 0.6)
        if t > wired:
            person(c, lerp(-150 if k == 0 else W + 150, x, e), 1500, 0.7, t=t + k, face='big', look=14 if k == 0 else -14,
                   flip=k == 1, armR=-1.2, **kw)
    if t > wired + 0.7:
        for k in range(5):
            hh = ((t - wired) * 0.7 + k / 5) % 1
            heart(c, 400 + k * 70 + math.sin(t * 3 + k) * 20, 1000 - hh * 300, 1.1, hx('FF6FA5'), 1 - hh)

def phone11(c, x, y, s, t, sent):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -400, 460, 800, 60); fill(c, C['ink'])
    rrect(c, -205, -370, 410, 740, 40); fill(c, hx('F2F2F7'))
    text_c(c, 'Share to', 0, -310, 40, C['ink'])
    for k, (col, nm) in enumerate([(C['coral'], 'that friend'), (C['mint'], 'bestie'), (C['sky'], 'group chat')]):
        yy = -190 + k * 150
        circle(c, -140, yy, 46, col); text_c(c, nm, 0, yy, 30, C['ink'], bold=False)
        if k == 0:
            bx = 140
            rrect(c, bx - 60, yy - 32, 120, 64, 32); fill(c, (0.85, 0.85, 0.9) if sent else BLUE)
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
        person(c, 0, 360, 0.75, t=t, face='worried', sweat=0.5, **YOU)
        c.restore(); c.restore()
        text_c(c, 'someone who hates', 290, 1160, 38, C['white'], True, clamp((lt - 0.4) / 0.3))
        text_c(c, 'being left on read', 290, 1215, 38, C['yellow'], True, clamp((lt - 0.4) / 0.3))
    sent = lt > 1.4
    phone11(c, 780, 1000, pop(t, s5 + 0.3), t, sent)
    fx = lerp(W + 200, 780 + 140, eio((lt - 0.7) / 0.5)); fy = lerp(1500, 1000 - 190 + 40, eio((lt - 0.7) / 0.5))
    bk = eio((lt - 1.7) / 0.4); fx = lerp(fx, W + 250, bk); fy = lerp(fy, 1700, bk)
    circle(c, fx, fy, 40, C['skin1']); line(c, fx, fy, fx + 60, fy + 240, 80, C['skin1'])
    if lt > 1.7:
        stamp(c, 290, 1360, pop(t, s5 + 1.7), 'Follow @neuronbites', C['sky'], C['white'], 34, 0.0)

SC = [scene0, scene1, scene2, scene3, scene4, scene5]
SCENES = [0, s1, s2, s3, s4, s5, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
