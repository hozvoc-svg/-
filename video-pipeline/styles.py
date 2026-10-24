"""Editing style library: font pairings, animated title styles, transitions, light effects and colour grades.

Every function draws onto a cairo context on the 1920x1080 canvas; `p` is progress 0..1 of the effect.
"""
import math, random
import cairo
import numpy as np
from scenes import W, H, clamp, ease

# ---------- font pairings (title font, subtitle font, mood) ----------
PAIRS = {
    "classic":   ("Cinzel", "Cormorant Garamond Light", "regal, timeless"),
    "storybook": ("Playfair Display", "Lora", "warm bedtime story"),
    "elegant":   ("Italiana", "Cormorant Light", "thin, airy, luxurious"),
    "decorative": ("Cinzel Decorative", "EB Garamond", "ornate, mythical"),
    "editorial": ("DM Serif Display", "Libre Baskerville", "magazine, documentary"),
    "ancient":   ("Marcellus", "Spectral Light", "museum, ancient worlds"),
    "modern":    ("Montserrat Thin", "Raleway Thin", "clean, minimal"),
    "geometric": ("Josefin Sans Thin", "Poppins Light", "calm modern"),
    "soft":      ("Comfortaa", "Quicksand Light", "rounded, gentle, cozy"),
    "scifi":     ("Orbitron", "Exo 2", "space station, futuristic"),
    "mission":   ("Michroma", "Space Grotesk Light", "NASA-style mission"),
    "wide":      ("Syncopate", "Tenor Sans", "wide spaced, cinematic"),
    "poster":    ("Bebas Neue", "Oswald", "bold YouTube thumbnail"),
    "impact":    ("Anton", "Poppins Medium", "loud thumbnail text"),
    "fatface":   ("Abril Fatface", "Alegreya", "retro poster"),
    "script":    ("Great Vibes", "Cormorant Garamond Light", "romantic handwriting"),
    "dreamy":    ("Parisienne", "Julius Sans One", "dreamy, delicate"),
    "handwritten": ("Caveat", "Nunito ExtraLight", "personal journal"),
    "chalk":     ("Amatic SC", "Philosopher", "hand-drawn, playful"),
    "dance":     ("Dancing Script", "Crimson Text", "warm, flowing"),
    "satisfy":   ("Satisfy", "Spectral Light", "casual elegant"),
    "audio":     ("Audiowide", "Exo 2", "retro-futuristic"),
}


