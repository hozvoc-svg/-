"""Detect shots in clips/*.mp4 (vertical), score beauty, reject letterboxed/dark/blurry. -> shots.json"""
import subprocess, json, glob, re, numpy as np, sys
from PIL import Image, ImageFilter
def scenes(f):
    r=subprocess.run(['ffmpeg','-i',f,'-vf',"select='gt(scene,0.28)',showinfo",'-f','null','-'],capture_output=True,text=True).stderr
    ts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',r)]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    b=[0.0]+ts+[dur]; return [(b[i],b[i+1]) for i in range(len(b)-1) if b[i+1]-b[i]>=0.9]
def frame(f,t):
    r=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',f,'-frames:v','1','-vf','scale=270:480','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
    return np.frombuffer(r.stdout,np.uint8).reshape(480,270,3).astype(float)
def sharp(a):
    g=a.mean(2); return np.var(g[1:,:]-g[:-1,:])+np.var(g[:,1:]-g[:,:-1])
out=[]
for f in sorted(glob.glob('clips/t*_*.mp4')):
    for s,e in scenes(f):
        a=frame(f,(s+e)/2); top=a[:110]; mid=a[150:330]; bot=a[370:]
        split=bool((a.mean(2)[200:280].mean(1)<8).any() or (a.mean(2)[300:420].mean(1)<8).any() and not (a.mean(2)[160:175].mean(1)<8).any()); lb=sharp(top)<0.15*sharp(mid) or sharp(bot)<0.15*sharp(mid)   # blurred bands = letterboxed
        bright=a.mean(); sat=(a.max(2)-a.min(2)).mean(); sh=sharp(a)
        score=min(sh,400)/400*0.4+min(sat,90)/90*0.35+(1-abs(bright-110)/110)*0.25
        ok=bool(not split and not lb and bright>35 and sh>20); lb=bool(lb and not split)
        out.append(dict(src=f,start=round(s,2),end=round(e,2),score=round(float(score),3),ok=ok,lb=lb,bright=int(bright),sat=int(sat),sharp=int(sh)))
json.dump(out,open('shots.json','w'),indent=1)
for o in out: print(o['src'][6:],o['start'],o['end'],'OK' if o['ok'] else ('LB' if o['lb'] else 'bad'),o['score'],o['bright'],o['sharp'])
