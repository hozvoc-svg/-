"""TikTok/Shorts sim: country balls bounce inside a spinning ring with a gap; whoever falls out is eliminated,
the last ball inside wins. Every wall bounce plays the next note of "Ode to Joy" (Beethoven, public domain).

    python3 sims/country_ring.py OUT.mp4 SEED [N]
"""
import math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
import cairo
import escape as E  # text(), tone(), hz(), shatter()

W, H, FPS, SUB = 1080, 1920, 60, 12
CX, CY, R = W / 2, 930, 390
BALL = 40
SR = 44100
FLAGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "flags")

COUNTRIES = [("us", "USA"), ("mx", "Mexico"), ("ca", "Canada"), ("br", "Brazil"), ("gb", "UK"), ("de", "Germany"),
             ("fr", "France"), ("it", "Italy"), ("es", "Spain"), ("pl", "Poland"), ("ua", "Ukraine"), ("tr", "Türkiye"),
             ("in", "India"), ("ph", "Philippines"), ("jp", "Japan"), ("kr", "South Korea"), ("au", "Australia"),
             ("ng", "Nigeria"), ("ar", "Argentina"), ("nl", "Netherlands"), ("se", "Sweden"), ("eg", "Egypt"),
             ("id", "Indonesia"), ("pt", "Portugal")]

_ODE = [64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 64, 62, 62,
        64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 62, 60, 60,
        62, 62, 64, 60, 62, 64, 65, 64, 60, 62, 64, 65, 64, 62, 60, 62, 55,
        64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 62, 60, 60]
MELODY = _ODE + [n + 12 for n in _ODE]


def simulate(seed, n=24, omega=1.15, gap0=11.0, gap_rate=0.17, end_boost=1.6, g=1300.0, vmin=780.0):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(COUNTRIES))[:n]
    teams = [COUNTRIES[i] for i in order]
    # start packed in the middle with random velocities
    p = np.zeros((n, 2))
    k = 0
    tries = 0
    while k < n:
        tries += 1
        lim = R - BALL - 20 if tries > 2000 else R * 0.7  # widen the area if the centre gets too crowded
        q = rng.uniform(-lim, lim, 2)
        if np.hypot(*q) < lim and all(np.hypot(*(q - p[j])) > 2.05 * BALL for j in range(k)):
            p[k] = q
            k += 1
    v = rng.uniform(-450, 450, (n, 2))
    alive = np.ones(n, bool)     # still inside the ring
    out_t = [None] * n           # time of elimination
    theta0 = rng.uniform(0, 2 * np.pi)
    dt = 1.0 / FPS / SUB
    t, events, frames = 0.0, [], []
    last_wall, last_click, done_at = -1.0, -1.0, None
    boost = 0.0  # extra gap (degrees) that grows once three or fewer balls are left, so the final is never slow
    while True:
        for _ in range(SUB):
            t += dt
            if alive.sum() <= 3:
                boost += end_boost * dt
            gap = math.radians(min(80.0, gap0 + gap_rate * t + boost))
            v[:, 1] += g * dt
            p += v * dt
            idx = np.nonzero(alive)[0]
            # ball-ball collisions (equal mass, elastic); numpy finds the overlapping pairs
            q = p[idx]
            dd = q[None, :, :] - q[:, None, :]
            dist2 = (dd ** 2).sum(-1)
            ii, jj = np.nonzero(np.triu(dist2 < (2 * BALL) ** 2, 1))
            for a_, b_ in zip(ii, jj):
                i, j = idx[a_], idx[b_]
                d = p[j] - p[i]
                dist = math.hypot(*d)
                if dist > 0:
                    nrm = d / dist
                    over = 2 * BALL - dist
                    p[i] -= nrm * over / 2
                    p[j] += nrm * over / 2
                    rel = np.dot(v[i] - v[j], nrm)
                    if rel > 0:
                        v[i] -= rel * nrm
                        v[j] += rel * nrm
                        if t - last_click > 0.06:
                            events.append((t, "click", int(i)))
                            last_click = t
            # ring
            for i in idx:
                d = math.hypot(*p[i])
                if d + BALL >= R - 7:
                    ang = math.atan2(p[i][1], p[i][0])
                    diff = (ang - (theta0 + omega * t) + math.pi) % (2 * math.pi) - math.pi
                    if done_at is None and (d > R or abs(diff) < gap / 2 - BALL / R * 0.6):
                        if d > R:   # centre past the ring line: it is out
                            alive[i] = False
                            out_t[i] = t
                            events.append((t, "out", int(i)))
                            if alive.sum() == 1:
                                done_at = t
                        continue
                    nrm = p[i] / d
                    v[i] -= 2 * np.dot(v[i], nrm) * nrm
                    sp = math.hypot(*v[i])
                    if sp < vmin:
                        v[i] *= vmin / sp
                    p[i] = nrm * (R - 7 - BALL - 0.5)
                    if t - last_wall > 0.05:
                        events.append((t, "wall", int(i)))
                        last_wall = t
        frames.append(dict(t=t, p=p.copy(), angle=theta0 + omega * t, gap=gap, alive=alive.copy()))
        if done_at is not None and t > done_at + 4.5:
            break
        if t > 110:
            break
    return dict(frames=frames, events=events, teams=teams, out_t=out_t, done_at=done_at, n=n, seed=seed)


