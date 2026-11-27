"""Music bed + SFX + voice -> final reel mp4 (-14 LUFS).
cues.json: {"chords": "minor"|"major", "sfx": [[time_or_phrase, "pop|ding|whoosh|buzz|thud|tick|crack", offset], ...]}
A cue time may be a phrase from the script; it is resolved through align.json.
Usage (inside a reel folder): python3 ../autopilot/mix.py cues.json out.mp4"""
import json, sys, wave, subprocess
import numpy as np
sr = 44100
cues = json.load(open(sys.argv[1])); out_mp4 = sys.argv[2]
a = json.load(open('align.json')); DUR = a['character_end_times_seconds'][-1] + 0.9
txt = ''.join(a['characters']); st = a['character_start_times_seconds']
n = int(sr * (DUR + 1)); rng = np.random.default_rng(0)
CH = {'minor': [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]],
      'major': [[261.6, 329.6, 392], [196, 246.9, 293.7], [220, 261.6, 329.6], [174.6, 220, 261.6]]}[cues.get('chords', 'minor')]
bed = np.zeros(n)
for i in range(int(DUR / 2) + 1):
    s = int(i * 2 * sr); e = min(n, s + int(2.3 * sr)); tt = np.arange(e - s) / sr
    env = np.minimum(1, tt / 0.4) * np.exp(-np.maximum(0, tt - 1.9) * 6)
    for f in CH[i % 4]: bed[s:e] += env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * 0.05
    for b in range(4):
        ks = s + int(b * 0.5 * sr); kt = np.arange(int(0.25 * sr)) / sr
        if ks + len(kt) < n: bed[ks:ks + len(kt)] += np.sin(2 * np.pi * (55 + 60 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 14) * 0.18
bed = np.convolve(bed, np.ones(6) / 6, 'same')
def T(n_): return np.arange(int(sr * n_)) / sr
def snd(kind):
    if kind == 'pop': t = T(0.09); return np.sin(2 * np.pi * rng.uniform(700, 1200) * t * (1 + 3 * t)) * np.exp(-t * 40) * 0.35
    if kind == 'ding': t = T(0.9); return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1977 * t)) * np.exp(-t * 5) * 0.22
    if kind == 'whoosh':
        m = int(sr * 0.5); x = rng.normal(0, 1, m); return np.convolve(x, np.ones(8) / 8, 'same') * np.sin(np.linspace(0, np.pi, m)) ** 2 * 0.18
    if kind == 'buzz': t = T(0.35); return np.sign(np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 8) * 0.08
    if kind == 'thud': t = T(0.25); return np.sin(2 * np.pi * 60 * t) * np.exp(-t * 20) * 0.6
    if kind == 'tick': t = T(0.03); return np.sin(2 * np.pi * 2000 * t) * np.exp(-t * 200) * 0.15
    if kind == 'crack': m = int(sr * 0.25); return rng.normal(0, 1, m) * np.exp(-np.arange(m) / sr * 25) * 0.25
    raise SystemExit('unknown sfx ' + kind)
sfx = np.zeros(n)
for at, kind, off in cues.get('sfx', []):
    if isinstance(at, str):
        k = txt.find(at)
        if k < 0: raise SystemExit('phrase not in script: ' + at)
        at = st[k]
    i = int((at + off) * sr); s_ = snd(kind)
    if 0 <= i < n: sfx[i:i + len(s_)] += s_[:n - i]
for name, sig in (('bed.wav', bed), ('sfx.wav', sfx)):
    w = wave.open(name, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(sig, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cartoon_video.mp4', '-i', 'voice.mp3', '-i', 'bed.wav', '-i', 'sfx.wav',
                '-filter_complex', '[2]volume=0.25[m];[3]volume=0.8[s];[1][m][s]amix=3:duration=first:normalize=0,apad=pad_dur=0.9,loudnorm=I=-14:TP=-1.5[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out_mp4], check=True)
print('ok', out_mp4)
