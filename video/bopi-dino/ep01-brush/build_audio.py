"""Backing track + SFX + Bopi's hook line, mixed with audio/vocals.wav -> audio/mix.wav"""
import json, os, base64, urllib.request, numpy as np, soundfile as sf, librosa, pyworld as pw
from scipy.signal import butter, sosfilt
SR=44100; d=json.load(open('song.json')); B=60/d['bpm']; T0=d['start']; TR=d['transpose']
voc,_=librosa.load('audio/vocals.wav',sr=SR); TOTAL=T0+16*4*B+2.0; voc=np.pad(voc,(0,max(0,int(TOTAL*SR)-len(voc))))[:int(TOTAL*SR)]
rng=np.random.default_rng(3)
def t(x): return np.arange(int(x*SR))/SR
def env(n,a=0.005,r=0.2):
    e=np.ones(n);na=max(1,int(a*SR));e[:na]=np.linspace(0,1,na);nr=min(n,int(r*SR));e[-nr:]*=np.linspace(1,0,nr)**2;return e
def lp(x,f,o=4): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=4): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
def hz(m): return 440*2**((m+TR-69)/12)
def add(buf,x,at,g=1.0):
    i=int(at*SR)
    if i<0: x=x[-i:];i=0
    j=min(len(buf),i+len(x)); buf[i:j]+=g*x[:j-i]
def pluck(f,dur=0.5,bright=0.996):
    n=int(dur*SR);p=max(2,int(SR/f));b=rng.uniform(-1,1,p);o=np.zeros(n)
    for i in range(n): o[i]=b[i%p];b[i%p]=0.5*(b[i%p]+b[(i+1)%p])*bright
    return o*env(n,0.001,0.08)
def glock(f,dur=0.9):
    x=t(dur);s=sum(a*np.sin(2*np.pi*f*m*x)*np.exp(-x*k) for m,a,k in [(1,1,4),(2.76,.35,8),(5.4,.15,14)]);return s*env(len(x),0.001,0.1)
def kick():
    x=t(0.3);f=50+90*np.exp(-x*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*9)
def clap():
    x=t(0.18);n=rng.normal(0,1,len(x));e=np.exp(-x*30)
    for dt in (0.0,0.012,0.024): e+=np.roll(np.exp(-x*60),int(dt*SR))*0.6
    return bp(n,900,3500)*e*0.5
def shaker(): x=t(0.07);return hp(rng.normal(0,1,len(x)),6000)*np.exp(-x*50)*0.25
def pop(f=600):
    x=t(0.09);fr=f*(1+2.5*np.exp(-x*60));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-x*45)
def sparkle(dur=1.2):
    o=np.zeros(int(dur*SR))
    for i,m in enumerate([84,88,91,96,100,103]): add(o,glock(440*2**((m-69)/12),0.8),i*0.06,0.5)
    return o
def boing():
    x=t(0.5);f=220+180*np.sin(2*np.pi*9*x)*np.exp(-x*5);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*5)*0.6
def scrub(dur):
    x=t(dur);n=rng.normal(0,1,len(x));am=0.5+0.5*np.sin(2*np.pi*8*x)
    return bp(n,1500,6000)*am*0.18*env(len(x),0.05,0.1)
def whoosh(dur=0.5):
    x=t(dur);n=rng.normal(0,1,len(x));e=np.sin(np.pi*x/dur)**2;return bp(n,400,2500)*e*0.4
def gasp_sting():
    o=np.zeros(int(1.6*SR))
    for i,m in enumerate([79,75,72]): add(o,glock(440*2**((m-69)/12),0.7),i*0.14,0.6)
    return o
