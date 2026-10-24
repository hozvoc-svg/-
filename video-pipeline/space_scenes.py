"""Space scenes for Sleepy Cosmos: rotating textured planets (numpy sphere renderer), the Sun, asteroid belt,
Voyager, Oort cloud and the pale blue dot, over slowly drifting star fields and nebulae."""
import math, random
import numpy as np
import cairo
import space_art as A
from scenes import W, H, clamp, ease, prog, rgba, text_w, rrect

INK = (1, 1, 1)
BG1 = (0.01, 0.01, 0.04)
_tex, _bg, _grids = {}, {}, {}


def snowfall(c, T, amount=1.0, wind=1.0):
    pass


def text(c, s, x, y, size=48, col=INK, a=1.0, align="center", bold=True, italic=False):
    A.text(c, s, x, y, size, col, a, bold=bold, italic=italic)


# ---------- textures (equirectangular, RGB float 0..1) ----------

def _n(h, w, seed, oct=6, pers=0.55):
    return A.fractal_noise(h, w, seed, oct, pers)


def _lerp(a, b, t):
    return a + (b - a) * t[..., None]


def _craters(img, seed, n, dark=0.75, rim=1.15, rmax=0.05):
    h, w, _ = img.shape
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    for _ in range(n):
        cx, cy = r.random() * w, h * (0.1 + 0.8 * r.random())
        rad = (r.random() ** 3 * rmax + 0.004) * w
        d = np.sqrt(((xx - cx + w / 2) % w - w / 2) ** 2 * (math.cos((cy / h - 0.5) * math.pi) ** 2) + (yy - cy) ** 2) / rad
        f = np.where(d < 1, dark + (1 - dark) * d ** 2, np.where(d < 1.25, rim, 1.0))
        img *= f[..., None]
    return img


