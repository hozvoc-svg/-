"""Pro montage (see ../STYLE.md). Usage: python3 assemble_pro.py <id> <src1,src2,...> [music_offset]
Beat-synced cuts over the best shots, cinematic grade, clean captions, calm mascot, real music."""
import json, os, sys, math, subprocess, numpy as np
from PIL import Image
sys.path.insert(0,'.'); from build_audio import load, SR
ID=sys.argv[1]; SRCS=sys.argv[2].split(','); MOFF=float(sys.argv[3]) if len(sys.argv)>3 else 3.5
FPS=30; W,H=1080,1920; tmp=f'tmpp_{ID}'; os.makedirs(f'{tmp}/m',exist_ok=True); os.makedirs('out',exist_ok=True)
ev=json.load(open(f'audio/{ID}_events.json')); WORDS=ev['words']
vo=load(f'audio/{ID}_vo.mp3'); DUR=round(len(vo)/SR+1.2,2); NF=int(DUR*FPS)
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: raise SystemExit(r.stderr[-1200:])
# ---- music onsets
mus=load('audio/music_synthwave.wav'); seg=mus[int(MOFF*SR):]
hop=512; e=np.array([np.sum(seg[i:i+hop]**2) for i in range(0,len(seg)-hop,hop)]); on=np.maximum(0,np.diff(np.log(e+1e-6)))
ot=np.arange(len(on))*hop/SR; peaks=[ot[i] for i in range(1,len(on)-1) if on[i]>on[i-1] and on[i]>=on[i+1] and on[i]>np.percentile(on,88)]
# ---- sentence-driven edit plan (edits.json: shot indices from shots_good.json per sentence)
G=json.load(open('shots_good.json')); plan=json.load(open('edits.json'))[ID]
sc=ev['cuts']+[DUR]
cuts=[];best=[];SENT=[]
for i,shots in enumerate(plan):
    a0,b0=sc[i],(sc[i+1] if i+1<len(sc) else DUR)
    if i==len(plan)-1: b0=DUR
    n=len(shots)
    for j,ix in enumerate(shots):
        c=a0+(b0-a0)*j/n
        if j>0 and peaks:
            p=min(peaks,key=lambda p:abs(p-c))
            if abs(p-c)<0.35: c=p
        cuts.append(c); best.append(G[ix]); SENT.append(j==0)
cuts.append(DUR); need=len(best)
def band(src,t):
    r=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',src,'-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True)
    a=np.frombuffer(r.stdout,np.uint8).reshape(1920,1080).astype(float); m=a.mean(1)
    up=[y for y in range(400,960) if m[y]<5]; dn=[y for y in range(960,1550) if m[y]<5]
    if not up or not dn: return 700,525
    y0=max(up)+4; y1=min(dn)-4; return y0,(y1-y0)//2*2
XT=0.25
GRADE=("colorbalance=rs=0.04:gs=-0.01:bs=-0.06:rm=0.03:bm=-0.03:rh=0.02:bh=0.05,"
       "curves=all='0/0.02 0.25/0.22 0.75/0.8 1/0.97',eq=contrast=1.08:saturation=1.18,noise=alls=5:allf=t,vignette=PI/5")
parts=[]
for k in range(need):
    s=best[k]; d=cuts[k+1]-cuts[k]+(XT if k<need-1 else 0); avail=s['end']-s['start']
    s0,s1=s['start']+0.08,s['end']-0.08; avail=s1-s0
    st=s0+max(0,(avail-d)/2) if avail>=d else s0
    take=min(avail,d); slow=min(2.5,d/take)
    push=f"scale=w='iw*(1.006+0.06*t/{d:.2f})':h=-2:eval=frame,crop={W if not s['lb'] else 1080}:{H if not s['lb'] else 525}"
    if s['lb']:
        y0,bh=band(s['src'],(s['start']+s['end'])/2)
        push=f"scale=w='iw*(1.006+0.06*t/{d:.2f})':h=-2:eval=frame,crop=1080:{bh}"
        v=(f"crop=1080:{bh}:0:{y0},{push},pad={W}:{H}:0:(oh-ih)/2:black")
    else:
        v=f"{push}"
    out=f'{tmp}/p{k:02d}.mp4'
    run(['ffmpeg','-y','-ss',f'{st:.2f}','-i',s['src'],'-t',f'{take:.2f}','-an','-vf',
         f"setpts={slow:.3f}*PTS,minterpolate=fps={FPS}:mi_mode=blend,{v},{GRADE},tpad=stop_mode=clone:stop_duration=3,setsar=1,format=yuv420p",'-t',f'{d:.3f}','-c:v','libx264','-crf','17','-preset','fast',out])
    parts.append(out)
