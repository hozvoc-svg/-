"""Clean stylized 3D shots for "Why Airplane Windows Are Round" (Blender Workbench, 1080x1920, 30 fps).

Usage:
  EGL_PLATFORM=surfaceless /opt/bpyenv/bin/python scenes.py <shot> [preview=<local frame>] [frames=a-b]
Shots and their length come from SHOTS below (timed to audio/voice.mp3).
Frames go to frames/<shot>/####.png; previews to preview/<shot>_<frame>.png.
"""
import bpy, sys, os, math, random
from math import radians, sin, cos, pi

FPS = 30
# shot id: (start s, end s) on the voiceover timeline
SHOTS = {
    'A': (0.00, 2.55),   # rounded cabin window, push-in
    'B': (2.55, 7.00),   # window turns square, cracks
    'C': (7.00, 15.60),  # the Comet flying
    'D': (15.60, 19.30), # Comet breaks apart
    'E': (19.30, 28.60), # water tank pressure test
    'F': (28.60, 32.00), # crack at a square corner
    'G': (32.00, 39.40), # fuselage inflates like a balloon
    'H': (39.40, 46.10), # stress: round vs square hole
    'I': (46.10, 52.20), # fatigue cracks grow
    'J': (52.20, 57.20), # corners get rounded, pull back to seat
    'K': (57.20, 61.00), # push-in to the tiny hole
}

def nframes(shot):
    a, b = SHOTS[shot]
    return round((b - a) * FPS)

# ---------- palette ----------
SKY = (0.36, 0.62, 0.92)
SKY_DARK = (0.10, 0.14, 0.24)
CREAM = (0.93, 0.91, 0.86)
WHITE = (0.97, 0.97, 0.97)
SILVER = (0.72, 0.74, 0.78)
DARK = (0.08, 0.09, 0.11)
BLUE = (0.10, 0.25, 0.62)
RED = (0.95, 0.12, 0.08)
ORANGE = (1.0, 0.55, 0.10)
WATER = (0.20, 0.52, 0.78)
_mats = {}

def mat(rgb, metal=0.0, rough=0.5):
    key = (tuple(round(c, 3) for c in rgb), metal, rough)
    if key in _mats: return _mats[key]
    m = bpy.data.materials.new('m%d' % len(_mats))
    m.diffuse_color = (*rgb, 1.0); m.metallic = metal; m.roughness = rough
    _mats[key] = m
    return m

def setmat(ob, rgb, **kw):
    ob.data.materials.clear(); ob.data.materials.append(mat(rgb, **kw))
    return ob

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.render.fps = FPS
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Standard'
    d = sc.display
    d.render_aa = '8'
    s = d.shading
    s.light = 'STUDIO'
    s.color_type = 'MATERIAL'
    s.show_shadows = True; s.shadow_intensity = 0.45
    s.show_cavity = True; s.cavity_type = 'BOTH'
    s.cavity_ridge_factor = 0.6; s.cavity_valley_factor = 1.0
    s.curvature_ridge_factor = 0.5; s.curvature_valley_factor = 0.6
    s.show_specular_highlight = True
    d.light_direction = (0.45, -0.55, 0.70)
    d.shadow_shift = 0.1; d.shadow_focus = 0.6
    w = bpy.data.worlds.new('w'); sc.world = w; w.color = SKY
    return sc

# ---------- primitives ----------
def cube(loc, size, rgb, rot=(0, 0, 0), **kw):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=[radians(a) for a in rot])
    ob = bpy.context.object; ob.scale = [s / 2 for s in size]
    return setmat(ob, rgb, **kw)

def sphere(loc, r, rgb, scale=(1, 1, 1), seg=32, **kw):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, segments=seg, ring_count=seg // 2)
    ob = bpy.context.object; ob.scale = scale
    bpy.ops.object.shade_smooth()
    return setmat(ob, rgb, **kw)

def cyl(loc, r, depth, rgb, rot=(0, 0, 0), verts=48, **kw):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=depth, vertices=verts,
                                        rotation=[radians(a) for a in rot])
    ob = bpy.context.object; bpy.ops.object.shade_smooth()
    return setmat(ob, rgb, **kw)