def texture(body):
    if body in _tex:
        return _tex[body]
    h, w = 512, 1024
    lat = np.linspace(-1, 1, h)[:, None] * np.ones((1, w))
    if body in ("mercury", "moon", "ceres", "callisto"):
        n = _n(h, w, 11 if body == "mercury" else 23)
        base = np.array({"mercury": (0.55, 0.52, 0.50), "moon": (0.62, 0.62, 0.64),
                         "ceres": (0.45, 0.44, 0.43), "callisto": (0.35, 0.32, 0.30)}[body])
        img = base * (0.75 + 0.5 * n[..., None])
        img = _craters(img, 5, 140 if body != "ceres" else 60)
        if body == "ceres":
            img = np.where((_n(h, w, 99) > 0.78)[..., None], np.array([0.95, 0.95, 0.92]), img)
    elif body == "venus":
        n = _n(h, w // 4 + 1, 3, 5)
        n = np.repeat(n, 4, axis=1)[:, :w] * 0.6 + 0.4 * _n(h, w, 4, 4)
        img = _lerp(np.array([0.85, 0.70, 0.45]), np.array([0.98, 0.92, 0.75]), n)
    elif body == "earth":
        land = _n(h, w, 7, 7) > 0.53
        n = _n(h, w, 8)
        ocean = _lerp(np.array([0.02, 0.10, 0.32]), np.array([0.05, 0.25, 0.55]), n)
        green = _lerp(np.array([0.15, 0.35, 0.12]), np.array([0.55, 0.45, 0.25]), _n(h, w, 9))
        img = np.where(land[..., None], green, ocean)
        ice = np.abs(lat) > 0.86
        img = np.where(ice[..., None], np.array([0.92, 0.95, 0.98]), img)
    elif body == "clouds":
        n = _n(h, w, 31, 7)
        img = np.clip((n - 0.5) * 3.0, 0, 1)
        return _tex.setdefault(body, img.astype(np.float32))
    elif body == "mars":
        n = _n(h, w, 12)
        img = _lerp(np.array([0.55, 0.22, 0.10]), np.array([0.82, 0.45, 0.25]), n)
        dark = _n(h, w, 13) > 0.6
        img = np.where(dark[..., None], img * 0.65, img)
        img = np.where((np.abs(lat) > 0.9)[..., None], np.array([0.95, 0.93, 0.90]), img)
    elif body in ("jupiter", "saturn"):
        warp = _n(h, w, 21, 5) * 0.08
        y = np.clip(lat + warp, -1, 1)
        stripes = 0.5 + 0.5 * np.sin(y * (22 if body == "jupiter" else 30) + 2.0 * _n(h, w, 22, 3))
        if body == "jupiter":
            img = _lerp(np.array([0.62, 0.42, 0.28]), np.array([0.96, 0.90, 0.80]), stripes)
            yy, xx = np.mgrid[0:h, 0:w]
            d = ((xx - w * 0.3) / (w * 0.045)) ** 2 + ((yy - h * 0.62) / (h * 0.045)) ** 2
            img = np.where((d < 1)[..., None], _lerp(np.array([0.75, 0.30, 0.18]), np.array([0.85, 0.50, 0.35]), np.clip(d, 0, 1)), img)
        else:
            img = _lerp(np.array([0.78, 0.66, 0.45]), np.array([0.95, 0.88, 0.70]), stripes)
    elif body == "uranus":
        n = _n(h, w, 41, 4)
        img = _lerp(np.array([0.55, 0.80, 0.82]), np.array([0.70, 0.90, 0.92]), 0.6 * n + 0.4 * (0.5 + 0.5 * np.sin(lat * 8)))
    elif body == "neptune":
        n = _n(h, w, 51, 6)
        img = _lerp(np.array([0.10, 0.22, 0.65]), np.array([0.25, 0.45, 0.90]), n * 0.6 + 0.4 * (0.5 + 0.5 * np.sin(lat * 10)))
        streak = (_n(h, w // 6 + 1, 52, 4) > 0.7)
        streak = np.repeat(streak, 6, axis=1)[:, :w]
        img = np.where(streak[..., None], np.array([0.85, 0.90, 1.0]), img)
    elif body == "pluto":
        n = _n(h, w, 61)
        img = _lerp(np.array([0.45, 0.32, 0.22]), np.array([0.85, 0.75, 0.62]), n)
        yy, xx = np.mgrid[0:h, 0:w]
        hx, hy = (xx - w * 0.55) / (w * 0.07), (yy - h * 0.52) / (h * 0.14)
        lobes = ((hx + 0.55) ** 2 + (hy + 0.35) ** 2 < 0.45) | ((hx - 0.55) ** 2 + (hy + 0.35) ** 2 < 0.45)
        point = (hy > -0.35) & (hy < 1.1) & (np.abs(hx) < (1.1 - hy) * 0.95)
        heart = lobes | point
        img = np.where(heart[..., None], np.array([0.93, 0.88, 0.80]) * (0.9 + 0.1 * n[..., None]), img)
    elif body == "sun":
        n = _n(h, w, 71, 7, 0.65)
        img = _lerp(np.array([1.0, 0.55, 0.12]), np.array([1.0, 0.92, 0.55]), n)
    else:  # small icy / rocky moons
        n = _n(h, w, hash(body) % 1000)
        img = np.array([0.75, 0.75, 0.78]) * (0.7 + 0.5 * n[..., None])
    _tex[body] = np.clip(img, 0, 1).astype(np.float32)
    return _tex[body]


# ---------- sphere renderer ----------

def _grid(R, tilt):
    key = (R, round(tilt, 3))
    if key not in _grids:
        ys, xs = np.mgrid[-R:R, -R:R].astype(np.float32) + 0.5
        x, y = xs / R, ys / R
        rr = x * x + y * y
        inside = rr < 1
        z = np.sqrt(np.clip(1 - rr, 0, 1))
        ct, st = math.cos(tilt), math.sin(tilt)
        xr, yr = x * ct + y * st, -x * st + y * ct  # axis tilt in the view plane
        lat = np.arcsin(np.clip(yr, -1, 1))
        lon = np.arctan2(xr, z)
        edge = np.clip((1 - np.sqrt(rr)) * R * 0.8, 0, 1)
        _grids[key] = (x, y, z, lat, lon, inside, edge)
    return _grids[key]


def sphere(body, R, phase, light=(-0.55, -0.35, 0.75), tilt=0.15, emissive=False, clouds_phase=None, night=0.0):
    """Return a cairo ImageSurface (2R x 2R) of a lit rotating planet with antialiased edge."""
    tex = texture(body)
    th, tw, _ = tex.shape
    x, y, z, lat, lon, inside, edge = _grid(R, tilt)
    u = ((lon / (2 * math.pi) + phase) % 1.0) * (tw - 1)
    v = (lat / math.pi + 0.5) * (th - 1)
    col = tex[v.astype(np.int32), u.astype(np.int32)]
    if clouds_phase is not None:
        ct = texture("clouds")
        uc = ((lon / (2 * math.pi) + clouds_phase) % 1.0) * (tw - 1)
        cl = ct[v.astype(np.int32), uc.astype(np.int32)][..., None]
        col = col * (1 - cl * 0.85) + cl * 0.95
    if emissive:
        shade = (0.55 + 0.45 * z ** 0.5)[..., None]
        col = np.clip(col * shade * 1.05, 0, 1)
    else:
        L = np.array(light, np.float32)
        L /= np.linalg.norm(L)
        d = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)
        lit = (0.04 + 0.96 * d ** 0.9) * (1 - night * 0.6)
        col = col * lit[..., None]
    a = np.where(inside, edge, 0).astype(np.float32)
    buf = np.zeros(col.shape[:2] + (4,), np.uint8)
    buf[..., 2] = (col[..., 0] * a * 255).astype(np.uint8)
    buf[..., 1] = (col[..., 1] * a * 255).astype(np.uint8)
    buf[..., 0] = (col[..., 2] * a * 255).astype(np.uint8)
    buf[..., 3] = (a * 255).astype(np.uint8)
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, 2 * R, 2 * R)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * R, 2 * R)
    cc = cairo.Context(out)
    cc.set_source_surface(surf, 0, 0)
    cc.paint()
    out.flush()
    return out


