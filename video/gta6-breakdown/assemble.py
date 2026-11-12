"""Assemble a Short: footage (clips/<id>.mp4 if present, else placeholder) + mascot + captions + mix.
Usage: python3 assemble.py <id> [--green]   -> out/<id>.mp4 or out/<id>_greenscreen.mp4
Footage: put a 16:9 or 9:16 clip at clips/<id>.mp4 (any length >= VO; extra is trimmed)."""
import json, os, sys, math, subprocess, numpy as np
from PIL import Image
sys.path.insert(0,'.'); from build_audio import load, SR
ID=sys.argv[1]; GREEN='--green' in sys.argv; FPS=30; W,H=1080,1920
ev=json.load(open(f'audio/{ID}_events.json')); DUR=ev['dur']; CUTS=ev['cuts']; WORDS=ev['words']
NF=int(DUR*FPS); os.makedirs('out',exist_ok=True); tmp=f'tmp_{ID}'; os.makedirs(f'{tmp}/m',exist_ok=True)
# ---- mascot frames (RGBA 640x640)
vo=load(f'audio/{ID}_vo.mp3'); hop=SR//FPS
rms=np.array([np.sqrt(np.mean(vo[i*hop:(i+1)*hop]**2)) if i*hop<len(vo) else 0 for i in range(NF)])
rms=np.convolve(rms,[0.25,0.5,0.25],'same'); thr=np.percentile(rms[rms>0.005],[35,75]) if (rms>0.005).any() else [1,1]
spr={(m,e):Image.open(f'img/sprites/m{m}_e{e}.png').convert('RGBA') for m in range(3) for e in range(2)}
S=640
for f in range(NF):
    tt=f/FPS; m=0 if rms[f]<thr[0]*0.6 else (1 if rms[f]<thr[1] else 2)
    e=1 if (tt%3.3)<0.1 or (tt%7.1)<0.1 else 0
    # pop-in with overshoot, bob, reaction tilt after cuts
    pin=min(1,tt/0.35); sc=1+0.25*math.sin(pin*math.pi)*(1-pin)+0.0 if pin<1 else 1
    sc*= (1-math.exp(-tt*12))
    since=min([tt-c for c in CUTS if tt>=c] or [9]); kick=math.exp(-since*8)
    sc*=1+0.08*kick; ang=8*kick*math.sin(since*25)*(1 if CUTS.index(max(c for c in CUTS if c<=tt))%2 else -1)+2*math.sin(tt*2.1)
    bob=int(10*math.sin(tt*4.2)+(-18*abs(math.sin(tt*9)) if m==2 else 0))
    im=spr[(m,e)].resize((max(1,int(S*sc)),)*2,Image.LANCZOS).rotate(ang,resample=Image.BICUBIC,expand=False)
    fr=Image.new('RGBA',(S,S+40)); fr.alpha_composite(im,((S-im.width)//2,(S+40-im.height)//2+bob+20 if im.height<=S+40 else 0))
    fr.save(f'{tmp}/m/{f:05d}.png',compress_level=1)
# ---- captions (ASS): 1-3 words, active word yellow & bigger
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
groups=[];g=[]
for w in WORDS:
    g.append(w)
    if len(g)==3 or w[0][-1] in '.?!,': groups.append(g); g=[]
if g: groups.append(g)
ass=['[Script Info]','ScriptType: v4.00+',f'PlayResX: {W}',f'PlayResY: {H}','','[V4+ Styles]',
'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
'Style: Cap,Inter Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,7,4,5,60,60,0,1',
'Style: Top,Inter Black,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,3,18,0,8,60,60,150,1',
'','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
for gi,g in enumerate(groups):
    end_g=groups[gi+1][0][1] if gi+1<len(groups) else g[-1][2]+0.4
    for k,w in enumerate(g):
        st=w[1]; en=g[k+1][1] if k+1<len(g) else end_g
        txt=' '.join(('{\\c&H00F5FF&\\fscx115\\fscy115}'+x[0].upper()+'{\\c&HFFFFFF&\\fscx100\\fscy100}') if j==k else x[0].upper() for j,x in enumerate(g))
        anim='{\\fad(0,0)\\t(0,80,\\fscx105\\fscy105)\\t(80,160,\\fscx100\\fscy100)}' if k==0 else ''
        ass.append(f'Dialogue: 1,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\pos(540,1010)}}{anim}{txt}')
title=json.load(open('shorts.json'))
ass.append(f'Dialogue: 0,{ts(0)},{ts(DUR)},Top,,0,0,0,,{{\\3c&H9B32FF&}}GTA 6 DETAILS YOU MISSED')
open(f'{tmp}/cap.ass','w').write('\n'.join(ass))
# ---- background
src=f'clips/{ID}.mp4'
zoom='+'.join(f'0.10*exp(-(t-{c:.2f})*5)*gte(t,{c:.2f})' for c in CUTS)
if GREEN:
    bg=f'color=c=0x00FF00:s={W}x{H}:r={FPS}:d={DUR}[bg]'; inp=[]
elif os.path.exists(src):
    inp=['-i',src]
    bg=(f'[2:v]trim=0:{DUR},setpts=PTS-STARTPTS,fps={FPS},scale=-2:{H},crop={W}:{H},'
        f"scale=w='{W}*(1.06+{zoom})':h=-2:eval=frame,crop={W}:{H}:x='(iw-{W})/2+8*sin(t*40)*exp(-mod(t,100))*0':y='(ih-{H})/2',"
        f"eq=contrast=1.12:saturation=1.25,vignette=PI/5[bg]")
else:
    inp=[]
    bg=(f'gradients=s={W}x{H}:c0=0x2a0845:c1=0xff2d95:c2=0x00e5ff:c3=0x120024:n=4:speed=0.02:r={FPS}:d={DUR},'
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='GTA VI FOOTAGE':fontsize=70:fontcolor=white@0.35:x=(w-tw)/2:y=700[bg]")
flash='+'.join(f'between(t,{c:.2f},{c+0.07:.2f})' for c in CUTS[1:])
fc=(f'{bg};[0:v]scale={460 if os.path.exists(src) and not GREEN else 600}:-1,format=rgba[mas];[bg][mas]overlay=x=W-w+10:y=H-h-120:shortest=0,'
    + ('' if GREEN else f"eq=brightness='0.35*({flash})':eval=frame,")
    + f"ass={tmp}/cap.ass,format=yuv420p[v]")
out=f'out/{ID}_greenscreen.mp4' if GREEN else f'out/{ID}.mp4'
cmd=['ffmpeg','-loglevel','error','-y','-framerate',str(FPS),'-i',f'{tmp}/m/%05d.png','-i',f'audio/{ID}_mix.wav']+inp
if 'gradients' in bg or GREEN: cmd=cmd
cmd+=['-filter_complex',fc,'-map','[v]','-map','1:a','-t',f'{DUR}','-c:v','libx264','-preset','medium','-crf','19','-profile:v','high',
      '-c:a','aac','-b:a','192k','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-movflags','+faststart',out]
if GREEN or 'gradients' in bg:
    cmd=[c for c in cmd]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.stderr[-1500:] if r.returncode else f'wrote {out}')
