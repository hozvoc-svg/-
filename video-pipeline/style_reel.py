"""Render a labelled demo reel of every title style, transition, light effect and colour grade in styles.py."""
import os, subprocess, sys
import cairo
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import space_scenes as S
import styles as ST

W, H, FPS = 1920, 1080, 24
OUT = os.path.join(HERE, "out", "style_reel.mp4")


def saturn(c, T):
    S.draw_backdrop(c, 3, T, 3)
    S.A.rings(c, 960, 560, 300, front=False)
    S.paint_sphere(c, "saturn", 960, 560, 300, T * 0.01, light=(-0.6, -0.3, 0.72))
    S.A.rings(c, 960, 560, 300, front=True)


def nebula(c, T):
    c.save(); c.rectangle(0, 0, W, H); c.clip()
    c.set_source_rgb(*S.BG1); c.rectangle(0, 0, W, H); c.fill()
    S.sc_nursery(c, 10, 40, T, dict(seed=11))
    c.restore()


def earth(c, T):
    S.draw_backdrop(c, 4, T, 2)
    S.paint_sphere(c, "earth", 960, 560, 330, T * 0.004, light=(-0.6, -0.3, 0.72), tilt=0.41, clouds_phase=T * 0.0055)


def label(c, text):
    c.select_font_face("Inter")
    c.set_font_size(34)
    w = c.text_extents(text).x_advance
    c.set_source_rgba(0, 0, 0, 0.55)
    c.rectangle(30, 30, w + 40, 60)
    c.fill()
    c.set_source_rgba(1, 1, 1, 0.9)
    c.move_to(50, 72)
    c.show_text(text)


def clips():
    bgs = [saturn, nebula, earth]
    for k, (name, fn) in enumerate(ST.TITLES.items()):
        pair = {"fade": "storybook", "letters": "classic", "spacing": "wide", "typewriter": "mission",
                "lowerthird": "editorial", "script": "script", "blur": "elegant", "poster": "poster"}[name]
        bg = bgs[k % 3]
        yield f"title: {name}  ({ST.PAIRS[pair][0]} + {ST.PAIRS[pair][1]})", 5.0, \
            (lambda c, t, T, fn=fn, bg=bg, pair=pair: (bg(c, T), fn(c, "Life of Stars", "a calm sleep story", t / 5.0, pair)))
    for name, fn in ST.TRANSITIONS.items():
        yield f"transition: {name}", 3.5, (lambda c, t, T, fn=fn: fn(c, lambda cc: saturn(cc, T), lambda cc: nebula(cc, T),
                                                                     min(1, max(0, (t - 0.6) / 2.3))))
    for name, fn in ST.FX.items():
        yield f"effect: {name}", 4.0, (lambda c, t, T, fn=fn: (saturn(c, T), fn(c, T if fn is not ST.fx_shooting_star else t * 0.9, 1.0)))
    for name in ST.GRADES:
        yield f"colour grade: {name}", 3.0, (lambda c, t, T, name=name: (earth(c, T), ST.grade(c, name)))


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                           "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    T0 = 0.0
    for name, dur, draw in clips():
        for f in range(int(dur * FPS)):
            t = f / FPS
            c = cairo.Context(surf)
            c.set_source_rgb(0, 0, 0)
            c.paint()
            draw(c, t, T0 + t)
            label(c, name)
            surf.flush()
            ff.stdin.write(bytes(surf.get_data()))
        T0 += dur
    ff.stdin.close()
    ff.wait()
    print(OUT, round(T0, 1), "s")


if __name__ == "__main__":
    main()