def paint_sphere(c, body, cx, cy, R, phase, **kw):
    s = sphere(body, R, phase, **kw)
    c.set_source_surface(s, cx - R, cy - R)
    c.paint()


# ---------- backgrounds ----------

def backdrop(seed):
    """Big static star+nebula plate (2400x1350) we pan slowly over."""
    if seed not in _bg:
        w, h = 2400, 1350
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        c = cairo.Context(s)
        A.background(c, w, h, (0.01, 0.01, 0.04), (0.03, 0.02, 0.08))
        palettes = [((0.20, 0.10, 0.45), (0.10, 0.35, 0.60), (0.75, 0.25, 0.55)),
                    ((0.10, 0.25, 0.50), (0.05, 0.40, 0.45), (0.30, 0.15, 0.50)),
                    ((0.45, 0.15, 0.30), (0.20, 0.10, 0.40), (0.60, 0.35, 0.20))]
        neb = A.nebula_surface(w, h, seed=seed * 3 + 1, colors=palettes[seed % 3], strength=0.75)
        c.set_source_surface(neb, 0, 0)
        c.paint_with_alpha(0.7)
        A.stars(c, w, h, n=1600, seed=seed + 40)
        s.flush()
        _bg[seed] = s
    return _bg[seed]


def draw_backdrop(c, seed, T, speed=4.0, alpha=1.0):
    s = _bg.get(seed) or backdrop(seed)
    ox = -((T * speed) % (2400 - W))
    oy = -60 - 40 * math.sin(T * 0.01)
    c.set_source_surface(s, ox, oy)
    c.paint_with_alpha(alpha)


