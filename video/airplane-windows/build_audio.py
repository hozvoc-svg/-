"""Music, SFX and the audio mix for "Why Airplane Windows Are Round", plus ASS captions and title cards.
Everything is synthesized here (the ElevenLabs key has no sound/music permission). Run, then assemble.sh."""
import json, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
TOTAL = 61.0
FPS = 30
rng = np.random.default_rng(11)

def t(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.3):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(n, max(1, int(r * SR))); e[-nr:] *= np.linspace(1, 0, nr) ** 2; return e
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x)); buf[i:j] += g * x[: j - i]
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def saw(f, x): return 2 * ((f * x) % 1) - 1

# ---------- MUSIC: dark documentary bed ----------
def pad(notes, d, cutoff=1200, a=1.0, r=1.5):
    x = t(d); s = sum(saw(midi(n) * dt, x) for n in notes for dt in (0.996, 1.0, 1.004)) / (3 * len(notes))
    return lp(s, cutoff) * env(len(x), a, r)
def sub(n, d):
    x = t(d); return np.sin(2 * np.pi * midi(n) * x) * env(len(x), 0.01, 0.25)
def pulse_bass(n, at, end, step):
    s = at
    while s < end:
        add(music, sub(n, step * 0.9) * np.exp(-t(step * 0.9) * 5), s, 0.8); s += step
def hit(d=2.5):
    x = t(d); body = np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 8)) * x) * np.exp(-x * 2.2)
    return body + lp(noise(d), 400) * 3 * np.exp(-x * 5)
def riser(d):
    x = t(d); n = noise(d); out = np.zeros_like(n)
    for s in range(0, len(n), 2048):
        fc = 200 + 7000 * (s / len(n)) ** 2; out[s:s + 2048] = bp(n[s:s + 2048], fc * 0.7, min(fc * 1.4, 18000))
    return out * (x / d) ** 2
def bell(f, d=1.5):
    x = t(d); s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * k) for m, a, k in [(1, 1, 2.5), (2.76, .35, 5), (5.4, .15, 9)])
    return s * env(len(x), 0.002, 0.2)

music = np.zeros(int(TOTAL * SR))
# hook: low drone (D minor), heartbeat bass
add(music, pad([38, 45, 50, 53], 7.6, 700), 0.0, 0.5)
pulse_bass(26, 0.0, 7.0, 0.75)
add(music, hit(), 4.8, 0.9)                                         # "tore planes apart"
# 1954 story: warmer, slightly hopeful (F major -> D minor)
add(music, pad([41, 48, 53, 57, 60], 5.0, 1500), 7.2, 0.45)
for i, n in enumerate([72, 76, 79, 77, 76, 72]): add(music, bell(midi(n)), 7.5 + i * 1.1, 0.12)
add(music, pad([38, 45, 50, 53, 57], 4.0, 900), 12.0, 0.45)
add(music, riser(2.6), 13.1, 0.35)
add(music, hit(3.5), 15.95, 1.0)                                     # break-up
# tank: ticking pulse that speeds up
add(music, pad([38, 44, 50, 53], 9.6, 800), 19.2, 0.5)
s, step = 19.8, 0.6
while s < 28.4:
    add(music, sub(26, 0.2) * np.exp(-t(0.2) * 12), s, 0.9); s += step; step = max(0.3, step * 0.96)
add(music, riser(1.6), 27.2, 0.45)
add(music, hit(3.0), 28.75, 1.0)                                      # "ripped open"
# explanation: calm minimal pulse
add(music, pad([38, 45, 50, 57], 14.5, 1000), 31.8, 0.42)
pulse_bass(26, 32.1, 46.0, 0.9)
for i, n in enumerate([62, 65, 69, 67, 65, 62, 60, 62]): add(music, bell(midi(n), 2.0), 33.0 + i * 1.6, 0.08)
# fatigue: tense, faster
add(music, pad([38, 44, 50, 56], 6.5, 1400), 46.0, 0.5)
pulse_bass(26, 46.1, 50.4, 0.45)
add(music, riser(1.4), 49.1, 0.5)
add(music, hit(2.0), 50.5, 0.9)                                       # "metal fatigue"
# resolution: D major lift
add(music, pad([38, 45, 50, 54, 57, 62], 5.4, 2000, a=0.4), 52.1, 0.55)
for i, n in enumerate([74, 78, 81, 86]): add(music, bell(midi(n), 2.0), 52.3 + i * 0.5, 0.15)
# tease: suspense, cut to silence at the end
add(music, pad([38, 44, 51], 3.9, 900), 57.1, 0.4)
add(music, riser(3.3), 57.4, 0.4)
music /= np.max(np.abs(music)) + 1e-9

