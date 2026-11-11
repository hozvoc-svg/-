import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *
import engine
def S(c, k): k = max(k, 1e-3); c.scale(k, k)

t_of, DUR = load_timing('align.json')
_a = json.load(open('align.json')); _txt = ''.join(_a['characters']); _st = _a['character_start_times_seconds']
def seq(phrases):
    out = []; pos = 0
    for p in phrases:
        k = _txt.find(p, pos); pos = k + 1; out.append(_st[k])
    return out
(s1, q1, e1, say1, s2, q2, e2, say2, s3, q3, e3, say3, s4, fol) = seq(
    ['Number one', '"You', 'It makes', 'Say', 'Number two', '"After', 'It turns', 'Say', 'Number three', '"If', "It's guilt", 'Say', 'Save this', 'Follow'])
engine.BG += [(hx('1E0B2E'), hx('6B1E5F')), (hx('0B2E2A'), hx('1F7A6A'))]

MANI = dict(shirt=hx('3D2B6B'), hair=C['hair1'], hairstyle=0, skin=C['skin1'])
YOU = dict(shirt=C['sky'], skin=C['skin2'], hairstyle=2, hair=C['hair2'])
RED = hx('E63946'); GREEN = C['mint']

def mbubble(c, x, y, w, lines, s, col, tcol, tail='left', size=44, icon=None):
    if s <= 0: return
    lh = size * 1.25; h = len(lines) * lh + 60
    c.save(); c.translate(x, y); S(c, s)
    c.set_source_rgba(0, 0, 0, 0.22); rrect(c, -w / 2 + 8, -h / 2 + 12, w, h, 40); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 40); fill(c, col)
    tx = -w / 4 if tail == 'left' else w / 4
    c.move_to(tx - 26, h / 2 - 2); c.line_to(tx + (-34 if tail == 'left' else 34), h / 2 + 50); c.line_to(tx + 26, h / 2 - 2); c.close_path(); fill(c, col)
    for i, ln in enumerate(lines):
        text_c(c, ln, 0, -h / 2 + 30 + lh * (i + 0.5), size, tcol)
    if icon == 'warn':
        c.save(); c.translate(-w / 2 + 10, -h / 2 + 10)
        c.move_to(0, -44); c.line_to(42, 30); c.line_to(-42, 30); c.close_path(); fill(c, C['yellow'])
        text_c(c, '!', 0, 4, 52, C['ink']); c.restore()
    if icon == 'shield':
        c.save(); c.translate(-w / 2 + 10, -h / 2 + 10)
        c.move_to(0, -44); c.curve_to(30, -34, 40, -34, 40, -30); c.line_to(36, 6); c.curve_to(30, 30, 10, 40, 0, 46)
        c.curve_to(-10, 40, -30, 30, -36, 6); c.line_to(-40, -30); c.curve_to(-40, -34, -30, -34, 0, -44); c.close_path(); fill(c, C['white'])
        c.set_line_width(8); c.set_source_rgb(*GREEN); c.move_to(-16, 0); c.line_to(-4, 14); c.line_to(18, -14); c.stroke(); c.restore()
    c.restore()

def strings(c, hx_, hy_, targets, t, a=0.8):
    c.set_line_width(4); c.set_source_rgba(1, 1, 1, a)
    for (x, y) in targets:
        c.move_to(hx_, hy_); c.curve_to(hx_, (hy_ + y) / 2, x, (hy_ + y) / 2 + math.sin(t * 3) * 20, x, y); c.stroke()

