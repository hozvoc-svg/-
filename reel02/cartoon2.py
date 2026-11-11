import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *
import engine
def S(c, k): k = max(k, 1e-3); c.scale(k, k)

t_of, DUR = load_timing('align.json')
T = dict(s1=t_of('Number one'), rem=t_of('They remember'), s2=t_of('Number two'), even=t_of('even when'),
         s3=t_of('Number three'), lean=t_of('You lean'), laugh=t_of('You laugh'), s4=t_of('Number four'),
         always=t_of('They always'), s5=t_of('Number five'), look=t_of('they look'), s6=t_of('Comment'),
         follow=t_of('And follow'))
engine.BG += [(hx('0B3D2E'), hx('11998E')), (hx('2B1E6B'), hx('C2457E'))]
BGI = [2, 0, 1, 3, 5, 4, 6]  # background per scene

YOU = dict(shirt=C['sky'], skin=C['skin2'], hairstyle=1)
LIKER = dict(shirt=C['coral'], hair=C['hair2'], hairstyle=2)

def leaned(c, x, y, ang, fn):
    c.save(); c.translate(x, y); c.rotate(ang); fn(); c.restore()

def gift(c, x, y, s):
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -55, -50, 110, 100, 12); fill(c, C['pink']); rrect(c, -62, -62, 124, 30, 10); fill(c, C['violet'])
    rrect(c, -10, -62, 20, 112, 4); fill(c, C['yellow'])
    c.set_line_width(10); c.set_source_rgb(*C['yellow']); c.arc(-22, -78, 20, 0, 2 * math.pi); c.stroke(); c.arc(22, -78, 20, 0, 2 * math.pi); c.stroke()
    c.restore()

def scene0(c, t):
    bg(c, BGI[0], t)
    title_pill(c, t, 0, None, '5 SIGNS THEY LIKE YOU', C['pink'])
    s = pop(t, 0.15, 0.5)
    if s > 0:
        b = 1 + 0.08 * math.sin(t * 9)
        heart(c, W / 2, 760, 4.2 * s * b, C['pink'])
        circle(c, W / 2 - 55, 700, 22 * s, C['white']); circle(c, W / 2 + 55, 700, 22 * s, C['white'])
        for k in range(8):
            ang = k * math.pi / 4 + t * 1.2
            heart(c, W / 2 + math.cos(ang) * 330, 760 + math.sin(ang) * 220, 0.7, C['white'], 0.85)
    person(c, 260, 1450, 0.9, t=t, face='smile', look=14, **YOU)
    person(c, 820, 1450, 0.9, t=t + 1, face='big', look=-16, flip=True, blush=True, armR=-2.5, **LIKER)

def scene1(c, t):
    bg(c, BGI[1], t); lt = t - T['s1']
    title_pill(c, lt, 0, '1', 'THEY REMEMBER DETAILS', C['yellow'])
    give = eio((t - T['rem'] - 0.8) / 0.8)
    person(c, 270, 1450, 0.9, t=t, face='big' if give > 0.9 else 'o', look=14, armR=-1.2 if give > 0.9 else -0.15, **YOU)
    person(c, 810, 1450, 0.9, t=t + 1, face='big', look=-16, flip=True, blush=True, armR=-1.3, **LIKER)
    gift(c, lerp(650, 430, give), 1080 - math.sin(give * math.pi) * 90, 1.0)
    bubble(c, 760, 760, 560, 140, pop(t, T['rem'] + 0.1), 'right', 'You said you love mango!', 40)
    s = pop(t, T['s1'] + 0.4)
    if s > 0:  # calendar flipping
        c.save(); c.translate(260, 640); S(c, s); c.rotate(-0.08)
        rrect(c, -120, -120, 240, 240, 24); fill(c, C['white']); rrect(c, -120, -120, 240, 70, 24); fill(c, C['coral'])
        c.rectangle(-120, -80, 240, 30); fill(c, C['coral'])
        day = min(21, 1 + int((t - T['s1']) * 9))
        text_c(c, str(day), 0, 30, 110, C['ink']); text_c(c, 'DAYS AGO' if day >= 21 else 'DAY', 0, -88, 30, C['white'])
        c.restore()