def cone(loc, r1, r2, depth, rgb, rot=(0, 0, 0), **kw):
    bpy.ops.mesh.primitive_cone_add(location=loc, radius1=r1, radius2=r2, depth=depth, vertices=32,
                                    rotation=[radians(a) for a in rot])
    ob = bpy.context.object; bpy.ops.object.shade_smooth()
    return setmat(ob, rgb, **kw)

def torus(loc, R, r, rgb, rot=(0, 0, 0), **kw):
    bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=R, minor_radius=r,
                                     major_segments=96, minor_segments=16,
                                     rotation=[radians(a) for a in rot])
    ob = bpy.context.object; bpy.ops.object.shade_smooth()
    return setmat(ob, rgb, **kw)

def empty(loc=(0, 0, 0)):
    bpy.ops.object.empty_add(location=loc); return bpy.context.object

def parent(child, par):
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()

def rrect_loop(w, h, r, n):
    pts = []
    for cx, cy, a0 in ((w/2 - r, h/2 - r, 0), (-w/2 + r, h/2 - r, 90),
                       (-w/2 + r, -h/2 + r, 180), (w/2 - r, -h/2 + r, 270)):
        for i in range(n + 1):
            a = radians(a0 + 90 * i / n)
            pts.append((cx + r * cos(a), cy + r * sin(a)))
    return pts

def rrect(name, w, h, depth, r_round, rgb, loc=(0, 0, 0), n=10, r_square=0.004):
    """Rounded-rectangle prism in the XZ plane (faces -Y). Shape key 'round' 0=square, 1=rounded."""
    def verts(r):
        lp = rrect_loop(w, h, r, n)
        return [(x, -depth / 2, z) for x, z in lp] + [(x, depth / 2, z) for x, z in lp]
    m = len(rrect_loop(w, h, r_square, n))
    faces = [list(range(m)), list(range(m, 2 * m))[::-1]]
    faces += [[i, m + i, m + (i + 1) % m, (i + 1) % m] for i in range(m)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts(r_square), [], faces); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    ob.location = loc
    ob.shape_key_add(name='Basis')
    k = ob.shape_key_add(name='round')
    for i, v in enumerate(verts(r_round)): k.data[i].co = v
    return setmat(ob, rgb)

def cut(target, cutter, hide=True):
    mod = target.modifiers.new('cut', 'BOOLEAN'); mod.operation = 'DIFFERENCE'
    mod.solver = 'MANIFOLD'; mod.object = cutter
    if hide: cutter.hide_render = True; cutter.display_type = 'WIRE'
    return mod

def crack(points, rgb=DARK, width=0.012, start=1, end=10):
    """Polyline crack that grows from start to end frame."""
    cu = bpy.data.curves.new('crack', 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = width; cu.bevel_resolution = 2
    sp = cu.splines.new('POLY'); sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points): p.co = (*co, 1)
    ob = bpy.data.objects.new('crack', cu); bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat(rgb))
    cu.bevel_factor_end = 0.0; cu.keyframe_insert('bevel_factor_end', frame=start)
    cu.bevel_factor_end = 1.0; cu.keyframe_insert('bevel_factor_end', frame=end)
    return ob

def zigzag(p0, direction, length, segs=7, jitter=0.05, seed=1):
    rnd = random.Random(seed)
    dx, dz = direction; n = math.hypot(dx, dz); dx, dz = dx / n, dz / n
    px, pz = -dz, dx
    pts = []
    for i in range(segs + 1):
        t = length * i / segs; j = 0 if i == 0 else rnd.uniform(-jitter, jitter)
        pts.append((p0[0] + dx * t + px * j, p0[1], p0[2] + dz * t + pz * j))
    return pts

def key(ob, path, frame, value, index=-1):
    if index >= 0:
        getattr(ob, path)[index] = value
    else:
        setattr(ob, path, value)
    ob.keyframe_insert(path, frame=frame, index=index)

def ease_all():
    for a in bpy.data.actions:
        for fc in _fcurves(a):
            for k in fc.keyframe_points: k.interpolation = 'BEZIER'; k.easing = 'AUTO'

def _fcurves(action):
    try:
        return list(action.fcurves)
    except AttributeError:  # Blender 5 layered actions
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags: out += list(bag.fcurves)
        return out

def camera(loc, look, lens=50):
    bpy.ops.object.camera_add(location=loc); cam = bpy.context.object
    cam.data.lens = lens; cam.data.sensor_fit = 'VERTICAL'
    tgt = empty(look); c = cam.constraints.new('TRACK_TO'); c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam
    return cam, tgt