# chords per line (C-major numbers before transpose)
CH={'C':[60,64,67],'Am':[57,60,64],'F':[53,57,60],'G':[55,59,62]}
prog=['C','Am','F','C', 'F','F','C','G', 'C','G','F','G', 'C','Am','F','C']
music=np.zeros(int(TOTAL*SR)); sfx=np.zeros_like(music)
# --- hook 0..2.5: sting + whoosh + fill
add(sfx,gasp_sting(),0.0,0.7)
add(sfx,whoosh(0.4),2.05,0.8)
for k in range(4): add(music,clap(),2.0+k*0.125,0.35*(k+1)/4)
for li,cn in enumerate(prog):
    bar=T0+li*4*B; part=d['lines'][li]['part']; ch=CH[cn]; soft=(part=='bridge')
    for b in range(4):
        tb=bar+b*B
        if not soft or (li==11 and b>=2):
            if b in (0,2): add(music,kick(),tb,0.9)
        if b in (1,3): add(music,clap(),tb,0.55 if not soft else 0.3)
        for e in (0,0.5): add(music,shaker(),tb+e*B,0.6)
        root=ch[0]-12 if b%2==0 else ch[2]-24
        add(music,pluck(hz(root),0.45,0.995),tb,0.75)
        for k,m in enumerate(ch): add(music,pluck(hz(m+12),0.35),tb+0.5*B+k*0.012,0.28)   # off-beat uke strum
    if li==11:   # build-up into final chorus
        for k in range(8): add(music,clap(),bar+2*B+k*0.25*B,0.15+0.05*k)
# glockenspiel doubles melody in choruses
tb=T0
for li,L in enumerate(d['lines']):
    tb=T0+li*4*B
    for w,b,nt in L['notes']:
        ns=nt if isinstance(nt,list) else [nt]
        if L['part']=='chorus':
            for k,n in enumerate(ns): add(music,glock(hz(n+12),0.6),tb+k*b*B/len(ns),0.18)
        tb+=b*B
# ending chord + sparkle
END=T0+16*4*B
add(music,sum(pluck(hz(m),1.6,0.998) for m in [48,60,64,67,72]),END,0.5)
add(sfx,sparkle(1.4),END-0.2,0.9)
# SFX tied to the story
add(sfx,boing(),T0+0.05,0.5)                          # toothbrush pops in
add(sfx,scrub(7.5),T0+0.3,1.0)                         # brushing chorus 1
add(sfx,scrub(5.5),T0+8*B+0.2,0.8)                     # brushing verse
for k,o in enumerate([2,2.5,3]): add(sfx,pop(700+150*k),T0+6*4*B+o*B,0.8)   # pop pop pop
for k in range(5): add(sfx,pop(500+90*k),T0+4*4*B+0.25+k*0.35,0.5)          # sugar bugs pop away
add(sfx,whoosh(0.6),T0+8*4*B-0.3,0.5)                  # transition to bridge
add(sfx,sparkle(1.0),T0+10*4*B+3*B,0.6)                # "smile" sparkle
# Bopi hook line (cute pitched voice)
os.makedirs('audio/lines',exist_ok=True); hp_='audio/lines/hook.mp3'
if not os.path.exists(hp_):
    body={"text":"Oh no! Sugar bugs!","model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.35,"similarity_boost":0.8,"style":0.7}}
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{d['voice']}?output_format=mp3_44100_128",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
    open(hp_,'wb').write(urllib.request.urlopen(req,timeout=120).read())
x,_=librosa.load(hp_,sr=SR); x=x.astype(np.float64)
f0,tt=pw.harvest(x,SR,frame_period=5);sp=pw.cheaptrick(x,f0,tt,SR);ap=pw.d4c(x,f0,tt,SR)
fb=np.arange(sp.shape[1]); sp2=np.array([np.interp(fb/1.12,fb,r) for r in sp])   # smaller "vocal tract" -> cuter
hook=pw.synthesize(f0*1.35,np.ascontiguousarray(sp2),ap,SR,5); hook/=np.max(np.abs(hook))
add(sfx,hook,0.25,0.95)
sf.write('audio/hook_voice.wav',hook,SR)
# mix: duck music under vocals
mix=np.zeros_like(music); add(mix,voc,0,1.0)
venv=np.convolve(np.abs(voc),np.ones(2205)/2205,'same')
duck=1-0.35*np.clip(venv/0.05,0,1)
mix+=music*0.55*duck+sfx*0.8
mix=np.tanh(mix*1.2)/1.2
mix/=np.max(np.abs(mix))*1.05
sf.write('audio/mix.wav',np.stack([mix,mix],1),SR)
print('mix',round(len(mix)/SR,2),'s')
