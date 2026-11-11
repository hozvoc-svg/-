"""Builds music, SFX and the final audio mix for the timeline, plus ASS captions."""
import json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
SHOTS = [3.0, 6.0, 5.8, 5.4, 4.2, 3.6, 3.6, 4.4]          # seconds per shot
STARTS = np.concatenate([[0], np.cumsum(SHOTS)[:-1]])
TOTAL = float(sum(SHOTS))
VO_OFFSET = [0.15, 0.35, 0.3, 0.3, 0.35, 0.6, 0.5, 0.4]   # VO start inside each shot
rng = np.random.default_rng(7)

def t(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.3):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(n, int(r * SR)); e[-nr:] *= np.linspace(1, 0, nr) ** 2; return e
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, at, g=1.0):
    i = int(at * SR); j = min(len(buf), i + len(x)); buf[i:j] += g * x[: j - i]
def midi(n): return 440 * 2 ** ((n - 69) / 12)

def pluck(f, d=0.5):  # Karplus-Strong pizzicato
    n = int(d * SR); p = max(2, int(SR / f)); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * env(n, 0.001, 0.1)
def bell(f, d=1.2):
    x = t(d); s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * k) for m, a, k in [(1, 1, 3), (2.76, .4, 6), (5.4, .2, 10), (8.9, .1, 14)])
    return s * env(len(x), 0.002, 0.2)
def saw(f, x): return 2 * ((f * x) % 1) - 1
def pad(fs, d, cutoff=1800):
    x = t(d); s = sum(saw(f * dt, x) for f in fs for dt in (0.997, 1.003)) / (2 * len(fs))
    return lp(s, cutoff) * env(len(x), 0.6, 1.0)
def brass(fs, d):
    x = t(d); s = sum(saw(f, x) + 0.5 * saw(f * 2.0, x) for f in fs) / len(fs)
    cut = lp(s, 2500) * np.minimum(1, x / 0.08); return s * 0 + cut * env(len(x), 0.08, 0.4)

# ---------- MUSIC ----------
music = np.zeros(int((TOTAL + 1) * SR))
bpm = 112; b = 60 / bpm
launch = STARTS[4]; space = STARTS[5]; ending = STARTS[7]
chords = [[48, 52, 55], [53, 57, 60], [55, 59, 62], [48, 52, 55]]   # C F G C
melody = [72, 76, 79, 76, 77, 74, 71, 74, 72, 76, 79, 84, 83, 79, 77, 74]
beat = 0.0
while beat < launch - 0.2:
    bar = int(beat / (4 * b)) % 4; ch = chords[bar]
    k = int(round(beat / b)) % 4
    add(music, pluck(midi(ch[0] - 12), 0.4), beat, 0.55)                  # bass
    if k in (1, 3): add(music, pluck(midi(ch[1]), 0.3), beat, 0.35); add(music, pluck(midi(ch[2]), 0.3), beat, 0.3)
    m = melody[int(round(beat / (b / 2))) % len(melody)]
    if int(round(beat / (b / 2))) % 2 == 0 or k == 3: add(music, bell(midi(m), 0.6), beat, 0.18)
    beat += b / 2
# launch: rising brass swell
add(music, brass([midi(n) for n in (48, 55, 60, 64)], 1.4), launch - 0.3, 0.35)
add(music, brass([midi(n) for n in (53, 57, 60, 65)], 1.2), launch + 1.1, 0.4)
add(music, brass([midi(n) for n in (55, 59, 62, 67)], 1.8), launch + 2.3, 0.45)
# space: dreamy pad + slow chimes
add(music, pad([midi(n) for n in (48, 55, 64, 71)], ending - space + 1.0), space - 0.3, 0.35)
for i, n in enumerate([84, 88, 91, 86, 84, 79, 88, 91, 93]):
    add(music, bell(midi(n), 1.5), space + i * 0.8, 0.13)
# ending: gentle plucked cadence
for i, n in enumerate([72, 76, 79, 77, 74, 72]):
    add(music, pluck(midi(n), 0.6), ending + 0.2 + i * b, 0.4)
add(music, pad([midi(n) for n in (48, 52, 55, 60)], TOTAL - ending), ending, 0.25)
music = music[: int(TOTAL * SR)]
music *= np.minimum(1, (TOTAL - np.arange(len(music)) / SR) / 1.2)   # fade out
music /= np.max(np.abs(music)) + 1e-9

# ---------- SFX ----------
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def rumble(d):
    x = t(d); n = lp(noise(d), 180) * 6; rattle = bp(noise(d), 300, 900) * (np.sin(2 * np.pi * 14 * x) > 0.6)
    return (n + 0.4 * rattle) * np.minimum(1, x / 0.5) * env(len(x), 0.01, 0.4)
def rip(d=0.35):
    x = t(d); return bp(noise(d), 1500, 6000) * (1 + np.sin(2 * np.pi * 60 * x)) * env(len(x), 0.002, 0.15)
