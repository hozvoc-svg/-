"""Turn ElevenLabs speech into singing: TTS each line with word timestamps,
then re-time every word onto its beat and replace its pitch with the melody (WORLD vocoder).
Output: audio/vocals.wav (+ audio/words.json for captions)."""
import json, os, base64, urllib.request, numpy as np, pyworld as pw, librosa, soundfile as sf
SR=44100; d=json.load(open('song.json')); beat=60/d['bpm']; T=d['transpose']
os.makedirs('audio/lines',exist_ok=True)
def tts_ts(text,out):
    if os.path.exists(out+'.json'): return json.load(open(out+'.json'))
    body={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.6,"similarity_boost":0.8,"style":0.4}}
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{d['voice']}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
    r=json.load(urllib.request.urlopen(req,timeout=120))
    open(out+'.mp3','wb').write(base64.b64decode(r['audio_base64'])); json.dump(r['alignment'],open(out+'.json','w')); return r['alignment']
def word_spans(al):
    ch,st,en=al['characters'],al['character_start_times_seconds'],al['character_end_times_seconds']
    spans=[];cur=None
    for c,s,e in zip(ch,st,en):
        if c.isalpha() or c=="'":
            if cur is None: cur=[s,e]
            else: cur[1]=e
        elif cur: spans.append(cur);cur=None
    if cur: spans.append(cur)
    return spans
def midi2hz(m): return 440*2**((m-69)/12)
def sing_word(x, notes, dur):
    x=x.astype(np.float64)
    f0,t=pw.harvest(x,SR,f0_floor=80,f0_ceil=700,frame_period=5)
    sp=pw.cheaptrick(x,f0,t,SR); ap=pw.d4c(x,f0,t,SR)
    n=len(f0); m=max(2,int(dur/0.005))
    # keep the first consonant frames at natural speed, stretch the vowel part
    voiced=np.where(f0>0)[0]; on=voiced[0] if len(voiced) else 0; on=min(on,int(m*0.3))
    idx=np.concatenate([np.arange(on), np.linspace(on, n-1, m-on)]).astype(int)
    f0n=f0[idx].copy(); spn=sp[idx]; apn=ap[idx]
    vmask=f0n>0
    # target melody: syllables split evenly over voiced region
    tgt=np.zeros(m); seg=np.array_split(np.arange(m), len(notes))
    for s,nn in zip(seg,notes): tgt[s]=midi2hz(nn+T)
    # glide between notes + vibrato on long notes
    k=7; tgt=np.convolve(np.pad(tgt,(k,k),mode='edge'),np.ones(2*k+1)/(2*k+1),'valid')
    tt=np.arange(m)*0.005; vib=1+0.012*np.sin(2*np.pi*5.5*tt)*np.clip((tt-0.25)/0.2,0,1)
    f0s=np.where(vmask,tgt*vib,0)
    # fill short unvoiced gaps inside vowels so notes are sustained
    if vmask.any():
        a,b=np.where(vmask)[0][[0,-1]]; f0s[a:b+1]=np.where(f0s[a:b+1]>0,f0s[a:b+1],tgt[a:b+1]*vib[a:b+1])
    # brighten / cute formants slightly
    y=pw.synthesize(np.ascontiguousarray(f0s),np.ascontiguousarray(spn),np.ascontiguousarray(apn),SR,5)
    fade=int(0.012*SR); y[-fade:]*=np.linspace(1,0,fade); y[:64]*=np.linspace(0,1,64)
    return y
total=d['start']+len(d['lines'])*4*beat+3
out=np.zeros(int(total*SR)); words=[]
t0=d['start']
for i,L in enumerate(d['lines']):
    text=' '.join(w for w,_,_ in L['notes'])
    al=tts_ts(text,f'audio/lines/{i:02d}')
    x,_=librosa.load(f'audio/lines/{i:02d}.mp3',sr=SR)
    spans=word_spans(al)
    if len(spans)!=len(L['notes']): raise SystemExit(f'line {i}: {len(spans)} words vs {len(L["notes"])} notes: {text}')
    tb=t0
    for (w,b,nt),(s,e) in zip(L['notes'],spans):
        notes=nt if isinstance(nt,list) else [nt]
        seg=x[max(0,int((s-0.03)*SR)):int((e+0.05)*SR)]
        dur=b*beat*0.92
        y=sing_word(seg,notes,dur)
        i0=int(tb*SR); out[i0:i0+len(y)]+=y[:len(out)-i0]
        words.append({"w":w,"t":round(tb,3),"d":round(b*beat,3),"part":L['part']})
        tb+=b*beat
    t0+=4*beat
out/=np.max(np.abs(out))*1.1
sf.write('audio/vocals.wav',out,SR); json.dump(words,open('audio/words.json','w'),indent=0)
print('vocals', round(total,2),'s', len(words),'words')