# ---------------- drawing ----------------

_flag_cache = {}


def flag_surface(code):
    if code not in _flag_cache:
        _flag_cache[code] = cairo.ImageSurface.create_from_png(os.path.join(FLAGS, code + ".png"))
    return _flag_cache[code]


def draw_ball(c, x, y, r, code, a=1.0, grey=False):
    c.save()
    c.translate(x, y)
    c.set_source_rgba(0, 0, 0, 0.35 * a)
    c.arc(4, 6, r, 0, 2 * math.pi)
    c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi)
    c.clip()
    img = flag_surface(code)
    s = 2 * r / img.get_width()
    c.scale(s, s)
    c.set_source_surface(img, -img.get_width() / 2, -img.get_height() / 2)
    c.paint_with_alpha(a)
    if grey:
        c.set_source_rgba(0.05, 0.05, 0.08, 0.6 * a)
        c.paint()
    c.restore()
    # glossy highlight + outline
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.4, 1, x - r * 0.35, y - r * 0.4, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.45 * a)
    g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgba(1, 1, 1, 0.95 * a)
    c.set_line_width(max(2.5, r * 0.1))
    c.arc(x, y, r, 0, 2 * math.pi)
    c.stroke()


def ring(c, angle, gap, t):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    a0, a1 = angle + gap / 2, angle - gap / 2 + 2 * math.pi
    for lw, al in ((44, 0.10), (28, 0.20), (14, 1.0)):
        g = cairo.LinearGradient(CX - R, CY - R, CX + R, CY + R)
        g.add_color_stop_rgba(0, 0.3, 0.93, 1.0, al)
        g.add_color_stop_rgba(1, 1.0, 0.3, 0.8, al)
        c.set_source(g)
        c.set_line_width(lw)
        c.new_path()
        c.arc(CX, CY, R, a0, a1)
        c.stroke()