def scene2(c, t):
    bg(c, BGI[2], t); lt = t - T['s2']
    title_pill(c, lt, 0, '2', 'FEET POINT TO YOU', C['mint'])
    away = t >= T['even']
    person(c, 260, 1450, 0.9, t=t, face='smile', look=14, **YOU)
    person(c, 800, 1450, 0.9, t=t + 1, face='flat' if away else 'smile', look=26 if away else -14, blush=True, **LIKER)
    # spotlight on feet
    s = pop(t, T['s2'] + 0.6)
    if s > 0:
        r = 140 + math.sin(t * 6) * 8
        c.set_line_width(12); c.set_source_rgba(*C['yellow'], 0.95); c.save(); c.translate(800, 1440); c.scale(s, 0.45 * s); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.stroke()
        prog = eo((t - T['s2'] - 0.9) / 0.7)
        x2 = lerp(700, 400, prog)
        line(c, 700, 1440, x2, 1440, 22, C['yellow'])
        if prog > 0.1:
            c.move_to(x2 - 40, 1440); c.line_to(x2 + 10, 1395); c.line_to(x2 + 10, 1485); c.close_path(); fill(c, C['yellow'])
    if away:
        bubble(c, 820, 700, 360, 120, pop(t, T['even']), 'right', 'not looking...', 40)
        s2 = pop(t, T['even'] + 0.6)
        if s2 > 0:
            c.save(); c.translate(W / 2, 470); S(c, s2); c.rotate(-0.05)
            rrect(c, -250, -55, 500, 110, 55); fill(c, C['yellow']); text_c(c, "FEET DON'T LIE", 0, 0, 50, C['ink']); c.restore()

def scene3(c, t):
    bg(c, BGI[3], t); lt = t - T['s3']
    title_pill(c, lt, 0, '3', 'THEY MIRROR YOU', C['sky'])
    lean = eio((t - T['lean']) / 0.5) * (1 - eio((t - T['laugh'] + 0.2) / 0.4)) * 0.18
    laughing = t >= T['laugh']
    arm = -2.6 + math.sin(t * 9) * 0.25 if laughing else -0.15
    face = 'big' if laughing else ('smile' if lean > 0.05 else 'smile')
    leaned(c, 290, 1450, lean, lambda: person(c, 0, 0, 0.9, t=t, face=face, look=16, armL=-arm if laughing else 0.15, armR=arm, **YOU))
    leaned(c, 790, 1450, -lean, lambda: person(c, 0, 0, 0.9, t=t, face=face, look=-16, flip=True, blush=True, armL=-arm if laughing else 0.15, armR=arm, **LIKER))
    # mirror line
    c.set_line_width(6); c.set_dash([24, 18]); c.set_source_rgba(1, 1, 1, 0.6); c.move_to(W / 2, 520); c.line_to(W / 2, 1480); c.stroke(); c.set_dash([])
    for k in range(4):
        star(c, W / 2 + math.sin(t * 2 + k) * 20, 600 + k * 230, 22, C['yellow'], 0.9, t * 2 + k)
    if laughing:
        for k, (x, y) in enumerate([(260, 690), (820, 690)]):
            s = pop(t, T['laugh'] + k * 0.15)
            c.save(); c.translate(x, y); S(c, s); c.rotate(-0.1 if k == 0 else 0.1); text_c(c, 'HAHA', 0, 0, 80, C['yellow']); c.restore()

def phone_frame(c):
    rrect(c, 160, 420, 760, 1080, 70); fill(c, C['ink']); rrect(c, 182, 442, 716, 1036, 52); fill(c, (0.96, 0.96, 0.98))
    rrect(c, 182, 442, 716, 120, 52); c.rectangle(182, 500, 716, 62); fill(c, C['white'])
    circle(c, 270, 502, 34, C['coral']); text_c(c, 'her', 350, 502, 36, C['ink'])

def msg(c, s, right, y, txt, col):
    if s <= 0: return
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(38)
    w = c.text_extents(txt).width + 70
    x = 860 - w if right else 220
    c.save(); c.translate(x + w / 2, y); S(c, s)
    rrect(c, -w / 2, -42, w, 84, 38); fill(c, col); text_c(c, txt, 0, 0, 38, C['white'] if right else C['ink']); c.restore()

def scene4(c, t):
    bg(c, BGI[4], t); lt = t - T['s4']
    title_pill(c, lt, 0, '4', 'THEY KEEP IT GOING', C['violet'])
    phone_frame(c)
    msgs = [(0.2, False, 'ok goodnight'), (T['always'] - T['s4'] + 0.1, True, 'wait wait'), (T['always'] - T['s4'] + 0.6, True, 'one more thing'),
            (T['always'] - T['s4'] + 1.1, True, 'did you see this?? haha'), (T['always'] - T['s4'] + 1.7, True, 'also...')]
    for k, (t0, right, txt) in enumerate(msgs):
        msg(c, pop(lt, t0, 0.3), right, 660 + k * 120, txt, C['violet'] if right else (0.86, 0.86, 0.9))
    if lt > T['always'] - T['s4'] + 2.0:  # typing dots
        for k in range(3):
            circle(c, 720 + k * 36, 1270 - abs(math.sin(t * 6 + k)) * 14, 12, C['violet'])
    s = pop(t, T['always'] + 1.3)
    if s > 0:
        c.save(); c.translate(860, 1400); S(c, s); c.rotate(0.2); heart(c, 0, 0, 1.6, C['pink']); c.restore()

