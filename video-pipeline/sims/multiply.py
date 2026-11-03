"""Shorts sim "every bounce = +1 ball": one ball bounces in a ring; each wall hit (per-ball cooldown) spawns
a copy, so the ring fills with hundreds of rainbow balls; at the cap the ring shatters and they spill out.
Starts in motion on frame 0, hook pops in, sound from the first frame, last 0.5 s dissolves into frame 0.

    python3 sims/multiply.py OUT.mp4 [seed] [cap]
"""
import colorsys, math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
import cairo
import escape as E  # text(), tone(), hz(), shatter()

W, H, FPS, SUB = 1080, 1920, 60, 6
CX, CY, R = W / 2, 960, 420
BALL = 11
SR = 44100
PENTA = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96]


def simulate(seed=1, cap=1000, g=900.0, vmin=650.0, cooldown=1.2, fast_until=16, fast_cooldown=0.3, hook=None):
    rng = np.random.default_rng(seed)
    ang = rng.uniform(0, 2 * np.pi)
    p = np.array([[math.cos(ang) * R * 0.55, math.sin(ang) * R * 0.55]])
    v = np.array([[rng.uniform(-900, 900), rng.uniform(-900, -400)]])
    cd = np.zeros(1)
    born = np.zeros(1)
    dt = 1.0 / FPS / SUB
    t, frames, events, full_at, shatter_at = 0.0, [], [], None, None
    last_note = -1.0
    while True:
        for _ in range(SUB):
            t += dt
            v[:, 1] += g * dt
            p += v * dt
            cd -= dt
            if shatter_at is None:
                d = np.hypot(p[:, 0], p[:, 1])
                hit = d > R - 8 - BALL
                if hit.any():
                    n = p[hit] / d[hit][:, None]
                    vh = v[hit]
                    vh -= 2 * (vh * n).sum(1)[:, None] * n
                    sp = np.hypot(vh[:, 0], vh[:, 1])
                    vh *= np.maximum(1, vmin / np.maximum(sp, 1e-6))[:, None]
                    v[hit] = vh
                    p[hit] = n * (R - 9 - BALL)
                    if t - last_note > 0.075:
                        events.append((t, "note", len(p)))
                        last_note = t
                    # duplicate the balls whose cooldown is over
                    idx = np.nonzero(hit & (cd <= 0))[0]
                    room = cap - len(p)
                    if room > 0 and len(idx):
                        idx = idx[:room]
                        rot = rng.uniform(0.25, 0.6, len(idx)) * rng.choice([-1, 1], len(idx))
                        c, s = np.cos(rot), np.sin(rot)
                        vv = v[idx]
                        nv = np.stack([vv[:, 0] * c - vv[:, 1] * s, vv[:, 0] * s + vv[:, 1] * c], 1)
                        p = np.concatenate([p, p[idx] + nv * 0.004])
                        v = np.concatenate([v, nv])
                        cdv = fast_cooldown if len(p) < fast_until else cooldown  # quick ramp-up at the start
                        cd[idx] = cdv
                        cd = np.concatenate([cd, np.full(len(idx), cdv)])
                        born = np.concatenate([born, np.full(len(idx), t)])
                        if len(p) >= cap and full_at is None:
                            full_at = t
            if full_at is not None and shatter_at is None and t > full_at + 0.8:
                shatter_at = t
                events.append((t, "shatter", len(p)))
                v *= 1.25  # burst out
        frames.append(dict(t=t, p=p.copy(), born=born.copy()))
        if shatter_at is not None and t > shatter_at + 2.0:
            break
        if t > 60:
            break
    return dict(frames=frames, events=events, full_at=full_at, shatter_at=shatter_at, cap=cap, seed=seed,
                hook=hook or ("EVERY BOUNCE", "= +1 BALL"))


# ---------------- drawing ----------------

def col(i):
    return colorsys.hsv_to_rgb((i * 0.0137) % 1.0, 0.75, 1.0)


