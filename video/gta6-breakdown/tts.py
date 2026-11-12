import json,base64,urllib.request,sys
d=json.load(open('shorts.json'))
for s in d['shorts']:
    body={'text':s['vo'],'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.35,'similarity_boost':0.8,'style':0.55,'use_speaker_boost':True}}
    r=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{d['voice']}/with-timestamps",data=json.dumps(body).encode(),headers={'Content-Type':'application/json','xi-api-key':'dummy'})
    j=json.load(urllib.request.urlopen(r,timeout=180))
    open(f"audio/{s['id']}_vo.mp3",'wb').write(base64.b64decode(j['audio_base64']))
    json.dump(j['alignment'],open(f"audio/{s['id']}_align.json",'w')); print(s['id'],'ok',j['alignment']['character_end_times_seconds'][-1])
