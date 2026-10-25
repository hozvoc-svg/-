"""Shorts physics simulation: a ball bounces inside spinning concentric rings, each with a gap.
Every bounce plays the next note of a public-domain melody; passing a gap shatters that ring.

    python3 sims/escape.py OUT.mp4 [seed] [rings]
"""
import math, os, subprocess, sys, wave, colorsys
from multiprocessing import Pool
import numpy as np
import cairo

W, H, FPS, SUB = 1080, 1920, 60, 10
CX, CY = W / 2, 960
SR = 44100
FONT = "Inter Display Black"

# In the Hall of the Mountain King (Grieg, 1875, public domain): main theme, then up a fifth, then up an octave
_A = [59, 61, 62, 64, 66, 62, 66, 65, 61, 65, 64, 60, 64, 59, 61, 62, 64, 66, 62, 66, 71, 69, 66, 62, 66, 69]
MELODY = _A + [n + 7 for n in _A] + [n + 12 for n in _A] + [n + 19 for n in _A]


def simulate(seed=1, rings=15, gap_deg=30.0, gap_grow=24.0, r_min=118.0, r_max=470.0, ball_r=16.0, g=1500.0, vmin=900.0):
    rng = np.random.default_rng(seed)
    radii = np.linspace(r_min, r_max, rings)
    omega = np.array([(1.0 + 0.07 * i) * (1 if i % 2 == 0 else -1) for i in range(rings)]) * rng.uniform(0.85, 1.15)
    theta0 = rng.uniform(0, 2 * np.pi, rings)
    gaps = np.radians(gap_deg + gap_grow * np.linspace(0, 1, rings))  # outer rings get wider gaps
    p = np.array([rng.uniform(-30, 30), -20.0])
    v = np.array([rng.uniform(-500, 500), rng.uniform(-300, 0)])
    broken = [None] * rings
    events, frames = [], []
    dt = 1.0 / FPS / SUB
    t, last_bounce, done_at = 0.0, -1.0, None
    while True:
        for _ in range(SUB):
            t += dt
            v[1] += g * dt
            p += v * dt
            k = next((i for i in range(rings) if broken[i] is None), None)
            if k is None:
                continue
            R = radii[k] - 6 - ball_r
            d = math.hypot(*p)
            if d >= R:
                ang = math.atan2(p[1], p[0])
                diff = (ang - (theta0[k] + omega[k] * t) + math.pi) % (2 * math.pi) - math.pi
                if abs(diff) < gaps[k] / 2 - ball_r / radii[k]:
                    broken[k] = t
                    events.append((t, "break", k))
                    if all(b is not None for b in broken):
                        done_at = t
                else:
                    n = p / d
                    v = v - 2 * np.dot(v, n) * n
                    sp = math.hypot(*v)
                    if sp < vmin:
                        v *= vmin / sp
                    p = n * (R - 0.5)
                    if t - last_bounce > 0.045:
                        events.append((t, "bounce", k))
                        last_bounce = t
        frames.append(dict(t=t, p=p.copy(), angles=theta0 + omega * t))
        if done_at is not None and t > done_at + 3.0:
            break
        if t > 75:
            break
    return dict(frames=frames, events=events, radii=radii, gaps=gaps, broken=broken, ball_r=ball_r,
                rings=rings, done_at=done_at, seed=seed)


# ---------------- drawing ----------------

def hue(i, n, s=0.75, v=1.0):
    return colorsys.hsv_to_rgb((0.95 - 0.8 * i / max(1, n - 1)) % 1.0, s, v)