def boing(d=0.6):
    x = t(d); f = 220 + 160 * np.exp(-x * 6) * np.sin(2 * np.pi * 9 * x)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 4)
def whoosh(d, up=True):
    x = t(d); n = noise(d); out = np.zeros_like(n)
    for i, s in enumerate(range(0, len(n), 2048)):
        frac = s / len(n); fc = 300 + (5000 if up else 3000) * (frac if up else 1 - frac)
        out[s:s + 2048] = bp(n[s:s + 2048], fc * 0.6, min(fc * 1.6, 18000))
    return out * np.sin(np.pi * x / d) ** 2
def sparkle(d=1.8):
    o = np.zeros(int(d * SR))
    for i in range(10): add(o, bell(midi(rng.integers(88, 100)), 0.6), rng.uniform(0, d - 0.6), 0.5)
    return o
def crunch(d=0.5):
    o = np.zeros(int(d * SR))
    for i in range(7): add(o, bp(noise(0.03), 800, 5000) * env(int(0.03 * SR), 0.001, 0.02), i * 0.06 + rng.uniform(0, .02))
    return o
def ding(): return bell(midi(96), 1.0) + 0.5 * bell(midi(103), 1.0)

sfx = np.zeros_like(music)
S = STARTS
add(sfx, rumble(3.0), S[0], 0.5)
for k in range(4): add(sfx, rip(), S[2] + 1.0 + k * 1.1, 0.35)
add(sfx, boing(), S[3] + 0.2, 0.4); add(sfx, ding(), S[3] + 2.4, 0.25)
add(sfx, rumble(1.6), S[4], 0.6); add(sfx, whoosh(2.4), S[4] + 1.6, 0.9); add(sfx, lp(noise(2.5), 120) * 4 * env(int(2.5 * SR), .05, 1.5), S[4] + 1.6, 0.6)
add(sfx, sparkle(), S[5] + 0.2, 0.4)
add(sfx, crunch(), S[6] + 1.6, 0.6)
add(sfx, ding(), S[7] + 3.3, 0.35)
for s in S[1:]:                       # soft transition whoosh on each cut
    add(sfx, whoosh(0.5), s - 0.25, 0.12)
sfx /= np.max(np.abs(sfx)) + 1e-9

# ---------- VOICE ----------
def load_mp3(p):
    import subprocess
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)
voice = np.zeros_like(music); words = []
for i in range(8):
    at = S[i] + VO_OFFSET[i]; v = load_mp3(f'audio/vo{i+1:02d}.mp3'); add(voice, v, at)
    al = json.load(open(f'audio/vo{i+1:02d}.json'))
    cur, st = '', None
    for ch, a, e in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if ch.isspace():
            if cur: words.append((at + st, at + end, cur)); cur = ''
            continue
        if not cur: st = a
        cur += ch; end = e
    if cur: words.append((at + st, at + end, cur))
voice /= np.max(np.abs(voice)) + 1e-9

# duck music under voice
venv = np.convolve(np.abs(voice), np.ones(2205) / 2205, 'same')
duck = 1 - 0.55 * np.clip(venv / 0.05, 0, 1)
duck = np.convolve(duck, np.ones(4410) / 4410, 'same')
mix = 0.95 * voice + 0.32 * music * duck + 0.45 * sfx
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write('audio/mix_raw.wav', SR, (mix * 0.9).astype(np.float32))
wavfile.write('audio/music.wav', SR, (music * 0.9).astype(np.float32))

# ---------- CAPTIONS (ASS, 2–3 words per line, active word highlighted) ----------
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
groups, g = [], []
for w in words:
    g.append(w)
    if len(g) == 3 or w[2][-1] in '.!?…,:' or (len(g) == 2 and len(''.join(x[2] for x in g)) > 14): groups.append(g); g = []
if g: groups.append(g)
lines = []
for gi, g in enumerate(groups):
    g_end = g[-1][1] + 0.25
    nxt = groups[gi + 1][0][0] if gi + 1 < len(groups) else TOTAL
    g_end = min(g_end, nxt)
    for k, (s, e, _) in enumerate(g):
        e2 = g[k + 1][0] if k + 1 < len(g) else g_end
        txt = ' '.join((r'{\c&H00D7FF&\fscx112\fscy112}' + w[2].upper() + r'{\r}') if j == k else w[2].upper() for j, w in enumerate(g))
        lines.append(f'Dialogue: 0,{ts(s)},{ts(e2)},Cap,,0,0,0,,{txt}')
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,1,0,1,7,3,2,80,80,620,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('captions.ass', 'w').write(head + '\n'.join(lines) + '\n')
json.dump({'shots': SHOTS, 'starts': list(map(float, S)), 'total': TOTAL}, open('timeline.json', 'w'))
print('total', TOTAL, 'words', len(words), 'caption events', len(lines))