def twinkle(c, T, n=60, seed=1):
    r = random.Random(seed)
    for i in range(n):
        x, y = r.random() * W, r.random() * H
        a = 0.5 + 0.5 * math.sin(T * (0.6 + r.random()) + i * 1.7)
        A.glow(c, x, y, 5 + 4 * r.random(), (0.85, 0.9, 1.0), 0.35 * a)


# ---------- scenes: f(c, t, d, T, args) ----------

def sc_title(c, t, d, T, a):
    draw_backdrop(c, 0, T)
    twinkle(c, T)
    ap = prog(t, 1.0, 4.0) * (1 - prog(t, d - 4, d - 1))
    A.crescent(c, W / 2 - 360, 330, 70)
    text(c, "Sleepy Cosmos", W / 2, 470, 120, INK, ap)
    text(c, "A Calm Journey Through the Solar System", W / 2, 580, 52, (1, 0.9, 0.7), ap, bold=False, italic=True)


def sc_travel(c, t, d, T, a):
    draw_backdrop(c, a.get("neb", 1), T, speed=6 if not a.get("slow") else 2.5)
    warp = a.get("warp", 0.25)
    r = random.Random(7)
    for i in range(140):
        ang = r.random() * 2 * math.pi
        sp = 0.05 + 0.25 * r.random()
        f = ((T * sp * warp + r.random()) % 1.0)
        dist = 40 + f ** 2 * 1300
        x = W / 2 + math.cos(ang) * dist
        y = H / 2 + math.sin(ang) * dist * 0.6
        rgba(c, (0.9, 0.93, 1.0), 0.15 + 0.7 * f)
        c.arc(x, y, 0.6 + 2.2 * f, 0, 2 * math.pi)
        c.fill()
    twinkle(c, T, 40, 3)
    fo = a.get("fade_out", 0)
    if fo and t > d - fo:
        rgba(c, (0, 0, 0), ease((t - (d - fo)) / fo))
        c.paint()


def sc_sun(c, t, d, T, a):
    draw_backdrop(c, 2, T, 2)
    z = a.get("zoom", 1.0) + 0.06 * t / d
    R = int(300 * z)
    cx, cy = W * 0.5, H * 0.52
    A.glow(c, cx, cy, R * 3.4, (1.0, 0.55, 0.15), 0.35)
    A.glow(c, cx, cy, R * 1.8, (1.0, 0.75, 0.35), 0.55)
    # corona streamers
    for i in range(18):
        ang = i * 2 * math.pi / 18 + 0.05 * math.sin(T * 0.1 + i)
        L = R * (1.35 + 0.35 * math.sin(T * 0.2 + i * 1.3))
        g = cairo.LinearGradient(cx, cy, cx + math.cos(ang) * L, cy + math.sin(ang) * L)
        g.add_color_stop_rgba(0, 1, 0.8, 0.45, 0.25)
        g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
        c.set_source(g)
        c.move_to(cx + math.cos(ang - 0.08) * R, cy + math.sin(ang - 0.08) * R)
        c.line_to(cx + math.cos(ang) * L, cy + math.sin(ang) * L)
        c.line_to(cx + math.cos(ang + 0.08) * R, cy + math.sin(ang + 0.08) * R)
        c.fill()
    paint_sphere(c, "sun", cx, cy, R, T * 0.004, emissive=True, tilt=0.1)
    # prominence loops
    for k in range(3):
        ang = -2.2 + k * 1.9 + 0.1 * math.sin(T * 0.05 + k)
        h = 0.18 + 0.06 * math.sin(T * 0.3 + k)
        c.set_line_width(R * 0.07)
        c.set_source_rgba(1.0, 0.55, 0.20, 0.18)
        x0, y0 = cx + math.cos(ang - 0.12) * R, cy + math.sin(ang - 0.12) * R
        x1, y1 = cx + math.cos(ang + 0.12) * R, cy + math.sin(ang + 0.12) * R
        mx, my = cx + math.cos(ang) * R * (1 + h * 2), cy + math.sin(ang) * R * (1 + h * 2)
        c.move_to(x0, y0)
        c.curve_to(mx, my, mx, my, x1, y1)
        c.stroke_preserve()
        c.set_line_width(R * 0.025)
        c.set_source_rgba(1.0, 0.70, 0.35, 0.30)
        c.stroke()


