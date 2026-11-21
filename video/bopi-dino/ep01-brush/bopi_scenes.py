"""Bopi Dino - ep01 'Brush Your Teeth'. Stylized glossy 3D (Pixar / nursery-3D look), Blender Cycles on CPU.
Run:  /opt/bpyenv/bin/python bopi_scenes.py -- S1 [preview] [frames=a-b]
Frames go to frames/S1/f_0001.png ...  Shot timings follow song.json (120 bpm, song starts at 2.5 s)."""
import bpy, math, random, sys, os
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['S1']
SHOT = ARGS[0]; PREVIEW = 'preview' in ARGS
FR = [a for a in ARGS if a.startswith('frames=')]
FPS = 12
# shot: (start s, end s) in the final timeline
SHOTS = {'S1': (0.0, 2.5), 'S2': (2.5, 6.5), 'S3': (6.5, 10.5), 'S4': (10.5, 14.5), 'S5': (14.5, 18.5),
         'S6': (18.5, 22.5), 'S7': (22.5, 26.5), 'S8': (26.5, 30.5), 'S9': (30.5, 36.5)}
T0, T1 = SHOTS[SHOT]; NF = int(round((T1 - T0) * FPS))
BEAT = 0.5
HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(hash(SHOT) % 1000)
def F(t):  # seconds inside the shot -> frame number
    return 1 + t * FPS
def beat_t(b):  # absolute song beat -> seconds inside this shot
    return 2.5 + b * BEAT - T0

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 10; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.06
sc.render.use_persistent_data = True; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 6; sc.cycles.transparent_max_bounces = 8; sc.cycles.volume_bounces = 0
sc.render.resolution_x, sc.render.resolution_y = 540, 960
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, NF
sc.render.image_settings.file_format = 'PNG'
sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = -0.3
try: sc.view_settings.look = 'None'
except Exception: pass
sc.render.film_transparent = False
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.75, 0.88, 1.0, 1); bg.inputs[1].default_value = 0.2

# ------------------------------------------------------------------ materials
MATS = {}
def P(b, names, v):
    for n in ([names] if isinstance(names, str) else names):
        if n in b.inputs: b.inputs[n].default_value = v; return