# ---------- SFX ----------
def crack_snd(d=0.5, bright=1.0):
    o = np.zeros(int(d * SR))
    for i in range(9):
        c = bp(noise(0.02), 900, 7000 * bright) * env(int(0.02 * SR), 0.0005, 0.015)
        add(o, c, i * 0.035 + rng.uniform(0, 0.015), rng.uniform(0.4, 1))
    x = t(d); o += 0.6 * np.sin(2 * np.pi * 90 * x) * np.exp(-x * 14)
    return o
def whoosh(d=0.5):
    x = t(d); n = noise(d); out = np.zeros_like(n)
    for s in range(0, len(n), 1024):
        fc = 400 + 3500 * np.sin(np.pi * s / len(n)); out[s:s + 1024] = bp(n[s:s + 1024], fc * 0.6, fc * 1.5)
    return out * np.sin(np.pi * x / d) ** 2
def thump(): x = t(0.35); return np.sin(2 * np.pi * (60 + 40 * np.exp(-x * 30)) * x) * np.exp(-x * 12)
def hiss(d): return hp(noise(d), 3000) * env(int(d * SR), 0.05, 0.1)
def creak(d):
    x = t(d); f = 70 + 40 * x / d
    return bp(saw(1, x) * 0 + np.sign(np.sin(2 * np.pi * np.cumsum(np.full(len(x), 1.0) * f) / SR)), 200, 1200) * env(len(x), 0.3, 0.4)
def debris(d=2.0):
    o = np.zeros(int(d * SR))
    for i in range(30): add(o, bp(noise(0.04), 600, 5000) * env(int(0.04 * SR), 0.001, 0.03), rng.uniform(0, d - 0.1), rng.uniform(0.2, 0.7))
    return o * np.exp(-t(d) * 1.0)
def ding(): return bell(midi(93), 1.4) + 0.4 * bell(midi(100), 1.4)

sfx = np.zeros_like(music)
for cut in (2.55, 7.0, 15.6, 19.3, 28.6, 32.0, 39.4, 46.1, 52.2, 57.2):
    add(sfx, whoosh(0.45), cut - 0.22, 0.25)
f_cr = 4.81
for i in range(4): add(sfx, crack_snd(0.4), f_cr + i * 0.1, 0.7)
add(sfx, crack_snd(0.8), 16.0, 1.0); add(sfx, debris(2.6), 16.0, 0.8)
# pump: one thump + hiss per pressure cycle (frames from scenes.shot_E)
f, period = 15, 18
while f < round((28.6 - 19.3) * FPS) - 6:
    add(sfx, thump(), 19.3 + f / FPS, 0.6); add(sfx, hiss(period / FPS * 0.4), 19.3 + (f + period / 2) / FPS, 0.12)
    f += period; period = max(8, period - 1)
for i in range(3): add(sfx, crack_snd(0.6), 28.6 + 0.2 + i * 4 / FPS, 0.9)
add(sfx, creak(3.2), 33.2, 0.25); add(sfx, hiss(1.3), 37.5, 0.18)
add(sfx, thump(), 42.45, 0.6)
for i in range(9): add(sfx, crack_snd(0.3, 0.7), 46.1 + (6 + i * 14) / FPS, 0.45)
add(sfx, ding(), 52.2 + 40 / FPS, 0.35)
add(sfx, ding(), 57.2 + 55 / FPS, 0.25)
def pop():
    x = t(0.12); return np.sin(2 * np.pi * (900 + 1400 * np.exp(-x * 60)) * x) * np.exp(-x * 45)
for p_at in (0.15, 3.45, 7.42, 8.99, 10.87, 15.9, 21.0, 28.75, 39.6, 42.4, 58.55):
    add(sfx, pop(), p_at, 0.35)
sfx /= np.max(np.abs(sfx)) + 1e-9

# ---------- VOICE + MIX ----------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'audio/voice.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                     capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
voice = np.zeros_like(music); add(voice, v, 0.0)
voice /= np.max(np.abs(voice)) + 1e-9
venv = np.convolve(np.abs(voice), np.ones(2205) / 2205, 'same')
duck = 1 - 0.6 * np.clip(venv / 0.04, 0, 1)
duck = np.convolve(duck, np.ones(4410) / 4410, 'same')
mix = 1.0 * voice + 0.30 * music * duck + 0.40 * sfx
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))
mix /= np.max(np.abs(mix)) + 1e-9
# hook pre-roll (result first): crack + impact before the first word
PRE = 0.6
pre = np.zeros(int(PRE * SR) + int(0.5 * SR))
for i in range(4): add(pre, crack_snd(0.4), 0.0 + i * 0.07, 0.8)
add(pre, hit(1.1) * env(int(1.1 * SR), 0.001, 0.4), 0.0, 0.9)
pre /= np.max(np.abs(pre)) + 1e-9
mix = np.concatenate([np.zeros(int(PRE * SR)), mix])
mix[:len(pre)] += 0.55 * pre
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write('audio/mix_raw.wav', SR, (mix * 0.9).astype(np.float32))