MOON_COLS = {"mars": ["phobos", "deimos"], "jupiter": ["io", "europa", "ganymede", "callisto"],
             "saturn": ["titan"], "uranus": ["miranda", "ariel", "titania"], "neptune": ["triton"], "pluto": ["charon"]}
MOON_TINT = {"io": (1.0, 0.85, 0.35), "europa": (0.92, 0.88, 0.80), "ganymede": (0.65, 0.60, 0.55),
             "callisto": (0.40, 0.36, 0.33), "titan": (0.95, 0.65, 0.30), "triton": (0.85, 0.80, 0.78),
             "charon": (0.60, 0.58, 0.58), "phobos": (0.45, 0.40, 0.38), "deimos": (0.55, 0.50, 0.45),
             "miranda": (0.70, 0.70, 0.72), "ariel": (0.75, 0.75, 0.78), "titania": (0.68, 0.66, 0.66)}


def small_moon(c, x, y, r, col, light=(-0.55, -0.35)):
    A.planet(c, x, y, r, base=col, dark=tuple(v * 0.12 for v in col), light_dir=light, atm=0.0)


def sc_planet(c, t, d, T, a):
    body = a["body"]
    draw_backdrop(c, hash(body) % 6, T, 3)
    twinkle(c, T, 30, hash(body) % 50)
    R = int(a.get("size", 360) * (1 + 0.05 * t / d))
    cx = W * a.get("x", 0.55) + 30 * math.sin(t / d * math.pi)
    cy = H * 0.52
    tilt = a.get("tilt", 0.12)
    spin = {"jupiter": 0.012, "saturn": 0.010, "venus": -0.002, "uranus": 0.006, "neptune": 0.008}.get(body, 0.005)
    light = (-0.6, -0.3, 0.72)
    if a.get("rings"):
        rc = (0.92, 0.85, 0.70) if body == "saturn" else (0.55, 0.62, 0.65)
        ang = (-0.35 if body == "saturn" else tilt)
        A.rings(c, cx, cy, R, tilt=0.28 if body == "saturn" else 0.12, angle=ang, col=rc, front=False)
    A.glow(c, cx, cy, R * 1.25, {"earth": (0.4, 0.6, 1.0), "venus": (1, 0.9, 0.6), "mars": (1, 0.6, 0.4),
                                 "uranus": (0.6, 0.9, 1.0), "neptune": (0.4, 0.6, 1.0)}.get(body, (0.8, 0.8, 0.85)), 0.22)
    paint_sphere(c, body, cx, cy, R, T * spin, light=light, tilt=tilt, night=a.get("night", 0))
    if a.get("rings"):
        rc = (0.92, 0.85, 0.70) if body == "saturn" else (0.55, 0.62, 0.65)
        ang = (-0.35 if body == "saturn" else tilt)
        A.rings(c, cx, cy, R, tilt=0.28 if body == "saturn" else 0.12, angle=ang, col=rc, front=True)
    n = a.get("moons", 0)
    for k, mname in enumerate(MOON_COLS.get(body, [])[:n]):
        orb = R * (1.6 + 0.45 * k)
        ph = T * (0.03 / (1 + k)) + k * 2.1
        mx = cx + math.cos(ph) * orb
        my = cy + math.sin(ph) * orb * 0.28
        if math.sin(ph) < 0 and abs(mx - cx) < R:
            continue  # behind the planet
        small_moon(c, mx, my, max(6, R * (0.07 if body != "pluto" else 0.5) * (1.4 if mname in ("ganymede", "titan") else 1)),
                   MOON_TINT.get(mname, (0.7, 0.7, 0.7)))