def toon(name, rgb, rough=0.35, sss=0.15, coat=0.4, emit=0.0, metal=0.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    P(b, 'Base Color', (*rgb, 1)); P(b, 'Roughness', rough); P(b, 'Metallic', metal)
    P(b, ['Subsurface Weight', 'Subsurface'], sss); P(b, 'Subsurface Radius', (0.4, 0.25, 0.2)); P(b, 'Subsurface Scale', 0.05)
    P(b, ['Coat Weight', 'Clearcoat'], coat); P(b, ['Coat Roughness', 'Clearcoat Roughness'], 0.15)
    P(b, ['Sheen Weight', 'Sheen'], 0.2)
    if emit: P(b, ['Emission Color', 'Emission'], (*rgb, 1)); P(b, 'Emission Strength', emit)
    MATS[name] = m; return m
def bubble_mat():
    if 'bubble' in MATS: return MATS['bubble']
    m = bpy.data.materials.new('bubble'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    P(b, 'Base Color', (1, 1, 1, 1)); P(b, 'Roughness', 0.0); P(b, ['Transmission Weight', 'Transmission'], 1.0); P(b, 'IOR', 1.02)
    P(b, 'Thin Film Thickness', 480.0); P(b, 'Thin Film IOR', 1.33)
    MATS['bubble'] = m; return m
def tiles_mat():
    m = bpy.data.materials.new('tiles'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    ck = nt.nodes.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = 24.0
    ck.inputs['Color1'].default_value = (0.30, 0.66, 0.95, 1); ck.inputs['Color2'].default_value = (0.45, 0.78, 1.0, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], ck.inputs['Vector'])
    nt.links.new(ck.outputs['Color'], b.inputs['Base Color']); P(b, 'Roughness', 0.3)
    return m

MINT = (0.12, 0.62, 0.30); BELLY = (1.0, 0.80, 0.35); SPIKE = (1.0, 0.32, 0.05); PINK = (1.0, 0.35, 0.45)
WHITE = (0.97, 0.97, 0.97); BLACK = (0.01, 0.01, 0.015); MOUTH = (0.35, 0.03, 0.06); TONGUE = (1.0, 0.35, 0.42)
BRUSH = (0.15, 0.45, 1.0); GERM = (0.55, 0.20, 0.85); WOOD = (0.95, 0.75, 0.55); DUCK = (1.0, 0.82, 0.1)

# ------------------------------------------------------------------ helpers
def _fin(o, mat, parent, smooth=True):
    if mat: o.data.materials.append(mat)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o
def sphere(loc, r=1, s=(1, 1, 1), mat=None, parent=None, seg=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = s; return _fin(o, mat, parent)
def cube(loc, size, mat=None, parent=None, bevel=0.05, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = size
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 4
    return _fin(o, mat, parent, smooth=True)
def cone(loc, r1, r2, depth, mat=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    return _fin(bpy.context.object, mat, parent)
def cyl(loc, r, depth, mat=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; md = o.modifiers.new('b', 'BEVEL'); md.width = min(r, depth) * 0.3; md.segments = 4; md.limit_method = 'ANGLE'
    return _fin(o, mat, parent)
def torus(loc, R, r, mat=None, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=48, minor_segments=16)
    return _fin(bpy.context.object, mat, parent)
def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); sc.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o
def K(o, path, t, v, interp=None):
    setattr(o, path, v); o.keyframe_insert(path, frame=F(t))
def light(kind, loc, energy, color=(1, 1, 1), size=3, target=(0, 0, 1)):
    d = bpy.data.lights.new(kind, kind); d.energy = energy; d.color = color
    if kind == 'AREA': d.size = size
    o = bpy.data.objects.new(kind, d); sc.collection.objects.link(o); o.location = loc
    tr = o.constraints.new('TRACK_TO'); tr.target = empty('lt', target); tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'
    return o
def camera(loc, target, lens=50, fstop=2.8):
    d = bpy.data.cameras.new('cam'); d.lens = lens; d.dof.use_dof = True; d.dof.aperture_fstop = fstop
    o = bpy.data.objects.new('cam', d); sc.collection.objects.link(o); o.location = loc; sc.camera = o
    t = empty('camtarget', target); tr = o.constraints.new('TRACK_TO'); tr.target = t
    tr.track_axis = 'TRACK_NEGATIVE_Z'; tr.up_axis = 'UP_Y'; d.dof.focus_object = t
    return o, t

# ------------------------------------------------------------------ Bopi
class Bopi:
    """Chubby baby dinosaur. Faces -Y (towards the camera). Rig = empties that shots animate."""
    def __init__(self, loc=(0, 0, 0)):
        mint = toon('mint', MINT); belly = toon('belly', BELLY); spike = toon('spike', SPIKE, coat=0.6)
        white = toon('white', WHITE, rough=0.15, sss=0.0, coat=0.8); black = toon('black', BLACK, rough=0.1, sss=0, coat=1.0)
        pink = toon('pink', PINK, rough=0.6); mouthm = toon('mouth', MOUTH, rough=0.6, sss=0); tongue = toon('tongue', TONGUE, rough=0.4)
        hl = toon('hl', WHITE, emit=6.0)
        self.root = empty('bopi', loc)
        self.body = empty('body', (0, 0, 0), self.root)            # squash / stretch pivot at the feet
        b = self.body
        sphere((0, 0, 0.62), 0.55, (1.0, 0.92, 1.05), mint, b)                       # torso
        sphere((0, -0.33, 0.56), 0.40, (0.85, 0.48, 0.95), belly, b)                 # belly
        for x in (-0.26, 0.26):                                                      # feet
            sphere((x, -0.12, 0.12), 0.2, (1, 1.25, 0.65), mint, b)
            for k in (-1, 0, 1): sphere((x + k * 0.07, -0.35, 0.1), 0.045, (1, 1, 0.8), white, b)   # toe claws
        tail = cone((0, 0.55, 0.35), 0.26, 0.02, 0.75, mint, b, rot=(math.radians(-70), 0, 0))
        for i, (y, z, s) in enumerate([(0.35, 1.0, 0.13), (0.5, 0.78, 0.12), (0.6, 0.55, 0.1), (0.75, 0.38, 0.08)]):
            cone((0, y, z), s, 0.0, s * 1.6, spike, b, rot=(math.radians(-40 - i * 12), 0, 0))
        # arms (shoulder empties rotate)
        self.armL = empty('armL', (0.44, -0.08, 0.85), b); self.armR = empty('armR', (-0.44, -0.08, 0.85), b)
        for a, sx in ((self.armL, 1), (self.armR, -1)):
            sphere((sx * 0.07, -0.02, -0.14), 0.13, (0.8, 0.8, 1.55), mint, a, rot=(0, math.radians(sx * 20), 0))
        self.handR = empty('handR', (-0.2, -0.1, -0.3), self.armR)
        # head
        self.head = empty('head', (0, 0, 1.05), b)
        h = self.head
        sphere((0, 0, 0.42), 0.5, (1.05, 0.95, 0.92), mint, h)                       # skull
        sphere((0, -0.33, 0.30), 0.34, (1.05, 0.75, 0.62), mint, h)                  # snout
        for i, (y, z, s) in enumerate([(-0.1, 0.93, 0.11), (0.12, 0.93, 0.14), (0.32, 0.82, 0.13), (0.45, 0.62, 0.11)]):
            cone((0, y, z), s, 0.0, s * 2.0, spike, h, rot=(math.radians(-5 - i * 28), 0, 0))
        for x in (-0.07, 0.07): sphere((x, -0.6, 0.36), 0.025, (1, 0.6, 1), toon('nostril', (0.12, 0.4, 0.2)), h)
        for x in (-0.36, 0.36): sphere((x, -0.38, 0.22), 0.09, (1, 0.4, 0.7), pink, h)   # cheeks (blush)
        self.cheeks = []
        for x in (-0.27, 0.27):   # puffable cheeks for swishing (hidden inside until puffed)
            c = sphere((x, -0.35, 0.22), 0.15, (0.4, 0.4, 0.4), mint, h); self.cheeks.append(c)
        # eyes
        self.eyes = []
        for x in (-0.19, 0.19):
            e = empty('eye', (x, -0.33, 0.58), h)
            sphere((0, 0, 0), 0.16, (1, 0.8, 1.1), white, e)
            sphere((0, -0.1, -0.01), 0.1, (1, 0.6, 1.1), toon('iris', (0.35, 0.18, 0.06), rough=0.1, sss=0, coat=1.0), e)
            sphere((0, -0.135, -0.01), 0.062, (1, 0.6, 1.1), black, e)
            sphere((-0.035, -0.17, 0.05), 0.03, (1, 0.6, 1), hl, e)
            sphere((0.03, -0.17, -0.04), 0.015, (1, 0.6, 1), hl, e)
            self.eyes.append(e)
        for x, rz in ((-0.19, 12), (0.19, -12)):   # eyebrows
            self.brow = cube((x, -0.36, 0.8), (0.12, 0.03, 0.025), toon('brow', (0.12, 0.45, 0.25)), h, bevel=0.012, rot=(0, math.radians(rz), 0))
        # mouth (open/close by scaling the mouth empty in Z)
        self.mouth = empty('mouth', (0, -0.6, 0.16), h)
        sphere((0, 0, 0), 0.17, (1.25, 0.3, 0.5), mouthm, self.mouth)
        sphere((0, -0.02, -0.04), 0.1, (1.2, 0.3, 0.35), tongue, self.mouth)
        self.teeth = []
        for k, x in enumerate((-0.13, -0.045, 0.045, 0.13)):
            t = cube((x, -0.045, 0.055), (0.07, 0.03, 0.05), white, self.mouth, bevel=0.012); self.teeth.append(t)
        self.mouth.scale = (1, 1, 0.35)
        self.sparkle_pt = (0.0, -0.7, 0.2)

    def bounce(self, t0, t1, every=0.5, h=0.06, sway=4):
        t = t0; i = 0
        while t <= t1 + 1e-6:
            K(self.body, 'location', t, (0, 0, 0)); K(self.body, 'scale', t, (1.05, 1.05, 0.93))
            if t + every / 2 <= t1:
                K(self.body, 'location', t + every / 2, (0, 0, h)); K(self.body, 'scale', t + every / 2, (0.97, 0.97, 1.04))
            K(self.head, 'rotation_euler', t, (0, math.radians(sway * (1 if i % 2 else -1)), 0))
            t += every; i += 1
    def blink(self, t):
        for e in self.eyes:
            K(e, 'scale', t - 0.05, (1, 1, 1)); K(e, 'scale', t + 0.03, (1, 1, 0.08)); K(e, 'scale', t + 0.12, (1, 1, 1))
    def mouth_open(self, t, amt):
        K(self.mouth, 'scale', t, (1 + amt * 0.1, 1, 0.35 + amt * 0.9))
    def sing(self, t0, t1, rate=0.25):
        t = t0; k = 0
        while t < t1:
            self.mouth_open(t, 0.65 if k % 2 == 0 else 0.15); t += rate; k += 1
        self.mouth_open(t1, 0.1)

def toothbrush(parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = empty('brush', loc, parent); e.rotation_euler = rot
    cyl((0, 0, 0), 0.045, 0.8, toon('brushh', BRUSH, coat=0.9), e)
    cube((0, -0.03, 0.38), (0.07, 0.06, 0.12), toon('brushhead', BRUSH, coat=0.9), e, bevel=0.02)
    for k in range(3):
        for j in range(2):
            cyl((-0.02 + j * 0.04, -0.08, 0.34 + k * 0.035), 0.012, 0.06, toon('bristle', WHITE), e, rot=(math.radians(90), 0, 0))
    cube((0, -0.1, 0.38), (0.06, 0.04, 0.09), toon('paste', (0.4, 0.85, 1.0), rough=0.6), e, bevel=0.02)   # toothpaste blob
    return e
def germ(loc, parent=None, s=1.0):
    e = empty('germ', loc, parent); e.scale = (s, s, s)
    sphere((0, 0, 0), 0.05, (1, 1, 1), toon('germ', GERM, rough=0.5), e, seg=24)
    for k in range(6):
        a = k * math.pi / 3
        cone((0.055 * math.cos(a), 0, 0.055 * math.sin(a)), 0.015, 0.0, 0.03, toon('germ', GERM), e, rot=(0, -a + math.pi / 2, 0))
    for x in (-0.017, 0.017):
        sphere((x, -0.042, 0.012), 0.014, (1, 1, 1), toon('white', WHITE), e, seg=16)
        sphere((x, -0.054, 0.012), 0.007, (1, 1, 1), toon('black', BLACK), e, seg=12)
    return e
def bubble(loc, r, parent=None):
    return sphere(loc, r, (1, 1, 1), bubble_mat(), parent, seg=32)

def bathroom(mirror=True):
    wall = cube((0, 2.0, 2.5), (12, 0.2, 8), tiles_mat(), bevel=0); wall.data.materials.clear(); wall.data.materials.append(tiles_mat())
    floor = cube((0, 0, -0.05), (12, 8, 0.1), toon('floor', (0.95, 0.6, 0.7), rough=0.3), bevel=0)
    cube((2.2, 1.4, 0.55), (1.6, 1.0, 1.1), toon('cabinet', (1.0, 1.0, 1.0), rough=0.3), bevel=0.08)   # sink cabinet
    cube((2.2, 1.4, 1.13), (1.8, 1.1, 0.08), toon('counter', (0.98, 0.7, 0.75), rough=0.25), bevel=0.03)
    sphere((2.2, 1.35, 1.17), 0.4, (1.2, 0.9, 0.25), toon('basin', WHITE, rough=0.1), None)
    cyl((2.2, 1.85, 1.35), 0.04, 0.4, toon('chrome', (0.9, 0.9, 0.95), rough=0.1, metal=1.0))
    sphere((1.65, 1.2, 1.25), 0.12, (1, 1, 1.1), toon('duck', DUCK), None)                   # rubber duck
    sphere((1.65, 1.1, 1.37), 0.08, (1, 1, 1), toon('duck', DUCK), None)
    cone((1.65, 1.0, 1.36), 0.035, 0.0, 0.07, toon('beak', (1, 0.5, 0.1)), None, rot=(math.radians(90), 0, 0))
    cyl((2.7, 1.2, 1.3), 0.1, 0.25, toon('cup', (1.0, 0.55, 0.75), coat=0.8))                # cup
    if mirror:
        torus((2.2, 1.88, 2.3), 0.6, 0.06, toon('frame', (1.0, 0.8, 0.3), coat=0.8), None, rot=(math.radians(90), 0, 0))
        cyl((2.2, 1.9, 2.3), 0.58, 0.02, toon('mirror', (0.8, 0.9, 0.95), rough=0.02, metal=1.0), None, rot=(math.radians(90), 0, 0))
    # bath mat + towel ring for colour accents
    cyl((0, -0.1, 0.005), 0.9, 0.02, toon('mat', (1.0, 0.65, 0.3), rough=0.9), None)
    torus((-2.0, 1.88, 2.0), 0.25, 0.03, toon('chrome', (0.9, 0.9, 0.95), rough=0.1, metal=1.0), None, rot=(math.radians(90), 0, 0))
    cube((-2.0, 1.8, 1.55), (0.5, 0.06, 0.7), toon('towel', (1.0, 0.85, 0.3), rough=0.9), bevel=0.05)
    for x, z, c in ((-3.0, 3.2, (1, 0.6, 0.7)), (-1.2, 3.6, (1, 0.9, 0.4)), (3.6, 3.4, (0.6, 1, 0.7))):   # wall stars (stickers)
        cone((x, 1.88, z), 0.2, 0.2, 0.02, toon(f'st{x}', c, rough=0.5), None, rot=(math.radians(90), 0, 0))

def lights(key=220, warm=(1, 0.92, 0.82)):
    light('AREA', (-2.5, -4.0, 4.0), key, warm, 4, (0, 0, 1.2))
    light('AREA', (3.5, -3.0, 2.0), key * 0.35, (0.8, 0.9, 1.0), 4, (0, 0, 1.2))
    light('AREA', (0.5, 1.2, 3.2), key * 0.7, (1.0, 0.95, 0.9), 2, (0, 0, 1.4))    # rim light: glossy outline

# ------------------------------------------------------------------ shots
bathroom(); lights()
bopi = Bopi((0, 0, 0))
MOUTH_W = lambda: bopi.mouth.matrix_world.translation

if SHOT == 'S1':   # HOOK: extreme close-up, mouth wide open, purple sugar bugs dancing on the teeth. "Oh no! Sugar bugs!"
    cam, tgt = camera((0.0, -3.0, 1.45), (0, -0.6, 1.4), lens=60, fstop=4)
    K(cam, 'location', 0, (0.0, -3.1, 1.45)); K(cam, 'location', 2.5, (0.0, -2.6, 1.42))       # push-in
    bopi.mouth_open(0, 1.0); bopi.mouth_open(0.3, 1.1); bopi.mouth_open(1.1, 0.8); bopi.mouth_open(1.4, 1.1); bopi.mouth_open(2.5, 1.0)
    for e in bopi.eyes: K(e, 'scale', 0, (1.15, 1.15, 1.25)); K(e, 'scale', 0.3, (1.25, 1.25, 1.35)); K(e, 'scale', 2.5, (1.2, 1.2, 1.3))
    K(bopi.head, 'rotation_euler', 0, (math.radians(-8), 0, 0)); K(bopi.head, 'rotation_euler', 0.4, (math.radians(-12), 0, math.radians(4)))
    K(bopi.head, 'rotation_euler', 1.2, (math.radians(-10), 0, math.radians(-4))); K(bopi.head, 'rotation_euler', 2.5, (math.radians(-12), 0, 0))
    for k, x in enumerate((-0.12, -0.04, 0.05, 0.13)):
        g = germ((x, -0.07, 0.0), bopi.mouth, 0.8)
        for j in range(6):
            t = j * 0.42 + k * 0.1
            K(g, 'location', t, (x, -0.07, -0.02)); K(g, 'location', t + 0.2, (x, -0.07, 0.06))
            K(g, 'rotation_euler', t, (0, 0, math.radians(15 * (1 if j % 2 else -1))))

elif SHOT == 'S2':  # toothbrush boings into Bopi's hand, he starts dancing. "Brush, brush, brush your teeth, Bopi brush your teeth!"
    cam, tgt = camera((0.3, -4.6, 1.3), (0, 0, 1.05), lens=45, fstop=4)
    K(cam, 'location', 0, (0.4, -4.8, 1.35)); K(cam, 'location', 4.0, (-0.2, -4.2, 1.25))
    br = toothbrush(bopi.handR, (0, -0.05, 0), (math.radians(10), 0, 0))
    K(br, 'scale', 0, (0.01, 0.01, 0.01)); K(br, 'scale', 0.15, (1.3, 1.3, 1.3)); K(br, 'scale', 0.3, (0.9, 0.9, 0.9)); K(br, 'scale', 0.45, (1, 1, 1))
    K(bopi.armR, 'rotation_euler', 0, (math.radians(-20), math.radians(-10), 0))
    for i in range(8):
        t = 0.5 + i * 0.5
        K(bopi.armR, 'rotation_euler', t, (math.radians(-90 + (20 if i % 2 else -10)), math.radians(-20), 0))
        K(bopi.armL, 'rotation_euler', t, (math.radians(-30 if i % 2 else 10), math.radians(10), 0))
        K(bopi.root, 'rotation_euler', t, (0, 0, math.radians(12 if i % 2 else -12)))
    bopi.bounce(0, 4.0, 0.5, 0.08, 6)
    bopi.sing(0.0, 4.0, 0.25); bopi.blink(1.6)

elif SHOT == 'S3':  # close-up brushing: up & down, then round & round, foam appears. "Up and down and round and round, make them shiny clean!"
    cam, tgt = camera((0.15, -3.0, 1.45), (0, -0.6, 1.4), lens=58, fstop=4)
    K(cam, 'location', 0, (0.3, -3.1, 1.45)); K(cam, 'location', 4.0, (-0.15, -2.7, 1.42))
    bopi.mouth_open(0, 0.25)
    for e in bopi.eyes: K(e, 'scale', 0, (1, 1, 0.75))    # happy squint
    br = toothbrush(None, (0.38, -0.7, 1.21), (0, math.radians(90), math.radians(180)))
    foam = []
    for k in range(9):
        a = k / 9 * 2 * math.pi
        f = sphere((0.2 * math.cos(a), -0.66, 1.2 + 0.07 * math.sin(a)), 0.05, (1, 1, 1), toon('foam', (1, 1, 1), rough=0.7, sss=0.5, coat=0), None, seg=20)
        K(f, 'scale', 0, (0, 0, 0)); K(f, 'scale', 0.4 + k * 0.25, (0, 0, 0)); K(f, 'scale', 0.6 + k * 0.25, (1.3, 1.3, 1.3)); K(f, 'scale', 0.8 + k * 0.25, (1, 1, 1))
    for i in range(8):   # up/down on each half beat for 2 s
        t = i * 0.25; K(br, 'location', t, (0.38 + 0.05 * (i % 3 - 1), -0.72, 1.27 if i % 2 else 1.15))
    for i in range(17):  # round and round
        t = 2.0 + i * 0.125; a = i * math.pi / 2
        K(br, 'location', t, (0.38 + 0.1 * math.cos(a), -0.72, 1.21 + 0.06 * math.sin(a)))
    K(bopi.head, 'rotation_euler', 0, (0, 0, 0))
    for i in range(8): K(bopi.head, 'rotation_euler', i * 0.5, (0, math.radians(5 if i % 2 else -5), 0))

elif SHOT == 'S4':  # sugar bugs pop away one by one. "Sugar bugs, go away! Scrub, scrub, scrub, hooray!"
    cam, tgt = camera((-0.3, -3.0, 1.45), (0, -0.6, 1.4), lens=60, fstop=4)
    K(cam, 'location', 0, (-0.35, -3.0, 1.45)); K(cam, 'location', 4.0, (0.25, -2.7, 1.42))
    bopi.mouth_open(0, 0.95); bopi.mouth_open(4.0, 0.95)
    br = toothbrush(None, (0.75, -0.72, 1.2), (0, math.radians(90), math.radians(180)))
    xs = (-0.12, -0.04, 0.05, 0.13, 0.0)
    for k, x in enumerate(xs):
        g = germ((x, -0.07, 0.0), bopi.mouth, 0.8)
        tp = 0.25 + k * 0.35 + (0.4 if k == 4 else 0)
        for j in range(8):
            t = j * 0.25
            if t < tp: K(g, 'location', t, (x, -0.07, -0.02 + (0.06 if j % 2 else 0)))
        K(g, 'scale', tp - 0.05, (0.9, 0.9, 0.9)); K(g, 'scale', tp + 0.04, (1.4, 1.4, 1.4)); K(g, 'scale', tp + 0.1, (0, 0, 0))
        K(br, 'location', tp - 0.15, (0.38 + x * 1.1, -0.72, 1.24)); K(br, 'location', tp, (0.43 + x * 1.1, -0.72, 1.18))
    K(br, 'location', 2.5, (0.25, -0.72, 1.22)); K(br, 'location', 3.0, (0.5, -0.72, 1.2)); K(br, 'location', 3.5, (0.25, -0.72, 1.22))
    K(br, 'location', 4.0, (0.9, -0.9, 1.0))
    for e in bopi.eyes: K(e, 'scale', 0, (1, 1, 1)); K(e, 'scale', 3.0, (1, 1, 1)); K(e, 'scale', 3.2, (1.1, 1.1, 0.6))   # "hooray" squint
    K(bopi.head, 'rotation_euler', 3.0, (0, 0, 0)); K(bopi.head, 'rotation_euler', 3.3, (math.radians(10), 0, 0))

elif SHOT == 'S5':  # bubbles float up, three pop on the beat. "Tiny bubbles, pop pop pop, brushing is the best!"
    cam, tgt = camera((0.0, -4.0, 1.4), (0, 0, 1.3), lens=42, fstop=5)
    K(cam, 'location', 0, (0.5, -4.0, 1.3)); K(cam, 'location', 4.0, (-0.4, -3.8, 1.5))
    br = toothbrush(bopi.handR, (0, -0.05, 0), (math.radians(10), 0, 0))
    bopi.bounce(0, 4.0, 0.5, 0.1, 6)
    K(bopi.armR, 'rotation_euler', 0, (math.radians(-80), math.radians(-20), 0))
    random.seed(5)
    for k in range(14):
        x = random.uniform(-1.2, 1.2); r = random.uniform(0.06, 0.16); y = random.uniform(-1.2, -0.3)
        b = bubble((x, y, 0.4), r)
        t0 = random.uniform(-1.5, 2.5)
        K(b, 'location', 0, (x, y, 0.5 + 0.55 * (0 - t0))); K(b, 'location', 4.0, (x + random.uniform(-0.3, 0.3), y, 0.5 + 0.55 * (4.0 - t0)))
    for j, (x, z) in enumerate(((-0.6, 1.9), (0.0, 2.2), (0.6, 1.9))):   # the three big bubbles
        b = bubble((x, -0.8, z), 0.24); tp = 1.0 + j * 0.25
        K(b, 'scale', 0, (0, 0, 0)); K(b, 'scale', 0.3 + j * 0.1, (1, 1, 1)); K(b, 'scale', tp - 0.03, (1, 1, 1))
        K(b, 'scale', tp + 0.03, (1.3, 1.3, 1.3)); K(b, 'scale', tp + 0.05, (0, 0, 0))
        K(bopi.armL, 'rotation_euler', tp - 0.1, (math.radians(-60), 0, math.radians(-20 + j * 20)))
        K(bopi.armL, 'rotation_euler', tp, (math.radians(-110), 0, math.radians(-20 + j * 20)))
    bopi.sing(0, 1.0, 0.25); bopi.sing(2.0, 4.0, 0.25)
    for k in range(3): bopi.mouth_open(1.0 + k * 0.25, 0.8); bopi.mouth_open(1.12 + k * 0.25, 0.2)
    bopi.blink(3.4)

elif SHOT == 'S6':  # swish with puffed cheeks, then "spit it out", count 1-2-3 with fingers. "Swish and swish and spit it out, one, two, three!"
    cam, tgt = camera((0.0, -3.0, 1.45), (0, 0, 1.4), lens=50, fstop=4)
    K(cam, 'location', 0, (0.0, -3.1, 1.45)); K(cam, 'location', 4.0, (0.0, -2.8, 1.45))
    bopi.mouth_open(0, 0.0)
    for i in range(5):
        t = i * 0.4
        for c, sgn in zip(bopi.cheeks, (-1, 1)):
            K(c, 'scale', t, (1.0, 0.9, 0.9) if (i % 2 == 0) == (sgn > 0) else (0.75, 0.75, 0.75))
        K(bopi.head, 'rotation_euler', t, (0, math.radians(8 if i % 2 else -8), 0))
    for c in bopi.cheeks: K(c, 'scale', 1.9, (0.4, 0.4, 0.4))
    bopi.mouth_open(1.9, 0.0); bopi.mouth_open(2.0, 0.9); bopi.mouth_open(2.3, 0.2)   # "spit"
    for k in range(7):
        d = sphere((0, -0.9, 1.25), 0.035, (1, 1, 1), bubble_mat(), None, seg=16)
        K(d, 'scale', 1.95, (0, 0, 0)); K(d, 'scale', 2.0, (1, 1, 1))
        K(d, 'location', 2.0, (0, -0.95, 1.22)); K(d, 'location', 2.5, (random.uniform(-0.4, 0.4), -1.4, 0.4))
    for j in range(3):   # count with the left arm on 1-2-3
        t = 2.0 + j * 0.5
        K(bopi.armL, 'rotation_euler', t, (math.radians(-40), 0, 0)); K(bopi.armL, 'rotation_euler', t + 0.15, (math.radians(-130), 0, 0))
        K(bopi.body, 'location', t, (0, 0, 0)); K(bopi.body, 'location', t + 0.15, (0, 0, 0.08))
    bopi.sing(2.0, 4.0, 0.5); bopi.blink(0.8)

elif SHOT == 'S7':  # big smile, tooth sparkle, wink. "Now give a great big smile, just like me!"
    cam, tgt = camera((0.0, -3.2, 1.45), (0, -0.6, 1.42), lens=58, fstop=4)
    K(cam, 'location', 0, (0.0, -3.3, 1.45)); K(cam, 'location', 4.0, (0.0, -2.7, 1.43))
    bopi.sing(0, 1.6, 0.25); bopi.mouth_open(1.7, 0.55); bopi.mouth_open(4.0, 0.55)
    for t in bopi.teeth:
        m = t.data.materials[0]
    star = empty('star', (0.09, -0.7, 1.26))
    for k in range(4):
        cone((0, 0, 0), 0.03, 0.0, 0.22, toon('hl', WHITE, emit=6.0), star, rot=(math.radians(90), math.radians(k * 90), 0))
    K(star, 'scale', 0, (0, 0, 0)); K(star, 'scale', 1.75, (0, 0, 0)); K(star, 'scale', 1.9, (1.4, 1.4, 1.4)); K(star, 'scale', 2.3, (0.8, 0.8, 0.8)); K(star, 'scale', 2.5, (0, 0, 0))
    K(star, 'rotation_euler', 1.75, (0, math.radians(0), 0)); K(star, 'rotation_euler', 2.5, (0, math.radians(90), 0))
    e = bopi.eyes[1]   # wink on "me"
    K(e, 'scale', 2.9, (1, 1, 1)); K(e, 'scale', 3.05, (1.05, 1, 0.08)); K(e, 'scale', 3.6, (1.05, 1, 0.08)); K(e, 'scale', 3.75, (1, 1, 1))
    K(bopi.head, 'rotation_euler', 0, (0, 0, 0)); K(bopi.head, 'rotation_euler', 3.0, (0, math.radians(-8), 0))

elif SHOT == 'S8':  # wide dance, camera orbits. Final chorus: "Brush, brush, brush your teeth, Bopi brush your teeth!"
    cam, tgt = camera((0, -5.0, 1.4), (0, 0, 1.0), lens=38, fstop=5)
    for i in range(5):
        a = math.radians(-25 + i * 12.5); K(cam, 'location', i, (5.0 * math.sin(a), -5.0 * math.cos(a), 1.3 + 0.1 * (i % 2)))
    br = toothbrush(bopi.handR, (0, -0.05, 0), (math.radians(10), 0, 0))
    for i in range(9):
        t = i * 0.5
        K(bopi.armR, 'rotation_euler', t, (math.radians(-150 if i % 2 else -60), math.radians(-20), 0))
        K(bopi.armL, 'rotation_euler', t, (math.radians(-60 if i % 2 else -150), math.radians(20), 0))
        K(bopi.root, 'rotation_euler', t, (0, 0, math.radians(15 if i % 2 else -15)))
    bopi.bounce(0, 4.0, 0.5, 0.15, 8); bopi.sing(0, 4.0, 0.25)
    random.seed(8)
    for k in range(10):
        x = random.uniform(-1.6, 1.6); y = random.uniform(-1.0, 0.8); b = bubble((x, y, 0), random.uniform(0.07, 0.15))
        K(b, 'location', 0, (x, y, random.uniform(0.2, 1.5))); K(b, 'location', 4.0, (x, y, random.uniform(2.2, 3.2)))

elif SHOT == 'S9':  # close smile and jump, "shiny teeth, yay!", sparkles; last frame matches the opening close-up for a loop
    cam, tgt = camera((0.0, -3.4, 1.4), (0, 0, 1.4), lens=45, fstop=4)
    K(cam, 'location', 0, (0.0, -3.6, 1.4)); K(cam, 'location', 3.6, (0.0, -3.2, 1.45)); K(cam, 'location', 6.0, (0.0, -2.6, 1.42))
    K(tgt, 'location', 0, (0, 0, 1.4)); K(tgt, 'location', 4.0, (0, -0.4, 1.35)); K(tgt, 'location', 6.0, (0, -0.6, 1.28))
    bopi.bounce(0, 2.0, 0.5, 0.08, 6); bopi.sing(0, 2.0, 0.25)
    # "yay" jump at 2.0 s
    K(bopi.body, 'location', 2.0, (0, 0, 0)); K(bopi.body, 'scale', 2.0, (1.1, 1.1, 0.85))
    K(bopi.body, 'location', 2.35, (0, 0, 0.55)); K(bopi.body, 'scale', 2.35, (0.92, 0.92, 1.1))
    K(bopi.body, 'location', 2.75, (0, 0, 0)); K(bopi.body, 'scale', 2.75, (1.08, 1.08, 0.9)); K(bopi.body, 'scale', 2.95, (1, 1, 1))
    for a, s in ((bopi.armL, 1), (bopi.armR, -1)):
        K(a, 'rotation_euler', 2.0, (0, 0, 0)); K(a, 'rotation_euler', 2.3, (math.radians(-160), 0, math.radians(s * -25))); K(a, 'rotation_euler', 3.5, (math.radians(-160), 0, math.radians(s * -25)))
        K(a, 'rotation_euler', 4.2, (0, 0, 0))
    bopi.mouth_open(2.0, 1.0); bopi.mouth_open(3.4, 0.6); bopi.mouth_open(4.5, 0.6)
    for e in bopi.eyes: K(e, 'scale', 2.0, (1, 1, 1)); K(e, 'scale', 2.2, (1.1, 1.1, 0.55)); K(e, 'scale', 3.5, (1.1, 1.1, 0.55)); K(e, 'scale', 3.8, (1, 1, 1))
    random.seed(9)
    for k in range(16):   # confetti stars burst
        c = sphere((0, -0.5, 1.6), 0.05, (1, 1, 0.3), toon(f'cf{k%4}', [(1, 0.4, 0.5), (1, 0.85, 0.2), (0.3, 0.7, 1), (0.5, 1, 0.5)][k % 4], emit=0.6), None, seg=16)
        a = random.uniform(0, 2 * math.pi); r = random.uniform(0.8, 1.6)
        K(c, 'scale', 2.0, (0, 0, 0)); K(c, 'scale', 2.1, (1, 1, 1))
        K(c, 'location', 2.0, (0, -0.5, 1.6)); K(c, 'location', 2.6, (r * math.cos(a), -0.6 - random.uniform(0, 0.6), 1.6 + r * math.sin(a)))
        K(c, 'location', 4.5, (r * math.cos(a) * 1.2, -0.8, 0.0)); K(c, 'rotation_euler', 4.5, (random.uniform(0, 9), random.uniform(0, 9), 0))
    bopi.blink(5.0)

# ------------------------------------------------------------------ render
out = os.path.join(HERE, 'frames', SHOT); os.makedirs(out, exist_ok=True)
if PREVIEW:
    fr = int(ARGS[ARGS.index('preview') + 1]) if len(ARGS) > ARGS.index('preview') + 1 and ARGS[ARGS.index('preview') + 1].isdigit() else NF // 2
    sc.frame_set(fr); sc.render.filepath = os.path.join(HERE, 'preview', f'{SHOT}_{fr:04d}.png')
    os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True); bpy.ops.render.render(write_still=True)
else:
    a, b = 1, NF
    if FR: a, b = map(int, FR[0].split('=')[1].split('-'))
    for f in range(a, b + 1):
        p = os.path.join(out, f'f_{f:04d}.png')
        if os.path.exists(p): continue
        sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