def shake(cam, f0, f1, amp=0.03, seed=3):
    rnd = random.Random(seed); base = tuple(cam.location)
    key(cam, 'location', f0 - 1, base[0], 0); key(cam, 'location', f0 - 1, base[2], 2)
    for f in range(f0, f1, 2):
        k = amp * (1 - (f - f0) / max(1, f1 - f0))
        key(cam, 'location', f, base[0] + rnd.uniform(-k, k), 0)
        key(cam, 'location', f, base[2] + rnd.uniform(-k, k), 2)
    key(cam, 'location', f1, base[0], 0); key(cam, 'location', f1, base[2], 2)

def clouds(n, area, z, seed=7, scale=1.0):
    rnd = random.Random(seed); grp = empty()
    for _ in range(n):
        cx = rnd.uniform(*area[0]); cy = rnd.uniform(*area[1]); cz = z + rnd.uniform(-0.3, 0.3)
        for _ in range(rnd.randint(3, 6)):
            r = rnd.uniform(0.35, 0.8) * scale
            s = sphere((cx + rnd.uniform(-0.8, 0.8) * scale, cy + rnd.uniform(-0.3, 0.3), cz + rnd.uniform(-0.15, 0.2) * scale),
                       r, WHITE, scale=(1.3, 1.0, 0.75), seg=24, rough=0.9)
            parent(s, grp)
    return grp

# ---------- cabin window (A, B, J, K) ----------
def cabin(sc, start_round=1.0):
    sc.world.color = SKY
    wall = cube((0, 0.25, 0), (6, 0.5, 9), CREAM, rough=0.7)
    hole = rrect('hole', 1.30, 1.85, 1.2, 0.55, CREAM, loc=(0, 0.25, 0.2), n=12)
    cut(wall, hole)
    # inner bezel (slightly darker) visible inside the hole
    bez = cube((0, 0.55, 0.2), (1.9, 0.08, 2.5), (0.82, 0.80, 0.76))
    bhole = rrect('bhole', 1.10, 1.62, 0.6, 0.48, CREAM, loc=(0, 0.55, 0.2), n=12)
    cut(bez, bhole)
    # sky + clouds behind, drifting
    cl = clouds(14, ((-6, 6), (5.5, 8.0)), -1.0, scale=1.2)
    hole.data.shape_keys.key_blocks['round'].value = start_round
    bhole.data.shape_keys.key_blocks['round'].value = start_round
    # pane rim with the breather hole (only visible as a thin ring + dot)
    return dict(wall=wall, hole=hole, bhole=bhole, clouds=cl, bez=bez)

def set_round(c, frame, v):
    for o in (c['hole'], c['bhole']):
        kb = o.data.shape_keys.key_blocks['round']; kb.value = v
        kb.keyframe_insert('value', frame=frame)

def drift(ob, f0, f1, dx, dz=0.0):
    key(ob, 'location', f0, ob.location[0], 0); key(ob, 'location', f0, ob.location[2], 2)
    key(ob, 'location', f1, ob.location[0] + dx, 0); key(ob, 'location', f1, ob.location[2] + dz, 2)
    for fc in _fcurves(ob.animation_data.action):
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'