# ---------- CAPTIONS + TITLES (ASS) ----------
words = json.load(open('vo_words.json'))   # [word, start, end]
def ts(x):
    x = max(0, x + PRE); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
groups, g = [], []
for w in words:
    g.append(w)
    if len(g) == 3 or w[0][-1] in '.!?,' or (len(g) == 2 and len(g[0][0] + g[1][0]) > 13):
        groups.append(g); g = []
if g: groups.append(g)

def cap_y(time):  # keep captions off the stacked panels in shot H
    return 975 if 39.4 <= time < 46.1 else 1310

ev = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else TOTAL
    g_end = min(g[-1][2] + 0.3, nxt)
    for wi, w in enumerate(g):
        a = w[1]; b = g[wi + 1][1] if wi + 1 < len(g) else g_end
        txt = ' '.join(('{\\c&H00D7FF&}' + x[0].upper() + '{\\c&HFFFFFF&}') if k == wi else x[0].upper() for k, x in enumerate(g))
        ev.append(f'Dialogue: 1,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\pos(540,{cap_y(a)})}}{txt}')

def title(a, b, text, y=330, style='Title', fade=(120, 120)):
    ev.append(f'Dialogue: 2,{ts(a)},{ts(b)},{style},,0,0,0,,{{\\pos(540,{y})\\fad({fade[0]},{fade[1]})}}{text}')
title(0.15, 2.55, 'NOTICED THIS?', 330)
title(3.45, 7.0, 'THIS SHAPE KILLED 56 PEOPLE', 330, 'Red')
title(7.42, 15.5, '1954', 300, 'Big')
title(8.99, 15.5, 'DE HAVILLAND COMET', 430)
title(10.87, 15.5, "WORLD'S FIRST JET AIRLINER", 500, 'Small')
title(15.9, 19.2, '2 CRASHES  ·  3 MONTHS', 360, 'Red')
# simulated-flight counter in the tank shot
c0, c1 = 21.0, 28.4
steps = int((c1 - c0) / 0.1)
for i in range(steps):
    a = c0 + i * 0.1; n = int(3000 * (i / (steps - 1)) ** 1.6)
    ev.append(f'Dialogue: 2,{ts(a)},{ts(a + 0.1 if i < steps - 1 else 28.6)},Small,,0,0,0,,{{\\pos(540,330)}}SIMULATED FLIGHTS: {n:,}')
title(28.75, 31.9, 'FAILURE POINT', 330, 'Red')
title(39.6, 46.0, 'SMOOTH CURVE', 700, 'Label')
title(42.4, 46.0, 'SHARP CORNER', 1610, 'LabelRed')
title(50.54, 52.15, 'METAL FATIGUE', 640, 'BigRed', (60, 100))
title(58.55, 61.0, '?', 520, 'Big')

head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,1,0,1,7,3,5,60,60,0,1
Style: Big,Inter ExtraBold,190,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,4,0,1,9,4,5,40,40,0,1
Style: BigRed,Inter ExtraBold,120,&H002A2AF0,&H00FFFFFF,&H00FFFFFF,&H90000000,1,0,0,0,100,100,2,0,1,8,4,5,40,40,0,1
Style: Title,Inter ExtraBold,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,3,0,1,6,3,5,40,40,0,1
Style: Small,Inter ExtraBold,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,2,0,1,5,2,5,40,40,0,1
Style: Red,Inter ExtraBold,66,&H002A2AF0,&H00FFFFFF,&H00FFFFFF,&H90000000,1,0,0,0,100,100,2,0,1,6,3,5,40,40,0,1
Style: Label,Inter ExtraBold,54,&H0000A5FF,&H00FFFFFF,&H00202020,&H90000000,1,0,0,0,100,100,2,0,1,5,2,5,40,40,0,1
Style: LabelRed,Inter ExtraBold,54,&H002A2AF0,&H00FFFFFF,&H00FFFFFF,&H90000000,1,0,0,0,100,100,2,0,1,5,2,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('captions.ass', 'w').write(head + '\n'.join(ev) + '\n')
print('ok', len(groups), 'caption groups')
