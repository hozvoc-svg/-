"""Shared pieces for the Bounce Lab "LEVEL 1-7" challenge series: colour themes, public-domain melodies,
the level badge + hook, audio from simulation events, and a parallel renderer with a seamless loop."""
import colorsys, math, os, subprocess, wave
from multiprocessing import Pool
import numpy as np
import cairo
import escape as E

W, H, FPS, SR = 1080, 1920, 60, 44100
CX, CY = W / 2, 960

THEMES = {  # bg gradient top/bottom, accent colour, hue range for objects
    "sunset": dict(bg=((0.20, 0.05, 0.20), (0.05, 0.01, 0.07)), acc=(1.0, 0.58, 0.28), hues=(0.93, 1.12)),
    "lava":   dict(bg=((0.16, 0.04, 0.02), (0.03, 0.00, 0.00)), acc=(1.0, 0.45, 0.15), hues=(0.98, 1.14)),
    "mint":   dict(bg=((0.02, 0.15, 0.14), (0.00, 0.03, 0.04)), acc=(0.35, 1.0, 0.80), hues=(0.40, 0.56)),
    "duel":   dict(bg=((0.07, 0.07, 0.11), (0.02, 0.02, 0.04)), acc=(1.0, 1.0, 1.0), hues=(0.0, 0.6)),
    "candy":  dict(bg=((0.17, 0.04, 0.19), (0.04, 0.01, 0.06)), acc=(1.0, 0.45, 0.85), hues=(0.76, 0.98)),
    "ocean":  dict(bg=((0.02, 0.07, 0.19), (0.00, 0.01, 0.05)), acc=(0.35, 0.78, 1.0), hues=(0.48, 0.70)),
    "gold":   dict(bg=((0.12, 0.09, 0.02), (0.02, 0.015, 0.0)), acc=(1.0, 0.82, 0.30), hues=(0.07, 0.17)),
}

# public-domain themes (MIDI), each video gets its own
MELODIES = {
    "ode_to_joy": [64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 64, 62, 62, 64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 62, 60, 60,
                   62, 62, 64, 60, 62, 64, 65, 64, 60, 62, 64, 65, 64, 62, 60, 62, 55],
    "fur_elise": [76, 75, 76, 75, 76, 71, 74, 72, 69, 60, 64, 69, 71, 64, 68, 71, 72, 64, 76, 75, 76, 75, 76, 71, 74, 72, 69, 60, 64, 69,
                  71, 64, 72, 71, 69],
    "morning_mood": [79, 76, 74, 72, 74, 76, 79, 76, 74, 72, 74, 76, 74, 76, 79, 76, 79, 81, 76, 81, 79, 76, 74, 72],
    "can_can": [60, 62, 65, 64, 62, 67, 67, 67, 69, 64, 65, 62, 62, 62, 65, 64, 62, 60, 72, 71, 69, 67, 65, 64, 62],
    "canon": [78, 76, 74, 73, 71, 69, 71, 73, 74, 73, 71, 69, 67, 66, 67, 64, 66, 69, 67, 66, 64, 66, 64, 62, 61, 62, 64, 66],
    "turkish_march": [71, 69, 68, 69, 72, 74, 72, 71, 72, 76, 77, 76, 75, 76, 83, 81, 80, 81, 83, 81, 80, 81, 84, 81, 84, 83, 81, 79, 81],
    "mountain_king": E.MELODY,
}
DIFF_COL = {"EASY": (0.35, 1.0, 0.5), "MEDIUM": (1.0, 0.85, 0.25), "HARD": (1.0, 0.5, 0.2), "INSANE": (1.0, 0.25, 0.35)}


def theme(name):
    return THEMES[name]


def col(th, i, n, s=0.78, v=1.0):
    h0, h1 = th["hues"]
    return colorsys.hsv_to_rgb((h0 + (h1 - h0) * i / max(1, n - 1)) % 1.0, s, v)


def background(c, th, t=0.0):
    top, bot = th["bg"]
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bot)
    c.set_source(g)
    c.paint()
    c.set_line_width(1.5)
    c.set_source_rgba(*th["acc"], 0.05)
    off = (t * 18) % 90
    for x in range(-90, W + 90, 90):
        c.move_to(x + off, 0); c.line_to(x + off, H)
    for y in range(0, H + 90, 90):
        c.move_to(0, y + off); c.line_to(W, y + off)
    c.stroke()
    v = cairo.RadialGradient(CX, CY, 400, CX, CY, 1250)
    v.add_color_stop_rgba(0, 0, 0, 0, 0)
    v.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(v)
    c.paint()


