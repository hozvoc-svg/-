import json,urllib.request
S={'whoosh':'fast cinematic whoosh transition','boom':'deep cinematic bass boom hit','riser':'short tension riser building up','glass':'glass shattering impact','pop':'cartoon pop bubble appear','record':'record scratch stop'}
for k,t in S.items():
    r=urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation',data=json.dumps({'text':t,'duration_seconds':1.5 if k!='riser' else 2.5}).encode(),headers={'Content-Type':'application/json','xi-api-key':'dummy'})
    try: open(f'audio/sfx_{k}.mp3','wb').write(urllib.request.urlopen(r,timeout=120).read()); print(k,'ok')
    except Exception as e: print(k,e, getattr(e,'read',lambda:b'')()[:200])