# ---------- the Comet ----------
def comet(windows='square', wings=True):
    root = empty(); front = empty(); rear = empty()
    parent(front, root); parent(rear, root)
    L = 6.0; R = 0.38
    # front half (x from 0 to +L/2), rear half (x from -L/2 to 0)
    f = cyl((L / 4, 0, 0), R, L / 2, WHITE, rot=(0, 90, 0), metal=0.1, rough=0.35); parent(f, front)
    r = cyl((-L / 4, 0, 0), R, L / 2, WHITE, rot=(0, 90, 0), metal=0.1, rough=0.35); parent(r, rear)
    nose = sphere((L / 2, 0, 0), R, WHITE, scale=(2.2, 1, 1), rough=0.35); parent(nose, front)
    cock = sphere((L / 2 + 0.45, 0, 0.12), 0.22, DARK, scale=(1.4, 1.2, 0.5), rough=0.2); parent(cock, front)
    tail = cone((-L / 2 - 0.55, 0, 0.05), R, 0.08, 1.1, WHITE, rot=(0, -90, 0), rough=0.35); parent(tail, rear)
    fin = cube((-L / 2 - 0.55, 0, 0.7), (0.9, 0.06, 1.0), WHITE, rot=(0, -28, 0)); parent(fin, rear)
    hst = cube((-L / 2 - 0.6, 0, 0.18), (0.55, 2.0, 0.05), WHITE, rot=(0, 0, 0)); parent(hst, rear)
    # silver belly + blue cheatline
    for half, sgn in ((front, 1), (rear, -1)):
        belly = cyl((sgn * L / 4, 0, -0.17), R * 1.012, L / 2, SILVER, rot=(0, 90, 0), metal=0.6, rough=0.3)
        belly.scale = (0.55, 1, 1)
        parent(belly, half)
        for side in (-1, 1):
            band = cube((sgn * L / 4, side * (R + 0.002), 0.02), (L / 2, 0.01, 0.07), BLUE); parent(band, half)
    # wings (swept) with engine intakes at the root
    for side in ((-1, 1) if wings else ()):
        wng = cube((0.15, side * 1.6, -0.12), (1.1, 2.7, 0.07), SILVER, rot=(0, 0, side * -22), metal=0.5, rough=0.3)
        parent(wng, front)
        for k in (0.3, 0.6):
            ei = cyl((0.75, side * (R + k * 0.7), -0.1), 0.09, 0.2, DARK, rot=(0, 90, 0)); parent(ei, front)
    # windows along both sides
    for side in (-1, 1):
        for i in range(14):
            x = -L / 2 + 0.55 + i * 0.37
            wv = cube((x, side * (R + 0.004), 0.13), (0.13, 0.012, 0.13) if windows == 'square' else (0.13, 0.012, 0.16), DARK)
            parent(wv, front if x > 0 else rear)
    return root, front, rear

# ---------- shots ----------
def shot_A(sc, N):
    c = cabin(sc, 1.0)
    cam, t = camera((0, -6.4, 0.2), (0, 0.5, 0.2), lens=50)
    key(cam, 'location', 1, -6.4, 1); key(cam, 'location', N, -5.2, 1)
    drift(c['clouds'], 1, N, -0.9)

def shot_B(sc, N):
    c = cabin(sc, 1.0)
    cam, t = camera((0, -5.2, 0.2), (0, 0.5, 0.2), lens=50)
    key(cam, 'location', 1, -5.2, 1); key(cam, 'location', 60, -5.2, 1); key(cam, 'location', N, -6.6, 1)
    drift(c['clouds'], 1, N, -1.4)
    set_round(c, 2, 1.0); set_round(c, 30, 0.0)        # "And that's not a design choice" -> square
    f_cr = round((4.81 - 2.55) * FPS)                    # "Square windows once tore planes apart"
    w2, h2 = 0.65, 0.925
    for i, (sx, sz) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        p0 = (sx * w2, -0.02, 0.2 + sz * h2)
        crack(zigzag(p0, (sx, sz), 0.75, seed=i), RED, 0.02, f_cr + i * 3, f_cr + 18 + i * 3)
    shake(cam, f_cr, f_cr + 25, 0.05)

def shot_C(sc, N):
    sc.world.color = SKY
    sky = cube((0, 40, 0), (200, 0.2, 200), SKY, rough=1.0)
    root, front, rear = comet()
    root.rotation_euler = (radians(4), 0, radians(-8))
    sea = clouds(34, ((-16, 16), (-6, 14)), -2.8, seed=4, scale=1.6)
    drift(sea, 1, N, -12.0)
    cam, t = camera((7.5, -6.5, 1.6), (0.6, 0, -0.2), lens=30)
    key(cam, 'location', 1, (7.5, -6.5, 1.6)); key(cam, 'location', N, (2.0, -9.0, 0.9))
    # gentle bob
    for f in range(1, N + 1, 30): key(root, 'location', f, 0.08 * sin(f / 20), 2)

