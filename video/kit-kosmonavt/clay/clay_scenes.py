"""Claymation scenes for 'kit-kosmonavt', built and rendered in Blender (Cycles, CPU).
Run:  blender -b -noaudio -P clay/clay_scenes.py -- 01 [preview]
Renders shot frames to clay/frames/NN/ ; 'preview' renders only the middle frame."""
import bpy, math, random, sys, os
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['01']
SHOT = ARGS[0]; PREVIEW = 'preview' in ARGS
FRAMES = [a for a in ARGS if a.startswith('frames=')]
FPS = 12
DUR = {'01': 3.0, '02': 6.0, '03': 5.8, '04': 5.4, '05': 4.2, '06': 3.6, '07': 3.6, '08': 4.4}
NF = int(round(DUR[SHOT] * FPS))
HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(int(SHOT))

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 16
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.max_bounces = 4; sc.cycles.transmission_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.volume_bounces = 0
sc.render.resolution_x, sc.render.resolution_y = 540, 960
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NF
sc.render.image_settings.file_format = 'PNG'
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
except Exception: pass
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
def world_color(c, s=1.0):
    bg = world.node_tree.nodes['Background']; bg.inputs[0].default_value = (*c, 1); bg.inputs[1].default_value = s

# ---------------------------------------------------------------- materials
MATS = {}
def P(bsdf, name, val):
    for n in ([name] if isinstance(name, str) else name):
        if n in bsdf.inputs: bsdf.inputs[n].default_value = val; return

