"""Raccoon gamer mascot 'Rocco' rendered as transparent sprites (mouth 0/1/2 x eyes open/closed).
Run: /opt/bpyenv/bin/python mascot_blender.py [preview]"""
import bpy, math, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'img','sprites'); os.makedirs(OUT,exist_ok=True)
PREVIEW='preview' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'
sc.cycles.samples=24 if PREVIEW else 48; sc.cycles.use_denoising=True
sc.render.resolution_x=sc.render.resolution_y=800; sc.render.film_transparent=True
sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'
try: sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
except Exception: pass
w=bpy.data.worlds.new('W'); sc.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs[0].default_value=(0.05,0.03,0.08,1); w.node_tree.nodes['Background'].inputs[1].default_value=0.6
def P(b,n,v):
    for k in ([n] if isinstance(n,str) else n):
        if k in b.inputs: b.inputs[k].default_value=v; return
def mat(name,rgb,rough=0.5,sss=0.0,fur=0.0,metal=0.0,emit=0.0,coat=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    P(b,'Base Color',(*rgb,1)); P(b,'Roughness',rough); P(b,'Metallic',metal); P(b,['Subsurface Weight','Subsurface'],sss)
    P(b,['Coat Weight','Clearcoat'],coat)
    if emit: P(b,['Emission Color','Emission'],(*rgb,1)); P(b,'Emission Strength',emit)
    if fur:
        n=nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value=180; n.inputs['Detail'].default_value=6
        bm=nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value=fur
        nt.links.new(n.outputs['Fac'],bm.inputs['Height']); nt.links.new(bm.outputs['Normal'],b.inputs['Normal'])
    return m
def shirt_mat():
    m=mat('shirt',(0.95,0.35,0.55),rough=0.7); nt=m.node_tree; b=nt.nodes['Principled BSDF']
    v=nt.nodes.new('ShaderNodeTexVoronoi'); v.inputs['Scale'].default_value=7
    r=nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].position=0.18; r.color_ramp.elements[0].color=(0.05,0.8,0.75,1)
    r.color_ramp.elements[1].position=0.2; r.color_ramp.elements[1].color=(0.95,0.32,0.55,1)
    nt.links.new(v.outputs['Distance'],r.inputs[0]); nt.links.new(r.outputs['Color'],b.inputs['Base Color']); return m
GREY=mat('grey',(0.42,0.42,0.46),0.75,0.1,fur=0.35); LIGHT=mat('light',(0.9,0.88,0.85),0.75,0.15,fur=0.3)
BLACK=mat('black',(0.03,0.03,0.035),0.7,fur=0.25); EYEW=mat('eyew',(0.97,0.97,0.97),0.15,coat=1)
PUPIL=mat('pupil',(0.01,0.01,0.01),0.05,coat=1); NOSE=mat('nose',(0.02,0.02,0.02),0.2,coat=1)
MOUTH=mat('mouth',(0.25,0.03,0.05),0.6); TONGUE=mat('tongue',(0.95,0.4,0.45),0.4,0.3)
PLASTIC=mat('plastic',(0.06,0.06,0.07),0.35); TEAL=mat('teal',(0.0,0.85,0.8),0.3,emit=0.6)
LENS=mat('lens',(0.9,0.2,0.6),0.05,metal=0.6,coat=1); SHIRT=shirt_mat(); INNER=mat('inner',(0.9,0.6,0.65),0.6,0.3)
def fin(o,m,par=None):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=True
    if par: o.parent=par
    return o
def sph(loc,r,s=(1,1,1),m=GREY,par=None,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=r,location=loc,rotation=rot); o=bpy.context.object; o.scale=s; return fin(o,m,par)
def cone(loc,r1,r2,d,m,rot):
    bpy.ops.mesh.primitive_cone_add(vertices=40,radius1=r1,radius2=r2,depth=d,location=loc,rotation=rot); return fin(bpy.context.object,m)
def cyl(loc,r,d,m,rot):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=d,location=loc,rotation=rot); o=bpy.context.object
    b=o.modifiers.new('b','BEVEL'); b.width=min(r,d)*0.2; b.segments=3; return fin(o,m)
def torus(loc,R,r,m,rot):
    bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,location=loc,rotation=rot,major_segments=64); return fin(bpy.context.object,m)
H=1.6  # head centre z
# body + shirt
sph((0,0,0.35),0.85,(1.05,0.75,0.95),SHIRT)
sph((0,-0.55,0.95),0.22,(1.6,0.5,0.5),LIGHT)  # chest fur at collar
cone((-0.22,-0.62,0.95),0.18,0.0,0.32,SHIRT,(math.radians(80),0,math.radians(-35)))  # collar flaps
cone((0.22,-0.62,0.95),0.18,0.0,0.32,SHIRT,(math.radians(80),0,math.radians(35)))
# head
sph((0,0,H),0.72,(1.12,0.95,0.9),GREY)
sph((-0.55,-0.25,H-0.18),0.28,(1,0.8,0.9),LIGHT); sph((0.55,-0.25,H-0.18),0.28,(1,0.8,0.9),LIGHT)  # cheek fluff
sph((0,-0.58,H-0.2),0.32,(1.15,0.85,0.75),LIGHT)  # muzzle
sph((0,-0.86,H-0.08),0.09,(1.3,1,0.85),NOSE)
sph((0,-0.48,H+0.1),0.5,(1.45,0.5,0.42),BLACK)  # bandit mask
for s in (-1,1):
    sph((s*0.12,-0.62,H+0.38),0.14,(1.4,0.5,0.35),LIGHT,rot=(0,s*0.35,0))  # white brows
    cone((s*0.55,0.0,H+0.62),0.24,0.04,0.42,GREY,(math.radians(-10),s*math.radians(28),0))
    cone((s*0.53,-0.06,H+0.6),0.15,0.02,0.32,INNER,(math.radians(-10),s*math.radians(28),0))