def text(c, s, x, y, size, col, outline=0.14, glow=None):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    w = c.text_extents(s).x_advance
    c.new_path()
    c.move_to(x - w / 2, y)
    c.text_path(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    if glow:
        for lw, a in ((size * 0.5, 0.10), (size * 0.3, 0.18)):
            c.set_source_rgba(*glow, a); c.set_line_width(lw); c.stroke_preserve()
    c.set_source_rgb(0, 0, 0); c.set_line_width(size * outline); c.stroke_preserve()
    c.set_source_rgb(*col); c.fill()


def shards(k, radius, angle, seed):
    r = np.random.default_rng(seed * 100 + k)
    n = 46
    a = angle + r.uniform(0, 2 * np.pi, n)
    speed = r.uniform(250, 900, n)
    return [(radius * math.cos(x), radius * math.sin(x), s * math.cos(x) + r.uniform(-150, 150),
             s * math.sin(x) + r.uniform(-300, 100), r.uniform(4, 11)) for x, s in zip(a, speed)]


def draw(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    n = S["rings"]
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.04, 0.03, 0.09)
    g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g)
    c.paint()
    left = sum(1 for b in S["broken"] if b is None or b > t)
    # rings
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        b = S["broken"][i]
        if b is not None and b <= t:
            # shatter: shards fly out and fade for 1.4 s
            age = t - b
            if age < 1.4:
                for x, y, vx, vy, sz in shards(i, S["radii"][i], f["angles"][i], S["seed"]):
                    px = CX + x + vx * age
                    py = CY + y + vy * age + 900 * age * age
                    col = hue(i, n)
                    c.set_source_rgba(*col, 1 - age / 1.4)
                    c.rectangle(px - sz / 2, py - sz / 2, sz, sz)
                    c.fill()
                ring = 1 - age / 0.25
                if ring > 0:  # flash
                    c.set_source_rgba(1, 1, 1, 0.5 * ring)
                    c.set_line_width(26)
                    c.arc(CX, CY, S["radii"][i], 0, 2 * math.pi)
                    c.stroke()
            continue
        col = hue(i, n)
        a0 = f["angles"][i] + S["gaps"][i] / 2
        a1 = f["angles"][i] - S["gaps"][i] / 2 + 2 * math.pi
        active = i == next((j for j in range(n) if S["broken"][j] is None or S["broken"][j] > t), -1)
        for lw, al in ((30, 0.10), (20, 0.18), (12, 1.0)):
            c.set_source_rgba(*col, al * (1.0 if active else 0.75))
            c.set_line_width(lw)
            c.new_path()
            c.arc(CX, CY, S["radii"][i], a0, a1)
            c.stroke()
    # ball trail + ball
    br = S["ball_r"]
    for k in range(14, 0, -1):
        j = max(0, fi - k)
        q = S["frames"][j]["p"]
        c.set_source_rgba(1, 1, 1, 0.25 * (1 - k / 14))
        c.arc(CX + q[0], CY + q[1], br * (1 - 0.5 * k / 14), 0, 2 * math.pi)
        c.fill()
    p = f["p"]
    gl = cairo.RadialGradient(CX + p[0], CY + p[1], 2, CX + p[0], CY + p[1], br * 4)
    gl.add_color_stop_rgba(0, 1, 1, 1, 0.55)
    gl.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(gl)
    c.arc(CX + p[0], CY + p[1], br * 4, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(1, 1, 1)
    c.arc(CX + p[0], CY + p[1], br, 0, 2 * math.pi)
    c.fill()
    # text
    text(c, "CAN THE BALL", W / 2, 250, 92, (1, 1, 1))
    text(c, "ESCAPE?", W / 2, 360, 110, (0.3, 0.93, 1.0), glow=(0.3, 0.93, 1.0))
    done = S["done_at"] is not None and t >= S["done_at"]
    if done:
        a = min(1, (t - S["done_at"]) / 0.3)
        sc = 1 + 0.15 * math.exp(-6 * (t - S["done_at"]))
        c.save(); c.translate(W / 2, 1530); c.scale(sc, sc)
        text(c, "ESCAPED!", 0, 0, 130, (0.35, 1.0, 0.5), glow=(0.35, 1.0, 0.5))
        c.restore()
    else:
        text(c, f"RINGS LEFT: {left}", W / 2, 1530, 76, (1, 1, 1))
    tt = min(t, S["done_at"]) if S["done_at"] else t  # the clock stops when the ball gets out
    text(c, f"{tt:5.1f}s", W / 2, 1640 if done else 1610, 54, (0.75, 0.75, 0.85), outline=0.1)


def _render(args):
    S, a, b, path = args
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "17", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for fi in range(a, b):
        c = cairo.Context(surf)
        draw(c, S, fi)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


# ---------------- audio ----------------

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tone(f, dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 4.5) * np.minimum(1, t / 0.004)
    s = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * k * 1.5) for k, a in ((1, 1.0), (2, 0.45), (3, 0.22), (4, 0.1)))
    return (s * env).astype(np.float32)


def shatter(seed):
    r = np.random.default_rng(seed)
    t = np.arange(int(0.7 * SR)) / SR
    noise = r.standard_normal(len(t)).astype(np.float32)
    noise = np.diff(noise, prepend=0) * np.exp(-t * 9)  # bright crackle
    bell = sum(np.sin(2 * np.pi * f * t) for f in (2093, 2637, 3136)) * np.exp(-t * 5) * 0.25
    return (noise * 0.35 + bell).astype(np.float32)


def audio(S, path):
    total = S["frames"][-1]["t"] + 0.5
    out = np.zeros(int(total * SR) + SR, np.float32)
    ni = 0
    for t, kind, k in S["events"]:
        i0 = int(t * SR)
        if kind == "bounce":
            s = tone(hz(MELODY[ni % len(MELODY)])) * 0.5
            ni += 1
        else:
            s = shatter(k) * 0.6
        out[i0:i0 + len(s)] += s[:len(out) - i0]
    if S["done_at"]:
        i0 = int(S["done_at"] * SR)
        for m in (59, 66, 71, 74, 78):  # final B-minor chord
            s = tone(hz(m), 2.5) * 0.3
            out[i0:i0 + len(s)] += s[:len(out) - i0]
    out = np.tanh(out * 1.1)
    st = np.stack([out, out], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767 * 0.9).astype(np.int16).tobytes())


def build(out, seed=1, rings=15):
    S = simulate(seed, rings)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), f".escape_{seed}")
    os.makedirs(tmp, exist_ok=True)
    nf = len(S["frames"])
    parts = 8
    jobs = [(S, nf * i // parts, nf * (i + 1) // parts, os.path.join(tmp, f"p{i}.mp4")) for i in range(parts)]
    with Pool(os.cpu_count()) as pool:
        paths = pool.map(_render, jobs)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in paths)
    wav = os.path.join(tmp, "a.wav")
    audio(S, wav)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-filter_complex", "[1:a]loudnorm=I=-14:TP=-1[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    return S


if __name__ == "__main__":
    o = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rings = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    S = build(o, seed, rings)
    print(o, round(S["frames"][-1]["t"], 1), "s", "escaped at", S["done_at"])
