import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel07'))
from engine import *
import engine
import cartoon7 as k7          # reuse stamp / speech / phone / bg presets from reel 7
from cartoon7 import S, stamp, speech, RED
os.chdir(HERE)

t_of, DUR = load_timing('align.json')
call = t_of('Then they'); fight = t_of('and you start'); why = t_of('Why?')
s1 = t_of('You saved'); distracted = t_of('but they'); hears = t_of('And your'); idm = t_of("I don")
s2 = t_of('Psychologists'); anger = t_of('The anger'); bid = t_of("It's a")
s3 = t_of('So instead'); tryit = t_of('try:'); missed = t_of('I missed')
s4 = t_of('Send this')

YOU = dict(shirt=C['pink'], skin=C['skin1'], hairstyle=2)
THEM = dict(shirt=C['sky'], skin=C['skin2'], hairstyle=1)

# ---------- pieces ----------
def room(c, x0, w, col_wall, t):
    rrect(c, x0, 0, w, H, 0); fill(c, col_wall)
    rrect(c, x0, 1380, w, H - 1380, 0); fill(c, (0, 0, 0), 0.18)

def desk(c, x, y):
    rrect(c, x - 200, y - 20, 400, 36, 10); fill(c, hx('8A5A3C'))
    line(c, x - 170, y, x - 170, y + 330, 18, hx('6B4430')); line(c, x + 170, y, x + 170, y + 330, 18, hx('6B4430'))

def laptop(c, x, y, s=1.0, glow=True):
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -120, -150, 240, 150, 14); fill(c, hx('2B2B3A'))
    rrect(c, -105, -138, 210, 126, 8); fill(c, hx('9FE3FF') if glow else hx('44445A'))
    rrect(c, -140, 0, 280, 20, 8); fill(c, hx('3A3A4A'))
    c.restore()

def hand_phone(c, x, y, s, ringing=0.0, t=0):
    c.save(); c.translate(x, y); S(c, s)
    if ringing > 0: c.rotate(math.sin(t * 40) * 0.12 * ringing)
    rrect(c, -50, -90, 100, 180, 18); fill(c, C['ink']); rrect(c, -40, -78, 80, 156, 10); fill(c, hx('3DDC97') if ringing else hx('15152A'))
    if ringing:
        for k in range(2):
            c.set_line_width(7); c.set_source_rgba(1, 1, 1, 0.8)
            c.arc(0, 0, 90 + k * 30 + (t * 60) % 30, -0.6, 0.6); c.stroke()
            c.arc(0, 0, 90 + k * 30 + (t * 60) % 30, math.pi - 0.6, math.pi + 0.6); c.stroke()
    c.restore()

def heart_pulse(c, x, y, s, t, col=None):
    if s <= 0: return
    k = 1 + 0.12 * math.sin(t * 6)
    heart(c, x, y, 5.0 * s * k, col or hx('FF3D7F'))

def split_bg(c, t):
    room(c, 0, W / 2, hx('3A2A6E'), t); room(c, W / 2, W / 2, hx('1F3B6B'), t)
    line(c, W / 2, 0, W / 2, H, 10, C['white'], 0.6)

# ---------- scenes ----------
def scene0(c, t):
    split_bg(c, t)
    title_pill(c, t, 0, None, 'MISS THEM... THEN FIGHT?', RED)
    # you: hugging phone, missing them
    ringing = 1.0 if call <= t < fight else 0.0
    face = 'smile' if t < call else ('big' if t < fight else 'worried')
    person(c, 270, 1500, 0.85, t=t, face=face, look=10, armR=-0.9, **YOU)
    hand_phone(c, 205, 1290, 0.75, ringing, t)
    if t < call:
        for k in range(3):
            hh = (t * 0.8 + k / 3) % 1
            heart(c, 200 + k * 60 + math.sin(t * 3 + k) * 20, 900 - hh * 300, 1.6, hx('FF6FA5'), 1 - hh)
        stamp(c, 270, 520, pop(t, 0.3), 'ALL DAY', C['white'], C['ink'], 40, -0.05)
    # them at laptop
    desk(c, 760, 1170)
    person(c, 900, 1500, 0.85, t=t + 1, face='flat', look=-10, flip=True, **THEM)
    laptop(c, 665, 1165, 0.8)
    if t >= fight:
        speech(c, 290, 640, pop(t, fight, 0.3), 'YOU NEVER CALL!', RED, size=40, tail='left')
        speech(c, 800, 820, pop(t, fight + 0.7, 0.3), 'WHAT?!', C['white'], C['ink'], 44, 'right')
    if t >= why:
        stamp(c, W / 2, 470, pop(t, why), 'WHY?', C['yellow'], C['ink'], 80, 0.05)

