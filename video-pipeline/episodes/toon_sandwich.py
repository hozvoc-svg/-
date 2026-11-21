"""Stix & Bolt, episode 1: "The Sandwich" (wordless, ~28 s vertical Short).

Every animation beat sits on the music grid (150 BPM, 1 beat = 0.4 s) and the score/SFX below use the same
beat numbers, so the cartoon is 'mickey-moused': layers land on notes, chomps play the scale backwards, etc.
"""
import math
from toon import *

BPM = 150
B = 60.0 / BPM
BEATS = 70
HOOK = ("HE JUST WANTED", "A SANDWICH")
X1 = 860           # Stix's spot
TX = 335           # sandwich centre
BASE = TABLE["top"]
DROP = [3 + i for i in range(14)]           # layer i lands on this beat
CHOMP = [33 + 0.5 * k for k in range(13)]   # each chomp removes the top layer
SCALE = [72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 96]


def layers_on(b):
    n = sum(1 for d in DROP if b >= d - 0.6)
    n -= sum(1 for ch in CHOMP if b >= ch)
    return max(0, min(14, n))


def tower_top(n):
    return BASE - sum(h for _, h in LAYERS[:n]) * 1.35


def pulse(b, beats, k=6.0):
    """1 at each listed beat, decaying quickly after it."""
    v = 0.0
    for x in beats:
        if b >= x:
            v = max(v, math.exp(-(b - x) * k))
    return v


def stix_state(b, T):
    st = dict(T=T, facing=-1, x=X1)
    if b < 3:                                   # walks in
        st.update(walk(b * math.pi), x=keys([(0, 1250), (3, X1)], b, lambda u: u))
        st.update(eyes="happy", mouth="smile")
    elif b < 17:                                # conducts the falling layers
        p = pulse(b, DROP)
        st.update(aF=(2.35 + 0.3 * p, -0.2), aB=(-0.3, 0.0), dy=-5 * p, eyes="open", look=(0.6, -0.7),
                  mouth="grin" if b > 10 else "smile", tilt=-0.15)
    elif b < 20:                                # ta-da!
        j = math.sin(clamp((b - 17) / 1.2) * math.pi)
        st.update(aF=(2.55, 0.1), aB=(-2.55, -0.1), dy=-40 * j, eyes="happy", mouth="grin",
                  squash=-0.06 * j)
    elif b < 24:                                # ...too tall to bite
        u = clamp((b - 20) / 1.5)
        late = b >= 21.5
        st.update(tilt=-0.38, lean=0.12 * u, look=(0.5, -0.9), eyes="wide" if late else "open",
                  mouth="wavy" if late else "open", mo=keys([(20, 0.2), (21.3, 1.0)], b), brows=-0.4 if late else 0,
                  aF=(0.35, 0.3), aB=(-0.35, 0.3))
    elif b < 25:                                # idea!
        st.update(aF=keys([(24, (0.3, 0.0)), (24.3, (2.9, -0.2))], b), eyes="happy", mouth="grin")
    elif b < 28:                                # off to get a knife
        st.update(walk((b - 25) * math.pi * 1.2), facing=1, x=keys([(25, X1), (28, 1330)], b, lambda u: u),
                  eyes="happy", mouth="smile")
    elif b < 41:
        st["x"] = 2000
    elif b < 45:                                # back, humming, eyes closed
        st.update(walk((b - 41) * math.pi), x=keys([(41, 1320), (45, X1)], b, lambda u: u), eyes="closed",
                  mouth="o", aF=(1.6, -0.9))
    elif b < 47:                                # freeze
        st.update(aF=keys([(45, (1.6, -0.9)), (46.6, (0.7, -0.2))], b), eyes="wide", look=(0.9, 0.0),
                  mouth="open", mo=0.45, squash=-0.03 * pulse(b, [45], 8))
    elif b < 49:                                # ...looks at the dog
        st.update(aF=(0.7, -0.2), eyes="open", look=keys([(47, (0.9, 0.0)), (47.8, (0.8, 0.75))], b),
                  mouth="flat", brows=keys([(47, 0.0), (48.8, 0.6)], b), tilt=0.12)
    elif b < 56:                                # boiling
        r = clamp((b - 49) / 2.5)
        stomp = pulse(b, [50, 51, 52, 52.5], 7)
        st.update(eyes="angry", look=(0.8, 0.7), mouth="grin", red=r, steam=clamp((b - 50.5) / 1.0),
                  shake=r, aF=(0.45, 1.6), aB=(-0.45, 1.6), dy=8 * stomp, squash=0.07 * stomp, tilt=0.1)
    elif b < 58:                                # melts
        u = clamp((b - 56) / 1.4)
        st.update(eyes="sad", look=(0.8, 0.7), mouth="frown", red=1 - u, steam=max(0, 1 - u * 2), lean=0.15 * u,
                  aF=(0.15, 0.0), aB=(-0.15, 0.0), dy=6 * u, tilt=0.15)
    elif b < 60:                                # picks up the last slice
        st.update(walk((b - 58) * math.pi, amp=1 - clamp(b - 59.2)), x=keys([(58, X1), (59.4, 730)], b),
                  aF=keys([(58, (0.4, 0.0)), (59.4, (1.75, 0.15))], b), eyes="open", look=(0.8, 0.4), mouth="flat")
    elif b < 64:                                # tears it, shares it, eats
        give = keys([(61.8, 0.0), (62.4, 1.0), (63.2, 1.0), (63.6, 0.0)], b)
        st.update(x=730, aF=(1.45 - 0.5 * give, -0.25 + 0.6 * give), aB=(1.3, -0.4), eyes="open" if b < 62.6 else "happy",
                  look=(0.7, 0.5), mouth="chew" if b > 63 else "smile")
    else:                                       # licked! hearts
        st.update(x=730, aF=(0.5, 0.2), aB=(-0.6, 0.2), eyes="happy", mouth="grin", red=0.25 * clamp(b - 64.5),
                  dy=-10 * pulse(b, [64.6], 5), tilt=-0.08)
    return st