def clay(name, rgb, rough=0.55, sss=0.25, bump=0.18, metal=0.0, emit=0.0):
    key = (name, rgb, metal, emit)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    P(b, 'Base Color', (*rgb, 1)); P(b, 'Roughness', rough); P(b, 'Metallic', metal)
    P(b, ['Subsurface Weight', 'Subsurface'], sss); P(b, 'Subsurface Radius', (0.25, 0.12, 0.08))
    if emit:
        P(b, ['Emission Color', 'Emission'], (*rgb, 1)); P(b, 'Emission Strength', emit)
    if bump:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 6; n1.inputs['Detail'].default_value = 8
        w = nt.nodes.new('ShaderNodeTexWave'); w.wave_type = 'RINGS'; w.inputs['Scale'].default_value = 16
        w.inputs['Distortion'].default_value = 9; w.inputs['Detail'].default_value = 2
        n2 = nt.nodes.new('ShaderNodeTexVoronoi'); n2.inputs['Scale'].default_value = 3.5
        nt.links.new(tc.outputs['Object'], n1.inputs['Vector']); nt.links.new(tc.outputs['Object'], w.inputs['Vector'])
        nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
        mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MULTIPLY'
        nt.links.new(w.outputs['Fac'], mx.inputs[0]); nt.links.new(n2.outputs['Distance'], mx.inputs[1])  # fingerprints in patches
        ad = nt.nodes.new('ShaderNodeMath'); ad.operation = 'ADD'
        nt.links.new(n1.outputs['Fac'], ad.inputs[0]); nt.links.new(mx.outputs[0], ad.inputs[1])
        bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; bm.inputs['Distance'].default_value = 0.02
        nt.links.new(ad.outputs[0], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    MATS[key] = m; return m

def glass():
    m = bpy.data.materials.new('glass'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    P(b, 'Base Color', (0.9, 0.97, 1, 1)); P(b, 'Roughness', 0.03); P(b, ['Transmission Weight', 'Transmission'], 1.0); P(b, 'IOR', 1.08)
    return m

ORANGE = (0.85, 0.36, 0.08); DARKOR = (0.55, 0.18, 0.03); WHITE = (0.92, 0.9, 0.85); PINK = (0.95, 0.45, 0.5)
GREEN = (0.15, 0.7, 0.25); BLACK = (0.02, 0.02, 0.02); CARD = (0.62, 0.43, 0.24); FOIL = (0.8, 0.8, 0.82)
CHEESE = (0.95, 0.72, 0.15); TAPE = (0.85, 0.78, 0.6)

# ---------------------------------------------------------------- primitives
def _fin(o, mat, parent, smooth=True):
    if mat: o.data.materials.append(mat)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o
def sphere(loc, r=1, sc=(1, 1, 1), mat=None, parent=None, seg=40):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.scale = sc; return _fin(o, mat, parent)
def cube(loc, size=(1, 1, 1), mat=None, parent=None, bevel=0.03, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 3
    return _fin(o, mat, parent, smooth=False)
def cyl(loc, r, depth, mat=None, parent=None, rot=(0, 0, 0), r2=None, verts=40):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    md = o.modifiers.new('b', 'BEVEL'); md.width = min(r, depth) * 0.15; md.segments = 3; md.limit_method = 'ANGLE'
    return _fin(o, mat, parent)
def torus(loc, R, r, mat=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot)
    return _fin(bpy.context.object, mat, parent)
def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); sc.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o
def key(o, path, f, v):
    setattr(o, path, v) if not isinstance(v, (list, tuple)) else setattr(o, path, v)
    o.keyframe_insert(path, frame=f)
def light(kind, loc, energy, color=(1, 1, 1), size=3, rot=None, target=(0, 0, 0.8)):
    d = bpy.data.lights.new(kind, kind); d.energy = energy; d.color = color
    if kind == 'AREA': d.size = size
    o = bpy.data.objects.new(kind, d); sc.collection.objects.link(o); o.location = loc
    tr = o.constraints.new('TRACK_TO'); tr.target = empty('lt', target); tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
    return o
def camera(loc, target, lens=50):
    d = bpy.data.cameras.new('cam'); d.lens = lens
    d.dof.use_dof = True; d.dof.aperture_fstop = 2.8
    o = bpy.data.objects.new('cam', d); sc.collection.objects.link(o); o.location = loc; sc.camera = o
    t = empty('camtarget', target); tr = o.constraints.new('TRACK_TO'); tr.target = t
    tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'; d.dof.focus_object = t
    return o, t

# ---------------------------------------------------------------- the cat
def make_cat(loc=(0, 0, 0), suit=False, helmet=False, lying=False):
    root = empty('cat', loc)
    body_m = clay('foil', FOIL, rough=0.22, sss=0, bump=0.9, metal=1.0) if suit else clay('fur', ORANGE)
    fur = clay('fur', ORANGE); white = clay('white', WHITE); dark = clay('stripe', DARKOR)
    bodyE = empty('bodyE', (0, 0, 0), root)
    body = sphere((0, 0.05, 0.5), 0.5, (1.0, 0.95, 0.88), body_m, bodyE)
    if not suit:
        sphere((0, -0.36, 0.62), 0.22, (1, 0.5, 1.25), white, bodyE)               # chest patch
        for k, z in enumerate((0.75, 0.55, 0.38)):
            sphere((0, 0.38, z), 0.2, (1.9, 0.35, 0.22), dark, bodyE)                 # back stripes
    else:
        torus((0, 0, 0.92), 0.3, 0.06, clay('collar', (0.75, 0.75, 0.78), 0.3, 0, 0.6, 1.0), bodyE)
        sphere((0, -0.44, 0.55), 0.09, (1, 0.5, 1), clay('btn', (0.9, 0.15, 0.1)), bodyE)   # red button
    for x in (-0.22, 0.22):
        sphere((x, -0.36, 0.1), 0.13, (1, 1.3, 0.75), body_m, bodyE)                  # front paws
        sphere((x * 1.4, 0.15, 0.12), 0.16, (1, 1.4, 0.7), body_m, bodyE)             # back legs
    # tail (curve)
    cu = bpy.data.curves.new('tail', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.06; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(2)
    for p, co in zip(sp.bezier_points, [(0, 0.45, 0.2), (0.3, 0.62, 0.3), (0.42, 0.7, 0.62)]):
        p.co = co; p.handle_left_type = p.handle_right_type = 'AUTO'
    tail = bpy.data.objects.new('tail', cu); sc.collection.objects.link(tail); tail.parent = bodyE
    tail.data.materials.append(fur if not suit else body_m)
    tailE = tail
    # head
    head = empty('head', (0, -0.05, 1.12), root)
    sphere((0, 0, 0), 0.42, (1.08, 0.95, 0.92), fur, head)
    for x in (-1, 1):
        e = cyl((0.24 * x, 0.02, 0.36), 0.14, 0.26, fur, head, rot=(0, 0.3 * x, 0), r2=0.01)
        cyl((0.24 * x, -0.03, 0.34), 0.08, 0.17, clay('innerear', PINK), head, rot=(0, 0.3 * x, 0), r2=0.01)
    for x in (-0.12, 0, 0.12):
        sphere((x, -0.06, 0.37), 0.06, (0.6, 1.6, 0.35), dark, head)                 # forehead stripes
    for x in (-0.09, 0.09):
        sphere((x, -0.36, -0.12), 0.11, (1, 0.7, 0.8), white, head)                  # muzzle
    sphere((0, -0.43, -0.04), 0.05, (1.3, 0.8, 0.8), clay('nose', PINK, 0.4), head)
    eyes = []
    for x in (-0.16, 0.16):
        eE = empty('eye', (x, -0.33, 0.06), head)
        sphere((0, 0, 0), 0.12, (1, 0.6, 1.1), clay('eyewhite', (0.97, 0.97, 0.95), 0.15, 0.05, 0.05), eE)
        sphere((0, -0.06, 0), 0.085, (1, 0.4, 1.05), clay('iris', GREEN, 0.15, 0.05, 0.03), eE)
        sphere((0, -0.085, 0), 0.05, (1, 0.35, 1.1), clay('pupil', BLACK, 0.1, 0, 0.02), eE)
        sphere((0.03, -0.105, 0.04), 0.018, (1, 1, 1), clay('hl', (1, 1, 1), 0.1, 0, 0, emit=3), eE)
        lid = sphere((0, -0.01, 0.0), 0.128, (1.05, 0.65, 0.001), fur, eE)            # eyelid (scale z to blink)
        eyes.append(lid)
    for s in (-1, 1):
        for k in range(3):
            cyl((0.27 * s, -0.42, -0.1 + 0.04 * (k - 1)), 0.009, 0.24, clay('wh', (0.95, 0.95, 0.9), 0.4, 0, 0), head,
                rot=(0, math.pi / 2 + 0.12 * (k - 1) * s, 0))
    if helmet:
        sphere((0, -0.02, 0.02), 0.62, (1, 1, 1), glass(), head, seg=64)
    if lying:
        root.rotation_euler = (0, 0, 0)
    return dict(root=root, body=bodyE, head=head, tail=tailE, lids=eyes)

def boil(objs, amt=0.012):
    """Stop-motion 'boil': tiny random pose changes every frame."""
    for o in objs:
        base_r = tuple(o.rotation_euler); base_l = tuple(o.location)
        for f in range(1, NF + 1):
            o.rotation_euler = tuple(b + random.uniform(-amt, amt) for b in base_r); o.keyframe_insert('rotation_euler', frame=f)

def blink(lids, f0, closed=2):
    for l in lids:
        for f, z in ((f0 - 1, 0.001), (f0, 1.0), (f0 + closed, 1.0), (f0 + closed + 1, 0.001)):
            l.scale = (1.05, 0.65, z); l.keyframe_insert('scale', frame=f)

def stars(n=160, rad=30, center=(0, 15, 5), zmin=-5):
    m = clay('star', (1, 0.95, 0.7), 0.5, 0, 0, emit=12)
    for _ in range(n):
        v = Vector((random.uniform(-1, 1), random.uniform(0.2, 1), random.uniform(-0.6, 1))).normalized() * rad
        p = Vector(center) + v
        if p.z > zmin: sphere(tuple(p), random.uniform(0.04, 0.12), (1, 1, 1), m, seg=8)

def rocket(loc, parent=None):
    r = empty('rocket', loc, parent)
    card = clay('card', CARD, 0.75, 0.05, 0.25)
    cube((0, 0, 0.9), (1.3, 1.3, 1.8), card, r, 0.04)
    cyl((0, 0, 2.15), 0.55, 0.9, clay('bottle', (0.3, 0.6, 0.9), 0.15, 0.1, 0.05), r, r2=0.05)
    for a in range(3):
        ang = a * 2 * math.pi / 3
        cube((0.75 * math.cos(ang), 0.75 * math.sin(ang), 0.35), (0.06, 0.5, 0.6), clay('fin', (0.85, 0.2, 0.15)), r, 0.02, rot=(0, 0, ang + math.pi / 2))
    torus((0, -0.66, 1.1), 0.3, 0.05, clay('foilring', FOIL, 0.25, 0, 0.7, 1.0), r, rot=(math.pi / 2, 0, 0))
    for k, z in enumerate((0.4, 0.7, 1.4, 1.65)):  # tape strips
        cube((0, -0.66, z), (1.32, 0.02, 0.1), clay('tape', TAPE, 0.35, 0.1, 0.1), r, 0)
    return r

# ---------------------------------------------------------------- shots
def shot01():  # hook: cat in fishbowl helmet inside cardboard rocket, shaking
    world_color((0.02, 0.03, 0.08), 0.6)
    cat = make_cat((0, 0, 0.3), suit=True, helmet=True)
    card = clay('card', CARD, 0.75, 0.05, 0.25)
    box = empty('box', (0, 0, 0))
    cube((0, -0.75, 0.55), (2.2, 0.08, 1.1), card, box)                         # front wall
    cube((0, 0.9, 1.0), (2.2, 0.08, 2.0), card, box); cube((-1.1, 0, 0.9), (0.08, 1.8, 1.8), card, box); cube((1.1, 0, 0.9), (0.08, 1.8, 1.8), card, box)
    cube((0, -0.82, 0.9), (1.6, 0.25, 0.16), clay('panel', (0.2, 0.25, 0.3)), box, 0.02, rot=(0.5, 0, 0))
    btns = []
    for k, c in enumerate([(1, 0.1, 0.1), (0.1, 1, 0.2), (1, 0.8, 0.1), (0.2, 0.5, 1), (1, 0.3, 0.8)]):
        b = cyl((-0.6 + k * 0.3, -0.9, 0.98), 0.07, 0.06, clay(f'btn{k}', c, 0.3, 0, 0, emit=1.2), box, rot=(0.5 + math.pi / 2, 0, 0))
        btns.append(b)
    # window with stars and moon behind
    cube((0, 3, 2.2), (8, 0.1, 6), clay('sky', (0.03, 0.05, 0.18), 0.9, 0, 0, emit=0.6), None, 0)
    sphere((1.4, 2.8, 2.6), 0.5, (1, 0.2, 1), clay('moonbg', CHEESE, 0.6, 0, 0.1, emit=2.5))
    for _ in range(40):
        sphere((random.uniform(-3, 3), 2.9, random.uniform(0.8, 4)), 0.025, (1, 1, 1), clay('star', (1, 0.95, 0.7), 0.5, 0, 0, emit=12), seg=8)
    light('AREA', (-2.5, -3, 3.5), 450, (1, 0.85, 0.7), 3); light('AREA', (2.5, -2, 2), 150, (0.6, 0.7, 1), 2)
    light('POINT', (0, -1.5, 1.2), 40, (0.4, 1, 0.6))
    cam, t = camera((0.15, -4.2, 1.9), (0, 0, 1.35), 55)
    key(cam, 'location', 1, (0.15, -4.2, 1.9)); key(cam, 'location', NF, (0.08, -3.1, 1.75))
    for f in range(1, NF + 1):  # rumble grows
        a = 0.01 + 0.05 * f / NF
        for o in (box, cat['root']):
            o.location = (random.uniform(-a, a), random.uniform(-a, a) * 0.3, random.uniform(0, a)) if o is box else (random.uniform(-a, a), 0, 0.3 + random.uniform(0, a))
            o.keyframe_insert('location', frame=f)
    blink(cat['lids'], 20)

def shot02():  # night window, cat looking at the moon
    world_color((0.01, 0.02, 0.06), 0.4)
    room = clay('wall', (0.35, 0.3, 0.45), 0.8, 0.05, 0.3)
    cube((0, 0.6, 0.0), (5, 1.4, 0.3), clay('sill', (0.55, 0.4, 0.3), 0.7), None, 0.04)            # sill
    for x in (-2.0, 2.0): cube((x, 0.7, 2.2), (1.4, 0.3, 4.4), room)
    cube((0, 0.7, 4.0), (5.4, 0.3, 0.9), room); cube((0, 0.62, 2.2), (0.12, 0.12, 3.6), room)           # frame + mullion
    cube((0, 6, 2), (20, 0.1, 14), clay('sky', (0.03, 0.06, 0.2), 0.9, 0, 0, emit=0.8), None, 0)
    sphere((1.1, 5.5, 3.2), 1.25, (1, 0.25, 1), clay('moon', CHEESE, 0.6, 0, 0.3, emit=3.5))
    for _ in range(80): sphere((random.uniform(-6, 6), 5.8, random.uniform(0.5, 7)), 0.03, (1, 1, 1), clay('star', (1, 0.95, 0.7), 0.5, 0, 0, emit=12), seg=8)
    cat = make_cat((-0.2, 0.2, 0.15)); cat['root'].rotation_euler = (0, 0, math.pi + 0.35)                # back to camera
    light('AREA', (1.2, 4.5, 3.5), 900, (0.6, 0.7, 1), 4, target=(0, 0, 0.8))                      # moonlight
    light('AREA', (-3, -3, 2.5), 260, (1, 0.7, 0.45), 3)
    cam, t = camera((-1.6, -3.4, 1.4), (0.2, 0.6, 1.6), 40)
    key(cam, 'location', 1, (-1.6, -3.4, 1.4)); key(cam, 'location', NF, (-1.1, -2.5, 1.45))
    tl = cat['tail']
    for f in range(1, NF + 1, 3):
        tl.rotation_euler = (0, 0, 0.35 * math.sin(f / 6)); tl.keyframe_insert('rotation_euler', frame=f)
    h = cat['head']
    for f, r in ((1, 0), (24, 0), (34, 0.3), (60, 0.3), (NF, 0.1)):
        h.rotation_euler = (0.25, r, 0); h.keyframe_insert('rotation_euler', frame=f)
    for f, s in ((1, 1), (40, 1), (46, 1.06), (54, 1)):   # sigh
        cat['body'].scale = (1, 1, s); cat['body'].keyframe_insert('scale', frame=f)

def shot03():  # workshop: building the rocket, tangled in tape
    world_color((0.3, 0.25, 0.2), 0.5)
    cube((0, 0, -0.05), (10, 10, 0.1), clay('floor', (0.45, 0.32, 0.22), 0.8, 0.05, 0.4), None, 0)
    cube((0, 3, 2.5), (10, 0.1, 5), clay('wall3', (0.75, 0.62, 0.45), 0.85), None, 0)
    for k in range(3):  # crayon moon drawings on wall
        cube((-2 + k * 1.3, 2.93, 2.4 + 0.2 * (k % 2)), (0.9, 0.02, 0.9), clay('paper', (0.95, 0.93, 0.85), 0.9, 0, 0.05), None, 0)
        sphere((-2 + k * 1.3, 2.9, 2.4 + 0.2 * (k % 2)), 0.28, (1, 0.05, 1), clay('crayonmoon', CHEESE, 0.9, 0, 0.1))
    rk = rocket((1.3, 0.8, 0)); rk.rotation_euler = (0, 0, -0.4)
    rolls = []
    for p in ((-1.4, -0.5, 0.1), (-0.9, 0.9, 0.1), (0.4, -1.1, 0.1)):
        rolls.append(torus(p, 0.22, 0.09, clay('tape', TAPE, 0.35, 0.1, 0.1)))
    cat = make_cat((-0.4, -0.2, 0)); cat['root'].rotation_euler = (0, 0, 0.35)
    # tape strip from paw to roll
    roll = torus((-0.3, -0.85, 0.5), 0.2, 0.08, clay('tape', TAPE, 0.35, 0.1, 0.1))
    strip = cube((-0.55, -0.7, 0.35), (0.06, 0.02, 0.5), clay('tape', TAPE, 0.35, 0.1, 0.1), None, 0, rot=(0.3, 0.6, 0))
    for f in range(1, NF + 1, 2):  # struggling: roll flaps around
        roll.location = (-0.3 + 0.25 * math.sin(f / 3), -0.85, 0.5 + 0.2 * abs(math.sin(f / 4))); roll.keyframe_insert('location', frame=f)
        roll.rotation_euler = (f / 4, 0.4 * math.sin(f / 2), 0); roll.keyframe_insert('rotation_euler', frame=f)
        strip.rotation_euler = (0.3, 0.6 + 0.4 * math.sin(f / 3), 0); strip.keyframe_insert('rotation_euler', frame=f)
        cat['head'].rotation_euler = (0.15, 0, 0.25 * math.sin(f / 5)); cat['head'].keyframe_insert('rotation_euler', frame=f)
    light('AREA', (-3, -3, 4), 650, (1, 0.85, 0.65), 4); light('AREA', (3, -2, 2), 180, (0.8, 0.85, 1), 3)
    cam, t = camera((0, -5, 2.0), (0.2, 0.1, 0.9), 40)
    for f in range(1, NF + 1, 4):
        a = -0.5 + 0.7 * f / NF
        cam.location = (5 * math.sin(a), -5 * math.cos(a), 2.0); cam.keyframe_insert('location', frame=f)
    blink(cat['lids'], 30)

def shot04():  # mirror pose in foil suit, annoyed goldfish
    world_color((0.6, 0.7, 0.75), 0.5)
    cube((0, 0, -0.05), (10, 10, 0.1), clay('tilefloor', (0.85, 0.85, 0.82), 0.6), None, 0)
    for i in range(-4, 5):
        for j in range(0, 7):
            cube((i * 0.62, 2.5, j * 0.62 + 0.3), (0.58, 0.06, 0.58), clay('tile', (0.55, 0.78, 0.82), 0.35, 0.05, 0.2), None, 0.03)
    cat = make_cat((0, 0, 0), suit=True, helmet=True)
    cube((1.15, 0.3, 0.45), (0.9, 0.7, 0.9), clay('stool', (0.9, 0.9, 0.9), 0.5), None, 0.08)
    sphere((1.15, 0.3, 1.25), 0.38, (1, 1, 0.8), glass(), seg=48)
    fish = []
    for k in range(2):
        fe = empty('fish', (1.15, 0.3, 1.2))
        f = sphere((0.15, 0, 0), 0.1, (1.4, 0.7, 1), clay('fishm', (1, 0.45, 0.05), 0.3), fe)
        cyl((0.32, 0, 0), 0.08, 0.12, clay('fishm', (1, 0.45, 0.05), 0.3), fe, rot=(0, math.pi / 2, 0), r2=0.0)
        sphere((0.05, -0.07, 0.03), 0.025, (1, 1, 1), clay('pupil', BLACK, 0.1, 0, 0.02), fe)
        cube((0.05, -0.07, 0.065), (0.05, 0.01, 0.012), clay('pupil', BLACK, 0.1, 0, 0.02), fe, 0, rot=(0, 0.5, 0))   # frown brow
        fish.append(fe)
    for f in range(1, NF + 1, 2):
        for k, fe in enumerate(fish):
            a = f / 6 + k * math.pi
            fe.rotation_euler = (0, 0, a + math.pi / 2); fe.location = (1.15 + 0.16 * math.cos(a), 0.3 + 0.16 * math.sin(a), 1.15 + 0.08 * k)
            fe.keyframe_insert('rotation_euler', frame=f); fe.keyframe_insert('location', frame=f)
    b = cat['body']; h = cat['head']
    for f, s, hr in ((1, 1.0, 0), (14, 1.0, 0), (20, 1.12, -0.18), (NF, 1.12, -0.18)):   # proud chest puff, chin up
        b.scale = (1, s, 1); b.keyframe_insert('scale', frame=f); h.rotation_euler = (hr, 0, 0); h.keyframe_insert('rotation_euler', frame=f)
    light('AREA', (-2, -3, 4), 550, (1, 0.95, 0.9), 4); light('AREA', (3, -1, 3), 200, (0.8, 0.9, 1), 3)
    cam, t = camera((0.8, -4.8, 1.4), (0.55, 0, 1.0), 42)
    key(cam, 'location', 1, (0.8, -4.8, 1.4)); key(cam, 'location', NF, (0.65, -3.9, 1.35))
    blink(cat['lids'], 44)

def shot05():  # launch
    world_color((0.02, 0.03, 0.09), 0.5)
    cube((0, 0, -0.05), (30, 30, 0.1), clay('grass', (0.12, 0.35, 0.12), 0.85, 0.05, 0.6), None, 0)
    cube((0, 8, 1.2), (30, 0.2, 2.4), clay('fence', (0.4, 0.28, 0.18), 0.8), None, 0.05)
    cube((0, 15, 8), (60, 0.1, 30), clay('sky', (0.03, 0.05, 0.18), 0.9, 0, 0, emit=0.6), None, 0)
    for _ in range(80): sphere((random.uniform(-14, 14), 14.8, random.uniform(2, 20)), 0.06, (1, 1, 1), clay('star', (1, 0.95, 0.7), 0.5, 0, 0, emit=12), seg=8)
    rk = rocket((0, 0, 0))
    cat = make_cat((0, -0.2, 0.75), suit=True, helmet=True); cat['root'].scale = (0.38, 0.38, 0.38); cat['root'].parent = rk
    fl = empty('flames', (0, 0, 0), rk)
    for k in range(5):
        cyl((random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), -0.55), 0.3, 1.2, clay(f'flame{k%2}', ((1, 0.55, 0.05) if k % 2 else (1, 0.85, 0.2)), 0.5, 0, 0.2, emit=8), fl, rot=(math.pi, 0, 0), r2=0.02)
    smoke = clay('cotton', (0.95, 0.95, 0.95), 0.9, 0.6, 1.2)
    puffs = [sphere((random.uniform(-1.5, 1.5), random.uniform(-1.2, 1.2), random.uniform(0.1, 0.5)), random.uniform(0.25, 0.5), (1, 1, 0.85), smoke) for _ in range(26)]
    lift = 14
    for f in range(1, NF + 1):
        t_ = max(0, (f - lift) / (NF - lift))
        rk.location = (random.uniform(-0.04, 0.04), random.uniform(-0.04, 0.04), 7.5 * t_ ** 2 + (random.uniform(0, 0.05) if f < lift else 0))
        rk.keyframe_insert('location', frame=f)
        fl.scale = (1, 1, 0.3 + (0.7 if f >= lift - 4 else 0.3 * f / lift) * random.uniform(0.85, 1.15)); fl.keyframe_insert('scale', frame=f)
        for p in puffs:
            g = 0.15 + 1.4 * min(1, f / NF * 1.4); p.scale = (g, g, g * 0.85); p.keyframe_insert('scale', frame=f)
    light('POINT', (0, -1.2, 0.3), 1500, (1, 0.6, 0.2)); light('AREA', (-4, -5, 5), 900, (0.7, 0.8, 1), 6); light('AREA', (3, -4, 3), 300, (1, 0.85, 0.7), 4)
    cam, t = camera((0, -6.2, 1.0), (0, 0, 1.4), 30)
    for f in range(1, NF + 1):
        t_ = max(0, (f - lift) / (NF - lift))
        t.location = (0, 0, 1.4 + 6.5 * t_ ** 2); t.keyframe_insert('location', frame=f)
        cam.location = (random.uniform(-0.05, 0.05), -6.2, 1.0 + random.uniform(-0.05, 0.05)); cam.keyframe_insert('location', frame=f)

def shot06():  # floating in space
    world_color((0.0, 0.0, 0.01), 0.2)
    stars(260, 30, (0, 10, 0), -40)
    earth = sphere((5.5, 12, -3.5), 2.6, (1, 1, 1), clay('ocean', (0.1, 0.35, 0.85), 0.5, 0.1, 0.4), seg=64)
    for _ in range(9):
        d = Vector((random.uniform(-1, 1), random.uniform(-1, 0.2), random.uniform(-1, 1))).normalized() * 2.5
        sphere(tuple(Vector((5.5, 12, -3.5)) + d), random.uniform(0.5, 0.9), (1, 1, 0.25), clay('land', (0.2, 0.6, 0.2), 0.7, 0.05, 0.5)).rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    cat = make_cat((0, 0, 0), suit=True, helmet=True)
    r = cat['root']
    for f in range(1, NF + 1, 2):
        r.rotation_euler = (0.25 * math.sin(f / 9), 0.5 * math.sin(f / 12) + f * 0.015, 0.3 * math.sin(f / 7)); r.location = (0, 0, 0.12 * math.sin(f / 6))
        r.keyframe_insert('rotation_euler', frame=f); r.keyframe_insert('location', frame=f)
    light('SUN', (-5, -5, 5), 3.5, (1, 0.95, 0.85)); light('AREA', (4, 2, -1), 250, (0.4, 0.6, 1), 4)
    cam, t = camera((0, -4.2, 1.0), (0.2, 0, 0.9), 40)
    for f in range(1, NF + 1, 3):
        a = -0.25 + 0.5 * f / NF
        cam.location = (4.2 * math.sin(a), -4.2 * math.cos(a), 1.0); cam.keyframe_insert('location', frame=f)

def shot07():  # cheese moon, bite
    world_color((0.0, 0.0, 0.01), 0.2)
    stars(160, 30, (0, 12, 2), 0)
    ch = clay('cheesemoon', CHEESE, 0.5, 0.35, 0.5)
    sphere((0, 0, -40), 40, (1, 1, 1), ch, seg=96)
    holes = clay('hole', (0.45, 0.28, 0.03), 0.8, 0.1, 0.3)
    for _ in range(20):
        sphere((random.uniform(-6, 6), random.uniform(-1, 10), 0.0), random.uniform(0.2, 0.7), (1, 1, 0.04), holes)
    sphere((-4, 14, 4), 1.2, (1, 1, 1), clay('ocean', (0.1, 0.35, 0.85), 0.5, 0.1, 0.4))
    cat = make_cat((0, 0, 0), suit=True, helmet=False)
    wedge = cube((0.25, -0.55, 0.85), (0.35, 0.28, 0.25), clay('cheesepiece', CHEESE, 0.45, 0.35, 0.4), cat['root'], 0.02, rot=(0, 0, 0.6))
    crumbs = [sphere((0.1, -0.6, 1.0), 0.035, (1, 1, 1), clay('cheesepiece', CHEESE, 0.45, 0.35, 0.4), seg=10) for _ in range(10)]
    bite = 20
    for f, p in ((1, (0.25, -0.55, 0.85)), (bite - 3, (0.1, -0.5, 0.98)), (bite, (0.05, -0.48, 1.0)), (bite + 4, (0.25, -0.55, 0.85)), (NF, (0.25, -0.55, 0.85))):
        wedge.location = p; wedge.keyframe_insert('location', frame=f)
    for c in crumbs:
        v = Vector((random.uniform(-1, 1), random.uniform(-1.2, -0.2), random.uniform(0.5, 1.5)))
        for f in range(1, NF + 1):
            tt = max(0, (f - bite) / 12)
            c.location = Vector((0.05, -0.5, 1.0)) + v * tt * 0.7 + Vector((0, 0, -0.9 * tt * tt)) if f >= bite else (0.05, -0.5, -5)
            c.keyframe_insert('location', frame=f)
    h = cat['head']
    for f, r in ((1, 0), (bite, 0.12), (bite + 3, -0.1), (bite + 8, 0.06), (NF, 0)):
        h.rotation_euler = (r, 0, 0); h.keyframe_insert('rotation_euler', frame=f)
    blink(cat['lids'], bite + 2, 8)   # blissful closed eyes
    light('SUN', (-5, -4, 6), 4.0, (1, 0.95, 0.85)); light('AREA', (3, -3, 2), 150, (0.6, 0.7, 1), 3)
    cam, t = camera((0.6, -4.0, 1.3), (0.1, 0, 1.0), 45)
    key(cam, 'location', 1, (0.6, -4.0, 1.3)); key(cam, 'location', NF, (0.35, -2.9, 1.25))

def shot08():  # morning, waking up in the box, cheese crumbs, wink
    world_color((0.9, 0.75, 0.55), 0.5)
    cube((0, 0, -0.05), (10, 10, 0.1), clay('rug', (0.65, 0.25, 0.25), 0.9, 0.05, 0.8), None, 0)
    cube((0, 3, 2.5), (10, 0.1, 5), clay('wallm', (0.9, 0.82, 0.62), 0.85), None, 0)
    card = clay('card', CARD, 0.75, 0.05, 0.25)
    cube((0, -0.95, 0.35), (2.2, 0.08, 0.7), card); cube((0, 0.95, 0.35), (2.2, 0.08, 0.7), card)
    cube((-1.1, 0, 0.35), (0.08, 1.9, 0.7), card); cube((1.1, 0, 0.35), (0.08, 1.9, 0.7), card)
    cube((0, -1.25, 0.45), (2.2, 0.06, 0.6), card, rot=(-0.7, 0, 0))   # open flap
    cat = make_cat((0, 0.1, 0.05)); cat['root'].scale = (1, 1, 0.92)
    cat['head'].location = (0, -0.25, 0.85)
    yel = clay('cheesepiece', CHEESE, 0.45, 0.35, 0.4)
    for p in ((-0.25, -0.75, 0.78), (0.27, -0.73, 0.8), (-0.3, -0.72, 0.72)): sphere(p, 0.03, (1, 1, 1), yel, seg=10)
    lids = cat['lids']
    for l in lids:  # eyes closed at start
        l.scale = (1.05, 0.65, 1.0); l.keyframe_insert('scale', frame=1); l.keyframe_insert('scale', frame=10)
    # left eye opens, right opens, then wink with right eye
    for f, z in ((14, 0.001),): lids[0].scale = (1.05, 0.65, z); lids[0].keyframe_insert('scale', frame=f)
    for f, z in ((16, 0.001), (36, 0.001), (38, 1.0), (44, 1.0), (46, 0.001)): lids[1].scale = (1.05, 0.65, z); lids[1].keyframe_insert('scale', frame=f)
    h = cat['head']
    for f, r in ((1, (0.2, 0, 0)), (12, (0.2, 0, 0)), (18, (0, 0, 0.1)), (36, (0, 0.18, 0)), (NF, (0, 0.18, 0))):
        h.rotation_euler = r; h.keyframe_insert('rotation_euler', frame=f)
    tongue = sphere((0.2, -0.44, -0.18), 0.05, (1, 0.6, 0.4), clay('tongue', (0.95, 0.35, 0.4), 0.3), h)
    for f, s in ((1, 0.0), (24, 0.0), (26, 1.0), (30, 1.0), (32, 0.0), (NF, 0.0)):
        tongue.scale = (s, s * 0.6, s * 0.4); tongue.keyframe_insert('scale', frame=f)
    light('AREA', (-3, -1, 3.5), 700, (1, 0.8, 0.55), 2.5); light('AREA', (3, -3, 2), 150, (0.8, 0.85, 1), 3)
    cam, t = camera((0.3, -4.0, 1.9), (0, -0.1, 0.8), 45)
    key(cam, 'location', 1, (0.3, -4.0, 1.9)); key(cam, 'location', NF, (0.15, -2.9, 1.6))

globals()['shot' + SHOT]()

# linear interpolation between poses; rendered at 12 fps for a stop-motion feel
def fcurves(act):
    if hasattr(act, 'fcurves'): return list(act.fcurves)
    out = []
    for layer in act.layers:
        for strip in layer.strips:
            for bag in strip.channelbags: out += list(bag.fcurves)
    return out
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        for fc in fcurves(o.animation_data.action):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

out = os.path.join(HERE, 'frames', SHOT); os.makedirs(out, exist_ok=True)
if PREVIEW:
    sc.frame_set(max(1, NF // 2)); sc.render.filepath = os.path.join(HERE, f'preview_{SHOT}.png')
    bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(out, 'f_')
    if FRAMES: a, b = FRAMES[0][7:].split('-'); sc.frame_start, sc.frame_end = int(a), int(b)
    bpy.ops.render.render(animation=True)