# xfade chain: stylish transitions on sentence changes, near-hard cuts inside sentences
inp=[];fc=[];prev='0:v';acc=0.0
for p in parts: inp+=['-i',p]
TR=['zoomin', 'smoothleft', 'hblur', 'fadeblack', 'smoothup', 'circleopen']
for k in range(1,need):
    acc+=cuts[k]-cuts[k-1]
    tr,du=(TR[k%len(TR)],XT) if SENT[k] else ('fade',0.07)
    off=acc-(du/2)
    fc.append(f"[{prev}][{k}:v]xfade=transition={tr}:duration={du}:offset={off:.3f}[x{k}]"); prev=f'x{k}'
run(['ffmpeg','-y']+inp+['-filter_complex',';'.join(fc),'-map',f'[{prev}]','-t',f'{DUR}','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',f'{tmp}/video.mp4'])
# ---- calm mascot
hopv=SR//FPS; rms=np.array([np.sqrt(np.mean(vo[i*hopv:(i+1)*hopv]**2)) if i*hopv<len(vo) else 0 for i in range(NF)])
rms=np.convolve(rms,[0.25,0.5,0.25],'same'); th=np.percentile(rms[rms>0.005],[35,75])
spr={(m,e):Image.open(f'img/sprites/m{m}_e{e}.png').convert('RGBA').resize((360,360),Image.LANCZOS) for m in range(3) for e in range(2)}
for f in range(NF):
    tt=f/FPS; m=0 if rms[f]<th[0]*0.6 else (1 if rms[f]<th[1] else 2); e=1 if (tt%3.7)<0.1 else 0
    fr=Image.new('RGBA',(360,400)); a=min(1,tt/0.4)
    im=spr[(m,e)].copy(); im.putalpha(im.split()[3].point(lambda v:int(v*a)))
    fr.alpha_composite(im,(0,20+int(6*math.sin(tt*2.4)))); fr.save(f'{tmp}/m/{f:05d}.png',compress_level=1)
# ---- captions
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
groups=[];g=[]
for w in WORDS:
    g.append(w)
    if len(g)==4 or w[0][-1] in '.?!,': groups.append(g); g=[]
if g: groups.append(g)
ass=['[Script Info]','ScriptType: v4.00+',f'PlayResX: {W}',f'PlayResY: {H}','','[V4+ Styles]',
'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
'Style: Cap,Inter ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H64000000,&H96000000,1,0,0,0,100,100,1,0,1,2,3,5,80,80,0,1',
'Style: WM,Inter ExtraBold,34,&H40FFFFFF,&H40FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,7,60,60,90,1',
'','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
for gi,g in enumerate(groups):
    endg=groups[gi+1][0][1] if gi+1<len(groups) else g[-1][2]+0.4
    for k,w in enumerate(g):
        en=g[k+1][1] if k+1<len(g) else endg
        txt=' '.join(('{\\c&H9DB4FF&}'+x[0]+'{\\c&HFFFFFF&}') if j==k else x[0] for j,x in enumerate(g))
        fade='{\\fad(120,0)}' if k==0 else ''
        ass.append(f'Dialogue: 1,{ts(w[1])},{ts(en)},Cap,,0,0,0,,{{\\pos(540,1440)}}{fade}{txt}')
ass.append(f'Dialogue: 0,{ts(0)},{ts(DUR)},WM,,0,0,0,,ROCCO GTA')
open(f'{tmp}/cap.ass','w').write('\n'.join(ass))
# ---- audio: real music ducked under VO
fc=(f"[2:a]atrim={MOFF}:{MOFF+DUR},asetpts=PTS-STARTPTS,volume=0.55,afade=t=out:st={DUR-1.8}:d=1.8[m];"
    f"[3:a]apad,asplit=2[v][k];[m][k]sidechaincompress=threshold=0.03:ratio=6:attack=10:release=350[md];"
    f"[v][md]amix=inputs=2:duration=first:normalize=0,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5:LRA=11[a];"
    f"[1:v]scale=360:-1,format=rgba[mas];[0:v][mas]overlay=x=W-w-30:y=H-h-110,ass={tmp}/cap.ass,format=yuv420p[vout]")
out=f'out/{ID}_pro.mp4'
run(['ffmpeg','-y','-i',f'{tmp}/video.mp4','-framerate',str(FPS),'-i',f'{tmp}/m/%05d.png','-i','audio/music_synthwave.wav','-i',f'audio/{ID}_vo.mp3',
     '-filter_complex',fc,'-map','[vout]','-map','[a]','-t',f'{DUR}','-c:v','libx264','-crf','18','-preset','medium','-profile:v','high',
     '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out])
print('wrote',out,'cuts',len(cuts)-1,'dur',DUR)