def story_icon(c, x, y, s, kind, t):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    circle(c, 0, 0, 70, C['white'])
    if kind == 0:  # cat
        circle(c, 0, 10, 36, hx('F4A261')); c.move_to(-34, -6); c.line_to(-26, -46); c.line_to(-8, -20); fill(c, hx('F4A261'))
        c.move_to(34, -6); c.line_to(26, -46); c.line_to(8, -20); fill(c, hx('F4A261'))
        circle(c, -12, 6, 5, C['ink']); circle(c, 12, 6, 5, C['ink'])
    elif kind == 1:  # coffee
        rrect(c, -30, -20, 50, 56, 10); fill(c, hx('6B4430')); c.set_line_width(8); c.set_source_rgb(*hx('6B4430'))
        c.arc(24, 8, 16, -1.4, 1.4); c.stroke()
        for k in range(2): line(c, -14 + k * 20, -34, -10 + k * 20, -54, 6, C['ink'], 0.4)
    else:  # star = good news
        star(c, 0, 0, 44, C['yellow'], 1, t)
    c.restore()

def scene1(c, t):
    lt = t - s1
    split_bg(c, t)
    title_pill(c, lt, 0, None, 'YOUR STORIES', C['violet'])
    person(c, 270, 1500, 0.85, t=t, face='big' if t < distracted else 'worried', look=10, armR=-2.4 if t < distracted else -0.2, **YOU)
    for k in range(3):
        story_icon(c, 120 + k * 150, 700 + 40 * math.sin(t * 2 + k), pop(t, s1 + 0.2 + k * 0.25), k, t)
    desk(c, 760, 1170)
    person(c, 900, 1500, 0.85, t=t + 1, face='flat', look=24, flip=True, **THEM)
    laptop(c, 665, 1165, 0.8)
    if t >= distracted:
        speech(c, 830, 820, pop(t, distracted + 0.1, 0.3), 'mhm...', C['white'], C['ink'], 44, 'right')
        for k in range(3):  # typing dots
            circle(c, 760 + k * 40, 940, 9, C['white'], 0.5 + 0.5 * math.sin(t * 8 + k))
    if t >= hears:
        stamp(c, W / 2, 470, pop(t, idm), '"I DON\'T MATTER"', RED, C['white'], 52, -0.04)

def scene2(c, t):
    lt = t - s2
    bg(c, 4, t)
    title_pill(c, lt, 0, None, 'PROTEST BEHAVIOR', C['yellow'])
    person(c, W / 2, 1520, 0.8, t=t, face='worried' if t < bid else 'smile', look=0, **YOU)
    # angry red cloud that cracks open into a heart
    open_ = eio((t - bid) / 0.6)
    cx, cy = W / 2, 720
    s = pop(t, s2 + 0.2)
    if s > 0 and open_ < 1:
        c.save(); c.translate(cx, cy); S(c, s)
        for side in (-1, 1):
            c.save(); c.translate(side * open_ * 260, open_ * 80); c.rotate(side * open_ * 0.4)
            c.rectangle(0 if side > 0 else -400, -300, 400, 600); c.clip()
            for (bx, by, r) in [(-120, -20, 120), (20, -80, 130), (140, 0, 120), (-30, 70, 120), (-160, 70, 90), (150, 80, 90)]:
                circle(c, bx, by, r, RED)
            if t < anger + 0.6 or True:
                text_c(c, 'ANGER', 0, 0, 80, C['white'])
            c.restore()
        # crack line
        if t > anger:
            c.set_line_width(10); c.set_source_rgb(*C['ink'])
            c.move_to(0, -200); c.line_to(-20, -100); c.line_to(25, -20); c.line_to(-15, 60); c.line_to(10, 180)
            c.stroke() if open_ < 0.05 else c.new_path()
        c.restore()
    if t >= bid:
        heart_pulse(c, cx, cy + 20, pop(t, bid + 0.1, 0.5), t)
        text_c(c, 'MISS', cx, cy - 30, 80, C['white'], True, clamp((t - bid - 0.3) / 0.3))
        text_c(c, 'YOU', cx, cy + 55, 80, C['white'], True, clamp((t - bid - 0.3) / 0.3))
        stamp(c, W / 2, 1000, pop(t, bid + 0.5), 'A BID FOR CONNECTION', C['mint'], C['ink'], 44, 0.03)