def draw(c, S, fi):
    f = S["frames"][fi]
    t, p, born = f["t"], f["p"], f["born"]
    n = len(p)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.05, 0.03, 0.10)
    g.add_color_stop_rgb(1, 0.01, 0.01, 0.03)
    c.set_source(g)
    c.paint()
    sh = S["shatter_at"]
    # ring (gone once shattered, with a flash)
    if sh is None or t < sh:
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        fill = min(1.0, n / S["cap"])
        for lw, al in ((40, 0.10), (26, 0.18), (12, 1.0)):
            lg = cairo.LinearGradient(CX - R, CY - R, CX + R, CY + R)
            lg.add_color_stop_rgba(0, 0.3, 0.93, 1.0, al)
            lg.add_color_stop_rgba(1, 1.0, 0.3 + 0.5 * fill, 0.8 - 0.6 * fill, al)
            c.set_source(lg)
            c.set_line_width(lw)
            c.new_path()
            c.arc(CX, CY, R, 0, 2 * math.pi)
            c.stroke()
    else:
        age = t - sh
        if age < 0.3:
            c.set_source_rgba(1, 1, 1, 0.7 * (1 - age / 0.3))
            c.paint()
    # balls: a small pop when each one is born
    for i in range(n):
        x, y = CX + p[i][0], CY + p[i][1]
        if y > H + 40 or x < -40 or x > W + 40:
            continue
        age = t - born[i]
        r = BALL * (1 + 0.8 * max(0.0, 1 - age / 0.15))
        cr, cg, cb = col(i)
        c.set_source_rgba(cr, cg, cb, 0.25)
        c.arc(x, y, r * 2.0, 0, 2 * math.pi)
        c.fill()
        c.set_source_rgb(cr, cg, cb)
        c.arc(x, y, r, 0, 2 * math.pi)
        c.fill()
    # hook pops in on the first frames
    pop = 1 + 0.45 * (1 - min(1, t / 0.25)) ** 2
    c.save(); c.translate(W / 2, 300); c.scale(pop, pop)
    E.text(c, S["hook"][0], 0, -50, 96, (1, 1, 1), max_w=W * 0.9)
    E.text(c, S["hook"][1], 0, 70, 120, (0.3, 0.93, 1.0), glow=(0.3, 0.93, 1.0), max_w=W * 0.9)
    c.restore()
    # counter: kicks every time the count doubles
    prev = len(S["frames"][max(0, fi - 1)]["p"])
    kick = 1.12 if prev and int(math.log2(max(n, 1))) > int(math.log2(max(prev, 1))) else 1.0
    c.save(); c.translate(W / 2, 1520); c.scale(kick, kick)
    done = sh is not None and t >= sh
    E.text(c, f"{n} BALL{'' if n == 1 else 'S'}" + ("!" if done else ""), 0, 0, 110 if done else 96,
           (0.35, 1.0, 0.5) if done else (1, 0.85, 0.3), glow=(0.35, 1.0, 0.5) if done else None)
    c.restore()
    if not done:
        E.text(c, "GUESS THE FINAL COUNT", W / 2, 1620, 50, (0.8, 0.8, 0.9), outline=0.1)


def _render(args):
    S, a, b, path = args
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    nf = len(S["frames"])
    loop = int(0.5 * FPS)
    for fi in range(a, b):
        c = cairo.Context(surf)
        draw(c, S, fi)
        if fi >= nf - loop:  # dissolve into the first frame so the Short loops seamlessly
            c.push_group()
            draw(c, S, 0)
            c.pop_group_to_source()
            c.paint_with_alpha((fi - (nf - loop)) / loop)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


# ---------------- audio ----------------

def audio(S, path):
    total = S["frames"][-1]["t"] + 0.5
    out = np.zeros(int(total * SR) + 3 * SR, np.float32)
    s0 = E.tone(E.hz(48), 1.2) * 0.6  # sound from the very first frame
    out[:len(s0)] += s0
    k = 0
    for t, kind, n in S["events"]:
        i0 = int(t * SR)
        if kind == "note":
            # the melody climbs as the ring fills up
            step = min(len(PENTA) - 1, int(math.log2(max(n, 1)) * 1.4) + (k % 3))
            s = E.tone(E.hz(PENTA[step]), 0.5) * 0.4
            k += 1
        else:
            s = E.shatter(3) * 0.9
            for m in (60, 64, 67, 72, 76):
                chord = E.tone(E.hz(m), 2.0) * 0.25
                out[i0:i0 + len(chord)] += chord[:len(out) - i0]
        out[i0:i0 + len(s)] += s[:len(out) - i0]
    out = np.tanh(out * 1.1)
    st = np.stack([out, out], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767 * 0.9).astype(np.int16).tobytes())


def build(out, seed=1, cap=1000, **kw):
    S = simulate(seed, cap, **kw)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), f".multiply_{seed}_{cap}")
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
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    S = build(o, seed, cap)
    print(o, round(S["frames"][-1]["t"], 1), "s; full at", S["full_at"] and round(S["full_at"], 1))