def pill(c, s, x, y, fill, size=46):
    c.select_font_face(E.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    half = c.text_extents(s).x_advance / 2 + 8
    r = size * 0.8
    c.new_path()
    c.arc(x - half, y, r, math.pi / 2, 3 * math.pi / 2)
    c.arc(x + half, y, r, -math.pi / 2, math.pi / 2)
    c.close_path()
    c.set_source_rgb(*fill)
    c.fill_preserve()
    c.set_source_rgb(0, 0, 0)
    c.set_line_width(5)
    c.stroke()
    E.text(c, s, x, y + size * 0.36, size, (0.05, 0.05, 0.08), outline=0.0)


def hud_top(c, S, t):
    """Level badge + two-line hook, popping in on the first frames."""
    th = THEMES[S["theme"]]
    pop = 1 + 0.45 * (1 - min(1, t / 0.25)) ** 2
    c.save()
    c.translate(W / 2, 0)
    c.scale(pop, pop)
    pill(c, f"LEVEL {S['level']}  ·  {S['diff']}", 0, 150, DIFF_COL[S["diff"]], 44)
    l1, l2 = S["title"]
    E.text(c, l1, 0, 290, 88, (1, 1, 1), max_w=W * 0.9)
    E.text(c, l2, 0, 400, 104, th["acc"], glow=th["acc"], max_w=W * 0.9)
    c.restore()


def big_result(c, s, t0, t, colr, y=1560):
    a = min(1, (t - t0) / 0.3)
    sc = 1 + 0.15 * math.exp(-6 * (t - t0))
    c.save()
    c.translate(W / 2, y)
    c.scale(sc, sc)
    E.text(c, s, 0, 0, 120, colr, glow=colr, max_w=W * 0.92)
    c.restore()


# ---------------- audio from events ----------------
def audio(S, path):
    """events: (t, 'note'|'tick'|'break'|'end', value). 'note' plays the next melody note (value=octave shift)
    or the given MIDI number if value > 20."""
    total = S["frames"][-1]["t"] + 0.5 if isinstance(S["frames"][-1], dict) else S["total"] + 0.5
    out = np.zeros(int(total * SR) + 3 * SR, np.float32)
    mel = MELODIES[S["melody"]]
    s = E.tone(E.hz(mel[0] - 12), 1.2) * 0.6  # sound from the very first frame
    out[:len(s)] += s
    ni = 0
    cache = {}

    def put(sig, t):
        i0 = int(t * SR)
        if 0 <= i0 < len(out):
            out[i0:i0 + len(sig)] += sig[:len(out) - i0]

    def tone(m, dur=0.9):
        if (m, dur) not in cache:
            cache[(m, dur)] = E.tone(E.hz(m), dur)
        return cache[(m, dur)]

    for t, kind, val in S["events"]:
        if kind == "note":
            m = val if val > 20 else mel[ni % len(mel)] + val
            if val <= 20:
                ni += 1
            put(tone(m) * 0.45, t)
        elif kind == "tick":
            put(tone(val if val > 20 else 96, 0.25) * 0.12, t)
        elif kind == "break":
            put(E.shatter(int(val)) * 0.55, t)
        elif kind == "end":
            root = mel[0] - 12
            for k in (0, 7, 12, 16, 19):
                put(tone(root + k, 2.5) * 0.28, t)
    out = np.tanh(out * 1.1)
    st = np.stack([out, out], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767 * 0.9).astype(np.int16).tobytes())


# ---------------- render ----------------
def _render(args):
    draw, S, a, b, path = args
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    nf = len(S["frames"])
    loop = int(0.5 * FPS)
    for fi in range(a, b):
        c = cairo.Context(surf)
        c.set_antialias(cairo.ANTIALIAS_GOOD)
        draw(c, S, fi)
        if fi >= nf - loop:  # dissolve into frame 0 so the Short loops
            c.push_group()
            draw(c, S, 0)
            c.pop_group_to_source()
            c.paint_with_alpha((fi - (nf - loop)) / loop)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    ff.wait()
    return path


def render(draw, S, out):
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), ".lab_" + os.path.splitext(os.path.basename(out))[0])
    os.makedirs(tmp, exist_ok=True)
    nf = len(S["frames"])
    parts = 8
    jobs = [(draw, S, nf * i // parts, nf * (i + 1) // parts, os.path.join(tmp, f"p{i}.mp4")) for i in range(parts)]
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
    print(out, round(nf / FPS, 1), "s")


def cover(draw, S, path, fi, top, mid, sticker):
    """Shorts cover frame with big text."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    S2 = dict(S, nohud=True)
    draw(c, S2, fi)
    th = THEMES[S["theme"]]
    pill(c, f"LEVEL {S['level']}  ·  {S['diff']}", W / 2, 140, DIFF_COL[S["diff"]], 50)
    E.text(c, top, W / 2, 300, 112, (1, 1, 1), max_w=W * 0.9)
    E.text(c, mid, W / 2, 440, 140, th["acc"], glow=th["acc"], max_w=W * 0.9)
    pill(c, sticker, W / 2, 1650, (0.95, 0.2, 0.25), 70)
    surf.write_to_png(path)