def scene3(c, t):
    lt = t - s3
    bg(c, 3, t)
    title_pill(c, lt, 0, None, 'TRY THIS INSTEAD', C['mint'])
    happy = t >= missed + 0.8
    person(c, 300, 1450, 0.66, t=t, face='smile' if t >= tryit else 'flat', look=12, **YOU)
    desk(c, 760, 1220)
    person(c, 900, 1450, 0.66, t=t + 1, face='big' if happy else 'flat', look=-14, flip=True,
           armL=2.5 if happy else 0.15, **THEM)
    laptop(c, 700 + (eo((t - missed - 0.4) / 0.5) * 420 if t > missed else 0), 1215, 0.75, glow=not happy)
    # bad line, crossed out
    s = pop(t, s3 + 0.2)
    if s > 0:
        c.save(); c.translate(W / 2, 560); S(c, s)
        rrect(c, -340, -60, 680, 120, 50); fill(c, C['ink'], 0.85)
        text_c(c, '"You never listen."', 0, 0, 48, C['white'])
        if t > tryit:
            k = eo((t - tryit) / 0.3)
            line(c, -300, 0, -300 + 600 * k, 0, 12, RED)
        c.restore()
    if t >= missed:
        speech(c, W / 2, 790, pop(t, missed, 0.35), '"I missed you. 5 minutes?"', C['yellow'], C['ink'], 42, 'left', w=760)
    if happy:
        for k in range(5):
            hh = ((t - missed) * 0.7 + k / 5) % 1
            heart(c, 450 + k * 50 + math.sin(t * 3 + k) * 20, 1050 - hh * 280, 0.9, hx('FF6FA5'), 1 - hh)

def scene4(c, t):
    lt = t - s4
    bg(c, 0, t)
    title_pill(c, lt, 0, None, 'SEND THIS TO...', C['coral'])
    heart_pulse(c, 280, 760, pop(t, s4 + 0.1) * 0.6, t)
    text_c(c, 'the person', 280, 960, 44, C['white'], True, clamp((lt - 0.3) / 0.3))
    text_c(c, 'you miss most', 280, 1015, 44, C['yellow'], True, clamp((lt - 0.3) / 0.3))
    sent = lt > 1.6
    phone8(c, 760, 1050, pop(t, s4 + 0.3), t, sent)
    fx = lerp(W + 200, 760 + 140, eio((lt - 0.8) / 0.5)); fy = lerp(1500, 1050 - 190 + 40, eio((lt - 0.8) / 0.5))
    bk = eio((lt - 1.9) / 0.4); fx = lerp(fx, W + 250, bk); fy = lerp(fy, 1700, bk)
    circle(c, fx, fy, 40, C['skin1']); line(c, fx, fy, fx + 60, fy + 240, 80, C['skin1'])
    if lt > 1.9:
        stamp(c, 300, 1250, pop(t, s4 + 1.9), 'Follow @neuronbites', C['sky'], C['white'], 36, 0.0)

def phone8(c, x, y, s, t, sent):
    if s <= 0: return
    c.save(); c.translate(x, y); S(c, s)
    rrect(c, -230, -400, 460, 800, 60); fill(c, C['ink'])
    rrect(c, -205, -370, 410, 740, 40); fill(c, hx('F2F2F7'))
    text_c(c, 'Share to', 0, -310, 40, C['ink'])
    for k, (col, nm) in enumerate([(C['pink'], 'my person'), (C['mint'], 'bestie'), (C['sky'], 'mom')]):
        yy = -190 + k * 150
        circle(c, -130, yy, 50, col); text_c(c, nm, -10, yy, 32, C['ink'], bold=False)
        if k == 0:
            bx = 140
            rrect(c, bx - 60, yy - 32, 120, 64, 32); fill(c, (0.85, 0.85, 0.9) if sent else hx('0095F6'))
            text_c(c, 'Sent' if sent else 'Send', bx, yy, 30, C['ink'] if sent else C['white'])
    c.restore()

SC = [scene0, scene1, scene2, scene3, scene4]
SCENES = [0, s1, s2, s3, s4, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