def draw(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.05, 0.04, 0.11)
    g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g)
    c.paint()
    done = S["done_at"] is not None and t >= S["done_at"]
    alive = f["alive"]
    left = int(alive.sum())
    ring(c, f["angle"], f["gap"], t)
    for i, (code, name) in enumerate(S["teams"]):
        x, y = CX + f["p"][i][0], CY + f["p"][i][1]
        if not alive[i]:
            if y > H + 80 or x < -80 or x > W + 80:
                continue
            draw_ball(c, x, y, BALL, code, a=0.8, grey=True)
        else:
            draw_ball(c, x, y, BALL, code)
    # header
    E.text(c, "WHICH COUNTRY", W / 2, 250, 86, (1, 1, 1), max_w=W * 0.86)
    E.text(c, "WINS?", W / 2, 360, 112, (0.3, 0.93, 1.0), glow=(0.3, 0.93, 1.0))
    if not done:
        E.text(c, f"{left} LEFT", W / 2, 445, 52, (1.0, 0.8, 0.3), outline=0.12)
        if left == 2:
            pulse = 1 + 0.08 * math.sin(t * 10)
            c.save(); c.translate(W / 2, 1400); c.scale(pulse, pulse)
            E.text(c, "FINAL 2!", 0, 0, 90, (1.0, 0.35, 0.35), glow=(1.0, 0.3, 0.3))
            c.restore()
    # elimination toasts (most recent three)
    outs = sorted([(S["out_t"][i], i) for i in range(S["n"]) if S["out_t"][i] is not None and S["out_t"][i] <= t])
    for k, (ot, i) in enumerate(reversed(outs[-3:])):
        if done or (left == 2 and k == 0 and t - ot > 1.5):
            break
        age = t - ot
        a = min(1, age / 0.15) * (1 if age < 2.5 else max(0, 1 - (age - 2.5) / 0.5))
        if a <= 0:
            continue
        y = 1380 + k * 78 + (0 if left != 2 else 110)
        slide = (1 - min(1, age / 0.2)) * 120
        draw_ball(c, W / 2 - 200 + slide, y - 18, 28, S["teams"][i][0], a)
        E.text(c, f"{S['teams'][i][1].upper()} OUT", W / 2 + 60 + slide, y, 48, (1.0, 0.45, 0.45), outline=0.12)
    if done:
        win = int(np.nonzero(alive)[0][0])
        code, name = S["teams"][win]
        age = t - S["done_at"]
        z = min(1, age / 0.6)
        zz = z * z * (3 - 2 * z)
        x = CX + f["p"][win][0] * (1 - zz)
        y = CY + f["p"][win][1] * (1 - zz)
        c.set_source_rgba(0, 0, 0, 0.55 * zz)
        c.paint()
        rr = BALL + (190 - BALL) * zz
        glow = cairo.RadialGradient(x, y, rr, x, y, rr * 1.8)
        glow.add_color_stop_rgba(0, 1, 0.85, 0.3, 0.5 * zz)
        glow.add_color_stop_rgba(1, 1, 0.85, 0.3, 0)
        c.set_source(glow)
        c.arc(x, y, rr * 1.8, 0, 2 * math.pi)
        c.fill()
        draw_ball(c, x, y, rr, code)
        if zz > 0.95:
            # crown
            c.save(); c.translate(x, y - rr - 20)
            c.set_source_rgb(1.0, 0.82, 0.2)
            c.move_to(-90, 0); c.line_to(-90, -70); c.line_to(-45, -30); c.line_to(0, -90); c.line_to(45, -30)
            c.line_to(90, -70); c.line_to(90, 0); c.close_path(); c.fill()
            c.restore()
            sc = 1 + 0.12 * math.exp(-5 * (age - 0.6))
            c.save(); c.translate(W / 2, 1330); c.scale(sc, sc)
            E.text(c, name.upper(), 0, 0, 120, (1.0, 0.85, 0.3), glow=(1.0, 0.8, 0.2), max_w=W * 0.9)
            E.text(c, "WINS!", 0, 120, 110, (1, 1, 1))
            c.restore()
            # confetti
            r = np.random.default_rng(7)
            for k in range(90):
                cx_ = r.uniform(0, W)
                cy_ = (r.uniform(-400, 0) + (age - 0.6) * r.uniform(350, 650)) % (H + 200) - 100
                c.save(); c.translate(cx_, cy_); c.rotate(age * r.uniform(-6, 6))
                c.set_source_rgb(*[(1, .3, .4), (.3, .9, 1), (1, .85, .3), (.5, 1, .5)][k % 4])
                c.rectangle(-7, -4, 14, 8); c.fill(); c.restore()


def _render(args):
    S, a, b, path = args
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for fi in range(a, b):
        c = cairo.Context(surf)
        draw(c, S, fi)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


# ---------------- audio ----------------

def pop(seed):
    t = np.arange(int(0.5 * SR)) / SR
    f = 600 * np.exp(-t * 6) + 120
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    return (s * 0.8).astype(np.float32)


def click():
    t = np.arange(int(0.06 * SR)) / SR
    return (np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.25).astype(np.float32)


def audio(S, path):
    total = S["frames"][-1]["t"] + 0.5
    out = np.zeros(int(total * SR) + 3 * SR, np.float32)
    ni = 0
    ck = click()
    for t, kind, k in S["events"]:
        i0 = int(t * SR)
        if kind == "wall":
            s = E.tone(E.hz(MELODY[ni % len(MELODY)]), 0.7) * 0.45
            ni += 1
        elif kind == "out":
            s = pop(k) * 0.55
        else:
            s = ck
        out[i0:i0 + len(s)] += s[:len(out) - i0]
    if S["done_at"]:
        i0 = int((S["done_at"] + 0.6) * SR)
        for j, m in enumerate((60, 64, 67, 72, 76, 79)):  # rising C-major fanfare
            s = E.tone(E.hz(m), 2.6) * 0.32
            st = i0 + j * int(0.07 * SR)
            out[st:st + len(s)] += s[:len(out) - st]
    out = np.tanh(out * 1.1)
    st = np.stack([out, out], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767 * 0.9).astype(np.int16).tobytes())


def build(out, seed, n=24):
    S = simulate(seed, n)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), f".ring_{seed}")
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
    S = build(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 24)
    w = int(np.nonzero(S["frames"][-1]["alive"])[0][0])
    print(sys.argv[1], round(S["frames"][-1]["t"], 1), "s, winner", S["teams"][w][1])