def scene0(c, t):
    bg(c, 6, t)
    title_pill(c, t, 0, None, TITLE0, RED)
    # puppet master hand at top
    hxp = W / 2 + math.sin(t * 2) * 30; hyp = 560
    s = pop(t, 0.2, 0.5)
    c.save(); c.translate(hxp, hyp); S(c, s)
    rrect(c, -110, -40, 220, 70, 35); fill(c, C['skin1'])
    for k in range(4): rrect(c, -95 + k * 52, 10, 36, 80, 18); fill(c, C['skin1'])
    rrect(c, -150, -80, 300, 50, 20); fill(c, MANI['shirt'])
    c.restore()
    bob = math.sin(t * 3) * 0.4
    if s > 0.3:
        strings(c, hxp, hyp + 80, [(W / 2 - 120, 1080 - bob * 60), (W / 2 + 120, 1080 + bob * 60), (W / 2, 830)], t)
    person(c, W / 2, 1460, 0.95, t=t, face='worried', armL=0.9 + bob, armR=-0.9 + bob, **YOU)

def phrase_scene(c, t, bgi, num, title, sStart, q, e, say, phrase, resp, prop):
    bg(c, bgi, t); lt = t - sStart
    defended = t >= say
    title_pill(c, lt, 0, num, title, RED if not defended else GREEN)
    person(c, 260, 1450, 0.9, t=t, face='smile' if not defended else 'o', look=16, armR=-1.0 if (q <= t < e) else -0.15, **MANI)
    shrink = 0.0 if defended else eio((t - q - 0.3) / 0.8) * 0.12
    sc = 0.9 * (1 - shrink) + (0.06 * eio((t - say) / 0.4) if defended else 0)
    person(c, 810, 1450, sc, t=t + 1, face='worried' if not defended else 'smile', look=-16, flip=True,
           sweat=clamp((t - q) / 1.5) if (not defended and t > q) else 0, armR=-1.2 if defended else -0.15, **YOU)
    if t < say:
        mbubble(c, 360, 760, 640, phrase, pop(t, q), (0.12, 0.08, 0.2), C['white'], 'left', 46, 'warn')
    else:
        mbubble(c, 650, 760, 760, resp, pop(t, say), C['white'], C['ink'], 'right', 42, 'shield')
        # shield glow behind "you"
        r = 260 + math.sin(t * 5) * 8; a = 0.25 * eo((t - say) / 0.4)
        c.set_line_width(14); c.set_source_rgba(*GREEN, a + 0.2); c.arc(810, 1210, r, math.pi * 1.05, math.pi * 1.95); c.stroke()
    if e <= t < say:
        prop(c, t, t - e)

def prop_doubt(c, t, lt):
    s = pop(lt, 0)
    c.save(); c.translate(W / 2 + 10, 470); S(c, s)
    rrect(c, -230, -45, 460, 90, 45); fill(c, C['white'], 0.25)
    fw = 460 * (1 - 0.8 * eo(lt / 1.2)); rrect(c, -230, -45, max(fw, 90), 90, 45); fill(c, C['yellow'])
    text_c(c, 'SELF-TRUST', 0, 0, 40, C['ink']); c.restore()
    for k in range(3):
        qs = pop(lt, 0.2 + k * 0.2)
        c.save(); c.translate(720 + k * 70, 860 - k * 40); S(c, qs); text_c(c, '?', 0, 0, 90, C['yellow']); c.restore()

def prop_debt(c, t, lt):
    s = pop(lt, 0)
    c.save(); c.translate(780, 400); S(c, s * 0.8); c.rotate(0.06)
    h = 80 + 300 * eo(lt / 1.5)
    rrect(c, -200, -60, 400, h, 14); fill(c, C['white'])
    text_c(c, 'YOU OWE ME', 0, -20, 40, RED)
    items = ['ride home', 'birthday gift', 'that one favor']
    for k, it in enumerate(items):
        if 30 + k * 80 < h - 60:
            text_c(c, it, -40, 40 + k * 80, 32, C['ink'], False); text_c(c, '$$$', 140, 40 + k * 80, 32, RED)
    c.restore()

