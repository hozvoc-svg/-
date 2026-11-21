"""Bounce Lab "LEVEL 1-7": seven different physics challenges, each with its own mechanic, colour theme and
public-domain melody (so the channel isn't a pile of near-identical videos).

    python3 sims/levels.py N        -> out/level_0N.mp4 + out/level_0N_cover.png
"""
import math, os, sys
import numpy as np
import cairo
import escape as E
import lab as L
from lab import W, H, FPS, CX, CY

SUBDT = 10


def _done(S, t):
    return S["done_at"] is not None and t >= S["done_at"]


def ball(c, x, y, r, colr, glow=True):
    if glow:
        g = cairo.RadialGradient(x, y, 2, x, y, r * 3.5)
        g.add_color_stop_rgba(0, *colr, 0.5)
        g.add_color_stop_rgba(1, *colr, 0)
        c.set_source(g)
        c.arc(x, y, r * 3.5, 0, 2 * math.pi)
        c.fill()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgb(*colr)
    c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.9)
    c.set_line_width(max(2, r * 0.12))
    c.stroke()


def timer(c, S, t, y=1660):
    tt = min(t, S["done_at"]) if S["done_at"] else t
    E.text(c, f"{tt:5.1f}s", W / 2, y, 54, (0.78, 0.78, 0.88), outline=0.1)


# =============================================================== rings (levels 1 and 7)
def sim_rings(seed, **kw):
    R = E.simulate(seed, fast_start=True, tail=2.5, **kw)
    ev = [(t, "note", 0) if k == "bounce" else (t, "break", i) for t, k, i in R["events"]]
    if R["done_at"]:
        ev.append((R["done_at"], "end", 0))
    R["events"] = ev
    return R