def sc_earth(c, t, d, T, a):
    draw_backdrop(c, 4, T, 2.5)
    twinkle(c, T, 30, 9)
    z = a.get("zoom", 1.0) + 0.05 * t / d
    R = int(320 * z)
    cx, cy = W * 0.45, H * 0.52
    A.glow(c, cx, cy, R * 1.25, (0.4, 0.65, 1.0), 0.35)
    paint_sphere(c, "earth", cx, cy, R, T * 0.004, light=(-0.6, -0.3, 0.72), tilt=0.41,
                 clouds_phase=T * 0.0055, night=a.get("night", 0))
    mR = int(R * 0.27)
    mx = cx + R * 2.2 + 40 * math.sin(T * 0.01)
    my = cy - R * 0.35
    if a.get("moon_focus"):
        mx, my, mR = cx + R * 1.75, cy - R * 0.25, int(R * 0.36)
    paint_sphere(c, "moon", mx, my, mR, 0.25, light=(-0.6, -0.3, 0.72), tilt=0.05)


def sc_belt(c, t, d, T, a):
    draw_backdrop(c, 5, T, 2)
    r = random.Random(4)
    rocks = []
    for i in range(170):
        depth = r.random()
        rocks.append((depth, r.random(), r.random(), r.random() * 6, [0.6 + 0.4 * r.random() for _ in range(9)]))
    rocks.sort()
    if a.get("ceres"):
        paint_sphere(c, "ceres", W * 0.68, H * 0.45, 170, T * 0.006, light=(-0.6, -0.3, 0.72))
    for depth, rx, ry, ph, shape in rocks:
        size = 3 + depth ** 3 * 70
        speed = 8 + depth * 60
        x = (rx * (W + 400) - T * speed) % (W + 400) - 200
        y = ry * H + 30 * math.sin(T * 0.02 + ph)
        rot = T * (0.05 + 0.2 * depth) + ph
        c.save()
        c.translate(x, y)
        c.rotate(rot)
        c.move_to(size * shape[0], 0)
        for k in range(1, 9):
            ang = k * 2 * math.pi / 9
            c.line_to(math.cos(ang) * size * shape[k], math.sin(ang) * size * shape[k] * 0.8)
        c.close_path()
        g = cairo.LinearGradient(-size, -size, size, size)
        b = 0.25 + 0.35 * depth
        g.add_color_stop_rgb(0, b * 1.4, b * 1.3, b * 1.2)
        g.add_color_stop_rgb(1, b * 0.25, b * 0.22, b * 0.2)
        c.set_source(g)
        c.fill()
        c.restore()