# eyes
EYES=[]; LIDS=[]
for s in (-1,1):
    sph((s*0.27,-0.66,H+0.12),0.16,(1,0.6,1.1),EYEW)
    p=sph((s*0.25,-0.75,H+0.1),0.085,(1,0.5,1.1),PUPIL); sph((s*0.22,-0.79,H+0.15),0.025,(1,0.5,1),EYEW)
    LIDS.append(sph((s*0.27,-0.69,H+0.12),0.172,(1,0.6,1.1),BLACK))
# mouth variants
MOUTHS=[]
m0=sph((0,-0.83,H-0.34),0.09,(1.4,0.35,0.18),MOUTH)
m1=sph((0,-0.8,H-0.35),0.1,(1.2,0.4,0.55),MOUTH); t1=sph((0,-0.84,H-0.39),0.06,(1.2,0.4,0.4),TONGUE)
m2=sph((0,-0.79,H-0.38),0.12,(1.25,0.45,1.0),MOUTH); t2=sph((0,-0.86,H-0.46),0.075,(1.3,0.45,0.5),TONGUE)
MOUTHS=[[m0],[m1,t1],[m2,t2]]
# headset
torus((0,0.05,H+0.15),0.8,0.05,PLASTIC,(math.radians(90),0,0))
for s in (-1,1):
    cyl((s*0.8,0.0,H),0.24,0.16,PLASTIC,(0,math.radians(90),0)); torus((s*0.88,0.0,H),0.2,0.03,TEAL,(0,math.radians(90),0))
bpy.ops.curve.primitive_bezier_curve_add(location=(0,0,0)); c=bpy.context.object; sp=c.data.splines[0]
sp.bezier_points[0].co=(-0.85,-0.1,H-0.1); sp.bezier_points[0].handle_left=(-0.85,0,H); sp.bezier_points[0].handle_right=(-0.8,-0.4,H-0.35)
sp.bezier_points[1].co=(-0.3,-0.75,H-0.42); sp.bezier_points[1].handle_left=(-0.6,-0.65,H-0.45); sp.bezier_points[1].handle_right=(-0.2,-0.8,H-0.4)
c.data.bevel_depth=0.022; c.data.materials.append(PLASTIC)
sph((-0.27,-0.77,H-0.42),0.05,(1,1,1),TEAL)
# sunglasses on forehead
for s in (-1,1): sph((s*0.24,-0.55,H+0.58),0.15,(1.15,0.35,0.8),LENS,rot=(math.radians(-25),0,0))
cyl((0,-0.6,H+0.6),0.02,0.2,TEAL,(0,math.radians(90),0))
# arms
for s in (-1,1): sph((s*0.95,-0.1,0.45),0.28,(0.7,0.7,1.3),SHIRT,rot=(0,s*0.3,0))
# lights + camera
def light(loc,e,col,size):
    d=bpy.data.lights.new('l','AREA'); d.energy=e; d.color=col; d.size=size; o=bpy.data.objects.new('l',d); sc.collection.objects.link(o); o.location=loc
    t=bpy.data.objects.new('t',None); sc.collection.objects.link(t); t.location=(0,0,1.3)
    k=o.constraints.new('TRACK_TO'); k.target=t; k.track_axis='TRACK_NEGATIVE_Z'; k.up_axis='UP_Y'
light((2.5,-4,4),900,(1,0.95,0.9),3); light((-4,-1,2.5),700,(1,0.3,0.7),2); light((4,1.5,2.5),900,(0.1,0.9,1),2); light((0,4,3),500,(1,1,1),3)
cd=bpy.data.cameras.new('c'); cd.lens=55; cam=bpy.data.objects.new('c',cd); sc.collection.objects.link(cam); sc.camera=cam
cam.location=(1.6,-6.2,2.1); t=bpy.data.objects.new('ct',None); sc.collection.objects.link(t); t.location=(0,0,1.15)
k=cam.constraints.new('TRACK_TO'); k.target=t; k.track_axis='TRACK_NEGATIVE_Z'; k.up_axis='UP_Y'
def show(objs,v):
    for o in objs: o.hide_render=not v
combos=[(0,0)] if PREVIEW else [(m,e) for m in range(3) for e in range(2)]
for mi,ei in combos:
    for i,g in enumerate(MOUTHS): show(g,i==mi)
    show(LIDS,ei==1)
    sc.render.filepath=os.path.join(OUT,f'm{mi}_e{ei}.png'); bpy.ops.render.render(write_still=True); print('rendered',mi,ei,flush=True)