def bolt_state(b, T):
    st = dict(T=T, facing=1, x=-400, belly=1.0 if b >= 39 else 0.0)
    if b < 28:
        return None
    if b < 30:
        st.update(x=keys([(28, -260), (30, 600)], b, lambda u: u), gait=b * 2 * math.pi * 1.0)
    elif b < 32:
        sn = pulse(b, [30, 30.5, 30.9], 5)
        st.update(x=600, head=0.45 + 0.08 * sn, look=(0.5, -1.0) if b < 31.2 else (0.0, 0.2),
                  eye="open" if b < 31.2 else "half", tail=0.8)
    elif b < 39.4:                              # in the cloud
        u = clamp((b - 32) / 0.8)
        top = tower_top(14)
        st.update(x=lerp(600, TX - 60, u), dy=lerp(0, top - 1500 - 40, u) - math.sin(u * math.pi) * 260,
                  head=0.3, eye="happy", squash=0.0, hidden=b >= 32.8)
    elif b < 40.2:                              # jumps down, fat
        u = clamp((b - 39.4) / 0.8)
        y0 = BASE - 34 * 1.35 - 1500
        st.update(x=lerp(TX - 20, 640, u), dy=lerp(y0, 0, u) - math.sin(u * math.pi) * 150, sit=u, eye="happy")
    else:
        st.update(x=640, sit=1.0)
        if b < 47:
            st.update(eye="half", look=(-0.6, -0.9), whistle=1 if 40.2 < b < 43.4 else 0, tail=0.3, head=-0.15)
        elif b < 49:
            burp = pulse(b, [48.5], 4)
            st.update(eye="half", look=(-0.6, -0.9), jaw=burp * 0.9, head=-0.15 - 0.2 * burp)
        elif b < 53:
            st.update(eye="open", look=(1.0, -0.6), ears=-0.2, head=0.1)
        elif b < 56.5:
            st.update(eye="puppy", ears=0.8, head=0.25 + 0.05 * math.sin(T * 6), tail=0.4)
        elif b < 62:
            st.update(eye="open", look=(1.0, -0.4), tail=1.0, head=0.15)
        elif b < 64.4:
            st.update(eye="happy", jaw=abs(math.sin(T * 9)) * 0.7 if b > 62.4 else 0, tail=1.0, head=0.2)
        else:
            u = clamp((b - 64.4) / 1.4)
            st.update(x=lerp(640, 700, math.sin(u * math.pi)), dy=-math.sin(u * math.pi) * 330, sit=1 - math.sin(u * math.pi),
                      head=0.5 * math.sin(u * math.pi) + 0.2, eye="happy", tail=1.0, tongue=math.sin(u * math.pi))
    return st