def prop_guilt(c, t, lt):
    s = pop(lt, 0)
    c.save(); c.translate(W / 2, 560); S(c, s)
    heart(c, 0, 0, 2.8, C['pink'])
    c.set_line_width(14); c.set_source_rgb(*C['ink'])
    for k in range(5):
        x = -150 + k * 75; y = -20 + (k % 2) * 30
        c.save(); c.translate(x, y); c.scale(1, 0.6); c.arc(0, 0, 34, 0, 2 * math.pi); c.restore(); c.stroke()
    c.restore()
    s2 = pop(lt, 0.6)
    c.save(); c.translate(W / 2 + 230, 420); c.rotate(0.12); S(c, s2)
    rrect(c, -130, -48, 260, 96, 48); fill(c, RED); text_c(c, 'GUILT', 0, 0, 48, C['white']); c.restore()

def scene1(c, t): phrase_scene(c, t, 2, '1', "YOU'RE OVERREACTING", s1, q1, e1, say1,
                               ['"You\'re', 'overreacting."'], ['"My feelings are valid,', 'even if you don\'t', 'share them."'], prop_doubt)
def scene2(c, t): phrase_scene(c, t, 0, '2', 'AFTER ALL I DID FOR YOU', s2, q2, e2, say2,
                               ['"After everything', 'I\'ve done for you."'], ['"I appreciate it,', 'but that doesn\'t mean', 'I owe you this."'], prop_debt)
def scene3(c, t): phrase_scene(c, t, 4, '3', 'IF YOU REALLY LOVED ME', s3, q3, e3, say3,
                               ['"If you really', 'loved me, you would."'], ['"I do care.', 'And my answer', 'is still no."'], prop_guilt)

def scene4(c, t):
    bg(c, 7, t); lt = t - s4
    s = pop(lt, 0, 0.5)
    c.save(); c.translate(W / 2, 640); S(c, s)
    pressed = lt > 0.9
    c.move_to(-110, -150); c.line_to(110, -150); c.line_to(110, 150); c.line_to(0, 70); c.line_to(-110, 150); c.close_path()
    fill(c, C['yellow'] if pressed else C['white'])
    if not pressed:
        c.move_to(-80, -120); c.line_to(80, -120); c.line_to(80, 95); c.line_to(0, 35); c.line_to(-80, 95); c.close_path(); fill(c, (0.1, 0.3, 0.28))
    c.restore()
    if pressed:
        sp = pop(lt, 0.9); c.save(); c.translate(W / 2, 880); S(c, sp); text_c(c, 'SAVED', 0, 0, 70, C['white']); c.restore()
        for k in range(10):
            ang = k * math.pi / 5; r = 180 + (lt - 0.9) * 300
            star(c, W / 2 + math.cos(ang) * r, 640 + math.sin(ang) * r, 18, C['yellow'], clamp(1.5 - (lt - 0.9)), t * 3)
    f = fol - s4
    s2 = pop(lt, f); tapped = lt > f + 0.9
    if s2 > 0:
        c.save(); c.translate(W / 2, 1180); S(c, s2)
        rrect(c, -280, -75, 560, 150, 75); fill(c, (0.92, 0.92, 0.95) if tapped else C['sky'])
        text_c(c, 'Following' if tapped else 'Follow @neuronbites', 0, 0, 54 if tapped else 44, C['ink'] if tapped else C['white'])
        c.restore()
        fx = lerp(W / 2 + 420, W / 2 + 80, eio((lt - f - 0.2) / 0.5)); fy = lerp(1600, 1210, eio((lt - f - 0.2) / 0.5))
        bk = eio((lt - f - 1.2) / 0.4); fx = lerp(fx, W + 200, bk); fy = lerp(fy, 1900, bk)
        circle(c, fx, fy, 46, C['skin1']); line(c, fx, fy, fx + 70, fy + 260, 92, C['skin1'])
    if tapped:
        sp = pop(lt, f + 1.0)
        c.save(); c.translate(W / 2 + 280, 1390); c.rotate(0.12); S(c, sp)
        rrect(c, -150, -60, 300, 120, 60); fill(c, C['yellow']); text_c(c, PART_LABEL, 0, 0, 56, C['ink']); c.restore()

PART_LABEL = 'PART 2'
TITLE0 = '3 PHRASES MANIPULATORS USE'
SC = [scene0, scene1, scene2, scene3, scene4]
SCENES = [0, s1, s2, s3, s4, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