def shot_D(sc, N):
    sc.world.color = (0.55, 0.30, 0.22)
    sky = cube((0, 40, 0), (200, 0.2, 200), (0.55, 0.32, 0.25), rough=1.0)
    root, front, rear = comet()
    sea = clouds(30, ((-14, 14), (-6, 12)), -2.6, seed=4, scale=1.6)
    for o in sea.children: setmat(o, (0.75, 0.70, 0.68), rough=0.9)
    drift(sea, 1, N, -4.0, 2.0)
    cam, t = camera((-1.0, -9.5, 0.8), (0, 0, -0.6), lens=26)
    b = 12   # break frame
    for ob in (front, rear):
        key(ob, 'location', b, tuple(ob.location)); key(ob, 'rotation_euler', b, (0, 0, 0))
    key(front, 'location', N, (1.4, -0.3, -2.4)); key(front, 'rotation_euler', N, (radians(10), radians(38), radians(8)))
    key(rear, 'location', N, (-1.6, 0.6, -1.4)); key(rear, 'rotation_euler', N, (radians(-25), radians(-70), radians(-15)))
    rnd = random.Random(2)
    for i in range(26):
        d = cube((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(-0.2, 0.2)),
                 [rnd.uniform(0.05, 0.16)] * 3, rnd.choice([WHITE, SILVER, DARK]))
        d.hide_render = True; d.keyframe_insert('hide_render', frame=b - 1)
        d.hide_render = False; d.keyframe_insert('hide_render', frame=b)
        key(d, 'location', b, tuple(d.location))
        key(d, 'location', N, (rnd.uniform(-3, 3), rnd.uniform(-1.5, 1.5), rnd.uniform(-3.0, 1.2)))
        key(d, 'rotation_euler', N, [rnd.uniform(-6, 6) for _ in range(3)])
    shake(cam, b, b + 20, 0.12)

