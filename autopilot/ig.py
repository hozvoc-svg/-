"""Instagram API (Instagram Login), free. The access token is injected by the session proxy for graph.instagram.com.

  python3 autopilot/ig.py check                                   -> account name, followers (tests the token)
  python3 autopilot/ig.py publish reelNN/video.mp4 reelNN/cover.png reelNN/caption.txt "topic"
        (files must already be pushed to GitHub: Instagram downloads them from raw.githubusercontent.com)
  python3 autopilot/ig.py stats                                   -> refresh stats of every reel in autopilot/log.json
"""
import json, sys, time, subprocess, urllib.request, urllib.parse, urllib.error, os, datetime

BASE = 'https://graph.instagram.com/v23.0/'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, 'autopilot', 'log.json')
REPO = 'hozvoc-svg/-'

def call(path, method='GET', **params):
    data = None; url = BASE + path
    if method == 'GET':
        if params: url += '?' + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method, headers={'Authorization': 'Bearer dummy'})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        raise SystemExit(f'Instagram API error {e.code} on {path}: {body}')

def load_log():
    return json.load(open(LOG)) if os.path.exists(LOG) else []

def save_log(log):
    json.dump(log, open(LOG, 'w'), indent=1, ensure_ascii=False)

def raw_url(rel):
    branch = subprocess.check_output(['git', '-C', ROOT, 'rev-parse', '--abbrev-ref', 'HEAD'], text=True).strip()
    return f'https://raw.githubusercontent.com/{REPO}/{branch}/{urllib.parse.quote(rel)}'

def check():
    me = call('me', fields='user_id,username,account_type,followers_count,media_count')
    print(json.dumps(me, indent=1))

def publish(video, cover, caption_file, topic):
    caption = open(os.path.join(ROOT, caption_file)).read().strip()
    me = call('me', fields='user_id,username')
    uid = me['user_id']
    cont = call(f'{uid}/media', 'POST', media_type='REELS', video_url=raw_url(video), cover_url=raw_url(cover),
                caption=caption, share_to_feed='true')
    cid = cont['id']; print('container', cid)
    for _ in range(60):  # up to ~10 minutes
        st = call(cid, fields='status_code,status')
        print('status', st.get('status_code'), st.get('status', ''))
        if st.get('status_code') == 'FINISHED': break
        if st.get('status_code') in ('ERROR', 'EXPIRED'): raise SystemExit('upload failed: ' + json.dumps(st))
        time.sleep(10)
    else:
        raise SystemExit('upload did not finish in 10 minutes')
    pub = call(f'{uid}/media_publish', 'POST', creation_id=cid)
    mid = pub['id']
    info = call(mid, fields='permalink,timestamp')
    log = load_log()
    log.append(dict(folder=os.path.dirname(video), topic=topic, media_id=mid, permalink=info.get('permalink'),
                    published=info.get('timestamp'), stats=[]))
    save_log(log)
    print('PUBLISHED', info.get('permalink'))

METRICS = ['views', 'reach', 'saved', 'shares', 'likes', 'comments', 'total_interactions',
           'ig_reels_avg_watch_time', 'ig_reels_video_view_total_time']

def insights(mid):
    out = {}
    try:
        d = call(f'{mid}/insights', metric=','.join(METRICS))
        for m in d.get('data', []): out[m['name']] = m['values'][0]['value'] if m.get('values') else m.get('total_value', {}).get('value')
    except SystemExit:
        for m in METRICS:  # some metrics may be unavailable: fetch one by one
            try:
                d = call(f'{mid}/insights', metric=m)
                for x in d.get('data', []): out[x['name']] = x['values'][0]['value'] if x.get('values') else None
            except SystemExit:
                pass
    if out.get('ig_reels_avg_watch_time') is not None: out['avg_watch_s'] = round(out['ig_reels_avg_watch_time'] / 1000, 1)
    return out

def stats():
    log = load_log()
    me = call('me', fields='username,followers_count,media_count')
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    print(f"@{me.get('username')}  followers: {me.get('followers_count')}  posts: {me.get('media_count')}")
    for r in log:
        if not r.get('media_id'): continue
        s = insights(r['media_id']); s['at'] = now
        r.setdefault('stats', []).append(s)
        print(f"{r['folder']:<8} {r['topic'][:40]:<40} views={s.get('views')} avg_watch={s.get('avg_watch_s')}s "
              f"shares={s.get('shares')} saves={s.get('saved')} likes={s.get('likes')} comments={s.get('comments')}")
    acc = dict(at=now, followers=me.get('followers_count'))
    hist = os.path.join(ROOT, 'autopilot', 'followers.json')
    h = json.load(open(hist)) if os.path.exists(hist) else []
    h.append(acc); json.dump(h, open(hist, 'w'), indent=1)
    save_log(log)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'check': check()
    elif cmd == 'publish': publish(*sys.argv[2:6])
    elif cmd == 'stats': stats()
    else: raise SystemExit(__doc__)
