"""Voiceover with word timings (ElevenLabs, key injected by the proxy).
Usage (inside a reel folder): python3 ../autopilot/voice.py script.txt ["phrase to time" ...]"""
import json, sys, urllib.request, base64
VOICE = 'nPczCjzI2devNBz1zQrb'  # channel voice, keep it the same for every reel
txt = open(sys.argv[1]).read().replace('\n', ' ').strip()
body = json.dumps({"text": txt, "model_id": "eleven_multilingual_v2",
                   "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "speed": 1.1}}).encode()
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps", data=body,
                             headers={"Content-Type": "application/json", "xi-api-key": "dummy"})
d = json.load(urllib.request.urlopen(req, timeout=120))
open('voice.mp3', 'wb').write(base64.b64decode(d['audio_base64']))
json.dump(d['alignment'], open('align.json', 'w'))
a = d['alignment']; t = ''.join(a['characters']); st = a['character_start_times_seconds']
for p in sys.argv[2:]:
    k = t.find(p); print(p, round(st[k], 2) if k >= 0 else 'NOT FOUND')
print('end', a['character_end_times_seconds'][-1])