def draw(c, t):
    b = t / B
    c.save()
    cx, cy, z = keys([(0, (540, 1010, 1.12)), (44.8, (540, 1010, 1.12)), (45.15, (835, 1010, 1.75)),
                      (46.8, (835, 1010, 1.75)), (47.4, (540, 1010, 1.12)), (52.8, (540, 1010, 1.12)),
                      (53.15, (760, 1215, 1.8)), (56.0, (760, 1215, 1.8)), (56.6, (540, 1010, 1.12))], b)
    sh = 7 * (pulse(b, CHOMP, 9) * (33 <= b < 39.5) + pulse(b, [50, 51, 52, 52.5], 8))
    camera(c, cx + math.sin(t * 70) * sh, cy + math.cos(t * 63) * sh, z)
    kitchen(c, t)
    table(c)
    # sandwich
    n = layers_on(b)
    last = max([i for i, d in enumerate(DROP) if b >= d - 0.6] or [-1])
    drop = (last, b - (DROP[last] - 0.6)) if 0 <= last < 14 and b < DROP[last] and b < 32 else None
    land = pulse(b, DROP, 7) if b < 18 else 0
    wob = math.sin((b - 17) * 9) * math.exp(-(b - 17) * 1.1) if 17 <= b < 24 else 0.0
    bread_in_hand = b >= 59.5
    if not (bread_in_hand and n <= 1):
        c.save()
        c.translate(TX, BASE)
        c.scale(1.25, 1.35 * (1 - 0.05 * land))
        sandwich(c, 0, 0, n, wobble=wob, drop=(drop[0], drop[1]) if drop else None, w=200)
        c.restore()
    if 17 <= b < 19.5:
        for k in range(5):
            an = k * 1.3 + b
            sparkle(c, TX + math.cos(an) * 190, tower_top(14) + 120 + math.sin(an) * 160, 30,
                    math.sin(clamp((b - 17 - k * 0.15) / 1.6) * math.pi), (1, 0.85, 0.2))
    # dog
    ds = bolt_state(b, t)
    if ds and not ds.pop("hidden", False):
        bolt(c, y=1500, **ds)
    if 32.8 <= b < 39.6:
        a = clamp((b - 32.8) / 0.3) * clamp((39.6 - b) / 0.3)
        top = tower_top(max(1, layers_on(b)))
        dust_cloud(c, TX, top + 10, t, a, 190)
    # burp tomato
    if 48.5 <= b < 52:
        u = clamp((b - 48.5) / 0.9)
        x = 640 + 2.4 * 70 + 160 * u
        y = 1500 - 2.4 * 100 - math.sin(u * math.pi) * 120 + u * 240
        c.save(); c.translate(x, min(y, 1495)); c.rotate(u * 5); c.scale(0.55, 0.55)
        layer(c, "tomato", 0, 0, 110, 22)
        c.restore()
    # Stix
    st = stix_state(b, t)
    hands = stix(c, s=3.0, y=1500, **st)
    if 41 <= b < 49.4:                           # the big knife
        ang = keys([(41, -math.pi / 2 - 0.5), (45, -math.pi / 2 - 0.5), (46.6, math.pi / 2 + 0.35)], b)
        hx, hy = hands["F"]
        if b >= 49:
            u = clamp((b - 49) / 0.45)
            hy = lerp(hy, 1480, u * u)
            hx = lerp(hx, 900, u)
            ang = lerp(ang, math.pi + 0.08, u)
        knife(c, hx, hy, ang, 0.85)
    elif b >= 49.4:
        knife(c, 900, 1480, math.pi + 0.08, 0.85)
    if 24 <= b < 25.4:
        bulb(c, hands["head"][0], hands["head"][1] - 230, back(clamp((b - 24) / 0.35)) * clamp((25.4 - b) / 0.3), 1.0)
    # the last slice: in Stix's hand, then torn in two, then half for the dog
    if bread_in_hand:
        fx, fy = hands["F"]
        bx, by = hands["B"]
        if b < 61:
            c.save(); c.translate(fx, fy + 10); c.scale(0.8, 0.8)
            layer(c, "bread", 0, 0, 170, 34)
            c.restore()
        else:
            give = clamp((b - 61.8) / 0.6)
            gone_dog = b >= 63.2
            gone_me = b >= 64.0
            if not gone_me:
                c.save(); c.translate(bx, by + 10); c.scale(0.8, 0.8); layer(c, "bread", 0, 0, 80, 34); c.restore()
            if not gone_dog:
                dx = lerp(fx, 640 + 2.4 * 75, give)
                dy = lerp(fy, 1500 - 2.4 * 100, give)
                c.save(); c.translate(dx, dy + 10); c.scale(0.8, 0.8); layer(c, "bread", 0, 0, 80, 34); c.restore()
    if b >= 64.8:
        for k, b0 in enumerate((64.8, 65.3, 65.8)):
            if b >= b0:
                u = (b - b0) / 4
                heart(c, 760 + (k - 1) * 110 + math.sin(b * 3 + k) * 20, 1000 - u * 380, 1.6 * back(clamp((b - b0) / 0.3)),
                      clamp(1.2 - u))
    c.restore()
    # screen-space text
    for i, (s, col) in enumerate(zip(HOOK, ((1, 1, 1), (1.0, 0.82, 0.2)))):
        heavy_text(c, s, W / 2, 230 + i * 112, 100, col)
    if b >= 67:
        k = back(clamp((b - 67) / 0.4))
        c.save(); c.translate(W / 2, 1760); c.scale(k, k)
        heavy_text(c, "THE END?", 0, 0, 120, (1.0, 0.82, 0.2))
        c.restore()
    # thin fade in / out
    if t < 0.25 or b > BEATS - 1:
        a = max(clamp(1 - t / 0.25), clamp((b - (BEATS - 1)) / 1.0)) * 0.9
        c.set_source_rgba(0, 0, 0, a); c.paint()