def draw_rings(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    n = S["rings"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    c.save()
    kick = max([0.0] + [1 - (t - b) / 0.15 for b in S["broken"] if b is not None and 0 <= t - b < 0.15])
    if kick:
        z = 1 + 0.03 * kick
        c.translate(CX + 8 * kick * math.sin(t * 90), CY + 8 * kick * math.cos(t * 70)); c.scale(z, z); c.translate(-CX, -CY)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    active = next((j for j in range(n) if S["broken"][j] is None or S["broken"][j] > t), -1)
    thick = 12 if n < 20 else 7
    for i in range(n):
        colr = L.col(th, i, n)
        b = S["broken"][i]
        if b is not None and b <= t:
            age = t - b
            if age < 1.3:
                for x, y, vx, vy, sz in E.shards(i, S["radii"][i], f["angles"][i], S["seed"]):
                    c.set_source_rgba(*colr, 1 - age / 1.3)
                    c.rectangle(CX + x + vx * age - sz / 2, CY + y + vy * age + 900 * age * age - sz / 2, sz, sz)
                    c.fill()
            continue
        a0 = f["angles"][i] + S["gaps"][i] / 2
        a1 = f["angles"][i] - S["gaps"][i] / 2 + 2 * math.pi
        for lw, al in ((thick * 2.5, 0.10), (thick * 1.6, 0.18), (thick, 1.0)):
            c.set_source_rgba(*colr, al * (1.0 if i == active else 0.7))
            c.set_line_width(lw)
            c.new_path()
            c.arc(CX, CY, S["radii"][i], a0, a1)
            c.stroke()
    br = S["ball_r"]
    for k in range(12, 0, -1):
        q = S["frames"][max(0, fi - k)]["p"]
        c.set_source_rgba(*th["acc"], 0.25 * (1 - k / 12))
        c.arc(CX + q[0], CY + q[1], br * (1 - 0.5 * k / 12), 0, 2 * math.pi)
        c.fill()
    ball(c, CX + f["p"][0], CY + f["p"][1], br, (1, 1, 1))
    c.restore()
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    left = sum(1 for b in S["broken"] if b is None or b > t)
    if _done(S, t):
        L.big_result(c, "ESCAPED!", S["done_at"], t, (0.35, 1.0, 0.5))
    else:
        E.text(c, f"RINGS LEFT: {left}", W / 2, 1560, 76, (1, 1, 1))
    timer(c, S, t)


# =============================================================== level 2: the ball grows with every bounce
def sim_grow(seed=2, R=430, r0=22, grow=3.2, g=1400.0, vmin=900.0):
    rng = np.random.default_rng(seed)
    p = np.array([rng.uniform(-80, 80), -120.0])
    v = np.array([rng.uniform(-800, 800), -400.0])
    r, nb = r0, 0
    marks, frames, events = [], [], []
    dt = 1 / FPS / SUBDT
    t, last, lastnote, done = 0.0, -1, -1, None
    while True:
        for _ in range(SUBDT):
            t += dt
            if done is not None:
                continue
            v[1] += g * dt
            p += v * dt
            d = math.hypot(*p)
            lim = R - r
            if d >= lim:
                n = p / d
                v = v - 2 * np.dot(v, n) * n
                a = rng.normal(0, 0.05)
                v = np.array([v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a)])
                sp = math.hypot(*v)
                if sp < vmin:
                    v *= vmin / sp
                p = n * (lim - 0.5)
                if t - last > 0.035:
                    r = min(R - 4, r + grow * (1 + 0.5 * (r / R)))
                    nb += 1
                    marks.append((p[0] + n[0] * 0, p[1], r, nb))
                    last = t
                    if t - lastnote > 0.07:
                        events.append((t, "note", 0)); lastnote = t
                if r >= R - 8:
                    done = t
                    events.append((t, "end", 0))
                    events.append((t, "break", 3))
        frames.append(dict(t=t, p=p.copy(), r=r, nb=nb, nm=len(marks)))
        if (done is not None and t > done + 2.5) or t > 70:
            break
    return dict(frames=frames, events=events, marks=marks, R=R, r0=r0, done_at=done)


def draw_grow(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    R = S["R"]
    cy = CY + 40
    for x, y, r, k in S["marks"][max(0, f["nm"] - 90):f["nm"]]:
        colr = L.col(th, k % 24, 24)
        c.arc(CX + x, cy + y, r, 0, 2 * math.pi)
        c.set_source_rgba(*colr, 0.22)
        c.set_line_width(3)
        c.stroke()
    for lw, al in ((34, 0.10), (22, 0.2), (12, 1.0)):
        c.arc(CX, cy, R, 0, 2 * math.pi)
        c.set_source_rgba(*th["acc"], al)
        c.set_line_width(lw)
        c.stroke()
    colr = L.col(th, f["nb"] % 24, 24)
    fin = _done(S, t)
    pulse = math.exp(-6 * (t - S["done_at"])) if fin else 0
    ball(c, CX + f["p"][0], cy + f["p"][1], f["r"] * (1 + 0.04 * pulse), colr, glow=not fin)
    pct = int(round(100 * ((f["r"] - S["r0"]) / (R - 8 - S["r0"]))))
    E.text(c, f"{min(100, pct)}%", CX + f["p"][0], cy + f["p"][1] + 0.2 * f["r"], max(36, f["r"] * 0.55), (1, 1, 1),
           outline=0.1)
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    if fin:
        L.big_result(c, "IT'S FULL!", S["done_at"], t, th["acc"], 1580)
    else:
        E.text(c, f"BOUNCES: {f['nb']}", W / 2, 1580, 76, (1, 1, 1))
    timer(c, S, t)


# =============================================================== level 3: escape the spinning hexagons
def sim_hexa(seed=3, layers=11, a_min=120.0, a_max=450.0, br=14.0, g=1450.0, vmin=950.0, gapfrac=0.62):
    rng = np.random.default_rng(seed)
    ap = np.linspace(a_min, a_max, layers)
    omega = np.array([(0.55 + 0.06 * i) * (1 if i % 2 == 0 else -1) for i in range(layers)]) * rng.uniform(0.9, 1.1)
    th0 = rng.uniform(0, 2 * np.pi, layers)
    gap = rng.integers(0, 6, layers)
    p = np.array([rng.uniform(-20, 20), -10.0])
    v = np.array([rng.uniform(-1000, 1000), rng.uniform(-800, -400)])
    broken = [None] * layers
    frames, events = [], []
    dt = 1 / FPS / SUBDT
    t, last, done = 0.0, -1, None
    while True:
        for _ in range(SUBDT):
            t += dt
            v[1] += g * dt
            p += v * dt
            k = next((i for i in range(layers) if broken[i] is None), None)
            if k is None:
                continue
            a = ap[k]
            half = a * math.tan(math.pi / 6)
            th = th0[k] + omega[k] * t
            for j in range(6):
                an = th + j * math.pi / 3
                n = np.array([math.cos(an), math.sin(an)])
                pn = np.dot(p, n)
                if a - pn < br:
                    tang = -p[0] * math.sin(an) + p[1] * math.cos(an)
                    if j == gap[k] and abs(tang) < gapfrac * half - br * 0.6:
                        if pn > a + br:
                            broken[k] = t
                            events.append((t, "break", k))
                            if all(b is not None for b in broken):
                                done = t
                                events.append((t, "end", 0))
                        continue
                    if abs(tang) > half + br:
                        continue
                    vn = np.dot(v, n)
                    if vn > 0:
                        v = v - 2 * vn * n
                        sp = math.hypot(*v)
                        if sp < vmin:
                            v *= vmin / sp
                        if t - last > 0.045:
                            events.append((t, "note", 0)); last = t
                    p = p - n * (br - (a - pn))
        frames.append(dict(t=t, p=p.copy(), th=th0 + omega * t))
        if (done is not None and t > done + 2.5) or t > 70:
            break
    return dict(frames=frames, events=events, ap=ap, gap=gap, broken=broken, br=br, layers=layers, gapfrac=gapfrac,
                done_at=done, seed=seed)


def draw_hexa(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    n = S["layers"]
    c.save()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    active = next((j for j in range(n) if S["broken"][j] is None or S["broken"][j] > t), -1)
    for i in range(n):
        colr = L.col(th, i, n)
        a = S["ap"][i]
        b = S["broken"][i]
        if b is not None and b <= t:
            age = t - b
            if age < 1.3:
                for x, y, vx, vy, sz in E.shards(i, a * 1.05, f["th"][i], S["seed"]):
                    c.set_source_rgba(*colr, 1 - age / 1.3)
                    c.rectangle(CX + x + vx * age - sz / 2, CY + y + vy * age + 900 * age * age - sz / 2, sz, sz)
                    c.fill()
            continue
        R = a / math.cos(math.pi / 6)
        half = a * math.tan(math.pi / 6)
        segs = []
        for j in range(6):
            an = f["th"][i] + j * math.pi / 3
            nx, ny = math.cos(an), math.sin(an)
            tx, ty = -ny, nx
            p0 = (CX + nx * a - tx * half, CY + ny * a - ty * half)
            p1 = (CX + nx * a + tx * half, CY + ny * a + ty * half)
            if j == S["gap"][i]:
                gh = S["gapfrac"] * half
                segs.append((p0, (CX + nx * a - tx * gh, CY + ny * a - ty * gh)))
                segs.append(((CX + nx * a + tx * gh, CY + ny * a + ty * gh), p1))
            else:
                segs.append((p0, p1))
        for lw, al in ((26, 0.10), (17, 0.2), (10, 1.0)):
            c.set_source_rgba(*colr, al * (1.0 if i == active else 0.7))
            c.set_line_width(lw)
            for p0, p1 in segs:
                c.move_to(*p0); c.line_to(*p1)
            c.stroke()
    br = S["br"]
    for k in range(12, 0, -1):
        q = S["frames"][max(0, fi - k)]["p"]
        c.set_source_rgba(*th["acc"], 0.25 * (1 - k / 12))
        c.arc(CX + q[0], CY + q[1], br * (1 - 0.5 * k / 12), 0, 2 * math.pi)
        c.fill()
    ball(c, CX + f["p"][0], CY + f["p"][1], br, (1, 1, 1))
    c.restore()
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    left = sum(1 for b in S["broken"] if b is None or b > t)
    if _done(S, t):
        L.big_result(c, "ESCAPED!", S["done_at"], t, (0.35, 1.0, 0.5))
    else:
        E.text(c, f"HEXAGONS LEFT: {left}", W / 2, 1560, 72, (1, 1, 1))
    timer(c, S, t)


# =============================================================== level 4: red vs blue territory battle
RED_, BLUE_ = (1.0, 0.27, 0.33), (0.22, 0.56, 1.0)


def sim_paint(seed=4, N=28, size=900.0, dur=30.0, br=16.0):
    rng = np.random.default_rng(seed)
    cell = size / N
    grid = np.zeros((N, N), np.int8)
    grid[:, N // 2:] = 1   # [row, col]: left half red (0), right half blue (1)
    balls = []
    for owner, xs in ((0, (0.25,)), (1, (0.62, 0.75, 0.88))):   # 1 fast red ball vs 3 blue balls
        for k, fx in enumerate(xs):
            ang = rng.uniform(0, 2 * np.pi)
            sp = 1500.0 if owner == 0 else rng.uniform(700, 800)
            balls.append(dict(o=owner, p=np.array([fx * size, rng.uniform(0.2, 0.8) * size]),
                              v=np.array([math.cos(ang) * sp, math.sin(ang) * sp]), last=-1.0))
    frames, events = [], []
    dt = 1 / FPS / SUBDT
    t = 0.0
    while t < dur + 3:
        for _ in range(SUBDT):
            t += dt
            if t > dur:
                continue
            for b in balls:
                b["p"] += b["v"] * dt
                for ax in (0, 1):
                    if b["p"][ax] < br and b["v"][ax] < 0 or b["p"][ax] > size - br and b["v"][ax] > 0:
                        b["v"][ax] *= -1
                for ax, sg in ((0, 1), (0, -1), (1, 1), (1, -1)):
                    q = b["p"].copy()
                    q[ax] += sg * br
                    ci, cj = int(q[1] // cell), int(q[0] // cell)
                    if 0 <= ci < N and 0 <= cj < N and grid[ci, cj] != b["o"]:
                        grid[ci, cj] = b["o"]
                        if b["v"][ax] * sg > 0:
                            b["v"][ax] *= -1
                        a = rng.normal(0, 0.03)
                        vx, vy = b["v"]
                        b["v"] = np.array([vx * math.cos(a) - vy * math.sin(a), vx * math.sin(a) + vy * math.cos(a)])
                        if t - b["last"] > 0.09:
                            events.append((t, "note", -12 if b["o"] == 0 else 0)); b["last"] = t
                        break
        frames.append(dict(t=t, grid=grid.copy(), balls=[(b["o"], *b["p"]) for b in balls]))
    red = int((frames[-1]["grid"] == 0).sum())
    win = 0 if red * 2 > N * N else 1
    events.append((dur, "end", 0))
    return dict(frames=frames, events=events, N=N, size=size, br=br, dur=dur, done_at=dur, win=win)


def draw_paint(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    N, size = S["N"], S["size"]
    cell = size / N
    x0, y0 = CX - size / 2, 560
    g = f["grid"]
    for i in range(N):
        for j in range(N):
            colr = RED_ if g[i, j] == 0 else BLUE_
            k = 0.62 + 0.08 * ((i + j) % 2)
            c.set_source_rgb(*(x * k for x in colr))
            c.rectangle(x0 + j * cell, y0 + i * cell, cell + 0.5, cell + 0.5)
            c.fill()
    c.set_source_rgb(1, 1, 1)
    c.set_line_width(8)
    c.rectangle(x0, y0, size, size)
    c.stroke()
    for o, x, y in f["balls"]:
        ball(c, x0 + x, y0 + y, S["br"], tuple(min(1, v * 1.25 + 0.1) for v in (RED_ if o == 0 else BLUE_)))
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    red = (g == 0).sum() / (N * N)
    bw, by = 900, 1540
    c.set_source_rgb(*RED_); c.rectangle(CX - bw / 2, by, bw * red, 56); c.fill()
    c.set_source_rgb(*BLUE_); c.rectangle(CX - bw / 2 + bw * red, by, bw * (1 - red), 56); c.fill()
    c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.rectangle(CX - bw / 2, by, bw, 56); c.stroke()
    E.text(c, f"{red * 100:.1f}%", CX - bw / 2 + 110, by + 44, 50, (1, 1, 1), outline=0.12)
    E.text(c, f"{100 - red * 100:.1f}%", CX + bw / 2 - 110, by + 44, 50, (1, 1, 1), outline=0.12)
    if t >= S["dur"]:
        L.big_result(c, "RED WINS!" if S["win"] == 0 else "BLUE WINS!", S["dur"], t, RED_ if S["win"] == 0 else BLUE_, 1720)
    else:
        E.text(c, f"{max(0, S['dur'] - t):4.1f}s", W / 2, 1700, 64, (0.85, 0.85, 0.92), outline=0.1)


# =============================================================== level 5: break out of a brick wall
def sim_bricks(seed=5, layers=3, per=36, r_in=290.0, thick=44.0, gapr=5.0, hp0=(1, 2, 3), br=15.0, g=1350.0, vmin=1000.0):
    rng = np.random.default_rng(seed)
    rin = np.array([r_in + l * (thick + gapr) for l in range(layers)])
    omega = np.array([(0.22 + 0.08 * l) * (1 if l % 2 == 0 else -1) for l in range(layers)])
    hp = np.array([[hp0[l] + (1 if rng.random() < 0.25 else 0) for _ in range(per)] for l in range(layers)])
    hp_max = hp.copy()
    p = np.array([0.0, -60.0])
    v = np.array([rng.uniform(-900, 900), -500.0])
    frames, events = [], []
    dt = 1 / FPS / SUBDT
    t, last, done, hits = 0.0, -1, None, []
    step = 2 * math.pi / per
    while True:
        for _ in range(SUBDT):
            t += dt
            v[1] += g * dt
            p += v * dt
            if done is not None:
                continue
            d = math.hypot(*p)
            ang = math.atan2(p[1], p[0])
            for l in range(layers):
                if rin[l] + thick < d - br:
                    continue
                idx = int(((ang - omega[l] * t) % (2 * math.pi)) // step)
                if hp[l, idx] <= 0:
                    continue
                n = p / d
                inside = d < rin[l] + thick / 2
                if inside and d + br < rin[l]:
                    break
                hp[l, idx] -= 1
                hits.append((t, l, idx))
                if inside:
                    p = n * (rin[l] - br - 0.5)
                    if np.dot(v, n) > 0:
                        v = v - 2 * np.dot(v, n) * n
                else:
                    p = n * (rin[l] + thick + br + 0.5)
                    if np.dot(v, n) < 0:
                        v = v - 2 * np.dot(v, n) * n
                sp = math.hypot(*v)
                if sp < vmin:
                    v *= vmin / sp
                if hp[l, idx] == 0:
                    events.append((t, "break", l * per + idx))
                elif t - last > 0.04:
                    events.append((t, "note", 0)); last = t
                break
            if d > rin[-1] + thick + br + 30:
                done = t
                events.append((t, "end", 0))
        frames.append(dict(t=t, p=p.copy(), hp=hp.copy()))
        if (done is not None and t > done + 2.5) or t > 70:
            break
    return dict(frames=frames, events=events, rin=rin, thick=thick, omega=omega, hp_max=hp_max, per=per, layers=layers,
                br=br, done_at=done, hits=hits, seed=seed)


def draw_bricks(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    per, step = S["per"], 2 * math.pi / S["per"]
    hp = f["hp"]
    c.save()
    for l in range(S["layers"]):
        rin, rout = S["rin"][l], S["rin"][l] + S["thick"]
        rot = S["omega"][l] * t
        for k in range(per):
            a0 = rot + k * step + 0.02
            a1 = rot + (k + 1) * step - 0.02
            h = hp[l, k]
            if h <= 0:
                continue
            colr = L.col(th, l * 2 + (h - 1), S["layers"] * 2 + 1, s=0.55 + 0.12 * h, v=0.65 + 0.12 * h)
            c.new_path()
            c.arc(CX, CY, rout, a0, a1)
            c.arc_negative(CX, CY, rin, a1, a0)
            c.close_path()
            c.set_source_rgb(*colr)
            c.fill_preserve()
            c.set_source_rgba(0, 0, 0, 0.55)
            c.set_line_width(3)
            c.stroke()
            am = (a0 + a1) / 2
            rm = (rin + rout) / 2
            E.text(c, str(h), CX + rm * math.cos(am), CY + rm * math.sin(am) + 11, 30, (1, 1, 1), outline=0.12)
    # shards of bricks broken in the last second
    for (tb, kind, val) in S["events"]:
        if kind == "break" and 0 <= t - tb < 1.1:
            l, k = divmod(int(val), per)
            age = t - tb
            am = S["omega"][l] * tb + (k + 0.5) * step
            rm = S["rin"][l] + S["thick"] / 2
            rng = np.random.default_rng(int(val) + 7)
            colr = L.col(th, l * 2, S["layers"] * 2 + 1)
            for _ in range(14):
                vx, vy = rng.uniform(-400, 400), rng.uniform(-500, 100)
                c.set_source_rgba(*colr, 1 - age / 1.1)
                c.rectangle(CX + rm * math.cos(am) + vx * age, CY + rm * math.sin(am) + vy * age + 900 * age * age, 9, 9)
                c.fill()
    br = S["br"]
    for k in range(12, 0, -1):
        q = S["frames"][max(0, fi - k)]["p"]
        c.set_source_rgba(*th["acc"], 0.25 * (1 - k / 12))
        c.arc(CX + q[0], CY + q[1], br * (1 - 0.5 * k / 12), 0, 2 * math.pi)
        c.fill()
    ball(c, CX + f["p"][0], CY + f["p"][1], br, (1, 1, 1))
    c.restore()
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    if _done(S, t):
        L.big_result(c, "ESCAPED!", S["done_at"], t, (0.35, 1.0, 0.5))
    else:
        E.text(c, f"BRICKS LEFT: {int((hp > 0).sum())}", W / 2, 1560, 72, (1, 1, 1))
    timer(c, S, t)


# =============================================================== level 6: plinko / Galton board
PENTA = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93]


def sim_plinko(seed=6, nballs=360, rows=13, dx=60.0, dy=54.0, y0=540.0, peg=7.0, br=7.0, every=0.05, g=1700.0):
    rng = np.random.default_rng(seed)
    floor = 1600.0
    bins_top = y0 + (rows - 1) * dy + 30
    last_x = CX - (rows + 1) * dx / 2 + np.arange(rows + 2) * dx   # bottom-row peg x = bin edges
    nb = rows + 1
    counts = np.zeros(nb, int)
    P = np.zeros((0, 2)); V = np.zeros((0, 2)); B = np.zeros(0, int)   # B: -1 falling, else bin index
    spawned = 0
    frames, events = [], []
    dt = 1 / FPS / 6
    t, lastnote, lasttick, done = 0.0, -1, -1, None
    while True:
        for _ in range(6):
            t += dt
            while spawned < nballs and t >= spawned * every:
                P = np.vstack([P, [CX + rng.normal(0, 2.5), 470.0]])
                V = np.vstack([V, [rng.uniform(-15, 15), 0.0]])
                B = np.append(B, -1)
                spawned += 1
            act = B == -1
            if not act.any():
                continue
            V[act, 1] += g * dt
            P[act] += V[act] * dt
            # pegs: only the nearest peg in the nearest row
            row = np.rint((P[:, 1] - y0) / dy).astype(int)
            ok = act & (row >= 0) & (row < rows)
            if ok.any():
                r_ = row[ok]
                left = CX - (r_ + 2) * dx / 2
                k = np.clip(np.rint((P[ok, 0] - left) / dx), 0, r_ + 2)
                px, py = left + k * dx, y0 + r_ * dy
                d = np.hypot(P[ok, 0] - px, P[ok, 1] - py)
                hit = d < peg + br
                if hit.any():
                    idx = np.where(ok)[0][hit]
                    nx, ny = (P[idx, 0] - px[hit]) / d[hit], (P[idx, 1] - py[hit]) / d[hit]
                    vn = V[idx, 0] * nx + V[idx, 1] * ny
                    m = vn < 0
                    V[idx[m], 0] -= 1.45 * vn[m] * nx[m]
                    V[idx[m], 1] -= 1.45 * vn[m] * ny[m]
                    V[idx, 0] += rng.normal(0, 25, len(idx))
                    P[idx, 0] = px[hit] + nx * (peg + br + 0.3)
                    P[idx, 1] = py[hit] + ny * (peg + br + 0.3)
                    if t - lasttick > 0.025:
                        events.append((t, "tick", 98)); lasttick = t
            # side walls of the board
            P[act, 0] = np.clip(P[act, 0], last_x[0] + br, last_x[-1] - br)
            # bins: keep each ball inside its column, then settle on the stack
            low = act & (P[:, 1] > bins_top)
            if low.any():
                bi = np.clip(((P[low, 0] - last_x[0]) // dx).astype(int), 0, nb - 1)
                ids = np.where(low)[0]
                lo = last_x[0] + bi * dx + br + 2
                P[ids, 0] = np.clip(P[ids, 0], lo, lo + dx - 2 * br - 4)
                V[ids, 0] *= 0.9
                for j, b in zip(ids, bi):
                    top = floor - (counts[b] // 4) * 13 - br
                    if P[j, 1] >= top:
                        B[j] = b
                        P[j] = [last_x[0] + b * dx + 8 + br + (counts[b] % 4) * 13, top]
                        counts[b] += 1
                        if t - lastnote > 0.03:
                            events.append((t, "note", PENTA[b])); lastnote = t
            if spawned == nballs and not (B == -1).any() and done is None:
                done = t
                events.append((t, "end", 0))
        frames.append(dict(t=t, P=P[B == -1].copy(), counts=counts.copy()))
        if (done is not None and t > done + 2.5) or t > 60:
            break
    win = int(np.argmax(counts))
    return dict(frames=frames, events=events, rows=rows, dx=dx, dy=dy, y0=y0, peg=peg, br=br, floor=floor,
                bins_top=bins_top, edges=last_x, done_at=done, win=win, nballs=nballs)


def draw_plinko(c, S, fi):
    f = S["frames"][fi]
    t = f["t"]
    th = L.THEMES[S["theme"]]
    L.background(c, th, t)
    rows, dx, dy, y0 = S["rows"], S["dx"], S["dy"], S["y0"]
    for r in range(rows):
        left = CX - (r + 2) * dx / 2
        for k in range(r + 3):
            c.arc(left + k * dx, y0 + r * dy, S["peg"], 0, 2 * math.pi)
            c.set_source_rgb(*th["acc"])
            c.fill()
    e = S["edges"]
    nb = len(e) - 1
    c.set_source_rgba(1, 1, 1, 0.85)
    c.set_line_width(4)
    for x in e:
        c.move_to(x, S["bins_top"]); c.line_to(x, S["floor"])
    c.move_to(e[0], S["floor"]); c.line_to(e[-1], S["floor"])
    c.stroke()
    br = S["br"]
    for b in range(nb):
        colr = L.col(th, b, nb, s=0.7)
        for j in range(f["counts"][b]):
            x = e[0] + b * dx + 8 + br + (j % 4) * 13
            y = S["floor"] - (j // 4) * 13 - br
            c.arc(x, y, br, 0, 2 * math.pi)
            c.set_source_rgb(*colr)
            c.fill()
    for x, y in f["P"]:
        c.arc(x, y, br, 0, 2 * math.pi)
        c.set_source_rgb(1, 1, 1)
        c.fill()
    fin = _done(S, t)
    for b in range(nb):
        x = e[0] + (b + 0.5) * dx
        hl = fin and b == S["win"]
        E.text(c, str(b + 1), x, S["floor"] + 50, 34, (1, 0.85, 0.3) if hl else (0.85, 0.85, 0.92), outline=0.1)
    if S.get("nohud"):
        return
    L.hud_top(c, S, t)
    if fin:
        L.big_result(c, f"BIN {S['win'] + 1} WINS!", S["done_at"], t, th["acc"], 1760)
    else:
        dropped = min(S["nballs"], int(t / 0.05) + 1)
        E.text(c, f"BALLS: {dropped}/{S['nballs']}", W / 2, 1760, 64, (1, 1, 1))


# =============================================================== the series
LEVELS = {
    1: dict(fn=(sim_rings, draw_rings), kw=dict(seed=2, rings=8, gap_deg=55, gap_grow=30, r_min=150, r_max=450, ball_r=18),
            theme="sunset", melody="ode_to_joy", diff="EASY", title=("CAN IT ESCAPE", "8 RINGS?"),
            cover=("CAN IT ESCAPE", "8 RINGS?", "EASY MODE")),
    2: dict(fn=(sim_grow, draw_grow), kw=dict(seed=2, grow=2.9), theme="lava", melody="fur_elise", diff="EASY",
            title=("EVERY BOUNCE", "IT GROWS"), cover=("EVERY BOUNCE", "IT GROWS", "WAIT FOR 100%")),
    3: dict(fn=(sim_hexa, draw_hexa), kw=dict(seed=1, gapfrac=0.7), theme="mint", melody="morning_mood", diff="MEDIUM",
            title=("ESCAPE THE", "HEXAGONS"), cover=("ESCAPE THE", "HEXAGONS", "NEW SHAPE")),
    4: dict(fn=(sim_paint, draw_paint), kw=dict(seed=3), theme="duel", melody="can_can", diff="MEDIUM",
            title=("1 RED VS 3 BLUE", "WHO WINS?"), cover=("1 RED VS 3 BLUE", "WHO WINS?", "PICK A SIDE")),
    5: dict(fn=(sim_bricks, draw_bricks), kw=dict(seed=1, hp0=(1, 1, 2), per=30), theme="candy", melody="canon", diff="HARD",
            title=("BREAK OUT OF", "90 BRICKS"), cover=("BREAK OUT OF", "90 BRICKS", "HARD MODE")),
    6: dict(fn=(sim_plinko, draw_plinko), kw=dict(seed=6), theme="ocean", melody="turkish_march", diff="HARD",
            title=("360 BALLS", "WHICH BIN WINS?"), cover=("360 BALLS", "WHICH BIN?", "GUESS NOW")),
    7: dict(fn=(sim_rings, draw_rings), kw=dict(seed=6, rings=30, gap_deg=36, gap_grow=24, r_min=95, r_max=470, ball_r=10),
            theme="gold", melody="mountain_king", diff="INSANE", title=("30 RINGS", "IMPOSSIBLE?"),
            cover=("30 RINGS", "IMPOSSIBLE?", "INSANE MODE")),
}


def make(n, render=True):
    cfg = LEVELS[n]
    sim, draw = cfg["fn"]
    S = sim(**cfg["kw"])
    S.update(theme=cfg["theme"], melody=cfg["melody"], diff=cfg["diff"], title=cfg["title"], level=n)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", f"level_{n:02d}.mp4")
    print(f"level {n}: {len(S['frames']) / FPS:.1f}s, done at {S['done_at']}", flush=True)
    if render:
        L.render(draw, S, out)
        fi = min(len(S["frames"]) - 1, int(2.0 * FPS))
        L.cover(draw, S, out.replace(".mp4", "_cover.png"), fi, *cfg["cover"])
    return S


if __name__ == "__main__":
    render = "--dry" not in sys.argv
    for a in sys.argv[1:]:
        if a != "--dry":
            make(int(a), render)
