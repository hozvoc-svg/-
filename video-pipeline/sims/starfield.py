"""Seamlessly looping deep-space starfield for long sleep videos (Sleepy Cosmos).

A dim nebula backdrop (rendered once) with slowly drifting, softly twinkling stars and a rare shooting star.
After LOOP seconds every star is back where it started, so the clip can be repeated for hours.

    python3 sims/starfield.py OUT.mp4 [loop_seconds] [fps]
"""
import math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
import cairo

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
W, H = 1920, 1080


def backdrop(path, seed=5):
    """Dark blue-violet nebula haze, drawn once."""
    import space_art as A
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.010, 0.012, 0.035)
    g.add_color_stop_rgb(1, 0.020, 0.018, 0.055)
    c.set_source(g)
    c.paint()
    rng = np.random.default_rng(seed)
    for k in range(9):  # soft clouds of colour
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(250, 600)
        col = [(0.35, 0.25, 0.65), (0.15, 0.30, 0.60), (0.55, 0.20, 0.45)][k % 3]
        A.glow(c, x, y, r, col, 0.10)
    # Milky Way: a diagonal band of haze and thousands of tiny faint stars
    c.save()
    c.translate(W / 2, H / 2)
    c.rotate(-0.42)
    for k in range(60):
        bx = rng.uniform(-W * 0.7, W * 0.7)
        by = rng.normal(0, 70)
        A.glow(c, bx, by, rng.uniform(90, 220), (0.75, 0.72, 0.90), 0.06)
    for k in range(5000):
        bx = rng.uniform(-W * 0.75, W * 0.75)
        by = rng.normal(0, 95)
        c.set_source_rgba(0.9, 0.9, 1.0, rng.uniform(0.15, 0.55))
        c.arc(bx, by, rng.uniform(0.4, 1.0), 0, 2 * math.pi)
        c.fill()
    for k in range(25):  # dark dust lanes along the band
        bx = rng.uniform(-W * 0.6, W * 0.6)
        A.glow(c, bx, rng.normal(0, 25), rng.uniform(40, 110), (0.0, 0.0, 0.02), 0.35)
    c.restore()
    surf.write_to_png(path)


def stars(seed, n=650, loop=1800.0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, W, n)
    y = rng.uniform(0, H, n)
    mag = rng.power(3.0, n)                       # mostly faint stars, a few bright ones
    laps = np.zeros(n, int)                       # stars stay put; only the bright layer drifts (parallax)
    laps[mag > 0.97] = 1  # only a handful of the brightest stars drift
    tw = rng.integers(3, 9, n)                    # whole (slow) twinkle cycles per loop -> seamless
    sparkle = mag > 0.95                          # the brightest stars scintillate visibly
    tw[sparkle] = rng.integers(120, 320, sparkle.sum())
    ph = rng.uniform(0, 2 * np.pi, n)
    hue = rng.uniform(0, 1, n)
    # a shooting star every ~40-110 s, with its own direction, length and speed
    meteors, t0 = [], rng.uniform(10, 40)
    while t0 < loop - 5:
        ang = rng.uniform(0.25, 0.75) * (1 if rng.random() < 0.6 else -1)
        meteors.append((t0, rng.uniform(150, W - 150), rng.uniform(60, H * 0.55), ang,
                        rng.uniform(300, 750), rng.uniform(0.7, 1.6), rng.uniform(0.6, 1.0)))
        t0 += rng.uniform(40, 110)
    return dict(x=x, y=y, mag=mag, laps=laps, tw=tw, ph=ph, hue=hue, loop=loop, meteors=meteors, sparkle=sparkle)


def draw(c, bg, S, t):
    c.set_source_surface(bg, 0, 0)
    c.paint()
    L = S["loop"]
    yy = (S["y"] + S["laps"] * H * t / L) % H
    tw = np.where(S["sparkle"], 0.65 + 0.35 * np.sin(2 * np.pi * S["tw"] * t / L + S["ph"]),
                  0.85 + 0.15 * np.sin(2 * np.pi * S["tw"] * t / L + S["ph"]))
    for i in range(len(yy)):
        m = S["mag"][i]
        a = (0.25 + 0.75 * m) * tw[i]
        r = 0.6 + 1.9 * m
        warm = S["hue"][i]
        col = (0.85 + 0.15 * warm, 0.88, 1.0 - 0.15 * warm)
        if m > 0.8:
            g = cairo.RadialGradient(S["x"][i], yy[i], 0, S["x"][i], yy[i], r * 5)
            g.add_color_stop_rgba(0, *col, 0.35 * a)
            g.add_color_stop_rgba(1, *col, 0)
            c.set_source(g)
            c.arc(S["x"][i], yy[i], r * 5, 0, 2 * math.pi)
            c.fill()
        c.set_source_rgba(*col, a)
        c.arc(S["x"][i], yy[i], r, 0, 2 * math.pi)
        c.fill()
    for t0, mx, my, ang, ln, dur, br in S["meteors"]:
        u = (t - t0) / dur
        if 0 <= u <= 1:
            dx, dy = math.cos(ang) * (1 if ang > 0 else -1), abs(math.sin(ang))
            hx, hy = mx + dx * ln * u, my + dy * ln * u
            tail = ln * 0.35 * min(1, u * 3)
            a = br * math.sin(math.pi * u)
            g = cairo.LinearGradient(hx, hy, hx - dx * tail, hy - dy * tail)
            g.add_color_stop_rgba(0, 1, 1, 1, a)
            g.add_color_stop_rgba(1, 0.7, 0.8, 1, 0)
            c.set_source(g)
            c.set_line_width(2.8)
            c.move_to(hx, hy)
            c.line_to(hx - dx * tail, hy - dy * tail)
            c.stroke()
            gl = cairo.RadialGradient(hx, hy, 0, hx, hy, 14)
            gl.add_color_stop_rgba(0, 1, 1, 1, a)
            gl.add_color_stop_rgba(1, 1, 1, 1, 0)
            c.set_source(gl)
            c.arc(hx, hy, 14, 0, 2 * math.pi)
            c.fill()


def _render(args):
    bg_path, S, fps, f0, f1, path = args
    bg = cairo.ImageSurface.create_from_png(bg_path)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "12", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        c = cairo.Context(surf)
        draw(c, bg, S, f / fps)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


def render(out, loop=1800.0, fps=12, seed=11, parts=8):
    tmp = os.path.abspath(os.path.splitext(out)[0] + "_parts")
    os.makedirs(tmp, exist_ok=True)
    bg_path = os.path.join(tmp, "bg.png")
    backdrop(bg_path, seed)
    S = stars(seed, loop=loop)
    nf = int(loop * fps)
    jobs = [(bg_path, S, fps, nf * i // parts, nf * (i + 1) // parts, os.path.join(tmp, f"p{i}.mp4")) for i in range(parts)]
    with Pool(os.cpu_count()) as pool:
        paths = pool.map(_render, jobs)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in paths)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", out], check=True)
    return out


if __name__ == "__main__":
    o = sys.argv[1]
    loop = float(sys.argv[2]) if len(sys.argv) > 2 else 1800.0
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    render(o, loop, fps)
    print(o)