def scene5(c, t):
    bg(c, BGI[5], t); lt = t - T['s5']
    title_pill(c, lt, 0, '5', 'THEY LOOK AT YOU FIRST', C['coral'])
    joke = lt > 0.6; turned = t >= T['look']
    person(c, 190, 1450, 0.72, t=t, face='big' if joke else 'smile', look=12, **YOU)
    person(c, 540, 1450, 0.72, C['mint'], t + 0.6, face='big' if joke else 'smile', armL=-2.4 + math.sin(t * 8) * 0.3, armR=2.4, hairstyle=0)
    person(c, 890, 1450, 0.72, t=t + 1.2, face='big' if joke else 'smile', look=-28 if turned else 10, flip=True, blush=turned, **LIKER)
    if joke:
        for k in range(3):
            s = pop(t, T['s5'] + 0.6 + k * 0.2)
            c.save(); c.translate(540 + (k - 1) * 170, 760 - k % 2 * 60); S(c, s); c.rotate((k - 1) * 0.15)
            text_c(c, 'HA', 0, 0, 90, C['yellow']); c.restore()
    if turned:
        prog = eo((t - T['look']) / 0.6)
        x1, y1, x2, y2 = 860, 1100, 250, 1100
        c.set_line_width(10); c.set_dash([22, 16]); c.set_source_rgba(*C['yellow'], 1); c.move_to(x1, y1)
        c.curve_to(lerp(x1, 550, prog), 950, lerp(x1, 400, prog), 950, lerp(x1, x2, prog), y2); c.stroke(); c.set_dash([])
        if prog > 0.95:
            heart(c, 250, 960 - (t - T['look'] - 0.6) * 60, 1.3, C['pink'])

def scene6(c, t):
    bg(c, BGI[6], t); lt = t - T['s6']
    s = pop(lt, 0, 0.5)
    c.save(); c.translate(W / 2, 640); S(c, s)
    rrect(c, -420, -150, 840, 300, 40); fill(c, C['white'])
    text_c(c, 'Comments', -260, -95, 34, C['ink'])
    circle(c, -330, 20, 42, C['coral'])
    name = '@who_came_to_mind'; n = int(clamp((lt - 0.4) / 1.2) * len(name))
    rrect(c, -270, -20, 620, 80, 40); fill(c, (0.94, 0.94, 0.97))
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(40); c.move_to(-240, 33)
    c.set_source_rgb(*C['violet']); c.show_text(name[:n] + ('|' if int(t * 3) % 2 else ''))
    c.restore()
    f = T['follow'] - T['s6']
    s2 = pop(lt, f)
    tapped = lt > f + 0.9
    if s2 > 0:
        c.save(); c.translate(W / 2, 1080); S(c, s2)
        rrect(c, -260, -75, 520, 150, 75); fill(c, (0.92, 0.92, 0.95) if tapped else C['sky'])
        text_c(c, 'Following' if tapped else 'Follow @neuronbites', 0, 0, 44 if not tapped else 54, C['ink'] if tapped else C['white'])
        c.restore()
        fx = lerp(W / 2 + 420, W / 2 + 80, eio((lt - f - 0.2) / 0.5)); fy = lerp(1600, 1110, eio((lt - f - 0.2) / 0.5))
        bk = eio((lt - f - 1.2) / 0.4); fx = lerp(fx, W + 200, bk); fy = lerp(fy, 1900, bk)
        circle(c, fx, fy, 46, C['skin1']); line(c, fx, fy, fx + 70, fy + 260, 92, C['skin1'])
    if tapped:
        sp = pop(lt, f + 1.0)
        c.save(); c.translate(W / 2 + 280, 1300); c.rotate(0.12); S(c, sp)
        rrect(c, -150, -60, 300, 120, 60); fill(c, C['yellow']); text_c(c, 'PART 2', 0, 0, 56, C['ink']); c.restore()
        for k in range(5):
            ht = lt - f - 1.0 - k * 0.15
            if ht > 0: heart(c, W / 2 - 320 + k * 150, 1450 - ht * 300, 1.0, C['pink'], clamp(1.5 - ht))

SC = [scene0, scene1, scene2, scene3, scene4, scene5, scene6]
SCENES = [0, T['s1'], T['s2'], T['s3'], T['s4'], T['s5'], T['s6'], DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR, {k: round(v, 2) for k, v in T.items()})