def shot_E(sc, N):
    sc.world.color = (0.13, 0.15, 0.19)
    floor = cube((0, 0, -2.3), (14, 14, 0.2), (0.28, 0.30, 0.33))
    back = cube((0, 2.4, 0), (8.0, 0.1, 4.4), WATER, rough=0.2)
    lw = cube((-3.9, 0, 0), (0.1, 4.8, 4.4), (0.16, 0.42, 0.66), rough=0.2)
    rw = cube((3.9, 0, 0), (0.1, 4.8, 4.4), (0.16, 0.42, 0.66), rough=0.2)
    bottom = cube((0, 0, -2.15), (7.8, 4.8, 0.1), (0.14, 0.38, 0.60))
    surf = cube((0, 0, 1.9), (7.8, 4.8, 0.03), (0.42, 0.72, 0.92), rough=0.1)
    for x in (-3.95, 3.95):
        for y in (-2.4, 2.4):
            cube((x, y, 0), (0.12, 0.12, 4.5), (0.35, 0.37, 0.40), metal=0.7)
    for z in (-2.2, 2.2):
        for y in (-2.4, 2.4): cube((0, y, z), (8.0, 0.12, 0.12), (0.35, 0.37, 0.40), metal=0.7)
    root, front, rear = comet(wings=False)
    root.location = (0, 0, -0.2); root.scale = (0.95, 0.95, 0.95)
    # pressure cycles: inflate/deflate, speeding up
    f, period = 15, 18
    while f < N - 6:
        key(root, 'scale', f, (0.95, 0.95, 0.95))
        key(root, 'scale', f + period // 2, (0.95, 1.06, 1.06))
        f += period; period = max(8, period - 1)
    key(root, 'scale', f, (0.95, 0.95, 0.95))
    # pipe to the pump
    pipe = cyl((0, 1.2, 1.5), 0.06, 2.6, (0.35, 0.37, 0.40), rot=(90, 0, 0), metal=0.7)
    pipe2 = cyl((0, 2.5, 2.3), 0.06, 1.8, (0.35, 0.37, 0.40), metal=0.7)
    rnd = random.Random(5)
    for i in range(40):
        b = sphere((rnd.uniform(-3.5, 3.5), rnd.uniform(-1.5, 2.0), -2.0), rnd.uniform(0.03, 0.07), (0.8, 0.92, 1.0), seg=12)
        f0 = rnd.randint(1, N); key(b, 'location', f0, tuple(b.location))
        key(b, 'location', min(N + 60, f0 + 90), (b.location[0], b.location[1], 2.0))
    cam, t = camera((-6.5, -7.5, 2.4), (0, 0, -0.3), lens=24)
    key(cam, 'location', 1, (-6.5, -7.5, 2.4)); key(cam, 'location', N, (-3.0, -8.0, 1.2))

def panel_with_hole(loc, shape, rgb=SILVER, size=(3.0, 0.08, 3.0), hw=1.0, hh=1.0):
    p = cube(loc, size, rgb, metal=0.6, rough=0.35)
    if shape == 'round':
        h = cyl(loc, hw / 2, 0.6, rgb, rot=(90, 0, 0), verts=96)
    else:
        h = rrect('sq', hw, hh, 0.6, 0.2, rgb, loc=loc)
    cut(p, h)
    # rivets
    for i in range(8):
        for sx, sz in ((1, 0), (0, 1)):
            pass
    return p, h

def rivets(loc, size, n=9):
    for i in range(n):
        x = loc[0] - size[0] / 2 + 0.15 + i * (size[0] - 0.3) / (n - 1)
        for z in (loc[2] - size[2] / 2 + 0.15, loc[2] + size[2] / 2 - 0.15):
            sphere((x, loc[1] - 0.05, z), 0.035, (0.55, 0.57, 0.6), seg=12, metal=0.7)

def shot_F(sc, N):
    sc.world.color = SKY
    sky = cube((0, 12, 0), (60, 0.2, 60), SKY, rough=1.0)
    skin = cube((0, 0, 0), (6, 0.08, 6), WHITE, metal=0.2, rough=0.35)
    h = rrect('sq', 1.2, 1.2, 0.6, 0.2, WHITE, loc=(0, 0, 0))
    cut(skin, h)
    rivets((0, 0, 0), (6, 0.08, 6), 14)
    cam, t = camera((0, -8.0, 0), (0, 0, 0), lens=50)
    k0 = round(0.2 * FPS)
    key(cam, 'location', 1, (0, -8.0, 0)); key(t, 'location', 1, (0, 0, 0))
    key(cam, 'location', 50, (0.55, -2.6, 0.55)); key(t, 'location', 50, (0.6, 0, 0.6))
    key(cam, 'location', N, (0.6, -2.2, 0.6)); key(t, 'location', N, (0.62, 0, 0.62))
    for i, d in enumerate(((1, 1), (1, 0.4), (0.4, 1))):
        crack(zigzag((0.6, -0.05, 0.6), d, 2.6, segs=10, jitter=0.07, seed=10 + i), DARK, 0.016, k0 + i * 4, k0 + 14 + i * 4)
    shake(cam, k0 + 50, k0 + 70, 0.04)

def shot_G(sc, N):
    sc.world.color = (0.12, 0.14, 0.18)
    ring = torus((0, 0, 0), 1.6, 0.09, WHITE, rot=(90, 0, 0), rough=0.3)
    inner = cyl((0, 0.05, 0), 1.6, 0.02, (0.85, 0.90, 0.98), rot=(90, 0, 0), verts=96)
    floor = cube((0, 0.06, -0.95), (2.9, 0.06, 0.06), (0.55, 0.57, 0.6))  # cabin floor beam
    grp = empty(); parent(ring, grp); parent(inner, grp); parent(floor, grp)
    arrows = []
    for i in range(12):
        a = 2 * pi * i / 12
        ar = empty((1.95 * cos(a), -0.2, 1.95 * sin(a)))
        shaft = cyl(tuple(ar.location), 0.05, 0.45, ORANGE, rot=(0, 90 - math.degrees(a), 0))
        tip = cone((2.3 * cos(a), -0.2, 2.3 * sin(a)), 0.13, 0, 0.25, ORANGE, rot=(0, 90 - math.degrees(a), 0))
        parent(shaft, ar); parent(tip, ar); arrows.append(ar)
    # 33.08 pressurize -> stretch until 37.1; 37.5 relax
    p_up0, p_up1 = round((33.1 - 32.0) * FPS), round((36.5 - 32.0) * FPS)
    p_dn0, p_dn1 = round((37.5 - 32.0) * FPS), round((39.0 - 32.0) * FPS)
    for f, s in ((1, 1.0), (p_up0, 1.0), (p_up1, 1.12), (p_dn0, 1.12), (p_dn1, 1.0)):
        key(grp, 'scale', f, (s, 1, s))
    for ar in arrows:
        for f, s in ((1, 0.0), (p_up0, 0.0), (p_up0 + 12, 1.0), (p_dn0, 1.0), (p_dn0 + 10, 0.0)):
            key(ar, 'scale', f, (s, s, s))
        base = tuple(ar.location)
        key(ar, 'location', p_up0, base)
        key(ar, 'location', p_up1, (base[0] * 1.12, base[1], base[2] * 1.12))
        key(ar, 'location', p_dn0, (base[0] * 1.12, base[1], base[2] * 1.12))
        key(ar, 'location', p_dn1, base)
    cam, t = camera((0, -14.5, 0), (0, 0, 0), lens=35)
    key(cam, 'location', 1, -15.5, 1); key(cam, 'location', N, -13.5, 1)

def shot_H(sc, N):
    sc.world.color = (0.12, 0.14, 0.18)
    L, Rr = (0, 0, 2.05), (0, 0, -2.05)
    pl, _ = panel_with_hole(L, 'round', size=(2.7, 0.08, 3.5), hw=1.2)
    pr, _ = panel_with_hole(Rr, 'square', size=(2.7, 0.08, 3.5), hw=1.2, hh=1.2)
    f_round, f_sq = round((39.5 - 39.4) * FPS) + 6, round((42.41 - 39.4) * FPS)
    # even stress ring around the round hole (amber)
    ring = torus((L[0], -0.06, L[2]), 0.66, 0.05, ORANGE, rot=(90, 0, 0))
    key(ring, 'scale', 1, (0.01, 0.01, 0.01)); key(ring, 'scale', f_round + 20, (1, 1, 1))
    # hot spots at the square corners (red, growing + pulsing)
    for sx in (-1, 1):
        for sz in (-1, 1):
            hs = sphere((Rr[0] + sx * 0.6, -0.08, Rr[2] + sz * 0.6), 0.16, RED, scale=(1, 0.3, 1), rough=0.2)
            key(hs, 'scale', 1, (0.01, 0.01, 0.01)); key(hs, 'scale', f_sq, (0.01, 0.01, 0.01))
            key(hs, 'scale', f_sq + 15, (1.6, 0.3, 1.6))
            for k, f in enumerate(range(f_sq + 25, N, 14)):
                s = 1.4 if k % 2 else 1.8
                key(hs, 'scale', f, (s, 0.3, s))
    # pulling arrows on outer edges
    for x, d in ((-1.75, -1), (1.75, 1)):
        for z in (-3.1, -2.05, -1.0, 1.0, 2.05, 3.1):
            a = cone((x + d * 0.25, -0.1, z), 0.12, 0, 0.3, (0.9, 0.9, 0.9), rot=(0, 90 * d, 0))
            s = cyl((x, -0.1, z), 0.04, 0.35, (0.9, 0.9, 0.9), rot=(0, 90, 0))
    cam, t = camera((0, -15.0, 0), (0, 0, 0), lens=40)
    key(cam, 'location', 1, -15.5, 1); key(cam, 'location', N, -14.5, 1)

def shot_I(sc, N):
    sc.world.color = (0.12, 0.14, 0.18)
    skin = cube((0, 0, 0), (5, 0.08, 5), SILVER, metal=0.6, rough=0.35)
    h = rrect('sq', 1.6, 1.6, 0.6, 0.2, SILVER, loc=(-0.8, 0, -0.8))
    cut(skin, h)
    corner = (0.0, -0.05, 0.0)
    rnd = random.Random(9)
    f = 6
    for i in range(9):
        ang = radians(rnd.uniform(15, 75))
        crack(zigzag(corner, (cos(ang), sin(ang)), rnd.uniform(0.6, 1.8), segs=9, jitter=0.06, seed=20 + i),
              DARK, 0.012, f, f + 20)
        f += 14
    glow = sphere((corner[0], -0.06, corner[2]), 0.12, RED, scale=(1, 0.3, 1))
    for k, fr in enumerate(range(1, N, 9)):
        s = 1.0 if k % 2 else 1.6
        key(glow, 'scale', fr, (s, 0.3, s))
    cam, t = camera((0.6, -4.0, 0.6), (0.35, 0, 0.35), lens=50)
    key(cam, 'location', 1, -4.2, 1); key(cam, 'location', N, -3.0, 1)
    # tiny tremor each cycle
    shake(cam, 2, N - 2, 0.012, seed=8)

def shot_J(sc, N):
    c = cabin(sc, 0.0)
    cam, t = camera((0, -4.4, 0.2), (0, 0.5, 0.2), lens=50)
    drift(c['clouds'], 1, N, -1.5)
    set_round(c, 6, 0.0); set_round(c, 40, 1.0)          # "rounded every corner"
    # pull back to reveal the seat (around 54.3 s)
    f_back = round((54.3 - 52.2) * FPS)
    key(cam, 'location', f_back, (0, -4.4, 0.2)); key(t, 'location', f_back, (0, 0.5, 0.2))
    key(cam, 'location', N, (-2.6, -9.5, 0.6)); key(t, 'location', N, (0.6, 0.3, -0.6))
    # second window + seat
    w2 = rrect('hole2', 1.30, 1.85, 1.2, 0.55, CREAM, loc=(2.6, 0.25, 0.2), n=12)
    w2.data.shape_keys.key_blocks['round'].value = 1.0
    cut(c['wall'], w2)
    seat = empty((-0.9, -1.4, -2.4))
    back = cube((-0.9, -1.25, -1.0), (1.6, 0.45, 2.4), (0.16, 0.22, 0.42), rot=(-8, 0, 0), rough=0.8)
    head = cube((-0.9, -1.2, 0.35), (1.3, 0.4, 0.5), (0.85, 0.85, 0.88), rot=(-8, 0, 0), rough=0.8)
    cush = cube((-0.9, -2.1, -2.05), (1.6, 1.4, 0.4), (0.16, 0.22, 0.42), rough=0.8)
    arm = cube((-0.05, -1.9, -1.7), (0.12, 1.4, 0.15), (0.3, 0.3, 0.32))
    floor = cube((0, -3, -2.5), (12, 8, 0.2), (0.35, 0.36, 0.40))

def shot_K(sc, N):
    c = cabin(sc, 1.0)
    # pane rim + tiny breather hole near the bottom of the pane
    rim = rrect('rim', 1.02, 1.52, 0.02, 0.44, (0.90, 0.92, 0.95), loc=(0, 0.62, 0.2), n=12)
    inner = rrect('rimc', 0.98, 1.48, 0.2, 0.42, (0.9, 0.9, 0.9), loc=(0, 0.62, 0.2), n=12)
    rim.data.shape_keys.key_blocks['round'].value = 1; inner.data.shape_keys.key_blocks['round'].value = 1
    cut(rim, inner)
    dot = cyl((0, 0.62, -0.42), 0.022, 0.03, DARK, rot=(90, 0, 0))
    halo = torus((0, 0.60, -0.42), 0.07, 0.008, RED, rot=(90, 0, 0))
    key(halo, 'scale', 1, (0.01, 0.01, 0.01)); key(halo, 'scale', 40, (0.01, 0.01, 0.01)); key(halo, 'scale', 55, (1, 1, 1))
    drift(c['clouds'], 1, N, -0.8)
    cam, t = camera((0, -5.2, 0.2), (0, 0.5, 0.2), lens=50)
    key(cam, 'location', 1, (0, -5.2, 0.2)); key(t, 'location', 1, (0, 0.5, 0.2))
    key(cam, 'location', N - 10, (0, -0.6, -0.40)); key(t, 'location', N - 10, (0, 0.62, -0.42))

def build(shot):
    sc = reset()
    N = nframes(shot)
    sc.frame_start, sc.frame_end = 1, N
    globals()['shot_' + shot](sc, N)
    ease_all()
    return sc, N

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    shot = args[0]
    opts = dict(a.split('=') for a in args[1:])
    sc, N = build(shot)
    here = os.path.dirname(os.path.abspath(__file__))
    if 'preview' in opts:
        os.makedirs(f'{here}/preview', exist_ok=True)
        for fr in opts['preview'].split(','):
            sc.frame_set(int(fr)); sc.render.filepath = f'{here}/preview/{shot}_{int(fr):04d}.png'
            bpy.ops.render.render(write_still=True)
    else:
        a, b = (int(x) for x in opts['frames'].split('-')) if 'frames' in opts else (1, N)
        os.makedirs(f'{here}/frames/{shot}', exist_ok=True)
        for fr in range(a, b + 1):
            out = f'{here}/frames/{shot}/{fr:04d}.png'
            if os.path.exists(out) and 'force' not in opts: continue
            sc.frame_set(fr); sc.render.filepath = out
            bpy.ops.render.render(write_still=True)
        print('DONE', shot, N)