# ---------------------------------------------------------------- music
def T_(beat):
    return beat * B


def score(m):
    prog_a = {0: 48, 4: 53, 8: 48, 12: 55, 16: 48}        # C F C G C (bass roots, midi)
    chords = {48: (60, 64, 67), 53: (60, 65, 69), 55: (59, 62, 67), 57: (60, 64, 69)}

    def groove(b0, b1, roots, vol=1.0, drums=True):
        for bt in range(b0, b1):
            root = roots[max(k for k in roots if k <= bt)]
            m.put(T_(bt), pluck(hz(root - 12 + (7 if bt % 2 else 0)), 0.5), 0.55 * vol)
            for n_ in chords[root]:
                m.put(T_(bt + 0.5), pluck(hz(n_), 0.25, 2.0), 0.09 * vol, 0.3)
            if drums:
                if bt % 2 == 0:
                    m.put(T_(bt), kick(), 0.5 * vol)
                else:
                    m.put(T_(bt), snare(), 0.22 * vol, -0.1)
                for h in (0, 0.5):
                    m.put(T_(bt + h), shaker(), 0.14 * vol, 0.4)

    # A: build-up groove, layers play the C major scale
    groove(0, 17, prog_a)
    for i, d in enumerate(DROP):
        m.put(T_(d), glock(hz(SCALE[i])), 0.42, -0.2)
    for k, f in enumerate((180, 150, 125, 105)):
        m.put(T_(16 + k * 0.25), tom(f), 0.35)
    # ta-da
    for n_ in (60, 64, 67, 72):
        m.put(T_(17), brass(hz(n_), 0.9), 0.16)
    m.put(T_(17), cymbal(), 0.35, 0.2)
    m.put(T_(17), kick(), 0.6)
    for k, n_ in enumerate((48, 48)):
        m.put(T_(18 + k), pluck(hz(n_), 0.4), 0.35)
    # realisation: a sad chromatic walk down
    for k, n_ in enumerate((48, 47, 46, 45)):
        m.put(T_(20 + k), pluck(hz(n_), 0.7), 0.5)
    # tip-toe exit
    for k, n_ in enumerate((55, 57, 59, 60, 62, 64)):
        m.put(T_(25 + k * 0.5), pluck(hz(n_), 0.3, 1.5), 0.35)
    # sneaky dog theme (A minor), busier during the chomping
    sneak = [45, None, 48, None, 52, None, 51, 52, 45, None, 48, None, 52, 53, 52, 48]
    k = 0
    bt = 28.0
    while bt < 39:
        n_ = sneak[k % len(sneak)]
        if n_:
            m.put(T_(bt), reed(hz(n_), 0.15), 0.32)
        if bt == int(bt) and int(bt) % 2 == 1:
            m.put(T_(bt), snare(False), 0.14, 0.2)
        if bt >= 32:
            if bt == int(bt):
                m.put(T_(bt), kick(), 0.45)
            m.put(T_(bt), shaker(), 0.12, -0.3)
        k += 1
        bt += 0.5
    for i, ch in enumerate(CHOMP):
        m.put(T_(ch), glock(hz(SCALE[12 - i] if i < 13 else 72), 0.6), 0.3, 0.2)
    # innocent whistle (dog)
    for bt, n_, d in ((40.4, 88, 0.6), (41.1, 84, 0.6), (41.8, 86, 0.5), (42.5, 79, 0.8)):
        m.put(T_(bt), hum(hz(n_), d * B * 1.6), 0.18, 0.3)
    # happy reprise + Stix humming
    groove(41, 45, {41: 48, 43: 53}, 0.8)
    for bt, n_, d in ((41, 64, 0.5), (41.5, 67, 0.5), (42, 69, 0.5), (42.5, 67, 0.5), (43, 64, 1), (44, 60, 0.9)):
        m.put(T_(bt), hum(hz(n_), d * B), 0.22, -0.2)
    # scratch -> silence -> suspense
    for bt in (47, 48):
        m.put(T_(bt), pluck(hz(33), 0.9), 0.6)
    # anger: rising staccato 16ths + timpani
    bt, n_ = 49.0, 48
    while bt < 53:
        m.put(T_(bt), reed(hz(n_ - 12), 0.08), 0.28)
        m.put(T_(bt), reed(hz(n_), 0.08), 0.12)
        bt += 0.25
        n_ += 0.5 if int(bt * 4) % 2 else 0
        n_ = round(n_)
    for bt in (50, 51, 52, 52.5):
        m.put(T_(bt), tom(70), 0.7)
        m.put(T_(bt), kick(), 0.5)
    # aww
    m.put(T_(53), pad([hz(n_) for n_ in (53, 57, 60, 64)], 3 * B, 0.15, 0.8), 0.5)
    for k, n_ in enumerate((65, 69, 72, 76, 77, 81)):
        m.put(T_(53) + k * 0.06, pluck(hz(n_), 0.8, 2.5), 0.22, -0.3 + k * 0.12)
    for bt in (54, 54.5, 55.25):
        m.put(T_(bt), glock(hz(96)), 0.14, 0.4)
    # warm ending
    warm = {58: 48, 60: 45, 62: 53, 64: 55, 66: 48}
    for bt in range(58, 67):
        root = warm[max(k for k in warm if k <= bt)]
        m.put(T_(bt), pluck(hz(root - 12), 0.6), 0.45)
        if bt % 2 == 1:
            m.put(T_(bt), snare(), 0.12)
        m.put(T_(bt + 0.5), shaker(), 0.08, 0.4)
        if bt % 2 == 0:
            m.put(T_(bt), pad([hz(n_) for n_ in chords.get(root, (60, 64, 67))], 2 * B, 0.08, 0.5), 0.32)
    for bt, n_ in ((58, 76), (59, 79), (60, 81), (61, 79), (62, 77), (63, 76), (64, 74), (65, 79), (66, 84)):
        m.put(T_(bt), glock(hz(n_)), 0.3, 0.1)
    # button
    for n_ in (60, 64, 67, 72):
        m.put(T_(67), brass(hz(n_), 0.5, 0.6), 0.15)
    m.put(T_(67), cymbal(2.4), 0.3)
    m.put(T_(67), kick(), 0.6)


