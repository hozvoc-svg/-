import json, sys, time, urllib.request, urllib.error
BASE='https://platform.higgsfield.ai'
def call(m,p,b=None):
    u=p if p.startswith('http') else f'{BASE}/{p}'
    r=urllib.request.Request(u,data=json.dumps(b).encode() if b else None,method=m,headers={'Content-Type':'application/json','Accept':'application/json'})
    try: return json.load(urllib.request.urlopen(r,timeout=120))
    except urllib.error.HTTPError as e: raise SystemExit(f'{m} {u} -> {e.code}: {e.read()[:400].decode(errors="replace")}')
def find(o,ex):
    if isinstance(o,str): return o if o.startswith('http') and any(e in o.lower() for e in ex) else None
    for v in (o.values() if isinstance(o,dict) else o if isinstance(o,list) else []):
        x=find(v,ex)
        if x: return x
def run(model,body,ex):
    r=call('POST',model,body); print('submitted',json.dumps(r)[:200],flush=True)
    su=r.get('status_url') or f"{BASE}/requests/{r.get('request_id') or r.get('id')}/status"
    for _ in range(200):
        s=call('GET',su); st=str(s.get('status','')).lower()
        if st in('completed','succeeded','success','done'): return find(s,ex)
        if st in('failed','error','nsfw','canceled','cancelled'): raise SystemExit(json.dumps(s)[:400])
        time.sleep(5)
mode=sys.argv[1]
if mode=='img':
    p=open('mascot_prompt.txt').read().strip()
    for i in range(2):
        u=run('higgsfield-ai/soul/standard',{'prompt':p,'aspect_ratio':'1:1','resolution':'1080p'},('.png','.jpg','.jpeg','.webp'))
        urllib.request.urlretrieve(u,f'img/mascot_{i}.png'); json.dump({'url':u},open(f'img/mascot_{i}.json','w')); print('saved',i,u)
else:
    src,motion,out=sys.argv[2],sys.argv[3],sys.argv[4]
    u=run('higgsfield-ai/dop/standard',{'prompt':motion,'image_url':json.load(open(src))['url']},('.mp4','.mov','.webm'))
    urllib.request.urlretrieve(u,out); print('saved',out)