def voyager(c, x, y, s, rot):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    c.set_line_width(3)
    # dish
    c.save(); c.scale(1, 0.35)
    g = cairo.RadialGradient(-10, -20, 5, 0, 0, 90)
    g.add_color_stop_rgb(0, 0.95, 0.95, 0.92)
    g.add_color_stop_rgb(1, 0.55, 0.55, 0.55)
    c.set_source(g)
    c.arc(0, 0, 90, 0, 2 * math.pi)
    c.fill()
    c.restore()
    c.set_source_rgb(0.75, 0.72, 0.65)
    c.rectangle(-28, 10, 56, 34)
    c.fill()
    c.set_source_rgb(0.85, 0.65, 0.25)
    c.arc(18, 28, 8, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(0.7, 0.7, 0.72)
    for (x1, y1, x2, y2) in [(-28, 30, -230, 80), (28, 30, 160, 110), (0, 44, 20, 180)]:
        c.move_to(x1, y1); c.line_to(x2, y2); c.stroke()
    c.rectangle(-250, 70, 30, 22); c.fill()
    c.restore()


def sc_voyager(c, t, d, T, a):
    draw_backdrop(c, 1, T, 1.5)
    twinkle(c, T, 50, 21)
    z = a.get("zoom", 1.0)
    A.glow(c, W * 0.12, H * 0.3, 90, (1, 0.9, 0.7), 0.6)
    A.glow(c, W * 0.12, H * 0.3, 10, (1, 1, 1), 1.0)
    voyager(c, W * 0.55 + 40 * t / d, H * 0.55 - 20 * t / d, 1.6 * z, -0.25 + 0.03 * math.sin(T * 0.05))


def sc_oort(c, t, d, T, a):
    draw_backdrop(c, 3, T, 1.0, 0.7)
    z = a.get("zoom", 1.0) * (1 - 0.15 * t / d)
    cx, cy = W / 2, H / 2
    A.glow(c, cx, cy, 30, (1, 0.9, 0.7), 0.8)
    r = random.Random(12)
    for i in range(900):
        th = r.random() * 2 * math.pi
        ph = math.acos(2 * r.random() - 1)
        rad = (420 + 120 * r.random()) * z
        rot = T * 0.004
        x = rad * math.sin(ph) * math.cos(th + rot)
        y = rad * math.cos(ph) * 0.9
        zz = rad * math.sin(ph) * math.sin(th + rot)
        a_ = 0.25 + 0.5 * (zz / rad + 1) / 2
        rgba(c, (0.75, 0.85, 1.0), a_)
        c.arc(cx + x, cy + y, 1.2 + 0.8 * r.random(), 0, 2 * math.pi)
        c.fill()


def sc_dot(c, t, d, T, a):
    rgba(c, (0.01, 0.01, 0.02))
    c.paint()
    twinkle(c, T, 25, 33)
    for k, (x, wd, al) in enumerate([(0.30, 70, 0.10), (0.52, 110, 0.13), (0.70, 60, 0.08)]):
        g = cairo.LinearGradient(W * x - wd, 0, W * x + wd, 0)
        g.add_color_stop_rgba(0, 0.9, 0.6, 0.4, 0)
        g.add_color_stop_rgba(0.5, 0.95, 0.70, 0.55, al + 0.02 * math.sin(T * 0.1 + k))
        g.add_color_stop_rgba(1, 0.9, 0.6, 0.4, 0)
        c.save(); c.translate(W * x, H / 2); c.rotate(0.18); c.translate(-W * x, -H / 2)
        c.set_source(g); c.rectangle(W * x - wd, -400, 2 * wd, H + 800); c.fill(); c.restore()
    z = a.get("zoom", 1.0)
    A.glow(c, W * 0.535, H * 0.58, 14 * z, (0.55, 0.75, 1.0), 0.7)
    rgba(c, (0.75, 0.88, 1.0))
    c.arc(W * 0.535, H * 0.58, 2.2 * z, 0, 2 * math.pi)
    c.fill()


def sc_outro(c, t, d, T, a):
    draw_backdrop(c, 0, T, 2)
    twinkle(c, T)
    ap = prog(t, 0.5, 3.0) * (1 - prog(t, d - 4, d - 1))
    A.crescent(c, W / 2, 360, 80)
    text(c, "Sleep well", W / 2, 560, 96, INK, ap)
    text(c, "New calm space journeys every week", W / 2, 650, 40, (1, 0.9, 0.7), ap, bold=False, italic=True)
    fo = a.get("fade_out", 0)
    if fo:
        rgba(c, (0, 0, 0), ease((t - (d - fo)) / fo))
        c.paint()


def vignette(c):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.5, W / 2, H / 2, H * 1.15)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.45)
    c.set_source(g)
    c.rectangle(-400, -600, W + 800, H + 1200)
    c.fill()


SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}
