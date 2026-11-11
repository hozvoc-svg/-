import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *
import engine
def S(c, k): k = max(k, 1e-3); c.scale(k, k)

t_of, DUR = load_timing('align.json')
why = t_of("Here's why"); s1 = t_of('Every swipe'); never = t_of('You never'); boring = t_of('boring'); amazing = t_of('amazing')
s2 = t_of('That uncertainty'); notr = t_of('Not the'); antic = t_of('The anticipation')
s3 = t_of('And the feed'); nolast = t_of("There's no"); s4 = t_of('Want to'); fric = t_of('Add friction'); move = t_of('Move the')
habit = t_of('and the habit'); s5 = t_of('But first'); thisis = t_of('This is')
engine.BG += [(hx('0D1B2A'), hx('1B4965')), (hx('3C0D0D'), hx('9E2A2B'))]
YOU = dict(shirt=C['violet'], skin=C['skin1'], hairstyle=0, hair=C['hair2'])
CARD = [C['coral'], C['mint'], C['yellow'], C['sky'], C['pink'], C['violet']]

def feed(c, x, y, w, h, off, t):
    """phone screen at (x,y) top-left with scrolling cards"""
    c.save(); rrect(c, x, y, w, h, 30); c.clip()
    rrect(c, x, y, w, h, 30); fill(c, hx('101020'))
    ch = h * 0.62; gap = 24
    k0 = int(off // (ch + gap))
    for k in range(k0 - 1, k0 + 3):
        cy = y + k * (ch + gap) - off + 20
        rrect(c, x + 20, cy, w - 40, ch, 24); fill(c, CARD[k % 6])
        circle(c, x + w / 2, cy + ch * 0.42, ch * 0.16, C['white'], 0.85)
        c.move_to(x + w / 2 - ch * 0.05, cy + ch * 0.42 - ch * 0.08); c.line_to(x + w / 2 + ch * 0.08, cy + ch * 0.42); c.line_to(x + w / 2 - ch * 0.05, cy + ch * 0.42 + ch * 0.08); c.close_path(); fill(c, CARD[k % 6])
        rrect(c, x + 50, cy + ch - 70, (w - 100) * 0.7, 20, 10); fill(c, C['white'], 0.7)
        rrect(c, x + 50, cy + ch - 40, (w - 100) * 0.45, 16, 8); fill(c, C['white'], 0.5)
    c.restore()

def phone(c, cx, cy, w, h, off, t):
    rrect(c, cx - w / 2 - 18, cy - h / 2 - 18, w + 36, h + 36, 56); fill(c, C['ink'])
    feed(c, cx - w / 2, cy - h / 2, w, h, off, t)
    rrect(c, cx - 50, cy - h / 2 - 8, 100, 14, 7); fill(c, C['ink'])

def thumb(c, x, y, swipe):
    yy = y - swipe * 160
    circle(c, x, yy, 44, C['skin1']); line(c, x, yy, x + 60, yy + 240, 88, C['skin1'])

def scroll_off(t, speed=1.0):
    # swipe every 0.8s with ease
    n = t * speed / 0.8; base = math.floor(n); f = n - base
    return (base + eio(f / 0.5)) * 700

def scene0(c, t):
    bg(c, 0, t)
    off = scroll_off(t)
    phone(c, W / 2, 920, 520, 900, off, t)
    sw = ((t / 0.8) % 1); thumb(c, W / 2 + 120, 1250, eio(sw / 0.5) if sw < 0.5 else 1 - eio((sw - 0.5) / 0.3))
    s = pop(t, 0.2)
    c.save(); c.translate(W / 2, 330); S(c, s); c.rotate(-0.04)
    rrect(c, -260, -60, 520, 120, 60); fill(c, C['yellow']); text_c(c, 'YOU, RIGHT NOW', 0, 0, 54, C['ink']); c.restore()
    if t > why:
        s2_ = pop(t, why)
        c.save(); c.translate(870, 600); S(c, s2_); c.rotate(0.15)
        circle(c, 0, 0, 90, hx('E63946')); text_c(c, '?!', 0, 0, 80, C['white']); c.restore()

def symbol(c, kind, x, y, r):
    if kind == 0:  # meh face
        circle(c, x, y, r, (0.75, 0.75, 0.8)); circle(c, x - r * 0.35, y - r * 0.15, r * 0.12, C['ink']); circle(c, x + r * 0.35, y - r * 0.15, r * 0.12, C['ink'])
        line(c, x - r * 0.35, y + r * 0.35, x + r * 0.35, y + r * 0.35, r * 0.12, C['ink'])
    elif kind == 1: star(c, x, y, r * 1.1, C['yellow'])
    elif kind == 2: heart(c, x, y + r * 0.1, r / 40, C['pink'])
    else:
        c.save(); c.translate(x, y + r * 0.3); c.move_to(0, -r * 1.2); c.curve_to(r, -r * 0.4, r * 0.8, r * 0.5, 0, r * 0.6); c.curve_to(-r * 0.8, r * 0.5, -r, -r * 0.4, 0, -r * 1.2); fill(c, hx('FF6B1A')); c.restore()

def slot(c, cx, cy, t, results, stops):
    rrect(c, cx - 380, cy - 300, 760, 600, 60); fill(c, hx('E63946'))
    rrect(c, cx - 300, cy - 360, 600, 120, 40); fill(c, C['yellow']); text_c(c, 'NEXT VIDEO', cx, cy - 300, 50, C['ink'])
    for i in range(3):
        wx = cx - 330 + i * 225; wy = cy - 180
        rrect(c, wx, wy, 210, 300, 24); fill(c, C['white'])
        c.save(); rrect(c, wx, wy, 210, 300, 24); c.clip()
        if t < stops[i]:
            off = (t * 2400 + i * 300) % 400
            for k in range(-1, 3): symbol(c, (k + i + int(t * 6)) % 4, wx + 105, wy + 150 + k * 200 - off + 200, 60)
        else:
            bounce = (1 - eo((t - stops[i]) / 0.3)) * 30
            symbol(c, results[i], wx + 105, wy + 150 + bounce, 70)
        c.restore()
    # lever
    pull = 1.0 if (t % 2.2) < 0.3 else 0.0
    line(c, cx + 400, cy - 40, cx + 470, cy - 220 + pull * 200, 22, (0.7, 0.7, 0.75)); circle(c, cx + 470, cy - 220 + pull * 200, 44, C['yellow'])

def scene1(c, t):
    bg(c, 2, t); lt = t - s1
    title_pill(c, lt, 0, None, 'A SLOT MACHINE', C['coral'])
    if t < boring + 0.4:
        res = [0, 0, 0]; stops = [boring - 0.5, boring - 0.25, boring]
        slot(c, W / 2, 900, t, res, stops)
        if t > boring:
            s = pop(t, boring); c.save(); c.translate(W / 2, 1320); S(c, s); rrect(c, -170, -50, 340, 100, 50); fill(c, (0.6, 0.6, 0.65)); text_c(c, 'BORING', 0, 0, 52, C['white']); c.restore()
    else:
        res = [1, 1, 1]; stops = [amazing - 0.3, amazing - 0.15, amazing]
        slot(c, W / 2, 900, t, res, stops)
        if t > amazing:
            s = pop(t, amazing); c.save(); c.translate(W / 2, 1320); S(c, s); c.rotate(-0.05)
            rrect(c, -230, -60, 460, 120, 60); fill(c, C['yellow']); text_c(c, 'JACKPOT!', 0, 0, 62, C['ink']); c.restore()
            for k in range(14):
                ang = k * math.pi / 7; r = 300 + (t - amazing) * 500
                star(c, W / 2 + math.cos(ang) * r, 900 + math.sin(ang) * r, 24, C['yellow'], clamp(1.2 - (t - amazing)), t * 4)

def brain(c, x, y, s, glow=0.0):
    c.save(); c.translate(x, y); S(c, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 330); g.add_color_stop_rgba(0, 1, 0.85, 0.3, 0.6 * glow); g.add_color_stop_rgba(1, 1, 0.85, 0.3, 0)
        c.set_source(g); c.arc(0, 0, 330, 0, 2 * math.pi); c.fill()
    for (bx, by, r) in [(-70, -10, 85), (40, -50, 90), (90, 30, 75), (-20, 50, 80), (-100, 50, 60)]: circle(c, bx, by, r, C['pink'])
    for k in range(4):
        c.new_sub_path(); c.set_line_width(10); c.set_source_rgba(1, 1, 1, 0.55); c.arc(-60 + k * 45, -10 + (k % 2) * 30, 30, 0.2, 2.6); c.stroke()
    c.restore()

def scene2(c, t):
    bg(c, 1, t); lt = t - s2
    title_pill(c, lt, 0, None, 'DOPAMINE', C['sky'])
    spin = (lt % 1.6) < 1.1
    brain(c, W / 2, 700, 1.25, glow=0.6 + 0.4 * math.sin(t * 6) if t < notr else 0.0)
    # drops
    if t < notr:
        for k in range(6):
            dt = (lt * 1.4 + k / 6) % 1.0
            x = W / 2 - 250 + k * 100; y = 330 + dt * 300
            c.save(); c.translate(x, y); c.move_to(0, -30); c.curve_to(22, -5, 22, 20, 0, 24); c.curve_to(-22, 20, -22, -5, 0, -30); fill(c, C['sky'], 1 - dt); c.restore()
        s = pop(t, s2 + 0.8)
        c.save(); c.translate(W / 2, 1060); S(c, s); rrect(c, -260, -55, 520, 110, 55); fill(c, C['white'])
        text_c(c, '?  ?  ?  UNCERTAINTY', 0, 0, 40, C['ink']); c.restore()
    else:
        # bars: reward vs anticipation
        base = 1440
        for i, (lbl, val, t0, col) in enumerate([('REWARD', 0.3, notr + 0.2, (0.6, 0.6, 0.7)), ('ANTICIPATION', 1.0, antic, C['yellow'])]):
            hgt = 420 * val * eo((t - t0) / 0.8) if t > t0 else 0
            x = W / 2 - 230 + i * 300
            rrect(c, x - 90, base - hgt - 1, 180, hgt + 1, 24); fill(c, col)
            if t > t0: text_c(c, lbl, x + (30 if i else 0), base + 50, 40 if i else 44, C['white'])
        if t > antic + 0.6:
            star(c, W / 2 + 70, base - 480, 40, C['yellow'], 1, t * 2)

def scene3(c, t):
    bg(c, 6, t); lt = t - s3
    title_pill(c, lt, 0, None, 'THE FEED NEVER ENDS', C['mint'])
    off = lt * 1600
    phone(c, W / 2, 900, 560, 980, off, t)
    # scrollbar that never reaches the end
    sb = 0.2 + 0.6 * (1 - math.exp(-lt * 0.6))
    rrect(c, W / 2 + 320, 440, 14, 920, 7); fill(c, C['white'], 0.2); rrect(c, W / 2 + 320, 440 + sb * 700, 14, 120, 7); fill(c, C['white'])
    if t > nolast:
        s = pop(t, nolast)
        c.save(); c.translate(W / 2, 1450); S(c, s); c.rotate(0.04)
        rrect(c, -280, -60, 560, 120, 60); fill(c, hx('E63946')); text_c(c, 'NO LAST PAGE', 0, 0, 56, C['white']); c.restore()
        # stop signal crossed out
        s2_ = pop(t, nolast + 0.7)
        c.save(); c.translate(165, 1150); S(c, s2_ * 0.8)
        c.move_to(-70, -170);
        pts = [(math.cos(math.pi / 8 + k * math.pi / 4) * 90, math.sin(math.pi / 8 + k * math.pi / 4) * 90) for k in range(8)]
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fill(c, hx('E63946'))
        text_c(c, 'STOP', 0, 0, 38, C['white']); line(c, -90, 90, 90, -90, 16, C['ink']); c.restore()

def home(c, cx, cy, t, drag):
    rrect(c, cx - 300, cy - 520, 600, 1040, 60); fill(c, C['ink'])
    g = cairo.LinearGradient(0, cy - 500, 0, cy + 500); g.add_color_stop_rgb(0, *hx('7B5CFF')); g.add_color_stop_rgb(1, *hx('F72585'))
    rrect(c, cx - 282, cy - 502, 564, 1004, 46); c.set_source(g); c.fill()
    cols = [C['mint'], C['yellow'], C['sky'], C['coral'], C['white'], C['violet'], C['mint'], C['yellow'], C['sky'], C['coral'], C['white'], C['violet']]
    for k in range(12):
        x = cx - 210 + (k % 4) * 140; y = cy - 400 + (k // 4) * 160
        rrect(c, x - 50, y - 50, 100, 100, 26); fill(c, cols[k], 0.9)
    # the target app (pink with play) at slot 5 position
    ax = cx - 210 + 1 * 140; ay = cy - 400 + 1 * 160
    px = lerp(ax, cx + 520, eio(drag)); py = lerp(ay, ay + 200, eio(drag)) - math.sin(drag * math.pi) * 120
    c.save(); c.translate(px, py); S(c, 1 + 0.15 * math.sin(drag * math.pi))
    rrect(c, -58, -58, 116, 116, 30); fill(c, hx('FF2D55'))
    c.move_to(-16, -26); c.line_to(28, 0); c.line_to(-16, 26); c.close_path(); fill(c, C['white']); c.restore()
    return px, py

def scene4(c, t):
    bg(c, 3, t); lt = t - s4
    title_pill(c, lt, 0, None, 'ADD FRICTION', C['yellow'])
    drag = clamp((t - move) / 1.4)
    px, py = home(c, W / 2 - 60, 960, t, drag)
    if 0 < drag < 1:
        circle(c, px + 30, py + 40, 40, C['skin1'], 0.95); line(c, px + 30, py + 40, px + 90, py + 260, 80, C['skin1'], 0.95)
    if t > fric:
        s = pop(t, fric)
        c.save(); c.translate(860, 520); S(c, s); c.rotate(0.1)
        for r_ in range(3):
            for k in range(3):
                rrect(c, -150 + k * 100 + (50 if r_ % 2 else 0) - 25, -80 + r_ * 60, 92, 52, 6); fill(c, hx('C0573E'))
        rrect(c, -150, -170, 300, 70, 35); fill(c, C['white']); text_c(c, 'FRICTION', 0, -135, 40, C['ink']); c.restore()
    if t > habit:
        s = pop(t, habit)
        c.save(); c.translate(W / 2, 1560 - 120); S(c, s)
        rrect(c, -300, -45, 600, 90, 45); fill(c, C['white'], 0.25)
        fw = 600 * (1 - 0.75 * eo((t - habit) / 1.2)); rrect(c, -300, -45, max(fw, 90), 90, 45); fill(c, C['mint'])
        text_c(c, 'HABIT', 0, 0, 44, C['ink']); c.restore()

def scene5(c, t):
    bg(c, 5, t); lt = t - s5
    stopped = t > thisis + 0.4
    off = scroll_off(lt, 1.6) if t < thisis else scroll_off(thisis - s5, 1.6)
    c.save(); phone(c, W / 2, 900, 520, 900, off, t); c.restore()
    if stopped:
        s = pop(t, thisis + 0.4)
        c.save(); c.translate(W / 2, 860); S(c, s)
        rrect(c, -230, -260, 460, 520, 30); fill(c, C['white'])
        circle(c, 0, -130, 80, C['violet']); brain(c, 0, -130, 0.35)
        text_c(c, '@neuronbites', 0, 0, 44, C['ink'])
        tapped = lt > (thisis - s5) + 1.4
        rrect(c, -170, 80, 340, 100, 50); fill(c, (0.9, 0.9, 0.93) if tapped else C['sky'])
        text_c(c, 'Following' if tapped else 'Follow', 0, 130, 46, C['ink'] if tapped else C['white']); c.restore()
        s2_ = pop(t, thisis + 0.9)
        c.save(); c.translate(W / 2, 340); S(c, s2_); c.rotate(-0.04)
        rrect(c, -330, -60, 660, 120, 60); fill(c, C['yellow']); text_c(c, 'WORTH STOPPING FOR', 0, 0, 50, C['ink']); c.restore()
        f0 = thisis + 1.0
        fx = lerp(W / 2 + 420, W / 2 + 120, eio((t - f0) / 0.4)); fy = lerp(1600, 1010, eio((t - f0) / 0.4))
        bk = eio((t - f0 - 0.7) / 0.4); fx = lerp(fx, W + 200, bk); fy = lerp(fy, 1900, bk)
        circle(c, fx, fy, 46, C['skin1']); line(c, fx, fy, fx + 70, fy + 260, 92, C['skin1'])
    else:
        sw = ((lt * 1.6 / 0.8) % 1); thumb(c, W / 2 + 120, 1250, eio(sw / 0.5) if sw < 0.5 else 1 - eio((sw - 0.5) / 0.3))

SC = [scene0, scene1, scene2, scene3, scene4, scene5]
SCENES = [0, s1, s2, s3, s4, s5, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