def sfx(m):
    for bt in (0, 1, 2, 25, 26, 27, 41, 42, 43, 44, 58.2, 59.0):
        m.put(T_(bt), fx_step(), 0.8)
    for bt in (28, 28.5, 29, 29.5):
        m.put(T_(bt), fx_step(), 0.35, -0.5)
    m.put(T_(17.3), fx_boing(), 0.45, -0.3)
    m.put(T_(21.5), fx_slide(1300, 330, 2 * B), 0.5)
    m.put(T_(24), fx_ding(), 0.5)
    m.put(T_(30), fx_sniff(), 0.6, -0.3)
    m.put(T_(31.1), fx_sniff(), 0.5, -0.3)
    m.put(T_(32), fx_jump(), 0.5)
    m.put(T_(32), fx_whoosh(), 0.6)
    m.put(T_(32.8), fx_pop(250), 0.7)
    for ch in CHOMP:
        m.put(T_(ch), fx_chomp(), 0.75, -0.2)
    m.put(T_(39.4), fx_whoosh(), 0.5)
    m.put(T_(40.2), kick(), 0.5)
    m.put(T_(40.2), fx_boing(0.4), 0.3)
    m.put(T_(45), fx_scratch(), 0.9)
    m.put(T_(48.5), fx_burp(), 0.9)
    m.put(T_(48.6), fx_pop(500), 0.4)
    m.put(T_(49.4), fx_clang(), 0.6)
    m.put(T_(50.7), fx_steam(1.8), 0.45)
    m.put(T_(53.5), fx_whimper(), 0.6, -0.2)
    m.put(T_(56), fx_sigh(), 0.8)
    m.put(T_(61), fx_tear(), 0.8)
    for bt in (62.6, 63.0, 63.4, 63.8):
        m.put(T_(bt), fx_chomp(), 0.4)
    m.put(T_(64.4), fx_jump(), 0.4)
    m.put(T_(64.9), fx_slurp(), 0.7)
    for k, bt in enumerate((64.8, 65.3, 65.8)):
        m.put(T_(bt), fx_pop(800 + 200 * k), 0.4)
    m.put(T_(67), fx_ding(), 0.4)