def _font(c, family, size, bold=False, italic=False):
    c.select_font_face(family, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def _width(c, s, spacing=0.0):
    return sum(c.text_extents(ch).x_advance for ch in s) + spacing * max(0, len(s) - 1)


def _glyphs(c, s, x, y, col, a, spacing=0.0, per_char=None, shadow=0.6):
    """Draw text char by char; per_char(i, n) -> (alpha_mult, dy) lets styles animate each letter."""
    px = x
    n = len(s)
    for i, ch in enumerate(s):
        am, dy = per_char(i, n) if per_char else (1.0, 0.0)
        if shadow:
            c.move_to(px + 3, y + dy + 3)
            c.set_source_rgba(0, 0, 0.05, shadow * a * am)
            c.show_text(ch)
        c.move_to(px, y + dy)
        c.set_source_rgba(*col, a * am)
        c.show_text(ch)
        px += c.text_extents(ch).x_advance + spacing
    c.new_path()


# ---------- animated title styles: title(c, text, sub, p, pair) ----------

def title_fade(c, text, sub, p, pair="storybook", y=H * 0.45, col=(1, 0.95, 0.85)):
    """Soft fade in, hold, fade out."""
    f1, f2, _ = PAIRS[pair]
    a = ease(p / 0.2) * (1 - ease((p - 0.8) / 0.2))
    _font(c, f1, 110)
    _glyphs(c, text, W / 2 - _width(c, text) / 2, y, col, a)
    if sub:
        _font(c, f2, 46, italic=True)
        _glyphs(c, sub, W / 2 - _width(c, sub) / 2, y + 80, (0.85, 0.85, 0.95), a * 0.9)


def title_letters(c, text, sub, p, pair="classic", y=H * 0.45, col=(1, 0.92, 0.78)):
    """Letters rise and fade in one after another."""
    f1, f2, _ = PAIRS[pair]
    _font(c, f1, 104)
    sp = 6
    out = 1 - ease((p - 0.85) / 0.15)

    def pc(i, n):
        t = clamp((p * 1.6 - i / n * 0.6) / 0.4)
        return ease(t) * out, (1 - ease(t)) * 30
    _glyphs(c, text, W / 2 - _width(c, text, sp) / 2, y, col, 1.0, sp, pc)
    if sub:
        _font(c, f2, 44)
        a = ease((p - 0.45) / 0.2) * out
        _glyphs(c, sub, W / 2 - _width(c, sub) / 2, y + 80, (0.85, 0.88, 1.0), a)


def title_spacing(c, text, sub, p, pair="wide", y=H * 0.48, col=(1, 1, 1)):
    """Cinematic: letter spacing slowly widens while fading in."""
    f1, f2, _ = PAIRS[pair]
    a = ease(p / 0.3) * (1 - ease((p - 0.8) / 0.2))
    sp = 4 + 22 * ease(p)
    _font(c, f1, 70)
    _glyphs(c, text.upper(), W / 2 - _width(c, text.upper(), sp) / 2, y, col, a, sp)
    if sub:
        _font(c, f2, 30)
        _glyphs(c, sub.upper(), W / 2 - _width(c, sub.upper(), 8) / 2, y + 70, (0.75, 0.8, 0.95), a * 0.85, 8)


def title_typewriter(c, text, sub, p, pair="mission", y=H * 0.5, col=(0.75, 0.95, 1.0)):
    """Mission-log typewriter with a blinking cursor."""
    f1, f2, _ = PAIRS[pair]
    _font(c, f1, 58)
    n = int(len(text) * clamp(p / 0.6))
    shown = text[:n]
    x = W / 2 - _width(c, text) / 2
    a = 1 - ease((p - 0.85) / 0.15)
    _glyphs(c, shown, x, y, col, a, shadow=0)
    if int(p * 40) % 2 == 0 and p < 0.85:
        cx = x + _width(c, shown) + 8
        c.rectangle(cx, y - 48, 22, 56)
        c.set_source_rgba(*col, 0.8 * a)
        c.fill()
    if sub and p > 0.6:
        _font(c, f2, 30)
        _glyphs(c, sub, W / 2 - _width(c, sub) / 2, y + 70, (0.6, 0.75, 0.85), ease((p - 0.6) / 0.15) * a, shadow=0)


def title_lowerthird(c, text, sub, p, pair="editorial", col=(1, 1, 1)):
    """Documentary lower third: a thin line grows, the label slides in beside it."""
    f1, f2, _ = PAIRS[pair]
    a = 1 - ease((p - 0.85) / 0.15)
    lx, ly = 140, H - 210
    ln = 520 * ease(p / 0.25)
    c.set_source_rgba(1, 0.85, 0.6, 0.9 * a)
    c.rectangle(lx, ly, ln, 3)
    c.fill()
    s = ease((p - 0.1) / 0.25)
    _font(c, f1, 54)
    _glyphs(c, text, lx + 40 * (1 - s), ly - 22, col, s * a)
    if sub:
        _font(c, f2, 30, italic=True)
        _glyphs(c, sub, lx + 40 * (1 - s), ly + 52, (0.82, 0.82, 0.9), s * a * 0.9)


def title_script(c, text, sub, p, pair="script", y=H * 0.47, col=(1, 0.9, 0.8)):
    """Handwritten title revealed left-to-right like ink, with a soft glow."""
    f1, f2, _ = PAIRS[pair]
    _font(c, f1, 130)
    wdt = _width(c, text)
    x = W / 2 - wdt / 2
    reveal = ease(p / 0.5)
    a = 1 - ease((p - 0.85) / 0.15)
    g = cairo.RadialGradient(W / 2, y - 40, 10, W / 2, y - 40, wdt * 0.6)
    g.add_color_stop_rgba(0, 1, 0.85, 0.6, 0.14 * a * reveal)
    g.add_color_stop_rgba(1, 1, 0.85, 0.6, 0)
    c.set_source(g)
    c.arc(W / 2, y - 40, wdt * 0.6, 0, 2 * math.pi)
    c.fill()
    c.save()
    c.rectangle(x - 40, y - 160, (wdt + 80) * reveal, 240)
    c.clip()
    _glyphs(c, text, x, y, col, a, shadow=0.4)
    c.restore()
    if sub:
        _font(c, f2, 40)
        _glyphs(c, sub, W / 2 - _width(c, sub) / 2, y + 85, (0.85, 0.85, 0.95), ease((p - 0.45) / 0.2) * a)


def title_blur(c, text, sub, p, pair="elegant", y=H * 0.47, col=(1, 1, 1)):
    """Dreamy: several offset copies converge into one sharp title (fake focus pull)."""
    f1, f2, _ = PAIRS[pair]
    _font(c, f1, 120)
    wdt = _width(c, text)
    x = W / 2 - wdt / 2
    focus = ease(p / 0.45)
    a = 1 - ease((p - 0.85) / 0.15)
    spread = (1 - focus) * 18
    for k in range(8):
        ang = k * math.pi / 4
        c.move_to(x + math.cos(ang) * spread, y + math.sin(ang) * spread)
        c.set_source_rgba(*col, 0.10 * a * (0.3 + focus))
        c.show_text(text)
    c.move_to(x, y)
    c.set_source_rgba(*col, a * focus)
    c.show_text(text)
    c.new_path()
    if sub:
        _font(c, f2, 40)
        _glyphs(c, sub, W / 2 - _width(c, sub, 4) / 2, y + 80, (0.8, 0.85, 1.0), ease((p - 0.4) / 0.2) * a, 4)


def title_poster(c, text, sub, p, pair="poster", y=H * 0.5, col=(1, 0.88, 0.55)):
    """Bold thumbnail-style title with a punchy scale-in and a dark band."""
    f1, f2, _ = PAIRS[pair]
    s = 0.85 + 0.15 * ease(p / 0.15)
    a = ease(p / 0.1) * (1 - ease((p - 0.85) / 0.15))
    c.set_source_rgba(0, 0, 0, 0.45 * a)
    c.rectangle(0, y - 120, W, 200)
    c.fill()
    c.save()
    c.translate(W / 2, y)
    c.scale(s, s)
    _font(c, f1, 150)
    _glyphs(c, text.upper(), -_width(c, text.upper(), 4) / 2, 50, col, a, 4, shadow=0.8)
    c.restore()
    if sub:
        _font(c, f2, 36)
        _glyphs(c, sub.upper(), W / 2 - _width(c, sub.upper(), 6) / 2, y + 125, (1, 1, 1), a, 6)


TITLES = {"fade": title_fade, "letters": title_letters, "spacing": title_spacing, "typewriter": title_typewriter,
          "lowerthird": title_lowerthird, "script": title_script, "blur": title_blur, "poster": title_poster}


# ---------- transitions: draw scene B over A; transition(c, draw_a, draw_b, p) ----------

def _paint(c, draw):
    c.push_group()
    draw(c)
    return c.pop_group()


def tr_crossfade(c, a, b, p):
    a(c)
    c.set_source(_paint(c, b)); c.paint_with_alpha(ease(p))


def tr_dip_black(c, a, b, p):
    (a if p < 0.5 else b)(c)
    c.set_source_rgba(0, 0, 0, 1 - abs(ease(p) * 2 - 1)); c.paint()


def tr_dip_white(c, a, b, p):
    (a if p < 0.5 else b)(c)
    c.set_source_rgba(1, 0.97, 0.92, 1 - abs(ease(p) * 2 - 1)); c.paint()


def tr_zoom_through(c, a, b, p):
    """A zooms in and fades while B settles from slightly large to normal."""
    e = ease(p)
    c.save(); c.translate(W / 2, H / 2); c.scale(1 + 0.6 * e, 1 + 0.6 * e); c.translate(-W / 2, -H / 2)
    a(c); c.restore()
    pb = _paint(c, b)
    c.save(); c.translate(W / 2, H / 2); s = 1.25 - 0.25 * e; c.scale(s, s); c.translate(-W / 2, -H / 2)
    c.set_source(pb); c.paint_with_alpha(e); c.restore()


def tr_slide(c, a, b, p):
    """Gentle horizontal pan from A to B, like a camera drifting sideways."""
    e = ease(p)
    c.save(); c.translate(-W * e, 0); a(c); c.restore()
    c.save(); c.translate(W * (1 - e), 0); b(c); c.restore()


def tr_iris(c, a, b, p):
    """Circular reveal of B from the centre with a soft edge."""
    a(c)
    r = ease(p) * math.hypot(W, H) * 0.6
    g = cairo.RadialGradient(W / 2, H / 2, max(0, r - 120), W / 2, H / 2, r + 1)
    g.add_color_stop_rgba(0, 0, 0, 0, 1)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(_paint(c, b)); c.mask(g)


def tr_light_leak(c, a, b, p):
    """Warm film light leak washes across while crossfading."""
    tr_crossfade(c, a, b, p)
    x = -W * 0.3 + W * 1.6 * ease(p)
    g = cairo.LinearGradient(x - 500, 0, x + 500, H)
    k = math.sin(math.pi * p)
    g.add_color_stop_rgba(0, 1, 0.5, 0.2, 0)
    g.add_color_stop_rgba(0.5, 1, 0.75, 0.45, 0.55 * k)
    g.add_color_stop_rgba(1, 1, 0.5, 0.2, 0)
    c.set_source(g); c.paint()


def tr_star_wipe(c, a, b, p):
    """B is revealed through a growing field of soft star-shaped holes."""
    a(c)
    r = random.Random(3)
    c.push_group()
    for i in range(70):
        x, y = r.random() * W, r.random() * H
        rad = ease(clamp(p * 1.4 - r.random() * 0.4)) * 320
        g = cairo.RadialGradient(x, y, 0, x, y, rad + 1)
        g.add_color_stop_rgba(0, 0, 0, 0, 1)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.set_source(g); c.arc(x, y, rad + 1, 0, 2 * math.pi); c.fill()
    mask = c.pop_group()
    c.set_source(_paint(c, b)); c.mask(mask)


TRANSITIONS = {"crossfade": tr_crossfade, "dip_black": tr_dip_black, "dip_white": tr_dip_white,
               "zoom_through": tr_zoom_through, "slide": tr_slide, "iris": tr_iris,
               "light_leak": tr_light_leak, "star_wipe": tr_star_wipe}


# ---------- light & lens effects: fx(c, T, strength) ----------

def fx_lens_flare(c, T, s=1.0, x=W * 0.75, y=H * 0.25):
    for k, (d, r, col, al) in enumerate([(0, 160, (1, 0.9, 0.7), 0.35), (0.35, 40, (0.6, 0.8, 1.0), 0.25),
                                         (0.6, 70, (1, 0.6, 0.8), 0.15), (0.9, 25, (0.7, 1.0, 0.8), 0.2),
                                         (1.25, 110, (0.6, 0.7, 1.0), 0.10)]):
        px, py = x + (W / 2 - x) * d * 2, y + (H / 2 - y) * d * 2
        g = cairo.RadialGradient(px, py, 0, px, py, r)
        g.add_color_stop_rgba(0, *col, al * s * (0.85 + 0.15 * math.sin(T * 0.7 + k)))
        g.add_color_stop_rgba(1, *col, 0)
        c.set_source(g); c.arc(px, py, r, 0, 2 * math.pi); c.fill()
    c.set_line_width(3)
    g = cairo.LinearGradient(x - 600, y, x + 600, y)
    g.add_color_stop_rgba(0, 0.7, 0.85, 1, 0)
    g.add_color_stop_rgba(0.5, 0.8, 0.9, 1, 0.5 * s)
    g.add_color_stop_rgba(1, 0.7, 0.85, 1, 0)
    c.set_source(g); c.move_to(x - 600, y); c.line_to(x + 600, y); c.stroke()


def fx_god_rays(c, T, s=1.0, x=W * 0.2, y=-100):
    for k in range(9):
        ang = 0.35 + k * 0.11 + 0.02 * math.sin(T * 0.2 + k)
        L = 2200
        g = cairo.LinearGradient(x, y, x + math.cos(ang) * L, y + math.sin(ang) * L)
        g.add_color_stop_rgba(0, 1, 0.92, 0.75, 0.10 * s)
        g.add_color_stop_rgba(1, 1, 0.92, 0.75, 0)
        c.set_source(g)
        wdt = 0.025 + 0.015 * math.sin(k * 1.7)
        c.move_to(x, y)
        c.line_to(x + math.cos(ang - wdt) * L, y + math.sin(ang - wdt) * L)
        c.line_to(x + math.cos(ang + wdt) * L, y + math.sin(ang + wdt) * L)
        c.close_path(); c.fill()


def fx_bokeh(c, T, s=1.0, n=26, seed=4):
    r = random.Random(seed)
    for i in range(n):
        x = (r.random() * W + T * 6 * (0.5 + r.random())) % (W + 200) - 100
        y = r.random() * H + 20 * math.sin(T * 0.2 + i)
        rad = 20 + r.random() * 60
        col = r.choice([(1, 0.85, 0.6), (0.6, 0.75, 1.0), (1, 0.7, 0.85)])
        c.set_source_rgba(*col, (0.05 + 0.08 * r.random()) * s)
        c.arc(x, y, rad, 0, 2 * math.pi); c.fill()
        c.set_line_width(2); c.set_source_rgba(*col, 0.08 * s)
        c.arc(x, y, rad, 0, 2 * math.pi); c.stroke()


def fx_shooting_star(c, T, s=1.0, period=37.0, seed=1):
    r = random.Random(int(T // period) + seed)
    ph = (T % period) / 1.4
    if ph > 1:
        return
    x0, y0 = r.random() * W * 0.7 + W * 0.2, r.random() * H * 0.3
    ang = 2.5 + r.random() * 0.4
    L = 500
    hx, hy = x0 + math.cos(ang) * L * ph, y0 + math.sin(ang) * L * ph
    g = cairo.LinearGradient(hx, hy, hx - math.cos(ang) * 220, hy - math.sin(ang) * 220)
    a = math.sin(math.pi * ph) * s
    g.add_color_stop_rgba(0, 1, 1, 1, 0.9 * a)
    g.add_color_stop_rgba(1, 0.7, 0.85, 1, 0)
    c.set_source(g); c.set_line_width(2.5)
    c.move_to(hx, hy); c.line_to(hx - math.cos(ang) * 220, hy - math.sin(ang) * 220); c.stroke()


def fx_film_grain(c, T, s=1.0):
    rng = np.random.default_rng(int(T * 24) % 97)
    h, w = H // 3, W // 3
    n = (rng.random((h, w)) * 255).astype(np.uint8)
    buf = np.zeros((h, w, 4), np.uint8)
    buf[..., 3] = (n * 0.35).astype(np.uint8)
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h)
    c.save(); c.scale(3, 3); c.set_source_surface(surf, 0, 0); c.paint_with_alpha(0.12 * s); c.restore()
    surf.finish()


def fx_letterbox(c, T, s=1.0):
    bar = 130 * s
    c.set_source_rgb(0, 0, 0)
    c.rectangle(0, 0, W, bar); c.rectangle(0, H - bar, W, bar); c.fill()


def fx_vignette_soft(c, T, s=1.0):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.65 * s)
    c.set_source(g); c.paint()


FX = {"lens_flare": fx_lens_flare, "god_rays": fx_god_rays, "bokeh": fx_bokeh, "shooting_star": fx_shooting_star,
      "film_grain": fx_film_grain, "letterbox": fx_letterbox, "vignette": fx_vignette_soft}


# ---------- colour grades: a translucent wash over the frame ----------

GRADES = {
    "warm_dream": [((1.0, 0.65, 0.35), cairo.OPERATOR_SOFT_LIGHT, 0.35)],
    "cool_night": [((0.25, 0.45, 0.9), cairo.OPERATOR_SOFT_LIGHT, 0.40)],
    "teal_orange": [((0.1, 0.55, 0.6), cairo.OPERATOR_SOFT_LIGHT, 0.25), ((1.0, 0.6, 0.3), cairo.OPERATOR_OVERLAY, 0.10)],
    "faded_film": [((0.9, 0.85, 0.75), cairo.OPERATOR_SCREEN, 0.12), ((0.4, 0.3, 0.25), cairo.OPERATOR_SOFT_LIGHT, 0.2)],
    "violet_haze": [((0.6, 0.35, 0.9), cairo.OPERATOR_SOFT_LIGHT, 0.35)],
    "golden_hour": [((1.0, 0.8, 0.4), cairo.OPERATOR_OVERLAY, 0.18)],
}


def grade(c, name, s=1.0):
    for col, op, al in GRADES[name]:
        c.save(); c.set_operator(op); c.set_source_rgba(*col, al * s); c.paint(); c.restore()
