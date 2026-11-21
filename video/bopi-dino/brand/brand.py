"""Channel avatar (800x800) and banner art (2560x1440) of Bopi, reusing the ep01 character builder.
Run: /opt/bpyenv/bin/python brand/brand.py -- avatar|banner"""
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
WHAT = sys.argv[sys.argv.index('--') + 1]
src = open(os.path.join(HERE, '..', 'ep01-brush', 'bopi_scenes.py')).read()
src = src.split('# ------------------------------------------------------------------ shots')[0]
sys.argv = ['x', '--', 'S2']
exec(compile(src, 'bopi_scenes', 'exec'))
sc.cycles.samples = 48
for o in list(bpy.data.objects): bpy.data.objects.remove(o)   # no bathroom: clean studio colour
bg.inputs[0].default_value = (1.0, 0.85, 0.35, 1); bg.inputs[1].default_value = 0.9
lights(260)
bopi = Bopi((0, 0, 0))
bopi.mouth.scale = (1.15, 1, 1.1)                         # big open smile
for e in bopi.eyes: e.scale = (1.05, 1.05, 0.92)
bopi.armL.rotation_euler = (math.radians(-150), 0, math.radians(-20)); bopi.armR.rotation_euler = (math.radians(-150), 0, math.radians(20))
bopi.head.rotation_euler = (0, math.radians(-6), 0)
if WHAT == 'avatar':
    sc.render.resolution_x = sc.render.resolution_y = 800
    camera((0, -2.7, 1.55), (0, 0, 1.38), lens=50, fstop=8)
else:
    sc.render.resolution_x, sc.render.resolution_y = 2560, 1440
    bopi.root.location = (0, 0, 0)
    sc.render.resolution_x, sc.render.resolution_y = 1000, 1400
    camera((0, -5.0, 1.05), (0, 0, 1.05), lens=50, fstop=8)
sc.render.film_transparent = True
sc.render.filepath = os.path.join(HERE, f'{WHAT}_raw.png'); bpy.ops.render.render(write_still=True)
