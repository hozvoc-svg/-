"""Synth music bed (dark phonk/trap, 140bpm) + SFX, then mix per short with VO. Writes audio/<id>_mix.wav and audio/<id>_events.json"""
import numpy as np, json, subprocess, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=44100; rng=np.random.default_rng(7)
def t(d): return np.arange(int(d*SR))/SR
def lp(x,f): return sosfilt(butter(4,f,'low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(4,f,'high',fs=SR,output='sos'),x)
def add(b,x,at,g=1.0):
    i=int(at*SR); x=x[:max(0,len(b)-i)]; b[i:i+len(x)]+=g*x
def load(p):
    r=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True); return np.frombuffer(r.stdout,np.float32).copy()
# --- sfx
def whoosh(d=0.5):
    n=rng.uniform(-1,1,int(d*SR)); x=t(d); e=np.sin(np.pi*x/d)**2
    out=np.zeros_like(n)
    for i,f in enumerate(np.linspace(300,4000,8)): out+=sosfilt(butter(2,[f*0.8,f*1.2],'band',fs=SR,output='sos'),n)*np.exp(-((x/d-i/8)**2)/0.02)
    return out*e*1.5
def boom(d=1.4):
    x=t(d); f=120*np.exp(-x*6)+38; ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(2.5*np.sin(ph)*np.exp(-x*2.2))+lp(rng.uniform(-1,1,len(x)),400)*np.exp(-x*9)*0.6
def riser(d=2.0):
    x=t(d); f=200+1800*(x/d)**2; ph=2*np.pi*np.cumsum(f)/SR
    return (0.3*np.sign(np.sin(ph))*0.4+hp(rng.uniform(-1,1,len(x)),2000)*0.5)*(x/d)**2
def pop(d=0.18):
    x=t(d); f=600+1400*np.exp(-x*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*25)
def glitch(d=0.25):
    x=t(d); s=np.sign(np.sin(2*np.pi*np.repeat(rng.uniform(80,1200,10),len(x)//10+1)[:len(x)]*x)); return s*0.5*(rng.uniform(size=len(x))>0.3)
# --- music: 140bpm phonk-ish
BPM=140; B=60/BPM
def kick(): x=t(0.5); return np.tanh(3*np.sin(2*np.pi*np.cumsum(50+150*np.exp(-x*35))/SR)*np.exp(-x*7))
def snare(): x=t(0.3); return (hp(rng.uniform(-1,1,len(x)),1500)*0.8+np.sin(2*np.pi*190*x)*0.5)*np.exp(-x*18)
def hat(o=False): x=t(0.25 if o else 0.06); return hp(rng.uniform(-1,1,len(x)),7000)*np.exp(-x*(12 if o else 70))
def cowbell(f):
    x=t(0.35); s=np.sign(np.sin(2*np.pi*f*x))+np.sign(np.sin(2*np.pi*f*1.48*x)); return lp(s,3000)*np.exp(-x*9)*0.35
def b808(f,d):
    x=t(d); return np.tanh(2*np.sin(2*np.pi*f*x)*np.minimum(1,np.exp(-(x-0.05)*1.5)))
def music(dur):
    out=np.zeros(int((dur+2)*SR)); bars=int(dur/(4*B))+2
    notes=[55,55,52,50]; bell=[880,830.6,739.99,659.25,739.99,830.6,880,987.77]
    for bar in range(bars):
        t0=bar*4*B; root=notes[bar%4]
        for k in (0,1.5,2.5): add(out,kick(),t0+k*B,0.9)
        for k in (1,3): add(out,snare(),t0+k*B,0.6)
        for k in range(16): add(out,hat(k%8==7),t0+k*B/4,0.25 if k%2==0 else 0.15)
        if bar%2==1:
            for k in (3.5,3.625,3.75,3.875): add(out,hat(),t0+k*B,0.2)
        add(out,b808(root,1.4*B),t0,0.55); add(out,b808(root,0.9*B),t0+2.5*B,0.5)
        for k in range(8): add(out,cowbell(bell[(k+bar*3)%8]),t0+k*B/2,0.5)
    return out
def words(al):
    ch,st,en=al['characters'],al['character_start_times_seconds'],al['character_end_times_seconds']; W=[];cur='';s=None
    for c,a,b in zip(ch,st,en):
        if c==' ':
            if cur: W.append([cur,s,e]); cur=''
            continue
        if not cur: s=a
        cur+=c; e=b
    if cur: W.append([cur,s,e])
    return W
if __name__=='__main__':
    d=json.load(open('shorts.json'))
    for sh in d['shorts']:
        i=sh['id']; vo=load(f'audio/{i}_vo.mp3'); al=json.load(open(f'audio/{i}_align.json'))
        W=words(al); LEAD=0.0; dur=len(vo)/SR+1.2
        # sentence starts = cut points
        cuts=[0.0]+[W[k+1][1] for k in range(len(W)-1) if W[k][0][-1] in '.?!']
        mix=np.zeros(int((dur+0.5)*SR)); add(mix,vo,LEAD,1.0)
        m=music(dur); m=m[:len(mix)]; m=np.pad(m,(0,len(mix)-len(m)))
        # duck music under voice
        envv=np.convolve(np.abs(np.pad(vo,(int(LEAD*SR),0))),np.ones(4410)/4410,'same'); envv=np.pad(envv,(0,max(0,len(mix)-len(envv))))[:len(mix)]
        duck=1-0.55*np.clip(envv/0.05,0,1); mix+=m*0.32*duck
        add(mix,boom(),0.0,0.7); add(mix,riser(1.0),-0+max(0,cuts[1]-1.0) if len(cuts)>1 else 0,0.0)
        for c in cuts[1:]:
            add(mix,whoosh(0.45),max(0,c-0.3),0.35)
        # big moments: boom on 3rd and last-but-one sentences, glitch on others
        for k,c in enumerate(cuts[1:],1):
            if k in (2,len(cuts)-2): add(mix,boom(),c,0.45)
            elif k%2: add(mix,glitch(),c,0.12)
        add(mix,pop(),0.25,0.4)
        mix/=max(1e-6,np.max(np.abs(mix)))*1.05
        wavfile.write(f'audio/{i}_mix.wav',SR,(mix*32767).astype(np.int16))
        json.dump({'dur':dur,'cuts':cuts,'words':W},open(f'audio/{i}_events.json','w'))
        print(i,'dur',round(dur,2),'cuts',[round(c,2) for c in cuts])
