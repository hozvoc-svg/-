import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '..', 'reel03'))
from engine import *
import engine
import cartoon3 as k3   # reuse characters/bubbles/props from part 1
from cartoon3 import S, mbubble, MANI, YOU, RED, GREEN, phrase_scene, strings, prop_guilt

engine.chunks.clear()
t_of, DUR = load_timing('align.json')
_a = json.load(open('align.json')); _txt = ''.join(_a['characters']); _st = _a['character_start_times_seconds']
def seq(phrases):
    out = []; pos = 0
    for p in phrases:
        k = _txt.find(p, pos); pos = k + 1; out.append(_st[k])
    return out
(n3, q1, say1, q2, say2, q3, iso, say3, fol) = seq(['Number three', '"I was', 'Say', '"You', 'Say', '"Nobody', 'This one', 'Say', 'Follow'])

def counter(c, t, k):
    s = pop(t, 0.0, 0.3)
    c.save(); c.translate(W - 130, 420); S(c, s)
    circle(c, 0, 0, 70, C['yellow']); text_c(c, f'{k}/3', 0, 0, 48, C['ink']); c.restore()

def scene0(c, t):
    k3.TITLE0 = '3 MORE PHRASES'
    k3.scene0(c, t)
    s = pop(t, 0.1)
    c.save(); c.translate(870, 400); S(c, s); c.rotate(0.12)
    rrect(c, -150, -55, 300, 110, 55); fill(c, C['yellow']); text_c(c, 'PART 2', 0, 0, 56, C['ink']); c.restore()
    if t > n3:
        s2 = pop(t, n3)
        c.save(); c.translate(W / 2, 760); S(c, s2); c.rotate(-0.04)
        rrect(c, -330, -60, 660, 120, 60); fill(c, RED); text_c(c, '#3 IS THE MOST DANGEROUS', 0, 0, 40, C['white']); c.restore()

def none_prop(c, t, lt): pass

def prop_isolate(c, t, lt):
    # friends fading away behind "you"
    for k, x in enumerate([640, 760, 900, 1010]):
        a = clamp(1 - lt * 0.9 - k * 0.1)
        if a > 0:
            c.save(); c.push_group(); person(c, x + lt * 80, 1300, 0.45, [C['mint'], C['yellow'], C['pink'], C['coral']][k], t + k, face='smile', flip=True, hairstyle=k % 3)
            c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
    s = pop(lt, 0.3)
    c.save(); c.translate(W / 2, 470); S(c, s); c.rotate(-0.05)
    rrect(c, -220, -55, 440, 110, 55); fill(c, RED); text_c(c, 'ISOLATION', 0, 0, 52, C['white']); c.restore()

def wrap(n, bgi, title, q, e, say, phrase, resp, prop):
    def f(c, t):
        phrase_scene(c, t, bgi, str(n), title, q, q, e, say, phrase, resp, prop)
        counter(c, t - q, n)
    return f

scene1 = wrap(1, 2, 'I WAS JUST JOKING', q1, say1, say1, ['"I was', 'just joking."'], ['"It didn\'t feel', 'like a joke to me."'], none_prop)
scene2 = wrap(2, 0, "YOU'RE TOO SENSITIVE", q2, say2, say2, ['"You\'re too', 'sensitive."'], ['"My feelings aren\'t', 'the problem.', 'Your words were."'], none_prop)
scene3 = wrap(3, 4, 'NOBODY ELSE WOULD...', q3, iso, say3, ['"Nobody else would', 'put up with you."'], ['"I\'d rather be alone', 'than be treated', 'like this."'], prop_isolate)

def scene4(c, t):
    k3.s4 = fol; k3.fol = fol + 0.3; k3.PART_LABEL = 'PART 3'
    k3.scene4(c, t)

SC = [scene0, scene1, scene2, scene3, scene4]
SCENES = [0, q1, q2, q3, fol, DUR + 1]

if __name__ == '__main__':
    run(SCENES, SC, DUR, preview=sys.argv[1:] or None)
    if len(sys.argv) == 1: print('dur', DUR)
