"""Generate the 8 shots with Higgsfield: Soul (image) -> DoP (image-to-video).
Skips shots that already exist, so it is safe to re-run. Then run assemble.py.
Usage: python3 generate_shots.py [shot ids...]   e.g. python3 generate_shots.py 01 05"""
import json, os, sys, time, urllib.request, urllib.error

BASE = 'https://platform.higgsfield.ai'
d = json.load(open('shots.json'))
only = set(sys.argv[1:])

def call(method, path, body=None):
    url = path if path.startswith('http') else f'{BASE}/{path}'
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method=method,
                                 headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{method} {url} -> HTTP {e.code}: {e.read()[:300].decode(errors="replace")}')

def find_url(obj, exts):
    """Find the first media URL in a response, wherever the API puts it."""
    if isinstance(obj, str):
        return obj if obj.startswith('http') and any(e in obj.lower() for e in exts) else None
    items = obj.values() if isinstance(obj, dict) else obj if isinstance(obj, list) else []
    for v in items:
        u = find_url(v, exts)
        if u: return u

def run(model, body, exts):
    r = call('POST', model, body)
    print('  submitted:', json.dumps(r)[:200])
    status_url = r.get('status_url') or f"{BASE}/requests/{r.get('request_id') or r.get('id')}/status"
    for _ in range(180):  # up to ~15 min
        s = call('GET', status_url)
        st = str(s.get('status', '')).lower()
        if st in ('completed', 'succeeded', 'success', 'done'):
            u = find_url(s, exts)
            if u: return u
            raise SystemExit(f'completed but no media URL: {json.dumps(s)[:400]}')
        if st in ('failed', 'error', 'nsfw', 'canceled', 'cancelled'):
            raise SystemExit(f'generation {st}: {json.dumps(s)[:400]}')
        time.sleep(5)
    raise SystemExit('timed out')

os.makedirs('img', exist_ok=True); os.makedirs('shots', exist_ok=True)
for s in d['shots']:
    sid = s['id']
    if only and sid not in only: continue
    if os.path.exists(f'shots/{sid}.mp4'): print(sid, 'exists, skip'); continue
    print('shot', sid)
    meta = f'img/{sid}.json'
    if os.path.exists(meta):
        img_url = json.load(open(meta))['url']
    else:
        prompt = s['img'].replace('{cat}', d['cat']) + ', ' + d['style']
        img_url = run('higgsfield-ai/soul/standard', {'prompt': prompt, 'aspect_ratio': '9:16', 'resolution': '1080p'}, ('.png', '.jpg', '.jpeg', '.webp'))
        json.dump({'url': img_url}, open(meta, 'w'))
        urllib.request.urlretrieve(img_url, f'img/{sid}.png')
    motion = s['move'] + ', claymation stop-motion animation, plasticine textures, slightly choppy handmade motion'
    vid_url = run('higgsfield-ai/dop/standard', {'prompt': motion, 'image_url': img_url}, ('.mp4', '.mov', '.webm'))
    urllib.request.urlretrieve(vid_url, f'shots/{sid}.mp4')
    print('  saved', f'shots/{sid}.mp4')
print('done — now run: python3 build_audio.py && python3 assemble.py')
